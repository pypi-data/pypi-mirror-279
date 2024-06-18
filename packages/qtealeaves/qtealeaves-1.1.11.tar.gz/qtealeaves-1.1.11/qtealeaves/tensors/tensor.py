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
Tensor class based on numpy / cupy
"""

# pylint: disable=too-many-locals
import itertools
import warnings
import numpy as np
import scipy as sp
import scipy.sparse.linalg as ssla

# Try to import cupy
try:
    import cupy as cp
    import cupyx.scipy.sparse.linalg as csla
    from cupy_backends.cuda.api.runtime import CUDARuntimeError

    try:
        # _ = cp.cuda.Device()
        GPU_AVAILABLE = True
    except CUDARuntimeError:
        GPU_AVAILABLE = False
except ImportError:
    cp = None
    GPU_AVAILABLE = False


from qtealeaves.tooling import read_tensor, write_tensor
from qtealeaves.solvers import EigenSolverH
from qtealeaves.operators import TNOperators
from qtealeaves.convergence_parameters import TNConvergenceParameters

from .abstracttensor import _AbstractQteaBaseTensor

__all__ = ["QteaTensor"]


class QteaTensor(_AbstractQteaBaseTensor):
    """
    Dense tensor for Quantum Tea simulations using numpy or cupy as
    underlying arrays and linear algebra.

    **Arguments**

    links : list of integers
        Dimension along each link.

    ctrl : str, optional
        Initialization of tensor. Valid are "N" (uninitialized array),
        "Z" (zeros) "R", "random" (random), "ground" for first element
        equal to one, or `None` (elem completely not set)
        Default to "Z"

    are_links_outgoing : list of bools, optional
        Used in symmetric tensors only

    base_tensor_cls : valid dense quantum tea tensor or `None`, optional
        Used in symmetric tensors only

    dtype : data type, optional
        Data type for numpy or cupy.
        Default to np.complex128

    device : device specification, optional
        Default to `"cpu"`.
        Available: `"cpu", "gpu"`
    """

    implemented_devices = ("cpu", "gpu")

    def __init__(
        self,
        links,
        ctrl="Z",
        are_links_outgoing=None,
        base_tensor_cls=None,
        dtype=np.complex128,
        device=None,
    ):
        """

        links : list of ints with shape (links works towards generalization)
        """
        super().__init__(links)
        self._device = device
        xp = self._device_checks()

        if ctrl is None:
            self._elem = None
        elif ctrl in ["N"]:
            self._elem = xp.ndarray(links, dtype=dtype)
        elif ctrl in ["O"]:
            self._elem = xp.ones(links, dtype=dtype)
        elif ctrl in ["Z"]:
            self._elem = xp.zeros(links, dtype=dtype)
        elif ctrl in ["R", "random"]:
            self._elem = xp.random.rand(*links) + 1j * xp.random.rand(*links)
            self.convert(dtype, device)
        elif ctrl in ["ground"]:
            dim = np.prod(links)
            self._elem = xp.zeros([dim], dtype=dtype)
            self._elem[0] = 1.0
            self._elem = self._elem.reshape(links)
        else:
            raise Exception(f"Unknown initialization {ctrl}.")

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def are_links_outgoing(self):
        """Define property of outgoing links as property (always False)."""
        return [False] * self.ndim

    @property
    def base_tensor_cls(self):
        """Base tensor class."""
        # None is sufficient, no symmetric tensor
        return None

    @property
    def device(self):
        """Device where the tensor is stored."""
        return self._device

    @property
    def elem(self):
        """Elements of the tensor."""
        return self._elem

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        return self._elem.dtype

    @property
    def dtype_eps(self):
        """Data type's machine precision."""
        eps_dict = {
            "float16": 1e-3,
            "float32": 1e-7,
            "float64": 1e-14,
            "complex64": 1e-7,
            "complex128": 1e-14,
        }

        return eps_dict[str(self.dtype)]

    @property
    def has_symmetry(self):
        """Boolean flag if tensor encodes symmetries."""
        return False

    @property
    def links(self):
        """Here, as well dimension of tensor along each dimension."""
        return self.shape

    @property
    def ndim(self):
        """Rank of the tensor."""
        return self._elem.ndim

    @property
    def shape(self):
        """Dimension of tensor along each dimension."""
        return self._elem.shape

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------
    #
    # inherit def __eq__
    # inherit def __ne__

    def __add__(self, other):
        """
        Addition of a scalar to a tensor adds it to all the entries.
        If other is another tensor, elementwise addition if they have the same shape
        """
        new_tensor = self.copy()
        if np.isscalar(other):
            new_tensor._elem += other
        elif isinstance(other, QteaTensor):
            new_tensor._elem += other.elem
        else:
            raise TypeError(
                "Addition for QteaTensor is defined only for scalars and QteaTensor,"
                + f" not {type(other)}"
            )
        return new_tensor

    def __iadd__(self, other):
        """In-place addition of tensor with tensor or scalar (update)."""
        if np.isscalar(other):
            self._elem += other
        elif isinstance(other, QteaTensor):
            self._elem += other.elem
        else:
            raise TypeError(
                "Addition for QteaTensor is defined only for scalars and QteaTensor,"
                + f" not {type(other)}"
            )
        return self

    def __mul__(self, sc):
        """Multiplication of tensor with scalar returning new tensor as result."""
        return QteaTensor.from_elem_array(
            sc * self._elem, dtype=self.dtype, device=self.device
        )

    def __matmul__(self, other):
        """Matrix multiplication as contraction over last and first index of self and other."""
        idx = self.ndim - 1
        return self.tensordot(other, ([idx], [0]))

    def __imul__(self, sc):
        """In-place multiplication of tensor with scalar (update)."""
        self._elem *= sc
        return self

    def __itruediv__(self, sc):
        """In-place division of tensor with scalar (update)."""
        if sc == 0:
            raise Exception("Trying to divide by zero.")
        self._elem /= sc
        return self

    def __truediv__(self, sc):
        """Division of tensor with scalar."""
        if sc == 0:
            raise Exception("Trying to divide by zero.")
        elem = self._elem / sc
        return QteaTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def __neg__(self):
        """Negative of a tensor returned as a new tensor."""
        # pylint: disable-next=invalid-unary-operand-type
        neg_elem = -self._elem
        return QteaTensor.from_elem_array(
            neg_elem, dtype=self.dtype, device=self.device
        )

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @staticmethod
    def convert_operator_dict(
        op_dict,
        params=None,
        symmetries=None,
        generators=None,
        base_tensor_cls=None,
        dtype=np.complex128,
        device="cpu",
    ):
        """
        Iterate through an operator dict and convert the entries. Converts as well
        to rank-4 tensors.

        **Arguments**

        op_dict : instance of :class:`TNOperators`
            Contains the operators as xp.ndarray.

        params : dict, optional
            To resolve operators being passed as callable.

        symmetries:  list, optional, for compatability with symmetric tensors.
            Must be empty list.

        generators : list, optional, for compatability with symmetric tensors.
            Must be empty list.

        base_tensor_cls : None, optional, for compatability with symmetric tensors.
            No checks on this one here.

        dtype : data type for xp, optional
            Specify data type.
            Default to `np.complex128`

        device : str
            Device for the simulation. Available "cpu" and "gpu"
            Default to "cpu"

        **Details**

        The conversion to rank-4 tensors is useful for future implementations,
        either to support adding interactions with a bond dimension greater than
        one between them or for symmetries. We add dummy links of dimension one.
        The order is (dummy link to the left, old link-1, old link-2, dummy link
        to the right).
        """
        if params is None:
            params = {}

        if symmetries is None:
            symmetries = []

        if generators is None:
            generators = []

        if len(symmetries) != 0:
            raise Exception("Symmetries not supported, but symmetry given.")

        if len(generators) != 0:
            raise Exception("Symmetries not supported, but generators given.")

        new_op_dict = TNOperators()
        for key in op_dict.keys():
            if isinstance(op_dict[key], QteaTensor):
                new_op_dict.ops[key] = op_dict[key]

                if op_dict[key].ndim == 2:
                    new_op_dict.ops[key].attach_dummy_link(0)
                    new_op_dict.ops[key].attach_dummy_link(3)

                continue

            tensor = op_dict.eval_numeric_param(op_dict[key], params)

            new_op_dict.ops[key] = QteaTensor.from_elem_array(
                tensor, dtype=dtype, device=device
            )

            new_op_dict.ops[key].attach_dummy_link(0)
            new_op_dict.ops[key].attach_dummy_link(3)

        return new_op_dict

    def copy(self, dtype=None, device=None):
        """Make a copy of a tensor."""
        if dtype is None:
            dtype = self.dtype
        if device is None:
            device = self.device
        tensor = self.from_elem_array(self._elem.copy(), dtype=dtype, device=device)
        return tensor

    def eye_like(self, link):
        """
        Generate identity matrix.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here integer.
            Dimension of the square, identity matrix.
        """
        xp = self._device_checks()
        elem = xp.eye(link)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def random_unitary(self, link):
        """
        Generate a random unitary matrix via performing a SVD on a
        random tensor.

        **Arguments**

        self : instance of :class:`QteaTensor`
            Extract data type etc from this one here.

        link : same as returned by `links` property, here integer.
            Dimension of the square, random unitary matrix.
        """
        xp = self._device_checks()
        elem = xp.random.rand(link, link)
        elem, _, _ = xp.linalg.svd(elem, full_matrices=False)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    @classmethod
    def read(cls, filehandle, dtype, device, base_tensor_cls, cmplx=True, order="F"):
        """Read a tensor from file."""
        elem = read_tensor(filehandle, cmplx=cmplx, order=order)

        obj = cls(elem.shape, ctrl="Z", dtype=dtype, device=device)
        obj._elem += elem

        obj.convert(None, device)

        return obj

    @staticmethod
    def set_missing_link(links, max_dim, are_links_outgoing=None):
        """
        Calculate the property of a missing link in a list.

        **Arguments**

        links : list
            Contains data like returned by property `links`, except
            for one element being `None`

        max_dim : int
            Maximal dimension of link allowed by convergence parameters
            or similar.

        are_links_outgoing : list of bools
            Indicates link direction for symmetry tensors only.
        """
        dim = 1
        idx = None

        for ii, elem in enumerate(links):
            if elem is None:
                idx = ii
            else:
                dim *= elem

        if max_dim is not None:
            links[idx] = min(dim, max_dim)
        else:
            links[idx] = dim

        return links

    def zeros_like(self):
        """Get a tensor same as `self` but filled with zeros."""
        return QteaTensor(self.shape, ctrl="Z", dtype=self.dtype, device=self.device)

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------
    #
    # inherit def assert_normalized
    # inherit def assert_unitary
    # inherit def sanity_check

    def are_equal(self, other, tol=1e-7):
        """Check if two tensors are equal."""
        xp = self._device_checks()

        if self.ndim != other.ndim:
            return False

        if np.any(self.shape != other.shape):
            return False

        return xp.isclose(self._elem, other._elem, atol=tol).all()

    def assert_identical_irrep(self, link_idx):
        """Assert that specified link is identical irreps."""
        if self.shape[link_idx] != 1:
            raise Exception("Link dim is greater one in identical irrep check.")

    def assert_identity(self, tol=1e-7):
        """Check if tensor is an identity matrix."""

        if not self.is_close_identity(tol=tol):
            print("Error information tensor", self._elem)
            raise Exception("Tensor not diagonal with ones.")

    def is_close_identity(self, tol=1e-7):
        """Check if rank-2 tensor is close to identity."""
        xp = self._device_checks()

        if self.ndim != 2:
            return False

        if self.shape[0] != self.shape[1]:
            return False

        eye = xp.eye(self.shape[0])

        eps = (np.abs(eye - self._elem)).max()

        return eps < tol

    def is_dtype_complex(self):
        """Check if data type is complex."""
        xp = self._device_checks()
        return xp.issubdtype(self._elem.dtype, xp.complexfloating)

    def is_link_full(self, link_idx):
        """Check if the link at given index is at full bond dimension."""
        links = list(self.links)
        links[link_idx] = None

        links = self.set_missing_link(links, None)

        return self.links[link_idx] >= links[link_idx]

    # --------------------------------------------------------------------------
    #                       Single-tensor operations
    # --------------------------------------------------------------------------
    #
    # inherit def flip_links_update

    def attach_dummy_link(self, position, is_outgoing=True):
        """Attach dummy link at given position (inplace update)."""
        # Could use xp.expand_dims
        new_shape = list(self.shape)[:position] + [1] + list(self.shape)[position:]
        self.reshape_update(new_shape)
        return self

    def conj(self):
        """Return the complex conjugated in a new tensor."""
        return QteaTensor.from_elem_array(
            self._elem.conj(), dtype=self.dtype, device=self.device
        )

    def conj_update(self):
        """Apply the complex conjugated to the tensor in place."""
        xp = self._device_checks()
        xp.conj(self._elem, out=self._elem)

    def convert(self, dtype, device):
        """Convert underlying array to the specified data type inplace."""

        if device is not None:
            if device not in self.implemented_devices:
                raise ValueError(
                    f"Device {device} is not implemented. Select from"
                    + f" {self.implemented_devices}"
                )
            if (device == "gpu") and (not GPU_AVAILABLE):
                raise ImportError("CUDA GPU is not available")

            # Both devices available, figure out what we currently have
            # and start converting
            if isinstance(self._elem, np.ndarray):
                current = "cpu"
            elif cp is None:
                current = None
            elif isinstance(self.elem, cp.ndarray):
                current = "gpu"
            else:
                current = None

            if device == current:
                # We already are in the correct device
                pass
            elif device == "gpu":
                # We go to the cpu to gpu
                self._elem = cp.asarray(self._elem)
            elif device == "cpu":
                # We go from gpu to cpu
                self._elem = cp.asnumpy(self._elem)

            self._device = device
        if dtype is not None:
            if dtype != self.dtype:
                self._elem = self._elem.astype(dtype)

        return self

    def convert_singvals(self, singvals, dtype, device):
        """Convert the singular values via a tensor."""
        if device is not None:
            if device not in self.implemented_devices:
                raise ValueError(
                    f"Device {device} is not implemented. Select from"
                    + f" {self.implemented_devices}"
                )

            if (device == "gpu") and (not GPU_AVAILABLE):
                raise ImportError("CUDA GPU is not available")

            # Both devices available, figure out what we currently have
            # and start converting
            if isinstance(singvals, np.ndarray):
                current = "cpu"
            elif cp is None:
                current = None
            elif isinstance(singvals, cp.ndarray):
                current = "gpu"
            else:
                current = None

            if device == current:
                # We already are in the correct device
                pass
            elif device == "gpu":
                # We go to the cpu to gpu
                singvals = cp.asarray(singvals)
            elif device == "cpu":
                # We go from gpu to cpu
                singvals = cp.asnumpy(singvals)

        if dtype is not None:
            dtype = dtype(0).real.dtype
            if dtype != singvals.dtype:
                singvals = singvals.astype(dtype)

        return singvals

    def diag(self, real_part_only=False, do_get=False):
        """Return the diagonal as array of rank-2 tensor."""
        xp = self._device_checks()

        if self.ndim != 2:
            raise Exception("Can only run on rank-2.")

        diag = xp.diag(self._elem)

        if real_part_only:
            diag = xp.real(diag)

        if self.device == "gpu" and do_get:
            diag = diag.get()

        return diag

    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""
        xp = self._device_checks()

        data_types = {
            "C": xp.complex64,
            "D": xp.float64,
            "H": xp.float16,
            "S": xp.float32,
            "Z": xp.complex128,
        }

        return data_types[dtype]

    def eig_api(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """
        Interface to hermitian eigenproblem

        **Arguments**

        matvec_func : callable
            Mulitplies "matrix" with "vector"

        links : links according to :class:`QteaTensor`
            Contain the dimension of the problem.

        conv_params : instance of :class:`TNConvergenceParameters`
            Settings for eigenproblem with Arnoldi method.

        args_func : arguments for matvec_func

        kwargs_func : keyword arguments for matvec_func

        **Returns**

        eigenvalues : scalar

        eigenvectors : instance of :class:`QteaTensor`
        """
        xp = self._device_checks()

        eig_api_qtea_half = self.dtype == xp.float16

        # scipy eigsh switches for complex data types to eigs and
        # can only solve k eigenvectors of a nxn matrix with
        # k < n - 1. This leads to problems with 2x2 matrices
        # where one can get not even one eigenvector.
        eig_api_qtea_dim2 = self.is_dtype_complex() and (np.prod(self.shape) == 2)

        if eig_api_qtea_half or eig_api_qtea_dim2:
            val, vec = self.eig_api_qtea(
                matvec_func,
                conv_params,
                args_func=args_func,
                kwargs_func=kwargs_func,
            )

            # Half precision had problems with normalization (most likely
            # as eigh is executed on higher precision
            vec /= vec.norm_sqrt()

            return val, vec

        return self.eig_api_arpack(
            matvec_func,
            links,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
        )

    def eig_api_qtea(self, matvec_func, conv_params, args_func=None, kwargs_func=None):
        """
        Interface to hermitian eigenproblem via qtealeaves.solvers. Arguments see `eig_api`.
        """
        solver = EigenSolverH(
            self,
            matvec_func,
            conv_params,
            args_func=args_func,
            kwargs_func=kwargs_func,
        )

        return solver.solve()

    def eig_api_arpack(
        self, matvec_func, links, conv_params, args_func=None, kwargs_func=None
    ):
        """
        Interface to hermitian eigenproblem via Arpack. Arguments see `eig_api`.
        """
        if args_func is None:
            args_func = []

        if kwargs_func is None:
            kwargs_func = {}

        xp = self._device_checks()
        kwargs, linear_operator, eigsh = self.prepare_eig_api(conv_params)

        def my_matvec(
            vec,
            func=matvec_func,
            this=self,
            links=links,
            xp=xp,
            args=args_func,
            kwargs=kwargs_func,
        ):
            if isinstance(vec, xp.ndarray):
                tens = this.from_elem_array(vec, dtype=self.dtype, device=self.device)
                tens.reshape_update(links)
            else:
                raise Exception("unknown type")

            tens = -func(tens, *args, **kwargs)

            return tens._elem.reshape(-1)

        ham_dim = int(np.prod(links))
        lin_op = linear_operator((ham_dim, ham_dim), matvec=my_matvec)

        if "v0" in kwargs:
            kwargs["v0"] = self._elem.reshape(-1)

        eigenvalues, eigenvectors = eigsh(lin_op, **kwargs)

        return -eigenvalues, self.from_elem_array(
            eigenvectors.reshape(links), dtype=self.dtype, device=self.device
        )

    # pylint: disable-next=unused-argument
    def fuse_links_update(self, fuse_low, fuse_high, is_link_outgoing=True):
        """
        Fuses one set of links to a single link (inplace-update).

        Parameters
        ----------
        fuse_low : int
            First index to fuse
        fuse_high : int
            Last index to fuse.

        Example: if you want to fuse links 1, 2, and 3, fuse_low=1, fuse_high=3.
        Therefore the function requires links to be already sorted before in the
        correct order.
        """
        shape = list(self.shape[:fuse_low])
        shape += [np.prod(self.shape[fuse_low : fuse_high + 1])]
        shape += list(self.shape[fuse_high + 1 :])

        self.reshape_update(shape)

    def getsizeof(self):
        """Size in memory (approximate, e.g., without considering meta data)."""
        # Enable fast switch, previously use sys.getsizeof had trouble
        # in resolving size, numpy attribute is only for array without
        # metadata, but metadata like dimensions is only small overhead.
        # (fast switch if we want to use another approach for estimating
        # the size of a numpy array)
        return self._elem.nbytes

    def get_entry(self):
        """Get entry if scalar on host."""
        if np.prod(self.shape) != 1:
            raise Exception("Cannot get entry, more than one.")

        if self.device == "gpu":
            return self._elem.get().reshape(-1)[0]

        return self._elem.reshape(-1)[0]

    def mpi_send(self, to_, comm, tn_mpi_types):
        """
        Send tensor via MPI.

        **Arguments**

        to : integer
            MPI process to send tensor to.

        comm : instance of MPI communicator to be used

        tn_mpi_types : dict
            Dictionary mapping dtype to MPI data types.
        """

        # Send the dim of the shape
        comm.send(self.ndim, to_)

        # Send the shape first
        shape = np.array(list(self.shape), dtype=int)
        comm.Send([shape, tn_mpi_types["<i8"]], to_)

        # Send the tensor
        if hasattr(self._elem, "get"):
            elem = self._elem.get()
        else:
            elem = self._elem
        comm.Send([np.ascontiguousarray(elem), tn_mpi_types[self._elem.dtype.str]], to_)

    @classmethod
    def mpi_recv(cls, from_, comm, tn_mpi_types, tensor_backend):
        """
        Send tensor via MPI.

        **Arguments**

        from_ : integer
            MPI process to receive tensor from.

        comm : instance of MPI communicator to be used

        tn_mpi_types : dict
            Dictionary mapping dtype to MPI data types.

        tensor_backend : instance of :class:`TensorBackend`
        """
        # Receive the number of legs
        ndim = comm.recv(source=from_)

        # Receive the shape
        shape = np.empty(ndim, dtype=int)
        comm.Recv([shape, tn_mpi_types["<i8"]], from_)

        dtype = tensor_backend.dtype
        obj = cls(shape, ctrl="N", dtype=dtype, device="cpu")

        # Receive the tensor
        comm.Recv([obj._elem, tn_mpi_types[np.dtype(dtype).str]], from_)

        obj.convert(dtype, tensor_backend.device)

        return obj

    def norm(self):
        """Calculate the norm of the tensor <tensor|tensor>."""
        xp = self._device_checks()
        cidxs = np.arange(self.ndim)
        return xp.real(xp.tensordot(self._elem, self._elem.conj(), (cidxs, cidxs)))

    def norm_sqrt(self):
        """
        Calculate the square root of the norm of the tensor,
        i.e., sqrt( <tensor|tensor>).
        """
        xp = self._device_checks()
        norm = self.norm()
        return xp.sqrt(norm)

    def normalize(self):
        """Normalize tensor with sqrt(<tensor|tensor>)."""
        self._elem /= self.norm_sqrt()

    def remove_dummy_link(self, position):
        """Remove the dummy link at given position (inplace update)."""
        if self.shape[position] != 1:
            raise Exception(
                "Can only remove links with dimension 1. "
                + f"({self.shape[position]} at {position})"
            )
        # Could use xp.squeeze
        new_shape = list(self.shape)[:position] + list(self.shape)[position + 1 :]
        self.reshape_update(new_shape)
        return self

    def scale_link(self, link_weights, link_idx):
        """
        Scale tensor along one link at `link_idx` with weights.

        **Arguments**

        link_weights : np.ndarray
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.

        **Returns**

        updated_link : instance of :class:`QteaTensor`
        """
        xp = self._device_checks()
        diag = self.from_elem_array(xp.diag(link_weights), self.dtype, self.device)

        if link_idx == 0:
            tmp = diag.tensordot(self, ([0], [link_idx]))
        elif link_idx + 1 == self.ndim:
            tmp = self.tensordot(diag, ([link_idx], [0]))
        else:
            # Need permutation
            tmp = self.tensordot(diag, ([link_idx], [0]))

            # Last index is nn = (length - 1)
            nn = self.ndim - 1
            perm = list(range(link_idx)) + [nn] + list(range(link_idx, nn))

            tmp = tmp.transpose(perm)

        return tmp

    def scale_link_update(self, link_weights, link_idx):
        """
        Scale tensor along one link at `link_idx` with weights (inplace update).

        **Arguments**

        link_weights : np.ndarray
            Scalar weights, e.g., singular values.

        link_idx : int
            Link which should be scaled.
        """
        if link_idx == 0:
            shape = list(self.shape)
            d1 = shape[0]
            d2 = np.prod(shape[1:])
            self.reshape_update((d1, d2))

            for ii, scalar in enumerate(link_weights):
                self._elem[ii, :] *= scalar

            self.reshape_update(shape)
            return self

        if link_idx + 1 == self.ndim:
            # For last link xp.multiply will do the job as the
            # last index is one memory block anyway
            self._elem[:] = self._elem * link_weights
            return self

        # Need permutation
        t_shape = np.array(self.shape)
        contr_legs = [link_idx]
        not_contr_legs = self._invert_link_selection(contr_legs)

        # Transpose and reshape in matrix
        transposition = not_contr_legs + contr_legs
        matrix = self._elem.transpose(transposition).reshape(
            -1, np.prod(t_shape[contr_legs])
        )

        # * is shorthand for xp.multiply (see link_idx = 0)
        matrix = matrix * link_weights

        self._elem[:] = matrix.reshape(t_shape[transposition]).transpose(
            np.argsort(transposition)
        )

        return self

    def set_diagonal_entry(self, position, value):
        """Set the diagonal element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise Exception("Can only run on rank-2 tensor.")
        self._elem[position, position] = value

    def set_matrix_entry(self, idx_row, idx_col, value):
        """Set one element in a rank-2 tensor (inplace update)"""
        if self.ndim != 2:
            raise Exception("Can only run on rank-2 tensor.")
        self._elem[idx_row, idx_col] = value

    def set_subtensor_entry(self, corner_low, corner_high, tensor):
        """
        Set a subtensor (potentially expensive as looping explicitly, inplace update).

        **Arguments**

        corner_low : list of ints
            The lower index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        corner_high : list of ints
            The higher index of each dimension of the tensor to set. Length
            must match rank of tensor `self`.

        tensor : :class:`QteaTensor`
           Tensor to be set as subtensor. Rank must match tensor `self`.
           Dimensions must match `corner_high - corner_low`.

        **Examples**

        To set the tensor of shape 2x2x2 in a larger tensor `self` of shape
        8x8x8 the corresponing call is in comparison to a numpy syntax:

        * self.set_subtensor_entry([2, 4, 2], [4, 6, 4], tensor)
        * self[2:4, 4:6, 2:4] = tensor

        To be able to work with all ranks, we currently avoid the numpy
        syntax in our implementation.
        """
        lists = []
        for ii, corner_ii in enumerate(corner_low):
            corner_jj = corner_high[ii]
            lists.append(list(range(corner_ii, corner_jj)))

        shape = self.elem.shape
        cdim = np.cumsum(np.array(shape, dtype=int))
        cdim = np.array(list(cdim[1:]) + [1], dtype=int)
        self.elem = self.elem.flatten()

        kk = -1
        for elem in itertools.product(*lists):
            kk += 1
            elem = np.array(elem, dtype=int)
            idx = np.sum(elem * cdim)

            self.elem[idx] = tensor[kk]

        self.elem = self.elem.reshape(shape)

    def to_dense(self, true_copy=False):
        """Return dense tensor (if `true_copy=False`, same object may be returned)."""
        if true_copy:
            return self.copy()

        return self

    def to_dense_singvals(self, s_vals, true_copy=False):
        """Convert singular values to dense vector without symmetries."""
        if true_copy:
            return s_vals.copy()

        return s_vals

    def trace(self, return_real_part=False, do_get=False):
        """Take the trace of a rank-2 tensor."""
        xp = self._device_checks()

        if self.ndim != 2:
            raise Exception("Can only run on rank-2 tensor.")

        value = xp.trace(self._elem)

        if return_real_part:
            value = xp.real(value)

        if self.device == "gpu" and do_get:
            value = value.get()

        return value

    def trace_one_dim_pair(self, links):
        """Trace a pair of links with dimenion one. Inplace update."""
        if len(links) != 2:
            raise Exception("Can only run on pair of links")

        ii = min(links[0], links[1])
        jj = max(links[1], links[0])

        if ii == jj:
            raise Exception("Same link.")

        self.remove_dummy_link(jj)
        self.remove_dummy_link(ii)

        return self

    def transpose(self, permutation):
        """Permute the links of the tensor and return new tensor."""
        tens = QteaTensor(None, ctrl=None, dtype=self.dtype, device=self.device)
        tens._elem = self._elem.transpose(permutation)
        return tens

    def transpose_update(self, permutation):
        """Permute the links of the tensor inplace."""
        self._elem = self._elem.transpose(permutation)

    def write(self, filehandle, cmplx=None):
        """
        Write tensor in original Fortran compatible way.

        **Details**

        1) Number of links
        2) Line with link dimensions
        3) Entries of tensors line-by-line in column-major ordering.
        """
        xp = self._device_checks()

        if cmplx is None:
            cmplx = xp.sum(xp.abs(xp.imag(self.elem))) > 1e-15

        write_tensor(self.elem, filehandle, cmplx=cmplx)

    # --------------------------------------------------------------------------
    #                         Two-tensor operations
    # --------------------------------------------------------------------------

    def add_update(self, other, factor_this=None, factor_other=None):
        """
        Inplace addition as `self = factor_this * self + factor_other * other`.

        **Arguments**

        other : same instance as `self`
            Will be added to `self`. Unmodified on exit.

        factor_this : scalar
            Scalar weight for tensor `self`.

        factor_other : scalar
            Scalar weight for tensor `other`
        """
        if (factor_this is None) and (factor_other is None):
            self._elem += other._elem
            return

        if factor_this is not None:
            self._elem *= factor_this

        if factor_other is None:
            self._elem += other._elem
            return

        self._elem += factor_other * other._elem

    def dot(self, other):
        """Inner product of two tensors <self|other>."""
        xp = self._device_checks()
        return xp.vdot(other._elem.reshape(-1), self._elem.reshape(-1))

    def expand_link_tensorpair(self, other, link_self, link_other, new_dim, ctrl="R"):
        """
        Expand the link between a pair of tensors. If ctrl="R", the expansion is random

        **Arguments**

        other : instance of :class`QteaTensor`

        link_self : int
            Expand this link in `self`

        link_other : int
            Expand this link in `other`. Link must be a match (dimension etc.)

        ctrl : str, optional
            How to fill the extension. Default to "R" (random)

        **Returns**

        new_this : instance of :class`QteaTensor`
            Expanded version of `self`

        new_other : instance of :class`QteaTensor`
            Expanded version of `other`
        """
        new_this = self._expand_tensor(link_self, new_dim, ctrl=ctrl)
        new_other = other._expand_tensor(link_other, new_dim, ctrl=ctrl)

        return new_this, new_other

    # pylint: disable-next=unused-argument
    def split_qr(
        self,
        legs_left,
        legs_right,
        perm_left=None,
        perm_right=None,
        is_q_link_outgoing=True,
    ):
        """
        Split the tensor via a QR decomposition.

        Parameters
        ----------

        self : instance of :class:`QteaTensor`
            Tensor upon which apply the QR
        legs_left : list of int
            Legs that will compose the rows of the matrix
        legs_right : list of int
            Legs that will compose the columns of the matrix
        perm_left : list of int, optional
            permutations of legs after the QR on left tensor
        perm_right : list of int, optional
            permutation of legs after the QR on right tensor

        Returns
        -------

        tens_left: instance of :class:`QteaTensor`
            unitary tensor after the QR, i.e., Q.
        tens_right: instance of :class:`QteaTensor`
            upper triangular tensor after the QR, i.e., R
        """
        xp = self._device_checks()

        legs_l = np.array(legs_left)
        legs_r = np.array(legs_right)
        is_good_bipartition = np.max(legs_l) < np.min(legs_r)
        is_sorted_l = (
            True if (legs_l.ndim < 2) else np.all(legs_l[1:] - legs_l[:-1] > 0)
        )
        is_sorted_r = (
            True if (legs_r.ndim < 2) else np.all(legs_r[1:] - legs_r[:-1] > 0)
        )

        if is_good_bipartition and is_sorted_l and is_sorted_r:
            d1 = np.prod(np.array(self.shape)[legs_left])
            d2 = np.prod(np.array(self.shape)[legs_right])

            tens_left, tens_right = self._split_qr_dim(d1, d2)

            k_dim = tens_right.shape[0]

            tens_left.reshape_update(list(np.array(self.shape)[legs_left]) + [k_dim])
            tens_right.reshape_update([k_dim] + list(np.array(self.shape)[legs_right]))

        else:
            # Reshaping
            matrix = self._elem.transpose(legs_left + legs_right)
            shape_left = np.array(self.shape)[legs_left]
            shape_right = np.array(self.shape)[legs_right]
            matrix = matrix.reshape(np.prod(shape_left), np.prod(shape_right))
            k_dim = np.min([matrix.shape[0], matrix.shape[1]])

            if self.dtype == xp.float16:
                matrix = matrix.astype(xp.float32)

            # QR decomposition
            mat_left, mat_right = xp.linalg.qr(matrix)

            if self.dtype == xp.float16:
                mat_left = mat_left.astype(xp.float16)
                mat_right = mat_right.astype(xp.float16)

            # Reshape back to tensors
            tens_left = QteaTensor.from_elem_array(
                mat_left.reshape(list(shape_left) + [k_dim]),
                dtype=self.dtype,
                device=self.device,
            )
            tens_right = QteaTensor.from_elem_array(
                mat_right.reshape([k_dim] + list(shape_right)),
                dtype=self.dtype,
                device=self.device,
            )

        if perm_left is not None:
            tens_left.transpose_update(perm_left)

        if perm_right is not None:
            tens_right.transpose_update(perm_right)

        return tens_left, tens_right

    # pylint: disable-next=unused-argument
    def split_qrte(
        self,
        tens_right,
        singvals_self,
        operator=None,
        conv_params=None,
        is_q_link_outgoing=True,
    ):
        """
        Perform an Truncated ExpandedQR decomposition, generalizing the idea
        of https://arxiv.org/pdf/2212.09782.pdf for a general bond expansion
        given the isometry center of the network on  `tens_left`.
        It should be rather general for three-legs tensors, and thus applicable
        with any tensor network ansatz. Notice that, however, you do not have
        full control on the approximation, since you know only a subset of the
        singular values truncated.

        Parameters
        ----------
        tens_left: xp.array
            Left tensor
        tens_right: xp.array
            Right tensor
        singvals_left: xp.array
            Singular values array insisting on the link to the left of `tens_left`
        operator: xp.array or None
            Operator to contract with the tensors. If None, no operator is contracted

        Returns
        -------
        tens_left: ndarray
            left tensor after the EQR
        tens_right: ndarray
            right tensor after the EQR
        singvals: ndarray
            singular values kept after the EQR
        singvals_cutted: ndarray
            subset of thesingular values cutted after the EQR,
            normalized with the biggest singval
        """
        xp = self._device_checks()

        if conv_params is None:
            conv_params = TNConvergenceParameters()
            warnings.warn("Using default convergence parameters.")
        elif not isinstance(conv_params, TNConvergenceParameters):
            raise ValueError(
                "conv_params must be TNConvergenceParameters or None, "
                + f"not {type(conv_params)}."
            )

        # Trial bond dimension
        eta = int(np.ceil((1 + conv_params.min_expansion_qr) * self.shape[0]))

        # Contract the two tensors together
        twotensors = xp.tensordot(self._elem, tens_right._elem, (2, 0))
        twotensors = xp.tensordot(xp.diag(singvals_self), twotensors, (1, 0))

        # Contract with the operator if present
        if operator is not None:
            twotensors = xp.tensordot(twotensors, operator._elem, ([1, 2], [2, 3]))
        # For simplicity, transpose in the same order as obtained
        # after the application of the operator
        else:
            twotensors = twotensors.transpose(0, 3, 1, 2)

        # Apply first phase in expanding the bond dimension
        expansor = xp.eye(eta, np.prod(self.shape[:2])).reshape(eta, *self.shape[:2])
        expanded_y0 = xp.tensordot(expansor, twotensors, ([1, 2], [0, 2]))
        expanded_y0 = expanded_y0.transpose([0, 2, 1])

        # Contract with the (i+1)th site dagger
        first_qr = xp.tensordot(twotensors, expanded_y0.conj(), ([1, 3], [2, 1]))
        first_q, _ = xp.linalg.qr(first_qr.reshape(-1, first_qr.shape[2]))
        first_q = first_q.reshape(first_qr.shape)

        # Contract the new q with the i-th site. The we would need a rq decomposition.
        second_qr = xp.tensordot(twotensors, first_q.conj(), ([0, 2], [0, 1]))
        second_qr = second_qr.transpose(2, 1, 0)
        second_q, second_r = xp.linalg.qr(second_qr.reshape(second_qr.shape[0], -1).T)
        second_q = second_q.T.reshape(second_qr.shape)
        # To get the real R matrix I would have to transpose, but to avoid a double
        # transposition I simply avoid that
        # second_r = second_r.T

        # Second phase in the expansor
        eigvl, eigvc = xp.linalg.eigh(second_r.conj() @ second_r.T)
        # Singvals are sqrt of eigenvalues, and sorted in the opposite order
        singvals = xp.sqrt(eigvl)[::-1]

        # Routine to select the bond dimension
        cut, singvals, singvals_cutted = self._truncate_singvals(singvals)
        tens_right = xp.tensordot(eigvc[:cut, ::-1], second_q, ([1], [0]))

        # Get the last tensor
        tens_left = xp.tensordot(twotensors, tens_right.conj(), ([1, 3], [2, 1]))

        tens_left = self.from_elem_array(
            tens_left, dtype=self.dtype, device=self.device
        )
        tens_right = self.from_elem_array(
            tens_right, dtype=self.dtype, device=self.device
        )

        return tens_left, tens_right, singvals, singvals_cutted

    # pylint: disable-next=unused-argument
    # pylint: disable-next=too-many-branches
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
        """
        Perform a truncated Singular Value Decomposition by
        first reshaping the tensor into a legs_left x legs_right
        matrix, and permuting the legs of the ouput tensors if needed.
        If the contract_singvals = ('L', 'R') it takes care of
        renormalizing the output tensors such that the norm of
        the MPS remains 1 even after a truncation.

        Parameters
        ----------
        self : instance of :class:`QteaTensor`
            Tensor upon which apply the SVD
        legs_left : list of int
            Legs that will compose the rows of the matrix
        legs_right : list of int
            Legs that will compose the columns of the matrix
        perm_left : list of int, optional
            permutations of legs after the SVD on left tensor
        perm_right : list of int, optional
            permutation of legs after the SVD on right tensor
        contract_singvals: string, optional
            How to contract the singular values.
                'N' : no contraction
                'L' : to the left tensor
                'R' : to the right tensor
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure. If None is given,
            then use the default convergence parameters of the TN.
            Default to None.
        no_truncation : boolean, optional
            Allow to run without truncation
            Default to `False` (hence truncating by default)

        Returns
        -------
        tens_left: instance of :class:`QteaTensor`
            left tensor after the SVD
        tens_right: instance of :class:`QteaTensor`
            right tensor after the SVD
        singvals: xp.ndarray
            singular values kept after the SVD
        singvals_cut: xp.ndarray
            singular values cut after the SVD, normalized with the biggest singval
        """
        xp = self._device_checks()
        tensor = self._elem

        # Reshaping
        matrix = tensor.transpose(legs_left + legs_right)
        shape_left = np.array(tensor.shape)[legs_left]
        shape_right = np.array(tensor.shape)[legs_right]
        matrix = matrix.reshape([np.prod(shape_left), np.prod(shape_right)])

        if conv_params is None:
            svd_ctrl = "A"
            max_bond_dimension = min(matrix.shape)
        else:
            svd_ctrl = conv_params.svd_ctrl
            max_bond_dimension = conv_params.max_bond_dimension

        svd_ctrl = _process_svd_ctrl(
            svd_ctrl,
            max_bond_dimension,
            matrix.shape,
            self.device,
            contract_singvals,
        )
        if matrix.dtype == xp.float16:
            matrix = matrix.astype(xp.float32)

        # SVD decomposition
        if svd_ctrl in ("D", "V"):
            mat_left, singvals_tot, mat_right = self._normal_svd(matrix)
        elif svd_ctrl in ("E", "X"):
            mat_left, singvals_tot, mat_right = self._eigvl_svd(
                matrix,
                svd_ctrl,
                conv_params.max_bond_dimension,
                contract_singvals,
            )
        elif svd_ctrl == "R":
            mat_left, singvals_tot, mat_right = self._random_svd(
                matrix, conv_params.max_bond_dimension
            )

        if self.dtype == xp.float16:
            mat_left = mat_left.astype(xp.float16)
            mat_right = mat_right.astype(xp.float16)
            singvals_tot = singvals_tot.astype(xp.float16)

        # Truncation
        if not no_truncation:
            cut, singvals, singvals_cut = self._truncate_singvals(
                singvals_tot, conv_params
            )
            mat_left = mat_left[:, :cut]
            mat_right = mat_right[:cut, :]
        else:
            singvals = singvals_tot
            singvals_cut = []  # xp.array([], dtype=self.dtype)
            cut = mat_left.shape[1]

        # Contract singular values if requested
        if svd_ctrl in ("D", "V", "R"):
            if contract_singvals.upper() == "L":
                mat_left = xp.multiply(mat_left, singvals)
            elif contract_singvals.upper() == "R":
                mat_right = xp.multiply(singvals, mat_right.T).T
            elif contract_singvals.upper() != "N":
                raise ValueError(
                    f"Contract_singvals option {contract_singvals} is not "
                    + "implemented. Choose between right (R), left (L) or None (N)."
                )

        # Reshape back to tensors
        tens_left = mat_left.reshape(list(shape_left) + [cut])
        if perm_left is not None:
            tens_left = tens_left.transpose(perm_left)

        tens_right = mat_right.reshape([cut] + list(shape_right))
        if perm_right is not None:
            tens_right = tens_right.transpose(perm_right)

        # Convert into QteaTensor
        tens_left = self.from_elem_array(
            tens_left, dtype=self.dtype, device=self.device
        )
        tens_right = self.from_elem_array(
            tens_right, dtype=self.dtype, device=self.device
        )
        return tens_left, tens_right, singvals, singvals_cut

    def _normal_svd(self, matrix):
        """
        Normal SVD of the matrix. First try the faster gesdd iterative method.
        If it fails, resort to gesvd.

        Parameters
        ----------
        matrix: xp.array
            Matrix to decompose

        Returns
        -------
        xp.array
            Matrix U
        xp.array
            Singular values
        xp.array
            Matrix V^dagger
        """
        xp = self._device_checks()
        try:
            mat_left, singvals_tot, mat_right = xp.linalg.svd(
                matrix, full_matrices=False
            )
        except np.linalg.LinAlgError:
            warnings.warn("gesdd SVD decomposition failed. Resorting to gesvd.")
            mat_left, singvals_tot, mat_right = sp.linalg.svd(
                matrix, full_matrices=False, lapack_driver="gesvd"
            )

        return mat_left, singvals_tot, mat_right

    def _eigvl_svd(self, matrix, svd_ctrl, max_bond_dimension, contract_singvals):
        """
        SVD of the matrix through an eigvenvalue decomposition.

        Parameters
        ----------
        matrix: xp.array
            Matrix to decompose
        svd_crtl : str
            If "E" normal eigenvalue decomposition. If "X" use the sparse.
        max_bond_dimension : int
            Maximum bond dimension
        contract_singvals: str
            Whhere to contract the singular values

        Returns
        -------
        xp.array
            Matrix U
        xp.array
            Singular values
        xp.array
            Matrix V^dagger

        Details
        -------

        We use ᵀ*=^†, the adjoint.

        - In the contract-to-right case, which means:
          H = AAᵀ* = USV Vᵀ*SUᵀ* = U S^2 Uᵀ*
          To compute SVᵀ* we have to use:
          A = USVᵀ* -> Uᵀ* A = S Vᵀ*
        - In the contract-to-left case, which means:
          H = Aᵀ*A = VSUᵀ* USVᵀ* = VS^2 Vᵀ*
          First, we are given V, but we want Vᵀ*. However, let's avoid double work.
          To compute US we have to use:
          A = USVᵀ* -> AV = US
          Vᵀ* = right.T.conj()   (with the conjugation done in place)
        """
        xp, xsla = self._device_checks(return_sla=True)
        # The left tensor is unitary
        if contract_singvals == "R":
            herm_mat = matrix @ matrix.conj().T
        # contract_singvals == "L", the right tensor is unitary
        else:
            herm_mat = matrix.conj().T @ matrix

        # We put the condition on the matrix being bigger than 2x2
        # for the sparse eigensolver for stability of the arpack methods
        if svd_ctrl == "E" or (herm_mat.shape[0] - 1) <= 2:
            eigenvalues, eigenvectors = xp.linalg.eigh(herm_mat)
        elif svd_ctrl == "X":
            num_eigvl = min(herm_mat.shape[0] - 1, max_bond_dimension - 1)
            # Added in case bond dimension is 1
            num_eigvl = max(num_eigvl, 1)
            eigenvalues, eigenvectors = xsla.eigsh(herm_mat, k=num_eigvl)
        else:
            raise ValueError(
                f"svd_ctrl = {svd_ctrl} not valid with eigenvalue decomposition"
            )

        # Eigenvalues are sorted ascendingly, singular values descendengly
        # Only positive eigenvalues makes sense. Due to numerical precision,
        # there will be very small negative eigvl. We put them to 0.
        eigenvalues[eigenvalues < 0] = 0
        singvals = xp.sqrt(eigenvalues[::-1][: min(matrix.shape)])
        eigenvectors = eigenvectors[:, ::-1]

        # Taking only the meaningful part of the eigenvectors
        if contract_singvals == "R":
            left = eigenvectors[:, : min(matrix.shape)]
            right = left.T.conj() @ matrix
        else:
            right = eigenvectors[:, : min(matrix.shape)]
            left = matrix @ right
            xp.conj(right.T, out=right)

        return left, singvals, right

    def _random_svd(self, matrix, max_bond_dimension):
        """
        SVD of the matrix through a random SVD decomposition
        as prescribed in page 227 of Halko, Martinsson, Tropp's 2011 SIAM paper:
        "Finding structure with randomness: Probabilistic algorithms for constructing
        approximate matrix decompositions"

        Parameters
        ----------
        matrix: xp.array
            Matrix to decompose
        max_bond_dimension : int
            Maximum bond dimension

        Returns
        -------
        xp.array
            Matrix U
        xp.array
            Singular values
        xp.array
            Matrix V^dagger
        """
        xp = self._device_checks()

        rank = min(max_bond_dimension, min(matrix.shape))
        # This could be parameterized but in the paper they use this
        # value
        n_samples = 2 * rank
        random = xp.random.randn(matrix.shape[1], n_samples)
        reduced_matrix = matrix @ random
        # Find orthonormal basis
        ortho, _ = xp.linalg.qr(reduced_matrix)

        # Second part
        to_svd = ortho.T @ matrix
        left_tilde, singvals, right = xp.linalg.svd(to_svd)
        left = ortho @ left_tilde

        return left, singvals, right

    def stack_link(self, other, link):
        """
        Stack two tensors along a given link.

        **Arguments**

        other : instance of :class:`QteaTensor`
            Links must match `self` up to the specified link.

        link : integer
            Stack along this link.

        **Returns**

        new_this : instance of :class:QteaTensor`
        """
        newdim_self = list(self.shape)
        newdim_self[link] += other.shape[link]

        d1, d2, d3 = self._shape_as_rank_3(link)
        d4 = other.shape[link]

        new_dim = d2 + d4

        new_this = QteaTensor(
            [d1, new_dim, d3], ctrl="N", dtype=self.dtype, device=self.device
        )
        new_this._elem[:, :d2, :] = self._elem.reshape([d1, d2, d3])
        new_this._elem[:, d2:, :] = other._elem.reshape([d1, d4, d3])
        new_this.reshape_update(newdim_self)

        return new_this

    def tensordot(self, other, contr_idx):
        """Tensor contraction of two tensors along the given indices."""
        xp = self._device_checks()

        if isinstance(other, xp.ndarray):
            other = QteaTensor.from_elem_array(
                other, dtype=self.dtype, device=self.device
            )
            warnings.warn("Converting tensor on the fly.")

        elem = xp.tensordot(self._elem, other._elem, contr_idx)
        tens = QteaTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)
        return tens

    # --------------------------------------------------------------------------
    #                        Internal methods
    # --------------------------------------------------------------------------
    #
    # inherit _invert_link_selection

    # --------------------------------------------------------------------------
    #                                MISC
    # --------------------------------------------------------------------------

    def get(self):
        """Get the whole array of a tensor to the host as tensor."""
        if hasattr(self._elem, "get"):
            return self.from_elem_array(self._elem.get())

        return self

    def get_of(self, variable):
        """Run the get method to transfer to host on variable (same device as self)."""
        if hasattr(variable, "get"):
            return variable.get()

        return variable

    def _shift_iso_to_qr(self, target_tens, source_link, target_link):
        """Method to shift isometry center between two tensors."""
        nn = len(self.shape)
        lnk = source_link
        s_perm = list(range(lnk)) + list(range(lnk + 1, nn)) + [lnk]
        q_perm = list(range(lnk)) + [nn - 1] + list(range(lnk, nn - 1))

        tmp = self.transpose(s_perm)
        dim = list(np.arange(tmp.ndim))

        left_mat, right_mat = tmp.split_qr(dim[:-1], dim[-1:], perm_left=q_perm)

        tmp = target_tens.tensordot(right_mat, ([target_link], [1]))

        nn = len(target_tens.shape)
        lnk = target_link
        t_perm = list(range(lnk)) + [nn - 1] + list(range(lnk, nn - 1))

        t_tens = tmp.transpose(t_perm)

        return left_mat, t_tens

    def eigvalsh(self):
        """Calculate eigendecomposition for a rank-2 tensor."""
        xp = self._device_checks()

        if self.ndim != 2:
            raise Exception("Not a matrix, hence no sqrtm possible.")

        eigvals = xp.linalg.eigvalsh(self._elem)

        return eigvals

    def sqrtm(self):
        """Calculate matrix-square-root for a rank-2 tensor."""

        if self.ndim != 2:
            raise Exception("Not a matrix, hence no sqrtm possible.")

        if self.device == "gpu":
            raise Exception("sqrtm not implemented on the GPU through cupy")

        elem = sp.linalg.sqrtm(self._elem)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def stack_first_and_last_link(self, other):
        """Stack first and last link of tensor targeting MPS addition."""
        newdim_self = list(self.shape)
        newdim_self[0] += other.shape[0]
        newdim_self[-1] += other.shape[-1]

        d1 = self.shape[0]
        d2 = np.prod(self.shape[1:-1])
        d3 = self.shape[-1]
        i1 = other.shape[0]
        i3 = other.shape[-1]

        new_dims = [d1 + i1, d2, d3 + i3]

        new_this = QteaTensor(new_dims, ctrl="Z", dtype=self.dtype, device=self.device)
        new_this._elem[:d1, :, :d3] = self._elem.reshape([d1, d2, d3])
        new_this._elem[d1:, :, d3:] = other._elem.reshape([i1, d2, i3])
        new_this.reshape_update(newdim_self)

        return new_this

    @staticmethod
    def static_is_gpu_available():
        """Returns flag if GPU is available for this tensor class."""
        return GPU_AVAILABLE

    def is_gpu_available(self):
        """Returns flag if GPU is available for this tensor class."""
        return self.static_is_gpu_available()

    # --------------------------------------------------------------------------
    #                 Methods needed for _AbstractQteaBaseTensor
    # --------------------------------------------------------------------------

    def assert_diagonal(self, tol=1e-7):
        """Check that tensor is a diagonal matrix up to tolerance."""
        xp = self._device_checks()

        if self.ndim != 2:
            raise Exception("Not a matrix, hence not the identity.")

        tmp = xp.diag(xp.diag(self._elem))
        tmp -= self._elem

        if xp.abs(tmp).max() > tol:
            raise Exception("Matrix not diagonal.")

        return

    def assert_int_values(self, tol=1e-7):
        """Check that there are only integer values in the tensor."""
        xp = self._device_checks()

        tmp = xp.round(self._elem)
        tmp -= self._elem

        if xp.abs(tmp).max() > tol:
            raise Exception("Matrix is not an integer matrix.")

        return

    def assert_real_valued(self, tol=1e-7):
        """Check that all tensor entries are real-valued."""
        xp = self._device_checks()

        tmp = xp.imag(self._elem)

        if xp.abs(tmp).max() > tol:
            raise Exception("Tensor is not real-valued.")

    def elementwise_abs_smaller_than(self, value):
        """Return boolean if each tensor element is smaller than `value`"""
        xp = self._device_checks()

        return (xp.abs(self._elem) < value).all()

    def flatten(self):
        """Returns flattened version (rank-1) of dense array in native array type."""
        return self._elem.flatten()

    @classmethod
    def from_elem_array(cls, tensor, dtype=None, device=None):
        """
        New tensor from array

        **Arguments**

        tensor : xp.ndarray
            Array for new tensor.

        dtype : data type, optional
            Can allow to specify data type.
            If not `None`, it will convert.
            Default to `None`
        """
        if dtype is None and np.issubdtype(tensor.dtype, np.integer):
            warnings.warn(
                (
                    "Initializing a tensor with integer dtype can be dangerous "
                    "for the simulation. Please specify the dtype keyword in the "
                    "from_elem_array method if it was not intentional."
                )
            )

        if dtype is None:
            dtype = tensor.dtype
        if (device is None) and (cp is None):
            # cupy not available
            device = "cpu"
        elif (device is None) and not GPU_AVAILABLE:
            # Well, cupy is there, but no GPU
            device = "cpu"
        elif device is None:
            # We can actually check with cp where we are running
            device = "cpu" if cp.get_array_module(tensor) == np else "gpu"

        obj = cls(tensor.shape, ctrl=None, dtype=dtype, device=device)
        obj._elem = tensor

        obj.convert(dtype, device)

        return obj

    def get_attr(self, *args):
        """High-risk resolve attribute for an operation on an elementary array."""
        xp = self._device_checks()

        attributes = []

        for elem in args:
            if not hasattr(xp, elem):
                raise Exception(
                    f"This tensor's elementary array does not support {elem}."
                )

            attributes.append(getattr(xp, elem))

        if len(attributes) == 1:
            return attributes[0]

        return tuple(attributes)

    def get_argsort_func(self):
        """Return callable to argsort function."""
        xp = self._device_checks()
        return xp.argsort

    def get_diag_entries_as_int(self):
        """Return diagonal entries of rank-2 tensor as integer on host."""
        xp = self._device_checks()

        if self.ndim != 2:
            raise Exception("Not a matrix, cannot get diagonal.")

        tmp = xp.diag(self._elem)
        if self.device == "gpu":
            tmp = tmp.get()

        return xp.real(tmp).astype(int)

    def get_sqrt_func(self):
        """Return callable to sqrt function."""
        xp = self._device_checks()
        return xp.sqrt

    def get_submatrix(self, row_range, col_range):
        """Extract a submatrix of a rank-2 tensor for the given rows / cols."""
        if self.ndim != 2:
            raise Exception("Cannot only set submatrix for rank-2 tensors.")

        r1, r2 = row_range
        c1, c2 = col_range

        return self.from_elem_array(
            self._elem[r1:r2, c1:c2], dtype=self.dtype, device=self.device
        )

    def permute_rows_cols_update(self, inds):
        """Permute rows and columns of rank-2 tensor with `inds`. Inplace update."""
        if self.ndim != 2:
            raise Exception("Cannot only permute rows & cols for rank-2 tensors.")

        tmp = self._elem[inds, :][:, inds]
        self._elem *= 0.0
        self._elem += tmp
        return self

    def prepare_eig_api(self, conv_params):
        """
        Return xp variables for eigsh.

        **Returns**

        kwargs : dict
            Keyword arguments for eigs call.
            If initial guess can be passed, key "v0" is
            set with value `None`

        LinearOperator : callable
            Function generating a LinearOperator

        eigsh : callable
            Interface with actual call to eigsh
        """
        _, xsla = self._device_checks(return_sla=True)

        tolerance = conv_params.sim_params["arnoldi_min_tolerance"]

        kwargs = {
            "k": 1,
            "which": "LA",
            "ncv": None,
            "maxiter": None,
            "tol": tolerance,
            "return_eigenvectors": True,
        }

        if self.device == "cpu":
            kwargs["v0"] = None

        return kwargs, xsla.LinearOperator, xsla.eigsh

    def reshape(self, shape, **kwargs):
        """Reshape a tensor."""
        elem = self._elem.reshape(shape, **kwargs)
        tens = QteaTensor.from_elem_array(elem, dtype=self.dtype, device=self.device)
        return tens

    def reshape_update(self, shape, **kwargs):
        """Reshape tensor dimensions inplace."""
        self._elem = self._elem.reshape(shape)

    def set_submatrix(self, row_range, col_range, tensor):
        """Set a submatrix of a rank-2 tensor for the given rows / cols."""

        if self.ndim != 2:
            raise Exception("Cannot only set submatrix for rank-2 tensors.")

        r1, r2 = row_range
        c1, c2 = col_range

        self._elem[r1:r2, c1:c2] = tensor._elem.reshape(r2 - r1, c2 - c1)

    def subtensor_along_link(self, link, lower, upper):
        """
        Extract and return a subtensor select range (lower, upper) for one line.
        """
        d1, d2, d3 = self._shape_as_rank_3(link)

        elem = self._elem.reshape([d1, d2, d3])
        elem = elem[:, lower:upper, :]

        new_shape = list(self.shape)
        new_shape[link] = upper - lower
        elem = elem.reshape(new_shape)

        return self.from_elem_array(elem, dtype=self.dtype, device=self.device)

    def _truncate_singvals(self, singvals, conv_params=None):
        """
        Truncate the singular values followling the
        strategy selected in the convergence parameters class

        Parameters
        ----------
        singvals : np.ndarray
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure. If None is given,
            then use the default convergence parameters of the TN.
            Default to None.

        Returns
        -------
        cut : int
            Number of singular values kept
        singvals_kept : np.ndarray
            Normalized singular values kept
        singvals_cutted : np.ndarray
            Normalized singular values cutted
        """

        if conv_params is None:
            conv_params = TNConvergenceParameters()
            warnings.warn("Using default convergence parameters.")
        elif not isinstance(conv_params, TNConvergenceParameters):
            raise ValueError(
                "conv_params must be TNConvergenceParameters or None, "
                + f"not {type(conv_params)}."
            )

        if conv_params.trunc_method == "R":
            cut = self._truncate_sv_ratio(singvals, conv_params)
        elif conv_params.trunc_method == "N":
            cut = self._truncate_sv_norm(singvals, conv_params)
        else:
            raise Exception(f"Unkown trunc_method {conv_params.trunc_method}")

        # Divide singvals in kept and cut
        singvals_kept = singvals[:cut]
        singvals_cutted = singvals[cut:]
        # Renormalizing the singular values vector to its norm
        # before the truncation
        norm_kept = (singvals_kept**2).sum()
        norm_trunc = (singvals_cutted**2).sum()
        normalization_factor = np.sqrt(norm_kept) / np.sqrt(norm_kept + norm_trunc)
        singvals_kept /= normalization_factor

        # Renormalize cut singular values to track the norm loss
        singvals_cutted /= np.sqrt(norm_trunc + norm_kept)

        return cut, singvals_kept, singvals_cutted

    def vector_with_dim_like(self, dim, dtype=None):
        """Generate a vector in the native array of the base tensor."""
        xp = self._device_checks()

        if dtype is None:
            dtype = self.dtype

        return xp.ndarray(dim, dtype=dtype)

    # --------------------------------------------------------------------------
    #             Internal methods (not required by abstract class)
    # --------------------------------------------------------------------------

    def _device_checks(self, return_sla=False):
        """
        Check if all the arguments of the function where
        _device_checks is called are on the correct device,
        select the correct

        Parameters
        ----------
        device : str
            Device where the computation should take place.
            If called inside an emulator it should be the
            emulator device
        return_sla : bool, optional
            If True, returns the handle to the sparse linear algebra.
            Either sp.sparse.linalg or cp.scipy.sparse.linalg.
            Default to False.

        Returns
        -------
        module handle
            cp if the device is GPU
            np if the device is CPU
        """
        if self.device is None:
            raise Exception("None is only valid device in conversion.")

        if self.device in ("cpu") or not GPU_AVAILABLE:
            xp = np
            xsla = ssla
        else:
            xp = cp
            xsla = csla

        if return_sla:
            return xp, xsla

        return xp

    def _expand_tensor(self, link, new_dim, ctrl="R"):
        """Expand  tensor along given link and to new dimension."""
        newdim = list(self.shape)
        newdim[link] = new_dim - newdim[link]

        expansion = QteaTensor(newdim, ctrl=ctrl, dtype=self.dtype, device=self.device)

        return self.stack_link(expansion, link)

    def _shape_as_rank_3(self, link):
        """Calculate the shape as rank-3, i.e., before-link, link, after-link."""
        if link > 0:
            d1 = int(np.prod(list(self.shape)[:link]))
        else:
            d1 = 1

        d2 = self.shape[link]

        if link == self.ndim - 1:
            d3 = 1
        else:
            d3 = int(np.prod(list(self.shape)[link + 1 :]))

        return d1, d2, d3

    def _split_qr_dim(self, rows, cols):
        """Split via QR knowing dimension of rows and columns."""
        xp = self._device_checks()

        if self.dtype == xp.float16:
            matrix = self._elem.astype(xp.float32).reshape(rows, cols)
            qmat, rmat = xp.linalg.qr(matrix)
            qmat = qmat.astype(xp.float16)
            rmat = rmat.astype(xp.float16)
        else:
            qmat, rmat = xp.linalg.qr(self._elem.reshape(rows, cols))

        qtens = QteaTensor.from_elem_array(qmat, dtype=self.dtype, device=self.device)
        rtens = QteaTensor.from_elem_array(rmat, dtype=self.dtype, device=self.device)

        return qtens, rtens

    def _truncate_sv_ratio(self, singvals, conv_params):
        """
        Truncate the singular values based on the ratio
        with the bigger one

        Parameters
        ----------
        singvals : np.ndarray
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure.

        Returns
        -------
        cut : int
            Number of singular values kept
        """
        xp = self._device_checks()

        # Truncation
        lambda1 = singvals[0]
        cut = xp.nonzero(singvals / lambda1 < conv_params.cut_ratio)[0]
        if self.device == "gpu":
            cut = cut.get()

        # Confront the cut w.r.t the maximum bond dimension
        if len(cut) > 0:
            cut = min(conv_params.max_bond_dimension, cut[0])
        else:
            cut = conv_params.max_bond_dimension
        cut = min(cut, len(singvals))

        if cut < conv_params.min_bond_dimension:
            cut = min(len(singvals), conv_params.min_bond_dimension)

        return cut

    def _truncate_sv_norm(self, singvals, conv_params):
        """
        Truncate the singular values based on the
        total norm cut

        Parameters
        ----------
        singvals : np.ndarray
            Array of singular values
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure.

        Returns
        -------
        cut : int
            Number of singular values kept
        """
        xp = self._device_checks()

        norm = (singvals[::-1] ** 2).cumsum() / (singvals**2).sum()
        # You get the first index where the constraint is broken,
        # so you need to stop an index before
        cut = xp.nonzero(norm > conv_params.cut_ratio)[0]
        if self.device == "gpu":
            cut = cut.get()

        # Confront the cut w.r.t the maximum bond dimension
        if len(cut) > 0:
            cut = len(singvals) - cut[0]
            cut = min(conv_params.max_bond_dimension, cut)
        else:
            cut = conv_params.max_bond_dimension
        cut = min(cut, len(singvals))

        if cut < conv_params.min_bond_dimension:
            cut = min(len(singvals), conv_params.min_bond_dimension)

        return cut


def _process_svd_ctrl(svd_ctrl, max_bond_dim, shape, device, contract_singvals):
    """
    Process the svd_ctrl parameter for an SVD decomposition

    Parameters
    ----------
    svd_ctrl: str
        SVD identifier chosen by the user
    max_bond_dim : int
        Maximum bond dimension
    shape: Tuple[int]
        Shape of the matrix to be split
    device: str
        Device where the splitting is taking place
    contract_singvals: str
        Where to contract the singvals

    Return
    ------
    str
        The svd_ctrl after the double-check
    """
    # First, resolve selection by user
    if svd_ctrl in ("V", "D", "R"):
        return svd_ctrl
    if svd_ctrl in ("E", "X") and contract_singvals != "N":
        return svd_ctrl

    # An eigenvalue decomposition is nice if we contract the singular values
    # to the right with shape[0] < shape[1] OR
    # contract singular values to the left with shape[1] < shape[0]
    good_eigvl_decomposition = (
        shape[0] <= 3 * shape[1] and contract_singvals == "R"
    ) or (shape[1] <= 3 * shape[0] and contract_singvals == "L")

    # If none of the above works, go with automatic selection
    # First, if we do not need to compute all the singvals, use
    # sparse eigenvalue decomposition
    if min(shape) >= 2 * max_bond_dim and good_eigvl_decomposition:
        return "X"
    # Sparse problem, but with no singvals contracted on cpu,
    # use random svd decomposition
    if min(shape) >= 2 * max_bond_dim and device == "cpu":
        return "R"
    # Non-sparse problem on GPU, with singvals contracted
    # to left or right
    if device == "gpu" and good_eigvl_decomposition:
        return "E"
    # If everything else fails, we go for normal svd
    return "D"
