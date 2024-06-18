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
Indexed tensor product operators for Hamiltonians or measurements.
"""

# pylint: disable=protected-access
# pylint: disable=too-many-lines
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

from copy import deepcopy
import warnings
import numpy as np

from qtealeaves.tooling import _ParameterizedClass
from qtealeaves.tooling.restrictedclasses import _RestrictedList
from qtealeaves.tooling.permutations import _transpose_idx
from qtealeaves.tensors import _AbstractQteaTensor, TensorBackend
from qtealeaves.operators import TNOperators

from .abstracteffop import _AbstractEffectiveOperators
from .densempos import MPOSite, DenseMPO, DenseMPOList

__all__ = ["ITPOTerm", "ITPOSites", "ITPO"]


class ITPOTerm(_ParameterizedClass):
    """Single iTPO term either for Hamiltonian or inside effective operators."""

    def __init__(self, do_indexing=True, enable_update=False):
        self._tensors = {}
        self._operators = {}
        self._link_inds = {}
        self._weights = {}
        self._local = None

        # Needed for measurements
        self._measurement_setup = False
        self._meas_vec = None

        # Needed for time evolution update mode
        self._enable_update = enable_update
        self._cache_update = {}

        # Needed to update while skipping contractions
        # --------------------------------------------

        # Keys are TPO IDs, values are scalars
        self._prefactor = {}

        # Keys are TPO IDs, values are something parameterized (scalar, callable, str)
        self._pstrength = {}

        self._local_ops = []
        self._local_prefactors = []
        self._local_pstrengths = []
        self._local_oqs = []

        # internal flag to allow TPO without indexing
        self._do_indexing = do_indexing

        # tracker for computational effort
        self._contraction_counter = 0

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def device(self):
        """Device where the tensor is stored."""
        for _, elem in self._tensors.items():
            return elem.device

        if self._local is not None:
            return self._local.device

        raise Exception("Running inquiery on empty iTPOTerm.")

    @property
    def enable_update(self):
        """Property if update of time-dependent couplings is enabled."""
        return self._enable_update

    @enable_update.setter
    def enable_update(self, value):
        """Setter for property if update of time-dependent couplings is enabled."""
        self._enable_update = value

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        for _, elem in self._tensors.items():
            return elem.dtype

        if self._local is not None:
            return self._local.dtype

        raise Exception("Running inquiery on empty iTPOTerm.")

    @property
    def idx_eye(self):
        """By convention, we will set the "eye" tensor at key -2."""
        return -2

    @property
    def has_oqs(self):
        """Return flag if the iTPOTerm contains any open system term."""
        has_oqs = False
        for has_oqs_ii in self._local_oqs:
            has_oqs = has_oqs or has_oqs_ii

        return has_oqs

    # --------------------------------------------------------------------------
    #                              classmethod, classmethod-like
    # --------------------------------------------------------------------------

    def empty_copy(self, other=None, do_copy_meas_vec=False):
        """Make a copy of the settings of a term without entries."""
        measurement_setup = self._measurement_setup
        if other is not None:
            measurement_setup = measurement_setup or other._measurement_setup

        obj = ITPOTerm(do_indexing=self._do_indexing, enable_update=self._enable_update)
        obj.set_meas_status(measurement_setup)

        if do_copy_meas_vec:
            obj._transfer_entries_measurement(self, other)

        return obj

    # --------------------------------------------------------------------------
    #                                       Methods
    # --------------------------------------------------------------------------

    def convert(self, dtype, device):
        """Convert underlying array to the specified data type inplace."""
        for _, tensor in self._tensors.items():
            tensor.convert(dtype, device)

        if self._local is not None:
            self._local.convert(dtype, device)

    def copy(self):
        """Actual copy of instance."""
        new = ITPOTerm()

        for key, value in self._tensors.items():
            new._tensors[key] = value.copy()

        new._operators = deepcopy(self._operators)
        new._link_inds = deepcopy(self._link_inds)
        new._weights = deepcopy(self._weights)
        new._local = deepcopy(self._local)

        # Needed for measurements
        new._measurement_setup = deepcopy(self._measurement_setup)
        new._meas_vec = deepcopy(self._meas_vec)

        # Need to update while skipping contractions
        new._prefactor = deepcopy(self._prefactor)
        new._pstrength = deepcopy(self._pstrength)
        new._local_ops = deepcopy(self._local_ops)
        new._local_prefactors = deepcopy(self._local_prefactors)
        new._local_pstrengths = deepcopy(self._local_pstrengths)

        # internal flag to allow TPO without indexing
        new._do_indexing = deepcopy(self._do_indexing)

        new._enable_update = deepcopy(self._enable_update)
        new._cache_update = deepcopy(self._cache_update)

        # tracker for computational effort
        new._contraction_counter = deepcopy(self._contraction_counter)

        return new

    def delete_or_cache_tensors(self, inds):
        """Delete or cache entries (used to remove terms which contracted to local."""
        for idx in inds:
            if self._enable_update:
                self._cache_update[idx] = self._tensors[idx]

            del self._tensors[idx]

    def get_max_tpo_id(self):
        """Get maximum TPO ID in this term."""
        max_tpo_id = -1
        for key in self._link_inds:
            max_tpo_id = max(max_tpo_id, key)

        return max_tpo_id

    def iter_tpo_ids(self):
        """Iterator over all TPO IDs present."""
        for key in self._link_inds:
            yield key

    def sanity_check(self):
        """Quick set of checks that the iTPOTerm fulfills certain criteria."""
        tensor = None
        for key, elem in self._tensors.items():
            tensor = elem

        if tensor is not None:
            for key, elem in self._tensors.items():
                if tensor.ndim != elem.ndim:
                    print("Error information", key, elem.shape, tensor.shape)
                    raise Exception("iTPO contains tensors of different rank.")

            if self._local is not None:
                if tensor.ndim - 2 != self._local.ndim:
                    print("Error information", key, self._local.shape, tensor.shape)
                    raise Exception("iTPO mismatch in rank of local.")

    def set_meas_status(self, do_measurement):
        """Set the measurement status of this iTPOTerm."""
        if do_measurement:
            self._measurement_setup = True
            self._meas_vec = {}
        else:
            self._measurement_setup = False
            self._meas_vec = None

    def update_couplings(self, params):
        """Update the coupling with a new params dictionary."""
        # Update couplings in TPO terms
        for key, value in self._pstrength.items():
            strength = self.eval_numeric_param(value, params)
            prefactor = self._prefactor[key]

            total_scaling = 1.0
            if strength is not None:
                total_scaling *= strength

            if prefactor is not None:
                total_scaling *= prefactor

            self._weights[key] = total_scaling

        # Update couplings in local terms
        self._local = None
        for ii, tensor in enumerate(self._local_ops):
            strength = self.eval_numeric_param(self._local_pstrengths[ii], params)
            prefactor = self._local_prefactors[ii]

            total_scaling = 1.0
            if strength is not None:
                total_scaling *= strength

            if prefactor is not None:
                total_scaling *= prefactor

            if self._local_oqs[ii]:
                # The one-half originates from L rho Ldagger - 0.5 {Ldagger L, rho}
                # in the Lindblad equation.
                local = tensor.conj().tensordot(tensor, [(0, 1, 3), (0, 1, 3)])
                local = local * (-0.5j * total_scaling)
            else:
                local = tensor * total_scaling
                local.remove_dummy_link(3)
                local.remove_dummy_link(0)

            if self._local is None:
                self._local = local
            else:
                self._local.add_update(local)

    def add_local(self, operator, prefactor, strength, pstrength, is_oqs):
        """Add a local term to the iTPOTerm when building a Hamiltonian."""

        self._local_ops.append(operator)
        self._local_prefactors.append(prefactor)
        self._local_pstrengths.append(pstrength)
        self._local_oqs.append(is_oqs)

        if strength is None:
            strength = 1.0

        if is_oqs:
            # The initialization is assumed to be for the statics and
            # therefore we do not add the Lindblad terms
            return

        local = operator * (prefactor * strength)
        local.remove_dummy_link(3)
        local.remove_dummy_link(0)

        if self._local is None:
            self._local = local
            return

        self._local.add_update(local)

    def add_term(self, tpo_id, operator, link_inds, prefactor, strength, pstrength):
        """Add an interaction term to the iTPOTerm when building a Hamiltonian."""
        idx_op = self.get_index_operator(operator)

        if tpo_id in self._operators:
            raise Exception("Cannot overwrite term with `add_term`.")

        self._operators[tpo_id] = idx_op
        self._link_inds[tpo_id] = link_inds
        self._weights[tpo_id] = prefactor * strength
        self._prefactor[tpo_id] = prefactor
        self._pstrength[tpo_id] = pstrength

    def collect_measurements(self):
        """Iterator to yield all iTPO-IDs and values of measurements."""
        for key, value in self._meas_vec.items():
            if isinstance(value, _AbstractQteaTensor):
                continue

            yield key, value

    def run_measurements(self, ket, idx_out, link_weights):
        """Run the measurements on the iTPOTerm, i.e., on all stored local tensors."""
        tmp = ket.conj()

        if link_weights is not None:
            link_weights_2 = link_weights**2
            tmp.scale_link_update(link_weights_2, idx_out)

        cidx = list(range(tmp.ndim))

        value_dict = {}
        for key, value in self._meas_vec.items():
            elem = tmp.tensordot(value, (cidx, cidx))
            value_dict[key] = elem.get_entry()

        self._meas_vec = value_dict

    def get_index_operator(self, operator):
        """Get an index for an operator; created if not existing yet."""
        if self._do_indexing:
            for key, tensor in self._tensors.items():
                if operator == tensor:
                    return key

        key = len(self._tensors)
        while key in self._tensors:
            key += 1

        self._tensors[key] = operator

        return key

    def get_index_copy_operator(self, idx):
        """Copy a tensor and return index of copy."""
        key = len(self._tensors)
        while key in self._tensors:
            key += 1
        if key in self._tensors:
            raise Exception("Key not new")
        self._tensors[key] = self._tensors[idx].copy()
        return key

    def _transfer_entries(self, link_inds, weights, operators):
        """Internal function to transfer entries for links, weights, and operators."""
        for key, value in link_inds.items():
            self._link_inds[key] = value
        for key, value in weights.items():
            self._weights[key] = value
        for key, value in operators.items():
            self._operators[key] = value

    def _transfer_entries_measurement(self, other_a, other_b=None):
        if not self._measurement_setup:
            return

        # rint("Transfer meas entries keys", self._meas_vec.keys())
        for key, value in other_a._meas_vec.items():
            if isinstance(value, _AbstractQteaTensor):
                self._meas_vec[key] = value

        if other_b is not None:
            for key, value in other_b._meas_vec.items():
                if isinstance(value, _AbstractQteaTensor):
                    self._meas_vec[key] = value

    def to_str(self, ind_offset=0):
        """String of values that are used for actual simulation."""
        str_buffer = "\n"

        ind0 = " " * ind_offset
        ind4 = " " * (4 + ind_offset)

        if self._local is None:
            str_buffer += ind0 + "No local term."
        else:
            tmp = self._local.flatten()
            if len(tmp) <= 32:
                str_buffer += ind0 + "Local term with " + str(tmp) + "\n"
            else:
                norm = self._local.norm()
                str_buffer += ind0 + "Local's norm is " + str(norm) + "\n"

        for key, weight in self._weights.items():
            op_idx = self._operators[key]
            str_buffer += ind0 + f"TPO ID: {key} with weight {weight}\n"
            tmp = self._tensors[op_idx].flatten()
            if len(tmp) <= 32:
                str_buffer += ind4 + "Tensor is " + str(tmp) + "\n"
            else:
                norm = self._tensors[op_idx].norm()
                str_buffer += ind4 + "Tensor's norm is " + str(norm) + "\n"

        return str_buffer

    def tensordot_with_tensor(
        self, tensor, cidx_self, cidx_tensor, perm_local_out=None, ctens=None
    ):
        """
        Execute contraction of iTPOTerm with tensors. Uncontracted
        non-MPO legs of self go before uncontracted non-MPO legs
        of tensor.

        **Arguments**

        tensor : instance of :class:`_AbstractQteaTensor`
            Tensor in the contraction as right/second tensor.

        cidx_self : list of ints
            Contraction legs for full TPO tensor (local will auto-adapt)

        cidx_tensor : list of ints
            Contraction legs for the `tensor`

        perm_local_out : list of intes
            Permutation of output (full TPO tensor will auto-adapt)

        ctens : `None` or :class:`ITPOTerm`
            If present, update mode is activating which assumes that only
            a scalar weight has changed.

        **Returns**

        ctens : :class:`ITPOTerm`
            Result of contraction.
        """
        if ctens is not None:
            ctens._transfer_entries({}, self._weights, {})
            tasks = []
            # Still have to contract local (as it is collapsed
            if self._local is not None:
                self._tensors[-1] = self._local
                ctens._tensors[-1] = None
                tasks.append(-1)
        else:
            ctens = self.empty_copy(do_copy_meas_vec=True)
            ctens._transfer_entries(self._link_inds, self._weights, self._operators)
            for key in self._tensors:
                ctens._tensors[key] = None

            if self._local is not None:
                self._tensors[-1] = self._local
                ctens._tensors[-1] = None

            tasks = list(self._tensors.keys())

        # Execute contractions (can be parallelized)
        # --------------------

        ctens._contraction_counter += len(tasks)
        for task in tasks:
            tens_a = self._tensors[task]

            if task == -1:
                cidx_self = [elem - 1 for elem in cidx_self]

            ctens._tensors[task] = tens_a.tensordot(tensor, (cidx_self, cidx_tensor))

            if task != -1:
                # Install order of MPO links (right now they are in the 1st half)
                num_ab = ctens._tensors[task].ndim
                idx_1 = tens_a.ndim - len(cidx_self) - 1

                perm = list(range(num_ab))
                perm.remove(idx_1)
                perm = perm + [idx_1]

                ctens._tensors[task].transpose_update(perm)

            if perm_local_out is not None:
                if task != -1:
                    perm_out = ITPOTerm._local_perm_to_full_perm(perm_local_out)
                else:
                    perm_out = perm_local_out

                ctens._tensors[task].transpose_update(perm_out)

        if self._local is not None:
            ctens._local = ctens._tensors[-1]
            del ctens._tensors[-1]
            del self._tensors[-1]

        ctens.sanity_check()
        return ctens

    def tensordot_with_tensor_left(
        self, tensor, cidx_tensor, cidx_self, perm_local_out=None, ctens=None
    ):
        """
        Execute contraction of iTPOTerm with tensors. Uncontracted
        non-MPO legs of tensor go before uncontracted non-MPO legs
        of self.

        **Arguments**

        tensor : instance of :class:`_AbstractQteaTensor`
            Tensor in the contraction as right/second tensor.

        cidx_tensor : list of ints
            Contraction legs for the `tensor`

        cidx_self : list of ints
            Contraction legs for full TPO tensor (local will auto-adapt)

        perm_local_out : list of intes
            Permutation of output (full TPO tensor will auto-adapt)

        ctens : `None` or :class:`ITPOTerm`
            If present, update mode is activating which assumes that only
            a scalar weight has changed.

        **Returns**

        ctens : :class:`ITPOTerm`
            Result of contraction.
        """
        if ctens is not None:
            ctens._transfer_entries({}, self._weights, {})
            tasks = []
            # Still have to contract local (as it is collapsed)
            if self._local is not None:
                self._tensors[-1] = self._local
                ctens._tensors[-1] = None
                tasks.append(-1)

        else:
            ctens = self.empty_copy(do_copy_meas_vec=True)
            ctens._transfer_entries(self._link_inds, self._weights, self._operators)
            for key in self._tensors:
                ctens._tensors[key] = None

            if self._local is not None:
                self._tensors[-1] = self._local
                ctens._tensors[-1] = None

            tasks = list(self._tensors.keys())

        # Execute contractions (can be parallelized)
        # --------------------

        ctens._contraction_counter += len(tasks)
        for task in tasks:
            tens_b = self._tensors[task]

            if task == -1:
                cidx_self = [elem - 1 for elem in cidx_self]

            ctens._tensors[task] = tensor.tensordot(tens_b, (cidx_tensor, cidx_self))

            if task != -1:
                # Install order of MPO links (right now they are in the 2nd half)
                num_ab = ctens._tensors[task].ndim
                idx_0 = tensor.ndim - len(cidx_tensor)

                perm = list(range(num_ab))
                perm.remove(idx_0)
                perm = [idx_0] + perm

                ctens._tensors[task].transpose_update(perm)

            if perm_local_out is not None:
                if task != -1:
                    perm_out = ITPOTerm._local_perm_to_full_perm(perm_local_out)
                else:
                    perm_out = perm_local_out

                ctens._tensors[task].transpose_update(perm_out)

        if self._local is not None:
            ctens._local = ctens._tensors[-1]
            del ctens._tensors[-1]
            del self._tensors[-1]

        ctens.sanity_check()
        return ctens

    def matrix_multiply(
        self,
        other,
        cidx_self,
        cidx_other,
        eye_a=None,
        eye_b=None,
        perm_local_out=None,
        ctens=None,
        verbose=0,
    ):
        """
        Contract of two iTPOTerms.

        **Arguments**

        other : instance of :class:`iTPOTerm`
            Right / second term in the multiplication

        cidx_self : list of ints
            Contraction legs for full TPO tensor (local will auto-adapt)

        cidx_other : list of ints
            Contraction legs for full TPO tensor (local will auto-adapt)

        eye_a : instance of :class:`_AbstractQteaTensor` or None, optional
            If `self` is not a rank-4 iTPOTerm, pass what should be used
            as identity.
            Default to `None`

        eye_b : instance of :class:`_AbstractQteaTensor` or None, optional
            If `other` is not a rank-4 iTPOTerm, pass what should be used
            as identity.
            Default to `None`

        perm_local_out : list of ints or None, optional
            Permutation of output (full TPO tensor will auto-adapt)
            (MPO links will be permuted in first and last place automatically)
            Default to `None`

        ctens : `None` or :class:`ITPOTerm`
            If present, update mode is activating which assumes that only
            a scalar weight has changed.

        verbose : int, optional
            Verbosity level.
            Default to 0.
        """
        self._print_matrix_multiply_entry(verbose)

        self.sanity_check()
        other.sanity_check()

        contr_tasks, link_ids = self._generate_tpo_ids_for_contrs(other)
        unique_tasks = self._group_contr_tasks(other, contr_tasks, eye_a, eye_b)

        self._print_contr_tasks(contr_tasks, unique_tasks, verbose)

        task_keys = list(unique_tasks.keys())
        num_tasks = len(task_keys)

        if ctens is not None:
            tensors = ctens._tensors
            for key, value in ctens._cache_update.items():
                tensors[key] = value

            ctens._local = None

            local_contr_tasks = {}
            local_unique_tasks = {}

            for elem in [-10, -20]:
                if elem in contr_tasks:
                    key = contr_tasks[elem]
                    local_contr_tasks[elem] = key
                    local_unique_tasks[key] = unique_tasks[key]

            local_task_keys = list(local_unique_tasks.keys())
            num_local_tasks = len(local_unique_tasks)
            case_funcs = self.get_case_funcs()

            for ii in range(num_local_tasks):
                # Retrieve information
                key = local_task_keys[ii]
                case_id, op_idx_a, op_idx_b = key
                target_key = local_unique_tasks[key]

                # Carry out contraction
                func = case_funcs[case_id]
                tensor_ii = func(
                    self._tensors[op_idx_a],
                    other._tensors[op_idx_b],
                    cidx_self,
                    cidx_other,
                    perm_local_out,
                )

                # Set value
                ctens._tensors[target_key] = tensor_ii

        else:
            # Dictionary prepared with None values
            tensors = {}
            for _, value in unique_tasks.items():
                tensors[value] = None

            # Carry out contractions (can be parallelized)
            # ----------------------

            case_funcs = self.get_case_funcs()

            for ii in range(num_tasks):
                # Retrieve information
                key = task_keys[ii]
                case_id, op_idx_a, op_idx_b = key
                target_key = unique_tasks[key]

                # Carry out contraction
                func = case_funcs[case_id]
                tensor_ii = func(
                    self._tensors[op_idx_a],
                    other._tensors[op_idx_b],
                    cidx_self,
                    cidx_other,
                    perm_local_out,
                )

                # Set value
                tensors[target_key] = tensor_ii

        # Post-process
        # ------------

        if ctens is None:
            ctens = self.empty_copy(other=other, do_copy_meas_vec=True)
            ctens._tensors = tensors
            ctens._contraction_counter += num_tasks
        else:
            ctens._transfer_entries_measurement(self, other_b=other)
            ctens._contraction_counter += num_local_tasks

        if verbose > 4:
            print("Tensors keys", tensors.keys())
            print("." * 15)

        to_be_deleted = set()
        for key, value in contr_tasks.items():
            if value[0] in [1, 34, 43, 53, 63, 99]:
                # Remaining TPO term - does not contract to local
                ctens._operators[key] = unique_tasks[value]
                ctens._link_inds[key] = link_ids[key]
                ctens._weights[key] = self._weights.get(key, 1.0) * other._weights.get(
                    key, 1.0
                )
                continue

            # Contraction to local
            # ....................

            op_idx = unique_tasks[value]
            to_be_deleted.add(op_idx)

            if verbose > 4:
                print("Local term", op_idx, value, ctens._tensors[op_idx].shape)

            weight = self._weights.get(key, 1.0) * other._weights.get(key, 1.0)

            if ctens._measurement_setup:
                if value[0] in [7, 8]:
                    ctens._meas_vec[key] = ctens._tensors[op_idx].copy() * weight

            if weight == 0.0:
                # Here we can check against exact zero, e.g., matching zero weights
                # coming from a compression
                continue

            if ctens._local is None:
                ctens._local = ctens._tensors[op_idx] * weight
            else:
                ctens._local.add_update(ctens._tensors[op_idx], factor_other=weight)

        # Remove local terms from tensors
        ctens.delete_or_cache_tensors(to_be_deleted)

        # Cleanup temporary items in original TPOs
        if self._local is not None:
            del self._tensors[-1]

        if other._local is not None:
            del other._tensors[-1]

        if self.idx_eye in self._tensors:
            del self._tensors[self.idx_eye]

        if other.idx_eye in other._tensors:
            del other._tensors[other.idx_eye]

        ctens.sanity_check()

        if verbose > 2:
            print("_" * 80 + "\n")

            if ctens._measurement_setup:
                print("ctens._meas_vec", ctens._meas_vec.keys())

        return ctens

    def _generate_tpo_ids_for_contrs(self, other):
        """Returns dict where keys are TPO-ID and values are case-ID and op-IDs."""

        # Do we profit from local_only=False argument as in fortran???

        # ordering is match_rl, match_lr, match_ll, match_rr: 34, 43
        itpo_contr_ids = {
            (True, False, False, False): 34,
            (False, True, False, False): 43,
            (False, False, True, False): 53,
            (False, False, False, True): 63,
            (True, True, False, False): 7,
            (False, False, True, True): 8,
        }

        tasks = {}
        link_ids = {}
        for key, op_idx_a in self._operators.items():
            op_idx_b = other._operators.get(key, None)
            if op_idx_b is None:
                tasks[key] = (1, op_idx_a, self.idx_eye)
                link_ids[key] = self._link_inds[key]
                continue

            match_rl = self._link_inds[key][1] == other._link_inds[key][0]
            match_lr = self._link_inds[key][0] == other._link_inds[key][1]
            match_ll = self._link_inds[key][0] == other._link_inds[key][0]
            match_rr = self._link_inds[key][1] == other._link_inds[key][1]
            key_bool = (match_rl, match_lr, match_ll, match_rr)

            case_id = itpo_contr_ids[key_bool]
            tasks[key] = (case_id, op_idx_a, op_idx_b)

            link_id = []
            if case_id in [34, 63]:
                link_id.append(self._link_inds[key][0])

            if case_id in [43, 53]:
                link_id.append(self._link_inds[key][1])

            if case_id in [43, 63]:
                link_id.append(other._link_inds[key][0])

            if case_id in [34, 53]:
                link_id.append(other._link_inds[key][1])

            link_ids[key] = link_id

        for key, op_idx_b in other._operators.items():
            op_idx_a = self._operators.get(key, None)
            if op_idx_a is not None:
                continue

            tasks[key] = (99, self.idx_eye, op_idx_b)
            link_ids[key] = other._link_inds[key]

        # Add local terms as well as task

        if self._local is not None:
            self._tensors[-1] = self._local
            tasks[-10] = (-10, -1, self.idx_eye)

        if other._local is not None:
            other._tensors[-1] = other._local
            tasks[-20] = (-20, self.idx_eye, -1)

        return tasks, link_ids

    def _group_contr_tasks(self, other, contr_tasks, eye_a, eye_b):
        """Returns dict where keys are case-ID/op-ID tuple and value is new tensor index."""

        # Aim for reproducible order which we need for update
        keys = sorted(list(contr_tasks.keys()))

        unique_tasks = {}
        idx = 0
        for key in keys:
            value = contr_tasks[key]
            if value in unique_tasks:
                continue

            unique_tasks[value] = idx
            idx += 1

        self._tensors[self.idx_eye] = eye_a
        other._tensors[self.idx_eye] = eye_b

        return unique_tasks

    @staticmethod
    def _local_perm_to_full_perm(perm):
        """Generate a full permutation keeping first and last link in place."""
        full_perm = [0]
        for elem in perm:
            full_perm.append(elem + 1)

        nn = len(full_perm)
        full_perm.append(nn)

        return full_perm

    @staticmethod
    def get_case_funcs():
        """
        Construct the mapping between contraction cases as integers and their functions.

        **Details**

        The cases and their IDs are a one-to-one copy from the fortran code. At the
        beginning, we had even more of them with every possible combination of
        contracting rank-3 and rank-4 MPOs with 0, 1, and 2 matching horizontal links.
        Now, they contain only rank-4 MPOs with 1 and matching horizontal links plus the
        local term rules at -10, -20. To simplify coding, the cases have each their own
        function (where in fortran it was still a select case).

        Copy-pasted from each-functions docstring:

        1) only left has TPO-ID
        7) lr and rl match to local term
        8) ll and rr match to local term
        34) match rl and keeping as TPO-ID
        43) match lr and keeping as TPO-ID
        53) match ll and keeping as TPO-ID
        63) match rr and keeping as TPO-ID
        99) only right has TPO-ID
        -10) local term in left
        -20) local term in right
        """
        case_funcs = {
            1: ITPOTerm._contr_1,
            7: ITPOTerm._contr_7,
            8: ITPOTerm._contr_8,
            34: ITPOTerm._contr_34,
            43: ITPOTerm._contr_43,
            53: ITPOTerm._contr_53,
            63: ITPOTerm._contr_63,
            99: ITPOTerm._contr_99,
            -10: ITPOTerm._contr_10,
            -20: ITPOTerm._contr_20,
        }
        return case_funcs

    @staticmethod
    def _contr_1(tens_a, eye_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 1: only left has TPO-ID"""

        # Offset by one for missing MPO link
        cidx_b = [ii - 1 for ii in cidx_b]

        if eye_b is not None:
            num_a = tens_a.ndim
            num_b = eye_b.ndim

            tmp = tens_a.tensordot(eye_b, (cidx_a, cidx_b))

            # permutation to move MPO links to first and last place

            num_ab = num_a + num_b - 2 * len(cidx_a)
            idx_1 = num_a - len(cidx_a) - 1

            perm = list(range(num_ab))
            perm.remove(idx_1)
            perm = perm + [idx_1]

            tmp.transpose_update(perm)

            # Permutation from argument
            if perm_out is not None:
                full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
                tmp.transpose_update(full_perm)

            return tmp

        # There must be an actual identity on eye_b, if we contract
        # over ...
        #
        # * zero links: outer product, need to construct identity
        # * one link: contraction with identity does not do anything
        # * two links: trace??

        if len(cidx_a) == 1:
            # Contraction with identity does not do anything, but we have
            # to check permutations

            num_a = tens_a.ndim

            ordered = list(range(num_a))

            order = deepcopy(ordered)
            order.remove(cidx_a[0])
            order = order[:-1] + cidx_a + [order[-1]]
            order = np.array(order)

            if perm_out is not None:
                full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
                final = order[full_perm]
                ordered = np.array(ordered)

                do_permute = not np.all(final == ordered)
            else:
                do_permute = True

            if do_permute:
                tmp = tens_a.transpose(order)

                if perm_out is not None:
                    tmp.transpose_update(full_perm)

            else:
                tmp = deepcopy(tens_a)

            return tmp

        raise NotImplementedError("Contr ID 1 without eye_b.")

    @staticmethod
    def _contr_7(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 7: lr and rl match to local term."""
        #    |   |
        # ---o---o---
        # |  |   |  |
        # |         |
        # |_________|

        num_a = tens_a.ndim
        num_b = tens_b.ndim

        cidx_a = [0] + cidx_a + [num_a - 1]
        cidx_b = [num_b - 1] + cidx_b + [0]

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        if perm_out is not None:
            tmp.transpose_update(perm_out)

        return tmp

    @staticmethod
    def _contr_8(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 8: ll and rr match to local term."""
        #      ________
        #      |      |
        #  |-O-|  |-O-|
        #  |______|
        num_a = tens_a.ndim
        num_b = tens_b.ndim

        cidx_a = [0] + cidx_a + [num_a - 1]
        cidx_b = [0] + cidx_b + [num_b - 1]

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        if perm_out is not None:
            tmp.transpose_update(perm_out)

        return tmp

    @staticmethod
    def _contr_10(tens_a, eye_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id -10: local term in left."""

        # Offset by one for missing MPO link in both
        cidx_a = [ii - 1 for ii in cidx_a]
        cidx_b = [ii - 1 for ii in cidx_b]

        if eye_b is not None:
            num_a = tens_a.ndim

            tmp = tens_a.tensordot(eye_b, (cidx_a, cidx_b))

            # Permutation from argument
            if perm_out is not None:
                # full_perm = iTPOTerm._local_perm_to_full_perm(perm_out)
                tmp.transpose_update(perm_out)

            return tmp

        # There must be an actual identity on eye_b, if we contract
        # over ...
        #
        # * zero links: outer product, need to construct identity
        # * one link: contraction with identity does not do anything
        # * two links: trace??

        if len(cidx_a) == 1:
            # Contraction with identity does not do anything, but we have
            # to check permutations

            num_a = tens_a.ndim

            ordered = list(range(num_a))

            order = deepcopy(ordered)
            order.remove(cidx_a[0])
            order = order + cidx_a
            order = np.array(order)

            if perm_out is not None:
                final = order[perm_out]
                ordered = np.array(ordered)

                do_permute = not np.all(final == ordered)
            else:
                do_permute = True

            if do_permute:
                tmp = tens_a.transpose(order)

                if perm_out is not None:
                    tmp.transpose_update(perm_out)

            else:
                tmp = deepcopy(tens_a)

            return tmp

        raise NotImplementedError("Contr ID -10 without eye_b.")

    @staticmethod
    def _contr_20(eye_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id -20: local term in right."""

        # Offset by one for missing MPO link in both
        cidx_a = [ii - 1 for ii in cidx_a]
        cidx_b = [ii - 1 for ii in cidx_b]

        if eye_a is not None:
            num_b = tens_b.ndim

            tmp = eye_a.tensordot(tens_b, (cidx_a, cidx_b))

            # Permutation from argument
            if perm_out is not None:
                tmp.transpose_update(perm_out)

            return tmp

        # There must be an actual identity on eye_a, if we contract
        # over ...
        #
        # * zero links: outer product, need to construct identity
        # * one link: contraction with identity does not do anything
        # * two links: trace??

        if len(cidx_b) == 1:
            # Contraction with identity does not do anything, but we have
            # to check permutations

            num_b = tens_b.ndim

            ordered = list(range(num_b))

            order = deepcopy(ordered)
            order.remove(cidx_b[0])
            order = cidx_b + order
            order = np.array(order)

            if perm_out is not None:
                final = order[perm_out]
                ordered = np.array(ordered)

                do_permute = not np.all(final == ordered)
            else:
                do_permute = True

            if do_permute:
                tmp = tens_b.transpose(order)

                if perm_out is not None:
                    tmp.transpose_update(perm_out)

            else:
                tmp = deepcopy(tens_b)

            return tmp

        raise NotImplementedError("Contr ID 20 without eye_a.")

    @staticmethod
    def _contr_34(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 34: match rl and keeping as TPO-ID"""
        #    |   |
        #  --o---o--
        #    |   |
        num_a = tens_a.ndim

        cidx_a = cidx_a + [num_a - 1]
        cidx_b = cidx_b + [0]

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        # No permutation required (first and last link already MPO links)

        # Permutation from argument
        if perm_out is not None:
            full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
            tmp.transpose_update(full_perm)

        return tmp

    @staticmethod
    def _contr_43(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 43: match lr and keeping as TPO-ID"""
        #    |     |
        # |--o-   -o--|
        # |  |     |  |
        # |           |
        # |___________|
        num_a = tens_a.ndim
        num_b = tens_b.ndim

        cidx_a = cidx_a + [0]
        cidx_b = cidx_b + [num_b - 1]

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        # Permutation to move MPO links to first and last place

        num_ab = num_a + num_b - 2 * len(cidx_a)
        idx_0 = num_ab - len(cidx_a) - 1
        idx_1 = num_ab - len(cidx_a)

        perm = list(range(num_ab))
        perm.remove(idx_0)
        perm.remove(idx_1)
        perm = [idx_0] + perm + [idx_1]

        tmp.transpose_update(perm)

        # Permutation from argument
        if perm_out is not None:
            full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
            tmp.transpose_update(full_perm)

        return tmp

    @staticmethod
    def _contr_53(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 53: match ll and keeping as TPO-ID"""
        #  |-O-  |-O-
        #  |_____|
        num_a = tens_a.ndim
        num_b = tens_b.ndim

        cidx_a = [0] + cidx_a
        cidx_b = [0] + cidx_b

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        # Permutation to move MPO links to first and last place

        num_ab = num_a + num_b - 2 - 2 * len(cidx_a)
        idx_0 = num_a - len(cidx_a) - 1

        perm = list(range(num_ab))
        perm.remove(idx_0)
        perm = [idx_0] + perm

        tmp.transpose_update(perm)

        # Permutation from argument
        if perm_out is not None:
            full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
            tmp.transpose_update(full_perm)

        return tmp

    @staticmethod
    def _contr_63(tens_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 63: match rr and keeping as TPO-ID"""
        #   -O-|  -O-|
        #      |_____|
        num_a = tens_a.ndim
        num_b = tens_b.ndim

        cidx_a = cidx_a + [num_a - 1]
        cidx_b = cidx_b + [num_b - 1]

        tmp = tens_a.tensordot(tens_b, (cidx_a, cidx_b))

        # Permutation to move MPO links to first and last place

        num_ab = num_a + num_b - 2 - 2 * len(cidx_a)
        idx_1 = num_a - len(cidx_a)

        perm = list(range(num_ab))
        perm.remove(idx_1)
        perm = perm + [idx_1]

        tmp.transpose_update(perm)

        # Permutation from argument
        if perm_out is not None:
            full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
            tmp.transpose_update(full_perm)

        return tmp

    @staticmethod
    def _contr_99(eye_a, tens_b, cidx_a, cidx_b, perm_out):
        """Contraction for case-id 99: only right has TPO-ID."""

        # Offset by one for missing MPO link
        cidx_a = [ii - 1 for ii in cidx_a]

        if eye_a is not None:
            num_a = eye_a.ndim
            num_b = tens_b.ndim

            tmp = eye_a.tensordot(tens_b, (cidx_a, cidx_b))

            # permutation to move MPO links to first and last place

            num_ab = num_a + num_b - 2 * len(cidx_a)
            idx_0 = num_a - len(cidx_a)

            perm = list(range(num_ab))
            perm.remove(idx_0)
            perm = [idx_0] + perm

            tmp.transpose_update(perm)

            # Permutation from argument
            if perm_out is not None:
                full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
                tmp.transpose_update(full_perm)

            return tmp

        # There must be an actual identity on eye_a, if we contract
        # over ...
        #
        # * zero links: outer product, need to construct identity
        # * one link: contraction with identity does not do anything
        # * two links: trace??

        if len(cidx_b) == 1:
            # Contraction with identity does not do anything, but we have
            # to check permutations

            num_b = tens_b.ndim

            ordered = list(range(num_b))

            order = deepcopy(ordered)
            order.remove(cidx_b[0])
            order = [order[0]] + cidx_b + order[1:]
            order = np.array(order)

            if perm_out is not None:
                full_perm = ITPOTerm._local_perm_to_full_perm(perm_out)
                final = order[full_perm]
                ordered = np.array(ordered)

                do_permute = not np.all(final == ordered)
            else:
                do_permute = True

            if do_permute:
                tmp = tens_b.transpose(order)

                if perm_out is not None:
                    tmp.transpose_update(full_perm)

            else:
                tmp = deepcopy(tens_b)

            return tmp

        raise NotImplementedError("Contr ID 99 without eye_a.")

    def _print_matrix_multiply_entry(self, verbose):
        """Print summary of self when entering matrix_multiply."""
        if verbose > 2:
            print("\n\n" + "*" * 80)
            print("matrix_multiply\n")

            for _, tensor in self._tensors.items():
                print("Tensor self", tensor.shape)

            if self._local is not None:
                print("Local self", self._local.shape)

    @staticmethod
    def _print_contr_tasks(contr_tasks, unique_tasks, verbose):
        """Print a summary of the contraction tasks found."""
        if verbose > 2:
            print("contr_tasks: TPO-ID, (case-ID, op_idx_a, op_idx_b)")
            for key, value in contr_tasks.items():
                print(" > ", key, value)

            print("\nunique_tasks: (case-ID, op_idx_a, op_idx_b), new_op_idx")
            for key, value in unique_tasks.items():
                print(" - ", key, value)


class ITPOSites(_RestrictedList):
    """iTPOSites contains the physical terms."""

    class_allowed = ITPOTerm

    def __init__(self, num_sites, do_indexing, enable_update):
        super().__init__()

        for _ in range(num_sites):
            self.append(ITPOTerm(do_indexing=do_indexing, enable_update=enable_update))

    @property
    def has_oqs(self):
        """Flag if MPO has Lindblad terms (just present, not looking at coupling)."""
        has_oqs = False
        for elem in self:
            has_oqs = has_oqs or elem.has_oqs

        return has_oqs

    def update_couplings(self, params):
        """Load couplings from an update params dictionary."""
        for elem in self:
            elem.update_couplings(params)

    def get_max_tpo_id(self):
        """Loop over all sites to get the maximal TPO ID."""
        max_tpo_id = -1
        for elem in self:
            max_tpo_id = max(max_tpo_id, elem.get_max_tpo_id())

        return max_tpo_id

    def add_dense_mpo_list(self, dense_mpo_list):
        """Add terms from a :class:`DenseMPOList` to the iTPO sites."""

        tpo_id = -1
        for _, mpo in enumerate(dense_mpo_list):
            if len(mpo) == 1:
                # Local term
                jj = mpo[0].site

                self[jj].add_local(
                    mpo[0].operator,
                    mpo[0].weight,
                    mpo[0].strength,
                    mpo[0].pstrength,
                    mpo.is_oqs,
                )
                continue

            if mpo.is_oqs:
                warnings.warn("Skipping non-local Lindblad terms.")
                continue

            tpo_id += 1
            for jj, site in enumerate(mpo):
                link_inds = (jj, jj + 1)
                if jj + 1 == len(mpo):
                    link_inds = (jj, 0)

                kk = site.site
                self[kk].add_term(
                    tpo_id,
                    site.operator,
                    link_inds,
                    site.weight,
                    site.strength,
                    site.pstrength,
                )

        for elem in self:
            elem.sanity_check()

    def to_dense_mpo_list(self, params):
        """Convert site terms into dense MPO list."""

        dense_mpo_list = DenseMPOList()
        tensor_backend = None
        op_dict = TNOperators()
        # Cover local terms
        for ii, elem in enumerate(self):
            for jj, ops in enumerate(elem._local_ops):
                prefactor = elem._local_prefactors[jj]
                pstrength = elem._local_pstrengths[jj]
                key = f"_local__{ii}_{jj}"
                op_dict.ops[key] = ops

                site = MPOSite(
                    ii, key, pstrength, prefactor, operators=op_dict, params=params
                )

                # Open question how to retrieve this information
                is_oqs = False

                tensor_backend = TensorBackend(
                    type(ops), ops.base_tensor_cls, ops.device, ops.dtype
                )

                dense_mpo = DenseMPO(
                    [site], is_oqs=is_oqs, tensor_backend=tensor_backend
                )

                dense_mpo_list.append(dense_mpo)

        max_tpo_id = self.get_max_tpo_id()
        for ii in range(max_tpo_id + 1):
            sites = []

            for jj, elem in enumerate(self):
                if ii not in elem._operators:
                    # TPO ID not present in this term
                    continue

                sites.append(jj)

            if len(sites) == 0:
                # For some reason, TPO ID not active
                continue

            if tensor_backend is None:
                itpo_term = self[0]
                op_ind = itpo_term._operators[0]
                operator = elem._tensors[op_ind]

                tensor_backend = TensorBackend(
                    type(operator),
                    operator.base_tensor_cls,
                    itpo_term.device,
                    itpo_term.dtype,
                )

            # Now we all the sites
            # Open question how to retrieve this information
            is_oqs = False

            dense_mpo = DenseMPO([], is_oqs=is_oqs, tensor_backend=tensor_backend)

            for jj in sites:
                elem = self[jj]
                prefactor = elem._prefactor[ii]
                pstrength = elem._pstrength[ii]
                ops = elem._operators[ii]
                key = f"_tpo_interaction_{ii}_{jj}"
                op_dict.ops[key] = elem._tensors[ops]

                site = MPOSite(
                    jj, key, pstrength, prefactor, operators=op_dict, params=params
                )

                dense_mpo.append(site)

            dense_mpo_list.append(dense_mpo)

        return dense_mpo_list, op_dict

    def to_str(self):
        """Generate a string with information on he Hamiltonian (site terms)."""
        str_buffer = "\n\n" + "=" * 80 + "\n"
        str_buffer += f"iTPO on {len(self)} sites\n"

        for ii, site in enumerate(self):
            str_buffer += f"Site {ii}\n"
            str_buffer += site.to_str()

            if ii + 1 == len(self):
                str_buffer += "=" * 80 + "\n\n"
            else:
                str_buffer += "-" * 40 + "\n\n"

        return str_buffer


class ITPO(_AbstractEffectiveOperators):
    """
    iTPO term with Hamiltonian and effective operators, e.g., for ground state search.

    **Arguments**

    num_sites : int
        Number of sites in the system, e.g., qubits.

    do_compress : bool, optional
        Flag if compression should be actived (True).
        Default ``False`` (no compression).

    do_indexing : bool, optional
        Flag if indexing should be used (True) or if running as TPO (False).
        Default to ``True``

    enable_update : bool, optional
        Flag if smart update of time-dependent parameters should be actived (True).
        Activation also caches additional states on top of the effective operators.
        Default to `False` (no smart update).

    **Details**

    The indexed tensor product operator comes in different flavors:

    * TPO : without indexing, pass `do_indexing` flag.
    * iTPO : with indexing, only unique operators are contracted (default)
    * iuTPO : iTPO with smart update for time-evolution: pass flag
      `enable_update` on initialization, moreover `do_update` has to be
      set and unset when updating the coupling of the Hamiltonian.
    * icTPO : iTPO with compression, set flag `do_compress`, which is beneficial
      for systems with many interactions.
    * iucTPO : iTPO with compression and smart update for time-dependent parameters.
    """

    # pylint: disable-next=super-init-not-called
    def __init__(
        self, num_sites, do_compress=False, do_indexing=True, enable_update=False
    ):
        self.site_terms = ITPOSites(
            num_sites, do_indexing=do_indexing, enable_update=enable_update
        )
        self.eff_ops = {}

        # tracking
        self._contraction_counter = {}

        # for convert, compression mode
        self._tensor_network = None

        # store mode on indexing / updating here as well
        self._do_indexing = do_indexing
        self._enable_update = enable_update
        self._do_update = False

        # for compression mode, convert
        self._do_compress = do_compress
        self._compressible = {}

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def device(self):
        """Device where the tensor is stored."""
        for _, elem in self.eff_ops.items():
            return elem.device

        raise Exception("Running inquiery on empty effective operator.")

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        for _, elem in self.eff_ops.items():
            return elem.dtype

        raise Exception("Running inquiery on empty effective operator.")

    @property
    def do_update(self):
        """Status of the flag for doing update of effective operators."""
        return self._do_update

    @do_update.setter
    def do_update(self, value):
        """Set status of the flag for doing update of effective operators."""
        self._do_update = value

    @property
    def has_oqs(self):
        """Flag if MPO has Lindblad terms (just present, not looking at coupling)."""
        return self.site_terms.has_oqs

    @property
    def num_sites(self):
        """Return the number of sites in the underlying system."""
        return len(self.site_terms)

    # --------------------------------------------------------------------------
    #                          Overwritten operators
    # --------------------------------------------------------------------------

    def __getitem__(self, key):
        """Get an entry from the effective operators."""
        return self.eff_ops[key]

    def __setitem__(self, key, value):
        """Set an entry from the effective operators."""
        if not isinstance(value, ITPOTerm):
            raise TypeError("`site_term` must be an iTPOTerm")

        self.eff_ops[key] = value

    # --------------------------------------------------------------------------
    #     Abstract effective operator methods requiring implementation here
    # --------------------------------------------------------------------------

    def contr_to_eff_op(self, tensor, pos, pos_links, idx_out):
        """
        Contract operator lists with tensors T and Tdagger to effective operator.


        **Arguments**

        tensor : :class:`_AbstractQteaTensor`
            Tensor to be contracted to effective operator.

        pos : int, tuple (depending on TN)
            Position of tensor.

        pos_links : list of int, tuple (depending on TN)
            Position of neighboring tensors where the links
            in `tensor` lead to.

        idx_out : int
            Uncontracted link to be used for effective operator.

        """
        ops_list = []
        idx_list = []
        for ii, pos_link in enumerate(pos_links):
            # detect the uncontracted link
            if ii == idx_out:
                pos_link_out = pos_link
                continue

            if pos_link is None:
                continue
            # get the tensor of the given positions
            pos_jj = self.eff_ops[(pos_link, pos)]
            ops_list.append(pos_jj)
            idx_list.append(ii)

        # Key and key for inverse direction
        key = (pos, pos_link_out)
        ikey = (pos_link_out, pos)
        c_counter = self._contraction_counter.get(key, 0)

        # Different loop starts are beneficial
        if idx_out > np.max(idx_list):
            # From left to right
            idx_start = 0
            stride = 1

        elif idx_out < np.min(idx_list):
            # Looping backwards requires flipping links - avoid for now
            idx_start = 0
            stride = 1
            ## From right to left
            # idx_start = len(idx_list) - 1
            # stride = -1

        else:
            # To get contractable stuff, we start right
            # of the gap and move rightwards
            stride = 1
            for ii, elem in enumerate(idx_list):
                if elem > idx_out:
                    idx_start = ii

        # Contract tree tensor with sparse MPO
        cidx = idx_list[idx_start]

        perm_out = _transpose_idx(tensor.ndim, cidx)
        # perm_out[perm_out == tensor.ndim - 1] += 1
        # perm_out = [tensor.ndim - 1] + list(perm_out) + [tensor.ndim + 1]

        ctens, ukey = self.get_ctens_for_update(key, -1)
        ctens = ops_list[idx_start].tensordot_with_tensor_left(
            tensor, [cidx], [2], perm_local_out=perm_out, ctens=ctens
        )
        self.set_ctens_for_update(ukey, ctens)

        c_counter += ctens._contraction_counter
        ctens._contraction_counter = 0

        ii = idx_start
        for jj in range(len(idx_list) - 1):
            ii += stride
            if ii == len(idx_list):
                ii = 0

            cached_ctens, ukey = self.get_ctens_for_update(key, jj)

            if stride > 0:
                mat_b = ops_list[ii]

                # Need offset of one as we have link to the left now
                cidx_a = [idx_list[ii] + 1]
                cidx_b = [2]
                perm_out = _transpose_idx(tensor.ndim, idx_list[ii])
                # perm_out = _transpose_idx(ctens.ndim - 1, cidx_a[0])
                # perm_out = list(perm_out) + [ctens.ndim - 1]
                # print('ctens shape: ', ctens._tensors[0].shape)
                # print('matb shape: ', mat_b._tensors[0].shape)
                ctens = ctens.matrix_multiply(
                    mat_b,
                    cidx_a,
                    cidx_b,
                    eye_a=tensor,
                    perm_local_out=perm_out,
                    ctens=cached_ctens,
                )

            else:
                mat_a = ops_list[ii]

                # Need offset of one as we have link to the left now (cidx_b)
                cidx_a = [2]
                cidx_b = [idx_list[ii] + 1]
                perm_out = _transpose_idx(tensor.ndim, idx_list[ii])
                # perm_out = _transpose_idx(ctens.ndim - 2, idx_list[ii])
                # perm_out += 1
                # perm_out = [0] + list(perm_out) + [ctens.ndim - 1]
                ctens = mat_a.matrix_multiply(
                    ctens,
                    cidx_a,
                    cidx_b,
                    eye_b=tensor,
                    perm_local_out=perm_out,
                    ctens=cached_ctens,
                )

            c_counter += ctens._contraction_counter
            ctens._contraction_counter = 0
            self.set_ctens_for_update(ukey, ctens)

        # Contract with complex conjugated
        cidx_a = tensor._invert_link_selection([idx_out])
        cidx_b = [ii + 1 for ii in cidx_a]

        # We get a four-link tensor
        # perm_out = [1, 0, 2, 3]
        cached_ctens, ukey = self.get_ctens_for_update(key, -2)
        ctens = ctens.tensordot_with_tensor_left(
            tensor.conj(),
            cidx_a,
            cidx_b,
            ctens=cached_ctens,  # , perm_local_out=perm_out
        )
        c_counter += ctens._contraction_counter
        ctens._contraction_counter = 0
        self.set_ctens_for_update(ukey, ctens)

        if (not ctens._measurement_setup) and ikey in self.eff_ops:
            del self.eff_ops[ikey]

        if ctens._measurement_setup and key in self.eff_ops:
            raise Exception("Potentially overwriting measurement results.")

        self.eff_ops[key] = ctens
        self._contraction_counter[key] = c_counter

        if self._do_compress:
            self.compress(key)

    def contract_tensor_lists(self, tensor, pos, pos_links, custom_ops=None):
        """
        Linear operator to contract all the effective operators
        around the tensor in position `pos`. Used in the optimization.

        **Arguments**

        tensor : :class:`_AbstractQteaTensor`
            Tensor to be contracted to effective operator.

        pos : int, tuple (depending on TN)
            Position of tensor.

        pos_links : list of int, tuple (depending on TN)
            Position of neighboring tensors where the links
            in `tensor` lead to.

        custom_ops : `None` or list of :class:`ITPOTerm`
            Ordered list of iTPO terms for tensor, which
            should be used instead of information in `pos`
            and `pos_links`.
        """
        if custom_ops is None:
            ops_list = []
            idx_list = []
            for ii, pos_link in enumerate(pos_links):
                if pos_link is None:
                    continue

                pos_jj = self.eff_ops[(pos_link, pos)]
                ops_list.append(pos_jj)
                idx_list.append(ii)
        else:
            # Required for time evolution backwards step on R-tensor
            # and two-tensor update; None entries must be acceptable
            ops_list = []
            idx_list = []
            for ii, elem in enumerate(custom_ops):
                if elem is None:
                    continue

                ops_list.append(elem)
                idx_list.append(ii)

        # Find the best start of the loop with an sparse MPO with just one
        # row if possible
        idx_start = 0
        # DIFF to SPO: for ii, elem in enumerate(ops_list):
        # DIFF to SPO:    if elem._sp_mat.shape[0] == 1:
        # DIFF to SPO:        idx_start = ii
        # DIFF to SPO:        break

        # Contract tree tensor with sparse MPO
        cidx = idx_list[idx_start]

        perm_out = _transpose_idx(tensor.ndim, cidx)
        # DIFF to SPO: perm_out[perm_out == tensor.ndim - 1] += 1
        # DIFF to SPO: perm_out = [tensor.ndim - 1] + list(perm_out) + [tensor.ndim + 1]

        ctens = ops_list[idx_start].tensordot_with_tensor_left(
            tensor, [cidx], [2], perm_local_out=perm_out
        )
        c_counter = self._contraction_counter.get(pos, 0)
        c_counter += ctens._contraction_counter
        ctens._contraction_counter = 0

        ii = idx_start
        for _ in range(len(idx_list) - 1):
            ii += 1
            if ii == len(idx_list):
                ii = 0

            op_ii = ops_list[ii]

            cidx_a = [idx_list[ii] + 1]
            cidx_b = [2]
            perm_out = _transpose_idx(tensor.ndim, idx_list[ii])
            # DIFF to SPO: perm_out = _transpose_idx(ctens.ndim - 1, cidx_a[0])
            # DIFF to SPO: perm_out = list(perm_out) + [ctens.ndim - 1]
            ctens = ctens.matrix_multiply(
                op_ii, cidx_a, cidx_b, eye_a=tensor, perm_local_out=perm_out
            )
            c_counter += ctens._contraction_counter
            ctens._contraction_counter = 0

        # DIFF to SPO:
        if len(ctens._operators) > 0:
            raise Exception("contract_tensor_lists does not contract to local.")

        ctens = ctens._local
        self._contraction_counter[pos] = c_counter

        return ctens

    def convert(self, dtype, device):
        """
        Convert underlying array to the speificed data type inplace. Original
        site terms are preserved.
        """
        if (self.dtype == dtype) and (self.device == device):
            return

        # We could detect up-conversion and down-conversion. Only for
        # conversion to higher precisions, we have to copy from the
        # site terms again which are in double precision
        if self._tensor_network is None:
            raise Exception("convert needs tensor network to be set.")

        for ii, key in enumerate(self._tensor_network._iter_physical_links()):
            self[key] = self.site_terms[ii].copy()

        for _, elem in self.eff_ops.items():
            elem.convert(dtype, device)

    # --------------------------------------------------------------------------
    #                    Overwriting methods from parent class
    # --------------------------------------------------------------------------

    def print_summary(self, log_file=None):
        """Print summary of computational effort."""
        if log_file is None:
            myprint = print
        else:

            def myprint(*args, log_file=log_file):
                log_file.write(str(args))
                log_file.write("\n")

        mode_str = f"(indexing={self._do_indexing}, "
        mode_str += f"compress={self._do_compress})"
        myprint("=" * 20 + f" Contraction summary iTPO {mode_str} " + "=" * 20)

        total = 0
        for key, value in self._contraction_counter.items():
            myprint("Count", key, "=", value)
            total += value

        myprint("Total contractions:", total)
        myprint("^" * 60)

    def add_contraction_counters(self, other):
        """Add a contraction counter in-place."""
        for key, value in other._contraction_counter.items():
            if key in self._contraction_counter:
                self._contraction_counter[key] += value
            else:
                self._contraction_counter[key] = value

    # --------------------------------------------------------------------------
    #                          Methods specific to iTPO
    # --------------------------------------------------------------------------

    def collect_measurements(self, num_terms=None):
        """Collect the measurements from measurement setup of iTPO."""
        if num_terms is None:
            results = {}
        else:
            results = np.zeros(num_terms, dtype=np.complex128)

        for _, elem in self.eff_ops.items():
            for key, value in elem.collect_measurements():
                results[key] = value

        return results

    def set_meas_status(self, do_measurement=True):
        """Set the measurement status for all iTPOTerms in iTPOSites."""
        for elem in self.site_terms:
            elem.set_meas_status(do_measurement)

    def compress(self, pos_tuple):
        """
        Compress iTPOTerm at a given position.

        **Arguments**

        pos_tuple : tuple
            position of the effective operator to be compressed
            via two tensor positions

        **Details**

        Considering an eight-site MPS-like structure with all-to-all
        two-body interactions the terms by default at link between
        sites 6 and 7 are

        * 1 acting at 7 and 8
        * 2 acting at 7 and 8
        * 3 acting at 7 and 8
        * 4 acting at 7 and 8
        * 5 acting at 7 and 8
        * 6 acting at 7 and 8

        and will be compressed to

        * (1 + 2 + 3 + 4 + 5 + 6) acting at 7
        * (1 + 2 + 3 + 4 + 5 + 6) acting at 8

        Thus, compression makes potentially sense for many interactions
        and if more than half of the system is integrated into an effective
        operator. The latter is checked to avoid unnecessary execution.
        """
        if self._tensor_network is None:
            raise Exception("iTPO was not set up for compression.")

        if not self._compressible.get(pos_tuple, True):
            # From previous evaluation, we can skip here
            return

        # Sanity check on incoming tensor
        self.eff_ops[pos_tuple].sanity_check()

        # Define tolerance hard-coded here
        tol = 1e-12

        sites_idx_eff, _ = self._tensor_network.get_bipartition_link(
            pos_tuple[0], pos_tuple[1]
        )

        num_sites_eff = len(sites_idx_eff)
        if 2 * num_sites_eff <= self.num_sites:
            # No benefit of compression
            self._compressible[pos_tuple] = False
            return

        orig_list = []
        for key, value in self.eff_ops[pos_tuple]._operators.items():
            orig_list.append(value)

        nn_orig = len(set(orig_list))

        # Status will keep track of
        # no key: TPO ID not treated yet
        # 1 : compressed as destination
        # 2 : compressed as (one of the) source(s)
        # 3 : compression not possible
        # 4 : zero weight,
        status = {}

        for tpo_id in self.eff_ops[pos_tuple].iter_tpo_ids():
            status_tpo_id = status.get(tpo_id, 0)
            if status_tpo_id > 0:
                # Already visited - skip
                continue

            if abs(self.eff_ops[pos_tuple]._weights[tpo_id]) < tol:
                # Weight zero (can be compressed, but we cannot use this one
                # as the one to keep)
                status[tpo_id] = 4
                continue

            dst_sites = []
            dst_ops = []
            dst_weights = self.eff_ops[pos_tuple]._weights[tpo_id]
            for ii, key in enumerate(self._tensor_network._iter_physical_links()):
                if ii in sites_idx_eff:
                    # Sites are already in effective operator
                    continue

                if tpo_id not in self.eff_ops[key]._link_inds:
                    # TPO ID not present
                    continue

                dst_weights *= self.eff_ops[key]._weights[tpo_id]
                dst_sites.append(ii)
                dst_ops.append(self.eff_ops[key]._operators[tpo_id])

            if abs(dst_weights) < tol:
                # Same as before (non-trivial case where another weight
                # is zero on one of the terms of this interaction)
                status[tpo_id] = 4
                continue

            # The inner loop over TPO IDs searches for a matching partner
            # to compress with for the `tpo_id` of the outer loop
            idx_tensor = None
            for idx in self.eff_ops[pos_tuple].iter_tpo_ids():
                if idx == tpo_id:
                    continue

                status_idx = status.get(idx, 0)
                if status_idx in [1, 2, 3]:
                    continue

                src_sites = []
                src_ops = []
                src_weights = self.eff_ops[pos_tuple]._weights[idx]
                for ii, key in enumerate(self._tensor_network._iter_physical_links()):
                    if ii in sites_idx_eff:
                        continue

                    if idx not in self.eff_ops[key]._link_inds:
                        continue

                    src_weights *= self.eff_ops[key]._weights[idx]
                    src_sites.append(ii)
                    src_ops.append(self.eff_ops[key]._operators[idx])

                if len(dst_sites) != len(src_sites):
                    continue

                if dst_sites != src_sites:
                    continue

                if dst_ops != src_ops:
                    continue

                # We actually can compress ...
                if status_tpo_id == 0:
                    # For first combination, we also have to add tensor as copy (cannot
                    # overwrite existing tensor as it might be used in another term)
                    idx_tensor = self.eff_ops[pos_tuple]._operators[tpo_id]
                    idx_tensor = self.eff_ops[pos_tuple].get_index_copy_operator(
                        idx_tensor
                    )
                    self.eff_ops[pos_tuple]._operators[tpo_id] = idx_tensor

                    status_tpo_id = 1
                    status[tpo_id] = 1

                if idx_tensor is None:
                    raise Exception("Check algorithm.")

                status[idx] = 2

                weight = src_weights / dst_weights
                idx_tensor_src = self.eff_ops[pos_tuple]._operators[idx]

                if weight != 0.0:
                    self.eff_ops[pos_tuple]._tensors[idx_tensor].add_update(
                        self.eff_ops[pos_tuple]._tensors[idx_tensor_src],
                        factor_other=weight,
                    )

                self.eff_ops[pos_tuple]._weights[idx] = 0.0
                self.eff_ops[pos_tuple]._operators[idx] = idx_tensor

            if status.get(tpo_id, 0) == 0:
                # Then, any compression is impossible here
                status[tpo_id] = 3

        comp_list = []
        for key, value in self.eff_ops[pos_tuple]._operators.items():
            comp_list.append(value)

        nn_comp = len(set(comp_list))

        self._compressible[pos_tuple] = nn_comp < nn_orig

        # Sanity check outgoing tensor
        self.eff_ops[pos_tuple].sanity_check()

    def update_couplings(self, params):
        """Load couplings from an update params dictionary."""
        self.site_terms.update_couplings(params)

        if self.do_update:
            # Transfer entries
            for ii, key in enumerate(self._tensor_network._iter_physical_links()):
                self[key] = self.site_terms[ii].copy()
                self[key].convert(
                    self._tensor_network.dtype, self._tensor_network.device
                )
                # print("update itposite", self[key]._local.elem)

    def get_ctens_for_update(self, key, identifier):
        """
        Extract a tensor for update of time-dependent coupling from cache.

        **Arguments**

        key : immutable
            Key from effective operator to be built serving as base key.

        identifier :
            Extension to identity step when building effective operator.

        **Returns**

        ctens : instance of :class:`ITPOTerm` or None
            Retrieve tensor from cache if updates are enabled.

        ukey : str or `None`
            Key for storing tensor again.
        """
        if not self._enable_update:
            return None, None

        ukey = tuple(list(key) + [identifier])
        ctens = self.eff_ops.get(ukey, None)

        if self._do_update:
            return ctens, ukey

        return None, ukey

    def set_ctens_for_update(self, ukey, ctens):
        """Set a tensor for time-dependent coupling updates (if enabled)."""
        if not self._enable_update:
            return

        self.eff_ops[ukey] = ctens

    def add_dense_mpo_list(self, dense_mpo_list):
        """Add terms from a :class:`DenseMPOList` to the iTPO sites."""
        self.site_terms.add_dense_mpo_list(dense_mpo_list)

    def to_dense_mpo_list(self, params, do_initialize=True):
        """Return the dense MPO form of the site terms, requires params dict."""
        dense_mpo_list, operators = self.site_terms.to_dense_mpo_list(params)

        if do_initialize:
            dense_mpo_list.initialize(operators, params)

        return dense_mpo_list

    def setup_as_eff_ops(self, tensor_network, measurement_mode=False):
        """Set this sparse MPO as effective ops in TN and initialize."""
        self._tensor_network = tensor_network

        for ii, key in enumerate(tensor_network._iter_physical_links()):
            self[key] = self.site_terms[ii].copy()

        tensor_network.eff_op = self
        tensor_network.build_effective_operators(measurement_mode=measurement_mode)

    def to_str(self):
        """Generate a string with information on the effective operators."""
        str_buffer = "\n\n" + "=" * 80 + "\n"
        str_buffer += "iTPOs for effective operators\n"
        str_buffer += "Sites:\n"

        ind4 = " " * 4

        tracker = {}
        for ii, key in enumerate(self._tensor_network._iter_physical_links()):
            str_buffer += ind4 + f"site ii = {ii}"
            str_buffer += self.eff_ops[key].to_str(ind_offset=4)
            str_buffer += ind4 + "-" * 40 + "\n\n"

            tracker[key] = None

        for key, value in self.eff_ops.items():
            if key in tracker:
                continue

            str_buffer += f"Link {str(key)}\n"
            str_buffer += value.to_str(ind_offset=4)

            str_buffer += ind4 + "-" * 40 + "\n\n"

        str_buffer += "=" * 80 + "\n\n"

        return str_buffer
