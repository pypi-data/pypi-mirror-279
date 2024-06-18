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
Disentangler layer class  used for aTTN.
"""

# pylint: disable=too-many-arguments

from warnings import warn
import numpy as np

from qtealeaves.tooling.restrictedclasses import _RestrictedList
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.tensors import _AbstractQteaTensor, QteaTensor
from qtealeaves.operators import TNOperators
from .indexedtpo import ITPO
from .densempos import MPOSite, DenseMPO, DenseMPOList


__all__ = ["DELayer"]


class DELayer(_RestrictedList):
    """
    Disentangler layer, i.e. the list of disentangler tensors. All the
    DE tensors must be unitary. One can access a specific tensor by
    checking DELayer[ind]. In aTTN, DELayer can be accessed via
    ATTN.de_layer. The leg ordering in disentangler is:

    .. code-block::
        |psi>
      2      3
      |      |
    |----------|
    |----------|
      |      |
      0      1
        <psi|

    Parameters
    ----------

    num_sites : int
        Number of sites

    de_sites : 2d np.array, optional
        Array with disentangler positions with n rows and 2
        columns, where n is the number of disentanglers. Counting starts from 0
        and indices are passed as in the mapped 1d system.
        If set to 'auto', the disentangler positions are automatically selected
        to fit as much disentanglers as possible.
        Default to 'random'.

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

    initialize : string, optional
        Define the initialization method. For identities use 'identity',
        for random entries use 'random'.
        Default to 'identity'.

    check_unitarity : Boolean, optional
        If True, all the disentangler tensors are checked for unitarity and
        an error is raised if the check fails.
        Default to True.
    """

    class_allowed = _AbstractQteaTensor

    def __init__(
        self,
        num_sites,
        de_sites,
        convergence_parameters,
        local_dim=2,
        initialize="identity",
        check_unitarity=True,
    ):
        super().__init__()
        # Pre-process local_dim to be a vector
        if np.isscalar(local_dim):
            local_dim = np.repeat(int(local_dim), num_sites)
        else:
            pass

        self.de_sites = np.array(de_sites)
        if len(self.de_sites) > 0:
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

        self._num_sites = num_sites
        self._local_dim = local_dim
        self._convergence_parameters = convergence_parameters
        self._check_unitarity = check_unitarity

        # disentangler gate initialization
        if initialize == "identity":
            de_tensor = QteaTensor(
                (local_dim[0] * local_dim[0], local_dim[0] * local_dim[0]),
                ctrl="R",
                device="cpu",
            )
            de_tensor = de_tensor.eye_like(de_tensor.links[0])
            de_tensor.reshape_update(
                (local_dim[0], local_dim[0], local_dim[0], local_dim[0])
            )
        elif initialize == "random":
            de_tensor = QteaTensor(
                np.repeat(local_dim[0] * local_dim[0], 2), ctrl="R", device="cpu"
            )
            de_tensor = de_tensor.random_unitary(link=local_dim[0] * local_dim[0])
            de_tensor = de_tensor.reshape(np.repeat(local_dim[0], 4))
        elif initialize == "auto":
            self.de_sites = []
            raise NotImplementedError(
                "Automatic disentangler selection requires a Hamiltonian and can "
                "be set only from the simulation."
            )
        else:
            raise ValueError(
                "Disentangler can only be initialized as 'identity' "
                f" or 'random', not as {initialize}."
            )
        for _ in range(self.num_de):
            self.append(de_tensor)

    @property
    def num_de(self):
        """
        Number of disentanglers.
        """
        return self.de_sites.shape[0]

    @property
    def num_sites(self):
        """Number of sites property"""
        return self._num_sites

    @property
    def local_dim(self):
        """Local dimension property"""
        return self._local_dim

    @property
    def convergence_parameters(self):
        """Get the convergence settings."""
        return self._convergence_parameters

    @convergence_parameters.setter
    def convergence_parameters(self, value):
        """
        Set the convergence settings from the TN. (no immediate effect, only
        in next steps).
        """
        self._convergence_parameters = value

    @property
    def check_unitarity(self):
        """Flag to check if disentanglers are unitaries."""
        return self._check_unitarity

    def check_if_de_eligible(self, tensor):
        """
        Makes several checks and raises an exception if a tensor is
        not eligible for a disentangler.
        """
        if len(tensor.elem.shape) != 4:
            raise Exception("Disentangler must be a rank-4 tensor.")
        if self.check_unitarity:
            tensor.assert_unitary([2, 3])

        return tensor

    def __setitem__(self, index, elem):
        """Overwriting setting items."""
        super().__setitem__(index, self.check_if_de_eligible(elem))

    def insert(self, index, elem):
        """Overwriting inserting an item."""
        super().insert(index, self.check_if_de_eligible(elem))
        if len(self) > self.num_de:
            raise Exception(
                "Cannot add more disentanglers than specified in positions."
            )

    def append(self, elem):
        """Overwriting appending an item."""
        super().append(self.check_if_de_eligible(elem))
        if len(self) > self.num_de:
            raise Exception(
                "Cannot add more disentanglers than specified in positions."
            )

    def extend(self, other):
        """Overwriting extending a list."""
        for elem in other:
            _ = self.check_if_de_eligible(elem)
        super().extend(other)
        if len(self) > self.num_de:
            raise Exception(
                "Cannot add more disentanglers than specified in positions."
            )

    def to_dense_mpo(self, de_ind, tensor_backend):
        """
        Splits the chosen disentangler into left and right operator and
        stores them as a dense MPO.

        Parameters
        ----------
        de_ind : int
            Index of disentangler which we want to store as dense MPO.
        tensor_backend: `TensorBackend`
            Tensor backend of the simulation.

        Return
        ------
        dense_de : `DenseMPO`
            Dense MPO with left and right disentangler as terms.
        """
        de_sites = self.de_sites[de_ind]
        de_tensor = self[de_ind].copy()
        de_tensor.attach_dummy_link(0)
        de_tensor.attach_dummy_link(5)

        de_left, de_right = de_tensor.split_qr(
            legs_left=[0, 1, 3], legs_right=[2, 4, 5]
        )

        # first must transform the DE tensors into operators
        op_dict = TNOperators()
        key_left = str(id(de_left))
        key_right = str(id(de_right))
        op_dict.ops[key_left] = de_left
        op_dict.ops[key_right] = de_right

        # store the operators as MPOSites
        dense_de_left = MPOSite(
            de_sites[0], key_left, None, 1.0, operators=op_dict, params={}
        )
        dense_de_right = MPOSite(
            de_sites[1], key_right, None, 1.0, operators=op_dict, params={}
        )
        # put them in the DenseMPO
        dense_de = DenseMPO(
            [dense_de_left, dense_de_right], tensor_backend=tensor_backend
        )

        return dense_de

    def contract_de_layer(self, itpo, tensor_backend, params=None):
        """
        Contracts the disentangler layer with a given iTPO. The procedure
        contracts the itpo between DE layer and DE^dag layer as a sandwich:

         (DE layer)
             |
           (iTPO)
             |
        (DE^dag layer)

        Parameters
        ----------
        itpo : `ITPO`
            iTPO which is to be contracted with the DE layer
        tensor_backend: `TensorBackend`
            Tensor backend of the simulation.
        params : dict or None, optional
            The parameters passed from the simulation. In particular,
            not needed here.
            Default to None.

        Return
        ------
        contracted_itpo : `ITPO`
            iTPO resulting from contracting itpo with DE layer.

        """
        if self.num_sites != itpo.num_sites:
            raise ValueError(
                f"Cannot contract disentangler layer of {self.num_sites}"
                f"-site system with iTPO of {itpo.num_sites}-system."
            )
        # for simplicity of implementation, first get dense mpo list out of iTPO
        dense_mpo_list = itpo.to_dense_mpo_list(params)

        contracted_dense_mpo_list = DenseMPOList()
        # loop over dense mpo terms and if they overlap with the disentangler
        # contract them appropriately
        for dense_mpo in dense_mpo_list:
            # iterate over disentanglers to check if there is overlap
            for ii in range(self.num_de):
                if len(set(self.de_sites[ii]).intersection(set(dense_mpo.sites))) != 0:
                    dense_mpo = self.apply_de_to_dense_mpo(
                        de_ind=ii, dense_mpo=dense_mpo, tensor_backend=tensor_backend
                    )

            contracted_dense_mpo_list.append(dense_mpo)

        # convert back to iTPO
        contracted_itpo = ITPO(num_sites=self.num_sites)
        contracted_itpo.add_dense_mpo_list(contracted_dense_mpo_list)

        return contracted_itpo

    # pylint: disable-next=too-many-locals
    def apply_de_to_dense_mpo(self, de_ind, dense_mpo, tensor_backend):
        """
        Contracts DE and DE^dag with a given dense MPO. Since there could be
        the sites which are in mpo, but not in DE (and vice versa), the
        function takes care to insert identity operators on appropriate places.

        Parameters
        ----------
        de_ind : int
            Index of disentangler which we want to contract with mpo.
        dense_mpo : `DenseMPO`
            Dense MPO to be contracted with disentangler.
        tensor_backend: `TensorBackend`
            Tensor backend of the simulation.

        Return
        ------
        contracted_dense_mpo : `DenseMPO`
            Dense MPO contracted with disentangler.
        Don't forget the truncation. Raise a warning if truncating.
        """
        de_sites = self.de_sites[de_ind]
        mpo_sites = dense_mpo.sites
        # extra_de = list(set(mpo_sites) - set(de_sites))[0]
        for ii in list(set(de_sites) - set(mpo_sites)):
            link = self[de_ind].links[0] if ii == de_sites[0] else self[de_ind].links[1]
            dense_mpo.add_identity_on_site(ii, link)

        dense_de = self.to_dense_mpo(de_ind, tensor_backend)

        i1 = None
        i2 = None

        # Contract upper DE
        for ii, site in enumerate(dense_mpo.sites):
            if site == dense_de.sites[0]:
                # First contraction
                i1 = ii
                ctens = dense_mpo[ii].operator.tensordot(
                    dense_de[0].operator, ([2], [1])
                )

                # Legs are: left, to-bra, right-mpo, left, to-ket, right-de
                ctens.remove_dummy_link(3)
                qtens, rtens = ctens.split_qr([0, 1, 3], [2, 4])

                dense_mpo[ii].operator = qtens

            elif site == dense_de.sites[1]:
                # Last contraction
                i2 = ii
                ctens = rtens.tensordot(dense_mpo[ii].operator, ([1], [0]))
                # legs are : left-mpo, right-de, bra, ket, right-mpo

                ctens = ctens.tensordot(dense_de[1].operator, ([1, 3], [0, 1]))
                # legs are: left-mpo, bra, right-mpo, ket, right-de

                ctens.remove_dummy_link(4)
                ctens.transpose_update([0, 1, 3, 2])

                dense_mpo[ii].operator = ctens

                break

            elif site > dense_de.sites[0]:
                # Propagate
                ctens = rtens.tensordot(dense_mpo[ii].operator, ([1], [0]))
                qtens, rtens = ctens.split_qr([0, 2, 3], [4, 1])

                dense_mpo[ii].operator = qtens

        # Contract lower DE (conjg(DE))
        for ii, site in enumerate(dense_mpo.sites):
            if site == dense_de.sites[0]:
                # First contraction
                de_conj = dense_de[0].operator.conj()
                ctens = dense_mpo[ii].operator.tensordot(de_conj, ([1], [2]))

                # Legs are: left, to-ket, right-mpo, left, to-bra, right-de
                ctens.remove_dummy_link(3)
                qtens, rtens = ctens.split_qr([0, 3, 1], [2, 4])

                dense_mpo[ii].operator = qtens

            elif site == dense_de.sites[1]:
                # Last contraction
                ctens = rtens.tensordot(dense_mpo[ii].operator, ([1], [0]))
                # legs are : left-mpo, right-de, bra, ket, right-mpo

                de_conj = dense_de[1].operator.conj()
                ctens = ctens.tensordot(de_conj, ([1, 2], [0, 2]))
                # legs are: left-mpo, ket, right-mpo, bra, right-de

                ctens.remove_dummy_link(4)
                ctens.transpose_update([0, 3, 1, 2])

                dense_mpo[ii].operator = ctens

                break

            elif site > dense_de.sites[0]:
                # Propagate
                ctens = rtens.tensordot(dense_mpo[ii].operator, ([1], [0]))
                qtens, rtens = ctens.split_qr([0, 2, 3], [4, 1])

                dense_mpo[ii].operator = qtens

        # create new convergence parameters for dense_mpo compression
        precision = dense_mpo[0].operator.dtype_eps
        conv_params_de = TNConvergenceParameters(
            max_bond_dimension=int(self.local_dim[0] ** self.num_sites),
            cut_ratio=10 * precision,
            trunc_method="N",
        )
        # compress dense_mpo
        trunc = True
        if trunc:
            warn(
                "Possibly truncating the disentangler, i.e. changing the Hamiltonian"
                " for the measurements."
            )
        dense_mpo.compress_links(i2, i1, trunc=trunc, conv_params=conv_params_de)

        return dense_mpo
