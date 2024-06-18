# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import unittest
import os
import os.path
import numpy as np
import numpy.linalg as nla
from shutil import rmtree
from qtealeaves import modeling

import qtealeaves as qtl
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.models import get_quantum_ising_1d, get_quantum_ising_2d


class TestsSimulationSetup(unittest.TestCase):
    def setUp(self):
        # Define convergence parameters
        self.conv_params = TNConvergenceParameters(
            max_iter=7, max_bond_dimension=20, cut_ratio=1e-9
        )

        # 1D Ising model and operators
        self.model_1d, self.my_ops_1d = get_quantum_ising_1d(False)
        self.params_1d = {
            "J": -1,
            "g": 1,
            "L": 64,
        }

        # 2D Ising model and operators
        self.model_2d, self.my_ops_2d = get_quantum_ising_2d(False)
        self.params_2d = {
            "J": -1,
            "g": 1,
            "L": [8, 8],
        }

        # Observables
        myObs = qtl.observables.TNObservables()
        self.myObs = myObs

        # input / output folder
        self.in_folder = "TEST_INPUT"
        self.out_folder = "TEST_OUTPUT"

        return

    def tearDown(self):
        """
        Remove input and output folders again
        """
        if os.path.isdir(self.in_folder):
            rmtree(self.in_folder)
        if os.path.isdir(self.out_folder):
            rmtree(self.out_folder)

        return

    def get_attn_disentanglers(self, dim):
        """
        Returns the automatically selected disentangler positions for aTTN.

        Parameters
        ----------
        dim : int
            Dimensionality of the system - is it 1D or 2D.

        Return
        ------
        disentanglers : np.array
            Automatically selected disentangler positions.
        """
        # Get the model and operators
        if dim == 1:
            model, my_ops = self.model_1d, self.my_ops_1d
            params = self.params_1d
        elif dim == 2:
            model, my_ops = self.model_2d, self.my_ops_2d
            params = self.params_2d
        else:
            raise ValueError(
                f"Invalid lattice. System dimension cannot be {dim}, only 1 or 2."
            )

        symmetry_sector = 0
        tensor_backend = 2 if (symmetry_sector is None) else 1

        # Define the simulation
        simulation = qtl.QuantumGreenTeaSimulation(
            model,
            my_ops,
            self.conv_params,
            self.myObs,
            tn_type=2,
            tensor_backend=tensor_backend,
            disentangler=None,
            folder_name_input=self.in_folder,
            folder_name_output=self.out_folder,
            has_log_file=True,
            verbosity=0,
        )

        disentanglers = simulation.autoselect_disentangler(params)

        return disentanglers

    def test_attn_automatic_de_position_1d(self):
        """
        Check if aTTN automatic disentangler position selection gives the
        correct number of disentanglers for 1D Ising model.
        """
        disentanglers = self.get_attn_disentanglers(dim=1)
        num_disentanglers = disentanglers.shape[1]

        self.assertEqual(
            16,
            num_disentanglers,
            "Disentangler autoselection returned wrong number of disentanglers for 1D Ising"
            " model.",
        )

        return

    def test_attn_automatic_de_position_2d(self):
        """
        Check if aTTN automatic disentangler position selection gives the
        correct number of disentanglers for 2D Ising model.
        """

        disentanglers = self.get_attn_disentanglers(dim=2)
        num_disentanglers = disentanglers.shape[1]

        self.assertEqual(
            16,
            num_disentanglers,
            "Disentangler autoselection returned wrong number of disentanglers for 2D Ising"
            " model.",
        )
        return
