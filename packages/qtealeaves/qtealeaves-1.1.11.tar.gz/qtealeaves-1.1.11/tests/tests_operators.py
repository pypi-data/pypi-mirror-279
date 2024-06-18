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
import os.path
import unittest
import numpy as np
from shutil import rmtree

from qtealeaves.operators import TNSpin12Operators, TNBosonicOperators


class TestsTNOperators(unittest.TestCase):
    """
    Tests on the operator classes.
    """

    def setUp(self):
        os.makedirs("TMP_TEST")

    def tearDown(self):
        rmtree("TMP_TEST")

    def test_spin12_symm(self):
        """
        Test that we can write symmetric tensors for the
        spin 1/2 operators.
        """
        ops = TNSpin12Operators()

        params = {
            "SymmetrySectors": [0],
            "SymmetryGenerators": ["n"],
            "SymmetryTypes": ["Z2"],
        }

        with open("TMP_TEST/test.dat", "w+") as fh:
            for elem in ops.ops:
                ops.write_operator(fh, elem, params, tensor_backend=1)

    def test_bosonic_symm(self):
        """
        Test that we can write symmetric tensors for the
        bosonic operators.
        """
        ops = TNBosonicOperators()

        params = {
            "SymmetrySectors": [4],
            "SymmetryGenerators": ["n"],
            "SymmetryTypes": ["Z2"],
        }

        for nmax in [1, 5, 8]:
            params["fock_space_nmax"] = nmax

            with open("TMP_TEST/test.dat", "w+") as fh:
                for elem in ops.ops:
                    ops.write_operator(fh, elem, params, tensor_backend=1)
