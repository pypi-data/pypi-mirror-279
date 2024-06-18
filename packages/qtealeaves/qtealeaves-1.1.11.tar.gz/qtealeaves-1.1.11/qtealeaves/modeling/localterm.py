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
Local terms in a Hamiltonian or Lindblad equation.
"""
from copy import deepcopy
import numpy as np

from qtealeaves import map_selector
from .baseterm import _ModelTerm


__all__ = ["LocalTerm", "LindbladTerm", "RandomizedLocalTerm"]


class LocalTerm(_ModelTerm):
    """
    Local Hamiltonian terms are versatile and probably part of any model
    which will be implemented. For example, the external field in the
    quantum Ising model can be represented as a local term.

    **Arguments**

    operator : str
        String identifier for the operator. Before launching the simulation,
        the python API will check that the operator is defined.

    strength : str, callable, numeric (optional)
        Defines the coupling strength of the local terms. It can
        be parameterized via a value in the dictionary for the
        simulation or a function.
        Default to 1.

    prefactor : numeric, scalar (optional)
        Scalar prefactor, e.g., in order to take into account signs etc.
        Default to 1.

    mask : callable or ``None``, optional
        The true-false-mask allows to apply the local Hamiltonians
        only to specific sites, i.e., with true values. The function
        takes the dictionary with the simulation parameters as an
        argument.
        Default to ``None`` (all sites have a local term)

    **Attributes**

    map_type : str, optional
        Selecting the mapping from a n-dimensional system to the
        1d system required for the TTN simulations.
    """

    def __init__(self, operator, strength=1, prefactor=1, mask=None):
        super().__init__()

        self.operator = operator
        self.strength = strength
        self.prefactor = prefactor
        self.mask = mask

        # Will be set when adding Hamiltonian terms
        self.map_type = None

    def count(self, params):
        """
        Defines length as number of terms in fortran input file,
        which by now depends the presence of a mask.

        **Arguments**

        params : dictionary
            Contains the simulation parameters.
        """
        if self.mask is None:
            return 1

        return np.sum(self.mask(params))

    def get_entries(self, params):
        """
        Return the operator and the strength of this term.

        **Arguments**

        params : dictionary
            Contains the simulation parameters.
        """
        strength = self.eval_strength(params)

        return self.operator, strength

    def collect_operators(self):
        """
        The required operators must be provided through this
        method; thus, we return the operator in the local term.
        """
        yield self.operator, None

    def get_fortran_str(self, ll, params, operator_map, param_map, dim):
        """
        Get the string representation needed to write the
        local terms as an plocal_type for Fortran.

        **Arguments**

        ll : int
            Number of sites along the dimensions, i.e., not the
            total number of sites. Assuming list of sites
            along all dimension.

        params : dictionary
            Contains the simulation parameters.

        operator_map : OrderedDict
            For operator string as dictionary keys, it returns the
            corresponding integer IDs.

        param_map : dict
            This dictionary contains the mapping from the parameters
            to integer identifiers.

        dim : int
            Dimensionality of the problem, e.g., a 2d system.
        """
        str_repr = ""
        op_id_str = str(operator_map[(self.operator, None)])

        has_spatial_dependency = False
        param_repr = self.get_param_repr(param_map)

        if self.mask is not None:
            for _, idx in self.get_interactions(ll, params, dim=dim):
                # Convert from python index to fortran index by
                # adding offset 1
                str_repr += "%d\n" % (idx[0] + 1)
                str_repr += op_id_str + "\n"
                str_repr += param_repr
                str_repr += "%30.15E\n" % (self.prefactor)

        elif has_spatial_dependency:
            # Write for each site
            raise NotImplementedError("To-do ...")
        else:
            str_repr += "-1\n"
            str_repr += op_id_str + "\n"
            str_repr += param_repr
            str_repr += "%30.15E\n" % (self.prefactor)

        return str_repr

    def get_interactions(self, ll, params, **kwargs):
        """
        Iterator returning the local terms one-by-one, e.g., to build
        a Hamiltonian matrix. (In that sense, the "interaction" is
        obviously misleading here.)

        **Arguments**

        ll : int
            Number of sites along the dimension, i.e., not the
            total number of sites. Assuming list of sites
            along all dimension.

        params : dictionary
            Contains the simulation parameters.

        dim : int (as keyword argument!)
            Dimensionality of the problem, e.g., a 2d system.
        """
        if "dim" not in kwargs:
            raise Exception("Local terms needs dim information")
        dim = kwargs["dim"]

        elem = {"coordinates": None, "operators": [self.operator]}

        if self.mask is None:

            def check_mask(*args):
                return True

        else:
            local_mask = self.mask(params)
            if len(local_mask.shape) != dim:
                raise Exception("Mask dimension does not match system dimension.")

            def check_mask(*args, local_mask=local_mask):
                if len(args) == 1:
                    return local_mask[args[0]]
                if len(args) == 2:
                    return local_mask[args[0], args[1]]
                if len(args) == 3:
                    return local_mask[args[0], args[1], args[2]]

                raise Exception("Unknown length of *args.")

        if dim > 1:
            map_to_1d = map_selector(dim, ll, self.map_type)

        if dim == 1:
            for ii in range(ll[0]):
                if not check_mask(ii):
                    continue

                elem_ii = deepcopy(elem)
                elem_ii["coordinates_nd"] = (ii,)

                yield elem_ii, [ii]
        elif dim == 2:
            idx = 0
            for ii in range(ll[0]):
                for jj in range(ll[1]):
                    idx += 1

                    if not check_mask(ii, jj):
                        continue

                    elem_ii = deepcopy(elem)
                    elem_ii["coordinates_nd"] = (ii, jj)

                    yield elem_ii, [map_to_1d[(ii, jj)]]
        elif dim == 3:
            idx = 0
            for ii in range(ll[0]):
                for jj in range(ll[1]):
                    for kk in range(ll[2]):
                        idx += 1

                        if not check_mask(ii, jj, kk):
                            continue

                        elem_ii = deepcopy(elem)
                        elem_ii["coordinates_nd"] = (ii, jj, kk)

                        yield elem_ii, [map_to_1d[(ii, jj, kk)]]
        else:
            raise Exception("Dimension unknown.")

        return

    def get_sparse_matrix_operators(
        self, ll, params, operator_map, param_map, sp_ops_cls, **kwargs
    ):
        """
        Construct the sparse matrix operator for this term.

        **Arguments**

        ll : int
            System size.

        params : dictionary
            Contains the simulation parameters.

        operator_map : OrderedDict
            For operator string as dictionary keys, it returns the
            corresponding integer IDs.

        param_map : dict
            This dictionary contains the mapping from the parameters
            to integer identifiers.

        sp_ops_cls : callable (e.g., constructor)
            Constructor for the sparse MPO operator to be built
            Has input bool (is_first_site), bool (is_last_site),
            bool (do_vectors).

        kwargs : keyword arguments
            Keyword arguments are passed to `get_interactions`
        """
        op_id = operator_map[(self.operator, None)]
        param_id = self.get_param_repr(param_map)

        sp_mat_ops = []
        for ii in range(np.prod(ll)):
            sp_mat_ops.append(sp_ops_cls(ii == 0, ii + 1 == np.prod(ll), True))

        for _, inds in self.get_interactions(ll, params, **kwargs):
            sp_mat_ops[inds[0]].add_local(op_id, param_id, self.prefactor, self.is_oqs)

        return sp_mat_ops


class LindbladTerm(LocalTerm):
    """
    Local Lindblad operators acting at one site are defined via this
    term. For the arguments see See :class:`LocalTerm.check_dim`.

    **Details**

    The Lindblad equation is implemented as

    .. math::

        \\frac{d}{dt} \\rho = -i [H, \\rho]
           + \\sum \\gamma (L \\rho L^{\\dagger}
           - \\frac{1}{2} \\{ L^{\\dagger} L, \\rho \\})

    """

    @property
    def is_oqs(self):
        """Status flag if term belongs to Hamiltonian or is Lindblad."""
        return True

    def quantum_jump_weight(self, state, operators, quench, time, params):
        """
        Evaluate the unnormalized weight for a jump with this Lindblad term.

        **Arguments**

        state : :class:`_AbstractTN`
            Current quantum state where jump should be applied.

        operators : :class:`TNOperators`
            Operator dictionary of the simulation.

        quench : :class:`DynamicsQuench`
            Current quench to evaluate time-dependent couplings.

        time : float
            Time of the time evolution (accumulated dt)

        params :  dict
            Dictionary with parameters, e.g., to extract parameters which
            are not in quench or to build mask.
        """
        if self.mask is None:
            mask = np.ones(state.num_sites, dtype=bool)
        else:
            mask = self.mask(params)

        mask = mask.astype(int).astype(np.float64)

        if self.strength in quench:
            strength = quench[self.strength](time)
        else:
            strength = self.eval_numeric_param(self.strength, params)

        total_scaling = strength * self.prefactor
        lindblad = operators[self.operator]
        operator = lindblad.conj().tensordot(lindblad, ([0, 1, 3], [0, 1, 3]))
        meas_vec = state.meas_local(operator)

        return np.sum(meas_vec * mask) * total_scaling

    def quantum_jump_apply(self, state, operators, params, rand_generator):
        """
        Apply jump with this Lindblad. Contains inplace update of state.

        **Arguments**

        state : :class:`_AbstractTN`
            Current quantum state where jump should be applied.

        operators : :class:`TNOperators`
            Operator dictionary of the simulation.

        params :  dict
            Dictionary with parameters, e.g., to extract parameters which
            are not in quench or to build mask.

        rand_generator : random number generator
            Needs method `random()`, used to decide on jump within
            the sites.
        """
        if self.mask is None:
            mask = np.ones(state.num_sites, dtype=bool)
        else:
            mask = self.mask(params)

        mask = mask.astype(int).astype(np.float64)

        lindblad = operators[self.operator]
        operator = lindblad.conj().tensordot(lindblad, ([0, 1, 3], [0, 1, 3]))
        meas_vec = state.meas_local(operator)

        meas_vec = meas_vec * mask
        meas_vec = np.cumsum(meas_vec)
        meas_vec /= meas_vec[-1]

        rand = rand_generator.random()

        idx = meas_vec.shape[0] - 1
        for ii in range(idx):
            if rand < meas_vec[ii]:
                idx = ii
                break

        if lindblad.ndim == 4:
            if lindblad.shape[0] == 1 and lindblad.shape[3] == 1:
                lindblad = lindblad.remove_dummy_link(3).remove_dummy_link(0)
            else:
                raise Exception("Cannot remove-non dummy links.")
        elif lindblad.ndim != 2:
            raise Exception("Operator neither rank-2 nor rank-4.")

        state.site_canonize(idx)
        state.apply_one_site_operator(lindblad, idx)
        state.normalize()


class RandomizedLocalTerm(LocalTerm):
    """
    Randomized local Hamiltonian terms are useful to model spinglass systems
    where the coupling of the local term is different for each site.

    **Arguments**

    operator : string
        String identifier for the operators. Before launching the simulation,
        the python API will check that the operator is defined.

    coupling_entries : numpy ndarray of rank-1,2,3
        The coupling for the different sites.
        These values can only be set once and cannot
        be time-dependent in a time-evolution. The rank depends
        on the usage in 1d, 2d, or 3d systems.

    strength : str, callable, numeric (optional)
        Defines the coupling strength of the local terms. It can
        be parameterized via a value in the dictionary for the
        simulation or a function.
        Default to 1.

    prefactor : numeric, scalar (optional)
        Scalar prefactor, e.g., in order to take into account signs etc.
        Default to 1.
    """

    mask = None

    def __init__(self, operator, coupling_entries, strength=1, prefactor=1):
        super().__init__(operator=operator, strength=strength, prefactor=prefactor)
        self.coupling_entries = coupling_entries

    def count(self, params):
        """
        Defines length as number of terms in fortran input file,
        which by now depends the presence of the coupling entries.

        **Arguments**

        params : dictionary
            Contains the simulation parameters.
        """
        ctens = self.eval_numeric_param(self.coupling_entries, params)
        return np.sum(np.abs(ctens) != 0)

    def get_interactions(self, ll, params, **kwargs):
        """
        See :class:`LocalTerm`
        """
        ctens = self.eval_numeric_param(self.coupling_entries, params)

        for elem, coords_1d in super().get_interactions(ll, params, **kwargs):
            elem["weight"] = ctens[elem["coordinates_nd"]]

            if elem["weight"] == 0.0:
                continue

            yield elem, coords_1d

    def get_fortran_str(self, ll, params, operator_map, param_map, dim):
        """
        Get the string representation needed to write the
        local terms as an plocal_type for Fortran.

        **Arguments**

        ll : int
            Number of sites along one dimension, i.e., not the
            total number of sites. Assuming equal number of sites
            along all dimension.

        params : dictionary
            Contains the simulation parameters.

        operator_map : OrderedDict
            For operator string as dictionary keys, it returns the
            corresponding integer IDs.

        param_map : dict
            This dictionary contains the mapping from the parameters
            to integer identifiers.

        dim : int
            Dimensionality of the problem, e.g., a 2d system.
        """
        str_repr = ""
        op_id_str = str(operator_map[(self.operator, None)])

        param_repr = self.get_param_repr(param_map)

        ctens = self.eval_numeric_param(self.coupling_entries, params)
        if isinstance(ctens, np.ndarray):
            if len(ctens.shape) != dim:
                raise Exception(
                    "Coupling %d and " % (len(ctens.shape))
                    + "dimensionality %d do not match." % (dim)
                )
        else:
            raise Exception("Unknown type for coupling.")

        for meta_info, idx in self.get_interactions(ll, params, dim=dim):
            if abs(ctens[meta_info["coordinates_nd"]]) == 0.0:
                # Skip entries with 0 coupling from randomization
                continue

            # Convert from python index to fortran index by
            # adding offset 1
            str_repr += "%d\n" % (idx[0] + 1)
            str_repr += op_id_str + "\n"
            str_repr += param_repr
            prefactor = self.prefactor * ctens[meta_info["coordinates_nd"]]
            str_repr += "%30.15E\n" % (prefactor)

        return str_repr
