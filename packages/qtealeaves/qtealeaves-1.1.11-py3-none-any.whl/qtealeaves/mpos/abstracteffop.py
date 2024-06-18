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
Abstract MPO terms defining the methods needed, e.g., for ground state search.
"""

import abc

__all__ = ["_AbstractEffectiveOperators"]


class _AbstractEffectiveOperators(abc.ABC):
    """
    Any effective operator or overlap.

    **Details**

    Effective operators should implement at least a dictionary
    functionality where the keys are made of a tuple of two
    entries, where each entry is the position of a tensor in
    the tensor network. The key `(pos_a, pos_b)` provides
    the effective operators of the tensor at `pos_a` contracted
    except for the link leading to the tensor at `pos_b`.
    The position itself can be implemented depending on the
    needs of the tensor networks, e.g., as integer or tuple
    of integers. Only each link needs a unique pair of positions.
    """

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    @abc.abstractmethod
    def device(self):
        """Device where the tensor is stored."""

    @property
    @abc.abstractmethod
    def dtype(self):
        """Data type of the underlying arrays."""

    @property
    @abc.abstractmethod
    def num_sites(self):
        """Return the number of sites in the underlying system."""

    @property
    def has_oqs(self):
        """Return if effective operators is open system (if no support, always False)."""
        return False

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def __getitem__(self, idxs):
        """Get an entry from the effective operators."""

    @abc.abstractmethod
    def __setitem__(self, key, value):
        """Set an entry from the effective operators."""

    # --------------------------------------------------------------------------
    #                        Abstract effective operator methods
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def contr_to_eff_op(self, tensor, pos, pos_links, idx_out):
        """Calulcate the effective operator along a link."""

    @abc.abstractmethod
    def contract_tensor_lists(self, tensor, pos, pos_links, custom_ops=None):
        """
        Linear operator to contract all the effective operators
        around the tensor in position `pos`. Used in the optimization.
        """

    @abc.abstractmethod
    def convert(self, dtype, device):
        """
        Convert underlying array to the speificed data type inplace. Original
        site terms are preserved.
        """

    @abc.abstractmethod
    def setup_as_eff_ops(self, tensor_network, measurement_mode=False):
        """Set this sparse MPO as effective ops in TN and initialize."""

    # Potential next abstract methods (missing consistent interfaces
    # in terms of permutation, i.e., whole legs or just non-MPO legs)
    #
    # * tensordot_with_tensor
    # * tensordot_with_tensor_left
    # * matrix_matrix_mult

    # --------------------------------------------------------------------------
    #                            Effective operator methods
    # --------------------------------------------------------------------------

    def print_summary(self, log_file=None):
        """Print summary of computational effort (by default no report)."""
