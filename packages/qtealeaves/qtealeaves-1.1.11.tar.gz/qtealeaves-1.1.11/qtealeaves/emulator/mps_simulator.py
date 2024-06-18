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
The module contains a light-weight MPS emulator.
"""
from copy import deepcopy
from warnings import warn
from joblib import delayed, Parallel
import numpy as np
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.tensors import _AbstractQteaTensor
from .abstract_tn import _AbstractTN, postprocess_statedict, _projector_for_rho_i

__all__ = ["MPS"]


class MPS(_AbstractTN):
    """Matrix product states class

    Parameters
    ----------
    num_sites: int
        Number of sites
    convergence_parameters: :py:class:`TNConvergenceParameters`
        Class for handling convergence parameters. In particular, in the MPS simulator we are
        interested in:
        - the *maximum bond dimension* :math:`\\chi`;
        - the *cut ratio* :math:`\\epsilon` after which the singular
            values are neglected, i.e. if :math:`\\lamda_1` is the
            bigger singular values then after an SVD we neglect all the
            singular values such that :math:`\\frac{\\lambda_i}{\\lambda_1}\\leq\\epsilon`
    local_dim: int or list of ints, optional
        Local dimension of the degrees of freedom. Default to 2.
        If a list is given, then it must have length num_sites.
    initialize: str, optional
        The method for the initialization. Default to "vacuum"
        Available:
        - "vacuum", for the |000...0> state
        - "random", for a random state at given bond dimension
    requires_singvals : boolean, optional
        Allows to enforce SVD to have singular values on each link available
        which might be useful for measurements, e.g., bond entropy (the
        alternative is traversing the whole TN again to get the bond entropy
        on each link with an SVD).
    tensor_backend : `None` or instance of :class:`TensorBackend`
        Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.
    sectors : dict, optional
        Can restrict symmetry sector and/or bond dimension in initialization.
        If empty, no restriction.
        Default to None
    """

    extension = "mps"

    def __init__(
        self,
        num_sites,
        convergence_parameters,
        local_dim=2,
        initialize="vacuum",
        requires_singvals=False,
        tensor_backend=None,
        sectors=None,
        **kwargs,
    ):
        super().__init__(
            num_sites,
            convergence_parameters,
            local_dim=local_dim,
            requires_singvals=requires_singvals,
            tensor_backend=tensor_backend,
        )

        # Set orthogonality tracker for left/right-orthogonal form
        self._first_non_orthogonal_left = 0
        self._first_non_orthogonal_right = num_sites - 1

        # We can set numpy double, will be converted
        self._singvals = [None for _ in range(num_sites + 1)]

        # Initialize the tensors to the |000....0> state
        self._tensors = []
        self._initialize_mps(initialize)

        # Attribute used for computing probabilities. See
        # meas_probabilities for further details
        self._temp_for_prob = {}

        # Variable to save the maximum bond dimension reached at any moment
        self.max_bond_dim_reached = 1

        # Each tensor has 3 links, but all tensors share links. So effectively
        # we have 2 links per tensor, plus one at the beginning and one at the end
        self.num_links = 2 + 2 * num_sites
        self.sectors = sectors
        # Contains the index of the neighboring effective operator in
        # a 1-d vector of operators. Each vector op_neighbors(:, ii)
        # contains the index of a link for the ii-th tensor in this layer.
        # 0-o-2-o-4-o-6-o-8  --->   i -o- i+2
        #   |1  |3  |4  |5             | i+1
        self.op_neighbors = np.zeros((3, num_sites), dtype=int)
        self.op_neighbors[0, :] = np.arange(0, 2 * num_sites, 2)
        self.op_neighbors[1, :] = np.arange(1, 2 * num_sites, 2)
        self.op_neighbors[2, :] = np.arange(2, 2 * num_sites + 1, 2)

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
            True,  # TNPbsProjective
            True,  # TNObsProbabilities
            True,  # TNObsBondEntropy
            False,  # TNObsTZeroCorr
            False,  # TNObsCorr4
            False,  # TNObsCustom
        ]
        # MPS initializetion not aware of device
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
        return self.num_sites - 1

    @property
    def tensors(self):
        """List of tensors componing the MPS"""
        return self._tensors

    @property
    def singvals(self):
        """List of singular values in the bonds"""
        return self._singvals

    @property
    def first_non_orthogonal_left(self):
        """First non orthogonal tensor starting from the left"""
        return self._first_non_orthogonal_left

    @property
    def first_non_orthogonal_right(self):
        """First non orthogonal tensor starting from the right"""
        return self._first_non_orthogonal_right

    @property
    def iso_center(self):
        """
        Output the gauge center if it is well defined, otherwise None
        """
        if self.first_non_orthogonal_left == self.first_non_orthogonal_right:
            center = self.first_non_orthogonal_right
        else:
            center = None
        return center

    @iso_center.setter
    def iso_center(self, value):
        self._first_non_orthogonal_left = value
        self._first_non_orthogonal_right = value

    @property
    def physical_idxs(self):
        """Physical indices property"""
        return self.op_neighbors[1, :].reshape(-1)

    @property
    def current_max_bond_dim(self):
        """Maximum bond dimension of the mps"""
        max_bond_dims = [tt.shape for tt in self]
        return np.max(max_bond_dims)

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __repr__(self):
        """
        Return the class name as representation.
        """
        return self.__class__.__name__

    def __len__(self):
        """
        Provide number of sites in the MPS
        """
        return self.num_sites

    def __getitem__(self, key):
        """Overwrite the call for lists, you can access tensors in the MPS using

        .. code-block::
            MPS[0]
            >>> [[ [1], [0] ] ]

        Parameters
        ----------
        key : int
            index of the MPS tensor you are interested in

        Returns
        -------
        np.ndarray
            Tensor at position key in the MPS.tensor array
        """
        return self.tensors[key]

    def __setitem__(self, key, value):
        """Modify a tensor in the MPS by using a syntax corresponding to lists.
        It is the only way to modify a tensor

        .. code-block::
            tens = np.ones( (1, 2, 1) )
            MPS[1] = tens


        Parameters
        ----------
        key : int
            index of the array
        value : np.array
            value of the new tensor. Must have the same shape as the old one
        """
        if not isinstance(value, _AbstractQteaTensor):
            raise TypeError("New tensor must be an _AbstractQteaTensor.")
        self._tensors[key] = value

        return None

    def __iter__(self):
        """Iterator protocol"""
        return iter(self.tensors)

    def __add__(self, other):
        """
        Add two MPS states in a "non-physical" way. Notice that this function
        is higly inefficient if the number of sites is very high.
        For example, adding |00> to |11> will result in |00>+|11> not normalized.
        Remember to take care of the normalization yourself.

        Parameters
        ----------
        other : MPS
            MPS to concatenate

        Returns
        -------
        MPS
            Summation of the first MPS with the second
        """
        if not isinstance(other, MPS):
            raise TypeError("Only two MPS classes can be summed")
        elif self.num_sites != other.num_sites:
            raise ValueError("Number of sites must be the same to concatenate MPS")
        elif np.any(self.local_dim != other.local_dim):
            raise ValueError("Local dimension must be the same to concatenate MPS")

        max_bond_dim = max(
            self.convergence_parameters.max_bond_dimension,
            other.convergence_parameters.max_bond_dimension,
        )
        cut_ratio = min(
            self._convergence_parameters.cut_ratio,
            other._convergence_parameters.cut_ratio,
        )
        convergence_params = TNConvergenceParameters(
            max_bond_dimension=int(max_bond_dim), cut_ratio=cut_ratio
        )

        tensor_list = []
        idx = 0
        for tens_a, tens_b in zip(self, other):
            shape_c = np.array(tens_a.shape) + np.array(tens_b.shape)
            shape_c[1] = tens_a.shape[1]
            if idx == 0 and [tens_a.shape[0], tens_b.shape[0]] == [1, 1]:
                tens_c = tens_a.stack_link(tens_b, 2)
            elif idx == self.num_sites - 1 and [tens_a.shape[2], tens_b.shape[2]] == [
                1,
                1,
            ]:
                tens_c = tens_a.stack_link(tens_b, 0)
            else:
                tens_c = tens_a.stack_first_and_last_link(tens_b)

            tensor_list.append(tens_c)
            idx += 1

        addMPS = MPS.from_tensor_list(tensor_list, conv_params=convergence_params)

        return addMPS

    def __iadd__(self, other):
        """Concatenate the MPS other with self inplace"""
        addMPS = self.__add__(other)

        return addMPS

    def __mul__(self, factor):
        """Multiply the mps by a scalar and return the new MPS"""
        if not np.isscalar(factor):
            raise TypeError("Multiplication is only defined with a scalar number")

        other = deepcopy(self)
        if other.iso_center is None:
            other.right_canonize(
                max(0, self.first_non_orthogonal_left), keep_singvals=True
            )
        other._tensors[self.iso_center] *= factor

        return other

    def __imul__(self, factor):
        """Multiply the mps by a scalar in place"""
        if not np.isscalar(factor):
            raise TypeError("Multiplication is only defined with a scalar number")
        mult_mps = self.__mul__(factor)

        return mult_mps

    def __truediv__(self, factor):
        """Divide the mps by a scalar and return the new MPS"""
        if not np.isscalar(factor):
            raise TypeError("Multiplication is only defined with a scalar number")

        other = deepcopy(self)
        if other.iso_center is None:
            other.right_canonize(
                max(0, self.first_non_orthogonal_left), keep_singvals=True
            )
        other._tensors[self.iso_center] /= factor
        return other

    def __itruediv__(self, factor):
        """Divide the mps by a scalar in place"""
        if not np.isscalar(factor):
            raise TypeError("Multiplication is only defined with a scalar number")
        div_mps = self.__truediv__(factor)

        return div_mps

    def __matmul__(self, other):
        """
        Implement the contraction between two MPSs overloading the operator
        @. It is equivalent to doing <self|other>. It already takes into account
        the conjugation of the left-term
        """
        if not isinstance(other, MPS):
            raise TypeError("Only two MPS classes can be contracted")

        return other.contract(self)

    def dot(self, other):
        """
        Calculate the dot-product or overlap between two MPSs, i.e.,
        <self | other>.

        Parameters
        ----------

        other : :class:`MPS`
            Measure the overlap with this other MPS.

        Returns
        -------a

        Scalar representing the overlap.
        """
        return other.contract(self)

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @classmethod
    def from_statevector(
        cls,
        statevector,
        local_dim=2,
        conv_params=None,
        tensor_backend=None,
    ):
        """
        Initialize the MPS tensors by decomposing a statevector into MPS form.
        All the degrees of freedom must have the same local dimension

        Parameters
        ----------
        statevector : ndarray of shape( local_dim^num_sites, )
            Statevector describing the interested state for initializing the MPS
        local_dim : int, optional
            Local dimension of the degrees of freedom. Default to 2.
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters for the new MPS. If None, the maximum bond
            bond dimension possible is assumed, and a cut_ratio=1e-9.
            Default to None.
        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Returns
        -------
        obj : :py:class:`MPS`
            MPS simulator class

        Examples
        --------
        >>> -U1 - U2 - U3 - ... - UN-
        >>>  |    |    |          |
        # For d=2, N=7 and chi=5, the tensor network is as follows:
        >>> -U1 -2- U2 -4- U3 -5- U4 -5- U5 -4- U6 -2- U7-
        >>>  |      |      |      |      |      |      |
        # where -x- denotes the bounds' dimension (all the "bottom-facing" indices
        # are of dimension d=2). Thus, the shapes
        # of the returned tensors are as follows:
        >>>      U1         U2         U3         U4         U5         U6         U7
        >>> [(1, 2, 2), (2, 2, 4), (4, 2, 5), (5, 2, 5), (5, 2, 4), (4, 2, 2), (2, 2, 1)]
        """
        if not isinstance(statevector, np.ndarray):
            raise TypeError("Statevector must be numpy array")
        else:
            statevector = statevector.reshape(-1)
        num_sites = int(np.log(len(statevector)) / np.log(local_dim))

        max_bond_dim = local_dim ** (num_sites // 2)
        if conv_params is None:
            conv_params = TNConvergenceParameters(max_bond_dimension=int(max_bond_dim))
        obj = cls(num_sites, conv_params, local_dim, tensor_backend=tensor_backend)

        state_tensor = statevector.reshape([1] + [local_dim] * num_sites + [1])
        tensor_cls = obj._tensor_backend.tensor_cls
        state_tensor = tensor_cls.from_elem_array(state_tensor)
        for ii in range(num_sites - 1):
            legs = list(range(len(state_tensor.shape)))
            tens_left, tens_right, singvals, _ = state_tensor.split_svd(
                legs[:2], legs[2:], contract_singvals="R", conv_params=conv_params
            )

            obj._tensors[ii] = tens_left
            obj._singvals[ii + 1] = singvals
            state_tensor = tens_right
        obj._tensors[-1] = tens_right

        # After this procedure the state is in left canonical form
        obj._first_non_orthogonal_left = obj.num_sites - 1
        obj._first_non_orthogonal_right = obj.num_sites - 1

        obj.convert(obj._tensor_backend.dtype, obj._tensor_backend.device)

        return obj

    def _initialize_mps(self, initialize):
        """
        Initialize the MPS with a given structure. Available are:
        - "vacuum", initializes the MPS in |00...0>
        - "random", initializes the MPS in a random state at fixed bond dimension

        Parameters
        ----------
        initialize : str
            Type of initialization.

        Returns
        -------
        None
        """
        kwargs = self._tensor_backend.tensor_cls_kwargs()
        tensor_cls = self._tensor_backend.tensor_cls

        if initialize.lower() == "vacuum":
            for ii in range(self.num_sites):
                state0 = tensor_cls(
                    [1, self._local_dim[ii], 1], ctrl="ground", **kwargs
                )
                self._tensors.append(state0)
            self._singvals = [
                np.ones(1, dtype=np.double) for _ in range(self.num_sites + 1)
            ]
        elif initialize.lower() == "random":
            # Works only for qubits right now
            chi_ini = self._convergence_parameters.ini_bond_dimension
            chis = [1] + [chi_ini] * (self.num_sites - 1) + [1]

            chi_tmp = 1
            for ii in range(self.num_sites):
                chi_tmp *= self._local_dim[ii]
                if chi_tmp < chis[ii + 1]:
                    chis[ii + 1] = chi_tmp
                    chis[-ii - 2] = chi_tmp
                else:
                    break

            for ii in range(self.num_sites):
                bd_left = chis[ii]
                bd_right = chis[ii + 1]

                mat = np.random.rand(bd_left, self._local_dim[ii], bd_right)

                self._tensors.append(
                    tensor_cls.from_elem_array(
                        mat,
                        kwargs.get("dtype", np.double),
                        kwargs.get("device", "cpu"),
                    )
                )

            self.site_canonize(self.num_sites - 1, normalize=True)
            self.normalize()

    def to_dense(self, true_copy=False):
        """
        Return MPS without symmetric tensors.

        Parameters
        ----------

        true_copy : bool, optional
            The function can be forced to return an actual copy with
            `true_copy=True`, while otherwise `self` can be returned
            if the MPS is already without symmetries.
            Default to `False`

        Returns
        -------

        dense_mps : :class:`MPS`
            MPS representation without symmetric tensors.
        """
        if self.has_symmetry:
            # Have to convert
            tensor_list = [elem.to_dense() for elem in self]

            obj = self.from_tensor_list(
                tensor_list,
                conv_params=self.convergence_parameters,
                tensor_backend=self._tensor_backend,
            )

            for ii, s_vals in enumerate(self.singvals):
                # Tensor list is shorter, still choose tensor belonging to singvals.
                jj = min(ii, len(self) - 1)
                obj._singvals[ii] = self[jj].to_dense_singvals(
                    s_vals, true_copy=true_copy
                )

            obj.iso_center = self.iso_center

            return obj

        # Cases without symmetry

        if true_copy:
            return self.copy()

        return self

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    #                     Abstract methods to be implemented
    # --------------------------------------------------------------------------

    def _convert_singvals(self, dtype, device):
        """Convert the singular values of the tensor network to dtype/device."""
        if len(self) == 0:
            return

        # Take any example tensor
        tensor = self[0]

        singvals_list = []
        for elem in self._singvals:
            if elem is None:
                singvals_list.append(None)
            else:
                singvals_ii = tensor.convert_singvals(elem, dtype, device)
                singvals_list.append(singvals_ii)

        self._singvals = singvals_list

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
        if pos_src < pos_dst:
            return list(range(pos_src + 1)), list(range(pos_src + 1, self.num_sites))

        # pos_src > pos_dst
        return list(range(pos_dst + 1, self.num_sites)), list(range(pos_dst + 1))

    def get_pos_links(self, pos):
        """
        List of tensor position where links are leading to.

        Parameters
        ----------
        pos : int
            Index of the tensor in the MPS

        Returns
        -------
        Tuple[int]
            Index of the tensor connected through links to pos.
            None if they are open links.
        """
        return [
            pos - 1 if pos > 0 else None,
            -pos - 2,
            pos + 1 if pos < self.num_sites - 1 else None,
        ]

    def get_rho_i(self, idx):
        """
        Get the reduced density matrix of the site at index idx

        Parameters
        ----------
        idx : int
            Index of the site

        Returns
        -------
        :class:`_AbstractQteaTensor`
            Reduced density matrix of the site
        """
        if self.iso_center is None:
            self.iso_towards(idx, keep_singvals=True)

        s_idx = 1 if self.iso_center > idx else 0
        if self.singvals[idx + s_idx] is None:
            self.iso_towards(idx, keep_singvals=True)
            tensor = self[idx]
        else:
            tensor = self[idx]
            if self.iso_center > idx:
                tensor = tensor.scale_link(self.singvals[idx + s_idx], 2)
            elif self.iso_center < idx:
                tensor = tensor.scale_link(self.singvals[idx + s_idx], 0)

        rho = tensor.tensordot(tensor.conj(), [[0, 2], [0, 2]])

        trace = rho.trace(return_real_part=True, do_get=True)
        if abs(1 - trace) > 10 * rho.dtype_eps:
            warn("Renormalizing reduced density matrix.")
            rho /= trace

        return rho

    def get_tensor_of_site(self, idx):
        """
        Generic function to retrieve the tensor for a specific site. Compatible
        across different tensor network geometries. This function does not
        shift the gauge center before returning the tensor.

        Parameters
        ----------
        idx : int
            Return tensor containin the link of the local
            Hilbert space of the idx-th site.
        """
        return self[idx]

    # pylint: disable-next=arguments-differ
    def iso_towards(
        self,
        new_iso,
        keep_singvals=False,
        trunc=False,
        conv_params=None,
        normalize=False,
    ):
        """
        Apply the gauge transformation to shift the isometry
        center to a specific site `new_iso`.
        The method might be different for
        other TN structure, but for the MPS it is the same.

        Parameters
        ----------
        new_iso : int
            Position in the TN of the tensor which should be isometrized.
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
        normalize : bool, optional
            Flag if intermediate steps should normalize.
            Default to `False`
        """

        self.left_canonize(
            new_iso,
            trunc=trunc,
            keep_singvals=keep_singvals,
            conv_params=conv_params,
            normalize=normalize,
        )
        self.right_canonize(
            new_iso,
            trunc=trunc,
            keep_singvals=keep_singvals,
            conv_params=conv_params,
            normalize=normalize,
        )

    def _iter_tensors(self):
        """Iterate over all tensors forming the tensor network (for convert etc)."""
        for elem in self._tensors:
            yield elem

    def norm(self):
        """
        Returns the norm of the MPS as sqrt(<self|self>)

        Return
        ------
        norm: float
            norm of the MPS
        """
        idx = self.first_non_orthogonal_right

        if self.first_non_orthogonal_left != self.first_non_orthogonal_right:
            self.left_canonize(self.first_non_orthogonal_right, keep_singvals=True)

        return self[idx].norm_sqrt()

    def scale(self, factor):
        """
        Scale the MPS state by a scalar constant using the gauge center.

        Parameters
        ----------

        factor : scalar
             Factor is multiplied to the MPS at the gauge center.
        """
        self._tensors[self.iso_center] *= factor

    def set_singvals_on_link(self, pos_a, pos_b, s_vals):
        """Update or set singvals on link via two positions."""
        if pos_a < pos_b:
            self._singvals[pos_b] = s_vals
        else:
            self._singvals[pos_a] = s_vals

    # pylint: disable-next=arguments-differ
    def site_canonize(self, idx, keep_singvals=False, normalize=False):
        """
        Apply the gauge transformation to shift the isoemtry
        center to a specific site `idx`.

        Parameters
        ----------
        idx: int
            index of the tensor up to which the canonization
            occurs from the left and right side.
        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.
        normalize : bool, optional
            Flag if intermediate steps should normalize.
            Default to `False`
        """
        self.iso_towards(idx, keep_singvals=keep_singvals, normalize=normalize)

    # --------------------------------------------------------------------------
    #                   Choose to overwrite instead of inheriting
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    #                                  Unsorted
    # --------------------------------------------------------------------------

    def _iter_all_links(self, pos):
        """
        Iterate through all the links of
        a given position of the MPS

        Parameters
        ----------
        pos : int
            Index of the tensor

        Yields
        ------
        int
            Index of the tensor. The order is
            left-physical-right
        """
        yield pos - 1, 2
        yield -pos - 2, 1
        yield pos + 1, 0

    def _iter_physical_links(self):
        """
        Gives an iterator through the physical links.
        In the MPS, the physical links are connected to nothing,
        i.e. we assign the tensor index -2

        Return
        ------
        Tuple[int]
            The identifier from_tensor, to_tensor
        """
        for pos in range(self.num_sites):
            yield -pos - 2, pos

    def right_canonize(
        self, idx, trunc=False, keep_singvals=False, conv_params=None, normalize=False
    ):
        """
        Apply a gauge transformation to all bonds between
        :py:method:`MPS.num_sites` and `idx`, so that all
        sites between the last (rightmost one) and idx
        are set to (semi)-unitary tensors.

        Parameters
        ----------
        idx: int
            index of the tensor up to which the canonization occurs
        trunc: bool, optional
            If True, use the SVD instead of the QR for the canonization.
            It might be useful to reduce the bond dimension. Default to False.
        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`.
        normalize : bool, optional
            Flag if intermediate steps should normalize.
            Default to `False`
        """
        # Get functions for elemtary arrays
        mysum, sqrt = self[0].get_attr("sum", "sqrt")

        do_svd = self._requires_singvals or trunc

        if idx > self.num_sites - 1 or idx < 0:
            raise ValueError(
                "The canonization index must be between the "
                + "number of sites-1 and 0"
            )
        if conv_params is None:
            conv_params = self._convergence_parameters

        for ii in range(self.first_non_orthogonal_right, idx, -1):
            if do_svd:
                rr_mat, tensor, singvals, _ = self[ii].split_svd(
                    [0],
                    [1, 2],
                    contract_singvals="L",
                    conv_params=conv_params,
                    no_truncation=not trunc,
                )
                if normalize:
                    norm = sqrt(mysum(singvals**2))
                    singvals /= norm
                    rr_mat /= norm

                self._singvals[ii] = singvals
            else:
                tensor, rr_mat = self[ii].split_qr(
                    [1, 2], [0], perm_left=[2, 0, 1], perm_right=[1, 0]
                )

                if normalize:
                    norm = rr_mat.norm()
                    rr_mat /= norm

                if not keep_singvals:
                    self._singvals[ii] = None
            # Update the tensors in the MPS
            self._tensors[ii] = tensor
            self._tensors[ii - 1] = self[ii - 1].tensordot(rr_mat, ([2], [0]))
            if self.eff_op is not None:
                self._update_eff_ops([ii, ii - 1])

        self._first_non_orthogonal_left = min(self.first_non_orthogonal_left, idx)
        self._first_non_orthogonal_right = idx

    def left_canonize(
        self, idx, trunc=False, keep_singvals=False, conv_params=None, normalize=False
    ):
        """
        Apply a gauge transformation to all bonds between 0 and `idx`,
        so that all sites between the first (òeftmpst one) and idx
        are set to (semi)-unitary tensors.

        Parameters
        ----------
        idx: int
            index of the tensor up to which the canonization occurs
        trunc: bool, optional
            If True, use the SVD instead of the QR for the canonization.
            It might be useful to reduce the bond dimension. Default to False.
        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`.
        normalize : bool, optional
            Flag if singular values should be normalized.
            Default to `False`
        """
        # Get functions for elemtary arrays
        mysum, sqrt = self[0].get_attr("sum", "sqrt")

        do_svd = self._requires_singvals or trunc

        if idx > self.num_sites - 1 or idx < 0:
            raise ValueError(
                "The canonization index must be between the "
                + "number of sites-1 and 0"
            )
        if conv_params is None:
            conv_params = self._convergence_parameters

        for ii in range(self.first_non_orthogonal_left, idx):
            tensor = self[ii]
            if do_svd:
                tensor, rr_mat, singvals, _ = self[ii].split_svd(
                    [0, 1],
                    [2],
                    contract_singvals="R",
                    conv_params=conv_params,
                    no_truncation=not trunc,
                )
                if normalize:
                    norm = sqrt(mysum(singvals**2))
                    singvals /= norm
                    rr_mat /= norm

                self._singvals[ii + 1] = singvals
            else:
                tensor, rr_mat = self[ii].split_qr([0, 1], [2])

                if normalize:
                    norm = rr_mat.norm()
                    rr_mat /= norm

                if not keep_singvals:
                    self._singvals[ii + 1] = None

            # Update the tensors in the MPS
            self._tensors[ii] = tensor
            self._tensors[ii + 1] = self[ii + 1].tensordot(rr_mat, ([0], [1]))
            self._tensors[ii + 1] = self._tensors[ii + 1].transpose([2, 0, 1])
            if self.eff_op is not None:
                self._update_eff_ops([ii, ii + 1])
        self._first_non_orthogonal_left = idx
        self._first_non_orthogonal_right = max(self.first_non_orthogonal_right, idx)

    def normalize(self):
        """
        Normalize the MPS state, by dividing by :math:`\\sqrt{<\\psi|\\psi>}`.
        """
        # Compute the norm. Internally, it set the gauge center
        norm = self.norm()
        # Update the norm
        self._tensors[self.iso_center] /= norm

    def modify_local_dim(self, value, idxs=None):
        """
        Modify the local dimension of sites `idxs` to the value `value`.
        By default modify the local dimension of all the sites. If `value` is
        a vector then it must have the same length of `idxs`.
        Notice that there may be loss of information, it is up to the
        user to be sure no error is done in this procedure.

        Parameters
        ----------
        value : int or array-like
            New value of the local dimension. If an int, it is assumed
            it will be the same for all sites idxs, otherwise its length
            must be the same of idxs.
        idxs : int or array-like, optional
            Indexes of the sites to modify. If None, all the sites are
            modified. Default to None.
        """
        # Transform scalar arguments in vectors
        if np.isscalar(value) and idxs is None:
            value = np.repeat(value, self.num_sites).astype(int)
        if idxs is None:
            idxs = np.arange(self.num_sites)
        elif np.isscalar(idxs) and np.isscalar(value):
            idxs = np.array([idxs])
            value = np.array([value])
        # Checks on parameters
        if np.any(idxs > self.num_sites - 1) or np.any(idxs < 0):
            raise ValueError(
                "The index idx must be between the " + "number of sites-1 and 0"
            )
        elif np.min(value) < 2:
            raise ValueError(
                f"The local dimension must be at least 2, not {min(value)}"
            )
        elif len(value) != len(idxs):
            raise ValueError(
                "value and idxs must have the same length, but "
                + f"{len(value)} != {len(idxs)}"
            )

        # Quick return
        if len(idxs) == 0:
            return
        # Sort arguments to avoid moving the gauge back and forth
        value = value[np.argsort(idxs)]
        idxs = np.sort(idxs)

        for ii, idx in enumerate(idxs):
            initial_local_dim = self.local_dim[idx]
            new_local_dim = value[ii]

            if initial_local_dim == new_local_dim:
                # Already right dimension
                continue

            self.site_canonize(idx, keep_singvals=True)
            initial_norm = self.norm()

            if new_local_dim < initial_local_dim:
                # Get subtensor along link
                res = self[idx].subtensor_along_link(1, 0, new_local_dim)
            else:
                shape = [
                    self[idx].shape[0],
                    new_local_dim - initial_local_dim,
                    self[idx].shape[2],
                ]
                kwargs = self._tensor_backend.tensor_cls_kwargs()

                # Will fail for symmetric tensors
                pad = self._tensor_backend.tensor_cls(shape, **kwargs)

                res = self[idx].stack_link(pad, 1)

            self._tensors[idx] = res

            final_norm = self.norm()
            self._tensors[self.iso_center] *= initial_norm / final_norm

            self._local_dim[idx] = new_local_dim

    def add_site(self, idx, state=None):
        """
        Add a site in a product state in the link idx
        (idx=0 is before the first site, idx=N+1 is after the last).
        The state of the new index is |0> or the one provided.

        Parameters
        ----------
        idx : int
            index of the link where you want to add the site
        state: None or array-like
            Vector state that you want to add

        Details
        -------
        To insert a new site in the MPS we first insert an identity on a link,
        then add a dimension-1 link to the identity and lastly contract the
        new link with the initial state, usually a |0>
        """
        if idx < 0 or idx > self.num_sites:
            raise ValueError(f"idx must be between 0 and N+1, not {idx}")
        if state is None:
            local_dim = int(np.min(self.local_dim))
            kwargs = self._tensor_backend.tensor_cls_kwargs()
            state = self._tensor_backend.tensor_cls(
                [1, local_dim, 1], ctrl="ground", **kwargs
            )

        old_norm = self.norm()

        # Insert an identity on link idx
        if idx == 0:
            id_dim = self[0].shape[0]
        else:
            id_dim = self[idx - 1].shape[2]

        identity = state.eye_like(id_dim)
        identity.reshape_update([id_dim, 1, id_dim])

        # Contract the identity with the desired state of the new tensor
        state = state.reshape([np.prod(state.shape), 1])
        new_site = identity.tensordot(state, ([1], [1]))
        new_site = new_site.transpose([0, 2, 1])

        # Insert it in the data structure
        self._tensors.insert(idx, new_site)
        self._local_dim = np.insert(self._local_dim, idx, new_site.shape[1])
        self._num_sites += 1
        self._singvals.insert(idx + 1, None)

        # Update the gauge center if we didn't add the site at the end of the chain
        if idx < self.num_sites - 1 and idx < self.iso_center:
            self._first_non_orthogonal_right += 1
            self._first_non_orthogonal_left += 1

        # Renormalize
        new_norm = self.norm()

        self._tensors[self.iso_center] *= old_norm / new_norm

    def to_statevector(self, qiskit_order=False, max_qubit_equivalent=20):
        """
        Given a list of N tensors *MPS* [U1, U2, ..., UN] , representing
        a Matrix Product State, perform the contraction in the Examples,
        leading to a single tensor of order N, representing a dense state.

        The index ordering convention is from left-to-right.
        For instance, the "left" index of U2 is the first, the "bottom" one
        is the second, and the "right" one is the third.

        Parameters
        ----------
        qiskit_order: bool, optional
            weather to use qiskit ordering or the theoretical one. For
            example the state |011> has 0 in the first position for the
            theoretical ordering, while for qiskit ordering it is on the
            last position.
        max_qubit_equivalent: int, optional
            Maximum number of qubit sites the MPS can have and still be
            transformed into a statevector.
            If the number of sites is greater, it will throw an exception.
            Default to 20.

        Returns
        -------
        psi : ndarray of shape (d ^ N, )
            N-order tensor representing the dense state.

        Examples
        --------
        >>> U1 - U2 - ... - UN
        >>>  |    |          |
        """
        if np.prod(self.local_dim) > 2**max_qubit_equivalent:
            raise RuntimeError(
                "Maximum number of sites for the statevector is "
                + f"fixed to the equivalent of {max_qubit_equivalent} qubit sites"
            )
        psi = self[0]
        for tensor in self[1:]:
            psi = psi.tensordot(tensor, ([-1], [0]))

        if qiskit_order:
            order = "F"
        else:
            order = "C"

        return psi.reshape(np.prod(self.local_dim), order=order)

    def to_tensor_list(self):
        """
        Return the tensor list representation of the MPS.
        Required for compatibility with TTN emulator

        Return
        ------
        list
            List of tensors of the MPS
        """
        return self.tensors

    def to_ttn(self):
        """
        Return a tree tensor network (TTN) representation as binary tree.

        Details
        -------

        The TTN is returned as a listed list where the tree layer with the
        local Hilbert space is the first list entry and the uppermost layer in the TTN
        is the last list entry. The first list will have num_sites / 2 entries. The
        uppermost list has two entries.

        The order of the legs is always left-child, right-child, parent with
        the exception of the left top tensor. The left top tensor has an
        additional link, i.e., the symmetry selector; the order is left-child,
        right-child, parent, symmetry-selector.

        Also see :py:func:ttn_simulator:`from_tensor_list`.
        """
        nn = len(self)
        if abs(np.log2(nn) - int(np.log2(nn))) > 1e-15:
            raise Exception(
                "A conversion to a binary tree requires 2**n "
                "sites; but having %d sites." % (nn)
            )

        if nn == 4:
            # Special case: iterations will not work
            left_tensor = self[0].tensordot(self[1], [[2], [0]])
            right_tensor = self[2].tensordot(self[3], [[2], [0]])

            # Use left link of dimension 1 as symmetry selector
            left_tensor.transpose_update([1, 2, 3, 0])

            # Eliminate one link
            right_tensor.reshape_update(right_tensor.shape[:-1])

            return [[left_tensor, right_tensor]]

        # Initial iteration
        theta_list = []
        for ii in range(nn // 2):
            ii1 = 2 * ii
            ii2 = ii1 + 1

            theta_list.append(self[ii1].tensordot(self[ii2], [[2], [0]]))

        child_list = []
        parent_list = []
        for ii, theta in enumerate(theta_list):
            qmat, rmat = theta.split_qr([1, 2], [0, 3], perm_right=[1, 0, 2])

            child_list.append(qmat)
            parent_list.append(rmat)

        layer_list = [child_list]
        while len(parent_list) > 4:
            theta_list = []
            for ii in range(len(parent_list) // 2):
                ii1 = 2 * ii
                ii2 = ii1 + 1

                theta_list.append(
                    parent_list[ii1].tensordot(parent_list[ii2], [[2], [0]])
                )

            child_list = []
            parent_list = []
            for ii, theta in enumerate(theta_list):
                qmat, rmat = theta.split_qr([1, 2], [0, 3], perm_right=[1, 0, 2])

                child_list.append(qmat)
                parent_list.append(rmat)

            layer_list.append(child_list)

        # Last iteration
        left_tensor = parent_list[0].tensordot(parent_list[1], [[2], [0]])
        right_tensor = parent_list[2].tensordot(parent_list[3], [[2], [0]])

        # The fourth-link is the symmetry selector, i.e., for tensor
        # networks without symmetries a link of dimension one. The link
        # to the left of the MPS fulfills this purpose
        left_tensor.transpose_update([1, 2, 3, 0])

        right_tensor.reshape_update(right_tensor.shape[:-1])
        right_tensor.transpose_update([1, 2, 0])

        layer_list.append([left_tensor, right_tensor])

        return layer_list

    @classmethod
    def from_tensor_list(
        cls,
        tensor_list,
        conv_params=None,
        tensor_backend=None,
    ):
        """
        Initialize the MPS tensors using a list of correctly shaped tensors

        Parameters
        ----------
        tensor_list : list of ndarrays or cupy arrays
            List of tensor for initializing the MPS
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters for the new MPS. If None, the maximum bond
            bond dimension possible is assumed, and a cut_ratio=1e-9.
            Default to None.
        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Returns
        -------
        obj : :py:class:`MPS`
            The MPS class
        """
        local_dim = []
        max_bond_dim = 2
        for ii, tens in enumerate(tensor_list):
            t_shape = tens.shape
            local_dim.append(t_shape[1])
            max_bond_dim = max(max_bond_dim, t_shape[0])
            if ii > 0 and t_shape[0] != tensor_list[ii - 1].shape[2]:
                raise ValueError(
                    f"Dimension mismatch of the left leg of tensor {ii} and "
                    + f"the right leg of tensor {ii-1}: "
                    + f"{t_shape[0]} vs {tensor_list[ii - 1].shape[2]}"
                )

        if conv_params is None:
            conv_params = TNConvergenceParameters(max_bond_dimension=int(max_bond_dim))
        obj = cls(
            len(tensor_list), conv_params, local_dim, tensor_backend=tensor_backend
        )

        qtea_tensor_list = []
        for elem in tensor_list:
            if not isinstance(elem, _AbstractQteaTensor):
                qtea_tensor_list.append(
                    obj._tensor_backend.tensor_cls.from_elem_array(elem)
                )
            else:
                qtea_tensor_list.append(elem)

        obj._tensors = qtea_tensor_list

        obj.convert(obj._tensor_backend.dtype, obj._tensor_backend.device)

        return obj

    def apply_one_site_operator(self, op, pos):
        """
        Applies a one operator `op` to the site `pos` of the MPS.

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

        res = self[pos].tensordot(op, ([1], [1]))
        self._tensors[pos] = res.transpose([0, 2, 1])

    def apply_two_site_operator(self, op, pos, swap=False, svd=True, parallel=False):
        """
        Applies a two-site operator `op` to the site `pos`, `pos+1` of the MPS.

        Parameters
        ----------
        op: numpy array shape (local_dim, local_dim, local_dim, local_dim)
            Matrix representation of the quantum gate
        pos: int or list of ints
            Position of the qubit where to apply `op`. If a list is passed,
            the two sites should be adjacent. The first index is assumed to
            be the control, and the second the target. The swap argument is
            overwritten if a list is passed.
        swap: bool
            If True swaps the operator. This means that instead of the
            first contraction in the following we get the second.
            It is written is a list of pos is passed.
        svd: bool
            If True, apply the usual contraction plus an SVD, otherwise use the
            QR approach explained in https://arxiv.org/pdf/2212.09782.pdf.
        parallel: bool
            If True, perform an approximation of the two-qubit gates faking
            the isometry center

        Returns
        -------
        singular_values_cutted: ndarray
            Array of singular values cutted, normalized to the biggest singular value

        Examples
        --------

        .. code-block::

            swap=False  swap=True
              -P-M-       -P-M-
              2| |2       2| |2
              3| |4       4| |3
               GGG         GGG
              1| |2       2| |1
        """
        if not np.isscalar(pos) and len(pos) == 2:
            if max(pos[0], pos[1]) - min(pos[0], pos[1]) > 1:
                warn("Using non-local gates. Errors might increase.")
                return self.apply_nonlocal_two_site_operator(op, pos[0], pos[1], swap)
            pos = min(pos[0], pos[1])
        elif not np.isscalar(pos):
            raise ValueError(
                f"pos should be only scalar or len 2 array-like, not len {len(pos)}"
            )

        if pos < 0 or pos > self.num_sites - 1:
            raise ValueError(
                "The position of the site must be between 0 and (num_sites-1)"
            )
        op = op.reshape([self._local_dim[pos], self._local_dim[pos + 1]] * 2)

        if swap:
            op = op.transpose([1, 0, 3, 2])

        if parallel:
            self[pos].scale_link_update(self.singvals[pos], 0)
            contract_singvals = "L"
        else:
            # Set orthogonality center
            self.site_canonize(pos, keep_singvals=True)
            contract_singvals = "R"

        # Perform SVD
        if svd:
            # Contract the two qubits
            twoqubit = self[pos].tensordot(self[pos + 1], ([2], [0]))

            # Contract with the gate
            twoqubit = twoqubit.tensordot(op, ([1, 2], [2, 3]))
            twoqubit.transpose_update([0, 2, 3, 1])
            tens_left, tens_right, singvals, singvals_cutted = twoqubit.split_svd(
                [0, 1],
                [2, 3],
                contract_singvals=contract_singvals,
                conv_params=self._convergence_parameters,
            )
        else:
            tens_left, tens_right, singvals, singvals_cutted = self[pos].split_qrte(
                self[pos + 1],
                self.singvals[pos],
                op,
                conv_params=self._convergence_parameters,
            )

        # Update state
        self._tensors[pos] = tens_left
        self._tensors[pos + 1] = tens_right
        self._singvals[pos + 1] = singvals

        if parallel:
            self[pos].scale_link_update(1 / self.singvals[pos], 0)

        else:
            self._first_non_orthogonal_left = pos + 1
            self._first_non_orthogonal_right = pos + 1

        # Update maximum bond dimension reached
        if self[pos].shape[2] > self.max_bond_dim_reached:
            self.max_bond_dim_reached = self[pos].shape[2]

        return singvals_cutted

    def swap_qubits(self, sites, conv_params=None, trunc=True):
        """
        This function applies a swap gate to sites in an MPS,
        i.e. swaps these two qubits

        Parameters
        ----------
        sites : Tuple[int]
            The qubits on site sites[0] and sites[1] are swapped
        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters to use for the SVD in the procedure.
            If `None`, convergence parameters are taken from the TTN.
            Default to `None`.

        Return
        ------
        np.ndarray
            Singualr values cut in the process of shifting the isometry center.
            None if moved through the QR.
        """
        if conv_params is None:
            conv_params = self._convergence_parameters
        # transform input into np array just in case the
        # user passes the list
        sites = np.sort(sites)
        singvals_cut_tot = []
        self.iso_towards(sites[0], True, False, conv_params)
        # Move sites[0] in sites[1] position
        for pos in range(sites[0], sites[1]):
            # Contract the two sites
            two_sites = self[pos].tensordot(self[pos + 1], ([2], [0]))
            # Swap the qubits
            two_sites.transpose_update([0, 2, 1, 3])
            if trunc:
                left, right, singvals, singvals_cut = two_sites.split_svd(
                    [0, 1], [2, 3], contract_singvals="R", conv_params=conv_params
                )
                self._singvals[pos + 1] = singvals
                singvals_cut_tot.append(singvals_cut)
            else:
                left, right = two_sites.split_qr([0, 1], [2, 3])

            # Update tensor and iso center
            self._tensors[pos] = left
            self._tensors[pos + 1] = right
            self._first_non_orthogonal_left += 1
            self._first_non_orthogonal_right += 1

        self.iso_towards(sites[1] - 1, True, False, conv_params)
        # Move sites[1] in sites[0] position
        for pos in range(sites[1] - 1, sites[0], -1):
            # Contract the two sites
            two_sites = self[pos - 1].tensordot(self[pos], ([2], [0]))
            # Swap the qubits
            two_sites.transpose_update([0, 2, 1, 3])
            if trunc:
                left, right, singvals, singvals_cut = two_sites.split_svd(
                    [0, 1], [2, 3], contract_singvals="L", conv_params=conv_params
                )
                self._singvals[pos] = singvals
                singvals_cut_tot.append(singvals_cut)
            else:
                right, left = two_sites.split_qr(
                    [2, 3], [0, 1], perm_left=[2, 0, 1], perm_right=[1, 2, 0]
                )

            # Update tensor and iso center
            self._tensors[pos - 1] = left
            self._tensors[pos] = right
            self._first_non_orthogonal_left -= 1
            self._first_non_orthogonal_right -= 1

        return singvals_cut_tot

    def apply_projective_operator(self, site, selected_output=None, remove=False):
        """
        Apply a projective operator to the site **site**, and give the measurement as output.
        You can also decide to select a given output for the measurement, if the probability is
        non-zero. Finally, you have the possibility of removing the site after the measurement.

        .. warning::

            Applying projective measurements/removing sites is ALWAYS dangerous. The information
            of the projective measurement should be in principle carried over the entire mps,
            by iteratively applying SVDs across all sites. However, this procedure is highly
            suboptimal, since it is not always necessary and will be processed by the
            following two-sites operators. Thus, the procedure IS NOT applied here. Take care
            that entanglement measures through :class:`TNObsBondEntropy` may give incorrect
            results right after a projective operator application. Furthermore, if working
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

        # Set the orthogonality center
        self.site_canonize(site, keep_singvals=True)

        # Normalize
        old_norm = self.norm()
        self._tensors[site] = self._tensors[site] / old_norm

        # Measure
        random_u = np.random.rand()
        rho_i = self.get_rho_i(site)

        probabilities = rho_i.diag(real_part_only=True, do_get=True)
        cumul_probs = np.cumsum(probabilities)

        meas_state = None
        for ii, cprob_ii in enumerate(cumul_probs):
            if selected_output is not None and ii != selected_output:
                continue

            if cprob_ii >= random_u or selected_output == ii:
                meas_state = ii
                state_prob = probabilities[ii]
                break

        if meas_state is None:
            raise Exception("Did not run into measurement.")

        # Renormalize and come back to previous norm
        if remove:
            ii = meas_state
            tens_to_remove = self._tensors[site].subtensor_along_link(1, ii, ii + 1)
            tens_to_remove.remove_dummy_link(1)

            if site < self.num_sites - 1:
                # contract the measured tensor in the next tensor
                self._tensors[site + 1] = tens_to_remove.tensordot(
                    self[site + 1], ([1], [0])
                )
            else:
                self._tensors[site - 1] = self[site - 1].tensordot(
                    tens_to_remove, ([2], [0])
                )

            self._tensors.pop(site)
            self._singvals.pop(site)
            self._local_dim = np.delete(self._local_dim, site)
            self._num_sites -= 1
            site = min(site, self._num_sites - 1)
            self._first_non_orthogonal_left = site
            self._first_non_orthogonal_right = site
        else:
            projector = _projector_for_rho_i(meas_state, rho_i)
            self.apply_one_site_operator(projector, site)

        # Renormalize
        self._tensors[site] = self._tensors[site] / self.norm()
        self._tensors[site] = self._tensors[site] * old_norm

        # Set to None all the singvals
        self._singvals = [None for _ in self.singvals]

        return meas_state, state_prob

    def apply_nonlocal_two_site_operator(self, op, control, target, swap=False):
        """Apply a non-local two-site operator, by taking first the SVD of the operator,
        contracting the almost-single-site operator to the respective sites and then
        propagating the operator to the correct site

        .. warning::
            The operations in this method are NOT ALWAYS well defined. If the left-operator
            tensor is not unitary, then we are applying a non-unitary operation to the
            state, and thus we will see a vanishing norm. Notice that, if the error can
            happen a warning message will be printed

        Parameters
        ----------
        op : np.ndarray
            Operator to be applied
        control : int
            control qubit index
        target : int
            target qubit index
        swap : bool, optional
            If True, transpose the tensor legs such that the control and target
            are swapped. Default to False

        Returns
        -------
        np.ndarray
            Singular values cutted when the gate link is contracted
        """

        if min(control, target) < 0 or max(control, target) > self.num_sites - 1:
            raise ValueError(
                "The position of the site must be between 0 and (num_sites-1)"
            )
        elif list(op.shape) != [self._local_dim[control], self._local_dim[target]] * 2:
            raise ValueError(
                "Shape of the input operator must be (local_dim, "
                + "local_dim, local_dim, local_dim)"
            )
        if swap:
            op = op.transpose([1, 0, 3, 2])

        min_site = min(control, target)
        max_site = max(control, target)
        left_gate, right_gate, _, _ = op.split_svd(
            [0, 2],
            [1, 3],
            perm_left=[0, 2, 1],
            perm_right=[1, 0, 2],
            contract_singvals="L",
            no_truncation=True,
            conv_params=self._convergence_parameters,
        )

        test = right_gate.tensordot(right_gate.conj(), ([0, 1], [0, 1]))
        if not test.is_close_identity():
            warn(
                "Right-tensor is not unitary. Thus, the contraction is not optimal. We"
                " suggest"
                + " to linearize the circuit instead of using non-local operators",
                RuntimeWarning,
            )

        self.site_canonize(min_site, keep_singvals=True)
        self._tensors[min_site] = self[min_site].tensordot(
            left_gate / np.sqrt(2), ([1], [2])
        )

        self._tensors[min_site] = self._tensors[min_site].transpose([0, 2, 3, 1])

        for idx in range(min_site, max_site):
            double_site = self[idx].tensordot(self[idx + 1], ([3], [0]))
            (self._tensors[idx], self._tensors[idx + 1]) = double_site.split_qr(
                [0, 1], [2, 3, 4], perm_right=[0, 2, 1, 3]
            )

        self._tensors[max_site] = self[max_site].tensordot(
            right_gate * np.sqrt(2), ([1, 2], [2, 1])
        )
        self._tensors[max_site] = self._tensors[max_site].transpose([0, 2, 1])

        # double_site = np.tensordot(self[max_site-1], self[max_site], ([3, 2], [0, 2]) )
        # self._tensors[max_site-1], self._tensors[max_site], _, singvals_cut = \
        #        self.tSVD(double_site, [0, 1], [2, 3], contract_singvals='R' )

        self._first_non_orthogonal_left = max_site
        self._first_non_orthogonal_right = max_site
        self.iso_towards(min_site, keep_singvals=True, trunc=True)

        return []

    def apply_mpo(self, mpo):
        """
        Apply an MPO to the MPS on the sites `sites`.
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

        self.site_canonize(sites[0], keep_singvals=True)

        tot_singvals_cut = []
        # Operator index
        oidx = 0
        next_site = self[sites[0]].eye_like(self[sites[0]].shape[0])
        for sidx in range(sites[0], sites[-1] + 1):
            tens = self[sidx]
            if sidx in sites:
                # i -o- k
                #    |j     = T(i,k,l,m,n) -> T(i,l,m, k,n)
                # l -o- n
                #    |m
                tens = tens.tensordot(operators[oidx], ([1], [2]))
                tens.transpose_update((0, 2, 3, 1, 4))
                # T(i,l,m, k,n) -> T(il, m, kn)
                tens.reshape_update((np.prod(tens.shape[:2]), tens.shape[2], -1))

                # The matrix next, from the second cycle, is bringing the isometry center in tens
                # next = next.reshape(-1, tens.shape[0])
                # x -o- il -o- kn = x -o- kn
                #           |m         |m
                tens = next_site.tensordot(tens, ([1], [0]))
                oidx += 1

                if sidx + 1 in sites:
                    # Move the isometry when the next site has an MPO (and thus left-dimension kn)
                    # x -o- kn -->  x -o- y -o- kn
                    #    |m            |m
                    self._tensors[sidx], next_site, _, singvals_cut = tens.split_svd(
                        [0, 1],
                        [2],
                        contract_singvals="R",
                        conv_params=self._convergence_parameters,
                        no_truncation=True,
                    )

                    tot_singvals_cut += list(singvals_cut)
                elif sidx == sites[-1]:
                    # End of the procedure
                    self._tensors[sidx] = tens
                else:
                    # Move the isometry when the next site does not have an MPO
                    # x -o- kn -->  x -o- y -o- kn
                    #    |m
                    self._tensors[sidx], next_site = tens.split_qr([0, 1], [2])
                    #                n|
                    # y -o- kn --> y -o- k
                    # T(y,kn) -> T(y, k, n) -> T(y, n, k)
                    next_site.reshape_update(
                        (next_site.shape[0], -1, operators[oidx - 1].shape[3])
                    )
                    next_site.transpose_update((0, 2, 1))

            else:
                # Site does not have an operator, just bring the isometry here
                #   n|
                # y -o- i -o- k -> T(y, n, j, k) -> T(y, j, n, k)
                #          | j
                tens = next_site.tensordot(tens, ([2], [0]))
                tens.transpose_update((0, 2, 1, 3))

                if sidx + 1 in sites:
                    tens.reshape_update((tens.shape[0], tens.shape[1], -1))
                    self._tensors[sidx], next_site, _, singvals_cut = tens.split_svd(
                        [0, 1],
                        [2],
                        contract_singvals="R",
                        conv_params=self._convergence_parameters,
                        no_truncation=True,
                    )
                    tot_singvals_cut += list(singvals_cut)
                else:
                    #   n|                 |n
                    # y -o- k --> y -o- s -o- k
                    #    |j          |j
                    self._tensors[sidx], next_site = tens.split_qr([0, 1], [2, 3])

        self._first_non_orthogonal_left = sites[-1]
        self._first_non_orthogonal_right = sites[-1]
        self.iso_towards(sites[0], trunc=True, keep_singvals=True)

        return tot_singvals_cut

    def reset(self, idxs=None):
        """
        Reset the states of the sites idxs to the |0> state

        Parameters
        ----------
        idxs : int or list of ints, optional
            indexes of the sites to reinitialize to 0.
            If default value is left all the sites are restarted.
        """
        if idxs is None:
            idxs = np.arange(self.num_sites)
        elif np.isscalar(idxs):
            idxs = [idxs]
        else:
            idxs = np.array(idxs)
            idxs = np.sort(idxs)

        for idx in idxs:
            state, _ = self.apply_projective_operator(idx)
            if state != 0:
                new_projector = np.zeros((self._local_dim[idx], self._local_dim[idx]))
                new_projector[0, state] = 1
                self.apply_one_site_operator(new_projector, idx)

        self.left_canonize(self.num_sites - 1, trunc=True)
        self.right_canonize(0, trunc=True)

    #########################################################################
    ######################### Optimization methods ##########################
    #########################################################################

    def default_sweep_order(self):
        """
        Default sweep order to be used in the ground state search/time evolution.
        Default for MPS is left-to-right.

        Returns
        -------
        List[int]
            The generator that you can sweep through
        """
        return list(range(self.num_sites))

    def get_pos_partner_link_expansion(self, pos):
        """
        Get the position of the partner tensor to use in the link expansion
        subroutine. It is the tensor towards the center, that is supposed to
        be more entangled w.r.t. the tensor towards the edge

        Parameters
        ----------
        pos : int
            Position w.r.t. which you want to compute the partner

        Returns
        -------
        int
            Position of the partner
        int
            Link of pos pointing towards the partner
        int
            Link of the partner pointing towards pos
        """
        pos_partner = pos + 1 if pos < self.num_sites / 2 else pos - 1
        link_self = 2 if pos < pos_partner else 0
        link_partner = 0 if pos < pos_partner else 2

        return pos_partner, link_self, link_partner

    #########################################################################
    ######################## Time evolution methods #########################
    #########################################################################

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
            link_self in no_rtens=True mode
        Tuple[int]
            The position of the partner (pos+-1 in MPSs)
        int
            The link of the partner pointing towards pos
        List[int]
            The update path to pass to _update_eff_ops
        """
        requires_singvals = self._requires_singvals

        # Needed in other TN geometries
        link_partner = 0 if pos < next_pos else 2
        pos_partner = pos + 1 if pos < next_pos else pos - 1

        path_elem = [pos, next_pos]
        if no_rtens:
            link_self = 2 if pos < next_pos else 0
            return link_self, pos_partner, link_partner, path_elem

        if (pos < next_pos) and requires_singvals:
            # Going left-to-right, SVD
            qtens, rtens, s_vals, _ = self[pos].split_svd(
                [0, 1],
                [2],
                no_truncation=True,
                conv_params=self._convergence_parameters,
                contract_singvals="R",
            )
            self.set_singvals_on_link(pos, pos_partner, s_vals)

        elif pos < next_pos:
            # Going left-to-right, QR
            qtens, rtens = self[pos].split_qr([0, 1], [2])
            self.set_singvals_on_link(pos, pos_partner, None)
        elif requires_singvals:
            # Going right-to-left, SVD
            qtens, rtens, s_vals, _ = self[pos].split_svd(
                [1, 2],
                [0],
                no_truncation=True,
                conv_params=self._convergence_parameters,
                contract_singvals="R",
                perm_left=[2, 0, 1],
            )
            self.set_singvals_on_link(pos, pos_partner, s_vals)
        else:
            # Going right-to-left, RQ. Need to permute Q tensor (this is called
            # also by abstractTN where R cannot be permuted, always the first
            # link needs to go to the Q-tensor.)
            qtens, rtens = self[pos].split_qr([1, 2], [0], perm_left=[2, 0, 1])
            self.set_singvals_on_link(pos, pos_partner, None)
        self[pos] = qtens

        return rtens, pos_partner, link_partner, path_elem

    def contract(self, other, boundaries=None):
        """
        Contract the MPS with another MPS other <other|self>.
        By default it is a full contraction, but also a partial
        contraction is possible

        Parameters
        ----------
        other : MPS
            other MPS to contract with
        boundaries : tuple of ints, optional
            Contract to MPSs from boundaries[0] to boundaries[1].
            In this case the output will be a tensor.
            Default to None, which is  full contraction

        Returns
        -------
        contraction : complex
            Result of the contraction
        """
        if not isinstance(other, MPS):
            raise TypeError("Only two MPS classes can be contracted")
        elif np.any(self.local_dim != other.local_dim):
            raise ValueError("Local dimension must be the same to contract MPS")
        elif self.num_sites != other.num_sites:
            raise ValueError(
                "Number of sites must be the same to contract two MPS together"
            )
        if boundaries is None:
            full_contraction = True
            boundaries = (0, self.num_sites, 1)
        else:
            full_contraction = False
            boundaries = (*boundaries, np.sign(boundaries[1] - boundaries[0]))

        idx = 0 if boundaries[1] > boundaries[0] else 2
        transfer_mat = self[boundaries[0]].eye_like(self[boundaries[0]].links[idx])
        for ii in range(*boundaries):
            if boundaries[2] > 0:
                transfer_mat = transfer_mat.tensordot(self[ii], ([0], [idx]))
            else:
                transfer_mat = self[ii].tensordot(transfer_mat, ([idx], [0]))

            transfer_mat = transfer_mat.tensordot(
                other[ii].conj(), ([idx, 1], [idx, 1])
            )
        if full_contraction:
            contraction = transfer_mat.get_entry()
        else:
            new_shape = (
                (1, *transfer_mat.shape)
                if boundaries[1] > boundaries[0]
                else (*transfer_mat.shape, 1)
            )
            contraction = transfer_mat.reshape(new_shape)
        return contraction

    def kron(self, other, inplace=False):
        """
        Concatenate two MPS, taking the kronecker/outer product
        of the two states. The bond dimension assumed is the maximum
        between the two bond dimensions.

        Parameters
        ----------
        other : :py:class:`MPS`
            MPS to concatenate
        inplace : bool, optional
            If True apply the kronecker product in place. Instead, if
            inplace=False give as output the product. Default to False.

        Returns
        -------
        :py:class:`MPS`
            Concatenation of the first MPS with the second in order
        """
        if not isinstance(other, MPS):
            raise TypeError("Only two MPS classes can be concatenated")
        elif self[-1].shape[2] != 1 and other[0].shape[0] != 1:
            raise ValueError(
                "Head and tail of the MPS not compatible. Last "
                + "and first dimensions of the tensors must be the same"
            )
        elif self._tensor_backend.device != other._tensor_backend.device:
            raise RuntimeError(
                "MPS to be kron multiplied must be on the same "
                + f"device, not {self._tensor_backend.device} and "
                + f"{other._tensor_backend.device}."
            )
        max_bond_dim = max(
            self._convergence_parameters.max_bond_dimension,
            other._convergence_parameters.max_bond_dimension,
        )
        cut_ratio = min(
            self._convergence_parameters.cut_ratio,
            other._convergence_parameters.cut_ratio,
        )
        convergence_params = TNConvergenceParameters(
            max_bond_dimension=int(max_bond_dim), cut_ratio=cut_ratio
        )
        tensor_list = self.tensors + other.tensors

        addMPS = MPS.from_tensor_list(
            tensor_list, convergence_params, tensor_backend=self._tensor_backend
        )
        addMPS._singvals[: self.num_sites + 1] = self.singvals
        addMPS._singvals[self.num_sites + 1 :] = other.singvals[1:]

        if inplace:
            self.__dict__.update(addMPS.__dict__)
            return None
        else:
            return addMPS

    # ---------------------------
    # ----- MEASURE METHODS -----
    # ---------------------------

    def meas_tensor_product(self, ops, idxs):
        """
        Measure the tensor products of n operators `ops` acting on the indexes `idxs`.
        The operators should be MPOs, i.e. rank-4 tensors of shape (left, up, down, right).
        To retrieve the tensor product operators, left=right=1.

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

        if len(idxs) == 0:
            return 1

        order = np.argsort(idxs)
        idxs = np.array(idxs)[order]
        self.site_canonize(idxs[0], keep_singvals=True)

        transfer_mat = (
            self[idxs[0]].eye_like(self[idxs[0]].links[0]).attach_dummy_link(1)
        )
        jj = 0
        closed = False
        for ii in range(idxs[0], self.num_sites):
            if closed:
                break

            # Case of finished tensors
            if jj == len(idxs):
                # close with transfer matrix of correct size
                closing_transfer_mat = (
                    self[ii].eye_like(self[ii].links[0]).attach_dummy_link(1)
                )
                measure = transfer_mat.tensordot(
                    closing_transfer_mat, ([0, 1, 2], [0, 1, 2])
                )
                closed = True
            # Case of operator inside
            elif idxs[jj] == ii:
                op_jj = ops[order[jj]]
                transfer_mat = transfer_mat.tensordot(self[ii], ([0], [0]))
                transfer_mat = transfer_mat.tensordot(op_jj, ([0, 2], [0, 2]))
                transfer_mat = transfer_mat.tensordot(self[ii].conj(), ([0, 2], [0, 1]))
                jj += 1
            # Case of no operator between the sites
            else:
                transfer_mat = transfer_mat.tensordot(self[ii], ([0], [0]))
                transfer_mat = transfer_mat.tensordot(self[ii].conj(), ([1, 2], [0, 1]))
                transfer_mat.transpose_update([1, 0, 2])

        if not closed:
            # close with transfer matrix of correct size
            closing_transfer_mat = (
                self[-1].eye_like(self[-1].links[2]).attach_dummy_link(1)
            )
            measure = transfer_mat.tensordot(
                closing_transfer_mat, ([0, 1, 2], [0, 1, 2])
            )
            closed = True

        measure = measure.get_entry()

        return np.real(measure)

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
            Keys are the range of the bipartition from 0 to which the entanglement
            (value) is relative
        """
        measures = {}
        for ii, ss in enumerate(self.singvals[1:-1]):
            if hasattr(ss, "get"):
                ss = ss.get()
            if ss is None:
                s_von_neumann = None
            else:
                s_von_neumann = -2 * (ss**2 * np.log(ss)).sum()

            measures[(0, ii + 1)] = s_von_neumann

        return measures

    def meas_even_probabilities(self, threshold, qiskit_convention=False):
        """
        Compute the probabilities of measuring a given state if it is greater
        than a threshold. The function goes down "evenly" on the probability
        tree. This means that there is the possibility that no state is
        returned, if their probability is lower then threshold. Furthermore,
        notice that the **maximum** number of states returned is
        :math:`(\frac{1}{threshold})`.

        For a different way of computing the probability tree see the
        function :py:func:`meas_greedy_probabilities` or
        :py:func:`meas_unbiased_probabilities`.

        Parameters
        ----------
        threshold : float
            Discard all the probabilities lower then the threshold
        qiskit_convention : bool, optional
            If the sites during the measure are represented such that
            |201> has site 0 with value one (True, mimicks bits ordering) or
            with value 2 (False usually used in theoretical computations).
            Default to False.

        Return
        ------
        probabilities : dict
            Dictionary where the keys are the states while the values their
            probabilities. The keys are separated by a comma if local_dim > 9.
        """
        if threshold < 0:
            raise ValueError("Threshold value must be positive")
        elif threshold < 1e-3:
            warn(
                "be careful when you keep too much info: the function might"
                + "be exponentially slower"
            )

        # Put in canonic form
        self.right_canonize(0, keep_singvals=True)
        old_norm = self.norm()
        self._tensors[0] /= old_norm

        self._temp_for_prob = {}
        self._measure_even_probabilities(threshold, 1, "", 0, self[0])

        # Rewrite with qiskit convention
        probabilities = postprocess_statedict(
            self._temp_for_prob,
            local_dim=self.local_dim,
            qiskit_convention=qiskit_convention,
        )

        self._tensors[0] *= old_norm

        return probabilities

    def _measure_even_probabilities(self, threshold, probability, state, idx, tensor):
        """
        Hidden recursive function to compute the probabilities

        Parameters
        ----------
        threshold : float
            Discard of all state with probability less then the threshold
        probability : float
            probability of having that state
        states : string
            string describing the state up to that point
        idx : int
            Index of the tensor currently on the function
        tensor : np.ndarray
            Tensor to measure

        Returns
        -------
        probabilities : dict
            Dictionary where the keys are the states while the values their
            probabilities. The keys are separated by a comma if local_dim > 9.
        """
        local_dim = self.local_dim[idx]

        if probability > threshold:
            probabilities, tensors_list = self._get_children_prob(tensor, idx)
            # Multiply by the probability of having the given state
            probabilities = probability * probabilities
            states = [state + str(ii) + "," for ii in range(local_dim)]

            if idx < self.num_sites - 1:
                # Call recursive part
                for tens, prob, ss in zip(tensors_list, probabilities, states):
                    self._measure_even_probabilities(threshold, prob, ss, idx + 1, tens)
            else:
                # Save the results
                for prob, ss in zip(probabilities, states):
                    if prob > threshold:
                        ss = ss[:-1]  # Remove trailing comma
                        self._temp_for_prob[ss] = prob

    def meas_greedy_probabilities(self, max_prob, qiskit_convention=False):
        """
        Compute the probabilities of measuring a given state until the total
        probability measured is greater than the threshold max_prob.
        The function goes down "greedily" on the probability
        tree. This means that there is the possibility that a path that was
        most promising at the tree root will become very computationally
        demanding and not so informative once reached the leaves. Furthermore,
        notice that there is no **maximum** number of states returned, and so
        the function might be exponentially slow.

        For a different way of computing the probability tree see the
        function :py:func:`meas_even_probabilities` or
        :py:func:`meas_unbiased_probabilities`

        Parameters
        ----------
        max_prob : float
            Compute states until you reach this probability
        qiskit_convention : bool, optional
            If the sites during the measure are represented such that
            |201> has site 0 with value one (True, mimicks bits ordering) or
            with value 2 (False usually used in theoretical computations).
            Default to False.

        Return
        ------
        probabilities : dict
            Dictionary where the keys are the states while the values their
            probabilities. The keys are separated by a comma if local_dim > 9.
        """
        if max_prob > 0.95:
            warn(
                "Execution of the function might be exponentially slow due "
                + "to the highness of the threshold",
                RuntimeWarning,
            )

        # Set gauge on the left and renormalize
        self.right_canonize(0)
        old_norm = self.norm()
        self._tensors[0] /= old_norm

        all_probs = [{}]
        probabilities = {}
        probability_sum = 0

        tensor = self[0]
        site_idx = 0
        curr_state = ""
        curr_prob = 1
        while probability_sum < max_prob:
            if len(all_probs) < site_idx + 1:
                all_probs.append({})
            if site_idx > 0:
                states = [
                    curr_state + f",{ii}" for ii in range(self.local_dim[site_idx])
                ]
            else:
                states = [
                    curr_state + f"{ii}" for ii in range(self.local_dim[site_idx])
                ]
            # Compute the children if we didn't already follow the branch
            if not np.all([ss in all_probs[site_idx] for ss in states]):
                probs, tensor_list = self._get_children_prob(tensor, site_idx)
                probs = curr_prob * probs

                # Update probability tracker for next branch
                for ss, prob, tens in zip(states, probs, tensor_list):
                    all_probs[site_idx][ss] = [prob, tens]
            # Retrieve values if already went down the path
            else:
                probs = []
                tensor_list = []
                for ss, (prob, tens) in all_probs[site_idx].items():
                    probs.append(prob)
                    tensor_list.append(tens)
            # Greedily select the next branch if we didn't reach the leaves
            if site_idx < self.num_sites - 1:
                # Select greedily next path
                tensor = tensor_list[np.argmax(probs)]
                curr_state = states[np.argmax(probs)]
                curr_prob = np.max(probs)
                site_idx += 1
            # Save values if we reached the leaves
            else:
                for ss, prob in zip(states, probs):
                    if not np.isclose(prob, 0, atol=1e-10):
                        probabilities[ss] = prob
                        probability_sum += prob
                # Remove this probability from the tree
                for ii in range(self.num_sites - 1):
                    measured_state = states[0].split(",")[: ii + 1]
                    measured_state = ",".join(measured_state)
                    all_probs[ii][measured_state][0] -= np.sum(probs)
                # Restart from the beginning
                site_idx = 0
                curr_state = ""

        # Rewrite with qiskit convention
        final_probabilities = postprocess_statedict(
            probabilities, local_dim=self.local_dim, qiskit_convention=qiskit_convention
        )

        self._tensors[0] *= old_norm

        return final_probabilities

    def _get_children_prob(self, tensor, site_idx, *args):
        """
        Compute the probability and the relative tensor state of all the
        children of site `site_idx` in the tensor tree

        Parameters
        ----------
        tensor : np.ndarray
            Parent tensor, with respect to which we compute the children
        site_idx : int
            Index of the parent tensor
        args : list
            other arguments are not needed for the MPS implementation
            and stored in `*args`.

        Returns
        -------
        probabilities : list of floats
            Probabilities of the children
        tensor_list : list of ndarray
            Child tensors, already contracted with the next site
            if not last site.
        """
        local_dim = self.local_dim[site_idx]
        if tensor is None:
            tmp = tensor.vector_with_dim_like(local_dim)
            tmp *= 0.0
            return tmp, np.repeat(None, local_dim)

        conjg_tens = tensor.conj()
        tensors_list = []

        # Construct rho at effort O(chi_l * chi_r * d^2) which is
        # equal to contracting one projector to one tensor
        reduced_rho = tensor.tensordot(conjg_tens, ([0, 2], [0, 2]))

        # Convert to array on host/CPU with real values; select diagonal elements
        probabilities = reduced_rho.diag(real_part_only=True, do_get=True)

        # Loop over basis states
        for jj, prob_jj in enumerate(probabilities):
            # Compute probabilities of the state; projecting always to
            # one index `j`, we can read the diagonal entries of the
            # reduced density matrix
            # --> we have it already due to the trace

            # Create list of updated tensors after the projection
            if prob_jj > 0 and site_idx < self.num_sites - 1:
                # Extract the rank-2 tensor without tensordot as we operator
                # on a diagonal projector with a single index
                temp_tens = tensor.subtensor_along_link(1, jj, jj + 1)
                temp_tens.remove_dummy_link(1)

                # Contract with the next site in the MPS
                temp_tens = temp_tens.tensordot(self[site_idx + 1], ([1], [0]))
                tensors_list.append(temp_tens * (prob_jj ** (-0.5)))
            else:
                tensors_list.append(None)

        return probabilities, tensors_list

    def _get_children_magic(self, transfer_matrix, site_idx, *args):
        """
        Compute the probability and the relative tensor state of all the
        children of site `site_idx` in the tensor tree

        Parameters
        ----------
        transfer_matrix : np.ndarray
            Parent tensor, with respect to which we compute the children
        site_idx : int
            Index of the parent tensor
        args : list
            other arguments are not needed for the MPS implementation
            and stored in `*args`.

        Returns
        -------
        probabilities : list of floats
            Probabilities of the children
        tensor_list : list of ndarray
            Child tensors, already contracted with the next site
            if not last site.
        """
        tensor = deepcopy(self.get_tensor_of_site(site_idx))

        if transfer_matrix is None:
            tmp = tensor.vector_with_dim_like(4)
            tmp *= 0.0
            return tmp, np.repeat(None, 4)

        sqrt, real = tensor.get_attr("sqrt", "real")
        probabilities = tensor.vector_with_dim_like(4)
        tensors_list = []

        rho_i = tensor.tensordot(tensor.conj(), ([0, 2], [0, 2]))
        pauli_1 = rho_i.zeros_like()
        pauli_x = rho_i.zeros_like()
        pauli_y = rho_i.zeros_like()
        pauli_z = rho_i.zeros_like()

        pauli_1.set_diagonal_entry(0, 1)
        pauli_1.set_diagonal_entry(1, 1)
        pauli_x.set_matrix_entry(0, 1, 1)
        pauli_x.set_matrix_entry(1, 0, 1)
        pauli_y.set_matrix_entry(0, 1, -1j)
        pauli_y.set_matrix_entry(1, 0, 1j)
        pauli_z.set_diagonal_entry(0, 1)
        pauli_z.set_diagonal_entry(1, -1)
        paulis = [pauli_1, pauli_x, pauli_y, pauli_z]

        original_transfer_matrix = deepcopy(transfer_matrix)
        for ii, pauli in enumerate(paulis):
            temp_tens = tensor.tensordot(pauli, ([1], [1]))
            transfer_matrix = original_transfer_matrix.tensordot(temp_tens, ([0], [0]))
            transfer_matrix = transfer_matrix.tensordot(tensor.conj(), ([0, 2], [0, 1]))

            probability_as_tensor = transfer_matrix.tensordot(
                transfer_matrix.conj(), ([0, 1], [0, 1])
            )
            probabilities[ii] = real(probability_as_tensor.flatten() / 2)
            prob_host = np.real(probability_as_tensor.get_entry()) / 2
            if prob_host > 0 and site_idx < self.num_sites - 1:
                tensors_list.append(transfer_matrix / sqrt(real(probabilities[ii] * 2)))
            else:
                tensors_list.append(None)

        probabilities = tensor.get_of(probabilities)
        probabilities = np.real(probabilities)

        return probabilities, tensors_list

    def _get_child_prob(self, tensor, site_idx, target_prob, unitary_setup, *args):
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
        args : list
            Other argument are not needed for the MPS implementation
            and stored in `*args`.
        """
        # Get functions for elemtary arrays
        cumsum, sqrt = tensor.get_attr("cumsum", "sqrt")

        local_dim = self.local_dim[site_idx]

        if unitary_setup is not None:
            # Have to apply local unitary
            unitary = unitary_setup.get_unitary(site_idx)

            # Contract and permute back
            tensor = unitary.tensordot(tensor, ([1], [1]))
            tensor.transpose_update([1, 0, 2])

        conjg_tens = tensor.conj()

        # Calculate the cumulated probabilities via the reduced
        # density matrix
        reduced_rho = tensor.tensordot(conjg_tens, ([0, 2], [0, 2]))

        probs = reduced_rho.diag(real_part_only=True)
        cumul_probs = cumsum(probs)
        measured_idx = None

        for jj in range(local_dim):
            if cumul_probs[jj] < target_prob:
                continue

            prob_jj = probs[jj]

            # Reached interval with target probability ... project
            measured_idx = jj
            temp_tens = tensor.subtensor_along_link(1, jj, jj + 1)
            temp_tens.remove_dummy_link(1)
            temp_tens /= sqrt(probs[jj])

            if site_idx < self.num_sites - 1:
                temp_tens = temp_tens.tensordot(self[site_idx + 1], ([1], [0]))
            else:
                temp_tens = None

            break

        return measured_idx, temp_tens, prob_jj

    # ------------------------
    # ---- I/O Operations ----
    # ------------------------

    def write(self, filename, cmplx=True):
        """
        Write an MPS in python format into a FORTRAN format, i.e.
        transforms row-major into column-major

        Parameters
        ----------
        filename: str
            PATH to the file
        cmplx: bool, optional
            If True the MPS is complex, real otherwise. Default to True

        Returns
        -------
        None
        """
        self.convert(None, "cpu")

        with open(filename, "w") as fh:
            fh.write(str(len(self)) + " \n")
            for tens in self:
                tens.write(fh, cmplx=cmplx)

        return None

    @classmethod
    def read(cls, filename, tensor_backend, cmplx=True, order="F"):
        """
        Read an MPS written by FORTRAN in a formatted way on file.
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
            If 'F' the tensor is transformed from column-major to row-major, if 'C'
            it is left as read.

        Returns
        -------
        obj: py:class:`MPS`
            MPS class read from file
        """
        ext = "pkl" + cls.extension
        if filename.endswith(ext):
            return cls.read_pickle(filename)

        tensors = []
        with open(filename, "r") as fh:
            num_sites = int(fh.readline())

            for _ in range(num_sites):
                tens = tensor_backend.tensor_cls.read(
                    fh,
                    tensor_backend.dtype,
                    tensor_backend.device,
                    tensor_backend.base_tensor_cls,
                    cmplx=cmplx,
                    order=order,
                )
                tensors.append(tens)

        obj = cls.from_tensor_list(tensors, tensor_backend=tensor_backend)

        return obj

    # --------------------------------------
    # ---- Effective operators methods -----
    # --------------------------------------

    # pylint: disable-next=unused-argument
    def build_effective_operators(self, measurement_mode=False):
        """
        Build the complete effective operator on each
        of the links. It assumes `self.eff_op` is set.

        Parameters
        ----------
        measurement_mode : bool, optional
            If True, enable measurement mode of effective operators
        """
        self.iso_towards(self.num_sites - 1, keep_singvals=True)

        if self.eff_op is None:
            raise Exception("Trying to build eff_op without attribute being set.")

        for pos, tens in enumerate(self[:-1]):
            # Retrieve the index of the operators for the left link
            # and the physical link
            idx_out = 2
            pos_links = self.get_pos_links(pos)
            self.eff_op.contr_to_eff_op(tens, pos, pos_links, idx_out)

            if measurement_mode:
                # pylint: disable-next=unsubscriptable-object
                self.eff_op[pos, pos_links[idx_out]].run_measurements(
                    tens, idx_out, self.singvals[pos + 1]
                )

        if measurement_mode:
            # To finish measurements, we keep going through the last site as
            # well
            pos = self.num_sites - 1
            idx_out = 2
            pos_links = self.get_pos_links(pos)
            self.eff_op.contr_to_eff_op(self[-1], pos, pos_links, idx_out)

            # Last center must be isometry center
            link_weights = None
            # pylint: disable-next=unsubscriptable-object
            self.eff_op[(pos, pos_links[idx_out])].run_measurements(
                self[-1], idx_out, link_weights
            )

    def _update_eff_ops(self, id_step):
        """
        Update the effective operators after the iso shift

        Parameters
        ----------
        id_step : list of ints
            List with the iso path, i.e. `[src_tensor, dst_tensor]`

        Returns
        -------
        None
            Updates the effective operators in place
        """
        # Get info on the source tensor
        tens = self[id_step[0]]
        src_link = 0 if id_step[0] > id_step[1] else 2
        links = self.get_pos_links(id_step[0])

        # Perform the contraction
        self.eff_op.contr_to_eff_op(tens, id_step[0], links, src_link)

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
        # pylint: disable-next=unsubscriptable-object
        eff_ops = [self.eff_op[oidx] for oidx in self.op_neighbors[:, pos]]
        idx_list = np.arange(3)

        return eff_ops, idx_list

    # ------------------------
    # ---- ML Operations -----
    # ------------------------
    def ml_get_gradient_tensor(self, idx, data_sample, true_label):
        """
        Get the gradient w.r.t. the tensors at position `idx`, `idx+1`
        of the MPS following the procedure explained in
        https://arxiv.org/pdf/1605.05775.pdf for the
        data_sample given

        Parameters
        ----------
        idx : int
            Index of the tensor to optimize
        data_sample : py:class:`MPS`
            Data sample in MPS class
        true_label : int
            True label of the datasample

        Returns
        -------
        xp.ndarray
            Gradient tensor
        """
        real = self[0].get_attr("real")

        self.site_canonize(idx, True)

        if idx == 0:
            left_effective_feature = self[0].eye_like(1)
        else:
            left_effective_feature = self.contract(data_sample, (0, idx))
            left_effective_feature.remove_dummy_link(0)

        if idx == self.num_sites - 2:
            right_effective_feature = self[0].eye_like(1)
        else:
            right_effective_feature = self.contract(
                data_sample, (self.num_sites - 1, idx + 1)
            )
            right_effective_feature.remove_dummy_link(2)

        # Compute the label efficiently
        label = left_effective_feature
        for ii in (idx, idx + 1):
            label = label.tensordot(self[ii], ([0], [0]))
            label = label.tensordot(data_sample[ii].conj(), ([0, 1], [0, 1]))
        label = label.tensordot(right_effective_feature, ([0, 1], [0, 1])).get_entry()

        # Compute the fl function
        func_l = real(label)
        diff = true_label - func_l

        # Compute the gradient
        grad = left_effective_feature.conj().tensordot(data_sample[idx], ([1], [0]))
        grad = grad.tensordot(data_sample[idx + 1], ([2], [0]))
        grad = grad.tensordot(right_effective_feature.conj(), ([3], [1]))
        grad *= func_l * diff

        loss = np.abs(true_label - np.round(np.real(label)))

        return grad, loss

    def ml_optmize_tensor(
        self, idx, data_samples, true_labels, learning_rate, n_jobs=1, direction=1
    ):
        """
        Optimize a single tensor using a batch of data damples

        Parameters
        ----------
        idx : int
            Index of the tensor to optimize
        data_samples : List[py:class:`MPS`]
            List of data samples
        true_labels : xp.ndarray
            List of labels (0 or 1)
        learning_rate : float
            Learining rate for the tensor update
        n_jobs : int, optional
            Number of parallel jobs for the optimization, by default 1

        Returns
        -------
        xp.ndarray
            Singular values cut in the optimization
        float
            Value of the loss function
        """
        array = self[0].get_attr("array")

        # Canonize to idx
        self.site_canonize(idx, True)

        # Run in parallel the data batch
        res = array(
            Parallel(n_jobs=n_jobs)(
                delayed(self.ml_get_gradient_tensor)(idx, ds, tl)
                for ds, tl in zip(data_samples, true_labels)
            ),
            dtype=object,
        )

        # Sum the values for computing gradient and loss
        grad = res[:, 0].sum()
        loss = res[:, 1].sum()

        # Compute the two_tensor of site idx, idx+1 for the update
        two_tensors = self[idx].tensordot(self[idx + 1], ([2], [0]))
        two_tensors += learning_rate * grad

        # Split the tensor back and update the MPS
        direction = "R" if direction > 0 else "L"
        left, right, singvals, singval_cut = two_tensors.split_svd(
            [0, 1],
            [2, 3],
            contract_singvals=direction,
            conv_params=self._convergence_parameters,
        )
        self[idx] = left
        self[idx + 1] = right
        self.singvals[idx + 1] = singvals
        # self.normalize()

        return singval_cut, loss

    def ml_optimize_mps(
        self,
        data_samples,
        true_labels,
        batch_size,
        learning_rate,
        num_sweeps,
        n_jobs=1,
        verbose=False,
    ):
        """
        Optimize the MPS using the algorithm of Stoudenmire

        Parameters
        ----------
        data_samples : List[py:class:`MPS`]
            Feature dataset
        true_labels : List[int]
            Labels of the dataset
        batch_size : int
            Number of samples for a single sweep(epoch)
        learning_rate : float or callable
            Learning rate for the tensor update. If callable, it can depend on the sweep.
        num_sweeps : int
            Number of optimization sweeps (epochs)
        n_jobs : int, optional
            Number of parallel jobs for the optimization, by default 1
        verbose : bool, optional
            If True, print info about the optimization

        Returns
        -------
        xp.ndarray
            Singular values cut in the optimization
        xp.ndarray
            Value of the loss function at each sweep(epoch)
        """
        singvals_cut = np.zeros((self.num_sites - 1) * num_sweeps)
        loss = np.zeros(num_sweeps)

        # If learning rate is not callable do a constant function
        if not callable(learning_rate):
            learning_rate_f = lambda x: learning_rate
        else:
            learning_rate_f = learning_rate

        for nswp in range(num_sweeps):
            if verbose:
                print("=" * 20 + f" Sweep {nswp} started " + "=" * 20)

            # Select the training batch
            indexes = np.random.randint(0, len(data_samples), batch_size)
            current_samples = [data_samples[sii] for sii in indexes]
            current_labels = true_labels[indexes]

            # Left-to-right on even epochs, right-to-left for odd
            boundaries = (
                (0, self.num_sites - 1, 1)
                if nswp % 2 == 0
                else (self.num_sites - 2, -1, -1)
            )

            for ii in range(*boundaries):
                singv_cut, loss_ii = self.ml_optmize_tensor(
                    ii,
                    current_samples,
                    current_labels,
                    learning_rate_f(nswp),
                    n_jobs,
                    direction=boundaries[2],
                )

                # Postprocess the singvals as prescribed in the convergence parameters
                singvals_cut[
                    nswp * (self.num_sites - 1) + ii
                ] = self._postprocess_singvals_cut(singv_cut)
                # Save the loss function
                loss[nswp] += loss_ii

            loss[nswp] /= batch_size
            if verbose:
                print(f"Sweep loss: {loss[nswp]}")

        return singvals_cut, loss

    def ml_predict(self, data_samples, n_jobs=1):
        """
        Predict the labels of the data samples passed

        Parameters
        ----------
        data_samples : List[py:class:`MPS`]
            Feature dataset
        true_labels : List[int]
            Labels of the dataset
        n_jobs : int, optional
            Number of parallel jobs for the optimization, by default 1

        Returns
        -------
        List
            Predicted labels
        """

        labels = Parallel(n_jobs=n_jobs)(
            delayed(self.contract)(sample) for sample in data_samples
        )
        labels = np.real(np.round(labels)).astype(int)

        return labels
