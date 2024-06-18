# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Anum_y modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import os.path
import unittest
import numpy as np
import numpy.linalg as nla
from shutil import rmtree

from qtealeaves.tooling import LatticeLayout


class TestLatticeLayout(unittest.TestCase):
    """
    Check if the 2D lattice layout is constructed properly.
    """

    def setUp(self):
        """
        Provide default setting for 4x4 square and triangle layout .
        """
        self.num_x = 4
        self.num_y = 4

        # Define square lattice
        self.square_lattice = LatticeLayout(self.num_x, self.num_y, "square")

        # Define triangle lattice
        self.triangle_lattice = LatticeLayout(self.num_x, self.num_y, "triangle")

        return

    def test_positions(self):
        """
        Test if the position is inizialized for each point in the lattice.
        """

        dim_square = self.square_lattice.positions.shape

        self.assertEqual(dim_square[0], self.num_x)
        self.assertEqual(dim_square[0], self.num_y)

        dim_triangle = self.triangle_lattice.positions.shape

        self.assertEqual(dim_triangle[0], self.num_x)
        self.assertEqual(dim_triangle[0], self.num_y)

        return

    def test_unique_distances(self):
        """
        Test the number of unique distances between the lattice
        point for the square lattice for n=num_x=num_y and n<=12.
        """

        # Number of unique distances for square lattice nxn with n=2-12
        num_unique_list_square = [
            [2, 2],
            [3, 5],
            [4, 9],
            [5, 14],
            [6, 19],
            [7, 26],
            [8, 33],
            [9, 41],
            [10, 50],
            [11, 60],
            [12, 70],
        ]

        if self.num_x == self.num_y:
            if self.num_x <= 12:
                for index, x in enumerate(num_unique_list_square):
                    if self.num_x == x[0]:
                        num_unique = x[1]
                num_unique_square = len(self.square_lattice.unique_distances())
                self.assertEqual(num_unique_square, num_unique)
            else:
                self.fail("This test works only for n=num_x=num_y and n<=12.")
        else:
            self.fail("This test works only for n=num_x=num_y and n<=12.")
        return
