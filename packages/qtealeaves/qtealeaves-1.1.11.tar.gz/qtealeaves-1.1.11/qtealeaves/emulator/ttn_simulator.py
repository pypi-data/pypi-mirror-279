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
The module contains a light-weight TTN class.
"""
import warnings
from copy import deepcopy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import colors
import matplotlib.cm as cmx

from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.tooling.hilbert_curvature import map_selector
from qtealeaves.tooling.permutations import _transpose_idx
from qtealeaves.tensors import _AbstractQteaTensor
from qtealeaves.mpos import SparseMatrixOperatorPy

from .tnnode import TNnode
from .abstract_tn import _AbstractTN, _projector_for_rho_i

__all__ = ["TTN"]


class TTNLayer(list):
    """
    One layer of the TTN.

    Parameters
    ----------

    layer_idx : int
        Index of the TTN layer. The top-layer inside
        the TTN has index 0.

    local_dim : int
        Local dimension of the physical legs, which is
        set indepently of the layer containing physical
        legs or not.

    max_bond_dimension : int
        Maximum bond dimension

    max_num_links : int, optional
        Maximum number of legs of a tensor in the TTN.
        It is the sum of children and parent links.
        Default to 4.

    num_tensors : int, optional
        Number of tensor in the TTN layer.
        Default to 1.

    device: string, optional
        Device where to create the MPS. Default to 'cpu'.
        Implemented devices:
        - 'cpu'
        - 'gpu'
    """

    implemented_devices = ("cpu", "gpu")

    def __init__(
        self,
        layer_idx,
        local_dim,
        max_bond_dimension,
        max_num_links=4,
        num_tensors=1,
    ):
        super().__init__()

        self.layer_idx = layer_idx
        self.local_dim = local_dim
        self.max_bond_dimension = max_bond_dimension
        self.num_tensors = num_tensors
        self.max_num_links = max_num_links

        # Identifies the address of all neighbors in the network.
        # Each column contains the [layer, index in layer, link, type]
        # to which the neighbor is connected. The type is 1 for
        # link to child, 2 for link to parent, 3 for select, 4 for unknown.
        self.neighbors = np.zeros((4, max_num_links, num_tensors), dtype=int) - 1

        # Contains the range of physical Hilbert spaces connected to the
        # children of this tensor.
        self.sites = np.zeros((2, max_num_links, num_tensors), dtype=int) - 1

        # Contains the index of the neighboring effective operator in
        # a 1-d vector of operators. Each vector op_neighbors(:, ii)
        # contains the index of a link for the ii-th tensor in this layer.
        self.op_neighbors = np.zeros((max_num_links, num_tensors), dtype=int) - 1

        # Singular values stored.
        # -------------------- Attention ---------------------
        # This attribute store the singular values for a quick
        # computation of the bond entropy and local observables.
        # However, if they are not kept updated (such as with
        # time evolution) there should be the possibility of
        # setting them to None to avoid wrong results.
        self.singvals = [None for _ in range(num_tensors)]

        #########################################################
        ## OBSERVABLES THE SIMULATOR IS ABLE TO MEASURE IN THE ##
        ## SAME ORDER OF THE ARRAY IN TNObservables            ##
        #########################################################
        self.is_measured = [
            True,  # TNObsLocal
            True,  # TNObsCorr
            True,  # TNDistance2Pure
            True,  # TnState2File
            True,  # TNObsTensorProduct
            True,  # TNObsWeightedSum
            True,  # TNObsProjective
            True,  # TNObsProbabilities
            True,  # TNObsBondEntropy
            False,  # TNObsTZeroCorr
            False,  # TNObsCorr4
            False,  # TNObsCustom
        ]

    @property
    def cc_tensors(self):
        """
        complex conjugate part of TTO layer, returns complex conjugated tensors
        """
        c_conj = [elem.conj() for elem in self]
        return c_conj

    @property
    def is_ttn_toplayer(self):
        """
        True if it is a top layer of the TTN ansatz
        """
        return self.layer_idx == 0 and self.num_tensors == 2

    @classmethod
    def from_tensorlist(
        cls, tensor_list, local_dim=2, max_bond_dimension=None, device="cpu"
    ):
        """
        Initialize the TTN layer tensors using a list of tensors

        Parameters
        ----------
        tensor_list : list of xp.ndarray
            list of tensors for initializing the TTN layer
        local_dim  : int or array-like
            local Hilbert space dimension
        max_bond_dimension : int
            Maximum bond dimension of the layer
        device: str, optional
            Device where the computations will take place

        Returns
        -------
        TTNLayer
            TTNLayer with given tensors
        """
        if not isinstance(tensor_list, list):
            raise TypeError("Input tensors must be stored in a list")
        num_tensors = len(tensor_list)
        if max_bond_dimension is None:
            max_bond_dimension = np.max([tens.shape for tens in tensor_list])
        max_num_links = np.max([tens.ndim for tens in tensor_list])
        layer_idx = int(np.log2(len(tensor_list)))

        obj = cls(layer_idx, local_dim, max_bond_dimension, max_num_links, num_tensors)
        obj[:] = tensor_list

        obj.convert(None, device)

        return obj

    def to_dense(self, true_copy=False):
        """Return layer without symmetric tensors."""
        tensor_list = []
        for elem in self:
            tensor_list.append(elem.to_dense(true_copy=true_copy))

        obj = self.from_tensorlist(
            tensor_list,
            local_dim=self.local_dim,
            max_bond_dimension=self.max_bond_dimension,
        )

        for ii, elem in enumerate(self.singvals):
            if elem is None:
                continue

            s_vals = self[ii].to_dense_singvals(elem, true_copy=true_copy)
            obj.singvals[ii] = s_vals

        return obj

    def initialize_layer(
        self,
        tensor_shape,
        tensor_backend,
        initialization="random",
        isometry=True,
        sectors={},
    ):
        """
        Initialize the layer with random tensor of shape tensor_shape.
        The only exception is the first tensor of the first layer,
        that has shape (*tensor_shape, 1) to encode the symmetry

        Parameters
        ----------
        tensor_shape : list
            shape of the tensor
        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.
        initialization : str, optional
            Strategy for the initialization. Available strategies are:
            - "random", all tensors initialized at random
            - "empty", layer initialized with no tensors
            - "ground", layer initialized in the state |00....0>
            Default to "random".
        isometry : bool, optional
            If True, the tree is initialized as isometry, by default True
        sectors : dict, optional
            Can restrict symmetry sector and/or bond dimension in initialization.
            If empty, no restriction.
            Default to empty dictionary.
        """
        if initialization == "empty":
            return

        link_dirs = [False, False, True]

        # For symmetries, we need to handle TTN top layer manually (completely)
        if self.is_ttn_toplayer and self.layer_idx == 0:
            # Right tensor first
            tshape = tensor_shape
            sector = sectors.get((0, 1), None)
            if sector is not None:
                tshape[-1].restrict_irreps(sector)
            rows = list(range(len(tshape)))[:-1]
            cols = list(range(len(tshape)))[-1:]

            tensor = tensor_backend.tensor_cls(
                tshape,
                ctrl=initialization,
                are_links_outgoing=link_dirs,
                **tensor_backend.tensor_cls_kwargs(),
            )

            if isometry:
                tensor, _ = tensor.split_qr(rows, cols)

            tensor_1 = tensor

            # Left tensor (last link is global symmetry sector!)
            link_dirs = [False, False, False, True]
            ini_bond_dimension = tshape[-1].shape if tensor.has_symmetry else 1
            links = tensor_backend.tensor_cls.set_missing_link(
                [tshape[0], tshape[1], tshape[2], None],
                ini_bond_dimension,
                are_links_outgoing=[False, False, False, True],
            )

            sector = sectors.get((0, 0), None)
            if sector is not None:
                # pylint: disable-next=no-member
                links[-1].restrict_irreps(sector)

            tensor = tensor_backend.tensor_cls(
                links,
                ctrl=initialization,
                are_links_outgoing=link_dirs,
                **tensor_backend.tensor_cls_kwargs(),
            )

            if isometry:
                # Normalization only make sense if other tensors are isometrized
                tensor.normalize()

            self.append(tensor)
            self.append(tensor_1)
        else:
            for ii in range(self.num_tensors):
                tshape = tensor_shape
                sector = sectors.get((self.layer_idx, ii), None)
                if sector is not None:
                    tshape[-1].restrict_irreps(sector)
                rows = list(range(len(tshape)))[:-1]
                cols = list(range(len(tshape)))[-1:]

                tensor = tensor_backend.tensor_cls(
                    tshape,
                    ctrl=initialization,
                    are_links_outgoing=link_dirs,
                    **tensor_backend.tensor_cls_kwargs(),
                )

                if isometry:
                    if self.layer_idx == 0:
                        # Must be TTO
                        tensor.normalize()
                    else:
                        # Some lower layers
                        tensor, _ = tensor.split_qr(rows, cols)

                self.append(tensor)

        # initializetion not aware of device
        self.convert(tensor_backend.dtype, tensor_backend.device)

    def convert(self, dtype, device, singvals_only=False):
        """Convert layer towards specified data type and device."""
        if len(self) == 0:
            return

        if singvals_only:
            tensor = self[0]
        else:
            for tensor in self:
                tensor.convert(dtype, device)

        singvals_list = []
        for elem in self.singvals:
            if elem is None:
                singvals_list.append(None)
            else:
                singvals_ii = tensor.convert_singvals(elem, dtype, device)
                singvals_list.append(singvals_ii)

        self.singvals = singvals_list

    def _iter_tensors(self):
        """Iterate over all tensors forming the tensor network (for convert etc)."""
        for elem in self:
            yield elem

    def extend_local_hilbert_space(self, number_levels):
        """
        Extend the local Hilbert by a certain number of levels without
        population. For use on lowest layer with physical Hilbert space.

        Parameters
        ----------

        number_levels : int
            Defines the number of levels to be added. The levels are
            always appended to the end.
        """
        for ii in range(len(self)):
            small = self[ii]

            shape = list(small.shape)
            shape[0] = shape[0] + number_levels
            shape[1] = shape[1] + number_levels

            big = np.zeros(shape, dtype=small.dtype)
            if len(big.shape) != 3:
                raise NotImplementedError("Shape does not match binary tree.")

            big[: small.shape[0], : small.shape[1], :] = small[:, :, :]

            self[ii] = big

    def dot(self, other):
        """
        Contract the layer with another layer, where the other is taken
        automatically as complex conjugate.

        Parameters
        ----------

        other : :class:`TTNLayer`
            Calculate dot product with this state.

        Returns
        -------

        list : list of rank-2 tensors, where the second leg is to
            be contracted with the |ket> and the first leg with
            the <bra| state. This results corresponds to a dot-product
            on the level of a TTN layer.
        """
        if not isinstance(other, TTNLayer):
            raise TypeError("Only two TTNLayer classes can be the input.")

        if len(self) != len(other):
            raise ValueError("Layers must have the same length.")

        sandwich_list = []
        for ii, ket in enumerate(self):
            bra = other[ii]

            new_tens = bra.conj().tensordot(ket, [[0, 1], [0, 1]])
            sandwich_list.append(new_tens)

        return sandwich_list

    def qr_towards_top(self, requires_singvals, conv_params):
        """
        Iterating over QR decompositions for the complete layer, where
        the q-tensors remain in the layer and the r-tensors have to
        be contracted with the parent links.

        One use-case is the initial isometrization.

        Arguments
        ---------

        requires_singvals : bool
            Flag if singular values should be calculated; then, SVDs are
            used instead of QRs.

        conv_params : :class:`TNConvergenceParameters`
            For SVD, settings with convergence parameters have to be
            passed.

        Returns
        -------

        List of r-tensors (rank-2, 1st link to this layer, 2nd link
        to parent)
        """
        if len(self) == 2 and self.layer_idx == 0:
            raise Exception("Looks like this is already the top layer.")

        r_list = []
        for ii in range(len(self)):
            d1 = list(range(self[ii].ndim))[:-1]
            d2 = list(range(self[ii].ndim))[-1:]

            if requires_singvals:
                self[ii], rmat, lambdas, _ = self[ii].split_svd(
                    d1,
                    d2,
                    contract_singvals="R",
                    conv_params=conv_params,
                    no_truncation=True,
                )
                norm = np.sum(lambdas**2)
                if abs(norm - 1.0) > 1e-12:
                    raise Exception("normalization")
                self.singvals[ii] = lambdas
            else:
                self[ii], rmat = self[ii].split_qr(d1, d2)

                # Unset the singular values
                self.unset_singvals(ii)

            r_list.append(rmat)

        return r_list

    def contr_rmats(self, r_list):
        """
        Contract a list or tensors, e.g. r-tensors from a
        QR decomposition, which is twice as long as the
        current layer, i.e., each tensor in this layer contracts
        two r-tensors.

        Parameters
        ----------

        r_list : list of tensors
            The i-th tensor is contracted with the i-th link
            pointing to any child in the current layer.

        Returns
        -------

        None

        Details
        -------

        One use-case is the initial isometrization.
        """
        if len(r_list) != 2 * len(self):
            raise Exception("Dimension of self and r_list do not match.")

        for ii in range(len(self)):
            # indices of r-tensors
            i1 = 2 * ii
            i2 = i1 + 1

            # Contract over the second child first avoids
            # permutations
            tmp = r_list[i2].tensordot(self[ii], [[1], [1]])
            self[ii] = r_list[i1].tensordot(tmp, [[1], [1]])

        return

    def fuse_all_children(self):
        """
        Fuse the links towards the children and return a list
        of matrices.
        """
        fused = []
        for elem in self:
            new_dim = [elem.shape[0] * elem.shape[1], elem.shape[2]]
            fused.append(elem.reshape(new_dim))

        return fused

    def qr_top_right(self, requires_singvals, conv_params):
        """
        Do QR decomposition on top layer with two tensors. R-tensor
        is moved into the left tensor.

        Arguments
        ---------

        requires_singvals : bool
            Flag if singular values should be calculated; then, SVDs are
            used instead of QRs.

        conv_params : :class:`TNConvergenceParameters`
            For SVD, settings with convergence parameters have to be
            passed.

        Returns
        -------

        None
        """
        if len(self) != 2 and self.layer_idx != 0:
            raise Exception("Only available for top layer.")

        d1 = list(range(self[1].ndim))[:-1]
        d2 = list(range(self[1].ndim))[-1:]

        if requires_singvals:
            self[1], rmat, s_vals, _ = self[1].split_svd(
                d1,
                d2,
                contract_singvals="R",
                conv_params=conv_params,
                no_truncation=True,
            )

            self.singvals[0] = s_vals
            self.singvals[1] = s_vals
        else:
            self[1], rmat = self[1].split_qr(d1, d2)

            # Unset the singular values
            self.unset_singvals(0)
            self.unset_singvals(1)

        tmp = self[0].tensordot(rmat, [[2], [1]])
        self[0] = tmp.transpose([0, 1, 3, 2])

        self.unset_singvals(0)

        return

    def write(self, filehandle, f90_ttn_version, num_layers, cmplx=True):
        """
        Get string of the TTN layer which is compatible with the
        FORTRAN library.

        Parameters
        ----------

        filehandle : writable / filehandle
            Open filehandle to write layer.

        f90_ttn_version : str(len=8)
            Oldest compatible tn_state_treenetwork version.

        num_layers : int
            Number of layers in the complete TTN.

        cmplx: bool, optional
            If True the TTN is complex, real otherwise. Default to True

        Returns
        -------

        None

        Details
        -------

        We assume a binary tree.
        """
        self.convert(None, device="cpu")

        filehandle.write(f90_ttn_version + "\n")
        filehandle.write("%d\n" % (len(self)))
        dim_n2 = 3 if (self.layer_idx != 0) else 4
        filehandle.write("%d\n" % (dim_n2))

        for elem in self:
            if elem.has_symmetry:
                raise Exception("Cannot write symmetric tensors so far.")

            elem.write(filehandle, cmplx=cmplx)

        # Cutoff (integer)
        filehandle.write("%d\n" % (self.max_bond_dimension))

        # is_truncated (vector of logicals)
        # We take the safe path and assume it is not truncated only
        # if the dimension are smaller than the maximal bond dimension
        is_truncated_list = []
        for elem in self:
            is_truncated = np.any(np.array(elem.shape) >= self.max_bond_dimension)
            is_truncated_str = "T" if (is_truncated) else "F"
            is_truncated_list.append(is_truncated_str)

        filehandle.write(" ".join(is_truncated_list) + "\n")

        # neighbors (tensor of integers, each column layer index, tensor index
        # link index, link type for all links)
        if self.layer_idx == 0:
            # Copy-paste from a ground state - no questions asked
            address_list = []

            # First tensor link by link
            address_list += ["2", "1", "3", "1"]
            address_list += ["2", "2", "3", "1"]
            address_list += ["1", "2", "3", "2"]
            address_list += ["-1", "-1", "-1", "3"]

            # Second tensor link by link
            address_list += ["2", "3", "3", "1"]
            address_list += ["2", "4", "3", "1"]
            address_list += ["1", "1", "3", "2"]
            address_list += ["-1", "-1", "-1", "-1"]
        else:
            # Layer for children and parent tensors (including py vs F90
            # index offset
            p_layer = str(self.layer_idx)
            if num_layers - 1 == self.layer_idx:
                # Last layer sets children to -1
                c_layer = "-1"
            else:
                c_layer = str(self.layer_idx + 2)

            address_list = []
            for ii in range(len(self)):
                # Information about the first two links to the children
                # in fortran indices
                address_list += [c_layer, str(2 * ii + 1), "3", "1"]
                address_list += [c_layer, str(2 * ii + 2), "3", "1"]

                # parent: offset of plus one is for python vs fortran indexing
                address_list += [p_layer, str(ii // 2 + 1), str(ii % 2 + 1), "2"]

        filehandle.write(" ".join(address_list) + "\n")

        # sites (tensors of integers, each column is the index of
        # the first and last local Hilbert space below that tensor listed
        # for all links)
        stride = 2 ** (num_layers - 1 - self.layer_idx)
        next_sites = 1
        site_list = []
        for ii in range(len(self)):
            site_list += [str(next_sites), str(next_sites + stride - 1)]
            next_sites += stride

            site_list += [str(next_sites), str(next_sites + stride - 1)]
            next_sites += stride

            site_list += [site_list[-4], site_list[-1]]

            if self.layer_idx == 0:
                site_list += ["-1", "-1"]

        filehandle.write(" ".join(site_list) + "\n")

        # op_neighbors (index of neighboring effective operator in a
        # one-dimensional list)
        # number of sites in the lowest layer
        stride = 2 ** (num_layers + 1)
        cntr = 0
        for ii in range(num_layers, self.layer_idx, -1):
            cntr += stride
            stride = stride // 2

        op_list = []
        if self.layer_idx == 0:
            op_list += [cntr - 3, cntr - 2, cntr + 1, -1]
            op_list += [cntr - 1, cntr, cntr + 1, -1]
        else:
            i1 = cntr - 2 * stride + 1
            i2 = cntr + 1

            for ii in range(stride):
                op_list += [i1, i1 + 1, i2]
                i1 += 2
                i2 += 1

        op_list = list(map(str, op_list))

        filehandle.write(" ".join(op_list) + "\n")

        return

    def initialize_quantities(self, network_layer):
        """
        Initialize the important quantities of the layer given
        the information on the layer connectivity.
        Network_layer is a list of TNnodes.

        Parameters
        ----------
        network_layer : list of TNnodes
            Connectivity of the layer
        """
        # Cycle over nodes
        for tdx, node in enumerate(network_layer):
            # Cycle over children of the node
            lidx = 0
            if node.children is None:
                self.neighbors[:, lidx, tdx] = [-1, -1, lidx, 1]
                lidx += 1
            else:
                for child in node.children:
                    # [layer, index in layer, link, type]
                    self.neighbors[:, lidx, tdx] = [child.layer, child.index, lidx, 1]
                    lidx += 1
            # Final, add parent
            self.neighbors[:, lidx, tdx] = [
                node.parent.layer if node.parent is not None else -1,
                node.parent.index if node.parent is not None else -1,
                lidx,
                2,
            ]

            # Add the index for the effective operators
            self.op_neighbors[: len(node.link_idxs), tdx] = node.link_idxs

        # Add circuit selector information
        if self.is_ttn_toplayer:
            self.neighbors[:, -1, 0] = [-1, -1, self.max_num_links - 1, 3]

    def unset_singvals(self, tens_idx):
        """
        Unset the singular values relative to the tensor tens_idx
        because they become outdated due to some QR (for example during
        time evolution)

        Parameters
        ----------
        tens_idx : int
            Index of the tensor with outdated singvals

        Returns
        -------
        None
        """

        # If it is layer 0 unset both singvals since they are referring
        # to the same link
        if self.is_ttn_toplayer:
            self.singvals = [None, None]
        else:
            self.singvals[tens_idx] = None

    def print_tensors(self, how_many=None):
        """
        Prints the tensors in TTO layer together with their shape
        ----------------------------------------------------
        Input parameters:
        how_many [int] : only the first <how_many> tensors are printed
                          if how_many=None, all of the tensors are printed

        Returns:
        None
        ----------------------------------------------------
        """
        if how_many is None:
            how_many = len(self)
        if how_many > len(self) or how_many < 0:
            raise ValueError("Invalid number of tensors")

        for ii in range(0, how_many):
            print("\nTensor", ii, ":")
            print("Shape: ", self[ii].shape)
            print(self[ii])
        print("\n")

        return None

    def print_tensor_shapes(self, how_many=None):
        """
        Prints the shape of tensors in TTO layer
        -----------------------------------
        Input parameters:
        how_many [int] : only the shapes of the first <how_many> tensors are printed
                          if how_many=None, shapes of all of the tensors are printed

        Returns:
        None
        -----------------------------------
        """
        if how_many is None:
            how_many = len(self)
        if how_many > len(self) or how_many < 0:
            raise ValueError("Invalid number of tensors")

        for ii in range(0, how_many):
            print("Tensor", ii, ":")
            print("Shape: ", self[ii].shape)
        print("\n")

        return None


class TTN(_AbstractTN):
    """
    Tree tensor network class.

    Parameters
    ----------

    num_sites: int
        Number of sites

    convergence_parameters: :py:class:`TNConvergenceParameters`
        Class for handling convergence parameters. In particular,
        in the TTN simulator we are interested in:
        - the *maximum bond dimension* :math:`\\chi`;
        - the *cut ratio* :math:`\\epsilon` after which the singular
            values are neglected, i.e. if :math:`\\lamda_1` is the
            bigger singular values then after an SVD we neglect all the
            singular values such that
            :math:`\\frac{\\lambda_i}{\\lambda_1}\\leq\\epsilon`

    local_dim: int, optional
        Local dimension of the degrees of freedom. Default to 2.

    requires_singvals : boolean, optional
        Allows to enforce SVD to have singular values on each link available
        which might be useful for measurements, e.g., bond entropy (the
        alternative is traversing the whole TN again to get the bond entropy
        on each link with an SVD).

    tensor_backend : `None` or instance of :class:`TensorBackend`
        Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

    network : str, optional
        Default to "binary" (probably only option right now).

    initialize: string, optional
        Define the initialization method. For random entries use
        'random', for empty TTN use 'empty'.
        Default to 'random'.

    sectors : dict, optional
        Can restrict symmetry sector and/or bond dimension in initialization.
        If empty, no restriction.
        Default to empty dictionary.

    Details
    -------

    The last layer contains the local Hilbert spaces and the
    most tensors.
    """

    is_ttn = True
    extension = "ttn"

    def __init__(
        self,
        num_sites,
        convergence_parameters,
        local_dim=2,
        requires_singvals=False,
        tensor_backend=None,
        network="binary",
        initialize="random",
        sectors={},
        **kwargs,
    ):
        # Pre-process local_dim to be a vector
        if np.isscalar(local_dim):
            local_dim = np.repeat(int(local_dim), num_sites)
        else:
            pass
            # local_dim = np.array(local_dim, dtype=int)

        super().__init__(
            num_sites,
            convergence_parameters,
            local_dim=local_dim,
            requires_singvals=requires_singvals,
            tensor_backend=tensor_backend,
        )

        # The number of links is defined in the network definition, i.e. at the
        # moment insite _generate_binary_network
        self.num_links = 0

        self._network = network
        if network == "binary":
            self.num_layers = int(np.log2(num_sites)) - int(self.is_ttn)
            network = self._generate_binary_network()

            if abs(np.log2(num_sites) - int(self.is_ttn) - self.num_layers) > 1e-14:
                raise Exception(
                    "Cannot construct TTN; num_sites is "
                    + "not power of two: %d." % (num_sites)
                )
        else:
            raise NotImplementedError("Only binary tree is implemented")

        # Layer and tree initialization
        self.layers = []
        for ii in range(self.num_layers):
            layer = TTNLayer(
                ii,
                self.local_links,
                self._convergence_parameters.max_bond_dimension,
                4,
                len(network[ii]),
            )
            layer.initialize_quantities(network[ii])
            self.layers.append(layer)
        self._initialize_sites_range(network)
        self._initialize_tree(initialize, sectors=sectors)

        # Caching of sampling steps
        self._cache_get_children_prob = {}
        self._cachesize_bytes_get_children_prob = 0
        self._cachelimit_bytes_get_children_prob = None
        self._cache_clearing_strategy = "num_qubits"

        self.is_measured = self[0].is_measured

        # TTN initializetion not aware of device
        self.convert(self._tensor_backend.dtype, self._tensor_backend.device)

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def default_iso_pos(self):
        """
        Returns default isometry center position, e.g., for initialziation
        of effective operators.
        """
        return [0, 0]

    @property
    def current_max_bond_dim(self):
        """Current maximum bond dimension of the TTN"""
        max_chi = 0
        for tensor in self._iter_tensors():
            max_chi = max(max_chi, np.max(tensor.shape))

        return max_chi

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __getitem__(self, idx):
        """
        Overwrite calls to get element in list, which refers to the layer
        in a TTN.

        Parameters
        ----------

        key : int or tuple
            Index of the layer to be returned if int.
            If tuple, the first int is the index of the layer and
            the second the index of the tensor

        Returns
        -------

        :class:`TTNLayer`
        """
        if np.isscalar(idx):
            out = self.layers[idx]
        else:
            layer_idx, tensor_idx = idx
            out = self.layers[layer_idx][tensor_idx]

        return out

    def __setitem__(self, idx, value):
        """
        Overwrite calls to set element in list, which refers to the layer
        in a TTN.

        Parameters
        ----------

        key : tuple of ints
            The first int is the index of the layer and
            the second the index of the tensor
        value : xp.array or :class:`TTNLayer`
            Tensor to be set in place of the old
        """
        if np.isscalar(idx):
            self.layers[idx] = value
        else:
            self.layers[idx[0]][idx[1]] = value

    def __matmul__(self, other):
        """
        Implement the contraction between two TTNs overloading the operator
        @. It is equivalent to doing <self|other>. It already takes into account
        the conjugation of the left-term
        """
        if not isinstance(other, TTN):
            raise TypeError("Only two TTN classes can be contracted")

        return other.dot(self)

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------
    #
    # Inheriting:
    #
    # * read_pickle

    @classmethod
    def from_statevector(
        cls, statevector, local_dim=2, conv_params=None, tensor_backend=None
    ):
        """
        Initialize the TTN by decomposing a statevector into TTN form.

        Parameters
        ----------

        statevector : ndarray of shape( [local_dim]*num_sites, )
            Statevector describing the interested state for initializing the TTN

        device : str, optional
            Device where the computation is done. Either "cpu" or "gpu".

        tensor_cls : type for representing tensors.
            Default to :class:`QteaTensor`
        """

        # At the moment, no truncation is implemented in the code
        num_sites = len(statevector.shape)

        if local_dim != statevector.shape[0]:
            raise Exception("Mismatch local dimension (passed and one in array).")

        if np.any(local_dim != np.array(statevector.shape)):
            raise Exception(
                "from_statevector requires equal local dim " + "across the system."
            )

        num_layers = int(np.log2(num_sites) - 1)
        state_tensor = statevector
        tensor_list = []
        singvals_list = []
        p0 = 1
        p1 = 2

        for ll in range(num_layers):
            tensor_layer_list = []
            singvals_layer_list = []
            i0 = p0
            i1 = p1

            if ll == (num_layers - 1):
                num_svd = 1
            else:
                num_svd = num_sites // p1

            for _ in range(num_svd):
                d0 = local_dim ** (p1 // 2)
                d1 = local_dim**p1
                d2 = np.prod(state_tensor.shape[2:])
                umat, s_tot, vhmat = np.linalg.svd(
                    state_tensor.reshape([d1, d2]), full_matrices=False
                )
                singvals_layer_list.append(s_tot)
                s_tot = np.diag(s_tot)

                umat = umat.reshape([d0, d0, d1])
                new_shape = (
                    [d1] + [d0] * ((num_sites - i1) // (p1 // 2)) + [d1] * (i0 - 1)
                )
                state_tensor = np.dot(s_tot, vhmat).reshape(new_shape)

                perm = [jj + 1 for jj in range(len(state_tensor.shape) - 1)] + [0]
                state_tensor = np.transpose(state_tensor, perm)

                i0 += 1
                i1 += p1
                tensor_layer_list.append(umat)

                if ll == (num_layers - 1):
                    tensor_layer_list.append(state_tensor)

            p1 *= 2
            tensor_list.append(tensor_layer_list)
            singvals_list.append(singvals_layer_list)

        tensor_list[-1][0] = np.reshape(
            tensor_list[-1][0], list(tensor_list[-1][0].shape) + [1]
        )
        # The two top links are the same link
        singvals_list[-1].append(singvals_list[-1][0])

        obj = cls.from_tensor_list(
            tensor_list,
            singvals_list=singvals_list,
            tensor_backend=tensor_backend,
            conv_params=conv_params,
        )

        obj.iso_center = (0, 1)
        obj.iso_towards([0, 0], keep_singvals=True)
        obj._requires_singvals = True

        return obj

    @classmethod
    def product_state_from_local_states_2d(
        cls,
        mat_2d,
        padding=None,
        mapping="HilbertCurveMap",
        return_map=False,
        conv_params=None,
        tensor_backend=None,
    ):
        """
        Construct a product (separable) state in 1d TTN form for a 2d system
        by mapping it to 1d, given the local states of each of the sites.

        Parameters
        ----------
        mat_2d : np.array of rank 2
            Array with third axis being a (normalized) local state of
            the (ii,jj)-th site (where ii and jj are indices of the
            first and second axes).
            Product of first two axes' dimensions is therefore equal
            to the total number of sites, and third axis dimension
            corresponds to the local dimension.

        padding : np.array of length 2 or `None`, optional
            Used to enable the growth of bond dimension in TDVP algorithms
            for TTN (necessary as well for two tensor updates).
            If not `None`, all the TTN tensors are padded such that the bond
            dimension is equal to `padding[0]`. The value `padding[1]`
            tells with which value are we padding the tensors. Note that
            `padding[1]` should be very small, as it plays the role of
            numerical noise.
            If False, the bond dimensions are equal to 1.
            Default to None.

        mapping : string or instance of :py:class:`HilbertCurveMap`,
                  optional
            Which 2d to 1d mapping to use. Possible inputs are:
            'HilbertCurveMap', 'SnakeMap', and 'ZigZagMap'.
            Default is 'HilbertCurveMap'.

        return_map : boolean, optional
            If True, the function returns array `map` with indices
            of 2d to 1d mapping.
            Default to False.

        convergence_parameters : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters for the new TTN.

        Return
        ------
        prod_ttn : :py:class:`TTN`
            Corresponding product state TTN.
        map : np.array, returned only if return_map==True
            Nx2 Matrix, where N is a total number of particles.
            The values in the ii-th row of the matrix denote
            particle's position in a corresponding 2d grid.

        """
        if len(mat_2d.shape) != 3:
            raise Exception("numpy ndarray must be of rank-3.")
        for ii in range(0, mat_2d.shape[0]):
            for jj in range(0, mat_2d.shape[1]):
                norm = np.linalg.norm(mat_2d[ii, jj, :])
                if abs(norm - 1) > 10e-5:
                    raise ValueError(
                        f"Local state on site ({ii+1},{jj+1}) "
                        f"not normalized. Norm = {norm}."
                    )

        dim = 2  # define that we are in 2d
        num_sites_x, num_sites_y, local_dim = mat_2d.shape
        size = [num_sites_x, num_sites_y]
        num_sites_tot = num_sites_x * num_sites_y

        # f ind the corresponding indices of 2d points in 1d
        map_indices = map_selector(dim, size, mapping)
        if return_map:
            # will be same as map_indices, just in np.ndarray form
            map_array = np.zeros((num_sites_tot, 2))

        # compute the corresponding array with local states for 1d
        mat_1d = np.zeros((num_sites_tot, local_dim))
        ii = 0
        for ind in map_indices:
            n_x, n_y = ind
            mat_1d[ii, :] = mat_2d[n_x, n_y, :]
            if return_map:
                map_array[ii] = ind
            ii += 1

        prod_ttn = TTN.product_state_from_local_states(
            mat_1d,
            padding=padding,
            convergence_parameters=conv_params,
            tensor_backend=tensor_backend,
        )

        if return_map:
            return prod_ttn, map_array
        return prod_ttn

    def to_dense(self, true_copy=False):
        """Return TTN without symmetric tensors."""
        if self.has_symmetry:
            obj = type(self)(
                self.num_sites,
                self.convergence_parameters,
                local_dim=self.local_dim,
                initialize="empty",
                tensor_backend=self._tensor_backend,
            )

            for ii, layer in enumerate(self.layers):
                layer_dense = layer.to_dense(true_copy=true_copy)

                obj[ii] = layer_dense

            return obj

        # Cases without symmetry

        if true_copy:
            return self.copy()

        return self

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    def pre_timeevo_checks(self, raise_error=False):
        """Check if a TN ansatz is ready for time evolution."""
        is_check_okay = super().pre_timeevo_checks(raise_error=raise_error)

        chi_max = 1
        for layer in self.layers[::-1]:
            for tensor in layer._iter_tensors():
                chi_tensor = np.max(tensor.shape)
                chi_max = max(chi_max, chi_tensor)

        is_product_state = chi_max == 1
        if is_product_state and raise_error:
            raise Exception("TTN time evolution with product state will fail.")

        if is_product_state:
            is_check_okay = False
            warnings.warn("TTN time evolution likely trapped in product state.")

        return is_check_okay

    # --------------------------------------------------------------------------
    #                     Abstract methods to be implemented
    # --------------------------------------------------------------------------

    def _convert_singvals(self, dtype, device):
        """Convert the singular values of the tensor network to dtype/device."""
        for layer in self.layers:
            layer.convert(dtype, device, singvals_only=True)

    def get_bipartition_link(self, pos_src, pos_dst):
        """
        Returns two sets of sites forming the bipartition of the system for
        a loopless tensor network. The link is specified via two positions
        in the tensor network.

        **Arguments**

        pos_src : tuple of two ints
            Specifies the first tensor and source of the link.

        pos_dst : tuple of two ints
            Specifies the second tensor and destination of the link.

        **Returns**

        sites_src : list of ints
            Hilbert space indices when looking from the link towards
            source tensor and following the links therein.

        sites_dst : list of ints
            Hilbert space indices when looking from the link towards
            destination tensor and following the links therein.
        """
        self.assert_binary_tree()

        if pos_src[0] > pos_dst[0]:
            # Use source tensor to start calculing
            span_sites = 2 ** (self.num_layers - pos_src[0])
            offset = span_sites * pos_src[1]

            sites_src = list(range(offset, offset + span_sites))

            sites_dst = list(range(offset))
            sites_dst += list(range(offset + span_sites, self.num_sites))

            return sites_src, sites_dst

        # Use destination tensor to start calculating
        span_sites = 2 ** (self.num_layers - pos_dst[0])
        offset = span_sites * pos_dst[1]

        sites_dst = list(range(offset, offset + span_sites))

        sites_src = list(range(offset))
        sites_src += list(range(offset + span_sites, self.num_sites))

        return sites_src, sites_dst

    def get_pos_links(self, pos):
        """
        Return a list of positions where all links are leading to. Number
        of entries is equal to number of links. Each entry contains the position
        as accessible in the actual tensor network.
        """
        pos_links = []
        for i1, i2, _ in self._iter_all_links(pos):
            if i2 is None:
                pos_links.append(None)
            else:
                pos_links.append((i1, i2))

        return pos_links

    def get_rho_i(self, idx):
        """
        Calculate the reduced density matrix for a single site.
        If the singular values are stored (i.e. not None) do not
        move the isometry center, but use them to compute local
        observables.

        Parameters
        ----------

        idx : integer
            Calculate the reduced density matrix of site ``idx``.
            Recall python indices start at zero.

        Returns
        -------

        numpy ndarray : rank-2 tensor with the reduced density
        matrix.
        """
        self.assert_binary_tree()

        layer_idx = self.num_layers - 1
        tensor_idx = idx // 2

        if (self.iso_center is None) or (self[layer_idx].singvals[tensor_idx] is None):
            self.iso_towards([layer_idx, tensor_idx], keep_singvals=True)
            tensor = self[layer_idx][tensor_idx]
        elif list(self.iso_center) == [layer_idx, tensor_idx]:
            tensor = self[layer_idx][tensor_idx]
        else:
            tensor = self[layer_idx][tensor_idx].scale_link(
                self[layer_idx].singvals[tensor_idx], 2
            )

        if idx % 2 == 0:
            contr_idx = [1, 2]
        else:
            contr_idx = [0, 2]

        rho = tensor.tensordot(tensor.conj(), [contr_idx, contr_idx])

        trace = rho.trace(return_real_part=True, do_get=True)
        if abs(1 - trace) > 10 * rho.dtype_eps:
            warnings.warn("Renormalizing reduced density matrix.")
            rho /= trace

        return rho

    def get_tensor_of_site(self, idx):
        """
        Generic function to retrieve the tensor for a specific site. Compatible
        across different tensor network geometries.

        Parameters
        ----------
        idx : int
            Return tensor containin the link of the local
            Hilbert space of the idx-th site.
        """
        self.assert_binary_tree()

        return self[-1][idx // 2]

    def iso_towards(self, new_iso, keep_singvals=False, trunc=False, conv_params=None):
        """
        Shift isometry center towards a certain tensor.

        Parameters
        ----------

        new_iso : list of two integers
            New isometry center in terms of layer and tensor.

        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.

        trunc : Boolean, optional
            If `True`, the shifting is done via truncated SVD.
            If `False`, the shifting is done via QR.
            Default to `False`.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD. If `None`, convergence
            parameters are taken from the TTN.
            Default to `None`.

        Returns
        -------

        singvals_cut_tot : np.ndarray
            Singualr values cut in the process of shifting the isometry center.
            None if moved through the QR.

        Details
        -------

        We introduce an overhead if the TTN has no
        isometry center set up to now. This choice could
        be further optimized.
        """
        if self.iso_center is not None:
            if (self.iso_center[0] == new_iso[0]) and (
                self.iso_center[1] == new_iso[1]
            ):
                # Return singular values cut, i.e., zeros in this case
                return np.zeros(1)
        else:
            # Isometry center is not set; we install it first
            # at [0, 0] and accept a small overhead
            self.isometrize_all()

        # Obtain the path
        complete_path = self.get_path(new_iso)

        singvals_cut_tot = []
        for elem in complete_path:
            # Get the tensor for the QR
            src_layer_idx = elem[0]
            src_tensor_idx = elem[1]
            src = self[src_layer_idx][src_tensor_idx]

            # Get the target/destination tensor
            dst_layer_idx = elem[3]
            dst_tensor_idx = elem[4]
            dst = self[dst_layer_idx][dst_tensor_idx]

            src_link = elem[2]
            dst_link = elem[5]
            src, dst, singvals_cut, singvals = self.shift_iso_to(
                src, dst, src_link, dst_link, trunc=trunc, conv_params=conv_params
            )
            singvals_cut_tot.append(singvals_cut)
            # Unset the singvals if the flag is not active, since the QRs might destroy
            # the entanglement in the PATH.
            if not keep_singvals:
                lowest_layer = max(src_layer_idx, dst_layer_idx)
                lowest_tensor = (
                    dst_tensor_idx if dst_layer_idx > src_layer_idx else src_tensor_idx
                )
                self[lowest_layer].unset_singvals(lowest_tensor)
            if trunc or self._requires_singvals:
                lowest_layer = max(src_layer_idx, dst_layer_idx)
                lowest_tensor = (
                    dst_tensor_idx if dst_layer_idx > src_layer_idx else src_tensor_idx
                )
                self[lowest_layer].singvals[lowest_tensor] = singvals

            self[src_layer_idx][src_tensor_idx] = src
            self[dst_layer_idx][dst_tensor_idx] = dst

            if self.eff_op is not None:
                self._update_eff_ops(elem)

            # And reset iso center to new value
            self.iso_center = elem[3:5]

        return np.array(singvals_cut_tot)

    def _iter_tensors(self):
        """Iterate over all tensors forming the tensor network (for convert etc)."""
        for layer in self.layers:
            for tensor in layer._iter_tensors():
                yield tensor

    def norm(self):
        """Return the norm of a TTN."""
        if self.iso_center is None:
            # We have to install isometry center, pick default
            self.isometrize_all()

        norm = self[self.iso_center[0]][self.iso_center[1]].norm()
        # norm = np.sum(np.real(tensor * tensor.conj()))

        return np.sqrt(norm)

    def scale(self, factor):
        """Scale a TTN with a scalar factor."""
        if self.iso_center is None:
            # We have to install isometry center, pick default
            self.isometrize_all()

        self[self.iso_center[0]][self.iso_center[1]] *= factor

    def set_singvals_on_link(self, pos_a, pos_b, s_vals):
        """Update or set singvals on link via two positions."""
        if pos_a[0] > pos_b[0]:
            # pos_a is in the lower layer
            pos = pos_a
        else:
            pos = pos_b

        if pos[0] == 0:
            self.layers[pos[0]].singvals[0] = s_vals
            self.layers[pos[0]].singvals[1] = s_vals
        else:
            self.layers[pos[0]].singvals[pos[1]] = s_vals

    def site_canonize(self, idx, keep_singvals=False):
        """
        Shift the isometry center to the tensor containing the
        corresponding site.

        Parameters
        ----------

        idx : int
            Index of the physical site which should be isometrized.

        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.

        """
        self.assert_binary_tree()

        target_layer = self.num_layers - 1
        target_tensor = idx // 2

        self.iso_towards([target_layer, target_tensor], keep_singvals=keep_singvals)

    # --------------------------------------------------------------------------
    #                   Choose to overwrite instead of inheriting
    # --------------------------------------------------------------------------

    def permute_spo_for_two_tensors(self, spo_list, theta, link_partner):
        """Incoming order Ta, Tb, Pa, Pb"""
        if not isinstance(spo_list[0], SparseMatrixOperatorPy):
            # Effective operator not affected
            return spo_list, theta, None

        if link_partner in [0, 2]:
            return spo_list, theta, None

        if (link_partner == 1) and (theta.ndim == 4):
            spo_list = [spo_list[0], spo_list[1], spo_list[3], spo_list[2]]
            theta.transpose_update([0, 1, 3, 2])
            inv_permutation = [0, 1, 3, 2]

            return spo_list, theta, inv_permutation

        if (link_partner == 1) and (theta.ndim == 5):
            spo_list = [spo_list[0], spo_list[1], spo_list[3], spo_list[2], spo_list[4]]
            theta.transpose_update([0, 1, 3, 2, 4])
            inv_permutation = [0, 1, 3, 2, 4]

            return spo_list, theta, inv_permutation

        raise Exception(f"Unknown link_partner being {link_partner}.")

    # --------------------------------------------------------------------------
    #                                  Unsorted
    # --------------------------------------------------------------------------

    def assert_binary_tree(self):
        """Assert for methods requiring binary trees."""
        if self._network != "binary":
            raise Exception("Tree is not binary tree; no support yet.")

    @property
    def iso_center(self):
        """Isometry center property"""
        return self._iso_center

    @iso_center.setter
    def iso_center(self, value):
        """Change the value of the iso center"""
        self._iso_center = value

    def _iter_all_links(self, pos):
        """
        Return an iterator over all the links of a position
        `pos` in the TTN. It treats specially the tensor at `(0, 0)`

        Parameters
        ----------
        pos : Tuple[int]
            Position in the tree as `(layer_idx, tensor_idx)`

        Returns
        -------
        Tuple[int]
            Tuple of `(layer_link, tensor_link, leg_toward_link)`
        """
        for elem in self._iter_children_pos(pos):
            yield elem

        _, info = self._get_parent_info(pos)
        yield info

        if pos[0] == 0 and pos[1] == 0 and self.is_ttn:
            yield None, None, None

    def _iter_physical_links(self):
        """
        Returns an iterator over the physical links.
        The physical links are represented as the tuple
        `( (layer_idx+1, site_idx), (layer_idx, tensor_idx) )`,
        where `layer_idx` is the physical (last) layer of the TTN.

        Returns
        -------
        Tuple[int]
            The extra physical layer and site index `(layer_idx+1, site_idx)`
        Tuple[int]
            The final TTN layer and the tensor index `(layer_idx, tensor_idx)`
        """

        # Relevant layer is the last layer
        layer = self[-1]
        lidx = layer.layer_idx

        idx = -1
        for ii, tens in enumerate(layer):
            nn = tens.ndim - 1
            if lidx == 0 and ii == 0:
                # Top-tensor in four-body TTN
                nn -= 1

            for _ in range(nn):
                idx += 1

                yield (lidx + 1, idx), (lidx, ii)

    def _iter_children_pos(self, pos):
        """
        Return an iterator over the tuple
        giving informations about the children of
        the tensor in position `pos`. The children are
        the legs pointing downwards.
        Works only for binary trees.

        Parameters
        ----------
        pos : Tuple[int]
            Position in the tree as `(layer_idx, tensor_idx)`

        Returns
        -------
        Tuple[int]
            Tuple of `(layer_child_1, tensor_child_1, leg_toward_parent)`
        Tuple[int]
            Tuple of `(layer_child_2, tensor_child_2, leg_toward_parent)`
        """
        self.assert_binary_tree()

        # Works only for binary tree:
        yield pos[0] + 1, 2 * pos[1], 2
        yield pos[0] + 1, 2 * pos[1] + 1, 2

    def _get_parent_info(self, pos):
        """
        Return informations about the parent of
        the tensor in position `pos`. The parent is
        the leg pointing upwards.
        Works only for binary trees.

        Parameters
        ----------
        pos : Tuple[int]
            Position in the tree as `(layer_idx, tensor_idx)`

        Returns
        -------

        link : int
            Link index of the tensor at `pos` which connects to
            the parent tensor.

        info : list of three ints
            Layer index of parent tensor, tensor index within
            layer of parent tensor, link index in parent tensor
            connecting to tensor at `pos`.
        """
        self.assert_binary_tree()

        info = -np.ones(3, dtype=int)
        link = 2

        if np.any(info < 0):
            # Works only for binary trees
            if list(pos) == [0, 0]:
                info[0] = 0
                info[1] = 1
                info[2] = 2
            elif list(pos) == [0, 1]:
                info[0] = 0
                info[1] = 0
                info[2] = 2
            else:
                info[0] = max(0, pos[0] - 1)
                info[1] = pos[1] // 2
                info[2] = pos[1] % 2

        return link, list(info)

    def _generate_binary_network(self):
        """
        Generate the network structure for the binary tree.
        This function just generate the network structure, not
        the TTN itself.

        Returns
        -------
        list of lists of TNnodes
            The outer list is the network, the inner list
            the layers with TNnodes
        """
        network = [[] for _ in range(self.num_layers)]
        link_idx = 0

        # Special case for first layer
        if self.is_ttn:
            num_tensors = 2 ** (self.num_layers)
        else:
            num_tensors = 2 ** (self.num_layers - 1)
        for tidx in range(num_tensors):
            network[self.num_layers - 1].append(
                TNnode(
                    layer=self.num_layers - 1,
                    index=tidx,
                    children=None,
                    link_idx=link_idx,
                )
            )
            link_idx += 3

        # Run on other layers
        for layer_idx in range(self.num_layers - 2, -1, -1):
            if self.is_ttn:
                num_tensors = 2 ** (layer_idx + 1)
            else:
                num_tensors = 2 ** (layer_idx)
            for tidx in range(num_tensors):
                network[layer_idx].append(
                    TNnode(
                        layer=layer_idx,
                        index=tidx,
                        children=network[layer_idx + 1][2 * tidx : 2 * tidx + 2],
                        link_idx=link_idx,
                    )
                )
                link_idx += 1

        if self.is_ttn:
            # Fix the latest tensor
            network[0][0].add_parent(network[0][1])
            network[0][1].add_parent(network[0][0])
            network[0][1].link_idxs[-1] = network[0][0].link_idxs[-1]
        self.num_links = link_idx

        return network

    def _initialize_sites_range(self, network):
        """
        Initialize each sites_range variable of the layers from
        the bottom to the top
        """
        # Case of the last layer, which is different from the
        # rest of the network
        layer = self.layers[self.num_layers - 1]
        sites = 0
        for tidx in range(layer.num_tensors):
            node = network[self.num_layers - 1][tidx]
            # Lower links
            for lidx in range(len(node.link_idxs) - 1):
                layer.sites[:, lidx, tidx] = [sites, sites + 1]
                sites += 1
            # Upper link
            layer.sites[:, len(node.link_idxs) - 1, tidx] = [
                np.min(layer.sites[:, :, tidx][layer.sites[:, :, tidx] > 0]),
                np.max(layer.sites[:, :, tidx]),
            ]

        # Do the rest of the network
        for layer_idx in range(self.num_layers - 2, -1, -1):
            layer = self.layers[layer_idx]
            for tidx in range(layer.num_tensors):
                node = network[layer_idx][tidx]
                # Lower links
                for lidx, child in enumerate(node.children):
                    layer.sites[:, lidx, tidx] = self.layers[layer_idx + 1].sites[
                        :, -2, child.index
                    ]
                # Upper link
                layer.sites[:, len(node.link_idxs) - 1, tidx] = [
                    np.min(layer.sites[:, :, tidx][layer.sites[:, :, tidx] > 0]),
                    np.max(layer.sites[:, :, tidx]),
                ]

    def _initialize_tree(self, method="empty", isometry=True, sectors={}):
        """
        Initialize the tree with random tensors

        Parameters
        ----------
        isometry : bool, optional
            If True, the tree is initialized as isometry, by default True

        sectors : dict, optional
            Can restrict symmetry sector and/or bond dimension in initialization.
            If empty, no restriction.
            Default to empty dictionary.
        """
        isometrize = isometry or self._requires_singvals

        if method == "vacuum":
            matrix = np.zeros((self.num_sites, self.local_dim[0]))
            matrix[:, 0] = 1
            ttn = TTN.product_state_from_local_states(
                matrix,
                convergence_parameters=self._convergence_parameters,
                tensor_backend=self._tensor_backend,
            )
            self.layers = ttn.layers
        else:
            # Assuming all equal local dims
            child_link = self.local_links[0]
            links = self._tensor_backend.tensor_cls.set_missing_link(
                [child_link, child_link, None],
                self._convergence_parameters.ini_bond_dimension,
                are_links_outgoing=[False, False, True],
            )

            for idx in range(self.num_layers - 1, -1, -1):
                self[idx].initialize_layer(
                    links,
                    self._tensor_backend,
                    initialization=method,
                    isometry=isometrize,
                    sectors=sectors,
                )

                child_link = links[-1]
                links = self._tensor_backend.tensor_cls.set_missing_link(
                    [child_link, child_link, None],
                    self._convergence_parameters.ini_bond_dimension,
                    are_links_outgoing=[False, False, True],
                )

        if isometrize and (method != "empty"):
            self.iso_center = (0, 0)

        if self._requires_singvals:
            # Cannot replace QR in initialize_layer with SVD as the values
            # will be thrown a way, only way is to iterate through everything.
            # So we skip QR in the first place, and do everything here.
            for ii in range(self.num_sites):
                self.site_canonize(ii)

            self.iso_towards((0, 0))

    def dot(self, other):
        """
        Calculate the dot-product or overlap between two TTNs, i.e.,
        <other | self>.

        Parameters
        ----------

        other : :class:`TTN`
            Measure the overlap with this other TTN.

        Returns
        -------

        Scalar representing the overlap.
        """
        return self.sandwich(other)

    def sandwich(self, other):
        """
        In the case of pure state TTN, calculate the dot-product, i.e.
        <other | self>.

        Parameters
        ----------

        other : :class:`TTN`
            Measure the overlap with this other TTN.

        Returns
        -------

        Scalar representing the overlap.
        """
        if not isinstance(other, TTN):
            raise TypeError("Only two TTNs can be the input.")

        if self.num_sites != other.num_sites:
            raise ValueError("States must have the same number of sites.")

        sandwich = self.layers[-1].dot(other.layers[-1])

        for ii in range(1, self.num_layers):
            ket = deepcopy(self.layers[-1 - ii])

            # contr_rmats will combine the tensors in the sandwich
            # list and the corresponding tensors in the ket, where
            # each ket tensor is contracted with two tensors in the
            # sandwich list
            ket.contr_rmats(sandwich)

            sandwich = ket.dot(other.layers[-1 - ii])

        if self.is_ttn:
            final = sandwich[0].tensordot(sandwich[1], [[0, 2], [0, 1]])
        else:
            final = sandwich[0]

        # It remain a 1x1 matrix with the links of the symmetry selector
        return final.get_entry()

    @classmethod
    def read(cls, filename, tensor_backend, cmplx=True, order="F"):
        """
        Read a TTN written by FORTRAN in a formatted way on file.
        Reads in column-major order but the output is in row-major.
        This is the only method that overrides the number of sites,
        since you may not know before reading.

        Parameters
        ----------
        filename: str
            PATH to the file
        tensor_backend : :class:`TensorBackend`
            Setup which tensor class to create.
        cmplx: bool, optional
            If True the MPS is complex, real otherwise. Default to True
        order: str, optional
            Format in which the tensors are saved. If 'F' column-major,
            if 'C' row major"

        Returns
        -------
        obj: py:class:`TTN`
            TTN class read from file

        Details
        -------

        Many fields stored in a TTN for the fortran code are not kept
        as they can be easily retrieved on the python side.

        The performance can be improved if we consider converting
        the isometry center in fortran to python and ensure a
        conversion is always possible.
        """
        ext = "pkl" + cls.extension
        if filename.endswith(ext):
            return cls.read_pickle(filename)

        tensor_list = []

        with open(filename, "r") as fh:
            # Version of tn_state_treenetwork
            _ = fh.readline().strip()

            # TTO flag
            is_tto = fh.readline().strip() == "T"

            if is_tto:
                raise NotImplementedError("TTO is not yet supported.")

            # Number of sites
            _ = int(fh.readline().strip())

            num_layers = int(fh.readline().strip())

            # Number of tensors
            _ = int(fh.readline().strip())

            for _ in range(num_layers):
                layer_list = []

                # Read version string
                _ = fh.readline()

                num_tensors_layer = int(fh.readline().strip())

                # maximum number of links n2
                _ = int(fh.readline().strip())

                for _ in range(num_tensors_layer):
                    tens_jj = tensor_backend.tensor_cls.read(
                        fh,
                        tensor_backend.dtype,
                        tensor_backend.device,
                        tensor_backend.base_tensor_cls,
                        cmplx=cmplx,
                        order=order,
                    )
                    layer_list.append(tens_jj)

                # the cutoff
                _ = int(fh.readline().strip())
                truncated = [xx == "T" for xx in fh.readline().strip().split()]
                tmp = list(map(int, fh.readline().strip().split()))

                # We have a newline issue, either the information is
                # stored in one or two lines ... divide into if-case
                if len(truncated) * 4 == len(tmp):
                    # upper_address: information about how the current
                    # tensor is connected to the parent layer For
                    # a binary tree, this can be retrieved really
                    # fast in python
                    _ = tmp[: 2 * len(truncated)]
                    # Site: information about how the current tensors
                    # connects to the layer with the children. For
                    # a binary tree, this can be retrieved really
                    # fast in python
                    _ = tmp[2 * len(truncated) :]
                else:
                    # upper_address
                    _ = tmp
                    # Site
                    _ = list(map(int, fh.readline().strip().split()))

                # op_neigbors is the last one to be read here
                _ = list(map(int, fh.readline().strip().split()))

                tensor_list.insert(0, layer_list)

            psi = cls.from_tensor_list(tensor_list)

            has_iso = fh.readline().split() == "T"
            if has_iso:
                # This is the iso position - convert to python indices
                iso_f90 = list(map(int, fh.readline().strip().split()))
                if len(iso_f90) == 2:
                    psi.iso_center = [iso_f90[0] - 1, iso_f90[1] - 1]

        return psi

    @classmethod
    def read_v0_2_29(cls, filename, tensor_backend, cmplx=True, order="F"):
        """
        Read a TTN written by FORTRAN in a formatted way on file.
        Reads in column-major order but the output is in row-major.
        This is the only method that overrides the number of sites,
        since you may not know before reading.

        Parameters
        ----------
        filename: str
            PATH to the file
        tensor_backend : :class:`TensorBackend`
            Setup which tensor class to create.
        cmplx: bool, optional
            If True the MPS is complex, real otherwise. Default to True
        order: str, optional
            Format in which the tensors are saved. If 'F' column-major,
            if 'C' row major"

        Returns
        -------
        obj: py:class:`TTN`
            TTN class read from file

        Details
        -------

        Many fields stored in a TTN for the fortran code are not kept
        as they can be easily retrieved on the python side.

        The performance can be improved if we consider converting
        the isometry center in fortran to python and ensure a
        conversion is always possible.
        """
        tensor_list = []

        with open(filename, "r") as fh:
            # TTO flag
            is_tto = fh.readline().strip() == "T"

            if is_tto:
                raise NotImplementedError("TTO is not yet supported.")

            # Number of sites
            _ = int(fh.readline().strip())

            num_layers = int(fh.readline().strip())

            # Number of tensors
            _ = int(fh.readline().strip())

            for _ in range(num_layers):
                layer_list = []

                num_tensors_layer = int(fh.readline().strip())

                for _ in range(num_tensors_layer):
                    tens_jj = tensor_backend.tensor_cls.read(
                        fh,
                        tensor_backend.dtype,
                        tensor_backend.device,
                        tensor_backend.base_tensor_cls,
                        cmplx=cmplx,
                        order=order,
                    )
                    layer_list.append(tens_jj)

                # the cutoff
                _ = int(fh.readline().strip())
                truncated = [xx == "T" for xx in fh.readline().strip().split()]
                tmp = list(map(int, fh.readline().strip().split()))

                # We have a newline issue, either the information is
                # stored in one or two lines ... divide into if-case
                if len(truncated) * 4 == len(tmp):
                    # upper_address: information about how the current
                    # tensor is connected to the parent layer For
                    # a binary tree, this can be retrieved really
                    # fast in python
                    _ = tmp[: 2 * len(truncated)]
                    # Site: information about how the current tensors
                    # connects to the layer with the children. For
                    # a binary tree, this can be retrieved really
                    # fast in python
                    _ = tmp[2 * len(truncated) :]
                else:
                    # upper_address
                    _ = tmp
                    # Site
                    _ = list(map(int, fh.readline().strip().split()))

                tensor_list.insert(0, layer_list)

            has_iso = fh.readline().split() == "T"
            if has_iso:
                # This would be the iso position, let's not trust it
                # We prefer to instantiate upon need
                _ = list(map(int, fh.readline().strip().split()))

        return cls.from_tensor_list(tensor_list)

    def to_statevector(self, qiskit_order=False, max_qubit_equivalent=20):
        """
        Decompose a given TTN into statevector form.

        Parameters
        ----------
        qiskit_order : bool, optional
            If true, the order is right-to-left. Otherwise left-to-right
            (which is the usual order in physics). Default to False.
        max_qubit_equivalent : int, optional
            Maximum number of qubits for which the statevector is computed.
            i.e. for a maximum hilbert space of 2**max_qubit_equivalent.
            Default to 20.

        Returns
        -------

        psi : instance of :class:`_AbstractQteaTensor`
            The statevector of the system
        """
        if np.prod(self.local_dim) > 2**max_qubit_equivalent:
            raise Exception(
                "Hilbert space %d**" % (self.local_dim)
                + "%d is too large to " % (self.num_sites)
                + "convert to statevector."
            )

        current_layer = self[-1]

        for ii in range(self.num_layers - 1):
            fused = current_layer.fuse_all_children()

            parent_layer = deepcopy(self[-2 - ii])
            parent_layer.contr_rmats(fused)

            current_layer = parent_layer

        # Top layer with two tensors
        psi = current_layer[0].tensordot(current_layer[1], [[2], [2]])
        if qiskit_order:
            order = "F"
        else:
            order = "C"

        return psi.reshape(self.local_dim).reshape(np.prod(self.local_dim), order=order)

    def to_tensor_list(self):
        """
        Return the tensors in the TTN as a nested list

        Returns
        -------
        list of lists numpy ndarray
            Tensors that will constitute the TTN
        """
        tensor_list = []
        for ii in range(self.num_layers - 1, -1, -1):
            tensor_list.append(self[ii][:])

        return tensor_list

    def to_mps_tensor_list(self, conv_params=None):
        r"""
        Map a binary TTN to a 1-layer tensor list that can be used
        to initialize an MPS with :py:function:`MPS.from_tensor_list(tensor_list)`.

        At each iteration the algorithm performs the operations highlighted in the
        codeblock below.

        .. codeblock::
              o-------o           o---o---o---o
             / \     / \  ====>   |   |   |   | ====>  o---o---o---o
            o   o   o   o         o   o   o   o       / \ / \ / \ / \

        Parameters
        ----------
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use in the procedure. If None is given,
            then use the default convergence parameters of the TTN.
            Default to None.

        Returns
        -------
        list of numpy ndarray
            Tensors that will constitute the MPS
        numpy ndarray
            Singular values cut in the procedure
        """
        # First, isometrize the top
        self.isometrize_all()

        # Start from uppermost layer
        curr_layer = self[0]  # Contains the current layer of tensors
        new_layer = []  # New layer being built
        cuts = []  # Approximation done in the procedure

        # Reshape first layer adding a dummy link for working with rank-4 tensors until the end
        # The convention is the following: links are numbered left to right, like in an MPS. This
        # means that, in the upper layer, we have [dummy, left_child, right_child, parent] on the
        # left tensor, while on the right we have [parent, left_child, right_child, dummy]
        # for curr_layer[0] we use only up to shpae[:-1] because we neglect the symmetry index
        curr_layer[0] = curr_layer[0].reshape([1] + list(curr_layer[0].shape[:-1]))
        curr_layer[1] = curr_layer[1].transpose([2, 0, 1])
        curr_layer[1] = curr_layer[1].reshape(list(curr_layer[1].shape) + [1])

        # Cycle over the TTN layers, up to the last
        for idx in range(self.num_layers - 1):
            # print(f'Layer {idx} contracting into {idx+1} over {len(self[:])} layers')
            for tens_idx, tens in enumerate(curr_layer):
                # First, divide the tensor with an SVD, such that each tensor in layer idx+1 has a
                # corresponding layer in the upper tensor, instead of 1/2 of them
                tens_left, tens_right, _, cut = tens.split_svd(
                    [0, 1], [2, 3], contract_singvals="R", conv_params=conv_params
                )
                tens_left_next = self[idx + 1][tens_idx * 2]
                tens_right_next = self[idx + 1][tens_idx * 2 + 1]

                # Contract each tensor in layer idx with its correspondent in layer idx+1
                new_tens_left = tens_left.tensordot(tens_left_next, ([1], [2]))
                new_tens_right = tens_right.tensordot(tens_right_next, ([1], [2]))
                # Transpose the legs in the correct format
                new_tens_right = new_tens_right.transpose([0, 2, 3, 1])
                new_tens_left = new_tens_left.transpose([0, 2, 3, 1])

                # Save the new tensor in the next layer
                new_layer.append(new_tens_left)
                new_layer.append(new_tens_right)
                cuts.append(cut)

            # Update variables for next cycle
            curr_layer = new_layer
            new_layer = []

        # Pass from a list of n/2 4-legs tensors to a list of n 3-legs tensors
        # that you can use to initialize an MPS
        tensor_list = []
        for tens in curr_layer:
            tens_left, tens_right, _, cut = tens.split_svd(
                [0, 1], [2, 3], contract_singvals="R", conv_params=conv_params
            )

            tensor_list.append(tens_left)
            tensor_list.append(tens_right)
            cuts.append(cut)

        return tensor_list, cuts

    @classmethod
    def from_tensor_list(
        cls, tensor_list, singvals_list=None, tensor_backend=None, conv_params=None
    ):
        """
        Construct a TTN from a listed list of tensors. The outer list contains
        the layers, the inner list contains the tensors within a layer.

        The local Hilbert space is the first list entry and the uppermost
        layer in the TTN is the last list entry. The first list will have
        num_sites / 2 entries. The uppermost list has two entries.

        The order of the legs is always left-child, right-child, parent with
        the exception of the left top tensor. The left top tensor has an
        additional link, i.e., the symmetry selector; the order is left-child,
        right-child, parent, symmetry-selector.

        Also see :py:func:`mps_simulator.MPS.to_ttn`.
        """
        # For now assume binary trees
        number_children = 2
        num_sites = number_children * len(tensor_list[0])

        # Do not assume equal local dimensions
        local_dim = []
        for elem in tensor_list[0]:
            local_dim.append(elem.shape[0])
            local_dim.append(elem.shape[1])

        # convergence parameters are hard-coded for now, find a meaningful
        # bond dimension
        if conv_params is None:
            chi = 1 + int(
                np.max(
                    np.array([np.max(xx.shape) for sub in tensor_list for xx in sub])
                )
            )
            conv_params = TNConvergenceParameters(max_bond_dimension=chi)

        obj = cls(
            num_sites,
            conv_params,
            local_dim=local_dim,
            initialize="empty",
            tensor_backend=tensor_backend,
        )
        tensor_cls = obj._tensor_backend.tensor_cls

        idx = obj.num_layers
        last_dim = num_sites
        for jdx, sub in enumerate(tensor_list):
            idx -= 1

            if last_dim / 2 != len(sub):
                raise Exception("Length of tensor list not correct.")

            last_dim = len(sub)

            for kdx, elem in enumerate(sub):
                if not isinstance(elem, _AbstractQteaTensor):
                    elem = tensor_cls.from_elem_array(elem)
                obj[idx].append(elem)
                if singvals_list is None:
                    obj[idx].singvals[kdx] = None
                else:
                    obj[idx].singvals[kdx] = singvals_list[jdx][kdx]

        obj.convert(obj._tensor_backend.dtype, obj._tensor_backend.device)

        return obj

    @classmethod
    def product_state_from_local_states(
        cls,
        mat,
        padding=None,
        convergence_parameters=None,
        tensor_backend=None,
    ):
        """
        Construct a product (separable) state in TTN form, given the local
        states of each of the sites.

        Parameters
        ----------
        mat : np.array of rank 2
            Matrix with ii-th row being a (normalized) local state of
            the ii-th site.
            Number of rows is therefore equal to the number of sites,
            and number of columns corresponds to the local dimension.

        padding : np.array of length 2 or `None`, optional
            Used to enable the growth of bond dimension in TDVP algorithms
            for TTN (necessary as well for two tensor updates).
            If not `None`, all the TTN tensors are padded such that the bond
            dimension is equal to `padding[0]`. The value `padding[1]`
            tells with which value are we padding the tensors. Note that
            `padding[1]` should be very small, as it plays the role of
            numerical noise.
            If False, the bond dimensions are equal to 1.
            Default to None.

        convergence_parameters : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters for the new TTN.

        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Return
        ------
        prod_ttn : :py:class:`TTN`
            Corresponding product state TTN.
        """
        if len(mat.shape) != 2:
            raise Exception("numpy ndarray must be of rank-2.")
        for ii in range(0, mat.shape[0]):
            norm = np.linalg.norm(mat[ii, :])
            if abs(norm - 1) > 10e-5:
                raise ValueError(
                    f"Local state on site {ii+1} not normalized. " f"Norm = {norm}."
                )

        num_sites, local_dim = mat.shape

        if padding is not None:
            pad, pad_value = padding[0], padding[1]

        # convergence parameters are hard-coded for now
        if convergence_parameters is None:
            convergence_parameters = TNConvergenceParameters(
                max_bond_dimension=local_dim
            )

        # initialize the TTN
        prod_ttn = cls(
            num_sites,
            convergence_parameters,
            local_dim=local_dim,
            tensor_backend=tensor_backend,
            initialize="empty",
        )

        # Bottom layer contains physical Hilbert space. We merge local states
        # into rank-2 tensors via Kronecker product.
        for ii in range(prod_ttn.num_sites // 2):
            # indices of states we want to merge into new rank-2 tensor
            i1 = 2 * ii
            i2 = i1 + 1

            # dimension of new tensor
            dims = [local_dim, local_dim, 1]
            # compute new tensor
            theta = np.kron(mat[i1, :], mat[i2, :])

            theta = np.reshape(theta, [local_dim, local_dim, 1])
            if padding is not None:
                theta = np.pad(
                    theta, ((0, 0), (0, 0), (0, pad - 1)), constant_values=pad_value
                )
            prod_ttn[-1].append(tensor_backend.tensor_cls.from_elem_array(theta))
        prod_ttn[-1].singvals = [np.ones(1) for _ in range(prod_ttn.num_sites // 2)]

        # Tensors in remaining layers are rank-3 tensor with all links
        # being of dimension 1, or `pad` in the case of padding
        # (symmetry sector is added in next step).
        tensor_fill = np.reshape(np.array([1], dtype=float), [1, 1, 1])
        if padding is not None:
            tensor_fill = np.pad(
                tensor_fill,
                ((0, pad - 1), (0, pad - 1), (0, pad - 1)),
                constant_values=pad_value,
            )
        tensor_fill = tensor_backend.tensor_cls.from_elem_array(tensor_fill)
        idx = prod_ttn.num_layers - 2
        last_dim = prod_ttn.num_sites // 2
        for ii in range(idx, -1, -1):
            last_dim = last_dim // 2
            for _ in range(last_dim):
                prod_ttn[ii].append(tensor_fill)
            prod_ttn[ii].singvals = [np.ones(1) for _ in range(last_dim)]

        # Top layer has to be conform with symmetry sector even if
        # TTN has no symmetry.
        if prod_ttn.is_ttn:
            if padding is not None:
                dims = [prod_ttn[0][0].shape[0], prod_ttn[0][0].shape[1], pad, 1]
            else:
                dims = [prod_ttn[0][0].shape[0], prod_ttn[0][0].shape[1], 1, 1]
            prod_ttn[0][0] = prod_ttn[0][0].reshape(dims)

        prod_ttn[0].singvals = [np.ones(1) for _ in range(prod_ttn[0].num_tensors)]

        prod_ttn.convert(
            prod_ttn._tensor_backend.dtype, prod_ttn._tensor_backend.device
        )

        return prod_ttn

    def extend_local_hilbert_space(self, number_levels):
        """
        Extend the local Hilbert by a certain number of levels without
        population. Extends the lowest layer with physical Hilbert space
        in the tree.

        Parameters
        ----------

        number_levels : int
            Defines the number of levels to be added. The levels are
            always appended to the end.
        """
        self[-1].extend_local_hilbert_space(number_levels)

    def isometrize_all(self):
        """
        Isometrize towards [0, 0] with no assumption of previous
        isometry center, e.g., works as well on random states.

        Returns
        -------

        None
        """
        if self.iso_center is not None:
            if (self.iso_center[0] == 0) and (self.iso_center[1] == 0):
                return

        for ii in range(1, self.num_layers):
            r_list = self[-ii].qr_towards_top(
                self._requires_singvals, self._convergence_parameters
            )
            self[-ii - 1].contr_rmats(r_list)

        if self.is_ttn:
            self[0].qr_top_right(self._requires_singvals, self._convergence_parameters)

        self.iso_center = [0, 0]

        return

    def get_path(self, target, start=None):
        """
        Calculates the path to a target, either starting
        at the isometry center or at a specified state.

        Parameters
        ----------

        target : list of two integers
            Destination in terms of layer index and tensor index.

        start : ``None`` or list of two integers, optional
            Starting point for the path; if ``None``, the
            isometry center is taken as the starting point.
            Default to ``None``

        Returns
        -------

        List of lists with six entries ... run
        # a QR on tensor path[*][1] in layer path[*][0] and r-link is
        # path[*][2]. Contract the r-tensor in tensor path[*][4]
        # in layer path[*][3] via link path[*][5].
        """
        path_down = []
        path_up = []

        needs_qr_top_tensors = True

        if start is None:
            start = self.iso_center

        if (target[0] == start[0]) and (target[1] == start[1]):
            # Target and start are identical
            return []

        # Construct the path going up
        for ii in range(1, self.num_layers):
            idx = self.num_layers - ii

            # Path up
            if (len(path_up) == 0) and (start[0] == idx):
                # Current iso center is in this layer - first action
                parent_tensor = start[1] // 2
                parent_link = start[1] % 2
                path_up.append(
                    [start[0], start[1], 2, start[0] - 1, parent_tensor, parent_link]
                )
            elif len(path_up) != 0:
                child_layer = path_up[-1][3]
                child_tensor = path_up[-1][4]

                parent_tensor = child_tensor // 2
                parent_link = child_tensor % 2

                path_up.append(
                    [
                        child_layer,
                        child_tensor,
                        2,
                        child_layer - 1,
                        parent_tensor,
                        parent_link,
                    ]
                )

            if (
                (len(path_up) != 0)
                and (path_up[-1][3] == target[0])
                and (path_up[-1][4] == target[1])
            ):
                # The parent tensor matches the target ... stop
                needs_qr_top_tensors = False
                break

            # Path down
            if (len(path_down) == 0) and (target[0] == idx):
                # New target iso is in this layer - last action
                parent_tensor = target[1] // 2
                parent_link = target[1] % 2
                path_down.insert(
                    0,
                    [
                        target[0] - 1,
                        parent_tensor,
                        parent_link,
                        target[0],
                        target[1],
                        2,
                    ],
                )
            elif len(path_down) != 0:
                child_layer = path_down[0][0]
                child_tensor = path_down[0][1]

                parent_tensor = child_tensor // 2
                parent_link = child_tensor % 2

                path_down.insert(
                    0,
                    [
                        child_layer - 1,
                        parent_tensor,
                        parent_link,
                        child_layer,
                        child_tensor,
                        2,
                    ],
                )

            if (
                (len(path_down) != 0)
                and (path_down[0][0] == start[0])
                and (path_down[0][1] == start[1])
            ):
                # The parent tensor matches the start ... stop
                needs_qr_top_tensors = False
                break

            # Check if the parent tensors of both paths match
            # By definition, the have to be in the same layer now,
            # just check the tensor
            if (
                (len(path_down) != 0)
                and (len(path_up) != 0)
                and (path_up[-1][4] == path_down[0][1])
            ):
                needs_qr_top_tensors = False
                break

        if needs_qr_top_tensors and (len(path_up) == 0):
            # Start is in the top layer
            if start[1] == 0:
                # QR from left to right
                path_up.append([0, 0, 2, 0, 1, 2])
            else:
                # QR from right to left
                path_up.append([0, 1, 2, 0, 0, 2])
        elif needs_qr_top_tensors and (path_up[-1][4] == 0):
            # QR from left to right
            path_up.append([0, 0, 2, 0, 1, 2])
        elif needs_qr_top_tensors:
            # QR from right to left
            path_up.append([0, 1, 2, 0, 0, 2])

        complete_path = path_up + path_down

        return complete_path

    def _iso_towards_via_cache(
        self, tensor_jj, start, target, state_jj, trunc=False, conv_params=None
    ):
        """
        Run isometrization from a start site to a target site for given
        tensor using the tensors in the cache for specific states.

        Paramters
        ---------
        tensor_jj :

        start :

        target :

        state_jj :

        trunc : Boolean, optional
            If `True`, the shifting is done via truncated SVD.
            If `False`, the shifting is done via QR.
            Default to `False`.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD. If `None`, convergence
            parameters are taken from the TTN. If isometry shifting
            is performed via QR, conv_params is set to `None` automatically.
            Default to `None`.

        Return
        ------
        tensor_jj :
        """
        key_target = (target[0], target[1], tuple(state_jj))
        if key_target in self._cache_get_children_prob:
            return self._get_cache(key_target)

        complete_path = self.get_path(target, start=start)

        for elem in complete_path:
            # Direction: going up (+1), going down (-1), or
            # horizontal (0, top tensors)
            direction = elem[0] - elem[3]

            # Construct the key for storing qmat (always store full state)
            if direction == 1:
                # Going up
                tuple_q = tuple(state_jj)

                if elem[5] == 1:
                    # Going up and contracting into the right child
                    # No need to store tensor
                    tuple_q = None
                elif elem[0] == self.num_layers - 1:
                    # For the lowest layer, we store the isometry
                    # center tensors, but not the orthogonalized
                    # ones
                    tuple_q = None
            elif direction == -1:
                # Going down
                tuple_q = tuple(state_jj)
            else:
                # Going horizontal
                tuple_q = tuple(state_jj)

            key_q = (elem[0], elem[1], tuple_q)

            # Construct the key for obtaining target tensor
            if direction == 1:
                # Going up
                delta = self.num_layers - elem[3] - 1
                nn = 2**delta
                tuple_t = tuple(state_jj[:-nn])

            elif direction == -1:
                # Going down
                tuple_t = None
            else:
                # Going horizontal
                tuple_t = None

            key_t = (elem[3], elem[4], tuple_t)
            target_tens = self._get_cache(key_t)

            r_link = elem[2]
            c_link = elem[5]

            # Get new q-tensor and new center-of-iso tensors
            new_q, tensor_jj, _, _ = self.shift_iso_to(
                tensor_jj,
                target_tens,
                r_link,
                c_link,
                trunc=trunc,
                conv_params=conv_params,
            )

            self._set_cache(key_q, new_q)

        # Set tensor itself in cache
        self._set_cache(key_target, tensor_jj)

        return tensor_jj

    def shift_leg_to(
        self,
        source_tens,
        target_tens,
        source_link,
        target_link,
        trunc=False,
        conv_params=None,
    ):
        """
        Shift a last leg from source tensor to target tensor by running a QR
        decomposition on source_tens and contracting R matrix with target_tens.
        If the shifting leg is not extra, i.e. does not come from contracting
        the 2-qubit gate, the procedure shifts the isometry center of the TTN.

        Parameters
        ----------
        source_tens : np.ndarray
            A tensor from which the leg is shifted. It is assumed that
            the leg to be shifted is on the last axis of this tensor.
            Run QR decomposition over one link of this tensor.

        target_tens : np.ndarray
            A tensor to which the leg is shifted.
            Contract R-matrix from QR into this tensor.

        source_link : int
            Run QR over the link `source_link` and last leg.

        target_link : int
            Contract R-matrix via the link `target_link` into the
            target tensor.

        trunc : Boolean, optional
            If `True`, the shifting is done via truncated SVD.
            If `False`, the shifting is done via QR.
            Default to `False`.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`. If leg shifting is performed via QR,
            conv_params is set to `None` automatically.
            Default to `None`.

        Return
        ------
        q_tens : np.ndarray
            New tensor taking the place of `source_tens`

        t_tens : np.ndarray
            New tensor taking the place of `target_tens`.
            If the shifting leg is not an extra leg, i.e.
            does not come from previously contracting the
            2-qubit gate,`target_tens` represents a new iso
            center.

        singvals_cut : float or None
            Singular values cut (if trunc=True) or None
        """
        no_truncation = not trunc

        # define some useful variables
        sdim = source_tens.ndim
        leg = sdim - 1
        # get the links which go to the left and to the
        # right in QR
        links = np.arange(sdim)
        links_right = [source_link, leg]
        links_left = np.delete(links, links_right).tolist()

        # define the correct permutation of the Q tensor for
        # after the QR based on the source_link position
        qperm = (
            list(range(source_link)) + [sdim - 2] + list(range(source_link, sdim - 2))
        )
        # if truncating, perform the splitting via truncated SVD
        if trunc:
            q_tens, r_tens, _, singvals_cut = source_tens.split_svd(
                links_left,
                links_right,
                perm_left=qperm,
                contract_singvals="R",
                conv_params=conv_params,
                no_truncation=no_truncation,
            )
            singvals_cut = self._postprocess_singvals_cut(
                singvals_cut=singvals_cut, conv_params=conv_params
            )
        # otherwise split the tensor via QR
        else:
            q_tens, r_tens = source_tens.split_qr(
                links_left, links_right, perm_left=qperm
            )
            singvals_cut = None

        # contract the R tensor to the target_tensor
        # t_tens = np.tensordot(r_tens, target_tens, axes=[[1], [target_link]])
        t_tens = target_tens.tensordot(r_tens, [[target_link], [1]])

        # find the correct permutation of the new target tensor based
        # on the target_link position
        tdim = t_tens.ndim
        tperm = (
            list(range(target_link))
            + [tdim - 2]
            + list(range(target_link, tdim - 2))
            + [tdim - 1]
        )

        # apply the permutation
        t_tens = t_tens.transpose(tperm)

        return q_tens, t_tens, singvals_cut

    def leg_towards(
        self, pos, leg_start=None, leg_end=None, trunc=False, conv_params=None
    ):
        """
        The function shifts a selected leg from `pos[0]` to `pos[1]`.
        Remark: the set isometry center is automatically shifted
        throughout procedure. However, this isometry center corresponds to
        the real isometry center only when the shifting leg is not extra,
        i.e. does not come from contracting the 2-qubit gate. Nevertheless,
        when the applying the 2-qubit gate, the final position tensor will become
        the real isometry center outside this function, after contracting the
        gate to the second site.

        Parameters
        ----------
        pos : 2x2 array
            `pos[0,:]` indicates the position of the starting tensor, and
            `pos[1,:]` indicates the position of the destination tensor, such that
            `pos[ii,:]` = [layer_index, tensor_index].

        leg_start : `None` or int
            Use only if you want to shift one of the physical links to another
            physical site.
            Tells on which position in a tensor is a leg we want to shift.
            If `None`, it is assumed that the shifting leg is on the last axis.
            Note that counting starts from
            zero.
            Default to `None`.

        leg_end : `None` or int
            Use only if you want to shift one of the physical links to another
            physical site.
            Tells on which position in a destination tensor we want the extra
            leg to be. If `None`, a shifted leg is assumed to be put on the
            last axis.
            Default to `None`.

        trunc : Boolean, optional
            If `True`, the shifting is done via truncated SVD.
            If `False`, the shifting is done via QR.
            Default to `False`.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD. If `None`, convergence
            parameters are taken from the TTN.
            Default to `None`.

        Return
        ------
        np.ndarray
            Singualr values cut in the process of shifting the isometry center.
            Array of None if moved through the QR.
        """
        # TTN must have the isometry center installed on the starting tensor
        if any(self.iso_center != pos[0]):
            raise ValueError(
                "Isometry center needs to be installed on"
                f" the start tensor position {pos[0]}. Currently"
                f" it is {self.iso_center}."
            )

        # The initial shifting leg position can only be set if we are shifting
        # a physical leg from one site to another
        if (leg_start is not None) and (self[pos[0, 0]][pos[0, 1]].ndim > 3):
            raise ValueError(
                "Initial shifting leg position can only be set for rank-3 tensor."
            )

        # if leg_start is defined, permute it to the end and add a dummy leg
        # of dimension 1 on its initial place
        if leg_start is not None:
            # add a dummy leg
            self[pos[0, 0]][pos[0, 1]].attach_dummy_link(leg_start, False)

            # permute the leg to the end
            perm = np.arange(self[pos[0, 0]][pos[0, 1]].ndim)
            perm = np.delete(perm, leg_start + 1)
            perm = np.append(perm, leg_start + 1)

            self[pos[0, 0]][pos[0, 1]].transpose_update(perm)

        # get path from initial to target position
        path = self.get_path(target=pos[1], start=pos[0])

        # for each step in the path, QR decompose the
        # source tensor and contract with the target tensor
        # to shift the extra leg.
        singvals_cut_tot = []
        for step in path:
            # position of source tensor
            ind1 = step[0:2]
            # source tensor
            tensor1 = self[ind1[0]][ind1[1]]
            # R-link of source tensor for QR
            link1 = step[2]
            # position of target tensor
            ind2 = step[3:5]
            # target tensor
            tensor2 = self[ind2[0]][ind2[1]]
            # link for contraction of target tensor to
            # R-tensor from QR
            link2 = step[5]

            # shift the extra leg
            (
                self[ind1[0]][ind1[1]],
                self[ind2[0]][ind2[1]],
                svals_trunc,
            ) = self.shift_leg_to(
                tensor1, tensor2, link1, link2, trunc=trunc, conv_params=conv_params
            )
            svals_trunc = tensor1.get_of(svals_trunc)
            singvals_cut_tot.append(svals_trunc)

            # set the isometry center to the next tensor
            self.iso_center = ind2

        # if set, permute the extra leg to the desired position
        if leg_end is not None:
            ind2 = pos[1]

            tdim = self[ind2[0]][ind2[1]].ndim
            tperm = np.arange(tdim - 1)
            tperm = np.insert(tperm, leg_end, tdim - 1)
            self[ind2[0]][ind2[1]] = self[ind2[0]][ind2[1]].transpose(tperm)

        return np.array(singvals_cut_tot)

    def write(self, filename, cmplx=True):
        """
        Write the TTN into a FORTRAN compatible file.

        Parameters
        ----------

        filename: str
            Path to the file. Folders in the path must exists and
            are not created on-the-fly.

        cmplx: bool, optional
            If True the TTN is complex, real otherwise. Default to True

        Returns
        -------

        None
        """
        self.convert(None, "cpu")

        # Oldest compatible tn_state_treenetwork version (length must be 8)
        f90_ttn_version = "0.3.4   "

        num_tensors = 0
        for ii in range(self.num_layers):
            num_tensors += len(self[ii])

        with open(filename, "w") as fh:
            fh.write(f90_ttn_version + "\n")
            fh.write("F\n")
            fh.write("%d\n" % (self.num_sites))
            fh.write("%d\n" % (self.num_layers))
            fh.write("%d\n" % (num_tensors))

            # Now write the layers
            for ii in range(self.num_layers):
                self[ii].write(fh, f90_ttn_version, self.num_layers, cmplx=cmplx)

            # Information about isometry (no information up to now stored)
            fh.write("F\n")

        return

    def print_tensors(self, how_many_layers=None, how_many=None):
        """
        Prints the tensors in TTO layer by layer, together with their shape.

        Parameters
        ----------
        how_many_layers : int, optional
            Only the tensors from the first
            <how_many_layers> layers are printed.
            If how_many_layers = `None`, all tensors
            from all layers are printed.
            Default is `None`.
        how_many: int, array-like of ints, optional
            Only the first <how_many> tensors of the layer are printed.
            If None, all the tensors are printed. If int, this number of
            tensor are printed for each layer. If array-like, you can individually
            select the number of tensors to be printed. By default None.

        Return
        ------
        None
        """
        self.convert(None, "cpu")

        if how_many_layers is None:
            how_many_layers = self.num_layers
        if how_many_layers > self.num_layers or how_many_layers < 0:
            raise ValueError("Invalid number of layers")
        if how_many is None or np.isscalar(how_many):
            how_many = np.repeat(how_many, self.num_layers)
        elif len(how_many) != self.num_layers:
            raise ValueError(
                f"how_many should be int, None or have len=num_layers, not {len(how_many)}"
            )

        print("\n")
        for ii in range(0, how_many_layers):
            print("Layer", ii, ":")
            self.layers[ii].print_tensors(how_many[ii])
            print("\n")

        return None

    def print_tensor_shapes(self, how_many_layers=None, how_many=None):
        """
        Prints the shape of tensors in TTO, layer by layer.

        Parameters
        ----------
        how_many_layers : int, optional
            Only the shapes of tensors from the first
            <how_many_layers> layers are printed
            if how_many_layers = `None`, shapes of all of
            the tensors are printed.
            Default is `None`.
        how_many: int, array-like of ints, optional
            Only the first <how_many> tensors of the layer are printed.
            If None, all the tensors are printed. If int, this number of
            tensor are printed for each layer. If array-like, you can individually
            select the number of tensors to be printed. By default None.

        Return
        ------
        None
        """
        if how_many_layers is None:
            how_many_layers = self.num_layers
        if how_many_layers > self.num_layers or how_many_layers < 0:
            raise ValueError("Invalid number of layers")
        if how_many is not None:
            if np.isscalar(how_many):
                how_many = np.repeat(how_many, self.num_layers)
            elif len(how_many) != self.num_layers:
                raise ValueError(
                    f"how_many should be int, None or have len=num_layers, not {len(how_many)}"
                )

        print("\n")
        for ii in range(0, how_many_layers):
            print("Layer", ii, ":")
            self.layers[ii].print_tensor_shapes(how_many[ii])
            print("\n")

        return None

    def _set_cache(self, key, value):
        """
        Internal function helping to set tensor during projective
        measurements.

        Parameters
        ----------

        key : tuple with three entries
            Tuple contains layer index, tensor index, and
            a state description, where the state description
            is a tuple of integers itself. State can also
            be `None` if storage should be skipped.

        value : np.ndarray
            Tensor at the specified layer and tensor index
            with the same projective measurements of sites
            to the left.

        Details
        -------

        Tensors of the lowest layer with the physical Hilbert
        space are never stored in this cache.

        The cache cannot be modified during one sample, the
        cache cleaning must be called after projecting on
        the last site before starting the next sample.
        """
        if key in self._cache_get_children_prob:
            raise Exception("Cannot overwrite tensor: " + str(key))

        if key[2] is None:
            # Memory efficiency step, right child of
            # downward path
            return

        if self.num_layers - 1 == key[0]:
            self._cache_get_children_prob[key] = deepcopy(value)
        else:
            self._cache_get_children_prob[key] = value

        if self._cachelimit_bytes_get_children_prob is not None:
            size_bytes = value.getsizeof()
            self._cachesize_bytes_get_children_prob += size_bytes

    def _get_cache(self, key):
        """
        Internal function helping to retrieve tensors during projective
        measurements.

        Parameters
        ----------

        key : tuple with three entries
            Tuple contains layer index, tensor index, and
            a state description, where the state description
            is a tuple of integers itself.

        Returns
        -------

        tensor : np.ndarray
            Tensor at the specified layer and tensor index
            with the same projective measurements of sites
            to the left.
        """
        if key not in self._cache_get_children_prob:
            # Not found in dict : key[0] and key[1] must be layer
            # and tensor index
            return self[key[0]][key[1]]

        # Key exists ...
        if key[2] is None:
            raise Exception("State not provided correctly")

        return self._cache_get_children_prob[key]

    def clear_cache(self, num_qubits_keep=None, all_probs=None, current_key=None):
        """
        Internal cache for unbiased measurements can grow
        quickly. This function can erase either the whole
        cache (with `num_qubits_keep == 0`) or measurements
        from `num_qubits_keep` upwards.

        **Arguments**

        num_qubits_keep : int or `None`, optional
            Delete at least all cached entries for up to num_qubits_keep.
            `num_qubits < num_qubits_keeped` are deleted based on the
            cache limit. Higher number of qubits are less likely to be
            accessed by other measurements.
            Default to `None` (clear enough to meet cache limit if set)

        current_key : str or `None`, optional
            If we empty the cache by the strategy ``state``, we need
            the current state as a (generalized) bitstring.
            Default to `None` (will fallback to num_qubit strategy)

        all_probs : list of dicts or `None`, optional
            Contains already calculated branches of probability tree. If cache
            of TTN is deleted, corresponding entries of the `all_probs` have
            to be deleted as well, otherwise they use the "wrong" tensor in the
            TTN afterwards, i.e., wrong in terms of the direction of the
            isometrization.
            Default to `None` (potential side-effects, see details)

        **Details**

        There is a tricky part when using this for cleaning
        during a superiteration, where `all_probs` has to
        be delete up to the same number of qubits.
        """
        if num_qubits_keep is None:
            pass
        elif num_qubits_keep == 0:
            # Quick return, delete all (respect independent of cache size)
            self._cache_get_children_prob = {}
            self._cachesize_bytes_get_children_prob = 0
            return {}
        else:
            # Backwards compatibility (delete up to users wish even in cache
            # size None or not exceeded)
            all_probs = self._clear_cache_by_num_qubits(all_probs, num_qubits_keep)

        if self._cachelimit_bytes_get_children_prob is None:
            # Nothing more to do, cache size not set by user
            return all_probs

        cachesize = self._cachesize_bytes_get_children_prob
        cachelimit = self._cachelimit_bytes_get_children_prob
        if cachesize < cachelimit:
            # Nothing to do, cache size still below limit
            return all_probs

        is_strategy_state = self._cache_clearing_strategy == "state"
        is_strategy_state = is_strategy_state and (current_key is not None)

        if is_strategy_state:
            all_probs, status = self._clear_cache_by_state(all_probs, current_key)

            if status:
                return all_probs

        # Change strategy in all cases, cache limit not reached yet, warning
        # was thrown inside function is going via state strategy
        is_strategy_state = False

        if not is_strategy_state:
            all_probs = self._clear_cache_by_num_qubits(all_probs, num_qubits_keep)

        return all_probs

    def _clear_cache_by_state(self, all_probs, current_key, reduce_to=0.9):
        """
        Cleaning cache by identifying different states.
        """
        previously_deleted_keys = []
        for key in self._clear_cache_by_state_step(current_key, reduce_to):
            # Stored is not the length of the key, but the qubit where
            # we are at in py-index. Thus, at the (n-1)-th qubit, we have n
            # projective measurements and a length of n
            ii = len(key) - 1

            if all_probs is not None:
                key_str = ",".join(map(str, key))

                if key_str in previously_deleted_keys:
                    continue
                previously_deleted_keys.append(key_str)

                try:
                    del all_probs[ii][key_str]
                except KeyError:
                    # site-cache in `abstract_tn` can delete entries, too. Keys do
                    # not neccessarily have to be present anymore. We could prevent
                    # in the `abstract_tn` the clearing of the cache for instances
                    # of TTNs to keep information
                    continue

        cachesize = self._cachesize_bytes_get_children_prob
        cachelimit = self._cachelimit_bytes_get_children_prob

        success_status = cachesize < cachelimit

        if not success_status:
            warnings.warn("Cache emptying strategy `state` not sufficient.")

        return all_probs, success_status

    def _clear_cache_by_state_step(self, current_key, reduce_to):
        """
        Cleaning cache by identifying different states; applying single step.
        """
        # Have to delete a sub-state, e.g., '0101' on four qubits, consistently
        # for every position in the TTN. Beyond that, other four-qubit states
        # like '0110' can remain
        keys_to_be_deleted = {}
        lens_to_be_deleted = []
        mapping = {}

        for key in self._cache_get_children_prob:
            nn = len(key[2])
            if key[2] != current_key[:nn]:
                # Different states, delete
                if key[2] not in keys_to_be_deleted:
                    keys_to_be_deleted[key[2]] = []
                    lens_to_be_deleted.append(nn)
                    mapping[len(mapping)] = key[2]

                keys_to_be_deleted[key[2]].append((key[0], key[1]))

        lens_to_be_deleted = np.array(lens_to_be_deleted)
        inds = np.argsort(lens_to_be_deleted)[::-1]

        for idx in inds:
            key2 = mapping[idx]

            for layer_idx, tensor_idx in keys_to_be_deleted[key2]:
                key = (layer_idx, tensor_idx, key2)

                if self._cachelimit_bytes_get_children_prob is not None:
                    size_bytes = self._cache_get_children_prob[key].getsizeof()
                    self._cachesize_bytes_get_children_prob -= size_bytes

                del self._cache_get_children_prob[key]
                yield key[2]

            if (
                self._cachesize_bytes_get_children_prob
                < reduce_to * self._cachelimit_bytes_get_children_prob
            ):
                break

    def _clear_cache_by_num_qubits_step(self, num_qubits_keep=0):
        """
        Internal cache for unbiased measurements can grow
        quickly. This function can erase either the whole
        cache (with `num_qubits_keep == 0`) or measurements
        from `num_qubits_keep` upwards.

        **Arguments**

        num_qubits_keep : int, optional
            Keep all cached entries for up to num_qubits_keep.
            Higher number of qubits are less likely to be
            accessed by other measurements.
        """
        if num_qubits_keep == 0:
            # Quick return, delete all
            self._cache_get_children_prob = {}
            self._cachesize_bytes_get_children_prob = 0
            return

        keys_to_delete = []
        for key in self._cache_get_children_prob:
            if len(key[2]) > num_qubits_keep:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            if self._cachelimit_bytes_get_children_prob is not None:
                size_bytes = self._cache_get_children_prob[key].getsizeof()
                self._cachesize_bytes_get_children_prob -= size_bytes

            del self._cache_get_children_prob[key]
            yield key[2]

    def _clear_cache_by_num_qubits(self, all_probs, num_qubits_keep):
        """
        Clear cache until cache size is below cache limit again. Function
        starts deleting intermediate results with the highest number of
        qubits first.

        **Arguments**

        all_probs : list of dicts
            Contains already calculated branches of probability tree. If cache
            of TTN is deleted, corresponding entries of the `all_probs` have
            to be deleted as well, otherwise they use the "wrong" tensor in the
            TTN afterwards, i.e., wrong in terms of the direction of the
            isometrization.
        """
        max_key_length = 0
        for key in self._cache_get_children_prob:
            max_key_length = max(max_key_length, len(key[2]))

        if num_qubits_keep is not None:
            start_with_length = min(num_qubits_keep, max_key_length)
        else:
            start_with_length = max_key_length

        for ii in range(start_with_length - 1, -1, -1):
            for key in self._clear_cache_by_num_qubits_step(num_qubits_keep=ii):
                pass

            if all_probs is not None:
                all_probs[ii] = {}

            cachesize = self._cachesize_bytes_get_children_prob
            cachelimit = self._cachelimit_bytes_get_children_prob
            if cachelimit is None:
                # on this level ignore if `None`
                continue

            if cachesize < cachelimit:
                break

        return all_probs

    def set_cache_limit_sampling(self, cache_limit_bytes):
        """
        Set a cache limit in bytes for the sampling procedure.

        **Arguments**

        cache_limit_bytes : int
            Size of the cache for sampling in bytes.
        """
        self._cachelimit_bytes_get_children_prob = cache_limit_bytes

    def set_cache_clearing_strategy_sampling(self, strategy):
        """
        Set strategy for clearing cache

        **Arguments**

        strategy : str
            Strategy to be applied, either `num_qubits` or `state`.
        """
        if strategy not in ["state", "num_qubits"]:
            raise Exception("Unknown cache clearing strategy %s." % (strategy))

        self._cache_clearing_strategy = strategy

    def shift_iso_to(
        self,
        source_tens,
        target_tens,
        source_link,
        target_link,
        trunc=False,
        conv_params=None,
    ):
        """
        Shift isometry from source tensor to target tensor.

        Parameters
        ----------
        source_tens : np.ndarray
            Run QR decomposition over one link of this tensor

        target_tens : np.ndarray
            Contract R-matrix from QR into this tensor.

        source_link : int
            Run QR over this link `source_link`

        target_link : int
            Contract R-matrix via this link `target_link` into the
            target tensor.

        trunc : Boolean, optional
            If `True`, the shifting is done via truncated SVD.
            If `False`, the shifting is done via QR.
            Default to `False`.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD. If `None`, convergence
            parameters are taken from the TTN. If isometry shifting
            is performed via QR, conv_params is set to `None` automatically.
            Default to `None`.

        Returns
        -------
        qtens : np.ndarray
            New gauged tensor taking the place of `source_tens`

        t_tens : np.ndarray
            New gauge center taking the place of `target_tens`

        singvals_cut : np.ndarray
            Singular values cut in moving the iso. If the iso is moved through the
            QR then it is None.
        """
        if conv_params is None:
            conv_params = self._convergence_parameters

        no_truncation = not trunc
        is_q_outgoing = source_tens.are_links_outgoing[source_link]

        r_links = [source_link]
        q_links = source_tens._invert_link_selection(r_links)

        # Permute link back
        nn = len(source_tens.shape)
        lnk = source_link
        q_perm = list(range(lnk)) + [nn - 1] + list(range(lnk, nn - 1))

        if trunc or self._requires_singvals:
            # truncating, perform the splitting via truncated SVD
            left_mat, right_mat, singvals, singvals_cut = source_tens.split_svd(
                q_links,
                r_links,
                perm_left=q_perm,
                contract_singvals="R",
                conv_params=conv_params,
                no_truncation=no_truncation,
                is_link_outgoing_left=is_q_outgoing,
            )
            singvals_cut = self._postprocess_singvals_cut(
                singvals_cut=singvals_cut, conv_params=conv_params
            )
            singvals_cut = left_mat.get_of(singvals_cut)

        else:
            # Otherwise split the tensor via QR
            # print("shift_iso_to", tmp.ndim, q_perm, len(tmp.links))
            left_mat, right_mat = source_tens.split_qr(
                q_links,
                r_links,
                perm_left=q_perm,
                is_q_link_outgoing=is_q_outgoing,
            )
            singvals_cut = None
            singvals = None

        # Contract rmat into target_tensor
        tmp = target_tens.tensordot(right_mat, ([target_link], [1]))

        nn = len(target_tens.shape)
        lnk = target_link
        t_perm = list(range(lnk)) + [nn - 1] + list(range(lnk, nn - 1))

        t_tens = tmp.transpose(t_perm)

        return left_mat, t_tens, singvals_cut, singvals

    def _get_children_prob(self, tensor, site_idx, curr_state, do_clear_cache):
        """
        Compute the probability and the relative tensor state of all the
        children of site `site_idx` in the probability tree

        Parameters
        ----------

        tensor : np.ndarray
            Parent tensor, with respect to which we compute the children
            Not save against changes, will be modified during function, e.g.,
            due to cutting subtensor `tensor_jj = tensor[jj:jj+1, :, :]`

        site_idx : int
            Index of the parent tensor

        curr_state : str
            Comma-separated string tracking the current state of all
            sites already done with their projective measurements.

        do_clear_cache : bool
            Flag if the cache should be cleared. Only read for first
            site when a new meausrement begins.

        Returns
        -------

        probabilities : list of floats
            Probabilities of the children

        tensor_list : list of ndarray
            Child tensors, already contracted with the next site
            if not last site.
        """
        # Get functions for elemtary arrays
        sqrt = tensor.get_attr("sqrt")

        # New measurements clean up the cache
        if (site_idx == 0) and do_clear_cache:
            self.clear_cache(num_qubits_keep=0)

        link_site = site_idx % 2
        local_dim = self.local_dim[site_idx]

        if tensor is None:
            # Response to the end of the loop, I assume
            tmp = tensor.vector_with_dim_like(local_dim)
            tmp *= 0.0
            return tmp, np.repeat(None, local_dim)

        # Build reduced density matrix
        if link_site == 0:
            reduced_rho = tensor.tensordot(tensor.conj(), ([1, 2], [1, 2]))
        else:
            reduced_rho = tensor.tensordot(tensor.conj(), ([0, 2], [0, 2]))

        # Convert to array on host/CPU with real values
        probabilities = reduced_rho.diag(real_part_only=True, do_get=True)

        tensors_list = []

        # Loop over basis states
        if np.abs(1 - probabilities.sum()) > tensor.dtype_eps * 1e2:
            print("reduced rho", site_idx, "#", curr_state)
            warnings.warn(
                "Reduced density matrix is not normalized; error = "
                + str(np.abs(1 - probabilities.sum()))
            )

        for jj, prob_jj in enumerate(probabilities):
            if (prob_jj > 0) and (link_site == 0):
                # link_site == 0 automatically fulfills site_idx < num_sites - 1

                # Projector is diagonal with one entry - cut entry for efficient
                # contractions (keep rank-3 structure)
                tensor_jj = tensor.subtensor_along_link(0, jj, jj + 1)

                # After scaling, we are done, the next site is as well in
                # this tensor
                tensor_jj /= sqrt(prob_jj)

                tensors_list.append(tensor_jj)
            elif (prob_jj > 0) and (site_idx < self.num_sites - 1):
                # Projector is diagonal with one entry - cut entry for efficent
                # QR (keep rank-3 structure)
                tensor_jj = tensor.subtensor_along_link(1, jj, jj + 1)

                state_jj = list(map(int, curr_state.split(","))) + [jj]

                # Scale tensor
                tensor_jj /= sqrt(prob_jj)

                # We are not done, we have to walk the TTN up and then down
                # the right path
                target_layer = self.num_layers - 1
                target_tensor = (site_idx + 1) // 2

                start = [target_layer, target_tensor - 1]
                target = [target_layer, target_tensor]

                tensor_jj = self._iso_towards_via_cache(
                    tensor_jj, start, target, state_jj
                )
                tensors_list.append(tensor_jj)
            else:
                tensors_list.append(None)

        return probabilities, tensors_list

    def _get_children_magic(self, *args, **kwargs):
        raise NotImplementedError("Function not implemented yet")

    def _get_child_prob(
        self,
        tensor,
        site_idx,
        target_prob,
        unitary_setup,
        curr_state,
        qiskit_convention,
    ):
        """
        Compute which child has to be selected for a given target probability
        and return the index and the tensor of the next site to be measured.

        Parameters
        ----------

        tensor : np.ndarray
            Tensor representing the site to be measured with a projective
            measurement.

        site_idx : int
            Index of the site to be measured and index of `tensor`.

        target_prob : scalar
            Scalar drawn from U(0, 1) and deciding on the which projective
            measurement outcome will be picked. The decision is based on
            the site `site_idx` only.

        unitary_setup : instance of :class:`UnitarySetupProjMeas` or `None`
            If `None`, no local unitaries are applied. Otherwise,
            unitary for local transformations are provided and applied
            to the local sites.

        curr_state : np.ndarray of rank-1 and type int
            Record of current projective measurements done so far.

        qiskit_convention : bool
            Qiskit convention, i.e., ``True`` stores the projective
            measurement in reverse order, i.e., the first qubit is stored
            in ``curr_state[-1]``. Passing ``False`` means indices are
            equal and not reversed.
        """
        # Get functions for elemtary arrays
        cumsum, sqrt = tensor.get_attr("cumsum", "sqrt")

        # New measurement clean up the cache
        if site_idx == 0:
            self.clear_cache(num_qubits_keep=0)

        link_site = site_idx % 2
        local_dim = self.local_dim[site_idx]

        if unitary_setup is not None:
            # Have to apply local unitary
            unitary = unitary_setup.get_unitary(site_idx)

            tensor = unitary.tensordot(tensor, ([1], [link_site]))
            if link_site == 1:
                # Need to permute links back to original order
                tensor = tensor.transpose([1, 0, 2])

        # Build reduced density matrix
        if link_site == 0:
            reduced_rho = tensor.tensordot(tensor.conj(), ([1, 2], [1, 2]))
        else:
            reduced_rho = tensor.tensordot(tensor.conj(), ([0, 2], [0, 2]))

        # Calculate the cumulated probabilities via the reduced
        # density matrix
        probs = reduced_rho.diag(real_part_only=True)
        cumul_probs = cumsum(probs)
        measured_idx = None

        # Check norm
        if np.abs(1 - cumul_probs[-1]) > tensor.dtype_eps * 1e2:
            raise Exception(
                "Reduced density matrix is not normalized; norm"
                + " is %2.6f." % (cumul_probs[-1])
            )

        for jj in range(local_dim):
            if cumul_probs[jj] < target_prob:
                continue

            prob_jj = probs[jj]

            # Reached interval with target probability ... project
            measured_idx = jj

            if link_site == 0:
                # link_site == 0 automatically fulfills site_idx < num_sites - 1

                # Projector is diagonal with one entry - cut entry for efficient
                # contractions (keep rank-3 structure)
                temp_tens = tensor.subtensor_along_link(0, jj, jj + 1)

                # After scaling, we are done, the next site is as well in
                # this tensor
                temp_tens /= sqrt(probs[jj])

            elif site_idx < self.num_sites - 1:
                # Projector is diagonal with one entry - cut entry for efficent
                # QR (keep rank-3 structure)
                temp_tens = tensor.subtensor_along_link(1, jj, jj + 1)

                if qiskit_convention:
                    state_jj = list(curr_state[::-1][:site_idx]) + [jj]
                else:
                    state_jj = list(curr_state[:site_idx]) + [jj]

                # Scale tensor
                temp_tens /= sqrt(probs[jj])

                norm_temp_tens = temp_tens.norm()
                if (
                    np.abs(1 - temp_tens.get_of(norm_temp_tens))
                    > tensor.dtype_eps * 1e2
                ):
                    raise Exception("Norm violation")

                # We are not done, we have to walk the TTN up and then down
                # the right path
                target_layer = self.num_layers - 1
                target_tensor = (site_idx + 1) // 2

                start = [target_layer, target_tensor - 1]
                target = [target_layer, target_tensor]

                temp_tens = self._iso_towards_via_cache(
                    temp_tens, start, target, state_jj
                )
            else:
                temp_tens = None

            break

        if temp_tens is not None:
            norm_temp_tens = temp_tens.norm()
            if np.abs(1 - temp_tens.get_of(norm_temp_tens)) > tensor.dtype_eps * 1e2:
                raise Exception("Norm violation")

        return measured_idx, temp_tens, prob_jj

    def unset_all_singvals(self):
        """
        Unset all the singvals in the TTN due to a
        local operation that is modifying the global
        state and the entanglement structure, such as
        a projective measurement.

        Returns
        -------
        None
        """
        for layer in self:
            for ii in range(layer.num_tensors):
                layer.unset_singvals(ii)

    #########################################################################
    ###################### Effective operators methods ######################
    #########################################################################
    def build_effective_operators(self, measurement_mode=False):
        """
        Build the complete effective operator on each
        of the links. Now assumes `self.eff_op` is set.
        """
        if self.iso_center is None:
            raise Exception("Need to isometrize to [0, 0], but is `None`.")

        if list(self.iso_center) != [0, 0]:
            raise Exception(f"Need to isometrize to [0, 0], but at {self.iso_center}.")

        if self.eff_op is None:
            raise Exception("Trying to build eff_op without attribute being set.")

        if not self.is_ttn:
            raise Exception("Double-check measurement setup and continue statements.")

        # loop over layers in TTN
        for layer in self.layers[::-1]:
            lidx = layer.layer_idx

            # loop over tensor index in a layer
            for tidx in range(len(layer) - 1, -1, -1):
                # tensor
                tens = layer[tidx]
                # position of a tensor: layer index, tensor index
                pos = (lidx, tidx)

                idx_out = 2
                pos_links = self.get_pos_links(pos)

                if lidx == 0 and tidx == 0 and (not measurement_mode):
                    # Would calculate entry towards (0, 1) and revert it again (TTN)
                    continue

                if lidx == 0 and tidx == 0:
                    # Want to finalize measurements, use symmetry selector
                    idx_out = 3
                    pos_links[-1] = (None, None)

                # get the effective operator for this tensor
                self.eff_op.contr_to_eff_op(tens, pos, pos_links, idx_out)

                if measurement_mode:
                    singvals = layer.singvals[tidx]
                    if lidx == 0 and tidx == 0:
                        singvals = None
                    elif singvals is None:
                        raise Exception("Missing singvals.")
                    self.eff_op[(pos, tuple(pos_links[idx_out]))].run_measurements(
                        tens, idx_out, singvals
                    )

    def _update_eff_ops(self, id_step):
        """
        Update the effective operators after the iso shift. Source tensor is
        iso position.

        Parameters
        ----------

        id_step : list of ints
            List with the iso path, i.e.
            [src_layer, src_tensor, src_link, dst_layer, dst_tensor, dst_link]

        Returns
        -------
        None
            Updates the effective operators in place
        """
        if tuple(id_step[:2]) != tuple(self.iso_center):
            print("Error information", id_step, self.iso_center)
            raise RuntimeError("Tried effective operators update not at the iso_center")

        # Information extracted from source tensor
        pos = (id_step[0], id_step[1])
        idx_out = id_step[2]
        tens = self[id_step[0]][id_step[1]]

        pos_links = self.get_pos_links(pos)
        self.eff_op.contr_to_eff_op(tens, pos, pos_links, idx_out)

    def deprecated_get_eff_op_on_pos(self, pos):
        """
        Obtain the list of effective operators adjacent
        to the position pos and the index where they should
        be contracted

        Parameters
        ----------
        pos : list
            list of [layer, tensor in layer]

        Returns
        -------
        list of IndexedOperators
            List of effective operators
        list of ints
            Indexes where the operators should be contracted
        """

        eff_ops = []
        idx_list = []
        # Link idx, operator idx
        for ll_idx, op_idx in enumerate(self[pos[0]].op_neighbors[:, pos[1]]):
            if op_idx != -1:
                eff_ops.append(self.eff_op[op_idx])
                idx_list.append(ll_idx)

        return eff_ops, idx_list

    #########################################################################
    ######################### Optimization methods ##########################
    #########################################################################
    def default_sweep_order(self):
        """
        Default sweep order to be used in the ground state search/time evolution.
        The optimization is bottom-top optimization
         - left to right in layer with index even
         - right to left in layer with index odd

        Returns
        -------
        List[Tuple[int]]
            The generator that you can sweep through
        """
        opt_path = []
        for ldx in range(self.num_layers - 1, -1, -1):
            if ldx % 2 == 0:
                opt_path += [(ldx, tdx) for tdx in range(self[ldx].num_tensors)]
            else:
                opt_path += [
                    (ldx, tdx) for tdx in range(self[ldx].num_tensors - 1, -1, -1)
                ]

        return opt_path

    def default_sweep_order_back(self):
        """Default sweep order backwards."""
        opt_path = []
        for ldx in range(self.num_layers - 1, -1, -1):
            opt_path_ii = []
            if ldx % 2 == 0:
                opt_path_ii += [(ldx, tdx) for tdx in range(self[ldx].num_tensors)]
            else:
                opt_path_ii += [
                    (ldx, tdx) for tdx in range(self[ldx].num_tensors - 1, -1, -1)
                ]

            opt_path += opt_path_ii[::-1]

        return opt_path

    def get_pos_partner_link_expansion(self, pos):
        """
        Get the position of the partner tensor to use in the link expansion
        subroutine.
        In TTN, it is always the parent tensor.

        Parameters
        ----------
        pos : Tuple[int]
            Position w.r.t. which you want to compute the partner

        Returns
        -------
        Tuple[int]
            Position of the partner
        int
            Link of pos pointing towards the partner
        int
            Link of the partner pointing towards pos
        """
        link_self, tdx_info = self._get_parent_info(pos)
        pos_partner = tuple(tdx_info[:2])
        link_partner = tdx_info[2]

        return pos_partner, link_self, link_partner

    def _partial_iso_towards_for_timestep(self, pos, next_pos, no_rtens=False):
        """
        Move by hand the iso for the evolution backwards in time

        Parameters
        ----------
        pos : Tuple[int]
            Position of the tensor evolved
        next_pos : Tuple[int]
            Position of the next tensor to evolve

        Returns
        -------
        QTeaTensor | link_self
            The R tensor of the iso movement
            link_self in no_rtens=True model
        Tuple[int]
            The position of the partner (the parent in TTNs)
        int
            The link of the partner pointing towards pos
        List[int]
            The update path to pass to _update_eff_ops
        """
        requires_singvals = self._requires_singvals

        # Needed in other TN geometries
        _ = next_pos
        link_self, tdx_info = self._get_parent_info(pos)

        pos_partner = tuple(tdx_info[:2])
        link_partner = tdx_info[2]

        nn = self[pos].ndim
        all_legs = np.array(range(nn))
        qlegs = list(all_legs[all_legs != link_self])

        path_elem = list(pos) + [link_self] + list(tdx_info)
        if no_rtens:
            return link_self, pos_partner, link_partner, path_elem

        if requires_singvals:
            qtens, rtens, s_vals, _ = self[pos].split_svd(
                qlegs,
                [link_self],
                no_truncation=True,
                conv_params=self._convergence_parameters,
                contract_singvals="R",
            )
            self.set_singvals_on_link(pos, pos_partner, s_vals)
        else:
            qtens, rtens = self[pos].split_qr(qlegs, [link_self])
            self.set_singvals_on_link(pos, pos_partner, None)
        if link_self + 1 != nn:
            # Have to permute
            qperm = list(range(link_self)) + [nn - 1] + list(range(link_self, nn - 1))
            self[pos] = qtens.transpose(qperm)
        else:
            self[pos] = qtens

        return rtens, pos_partner, link_partner, path_elem

    #########################################################################
    ############################ Apply methods ##############################
    #########################################################################

    def apply_one_site_operator(self, op, pos):
        """
        Applies a one operator `op` to the physical site `pos` of the TTN.

        Parameters
        ----------
        op: numpy array shape (local_dim, local_dim)
            Matrix representation of the quantum gate
        pos: int
            Position of the qubit where to apply `op`.

        """
        if pos < 0 or pos > self.num_sites - 1:
            raise ValueError(
                "The position of the site must be between 0 and (num_sites-1)"
            )
        # if list(op.shape) != [self._local_dim[pos]] * 2:
        #    raise ValueError(
        #        "Shape of the input operator must be (local_dim, local_dim)"
        #    )

        # The physical layer is always the last one
        physical_layer = self.num_layers - 1
        target_tensor = self[physical_layer][pos // 2]

        if pos % 2 == 0:
            # First index of the 3-legs tensor
            res = op.tensordot(target_tensor, ([1], [0]))
        else:
            # Second index of the 3-legs tensor
            res = op.tensordot(target_tensor, ([1], [1]))
            res = res.transpose([1, 0, 2])

        self[physical_layer][pos // 2] = res

    def apply_projective_operator(self, site, selected_output=None, remove=False):
        """
        Apply a projective operator to the site **site**, and give the measurement as output.
        You can also decide to select a given output for the measurement, if the probability is
        non-zero. Finally, you have the possibility of removing the site after the measurement.

        .. warning::

            Applying projective measurements/removing sites is ALWAYS dangerous. The information
            of the projective measurement should be in principle carried over the entire TTN,
            by iteratively applying SVDs across all the networks.
            However, this procedure is highly suboptimal, since it is not always necessary
            and will be processed by the following two-sites operators.
            Thus, the procedure IS NOT applied here. Take care
            that entanglement measures through :class:`TNObsBondEntropy` may give
            the None result. Furthermore, if working
            with parallel approaches, projective operators should be treated with even more
            caution, since they CANNOT be applied in parallel.

        Parameters
        ----------
        site: int
            Index of the site you want to measure
        selected_output: int, optional
            If provided, the selected state is measured. Throw an error if the probability of the
            state is 0
        remove: bool, optional
            If True, the measured index is traced away after the measurement. Default to False.

        Returns
        -------
        meas_state: int
            Measured state
        state_prob : float
            Probability of measuring the output state
        """
        if selected_output is not None and selected_output > self._local_dim[site] - 1:
            raise ValueError("The seleted output must be at most local_dim-1")

        physical_layer = self.num_layers - 1

        # Workaround in case we have an extra leg in the tensor due to a temporary site
        sites = np.cumsum([0] + [tens.ndim - 1 for tens in self[physical_layer]])
        tens_idx = np.nonzero(site < sites)[0][0] - 1
        leg_idx = site - sites[tens_idx]
        leg_dim = self[physical_layer][tens_idx].shape[leg_idx]
        if self[physical_layer][tens_idx].ndim < 4 and remove:
            raise RuntimeError(
                "Cannot remove site of tensor with only two physical legs"
            )

        # Set the orthogonality center
        self.iso_towards((physical_layer, tens_idx), keep_singvals=True)

        # Normalize
        old_norm = self.norm()
        self.scale(1 / old_norm)

        # Measure
        cum_prob = 0
        random_u = np.random.rand()
        # We don't use get_rho_ii since it can handle only physical tensors with 2
        # sites, while here we possibly have 3 sites
        tens = self[physical_layer][tens_idx]
        contr_legs = [ii for ii in range(tens.ndim) if ii != leg_idx]
        rho_ii = tens.tensordot(tens.conj(), (contr_legs, contr_legs))

        for ii in range(leg_dim):
            if selected_output is not None and ii != selected_output:
                continue
            projector = _projector_for_rho_i(ii, rho_ii)
            prob_ii = rho_ii.tensordot(projector, ([0, 1], [1, 0])).get_entry()
            cum_prob += np.real(prob_ii)
            if cum_prob >= random_u or selected_output == ii:
                meas_state = ii
                state_prob = prob_ii
                break

        # Remove the extra site or project into the correct
        # subspace
        if remove:
            projector_vect = rho_ii.zeros_like()
            projector_vect.set_diagonal_entry(meas_state, 1)

            # Project the state in the measured one
            tens_to_remove = tens.tensordot(projector_vect, ([leg_idx], [0]))
            self[physical_layer][tens_idx] = tens_to_remove
        else:
            new_tens = tens.tensordot(projector, ([leg_idx], [1]))
            new_tens = new_tens.transpose(_transpose_idx(tens.ndim, leg_idx))
            self[physical_layer][tens_idx] = new_tens

        # Unset all singvals since they are now outdated
        self.unset_all_singvals()

        # Renormalize and come back to previous norm
        self.normalize()
        self.scale(old_norm)

        return meas_state, state_prob

    def apply_two_site_operator(self, gate, sites, conv_params=None):
        """
        Applies a two-site operator `gate` to the TTN on sites `sites[0]`
        and `sites[1]`.

        Parameters
        ----------
        gate : np array of shape (local_dim*local_dim, local_dim*local_dim)
            Quantum gate to apply on a TTN. Note that links [2] and [3]
            of the gate are applied to the TTN.

        sites : list/array of two ints
            Left and right site on which to apply `gate`. The counting
            starts from 0.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`.

        Return
        ------
        np.ndarray
            Singular values cut in the process of shifting the isometry center.
            None if moved through the QR.
        """
        # first recast the site positions into tensors
        # and leg indices

        # transform input into np array just in case the
        # user passes the list
        sites = np.array(sites)

        # pos[0,:] indicates the position of the left site, and
        # pos[1,:] indicates the position of the right site, such that
        # pos[ii,:] = [tensor_index, leg_index]. Leg index can be 0 or 1.
        pos = np.zeros((2, 2), dtype=int)
        pos[:, 0] = sites // 2
        pos[:, 1] = sites % 2

        # Split the gate into two operators
        gate = gate.reshape((2, 2, 2, 2))
        conv_params_gate = TNConvergenceParameters(
            max_bond_dimension=int(self.local_dim[0] ** 2),
            trunc_method="N",
            cut_ratio=0,
        )
        op1, op2, _, _ = gate.split_svd(
            [0, 2], [1, 3], contract_singvals="R", conv_params=conv_params_gate
        )

        # Install the isometry center at the left operator site
        self.iso_towards([self.num_layers - 1, pos[0, 0]])

        # Contract the left operator with a physical site and transpose so that
        # extra leg is at the end
        self[-1][pos[0, 0]] = self[-1][pos[0, 0]].tensordot(op1, [pos[0, 1], [1]])
        self[-1][pos[0, 0]].transpose_update(
            [2 - 2 * pos[0, 1], 0 + 2 * pos[0, 1], 1, 3]
        )

        # Shift the extra link towards the site of the other operator, isometry center
        # is shifted automatically
        self.leg_towards(
            np.array(
                [[(self.num_layers - 1), pos[0, 0]], [(self.num_layers - 1), pos[1, 0]]]
            )
        )

        # Contract the right operator with the physical site. After this step,
        # the tensor network is in the shape of TTN.
        self[-1][pos[1, 0]] = self[-1][pos[1, 0]].tensordot(
            op2, [[3, pos[1, 1]], [0, 2]]
        )
        self[-1][pos[1, 0]].transpose_update([2 - 2 * pos[1, 1], 0 + 2 * pos[1, 1], 1])

        # Backpropagate the SVDs
        singvals_cut_tot = self.iso_towards(
            [self.num_layers - 1, pos[0, 0]],
            trunc=True,
            conv_params=conv_params,
            keep_singvals=True,
        )

        return singvals_cut_tot

    def apply_mpo(self, mpo):
        """
        Apply an MPO to the TTN on the sites `sites`.
        The MPO should have the following convention for the links:
        0 is left link. 1 is physical link pointing downwards.
        2 is phisical link pointing upwards. 3 is right link.

        The sites are encoded inside the DenseMPO class.

        Parameters
        ----------
        mpo : DenseMPO
            MPO to be applied

        Returns
        -------
        np.ndarray
            Singular values cutted when the gate link is contracted
        """
        # Sort sites
        # mpo.sort_sites()
        sites = np.array([mpo_site.site for mpo_site in mpo])
        if not np.isclose(sites, np.sort(sites)).all():
            raise RuntimeError("MPO sites are not sorted")

        # transform input into np array just in case the
        # user passes the list

        operators = [site.operator * site.weight for site in mpo]
        if mpo[0].strength is not None:
            operators[0] *= mpo[0].strength

        # pos[0,:] indicates the position of the left site, and
        # pos[1,:] indicates the position of the right site, such that
        # pos[ii,:] = [tensor_index, leg_index]. Leg index can be 0 or 1.
        pos = np.zeros((len(sites), 2), dtype=int)
        pos[:, 0] = sites // 2
        pos[:, 1] = sites % 2

        # Install the isometry center at the left operator site
        self.site_canonize(sites[0], keep_singvals=True)

        # Contract the left operator with a physical site and transpose so that
        # extra leg is at the end
        op1 = operators[0].remove_dummy_link(0)
        self[-1][pos[0, 0]] = self[-1][pos[0, 0]].tensordot(op1, [pos[0, 1], [1]])
        self[-1][pos[0, 0]].transpose_update(
            [2 - 2 * pos[0, 1], 0 + 2 * pos[0, 1], 1, 3]
        )

        for idx, site in enumerate(pos[1:, 0]):
            # Shift the extra link towards the site of the other operator, isometry center
            # is shifted automatically
            self.leg_towards(
                np.array(
                    [
                        [(self.num_layers - 1), pos[idx, 0]],
                        [(self.num_layers - 1), site],
                    ]
                )
            )

            # Contract the right operator with the physical site. After this step,
            # the tensor network is in the shape of TTN.
            op = operators[idx + 1]
            if idx == len(pos) - 2:
                op = op.remove_dummy_link(3)
                transpose_idxs = [2 - 2 * pos[idx + 1, 1], 0 + 2 * pos[idx + 1, 1], 1]
            else:
                transpose_idxs = [
                    2 - 2 * pos[idx + 1, 1],
                    0 + 2 * pos[idx + 1, 1],
                    1,
                    3,
                ]

            self[-1][site] = self[-1][site].tensordot(op, [[3, pos[1, 1]], [0, 2]])
            self[-1][site].transpose_update(transpose_idxs)

        for site in pos[:-1, 0][::-1]:
            # Backpropagate the SVDs
            singvals_cut_tot = self.iso_towards(
                [self.num_layers - 1, site], trunc=True, keep_singvals=True
            )

        return singvals_cut_tot

    def swap_qubits(self, sites, conv_params=None, trunc=True):
        """
        This function applies a swap gate to sites in a TTN,
        i.e. swaps these two qubits.

        Parameters
        ----------
        sites : list/array of two int
            The qubits on sites sites[0] and sites[1]
            are swapped.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`.

        trunc: bool, optional
            If True, move through SVDs, otherwise through QRs.
            Default to True.

        Return
        ------
        np.ndarray
            Singualr values cut in the process of shifting the isometry center.
            None if moved through the QR.
        """
        # first recast the site positions into tensors
        # and leg indices

        # transform input into np array just in case the
        # user passes the list
        sites = np.array(sites)

        # pos[0,:] indicates the position of the left site, and
        # pos[1,:] indicates the position of the right site, such that
        # pos[ii,:] = [tensor_index, leg_index]. Leg index can be 0 or 1.
        pos = np.zeros((2, 2), dtype=int)
        pos[:, 0] = sites // 2
        pos[:, 1] = sites % 2

        self.iso_towards([self.num_layers - 1, pos[0, 0]])

        # Shift the first leg from site 1 to site 2
        self.leg_towards(
            np.array(
                [[(self.num_layers - 1), pos[0, 0]], [(self.num_layers - 1), pos[1, 0]]]
            ),
            leg_start=pos[0, 1],
            leg_end=pos[1, 1],
        )

        tperm = np.arange(4)
        tperm = np.delete(tperm, pos[1, 1] + 1)
        tperm = np.append(tperm, pos[1, 1] + 1)

        self[-1][pos[1, 0]] = self[-1][pos[1, 0]].transpose(tperm)

        # Shift the second leg from site 2 to site 1 and backpropagate the
        # SVD truncation
        singvals_cut_tot = self.leg_towards(
            np.array(
                [[(self.num_layers - 1), pos[1, 0]], [(self.num_layers - 1), pos[0, 0]]]
            ),
            leg_end=pos[0, 1] + 1,
            trunc=trunc,
            conv_params=conv_params,
        )
        self[-1][pos[0, 0]].remove_dummy_link(pos[0, 1])

        return singvals_cut_tot

    #########################################################################
    ######################### Measurement methods ###########################
    #########################################################################

    def meas_local(self, op):
        """
        Measure a local observable along all sites of the TTN

        Parameters
        ----------
        op : ndarray, shape (local_dim, local_dim)
            local operator to measure

        Return
        ------
        measures : ndarray, shape (num_sites)
            Measures of the local operator along each site
        """
        self.check_obs_input(op)

        measures = np.zeros(self.num_sites)

        # This subroutine can be parallelized if the singvals are stored using
        # joblib
        for ii in range(self.num_sites):
            rho_i = self.get_rho_i(ii)

            if op.ndim == 2:
                expectation = rho_i.tensordot(op, ([0, 1], [1, 0]))
            else:
                tmp = deepcopy(op)
                tmp.trace_one_dim_pair([0, 3])
                expectation = rho_i.tensordot(tmp, ([0, 1], [1, 0]))
            measures[ii] = np.real(expectation.get_entry())

        return measures

    def meas_tensor_product(self, ops, idxs):
        """
        Measure the tensor products of n operators `ops` acting on the indexes `idxs`

        Parameters
        ----------
        ops : list of ndarrays
            List of numpy arrays which are one-site operators
        idxs : list of int
            Indexes where the operators are applied

        Returns
        -------
        measure : float
            Result of the measurement
        """
        self.check_obs_input(ops, idxs)
        # No operator to measure, return expectation value of identity (which is always 1)
        if len(idxs) == 0:
            return 1

        order = np.argsort(idxs)
        idxs = np.array(idxs)[order]
        ops = np.array(ops)
        ops = ops[order]

        # Inefficient way without transfer matrix. For an efficient implementation
        # see the MPS method.
        temp_ttn = deepcopy(self)

        # Apply local operators to TTN
        for idx, op in zip(idxs, ops):
            if op.ndim == 4:
                if (op.shape[3] == 1) and (op.shape[0] == 1):
                    op = op.copy().remove_dummy_link(3).remove_dummy_link(0)
                else:
                    raise RuntimeError(
                        "Only bond dimension 1 MPOs implemented in TTN meas_tensor_product"
                    )
            temp_ttn.apply_one_site_operator(op, idx)

        # Compute expectation  value through dot product.
        # It is inefficient, since if the observables are restricted to a subset of the
        # ttn we already know there are some contraction going to the identity for the
        # isometrization. For example, if the observable is only on the first quarter of
        # the tree, we know the remaining part contracts to the identity and we don't
        # need to compute it explicitely
        measure = temp_ttn.sandwich(self)

        # Move measure to host if necessary
        measure = np.real(ops[0].get_of(measure))

        return measure

    def meas_weighted_sum(self, op_strings, idxs_strings, coefs):
        """
        Measure the weighted sum of tensor product operators.
        See :py:func:`meas_tensor_product`

        Parameters
        ----------
        op_strings : list of lists of ndarray
            list of tensor product operators
        idxs_strings : list of list of int
            list of indexes of tensor product operators
        coefs : list of complex
            list of the coefficients of the sum

        Return
        ------
        measure : complex
            Result of the measurement
        """
        if not (
            len(op_strings) == len(idxs_strings) and len(idxs_strings) == len(coefs)
        ):
            raise ValueError(
                "op_strings, idx_strings and coefs must all have the same length"
            )

        measure = 0.0
        for ops, idxs, coef in zip(op_strings, idxs_strings, coefs):
            measure += coef * self.meas_tensor_product(ops, idxs)

        return measure

    def meas_bond_entropy(self):
        """
        Measure the entanglement entropy along all the sites of the MPS
        using the Von Neumann entropy :math:`S_V` defined as:

        .. math::

            S_V = - \\sum_i^{\\chi} s^2 \\ln( s^2)

        with :math:`s` the singular values

        Return
        ------
        measures : dict
            Keys are the range of the smallest bipartition to which the entanglement
            (value) is relative
        """
        # Get functions for elemtary arrays
        summ, log = self[0][0].get_attr("sum", "log")

        measures = {}
        for layer_idx, layer in enumerate(self):
            for idx, singvals in enumerate(layer.singvals):
                # If the singvals are not present for some reason the bond entropy
                # value for that bond is set to None
                if singvals is None:
                    s_von_neumann = None
                else:
                    # Remove 0s from the singvals (they might come from the from_statevector method)
                    singvals = singvals[singvals > 0]
                    s_von_neumann = -summ(singvals**2 * log(singvals**2))
                    s_von_neumann = self[0][0].get_of(s_von_neumann)

                pos_src = (layer_idx, idx)
                _, pos_parent = self._get_parent_info(pos_src)
                pos_parent = pos_parent[:2]
                sites_src, sites_dst = self.get_bipartition_link(pos_src, pos_parent)

                # Find the smaller bipartation and lower sites for equal bipartitions
                if len(sites_src) < len(sites_dst):
                    key = tuple([np.min(sites_src), np.max(sites_src)])
                elif len(sites_src) > len(sites_dst):
                    key = tuple([np.min(sites_dst), np.max(sites_dst)])
                elif sites_src[0] < sites_dst[0] and sites_src[-1] < sites_dst[-1]:
                    key = tuple([np.min(sites_src), np.max(sites_src)])
                elif sites_src[0] > sites_dst[0] and sites_src[-1] > sites_dst[-1]:
                    key = tuple([np.min(sites_dst), np.max(sites_dst)])
                else:
                    raise NotImplementedError(
                        "No rule implemented to choose bipartition."
                    )

                measures[key] = s_von_neumann

        return measures

    #########################################################################
    ######################## Visualisation methods ##########################
    #########################################################################

    def plot(
        self,
        fig,
        axis,
        link_quantity=None,
        plot_tensors=False,
        noticks=True,
        colormap="jet",
        cmap_label=None,
    ):
        """
        Plot the TTN in a matplotlib figure on a specific axis. The plot is a TTN,
        with links and tensors. The physical links are not represented.
        The color of the links is encoding the link_quantity value.
        For example, if the link quantity is the entanglement,
        the color of the link will encode the entanglement of that link.
        You can pass some quantity that will be represented as a colorcode on the link.

        TODO: add color code for quantities for the tensors too.

        Parameters
        ----------
        fig : matplotlib Figure
            The figure where to plot
        axis : matplotlib axis
            The axis where to plot
        link_quantity : np.ndarray, optional
            Colorcode of the link through np.ndarray of double, by default None.
            If None, black is used
        plot_tensors : bool, optional
            If True, plot tensors as white dots with black edge, by default False
        noticks : bool, optional
            If True, remove the ticks from the axis, by default True
        colormap : str, optional
            Colormap to use, by default "jet"
        cmap_label: str, optional
            Label of the colormap, by default None.

        Returns
        -------
        None
            Acts in place on the figure/axis
        """
        depth_dist = 1

        def bintree_level(x_coord, y_coord, width):
            """
            Function to get the segments to plot a
            single level of the TTN
            """
            segments = []
            y_left = y_coord + depth_dist
            x_left = x_coord - width / 2
            y_right = y_coord + depth_dist
            x_right = x_coord + width / 2
            segments.append([[x_coord, y_coord], [x_left, y_left]])
            segments.append([[x_coord, y_coord], [x_right, y_right]])
            return segments

        def bintree(levels, width):
            """
            Function to get the segments to plot
            all the TTN
            """
            segs = [[] for _ in range(levels)]
            x_coord, y_coord = (0, 0)
            for ii in range(levels):
                for jj in range(2**ii):
                    if ii > 0:
                        x_coord = segs[ii - 1][jj][1][0]
                        y_coord = segs[ii - 1][jj][1][1]
                    segs[ii] += bintree_level(x_coord, y_coord, width / (2**ii))
            new_segs = []
            for layer in segs:
                for seg in layer:
                    new_segs += [seg]

            return new_segs

        # Colors for the links
        cmap = plt.get_cmap(colormap)
        if link_quantity is not None:
            cnorm = colors.Normalize(vmin=link_quantity.min(), vmax=link_quantity.max())
            scalarmap = cmx.ScalarMappable(norm=cnorm, cmap=cmap)
            cols = [scalarmap.to_rgba(val) for val in link_quantity]
        else:
            cols = ["black"] * link_quantity

        # Generate the segments of the binary tree
        width_dist = 2
        levels = self.num_layers - 1
        segs = bintree(levels, width_dist)
        # Plot lines
        line_segments = LineCollection(
            segs, linewidths=2, colors=cols, linestyle="solid"
        )
        axis.add_collection(line_segments)

        # Generate and plot points (tensors)
        if plot_tensors:
            x_coord = [ii[0] for jj in segs for ii in jj]
            y_coord = [ii[1] for jj in segs for ii in jj]
            axis.scatter(x_coord, y_coord, c="white", edgecolors="black")
        axis.set_ylim(levels * depth_dist + 1, -1)
        axis.set_xlim(-1.5 * width_dist, 1.5 * width_dist)

        # Add colorbar to the figure
        if link_quantity is not None:
            fig.colorbar(scalarmap, ax=axis, label=cmap_label)

        if noticks:
            axis.tick_params(
                axis="both",  # changes apply to the x-axis
                which="both",  # both major and minor ticks are affected
                bottom=False,  # ticks along the bottom edge are off
                top=False,  # ticks along the top edge are off
                labelbottom=False,
                left=False,
                labelleft=False,
            )  # labels along the bottom edge are off
