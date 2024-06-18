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
Dense Matrix Product Operators representing Hamiltonians.
"""
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from copy import deepcopy
import warnings
import numpy as np

from qtealeaves.tooling import _ParameterizedClass
from qtealeaves.tooling.restrictedclasses import _RestrictedList
from qtealeaves.tensors import TensorBackend
from qtealeaves.operators import TNOperators


__all__ = ["MPOSite", "DenseMPO", "DenseMPOList"]


class MPOSite(_ParameterizedClass):
    """
    One site in a dense MPO term.

    **Arguments**

    site : integer
        Site index.

    str_op : str
        Key for the operator.

    pstrength : pstrength, callable, numeric
        Containing the parameterization of the term.

    weight : scalar
        Scalar constant prefactor.

    operators : :class:`TNOperators` or None
        If present, operators will be directly extracted.

    params : dict or None
        If present, parameterization will be directly extracted.
    """

    def __init__(self, site, str_op, pstrength, weight, operators=None, params=None):
        self.site = site
        self.str_op = str_op
        self.pstrength = pstrength

        self.operator = (
            None if operators is None else deepcopy(operators[(site, str_op)])
        )
        self.strength = (
            None if params is None else self.eval_numeric_param(self.pstrength, params)
        )
        if self.pstrength is None:
            self.strength = 1.0
        self.weight = weight

    @property
    def total_scaling(self):
        """Returns the scaling combining params and weight."""
        return self.strength * self.weight

    def copy_with_new_op(self, operator):
        """
        Create a copy of self, but without replacing the operator with the one passed.
        Corresponding string identifier will be set to `None`.
        """
        obj = deepcopy(self)
        obj.operator = operator
        obj.str_op = None

        return obj

    def initialize(self, operators, params):
        """Resolve operators and parameterization for the given input."""
        self.set_op(operators)
        self.set_param(params)

    def set_op(self, operators):
        """Resolve operators for the given input."""
        if self.str_op is None:
            raise Exception("Operator string no longer available.")
        self.operator = operators[(self.site, self.str_op)]

    def set_param(self, params):
        """Resolve parameterization for the given input."""
        if self.pstrength is None:
            self.strength = 1.0
            return

        strength = self.eval_numeric_param(self.pstrength, params)

        if hasattr(strength, "__len__"):
            raise Exception("Strength cannot be a list.")

        if strength == 0.0:
            warnings.warn("Adding term with zero-coupling.")

        self.strength = strength


class DenseMPO(_RestrictedList):
    """Dense MPO as a list of :class:`MPOSite's."""

    class_allowed = MPOSite

    def __init__(self, *args, is_oqs=False, tensor_backend=TensorBackend()):
        super().__init__(*args)
        self.is_oqs = is_oqs
        self.tensor_backend = tensor_backend

    @property
    def sites(self):
        """Generate list of site indices."""
        sites = [elem.site for elem in self]
        return sites

    def compress_links(self, idx_start, idx_end, trunc=False, conv_params=None):
        """
        Compresses links between sites in a dense MPO by performing a QR or SVD,
        optionally performs the additional truncation along the way.

        Parameters
        ----------
        idx_start : int
            MPO site from which to start the compression.

        idx_end : int
            MPO site on which to end the compression.

        trunc : Boolean, optional
            If True, the truncation will be done according to the `conv_params`.
            Default to False.

        conv_params : :py:class:`TNConvergenceParameters`, optional
            Convergence parameters for the truncation. Must be specified if
            `trunc` is set to True.
            Default to `None`.
        """
        stride = 1 if idx_start < idx_end else -1

        if trunc and conv_params is None:
            raise Exception(
                "Cannot truncate without the convergence parameters specified."
            )

        if stride == 1:
            for ii in range(idx_start, idx_end):
                shape = self[ii].operator.shape
                dim1 = np.prod(shape[:3])
                dim2 = shape[3]

                if (dim2 > dim1) and (not trunc):
                    qtens, rtens = self[ii].operator.split_qr([0, 1, 2], [3])
                    self[ii].operator = qtens
                    self[ii + 1].operator = rtens.tensordot(
                        self[ii + 1].operator, ([1], [0])
                    )
                elif dim2 > dim1:
                    qtens, rtens, _, _ = self[ii].operator.split_svd(
                        [0, 1, 2], [3], contract_singvals="R", conv_params=conv_params
                    )
                    self[ii].operator = qtens
                    self[ii + 1].operator = rtens.tensordot(
                        self[ii + 1].operator, ([1], [0])
                    )

        else:
            for ii in range(idx_start, idx_end, stride):
                shape = self[ii].operator.shape
                dim1 = np.prod(shape[1:])
                dim2 = shape[0]

                if (dim2 > dim1) and (not trunc):
                    qtens, rtens = self[ii].operator.split_qr(
                        [1, 2, 3], [0], perm_left=[3, 0, 1, 2]
                    )
                    self[ii].operator = qtens
                    self[ii - 1].operator = self[ii - 1].operator.tensordot(
                        rtens, ([3], [1])
                    )
                elif dim2 > dim1:
                    qtens, rtens, _, _ = self[ii].operator.split_svd(
                        [1, 2, 3],
                        [0],
                        perm_left=[3, 0, 1, 2],
                        contract_singvals="L",
                        conv_params=conv_params,
                    )
                    self[ii].operator = qtens
                    self[ii - 1].operator = self[ii - 1].operator.tensordot(
                        rtens, ([3], [1])
                    )

    def add_identity_on_site(self, idx, link_vertical):
        """
        Add identity with the correct links to neighboring terms on site `idx`.

        Parameters
        ----------
        idx : int
            Site to which add the identity. Goes from 0 to num sites in a system.

        link_vertical : link as returned by corresponding QteaTensor
            Needed to build the local Hilbert space (in case it is different across
            the system).
        """
        if len(self) == 0:
            raise Exception("Cannot use `add_identity_on_site` on empty DenseMPO.")

        sites = np.array(self.sites)
        if np.any(sites[1:] - sites[:-1] <= 0):
            raise Exception("Cannot use `add_identity_on_site` on unsorted DenseMPO.")

        if idx in self.sites:
            raise Exception("Site is already in DenseMPO.")

        sites = np.array(self.sites + [idx])
        inds = list(np.argsort(sites))

        # Index of terms on the left (even 0 works as there a periodic boundary
        # conditions for contracting links in the DenseMPO)
        left = inds[-1] - 1

        op = self[left].operator
        if op is None:
            raise Exception(
                "Cannot use `add_identity_on_site` on uninitialized DenseMPO."
            )

        eye_horizontal = op.eye_like(op.links[3])
        eye_vertical = op.eye_like(link_vertical)

        # Contract together
        eye_horizontal.attach_dummy_link(0, False)
        eye_vertical.attach_dummy_link(0, True)

        eye = eye_horizontal.tensordot(eye_vertical, ([0], [0]))
        eye.transpose_update([0, 2, 3, 1])

        key = str(id(eye))
        op_dict = TNOperators()
        op_dict.ops[key] = eye

        # add it to the correct site
        site = MPOSite(idx, key, None, 1.0, operators=op_dict, params={})

        insert_ind = np.argsort(inds)[-1]
        self.insert(insert_ind, site)

    def initialize(self, operators, params):
        """Resolve operators and parameterization for the given input for each site."""
        for elem in self:
            elem.initialize(operators, params)

    def sort_sites(self):
        """Sort sites while and install matching link for symmetries."""
        sites = [elem.site for elem in self]
        inds = np.argsort(sites)

        dims_l = [elem.operator.shape[0] for elem in self]
        dims_r = [elem.operator.shape[3] for elem in self]

        max_l = np.max(dims_l)
        max_r = np.max(dims_r)

        max_chi = max(max_l, max_r)

        if max_chi == 1:
            return self._sort_sites_chi_one(inds)

        raise Exception("For now, we only sort product terms.")

    def pad_identities(self, num_sites, eye_ops):
        """Pad identities on sites which are not in MPO yet respecting the symmetry."""
        sites = np.array([elem.site for elem in self])
        if np.any(sites[1:] - sites[:-1] < 1):
            sorted_mpo = self.sort_sites()
            return sorted_mpo.pad_identities(num_sites, eye_ops)

        raise Exception("Not implemtented yet.")

    def _sort_sites_chi_one(self, inds):
        """Sorting sites in the case of bond dimension equal to one."""
        new_mpo = DenseMPO(is_oqs=self.is_oqs, tensor_backend=self.tensor_backend)
        new_mpo.append(self[inds[0]])

        for ii in inds[1:]:
            link = new_mpo[-1].operator.links[-1]

            # Trivial tensor porting the sector
            one = self.tensor_backend.tensor_cls(
                [link, link],
                ctrl="O",
                are_links_outgoing=[False, True],
                **self.tensor_backend.tensor_cls_kwargs(),
            )
            one.attach_dummy_link(2, True)

            tens = one.tensordot(self[ii].operator, ([2], [0]))

            # We have five links [left, right-1, bra, ket, right-2]
            tens.transpose_update([0, 2, 3, 1, 4])
            tens.fuse_links_update(3, 4)

            mpo_site = self[ii].copy_with_new_op(tens)
            new_mpo.append(mpo_site)

        # Check that MPO does conserve symmetry
        if not self.is_oqs:
            new_mpo[-1].operator.assert_identical_irrep(3)

        return new_mpo

    @classmethod
    def from_matrix(
        cls,
        matrix,
        sites,
        dim,
        conv_params,
        tensor_backend=TensorBackend(),
        operators=TNOperators(),
    ):
        """
        For a given matrix returns dense MPO form decomposing with SVDs

        Parameters
        ----------
        matrix : QteaTensor | ndarray
            Matrix to write in (MPO) format
        sites : List[int]
            Sites to which the MPO is applied
        dim : int
            Local Hilbert space dimension
        conv_params : :py:class:`TNConvergenceParameters`
            Input for handling convergence parameters.
            In particular, in the LPTN simulator we
            are interested in:
            - the maximum bond dimension (max_bond_dimension)
            - the cut ratio (cut_ratio) after which the
            singular values in SVD are neglected, all
            singular values such that
            :math:`\\lambda` /:math:`\\lambda_max`
            <= :math:`\\epsilon` are truncated
        tensor_backend : instance of :class:`TensorBackend`
            Default for `None` is :class:`QteaTensor` with np.complex128 on CPU.

        Return
        ------
        DenseMPO
            The MPO decomposition of the matrix
        """

        if not isinstance(matrix, tensor_backend.tensor_cls):
            matrix = tensor_backend.tensor_cls.from_elem_array(matrix)

        mpo = cls(tensor_backend=tensor_backend)
        bond_dim = 1
        names = []
        work = matrix
        for ii, site in enumerate(sites[:-1]):
            #                dim  dim**(n_sites-1)
            #  |                 ||
            #  O  --[unfuse]-->  O   --[fuse upper and lower legs]-->
            #  |                 ||
            #
            # ==O==  --[SVD, truncating]-->  ==O-o-O==
            #
            #                 | |
            #  --[unfuse]-->  O-O           ---iterate
            #                 | |
            #             dim   dim**(n_sites-1)
            work = np.reshape(
                work,
                (
                    bond_dim,
                    dim,
                    dim ** (len(sites) - 1 - ii),
                    dim,
                    dim ** (len(sites) - 1 - ii),
                ),
            )
            tens_left, work, _, _ = work.split_svd(
                [0, 1, 3], [2, 4], contract_singvals="R", conv_params=conv_params
            )
            bond_dim = deepcopy(work.shape[0])
            operators.ops[(site, f"mpo{ii}")] = tens_left
            names.append((site, f"mpo{ii}"))

        work = work.reshape((work.shape[0], dim, dim, 1))
        operators.ops[(sites[-1], f"mpo{len(sites)-1}")] = work
        names.append((sites[-1], f"mpo{len(sites)-1}"))

        for site, name in zip(sites, names):
            mpo.append(MPOSite(site, name, 1, 1, operators=operators))

        return mpo


class DenseMPOList(_RestrictedList):
    """Collection of dense MPOs, i.e., for building iTPOs or other MPOs."""

    class_allowed = DenseMPO

    @property
    def has_oqs(self):
        """Return flag if the `DenseMPOList` contains any open system term."""
        has_oqs = False
        for elem in self:
            print("elem.is_oqs", has_oqs, elem.is_oqs)
            has_oqs = has_oqs or elem.is_oqs

        return has_oqs

    @classmethod
    def from_model(cls, model, params, tensor_backend=TensorBackend()):
        """Fill class with :class:`QuantumModel` and its parameters."""
        obj = cls()

        lx_ly_lz = model.eval_lvals(params)
        for term in model.hterms:
            for elem, coords in term.get_interactions(lx_ly_lz, params, dim=model.dim):
                weight = term.prefactor
                if "weight" in elem:
                    weight *= elem["weight"]

                pstrength = term.strength
                mpo = DenseMPO(is_oqs=term.is_oqs, tensor_backend=tensor_backend)

                for idx, coord in enumerate(coords):
                    site_term = MPOSite(
                        coord, elem["operators"][idx], pstrength, weight
                    )
                    mpo.append(site_term)

                    # Only needed on first site
                    pstrength = None
                    weight = 1.0

                obj.append(mpo)

        return obj

    def initialize(self, operators, params, do_sort=True):
        """Resolve operators and parameterization for the given input."""
        for elem in self:
            elem.initialize(operators, params)

        if do_sort:
            mpos_sorted = self.sort_sites()

            for ii, elem in enumerate(mpos_sorted):
                self[ii] = elem

    def sort_sites(self):
        """Sort the sites in each :class:`DenseMPO`."""
        mpos_sorted = DenseMPOList()

        for elem in self:
            elem_sorted = elem.sort_sites()
            mpos_sorted.append(elem_sorted)

        return mpos_sorted
