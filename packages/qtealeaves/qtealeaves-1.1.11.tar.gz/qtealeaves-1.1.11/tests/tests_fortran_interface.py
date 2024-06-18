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
import filecmp

from qtealeaves import write_symtensor


class TestsWriteSymTensor(unittest.TestCase):
    def setUp(self):
        os.makedirs("TMP_TEST")

    def tearDown(self):
        rmtree("TMP_TEST")

    def test_spin12_nosymm_id(self):
        """
        Check on symmetric tensor with one, single irreps.
        """
        # Create reference file
        one = "(         1.000000000000000E+00,          0.000000000000000E+00)"
        op_str = "1\nZ\n2\n2\nF T\n1\n0\n2\n1\n0\n2\nS\n2\n"
        op_str += "0 0, 1 1, " + one + "\n0 0, 2 2, " + one + "\n"
        fh = open("TMP_TEST/id.orig", "w+")
        fh.write(op_str)
        fh.close()

        eye = np.eye(2)
        gen = np.zeros([2, 2])

        fh = open("TMP_TEST/id.dat", "w+")
        write_symtensor(eye, fh, [gen], ["Z2"])
        fh.close()

        are_equal = filecmp.cmp("TMP_TEST/id.dat", "TMP_TEST/id.orig", shallow=False)

        self.assertTrue(are_equal)

        return
