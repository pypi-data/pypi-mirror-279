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
Tensor backend specification.
"""

# pylint: disable=too-few-public-methods

import numpy as np

from .tensor import QteaTensor

__all__ = ["TensorBackend"]


class TensorBackend:
    """
    Defines the complete tensor backend to be used. Contains the tensor class,
    the base tensor class in case it is needed for symmetric tensors, the
    target device, and the data type.
    """

    def __init__(
        self,
        tensor_cls=QteaTensor,
        base_tensor_cls=QteaTensor,
        device="cpu",
        dtype=np.complex128,
    ):
        self.tensor_cls = tensor_cls
        self.base_tensor_cls = base_tensor_cls
        self.device = device
        self.dtype = dtype

    def __call__(self, *args, **kwargs):
        auto = {}
        for key, value in self.tensor_cls_kwargs().items():
            if key not in kwargs:
                auto[key] = value

        return self.tensor_cls(*args, **kwargs, **auto)

    def tensor_cls_kwargs(self):
        """
        Returns the keywords arguments for an `_AbstractQteaTensor`.
        """
        return {
            "base_tensor_cls": self.base_tensor_cls,
            "device": self.device,
            "dtype": self.dtype,
        }
