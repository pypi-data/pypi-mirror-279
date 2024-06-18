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
import numpy as np
import qtealeaves as qtl


class TestsMaps(unittest.TestCase):
    """
    Check the mapping to 1d systems for various scenarios.
    """

    @staticmethod
    def traverse_map(map_obj, dims):
        """
        Traverse the whole map and return an numpy ndarray with
        True/False values for visited sites.

        **Arguments**

        map_obj : instance of HilbertCurveMap, SnakeMap, or ZigZagMap
            Mapping to the 1d system.

        dims : list of ints
            Contains the dimensions of the system.

        **Returns**

        visited : numpy ndarray
            Numpy boolean array where sites with True have
            been in the mapping.
        """
        visited = np.zeros(dims, dtype=bool)

        for ii in range(np.prod(dims)):
            visited[map_obj(ii)] = True

        return visited

    def test_visited_4x4(self):
        """
        Test that all sites have been visited in a 2d grid of 4x4 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(2, [4, 4], map_type)
            visited = self.traverse_map(obj, [4, 4])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(16, np.sum(visited), msg=msg)

    def test_visited_4x8(self):
        """
        Test that all sites have been visited in a 2d grid of 4x4 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(2, [4, 8], map_type)
            visited = self.traverse_map(obj, [4, 8])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(32, np.sum(visited), msg=msg)

    def test_visited_4x4x4(self):
        """
        Test that all sites have been visited in a 3d grid of 4x4x4 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(3, [4, 4, 4], map_type)
            visited = self.traverse_map(obj, [4, 4, 4])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(64, np.sum(visited), msg=msg)

    def test_visited_2x4x8(self):
        """
        Test that all sites have been visited in a 3d grid of 2x4x8 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(3, [4, 4, 4], map_type)
            visited = self.traverse_map(obj, [4, 4, 4])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(64, np.sum(visited), msg=msg)

    def test_visited_8x2x4(self):
        """
        Test that all sites have been visited in a 3d grid of 8x2x4 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(3, [4, 4, 4], map_type)
            visited = self.traverse_map(obj, [4, 4, 4])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(64, np.sum(visited), msg=msg)

    def test_visited_4x8x2(self):
        """
        Test that all sites have been visited in a 3d grid of 4x8x2 sites.
        """
        for map_type in ["HilbertCurveMap", "SnakeMap", "ZigZagMap"]:
            obj = qtl.map_selector(3, [4, 4, 4], map_type)
            visited = self.traverse_map(obj, [4, 4, 4])

            msg = "Not all sites have been visited in %s." % (map_type)
            self.assertEqual(64, np.sum(visited), msg=msg)

    def test_snake_2x2(self):
        """
        Test the actual snake map for a 2x2.
        """
        ref = [(0, 0), (1, 0), (1, 1), (0, 1)]
        obj = qtl.map_selector(2, [2, 2], "SnakeMap")

        for ii in range(4):
            self.assertEqual(ref[ii], obj(ii), msg="Snake mismatch.")

    def test_snake_2x2x2(self):
        """
        Test the actual snake map for a 2x2.
        """
        ref = [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 1, 1),
            (1, 1, 1),
            (1, 0, 1),
            (0, 0, 1),
        ]
        obj = qtl.map_selector(3, [2, 2, 2], "SnakeMap")

        for ii in range(8):
            self.assertEqual(ref[ii], obj(ii), msg="Snake mismatch.")

    def test_zigzag_2x2(self):
        """
        Test the actual zigzag map for a 2x2.
        """
        ref = [(0, 0), (0, 1), (1, 0), (1, 1)]
        obj = qtl.map_selector(2, [2, 2], "ZigZagMap")

        for ii in range(4):
            self.assertEqual(ref[ii], obj(ii), msg="ZigZag mismatch.")

    def test_zigzag_2x2x2(self):
        """
        Test the actual zigzag map for a 2x2x2.
        """
        ref = [
            (0, 0, 0),
            (0, 0, 1),
            (0, 1, 0),
            (0, 1, 1),
            (1, 0, 0),
            (1, 0, 1),
            (1, 1, 0),
            (1, 1, 1),
        ]
        obj = qtl.map_selector(3, [2, 2, 2], "ZigZagMap")

        for ii in range(8):
            self.assertEqual(ref[ii], obj(ii), msg="ZigZag mismatch.")

    def test_zigzag_2x4(self):
        """
        Test the actual zigzag map for a 2x4.
        """
        ref = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3)]
        obj = qtl.map_selector(2, [2, 4], "ZigZagMap")

        for ii in range(8):
            self.assertEqual(ref[ii], obj(ii), msg="ZigZag mismatch.")

    def test_backmapping_vector_observable_2d(self):
        """
        Test backmapping for a vector observable for a Hilbert curve in 2d.
        """
        obj = qtl.map_selector(2, [4, 4], "HilbertCurveMap")

        # Construct an observable array which maps to 10 * x_index + y_index
        vec = np.array([0, 10, 11, 1, 2, 3, 13, 12, 22, 23, 33, 32, 31, 21, 20, 30])

        res = obj.backmapping_vector_observable(vec)

        for ii in range(4):
            for jj in range(4):
                ref = int(str(ii) + str(jj))
                self.assertEqual(ref, res[ii, jj])

    def test_backmapping_vector_observable_3d(self):
        """
        Test backmapping for a vector observable for a Hilbert curve in 3d.
        """
        obj = qtl.map_selector(3, [2, 2, 2], "HilbertCurveMap")

        # Construct an observable array which maps to
        # 100 * x_index + 10 * y_index + z_index
        vec = np.array([0, 100, 110, 10, 11, 111, 101, 1])

        res = obj.backmapping_vector_observable(vec)

        for ii in range(2):
            for jj in range(2):
                for kk in range(2):
                    ref = int(str(ii) + str(jj) + str(kk))
                    self.assertEqual(ref, res[ii, jj, kk])

    def test_backmapping_matrix_observable_2d(self):
        """
        Test backmapping for a matrix observable for a Hilbert curve in 2d.
        """
        obj = qtl.map_selector(2, [4, 4], "HilbertCurveMap")

        # Construct an observable array which maps to 10 * x_index + y_index
        vec = np.array([0, 10, 11, 1, 2, 3, 13, 12, 22, 23, 33, 32, 31, 21, 20, 30])

        # Combine what we have for the vector in a convenient way
        mat = np.zeros([16, 16], dtype=int)
        for ii in range(16):
            for jj in range(16):
                mat[ii, jj] = vec[ii] * vec[jj]

        res = obj.backmapping_matrix_observable(mat)

        for i1 in range(4):
            for i2 in range(4):
                ref_1 = int(str(i1) + str(i2))

                for j1 in range(4):
                    for j2 in range(4):
                        ref_2 = int(str(j1) + str(j2))

                        ref = ref_1 * ref_2
                        self.assertEqual(ref, res[i1, i2, j1, j2])

    def test_backmapping_matrix_observable_3d(self):
        """
        Test backmapping for a matrix observable for a Hilbert curve in 3d.
        """
        obj = qtl.map_selector(3, [2, 2, 2], "HilbertCurveMap")

        # Construct an observable array which maps to
        # 100 * x_index + 10 * y_index + z_index
        vec = np.array([0, 100, 110, 10, 11, 111, 101, 1])

        # Combine what we have for the vector in a convenient way
        mat = np.zeros([8, 8], dtype=int)
        for ii in range(8):
            for jj in range(8):
                mat[ii, jj] = (vec[ii] + 2) * (vec[jj] + 3)

        res = obj.backmapping_matrix_observable(mat)

        for i1 in range(2):
            for i2 in range(2):
                for i3 in range(2):
                    ref_1 = int(str(i1) + str(i2) + str(i3)) + 2

                    for j1 in range(2):
                        for j2 in range(2):
                            for j3 in range(2):
                                ref_2 = int(str(j1) + str(j2) + str(j3)) + 3

                                ref = ref_1 * ref_2
                                self.assertEqual(ref, res[i1, i2, i3, j1, j2, j3])
