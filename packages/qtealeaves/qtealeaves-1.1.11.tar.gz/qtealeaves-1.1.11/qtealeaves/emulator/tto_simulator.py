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
The module contains a light-weight TTO emulator.
"""
from copy import deepcopy
from warnings import warn
import math as mt
import scipy.linalg as scla
import scipy.optimize as scop
import numpy as np
import numpy.linalg as nla
from qtealeaves.emulator.lptn_simulator import LPTN
from qtealeaves.convergence_parameters import TNConvergenceParameters
from .ttn_simulator import TTN, TTNLayer

__all__ = ["TTO"]


class TTO(TTN):
    r"""
    TREE TENSOR OPERATOR - represents a density matrix

    Parameters
    ----------
    num_sites : int
        Number of sites

    conv_params : :py:class::`TNConvergenceParameters`
        Input for handling convergence parameters.
        In particular, in the TTO simulator we are
        interested in:
        - the maximum bond dimension (max_bond_dimension)
        - the cut ratio (cut_ratio) after which the singular
        values in SVD are neglected, all singular values
        such that lambda/lambda_max <= eps
        are truncated

    local_dim : int, optional
        Dimension of Hilbert space of single site
        (defined as the same for each site).
        Default is 2.

    tensor_backend : `None` or instance of :class:`TensorBackend`
        Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

    iso_center : None or np.ndarray/list of two ints, optional
        Position of the gauge center. [i,j] means j-th
        tensor of i-th layer, i=0 is uppermost, j=0 is
        the leftmost tensor. If TTO has no gauge
        center, iso_center = None.
        Default is None.

    Initialization
    --------------

    Maximally mixed state is initialized, which may lead to memory issues for large system sizes.
    The option to initialize a (pure) product state will be included in the future.

    Tensor representation
    ---------------------
    .. codeblock::
    \ / \ /
     O   O
      \ /            } --> complex conjugates of tensors below,
       O                   access with TTO.cc_layers.tensors
       |
       O
      / \            } --> these are contained in TTO.layers
     O   O
    / \ / \

    Attributes
    ----------
    TTO.num_sites : int
        Number of sites in TTO

    TTO.local_dim : int
        Local Hilbert space dimension

    TTO.num_layers : int
        Number of layers in TTO

    TTO.layers : list of :py:class::`TTOLayer`-s
        Layers of the TTO, list of 'TTOLayer'
        objects

    TTO.cc_layers : list of :py:class::`TTOLayer`-s
        Complex conjugate part of the TTO, list
        of 'TTOLayer' objects

    TTO.probabilities : np.ndarray of float
        Mixed state probabilities for the case when
        TTO is a density matrix.

    TTO.iso_center : None or np.ndarray/list of two ints
        Position of the gauge center. [i,j] means j-th
        tensor of i-th layer, i=0 is uppermost, j=0 is
        the leftmost tensor. If the TTO has no gauge
        center, TTO.iso_center = None.

    TTO._max_bond_dim : int
        Maximal bond dimension

    TTO._cut_ratio : float
        Cut ratio

    Access to tensors
    -----------------
    - access to i-th layer with TTO[i]

        [ uppermost layer is indexed with i = 0 ]
    - access to [i,j]-th tensor with TTO[i][j]

        [ leftmost tensor is indexed with j = 0 ]
    - order of legs in tensor

        [ left leg - right leg - upper leg]
    """

    extension = "tto"
    is_ttn = False

    def __init__(
        self,
        num_sites,
        conv_params,
        local_dim=2,
        tensor_backend=None,
        iso_center=None,
        **kwargs,
    ):
        if "initialize" in kwargs:
            raise Exception("Input ignored.")
        if "sectors" in kwargs:
            raise Exception("Input ignored.")

        super().__init__(
            num_sites,
            conv_params,
            local_dim=local_dim,
            tensor_backend=None,
            initialize="ground",
        )

        self._probabilities = None

        if iso_center is not None and not isinstance(iso_center, (list, np.ndarray)):
            raise TypeError(
                "The iso_center must be None or list or np.ndarray,"
                f" not {type(iso_center)}."
            )
        if iso_center is not None:
            if len(iso_center) != 2:
                raise TypeError(
                    "The iso_center must contain exactly 2 elements,"
                    f" not {len(iso_center)} elements."
                )
            if iso_center[0] < 0 or iso_center[1] < 0:
                raise ValueError("Values in iso_center must be positive.")
            if iso_center[0] >= self.num_layers:
                raise ValueError(
                    "Invalid input for iso_center. A TTO does not"
                    f" contain {iso_center[0]}-th layer."
                )
            if iso_center[1] >= int(2 ** iso_center[0]):
                raise ValueError(
                    "Invalid input for iso_center."
                    f" The {iso_center[0]}-th layer does not contain"
                    f" {iso_center[1]} tensors."
                )
        self.iso_center = iso_center

        # TTO initializetion not aware of device
        self.convert(self._tensor_backend.dtype, self._tensor_backend.device)

    @property
    def cc_layers(self):
        """
        complex conjugate part of LPTN, returns complex conjugate tensors
        stored in TTOLayers
        """
        c_conj = [
            TTNLayer.from_tensorlist(
                x.cc_tensors,
                self.local_dim,
                self._convergence_parameters.max_bond_dim,
                self._tensor_backend.device,
            )
            for x in self.layers
        ]
        return c_conj

    @property
    def local_dim(self):
        """
        The local dimension is constrained to be always the same on the TTO
        """
        if isinstance(self._local_dim, int):
            return [self._local_dim] * self.num_sites

        return self._local_dim

    @property
    def probabilities(self):
        """
        Extracts the mixed, e.g. finite temperature, state probabilities
        from a TTO density matrix.

        Return
        ------
        prob : np.ndarray
            Mixed state probabilities in
            descending order.
        """
        if self._probabilities is not None:
            # Probabilities have been calculated before
            return self._probabilities

        # Get functions for elemtary arrays
        sort = self[0][0].get_attr("sort")

        if self.iso_center is None:
            warn(
                "Mixed state probabilities can be extracted"
                " only from TTO with gauge center at the"
                " uppermost tensor. Installing a gauge center"
                " to the TTO."
            )
            self.install_gauge_center()
        elif any(self.iso_center) != 0:
            warn(
                "Mixed state probabilities can be extracted"
                " only from TTO with gauge center at the"
                " uppermost tensor. Shifting a gauge center"
                f" from {self.iso_center} to [0,0]."
            )
            self.shift_gauge_center([0, 0])

        top = self[0][0]
        _, _, sing_val, _ = top.split_svd(
            [0, 1], [2], no_truncation=True, conv_params=self._convergence_parameters
        )  # compute_uv=False)
        prob = sort(sing_val**2)
        prob = prob[::-1]

        self._probabilities = prob
        return self._probabilities

    def trunc_probabilities(self, k_0, cut_ratio=1e-6, norm_track=False):
        """
        Truncates the mixed state probabilities of a TTO to a given
        dimension and cut ratio.

        Parameters
        ----------
        k_0 : int
            Maximal number of probabilities kept in a TTO.
        cut_ratio : float, optional
            Cut ratio.
        norm_track : Boolean, optional
            If True, the norm loss due to the truncation is returned.

        Return
        ------
        norm_loss : float, returned if `norm_track`==True
            Norm loss due to the truncation.
        """
        root = self[0][0]
        conv_params = TNConvergenceParameters(
            max_bond_dimension=k_0, cut_ratio=cut_ratio
        )
        root, _, _, norm_loss = root.split_svd(
            [0, 1],
            [2],
            contract_singvals="L",
            conv_params=conv_params,
        )
        norm_loss = 1 - np.sum(norm_loss**2)
        self[0][0] = deepcopy(root)
        self._probabilities = None
        self.iso_center = [0, 0]

        if norm_track:
            return norm_loss

        return None

    def install_gauge_center(self):
        """
        Install a gauge center to the position [0,0] (uppermost tensor)
        of the TTO.

        Return
        ------
        None
        """

        self.isometrize_all()
        return None

    def shift_gauge_center(self, ind_final, keep_singvals=False):
        """
        Shift a gauge center of the TTO to a given position.

        Parameters
        ----------
        ind_final : list or np.array of lenght 2
            Index where we want the new gauge center to be.
        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.

        Returns
        -------
        None

        **Remark : [i,j] means j-th tensor of i-th layer, i=0 is uppermost, j=0 is
                   the most left tensor
        """
        self.iso_towards(ind_final, keep_singvals)

        return None

    def purity(self, prob=None):
        """
        Computes the purity entanglement monotone for a
        density matrix in the TTO form.

        purity = Tr(rho^2), where rho is a density matrix.
        The above relation is equivalent to:
        purity = sum(prob^2), where prob are mixed state
        probabilities.

        Parameters
        ----------
        prob : np.ndarray, optional
            Mixed state probabilities.
            If given, purity is calculated
            with them. If None, the probabilities
            are calculated from the TTO.
            Default is None.

        Return
        ------
        float :
            Purity of the TTO density matrix.
        """
        if prob is None:
            prob = self.probabilities

        return np.sum(prob * prob)

    def negativity(self, sqrt=False):
        """
        Computes the negativity entanglement monotone
        for a mixed state density matrix in the TTO form.

        - Measures the entanglement between the left and right half of
        the 1D system.

        Parameters
        ----------
        sqrt : Boolean
            Methematically, negativity can be computed in two different ways.
            If True, it is computed via the square of partially transposed density
            matrix, and if False, it is computed via the eigenvalues of partially
            transposed density matrix.

        Return
        ------
        neg : float
            Negativity of the TTO.
        """
        if self.iso_center is None:
            warn(
                "Negativity can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                " Installing a gauge center to the uppermost"
                " tensor."
            )
            self.install_gauge_center()
        elif any(self.iso_center) != 0:
            warn(
                "Negativity can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                f" Shifting a gauge center from {self.iso_center}"
                " to [0,0]."
            )
            self.shift_gauge_center([0, 0])

        root_rho = self[0][0].tensordot(self[0][0].conj(), [[2], [2]])

        # partial transpose with respect to one subsystem (half of
        # the system in this case)
        # the resulting negativity is independent of the
        # choice of which from the two subsystems we transpose
        part_transpose = root_rho.transpose((2, 1, 0, 3))
        dims = part_transpose.shape
        part_transpose = part_transpose.reshape((dims[0] * dims[1], dims[0] * dims[1]))
        if part_transpose.device in ["gpu"]:
            sqrt = False

        # depending on a chosen method, perform corresponding calculation
        if sqrt:
            tmp = part_transpose.tensordot(part_transpose.conj(), ([1], [1]))
            neg = tmp.sqrtm()
            neg = neg.trace(return_real_part=True, do_get=True)
            neg = 0.5 * (neg - 1)
        else:
            absval, summe = part_transpose.get_attr("abs", "sum")
            eig_vals = part_transpose.eigvalsh()
            neg = summe(absval(eig_vals) - eig_vals)
            neg = part_transpose.get_of(neg)
            neg *= 0.5

        return neg

    def entropy(self, prob=None, local_dim=2, eps=1e-10):
        """
        This function calculates Von Neumann entropy of
        a TTO mixed state density matrix.
        entropy = -sum(prob log(prob)), where prob are the mixed state
        probabilities and logarithm base is local_dim.

        Parameters
        ----------
        prob : np.ndarray, optional
            Mixed state probabilities.
            If given, the entropy is calculated
            faster.
            Default is None.

        local_dim : int, optional
            Dimension of local Hilbert space.
            Default is 2.

        eps : float, optional
            To make calculation faster and avoid division
            by zero, all the probabilities smaller than
            <eps> are cut off.
            Default is 1e-10.

        Return
        ------
        entropy : float
            Von Neumann entropy of a TTO density matrix.
        """
        # if not given, get mixed state probabilities
        if prob is None:
            prob = self.probabilities

        # truncate probabilities
        mask = prob > eps
        prob = prob[mask]
        # convert logarithm base to local_dim and calculate entropy
        log_val = np.log(prob) / np.log(local_dim)
        entropy = -np.sum(prob * log_val)

        return entropy

    def renyi_entropy(self, alpha, prob=None, local_dim=2, eps=1e-10):
        """
        This function calculates Renyi entropy of order alpha for
        a TTO mixed state density matrix.
        Renyi entropy = 1/(1-alpha)*sum(log(prob**alpha)), where prob are
        the mixed state probabilities and logarithm base is local_dim

        Parameters
        ----------
        alpha : float
            order of Renyi entropy.

        prob : np.ndarray, optional
            Mixed state probabilities.
            If given, the entropy is calculated
            faster.
            Default is None.

        local_dim : int, optional
            Dimension of local Hilbert space.
            Default is 2.

        eps : float, optional
            To make calculation faster and avoid division
            by zero, all the probabilities smaller than
            <eps> are cut off.
            Default is 1e-10.

        Return
        ------
        entropy : float
            Alpha-order Renyi entropy of the given TTO
            density matrix.
        """
        if abs(alpha - 1) < 1e-8:
            raise ValueError("Value for input parameter alphacannot be equal to 1.")

        # if not given, get mixed state probabilities
        if prob is None:
            prob = self.probabilities

        # cut off all probabilities smaller than <eps>
        mask = prob > eps
        prob = prob[mask]

        # convert logarithm base to local_dim and calculate Renyi
        # entropy
        log_val_sum = np.log(np.sum(prob**alpha)) / np.log(local_dim)
        r_entropy = 1 / (1 - alpha) * log_val_sum

        return r_entropy

    def concurrence(self):
        """
        This function calculates the concurrence entanglement
        monotone for two qubits:

        C(rho) = sqrt(sqrt(rho)*rho_tilde*sqrt(rho)),

        where rho is a density matrix and rho_tilde
        is (sigma_y sigma_y) rho* (sigma_y sigma_y).

        Parameters
        ----------
        self : :pyclass:`TTO`
            Two-qubit density matrix TTO.

        Returns
        -------
        conc : float
            The concurrence entanglement monotone
            of a given TTO.
        """
        if (self.num_sites != 2) or (self.local_dim != 2):
            raise ValueError(
                "Concurrence can only be computed for the"
                f" case of two qubits, not {self.num_sites} sites with"
                f" local dimension {self.local_dim}."
            )

        if self.iso_center is None:
            warn(
                "Concurrence can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                " Installing a gauge center to the uppermost"
                " tensor."
            )
            self.install_gauge_center()
        elif any(self.iso_center) != 0:
            warn(
                "Concurrence can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                f" Shifting a gauge center from {self.iso_center}"
                " to [0,0]."
            )
            self.shift_gauge_center([0, 0])

        root_dm = self[0][0].tensordot(self[0][0].conj(), [[2], [2]])

        root_dm = root_dm.reshape(
            (root_dm.shape[0] * root_dm.shape[1], root_dm.shape[2] * root_dm.shape[3]),
        )

        rho_sqrt = root_dm.sqrtm()

        sigma_y_mat = rho_sqrt.zeros_like(root_dm)
        sigma_y_mat.set_matrix_entry(0, 3, -1)
        sigma_y_mat.set_matrix_entry(1, 2, 1)
        sigma_y_mat.set_matrix_entry(2, 1, 1)
        sigma_y_mat.set_matrix_entry(3, 0, -1)

        rho_tilde = sigma_y_mat @ root_dm.conj() @ sigma_y_mat
        conc_mat = rho_sqrt @ rho_tilde @ rho_sqrt

        conc_mat = conc_mat.sqrtm()

        # Move to host
        conc_mat = conc_mat.get().to_dense()

        val, _ = np.linalg.eig(conc_mat)
        val = np.sort(val)[::-1]
        conc = abs(2 * val[0] - np.sum(val))
        conc = max([0, conc])

        return conc

    def eof(self, init_guess=None, unitary=None, extra=0, maxiter=300):
        """
        This function estimates entanglement of formation
        (EoF) of a TTO mixed state density matrix.

        Definition:
        EoF = min( sum( p_j * E( psi_j ) ) ),
        where the minimum is found over all the possible
        decompositions of density matrix to states psi_j
        and corresponding probabilities p_j. E() is the
        entropy of entanglement with respect to two halves
        of the system.

        Parameters
        ----------
        extra : int, optional
            The minimization for computing EoF
            is run over unitary matrices of
            dimension K0 x k_dim, where k_dim = K0 + <extra>,
            K0 is the number of probabilities kept in a mixed
            state density matrix.
            Default is 0.

        init_guess : np.ndarray or list of real numbers, optional
            Initial entries for elements of Hermitian matrix needed for
            constructing the unitary matrix.
            First k_dim entries are the values on the diagonal.
            Next (k_dim^2-k_dim)/2 entries are the values for real
            part of matrix elements above the diagonal.
            Next (k_dim^2-k_dim)/2 entries are the values for imaginary
            part of matrix elements above the diagonal.
            When initializing the Hermitian matrix, the elements above
            the diagonal will be filled with the values from <init_guess>
            list row by row.
            Default is None.

        unitary : 2D np.ndarray, 1st axis dimension must be equal to the
                  number of probabilities kept in a density matrix, optional
            The EoF is computed only for the density matrix decomposition defined
            with this unitary matrix and no optimization is done.
            Either init_guess or unitary must be specified.
            Default is None.

        maxiter : int, optional
            Maximal number of iterations for minimization.
            Default is 300.

        Return
        ------
        eof : float
            An estimate of the EoF of a given mixed state
            density matrix.

        Only if init_params is not None:
        params.x : np.ndarray
            Optimal solution for entries for Hermitian matrix defining
            the decomposition of density matrix.
        """

        if (init_guess is None) and (unitary is None):
            raise ValueError("Either init_guess or unitary must be specified.")

        if self.iso_center is None:
            warn(
                "EoF can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                " Installing a gauge center to the uppermost"
                " tensor."
            )
            self.install_gauge_center()
        elif any(self.iso_center) != 0:
            warn(
                "EoF can be computed only for TTO"
                " with gauge center at the uppermost tensor."
                f" Shifting a gauge center from {self.iso_center}"
                " to [0,0]."
            )
            self.shift_gauge_center([0, 0])

        # take the root tensor of TTO, as all the important info
        # is stored in it
        root = self[0][0]
        n_20 = deepcopy(root.shape[0])
        n_21 = deepcopy(root.shape[1])
        # reshape it into matrix
        root = np.reshape(root, (root.shape[0] * root.shape[1], root.shape[2]))

        def func_target(params, unitary=None):
            """
            Takes an array of parameters and from it constructs the
            unitary matrix used to get the new decomposition of mixed state density
            matrix. Calculates the entropy of entanglement for each of
            the new pure states in this decomposition and multiplies it
            with the new probabilities to obtain the target function.

            Parameters
            ----------
            params : np.array
                Entry values for Hermitian matrix from which
                the unitary matrix is constructed.
                For the details of construction, see eof docstring
                above.

            Return
            ------
            target : float
                For EoF, we are looking for the decomposition which minimizes
                this target function:
                sum_j( pj * E(psi_j) ), where E() is entropy of entanglement
            """
            if unitary is None:
                # construct the hermitian matrix from input
                # parameters
                herm = np.zeros((k_dim, k_dim), dtype=np.complex128)

                num = int(0.5 * k_dim * (k_dim + 1))
                new_params = np.complex128(params[k_dim:num] + 1j * params[num:])
                ind = np.triu_indices_from(herm, 1)
                herm[ind] = new_params
                herm += herm.conj().T
                herm += np.diag(params[:k_dim])

                # get the unitary matrix from Hermitian by taking
                # an exponential
                unitary = scla.expm(herm * 1j)

                # take K0 rows for matrix to be compatible for
                # matrix matrix multiplication with <root> matrix
                unitary = unitary[:k_dim, :]

            # find the new root matrix for new decomposition
            new_root = np.matmul(root, unitary)

            # find the new probabilities
            new_prob = np.real(np.sum(new_root.conj() * new_root, axis=0))

            # now calculate the entropy of entanglement of each of the new
            # states in the decomposition (that is, every column of the
            # new_root matrix) - in code do loop over jj

            # The entanglement entropy E() for a pure state system composed of
            # two subsystems, A and B, is the Von Neumann entropy of the reduced
            # density matrix for any of the subsystems.

            # It can be shown that E(psi_AB) can be expressed through singular
            # values of the Schmidt decomposition of the system, by using the
            # squared singular values as probabilities for Von Neumann entropy.

            # reshape the matrix so it has two legs for two subsystems - needed
            # for Schmidt decomposition
            root_bipartite = np.reshape(new_root, (n_20, n_21, new_root.shape[1]))

            # find the minimization target value
            target = 0
            for jj in range(0, root_bipartite.shape[2]):
                # find the Schmidt decomposition singular values
                sing_vals = nla.svd(root_bipartite[:, :, jj], compute_uv=False)

                # use sing_vals to calculate the Von Neumann entropy
                # the sing_vals are divided with new_prob[jj] here, because of
                # the normalization of the new wave functions
                ent = self.entropy(
                    prob=sing_vals**2 / new_prob[jj], local_dim=self.local_dim
                )

                # the function which has to be minimized
                target += ent * new_prob[jj]

            return target

        if unitary is None:
            k_dim = root.shape[1] + extra

            # minimization
            params = scop.minimize(
                func_target,
                init_guess,
                method="Nelder-Mead",
                options={"maxiter": maxiter},
            )
            eof = params.fun
            return eof, params.x

        # Case with given unitary

        # compute EoF for the specific density matrix decomposition defined
        # with unitary
        eof = func_target(init_guess, unitary=unitary)
        return eof

    def tree(self, matrix_in, conv_params):
        """
        Transforms a given matrix into a tensor network as below:

        .. code-block::

                    |
            |       O
            O ---> / \
            |     O   O
                  |   |

        the first index of a matrix corresponds to the lower
        leg of the input tensor

        Parameters
        ----------

        self : :py:class:`TTO`
            Initialized TTO for which the tree method is used.
            From it, the local dimension and convergence parameters
            for SVD are extracted.

        matrix_in : ndarray
            Matrix to be transformed.

        conv_params : [TNConvergenceParameters]
            Input for handling convergence parameters.

        Returns
        -------

        tens_left, tens_mid, tens_right : ndarray
            Tensors of the second TN on the picture above,
            read from left to right.
            --> order of indices:
                tens_left, tens_right - [lower, upper]
                tens_mid - [lower left, upper, lower right]
        """
        dim = self.local_dim
        if len(set(list(dim))) != 1:
            raise Exception("Different local dimensions not yet supported for TTO.")

        dim = dim[0]
        num_sites2 = int(mt.log(matrix_in.shape[0], dim) / 2)

        matrix_in = matrix_in.reshape(
            (int(dim**num_sites2), int(dim**num_sites2), matrix_in.shape[1]),
        )
        tens_left, tens_mid, _, _ = matrix_in.split_svd(
            [0], [2, 1], contract_singvals="R", conv_params=conv_params
        )

        tens_mid, tens_right, _, _ = tens_mid.split_svd(
            [0, 1],
            [2],
            perm_left=[0, 2, 1],
            perm_right=[1, 0],
            contract_singvals="L",
            conv_params=conv_params,
        )

        return tens_left, tens_mid, tens_right

    @classmethod
    def dm_to_tto(cls, num_sites, dim, psi, prob, conv_params, tensor_backend=None):
        """
        Computes the TTO form of a given density matrix

        Parameters
        ----------
        num_sites : int
            Number of sites

        dim : int
            Local Hilbert space dimension

        psi,prob : matrix or vector, matrix or int
            - Mixed states :
                psi is a matrix with eigenstates as columns,
                prob is 1D array containing (possibly truncated)
                probabilities for each state
            - Pure states : psi is a state, prob = 1


        conv_params : :py:class::`TNConvergenceParameters`
            Input for handling convergence parameters.
            in particular, we are interested in:
            - the maximum bond dimension (max_bond_dimension)
            - the cut ratio (cut_ratio) after which the singular
            values in SVD are neglected, all singular values
            such that lambda/lambda_max <= eps
            are truncated

        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Return
        ------
        rho_tt : :py:class:`TTO`
            TTO form of the density matrix
        """
        if dim < 2:
            raise ValueError("Local dimension must be at least 2")

        # Initialize the TTO
        rho_tt = cls(
            num_sites,
            local_dim=dim,
            conv_params=conv_params,
            tensor_backend=tensor_backend,
        )
        tensor_cls = rho_tt._tensor_backend.tensor_cls

        # First construct the density matrix so that it is split in two parts,
        # sqrt(pj)|psi_j> and sqrt(pj)<psi_j|
        # Take the first part and work with it, the rest will be the complex
        # conjugate

        psi = np.sqrt(prob) * psi
        if len(psi.shape) == 1:
            psi = psi.reshape((len(psi), 1))  # =O-

        psi = tensor_cls.from_elem_array(psi)

        # Start growing branches layer by layer, starting from the uppermost
        # tensor towards below (check what TTO.tree function does)
        # tree2 wil be the tensor in TTO layer and tree1,tree3 are used to
        # grow lower branches
        mid = [deepcopy(psi)]
        for ii in range(0, rho_tt.num_layers - 1):  # iterate to get all the layers
            mid_t = deepcopy(mid)
            mid = []
            lay = []
            for tensor in mid_t:
                tree1, tree2, tree3 = rho_tt.tree(tensor, conv_params=conv_params)
                mid.append(tree1)
                mid.append(tree3)
                lay.append(tree2)
            rho_tt[ii] = TTNLayer.from_tensorlist(lay, dim)

        lay = []

        # Reshape the lowest layer tensors to get the shape we need
        for tensor in mid:
            tensor = np.reshape(tensor, (dim, dim, tensor.shape[1]))
            lay.append(tensor)
        rho_tt[-1] = TTNLayer.from_tensorlist(lay)
        rho_tt.iso_center = [0, 0]

        rho_tt.convert(rho_tt._tensor_backend.dtype, rho_tt._tensor_backend.device)

        return rho_tt

    @classmethod
    def lptn_to_tto(cls, tensor_list, conv_params, tensor_backend):
        """
        Transforms the density matrix from LPTN to TTO form

        Parameters
        ----------
        tensor_list : list
            Tensors in LPTN, LPTN.tensors

        conv_params : :py:class:`TNConvergenceParameters`
            Input for handling convergence parameters
            in particular, we are interested in:
            - the maximum bond dimension (max_bond_dimension)
            - the cut ratio (cut_ratio) after which the singular
            values in SVD are neglected, all singular values
            such that lambda/lambda_max <= eps
            are truncated

        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Return
        ------
        tto : :py:class:`TTO`
            TTO form of the input LPTN
        """

        num_sites = len(tensor_list)
        dim = tensor_list[0].shape[1]

        tto = cls(
            num_sites,
            local_dim=dim,
            conv_params=conv_params,
            tensor_backend=tensor_backend,
        )

        for ii in range(tto.num_layers - 1, 0, -1):
            work = tensor_list
            tensor_list = []
            for jj in range(0, len(work), 2):
                # First combine and merge tensors from the tensor_list
                # (initially LPTN tensors) into pairs
                work2 = work[jj].tensordot(work[jj + 1], [[3], [0]])
                work2 = work2.transpose([1, 3, 0, 2, 4, 5])

                #                 ||
                # SVD decompose  --O--  into l_mat,r_mat so that lower legs
                #                 ||   go to l_mat and the rest goes to r_mat

                # we do the SVD decomposition, truncate the
                # singular values and contract them into r_mat
                l_mat, r_mat, _, _ = work2.split_svd(
                    [0, 1],
                    [2, 3, 4, 5],
                    contract_singvals="R",
                    conv_params=conv_params,
                )

                # --> l_mat will be one of the tensors in TTO layer
                tto[ii][jj // 2] = l_mat

                #                                  ||
                # Now SVD decompose r_mat matrix --O-- so that lower and side legs
                #                                  |
                # go to tens_down and upper legs go to tens_up
                # tens_down is contracted with singular values, ignore tens_up because
                # it is unitary and it cancels out with the
                # complex conjugate from the upper part of the TN
                tens_down, _, _, _ = r_mat.split_svd(
                    [1, 0, 4],
                    [2, 3],
                    perm_left=[0, 1, 3, 2],
                    contract_singvals="L",
                    conv_params=conv_params,
                )

                # Now append tens_down to the new tensor_list and repeat the same
                # procedure in next iteration over ii to get the upper layers
                tensor_list.append(deepcopy(tens_down))

                # The whole procedure will be repeated with the new
                # lptn-like list stored in tensor_list.

        # For the uppermost tensor we do not need to do all of the above.
        # Contract the two remaining tensors from tensor_list and reshape
        # them to get the shape we need.
        work2 = tensor_list[0].tensordot(tensor_list[1], [[3], [0]])
        work2 = work2.transpose([0, 1, 2, 4, 3, 5])
        work2.reshape_update(
            (work2.shape[1], work2.shape[2] * work2.shape[3], work2.shape[4])
        )

        # To truncate the probabilities, SVD the tensor so that lower and
        # side legs + singular values go to work2.
        # Ignore the other tensor because it is unitary and cancels out with the
        # complex conjugate from the upper part of the TTO.

        # Remark: the multiplication with 100 in tto.tSVD is because the SVD algorithm
        # otherwise has a problem with convergence. The result is later divided with
        # 100 to restore the original value.
        work2, _, _, _ = work2.split_svd(
            [0, 2],
            [1],
            contract_singvals="L",
            conv_params=conv_params,
        )
        tto[0][0] = deepcopy(work2)
        tto.iso_center = [0, 0]

        tto.convert(tto._tensor_backend.dtype, tto._tensor_backend.device)
        return tto

    @classmethod
    def lptn_to_tto_iso(cls, tensor_list, conv_params, k_0=None, norm=False):
        """
        Transforms the density matrix from LPTN to TTO form,
        keeping the TN isometrized throughout the procedure.

        Parameters
        ----------
        tensor_list : list
            List of tensors in LPTN, LPTN.tensors.

        conv_params : :py:class:`TNConvergenceParameters`
            Input for handling convergence parameters
            in particular, we are interested in:
            - the maximum bond dimension (max_bond_dimension)
            - the cut ratio (cut_ratio) after which the singular
            values in SVD are neglected, all singular values
            such that lambda/lambda_max <= eps
            are truncated.

        k_0 : int, optional
            Dimension of link connecting two sides
            of TTO (upper link of the root tensor).
            Default to `None`.

        norm : Boolean, optional
            Used to track the cumulated norm loss due
            to the SVD truncation through the procedure.
            If `True`, the truncated norm of the TTO
            is returned.
            Default to `False`.

        Return
        ------
        tto : :py:class:`TTO`
            TTO form of the input LPTN

        norm_track : int
            Returned if `norm==True`.
            Truncated norm of the TTO obtained by keeping
            the track of singular value truncations.
            Note that this is not the actual norm of the TTO,
            as the singular values are renormalized after
            each truncation and therefore actual norm is kept
            to 1.
        """

        num_sites = len(tensor_list)
        dim = tensor_list[0].shape[1]
        if k_0 is None:
            k_0 = conv_params.max_bond_dimension

        tto = cls(num_sites, local_dim=dim, conv_params=conv_params)

        conv_params_lptn = TNConvergenceParameters(
            max_bond_dimension=int(dim**num_sites), cut_ratio=1e-8
        )

        norm_track = 1

        for ii in range(tto.num_layers - 1, 0, -1):
            # first move the isometry center of the LPTN tensors to the first
            # tensor
            n_lptn = len(tensor_list)
            lptn_work = LPTN.from_tensor_list(
                tensor_list,
                conv_params=conv_params_lptn,
                iso_center=[n_lptn - 1, n_lptn + 1],
            )
            lptn_work.shift_gauge_center([0, 2])

            work = deepcopy(lptn_work.tensors)
            tensor_list = []

            for jj in range(0, len(work), 2):
                # combine and merge tensors from the tensor_list
                # (initially LPTN tensors) into pairs
                work2 = work[jj].tensordot(work[jj + 1], [[3], [0]])
                work2 = work2.transpose([1, 3, 0, 2, 4, 5])

                #                 ||
                # SVD decompose  --O--  into l_mat,r_mat so that lower legs
                #                 ||   go to l_mat and the rest goes to r_mat

                # we do the SVD decomposition, truncate the
                # singular values and contract them into r_mat
                # Remark: work2 matrix is divided by 100 to solve some SVD convergence issue,
                # this is taken into account later so that the results remain the same.
                l_mat, r_mat, _, track = work2.split_svd(
                    [0, 1],
                    [2, 3, 4, 5],
                    contract_singvals="R",
                    conv_params=conv_params,
                )

                # track the norm loss
                norm_track = norm_track * (1 - np.sum((track) ** 2))

                # --> l_mat will be one of the tensors in TTO layer
                tto[ii][jj // 2] = deepcopy(l_mat)

                #                                  ||
                # Now SVD decompose r_mat matrix --O-- so that lower and side legs
                #                                  |

                # go to tens_down and upper legs go to tens_up
                # tens_down is contracted with singular values, ignore tens_up because
                # it is unitary and it cancels out with the
                # complex conjugate from the upper part of the TN
                tens_down, _, _, _ = r_mat.split_svd(
                    [1, 0, 4],
                    [2, 3],
                    perm_left=[0, 1, 3, 2],
                    contract_singvals="L",
                    conv_params=conv_params,
                )

                # track the norm loss
                norm_track = norm_track * (1 - np.sum(track**2))

                # QR decompose tens_down so that the tens_down becomes unitary, and contract
                # the R matrix with the next left tensor in order to shift the isometry center
                tens_down, r_mat = tens_down.split_qr([0, 1, 2], [3])
                if jj != (len(work) - 2):
                    work[jj + 2] = r_mat.tensordot(work[jj + 2], [[1], [0]])

                # Now append tens_down to the new tensor_list and repeat the same
                # procedure in next iteration over ii to get the upper layers
                tensor_list.append(deepcopy(tens_down))

                # The whole procedure will be repeated with the new
                # lptn-like list stored in tensor_list.

        # For the uppermost tensor we do not need to do all of the above.
        # Contract the two remaining tensors from tensor_list and reshape
        # them to get the shape we need.
        work2 = tensor_list[0].tensordot(tensor_list[1], [[3], [0]])
        work2 = np.transpose(work2, axes=[0, 1, 2, 4, 3, 5])
        work2 = np.reshape(
            work2, (work2.shape[1], work2.shape[2] * work2.shape[3], work2.shape[4])
        )

        # To truncate the probabilities, SVD the tensor so that lower and
        # side legs + singular values go to work2.
        # Ignore the other tensor because it is unitary and cancels out with the
        # complex conjugate from the upper part of the TTO.

        # Remark: the multiplication with 100 in tto.tSVD is because the SVD algorithm
        # otherwise has a problem with convergence. The result is later divided with
        # 100 to restore the original value.
        # conv_params.cut_ratio = np.sqrt(conv_params.cut_ratio)
        conv_params2 = TNConvergenceParameters(max_bond_dimension=k_0, cut_ratio=1e-8)
        work2, _, _, track = work2.split_svd(
            [0, 2],
            [1],
            contract_singvals="L",
            conv_params=conv_params2,
        )
        # track the norm loss
        norm_track = norm_track * (1 - np.sum(track**2))
        tto[0][0] = deepcopy(work2)
        tto.iso_center = [0, 0]

        if norm:
            return tto, norm_track

        return tto

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
    ############################ Apply methods ##############################
    #########################################################################

    #########################################################################
    ######################### Measurement methods ###########################
    #########################################################################

    @classmethod
    def from_statevector(
        cls, statevector, local_dim=2, conv_params=None, tensor_backend=None
    ):
        """
        Initialize the TTO by decomposing a statevector into TTO form.

        We use the dm_to_tto function isntead of mapping the statevector to
        TTN and the TTN to TTO since in this way we avoid the problems arising
        from the different structures of the top layer.

        Parameters
        ----------

        statevector : ndarray of shape( [local_dim]*num_sites, )
            Statevector describing the interested state for initializing the TTN

        tensor_backend : `None` or instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.
        """
        num_sites = len(statevector.shape)

        if local_dim != statevector.shape[0]:
            raise Exception("Mismatch local dimension (passed and one in array).")

        tto = cls.dm_to_tto(
            num_sites,
            local_dim,
            statevector.reshape(-1),
            1,
            conv_params,
            tensor_backend=tensor_backend,
        )

        tto.convert(tto._tensor_backend.dtype, tto._tensor_backend.device)

        return cls

    #########################################################################
    ######### Methods not well defined for TTOs inherited from TTN ##########
    #########################################################################
    def dot(self, other):
        """
        Not implemented
        """
        raise NotImplementedError("dot product not implemented for TTOs")

    def to_statevector(self, qiskit_order=False, max_qubit_equivalent=20):
        """
        Not implemented
        """
        raise NotImplementedError("to_statevector product not implemented for TTOs")

    def to_tensor_list(self):
        """
        Not implemented
        """
        raise NotImplementedError("to_tensor_list product not implemented for TTOs")

    def write(self, filename, cmplx=True):
        """
        Not implemented
        """
        raise NotImplementedError("write product not implemented for TTOs")

    @classmethod
    def read(cls, filename, tensor_backend, cmplx=True, order="F"):
        """
        Not implemented
        """
        raise NotImplementedError("read product not implemented for TTOs")

    @classmethod
    def read_v0_2_29(cls, filename, tensor_backend, cmplx=True, order="F"):
        """
        Not implemented
        """
        raise NotImplementedError("read product not implemented for TTOs")
