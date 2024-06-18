# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Spin operators.
"""

import numpy as np

from .tnoperators import TNOperators


__all__ = ["TNSpin12Operators"]


class TNSpin12Operators(TNOperators):
    """
    Operators specifically targeted at spin 1/2 systems. The operators
    ``id``, ``sx``, ``sz``, ``n``= 1/2*(1-``sz``), and
    ``nz`` = 1/2*(1+``sz``) are provided by default.

    **Arguments**

    folder_operators : str, optional
        The name of the subfolder inside the input folder, where
        we store operators.
        Default to ``SPIN12``
    """

    def __init__(self, folder_operators="SPIN12"):
        super().__init__(folder_operators=folder_operators)

        self.ops["id"] = np.array([[1, 0], [0, 1.0]])
        self.ops["sx"] = np.array([[0, 1], [1, 0.0]])
        self.ops["sz"] = np.array([[1, 0], [0, -1.0]])
        self.ops["n"] = np.array([[0, 0], [0, 1.0]])
        self.ops["nz"] = np.array([[1, 0], [0, 0.0]])
