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
Abstract class for tensors. Represents all the functions that should be
implemented in a tensor.

We provide two tensor types:

* :class:`_AbstractQteaTensor` : suitable for simulation
* :class:`_AbstractQteaBaseTensor` : suitable for simulation and
  suitable to be the base tensor type for a symmetric tensor.

"""

import abc

__all__ = ["_AbstractQteaTensor", "_AbstractQteaBaseTensor"]


class _AbstractQteaTensor(abc.ABC):
    """
    Tensor for Quantum Tea simulations.

    **Arguments**

    links : list
        Type of entries in list depends on tensor type and are either
        integers for dense tensors or some LinkType for symmetric
        tensors.

    ctrl : str, optional
        Initialization of tensor.
        Default to "Z"

    are_links_outgoing : list of bools
        Used in symmetric tensors only: direction of link in tensor.
        Length is same as rank of tensor.

    base_tensor_cls : valid dense quantum tea tensor or `None`
        Used in symmetric tensors only: class representing dense tensor

    dtype : data type, optional
        Valid data type for the underlying tensors.

    device : device specification, optional
        Valid device specification (depending on tensor).
    """

    @abc.abstractmethod
    def __init__(
        self,
        links,
        ctrl="Z",
        are_links_outgoing=None,
        base_tensor_cls=None,
        dtype=None,
        device=None,
    ):
        pass

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    @abc.abstractmethod
    def are_links_outgoing(self):
        """Define property of outgoing links as property (always False)."""

    @property
    @abc.abstractmethod
    def base_tensor_cls(self):
        """Base tensor class."""

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
    def dtype_eps(self):
        """Data type's machine precision of the underlying arrays."""

    @property
    @abc.abstractmethod
    def has_symmetry(self):
        """Boolean flag if tensor encodes symmetries."""

    @property
    @abc.abstractmethod
    def links(self):
        """Specification of link with full information to reconstruct link."""

    @property
    @abc.abstractmethod
    def ndim(self):
        """Rank of the tensor."""

    @property
    @abc.abstractmethod
    def shape(self):
        """Dimension of tensor along each dimension."""

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __eq__(self, other):
        """Checking equal tensors up to tolerance."""
        return self.are_equal(other)

    def __ne__(self, other):
        """Checking not equal tensors up to tolerance."""
        return not self.are_equal(other)

    @abc.abstractmethod
    def __add__(self, other):
        """
        Addition of a scalar to a tensor adds it to all the entries.
        If other is another tensor, elementwise addition if they have the same shape
        """

    @abc.abstractmethod
    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""

    @abc.abstractmethod
    def __mul__(self, sc):
        """Multiplication of tensor with scalar returning new tensor as result."""

    @abc.abstractmethod
    def __imul__(self, sc):
        """In-place multiplication of tensor with scalar (update)."""

    def __rmul__(self, sc):
        """Multiplication from the right of a scalar"""
        return self * sc

    @abc.abstractmethod
    def __itruediv__(self, sc):
        """In-place division of tensor with scalar (update)."""

    @abc.abstractmethod
    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @staticmethod
    @abc.abstractmethod
    def convert_operator_dict(
        op_dict,
        params=None,
        symmetries=None,
        generators=None,
        base_tensor_cls=None,
        dtype=None,
        device=None,
    ):
        """
        Iterate through an operator dict and convert the entries.

        **Arguments**

        op_dict : instance of :class:`TNOperators`
            Contains the operators as xp.ndarray.

        symmetries:  list, optional, for compatability with symmetric tensors.
            For symmetry, contains symmetries.
            Otherwise, must be empty list.

        generators : list, optional, for compatability with symmetric tensors.
            For symmetries, contains generator of the symmetries as str for dict.
            Must be empty list.

        base_tensor_cls : None, optional, for compatability with symmetric tensors.
            For symmetries, must be valid base tensor class.
            Otherwise, no checks on this one here.

        dtype : data type for xp, optional
            Specify data type.

        device : str
            Device for the simulation. Typically "cpu" and "gpu", but depending on
            tensor backend.
        """

    @abc.abstractmethod
    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor."""

    @abc.abstractmethod
    def random_unitary(self, link):
        """Generate a random unitary matrix via performing a SVD on a
        random tensor, where a matrix dimension is specified with
        `link`."""

    @classmethod
    @abc.abstractmethod
    def read(cls, filehandle, dtype, device, base_tensor_cls, cmplx=True, order="F"):
        """Read a tensor from file."""

    @staticmethod
    @abc.abstractmethod
    def set_missing_link(links, max_dim, are_links_outgoing=None):
        """Calculate the property of a missing link in a list."""

    @abc.abstractmethod
    def zeros_like(self):
        """Get a tensor with the same links as `self` but filled with zeros."""

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def are_equal(self, other, tol=1e-7):
        """Check if two tensors are equal."""

    @abc.abstractmethod
    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""

    def assert_normalized(self, tol=1e-7):
        """Raise exception if norm is not 1 up to tolerance."""
        norm = self.norm()

        if abs(norm - 1.0) > tol:
            raise Exception("Violating normalization condition.")

    def assert_unitary(self, links, tol=1e-7):
        """Raise exception if tensor is not unitary up to tolerance for given links."""
        ctensor = self.conj().tensordot(self, (links, links))
        # reshape into a matrix to check if identity
        half_links = len(ctensor.links) // 2
        ctensor.fuse_links_update(0, half_links - 1)
        ctensor.fuse_links_update(1, half_links)

        ctensor.assert_identity(tol=tol)

    @abc.abstractmethod
    def is_close_identity(self, tol=1e-7):
        """Check if rank-2 tensor is close to identity."""

    @abc.abstractmethod
    def is_dtype_complex(self):
        """Check if data type is complex."""

    @abc.abstractmethod
    def is_link_full(self, link_idx):
        """Check if the link at given index is at full bond dimension."""

    def sanity_check(self):
        """Quick set of checks for tensor."""
        return

    # --------------------------------------------------------------------------
    #                       Single-tensor operations
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def attach_dummy_link(self, position, is_outgoing=True):
        """Attach dummy link at given position (inplace update)."""

    @abc.abstractmethod
    def conj(self):
        """Return the complex conjugated in a new tensor."""

    @abc.abstractmethod
    def conj_update(self):
        """Apply the complex conjugate to the tensor in place."""

    @abc.abstractmethod
    def convert(self, dtype, device):
        """Convert underlying array to the specified data type inplace."""

    @abc.abstractmethod
    def convert_singvals(self, singvals, dtype, device):
        """Convert the singular values via a tensor."""

    @abc.abstractmethod
    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""

    @abc.abstractmethod
    def eig_api(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """Interface to hermitian eigenproblem"""

    @abc.abstractmethod
    def fuse_links_update(self, fuse_low, fuse_high, is_link_outgoing=True):
        """Fuses one set of links to a single link (inplace-update)."""

    @abc.abstractmethod
    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering small meta data)."""

    @abc.abstractmethod
    def get_entry(self):
        """Get entry if scalar on host."""

    # pylint: disable-next=unused-argument
    def flip_links_update(self, link_inds):
        """Flip irreps on given links (symmetric tensors only)."""
        return self

    @abc.abstractmethod
    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""

    @abc.abstractmethod
    def norm_sqrt(self):
        """Calculate the square root of the norm of the tensor <tensor|tensor>."""

    @abc.abstractmethod
    def normalize(self):
        """Normalize tensor with sqrt(<tensor|tensor>)."""

    @abc.abstractmethod
    def remove_dummy_link(self, position):
        """Remove the dummy link at given position (inplace update)."""

    @abc.abstractmethod
    def scale_link(self, link_weights, link_idx):
        """Scale tensor along one link at `link_idx` with weights."""

    @abc.abstractmethod
    def scale_link_update(self, link_weights, link_idx):
        """Scale tensor along one link at `link_idx` with weights (inplace update)."""

    @abc.abstractmethod
    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""

    @abc.abstractmethod
    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set element in a rank-2 tensor (inplace update)"""

    @abc.abstractmethod
    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""

    @abc.abstractmethod
    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""

    @abc.abstractmethod
    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""

    @abc.abstractmethod
    def trace_one_dim_pair(self, links):
        """Trace a pair of links with dimenion one. Inplace update."""

    @abc.abstractmethod
    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""

    @abc.abstractmethod
    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""

    @abc.abstractmethod
    def write(self, filehandle, cmplx=None):
        """Write tensor."""

    # --------------------------------------------------------------------------
    #                         Two-tensor operations
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def add_update(self, other, factor_this=None, factor_other=None):
        """
        Inplace addition as `self = factor_this * self + factor_other * other`.
        """

    @abc.abstractmethod
    def dot(self, other):
        """Inner product of two tensors <self|other>."""

    @abc.abstractmethod
    def expand_link_tensorpair(self, other, link_self, link_other, new_dim, ctrl="R"):
        """Expand the link between a pair of tensors based on the ctrl parameter. "R" for random"""

    @abc.abstractmethod
    def split_qr(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,
    ):
        """Split the tensor via a QR decomposition."""

    @abc.abstractmethod
    def split_qrte(
        self,
        tens_right,
        singvals_self,
        operator=None,
        conv_params=None,
        is_q_link_outgoing=True,
    ):
        """Split via a truncated expanded QR."""

    @abc.abstractmethod
    def split_svd(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        contract_singvals="N",
        conv_params=None,
        no_truncation=False,
        is_link_outgoing_left=True,
    ):
        """Split tensor via SVD for a bipartion of links."""

    @abc.abstractmethod
    def stack_link(self, other, link):
        """Stack two tensors along a given link."""

    @abc.abstractmethod
    def tensordot(self, other, contr_idx):
        """Tensor contraction of two tensors along the given indices."""

    # --------------------------------------------------------------------------
    #                        Internal methods
    # --------------------------------------------------------------------------

    def _invert_link_selection(self, links):
        """Invert the selection of links and return them as a list."""
        ilinks = [ii if (ii not in links) else None for ii in range(self.ndim)]
        ilinks = list(filter((None).__ne__, ilinks))
        return ilinks


class _AbstractQteaBaseTensor(_AbstractQteaTensor):
    @abc.abstractmethod
    def assert_diagonal(self, tol=1e-7):
        """Check that tensor is a diagonal matrix up to tolerance."""

    @abc.abstractmethod
    def assert_int_values(self, tol=1e-7):
        """Check that there are only integer values in the tensor."""

    @abc.abstractmethod
    def assert_real_valued(self, tol=1e-7):
        """Check that all tensor entries are real-valued."""

    @abc.abstractmethod
    def elementwise_abs_smaller_than(self, value):
        """Return boolean if each tensor element is smaller than `value`"""

    @abc.abstractmethod
    def get_argsort_func(self):
        """Return callable to argsort function."""

    @abc.abstractmethod
    def get_diag_entries_as_int(self):
        """Return diagonal entries of rank-2 tensor as integer on host."""

    @abc.abstractmethod
    def get_sqrt_func(self):
        """Return callable to sqrt function."""

    @abc.abstractmethod
    def get_submatrix(self, row_range, col_range):
        """Extract a submatrix of a rank-2 tensor for the given rows / cols."""

    @abc.abstractmethod
    def flatten(self):
        """Returns flattened version (rank-1) of dense array in native array type."""

    @classmethod
    @abc.abstractmethod
    def from_elem_array(cls, tensor, dtype=None, device=None):
        """New tensor from array."""

    @abc.abstractmethod
    def permute_rows_cols_update(self, inds):
        """Permute rows and columns of rank-2 tensor with `inds`. Inplace update."""

    @abc.abstractmethod
    def prepare_eig_api(self, conv_params):
        """Return variables for eigsh."""

    @abc.abstractmethod
    def reshape(self, shape, **kwargs):
        """Reshape a tensor."""

    @abc.abstractmethod
    def reshape_update(self, shape, **kwargs):
        """Reshape tensor dimensions inplace."""

    @abc.abstractmethod
    def set_submatrix(self, row_range, col_range, tensor):
        """Set a submatrix of a rank-2 tensor for the given rows / cols."""

    @abc.abstractmethod
    def subtensor_along_link(self, link, lower, upper):
        """Extract and return a subtensor select range (lower, upper) for one line."""

    @abc.abstractmethod
    def _truncate_singvals(self, singvals, conv_params=None):
        """Truncate the singular values followling the given strategy."""

    @abc.abstractmethod
    def vector_with_dim_like(self, dim, dtype=None):
        """Generate a vector in the native array of the base tensor."""
