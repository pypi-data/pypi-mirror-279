# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import unittest
import numpy as np
from shutil import rmtree

import qtealeaves as qtl
import qtealeaves.observables as obs
from qtealeaves.tensors import QteaTensor, TensorBackend
from qtealeaves.emulator.tn_simulation import run_tn_measurements
from qtealeaves.operators.spinoperators import TNSpin12Operators
from qtealeaves.emulator import TTN, MPS


class TestTNObservables(unittest.TestCase):
    def setUp(self):
        """
        Provide some default settings.
        """
        np.random.seed([11, 13, 17, 19])
        self.dtype = None
        self.device = None
        self.tensor_cls = None
        self.base_tensor_cls = None
        self._setup_types_devices()

        self.tensor_backend = TensorBackend(device=self.device, dtype=self.dtype)

        self.conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_bond_dimension=16, cut_ratio=1e-16, max_iter=10
        )
        self.ansatz = {5: TTN, 6: MPS}
        self.operators = self.base_tensor_cls.convert_operator_dict(
            TNSpin12Operators(),
            params={},
            symmetries=[],
            generators=[],
            base_tensor_cls=self.base_tensor_cls,
            dtype=self.dtype,
            device=self.device,
        )

        self.in_folder = "TEST_INPUT"
        self.out_folder = "TEST_OUTPUT"

    def _setup_types_devices(self):
        self.device = "cpu"
        self.dtype = np.complex128
        self.tensor_cls = QteaTensor
        self.base_tensor_cls = QteaTensor

    def tearDown(self):
        """
        Remove input and output folders again
        """
        if os.path.isdir(self.in_folder):
            rmtree(self.in_folder)
        if os.path.isdir(self.out_folder):
            rmtree(self.out_folder)

        return

    def _build_state(self):
        """
        Build GHZ state to use for measurement
        """
        state = np.zeros(2**8)
        state[0] = 1 / np.sqrt(2)
        state[-1] = 1 / np.sqrt(2)
        state = state.reshape([2] * 8)
        return state  # self.base_tensor_cls.from_elem_array(state, dtype=self.dtype, device=self.device)

    def run_measurements(self, observables, ansatz_id, obsv_id, requires_singvals=True):
        """Measure the given observables using the ghz state"""
        state = self.ansatz[ansatz_id].from_statevector(
            self._build_state(), tensor_backend=self.tensor_backend
        )
        # Compute singvals for bond_entropy
        if ansatz_id == 5:
            for tt in range(4):
                state.iso_towards(
                    (state.num_layers - 1, tt), keep_singvals=True, trunc=True
                )
            state.iso_towards((state.num_layers - 1, 0), keep_singvals=True, trunc=True)
        else:
            state.iso_towards(state.num_sites - 1, keep_singvals=True, trunc=True)
            state.iso_towards(0, keep_singvals=True, trunc=True)
        if state.is_measured[obsv_id]:
            observables = run_tn_measurements(
                state,
                observables,
                self.operators,
                {},
                self.tensor_backend,
                ansatz_id,
                requires_singvals,
            )
        else:
            observables = None
        return observables

    def test_rho_i(self):
        """test local density matrix, i.e., normalization."""
        for ansatz_id in self.ansatz:
            state = self.ansatz[ansatz_id].from_statevector(
                self._build_state(), tensor_backend=self.tensor_backend
            )

            if ansatz_id == 5:
                for tt in range(4):
                    state.iso_towards(
                        (state.num_layers - 1, tt), keep_singvals=True, trunc=True
                    )
                state.iso_towards(
                    (state.num_layers - 1, 0), keep_singvals=True, trunc=True
                )
            else:
                state.iso_towards(state.num_sites - 1, keep_singvals=True, trunc=True)
                state.iso_towards(0, keep_singvals=True, trunc=True)

            for ii in range(state.num_sites):
                rho_i = state.get_rho_i(ii)
                norm = rho_i.trace(do_get=True)
                eps = abs(1 - norm)

                msg = f"Failed on site {ii} for ansatz {ansatz_id}."
                self.assertLess(eps, 10 * rho_i.dtype_eps, msg=msg)

    def test_local(self):
        """test local observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsLocal("X", "sx")
        true_res = np.zeros(8)
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 0)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsLocal"].results_buffer["X"]
            cond = np.isclose(res, true_res).all()
            self.assertTrue(
                cond, msg=f"Local observable failing for ansatz {ansatz_id}"
            )

    def test_correlation(self):
        """test correlation observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsCorr("XX", ["sx", "sx"])
        true_res = np.identity(8)
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 1)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsCorr"].results_buffer["XX"]
            cond = np.isclose(res, true_res).all()
            self.assertTrue(
                cond, msg=f"Correlation observable failing for ansatz {ansatz_id}"
            )

    def test_tensor_product(self):
        """test TNObsTensorProduct observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsTensorProduct(
            "global_flip", ["sx"] * 8, [[ii] for ii in range(8)]
        )
        true_res = 1
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 4)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsTensorProduct"].results_buffer["global_flip"]
            cond = np.isclose(res, true_res)
            self.assertTrue(
                cond, msg=f"Tensor product observable failing for ansatz {ansatz_id}"
            )

    def test_weighted_sum(self):
        """test TNObsWeightedSum observable"""
        obsv = obs.TNObservables()
        tp_1 = obs.TNObsTensorProduct(
            "global_flip", ["sx"] * 8, [[ii] for ii in range(8)]
        )
        tp_1 += obs.TNObsTensorProduct("parity", ["sz"] * 8, [[ii] for ii in range(8)])
        obsv += obs.TNObsWeightedSum("obs", tp_1, [1, 2], use_itpo=True)
        true_res = 3
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 5)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsWeightedSum"].results_buffer["obs"]
            cond = np.isclose(res, true_res)
            self.assertTrue(
                cond, msg=f"Weighted Sum observable failing for ansatz {ansatz_id}"
            )

    def test_projective(self):
        """test TNObsProjective observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsProjective(128)
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 6)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsProjective"].results_buffer[
                "projective_measurements"
            ]
            cond = "0" * 8 in res and "1" * 8 in res
            self.assertTrue(
                cond,
                msg=f"Projective measurements observable failing for ansatz {ansatz_id}",
            )

    def test_probabilities(self):
        """test TNObsProbabilities observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsProbabilities()
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 7)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsProbabilities"].results_buffer[
                "unbiased_probability"
            ]
            cond = "0" * 8 in res and "1" * 8 in res
            self.assertTrue(
                cond,
                msg=f"Probability measurements observable failing for ansatz {ansatz_id}",
            )

    def test_bond_entropy(self):
        """test TNObsProbabilities observable"""
        obsv = obs.TNObservables()
        obsv += obs.TNObsBondEntropy()
        for ansatz_id in self.ansatz:
            obsv = self.run_measurements(obsv, ansatz_id, 8)

            # Observable not measurable by ansatz
            if obsv is None:
                continue

            res = obsv.obs_list["TNObsBondEntropy"].results_buffer["bond_entropy"]
            entanglement = list(res.values())
            true_ent = 0.6931471805599454
            cond = np.isclose(entanglement, true_ent).all()
            self.assertTrue(
                cond,
                msg=f"Entanglement measurements observable failing for ansatz {ansatz_id}",
            )
