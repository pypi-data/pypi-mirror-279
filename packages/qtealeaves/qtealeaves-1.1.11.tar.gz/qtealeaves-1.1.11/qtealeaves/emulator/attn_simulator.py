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
The module contains a light-weight aTTN class.
"""
from copy import deepcopy
from itertools import chain
import numpy as np

from qtealeaves.mpos.disentangler import DELayer
from qtealeaves.emulator.state_simulator import StateVector

from .ttn_simulator import TTN


__all__ = ["ATTN"]


class ATTN(TTN):
    """
    Augmented tree tensor network class = TTN + disentangler gates.

    Parameters
    ----------

    num_sites : int
        Number of sites

    convergence_parameters: :py:class:`TNConvergenceParameters`
        Class for handling convergence parameters. In particular,
        in the aTTN simulator we are interested in:
        - the *maximum bond dimension* :math:`\\chi`;
        - the *cut ratio* :math:`\\epsilon` after which the singular
            values are neglected, i.e. if :math:`\\lamda_1` is the
            bigger singular values then after an SVD we neglect all the
            singular values such that
            :math:`\\frac{\\lambda_i}{\\lambda_1}\\leq\\epsilon`

    local_dim: int, optional
        Local Hilbert space dimension. Default to 2.

    requires_singvals : boolean, optional
        Allows to enforce SVD to have singular values on each link available
        which might be useful for measurements, e.g., bond entropy (the
        alternative is traversing the whole TN again to get the bond entropy
        on each link with an SVD).

    tensor_backend : `None` or instance of :class:`TensorBackend`, optional
        Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

    initialize : string, optional
        Define the initialization method. For random entries use
        'random', for empty aTTN use 'empty'.
        Default to 'random'.

    sectors : dict, optional
        [Not Implemented for aTTN] For restricting symmetry sector and/or bond dimension
        in initialization. If empty, no restriction.
        Default to empty dictionary.

    de_sites : 2d np.array, optional
        Array with disentangler positions with n rows and 2
        columns, where n is the number of disentanglers. Counting starts from 0
        and indices are passed as in the mapped 1d system.
        If set to 'auto', the disentangler positions are automatically selected
        to fit as much disentanglers as possible.
        Default to 'random'.

    de_initialize : string, optional
        Define the initialization method. For identities use 'identity',
        for random entries use 'random'.
        Default to 'identity'.

    check_unitarity : Boolean, optional
        If True, all the disentangler tensors are checked for unitarity and
        an error is raised if the check fails.
        Default to True.


    Details
    -------
    Notation: the last layer in TTN contains the local Hilbert spaces and the
    most tensors.
    The order of legs in TTN is:
        |2
       (X)
      0| |1
    The order of legs in disentanglers is: 0,1 are attached to <psi|, and 2,3 are
    attached to |psi>, so that it matches the notation DE|psi>.
    """

    extension = "attn"
    has_de = True

    def __init__(
        self,
        num_sites,
        convergence_parameters,
        local_dim=2,
        requires_singvals=False,
        tensor_backend=None,
        initialize="random",
        sectors={},
        de_sites=None,
        de_initialize="identity",
        check_unitarity=True,
    ):
        # Pre-process local_dim to be a vector
        if np.isscalar(local_dim):
            local_dim = np.repeat(int(local_dim), num_sites)

        super().__init__(
            num_sites,
            convergence_parameters,
            local_dim=local_dim,
            requires_singvals=requires_singvals,
            tensor_backend=tensor_backend,
            initialize=initialize,
            sectors=sectors,
        )

        if de_sites is None:
            raise ValueError("de_sites have to be passed as they are model-dependent.")

        self.de_sites = np.array(de_sites)
        if len(de_sites) > 0:
            if self.de_sites.shape[1] != 2:
                raise ValueError(
                    f"Disentanglers must have 2 sites. {self.de_sites.shape[1]}"
                    "-site disentanglers not supported."
                )
            if np.max(self.de_sites) >= num_sites:
                raise ValueError(
                    f"Cannot place disentangler on site {np.max(self.de_sites)}"
                    f" in system of {num_sites} sites."
                )

        self.de_layer = DELayer(
            num_sites=num_sites,
            local_dim=local_dim,
            convergence_parameters=convergence_parameters,
            de_sites=de_sites,
            initialize=de_initialize,
            check_unitarity=check_unitarity,
        )

        # convert to the appropriate device because the aTTN initialization is
        # not aware of it
        self.convert(self._tensor_backend.dtype, self._tensor_backend.device)

    @classmethod
    def from_ttn(cls, ttn, de_sites, de_initialize="identity", check_unitarity=True):
        """
        Create aTTN from an existing TTN.

        Parameters
        ----------
        ttn : :py:class:`TTN`
            TTN part of the new aTTN
        de_sites : list or np.array
            Positions of disentanglers.
        de_initialize : str
            Method of disentangler initialization.
        """
        args = deepcopy(ttn.__dict__)
        new_attn = cls(
            num_sites=args["_num_sites"],
            convergence_parameters=args["_convergence_parameters"],
            de_sites=de_sites,
            de_initialize=de_initialize,
            check_unitarity=check_unitarity,
        )
        for key in args:
            new_attn.__dict__[key] = args[key]

        return new_attn

    def from_attn(self, include_disentanglers=True):
        """
        NOTE: For now works only for `include_disentanglers` = `False`.

        Create TTN from aTTN.

        Parameters
        ----------
        include_disentanglers : Boolean, optional
            If True, TTN will be constructed by contracting the disentanglers
            to the TTN part of aTTN. If False, only the TTN part of the aTTN
            is returned, regardless of the disentanglers.
            Default to True.
        truncation : Boolean
            Whether to truncate throughout the process of applying the
            disentangler.

        Return
        ------
        new_ttn : :py:class:`TTN`
            Resulting TTN.
        """
        # contracting the disentangler will increase the max bond dim by a factor of 4
        # new_max_bond_dim = 4 * self.convergence_parameters.max_bond_dimension
        # ttn_conv_params = TNConvergenceParameters(max_bond_dimension=new_max_bond_dim)
        # initialize the TTN from the aTTN's atributes
        args = deepcopy(self.__dict__)
        new_ttn = TTN(
            num_sites=args["_num_sites"],
            convergence_parameters=self.convergence_parameters.max_bond_dimension,
        )
        for key in args:
            if key in ["de_sites", "de_layer", "de_initialize", "check_unitarity"]:
                continue
            new_ttn.__dict__[key] = args[key]

        # contract the disentanglers if needed
        if include_disentanglers:
            raise NotImplementedError(
                "Contracting the disentanglers into TTN not yet implemented."
            )
            # for ii, disentangler in enumerate(self.de_layer):
            #     new_ttn.apply_two_site_operator(disentangler, self.de_layer.de_sites[ii])
            # new_ttn._requires_singvals = True
            # new_ttn.iso_towards([0, 0])

        return new_ttn

    @classmethod
    # pylint: disable-next=arguments-differ
    def from_statevector(
        cls,
        statevector,
        local_dim=2,
        conv_params=None,
        tensor_backend=None,
        check_unitarity=True,
    ):
        """
        Initialize an aTTN by decomposing a statevector into TTN form with 0
        disentanglers.

        Parameters
        ----------

        statevector : ndarray of shape( [local_dim]*num_sites, )
            Statevector describing the interested state for initializing the TTN

        device : str, optional
            Device where the computation is done. Either "cpu" or "gpu".

        tensor_cls : type for representing tensors.
            Default to :class:`QteaTensor`
        """

        obj_ttn = TTN.from_statevector(
            statevector, local_dim, conv_params, tensor_backend
        )
        obj = ATTN.from_ttn(obj_ttn, de_sites=[], check_unitarity=check_unitarity)

        return obj

    def to_statevector(self, qiskit_order=False, max_qubit_equivalent=20):
        """
        Decompose a given aTTN into statevector form.

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
        # get the statevector out of TTN
        statevect = super().to_statevector(qiskit_order, max_qubit_equivalent)
        statevect = StateVector(self.num_sites, self.local_dim, statevect)

        # apply the disentanglers to statevector as gates
        for ii, disentangler in enumerate(self.de_layer):
            statevect.apply_two_site_operator(disentangler, self.de_layer.de_sites[ii])

        return statevect.state

    def meas_local(self, op):
        """
        Measure a local observable along sites of the aTTN,
        excluding the sites with the disentangler (because there the
        measurement is not local anymore)

        Parameters
        ----------
        op : ndarray, shape (local_dim, local_dim)
            local operator to measure

        Return
        ------
        measures : ndarray, shape (num_sites)
            Measures of the local operator along each site except
            sites with the disentanglers. At the disentangler sites
            `measures` is set to zero.
        """
        self.check_obs_input(op)

        measures = np.zeros(self.num_sites)

        # This subroutine can be parallelized if the singvals are stored using
        # joblib
        for ii in range(self.num_sites):
            # skip disentangler sites
            if ii in self.de_layer.de_sites:
                measures[ii] = np.nan
            else:
                rho_i = self.get_rho_i(ii)

                if op.ndim == 2:
                    expectation = rho_i.tensordot(op, ([0, 1], [1, 0]))
                else:
                    tmp = deepcopy(op)
                    tmp.trace_one_dim_pair([0, 3])
                    expectation = rho_i.tensordot(tmp, ([0, 1], [1, 0]))
                measures[ii] = np.real(expectation.get_entry())

        return measures

    def get_rho_i(self, idx):
        """
        Get the reduced density matrix of the site at index idx.

        Parameters
        ----------
        idx : int
            Index of the site
        """
        # for sites without disentanglers, ingerit from TTN
        if idx not in self.de_layer.de_sites:
            return super().get_rho_i(idx)

        raise NotImplementedError(
            "get_rho_i not yet implemented for sites with disentanglers."
        )

    def _iter_de(self):
        """Iterate over all disentanglers (for convert etc)."""
        for de_tensor in self.de_layer:
            yield de_tensor

    def _iter_tensors(self):
        """Iterate over all tensors forming the tensor network (for convert etc)."""
        return chain(super()._iter_tensors(), self._iter_de())

    def _deprecated_get_eff_op_on_pos(self, pos):
        """
        Obtain the list of effective operators adjacent
        to the position pos and the index where they should
        be contracted

        Parameters
        ----------
        pos :
            key to the desired tensor

        Returns
        -------
        list of IndexedOperators
            List of effective operators
        list of ints
            Indexes where the operators should be contracted
        """
        raise NotImplementedError("Not implemented yet for aTTN.")

    def _get_children_magic(self, *args, **kwargs):
        raise NotImplementedError("Function not implemented yet")
