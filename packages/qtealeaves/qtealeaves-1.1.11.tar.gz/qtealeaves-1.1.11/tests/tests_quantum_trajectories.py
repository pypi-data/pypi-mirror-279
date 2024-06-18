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
import qtealeaves.modeling as modeling
from qtealeaves.models import get_quantum_ising_1d


class TestsQuantumTrajectories(unittest.TestCase):
    def setUp(self):
        """
        Provide some default settings.
        """
        np.random.seed([11, 13, 17, 19])

        self.conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_bond_dimension=16, cut_ratio=1e-16
        )

        self.in_folder = "TEST_INPUT"
        self.out_folder = "TEST_OUTPUT"

    def tearDown(self):
        """
        Remove input and output folders again
        """
        if os.path.isdir(self.in_folder):
            rmtree(self.in_folder)
        if os.path.isdir(self.out_folder):
            rmtree(self.out_folder)

        return

    def test_ising(self):
        """
        Testing ED code with quantum trajctories.
        """
        model, my_ops = get_quantum_ising_1d()

        def get_mask(params):
            tmp = np.zeros(8, dtype=bool)
            tmp[0] = True
            tmp[-1] = True
            return tmp

        model += modeling.LocalTerm("sz", strength="r", prefactor=-1, mask=get_mask)

        my_obs = qtl.observables.TNObservables(num_trajectories=3)
        my_obs += qtl.observables.TNObsLocal("sz", "sz")

        quench = qtl.DynamicsQuench([0.05] * 5, time_evolution_mode=0)
        quench["r"] = lambda tt, params: 0.5

        simulation = qtl.QuantumGreenTeaSimulation(
            model,
            my_ops,
            self.conv,
            my_obs,
            tn_type=0,
            folder_name_input=self.in_folder,
            folder_name_output=self.out_folder,
            has_log_file=True,
            verbosity=False,
            store_checkpoints=False,
        )

        for elem in [
            {
                "L": 8,
                "J": 1.0,
                "g": 0.5,
                "r": 0.0,
                "Quenches": [quench],
                "exclude_from_hash": ["Quenches"],
            }
        ]:
            simulation.run(elem, delete_existing_folder=True)

            ed_static = simulation.get_static_obs(elem)
            ed_dyn = simulation.get_dynamic_obs(elem)

            # Check that we can still access results as before
            energy = ed_static["energy"]
            energy = ed_dyn[-1][-1]["energy"]
            time = ed_dyn[-1][-1]["time"]

            # print(ed_static)
            # print(ed_dyn)
