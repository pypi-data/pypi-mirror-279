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
The module contains an abstract tensor network, from which other tensor
networks can be derived.
"""

import abc
import json
import pickle
import os
from time import time as tictoc
from warnings import warn
from copy import deepcopy
import numpy as np
import mpmath as mp

# try to import mpi4py
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

from qtealeaves.tooling import QteaJsonEncoder
from qtealeaves.convergence_parameters import TNConvergenceParameters
from qtealeaves.tensors import TensorBackend

__all__ = [
    "_AbstractTN",
    "postprocess_statedict",
    "MPI",
    "TN_MPI_TYPES",
]


# pickle in deepcopy fails if stored within the TN type
if MPI is not None:
    TN_MPI_TYPES = {
        "<c16": MPI.DOUBLE_COMPLEX,
        "<c8": MPI.COMPLEX,
        "<f4": MPI.REAL,
        "<f8": MPI.DOUBLE_PRECISION,
        "<i8": MPI.INT,
    }
else:
    TN_MPI_TYPES = {}


class _AbstractTN(abc.ABC):
    """
    Abstract tensor network class with methods applicable to any
    tensor network.

    Parameters
    ----------

    num_sites: int
        Number of sites

    convergence_parameters: :py:class:`TNConvergenceParameters`
        Class for handling convergence parameters. In particular,
        in the python TN simulator, we are interested in:
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
    """

    extension = "tn"
    has_de = False

    def __init__(
        self,
        num_sites,
        convergence_parameters,
        local_dim=2,
        requires_singvals=False,
        tensor_backend=None,
    ):
        # Class attributes by arguments
        self._num_sites = num_sites
        self._local_dim = (
            [local_dim] * num_sites if np.isscalar(local_dim) else local_dim
        )
        self._convergence_parameters = convergence_parameters
        self._tensor_backend = (
            TensorBackend() if tensor_backend is None else tensor_backend
        )

        # Other class attributes
        self._iso_center = None
        self.eff_op = None

        # internal storage for last energy measurement for algorithms whic
        # need an estimate where it is sufficient to rely that this number
        # is not too outdated
        self._prev_energy = None

        # Selection of QR vs SVD
        self._requires_singvals = requires_singvals
        # store solver to be used
        self._solver = None

        # log file for a simulation
        self._log_file = None
        self._log_verbosity = 0

        # Attributes for MPI
        self.comm = None

        # Run checks on input
        # -------------------

        if not isinstance(convergence_parameters, TNConvergenceParameters):
            raise TypeError(
                "convergence parameters must be " + "TNConvergenceParameters class"
            )

        if not isinstance(self._tensor_backend, TensorBackend):
            raise TypeError(
                f"Passed wrong type {type(self._tensor_backend)} to backend."
            )

        if self._convergence_parameters.max_bond_dimension < 1:
            raise ValueError("The minimum bond dimension for a product state is 1")

        if self._convergence_parameters.cut_ratio <= 0:
            raise ValueError("The cut_ratio value must be positive")

        if len(self.local_dim) != num_sites:
            raise ValueError(
                f"Length of local_dim {len(local_dim)} differs "
                + f"from num_sites {num_sites}."
            )

        if np.min(self.local_dim) < 2:
            raise ValueError("Local dimension cannot be smaller than 2.")

        # internal variable for flex-TDVP
        self._timestep_mode_5_counter = 0

        # MPI initialization
        self._initialize_mpi()

    # --------------------------------------------------------------------------
    #                               Properties
    # --------------------------------------------------------------------------

    @property
    def convergence_parameters(self):
        """Get the convergence settings from the TN."""
        return self._convergence_parameters

    @convergence_parameters.setter
    def convergence_parameters(self, value):
        """
        Set the convergence settings from the TN. (no immediate effect, only
        in next steps).
        """
        self._convergence_parameters = value

    @property
    @abc.abstractmethod
    def default_iso_pos(self):
        """
        Returns default isometry center position, e.g., for initialziation
        of effective operators.
        """

    @property
    def device(self):
        """Device where the tensor is stored."""
        for tensor in self._iter_tensors():
            return tensor.device

        return None

    @property
    def dtype(self):
        """Data type of the underlying arrays."""
        for tensor in self._iter_tensors():
            return tensor.dtype

        return None

    @property
    def dtype_eps(self):
        """Data type's machine precision of the underlying arrays."""
        for tensor in self._iter_tensors():
            return tensor.dtype_eps

        return None

    @property
    def iso_center(self):
        """Isometry center of the tensor network"""
        return self._iso_center

    @iso_center.setter
    def iso_center(self, value):
        """Change the value of the iso center"""
        self._iso_center = value

    @property
    def has_symmetry(self):
        """Check if TN is built out of symmetric tensors."""
        for tensor in self._iter_tensors():
            return tensor.has_symmetry

        return None

    @property
    def log_file(self):
        """Return the open filehandle for the log file or `None` if not open."""
        return self._log_file

    @property
    def num_sites(self):
        """Number of sites property"""
        return self._num_sites

    @property
    def local_dim(self):
        """Local dimension property"""
        if isinstance(self._local_dim, int):
            return self._local_dim
        elif isinstance(self._local_dim, np.ndarray):
            return self._local_dim
        elif isinstance(self._local_dim[0], int):
            return self._local_dim
        else:
            # Case for symmetries
            return [elem.shape for elem in self._local_dim]

    @property
    def local_links(self):
        """Return information on local link (for symmetries more than integer)."""
        return self._local_dim

    @property
    def solver(self):
        """Return current solver for the TN."""
        return self._solver

    @solver.setter
    def solver(self, value):
        """Set the solver, e.g., currently used for exp(-i H dt) |psi>."""
        self._solver = value

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
        Provide number of sites in the TN.
        """
        return self.num_sites

    # --------------------------------------------------------------------------
    #                       classmethod, classmethod like
    # --------------------------------------------------------------------------

    @classmethod
    @abc.abstractmethod
    def from_statevector(
        cls, statevector, local_dim=2, conv_params=None, tensor_backend=None
    ):
        """Decompose statevector to tensor network."""

    @classmethod
    def read_pickle(cls, filename):
        """Read via pickle-module."""
        ext = "pkl" + cls.extension
        if not filename.endswith(ext):
            raise Exception(
                f"Filename {filename} not valid, extension should be {ext}."
            )

        with open(filename, "rb") as fh:
            obj = pickle.load(fh)

        if not isinstance(obj, cls):
            raise TypeError(
                f"Loading wrong tensor network ansatz: {type(obj)} vs {cls}."
            )

        return obj

    @abc.abstractmethod
    def to_dense(self, true_copy=False):
        """Convert into a TN with dense tensors (without symmetries)."""

    def copy(self, dtype=None, device=None):
        """
        Make a copy of a TN.

        **Details**

        The following attributes have a special treatment and are not present
        in the copied object.

        * convergence_parameters
        * log file (filehandle)
        * MPI communicator

        """
        # Store attributes which cannot be pickled, so also potential problems
        # with deepcopy
        storage = self._store_attr_for_pickle()
        obj = deepcopy(self)
        self._restore_attr_for_pickle(storage)

        obj.convert(dtype, device)
        return obj

    @classmethod
    @abc.abstractmethod
    def read(cls, filename, tensor_backend, cmplx=True, order="F"):
        """Read a TN from a formatted file."""

    # --------------------------------------------------------------------------
    #                            Checks and asserts
    # --------------------------------------------------------------------------

    def is_dtype_complex(self):
        """Check if data type is complex based on one example tensor.."""
        for tensor in self._iter_tensors():
            return tensor.is_dtype_complex()

    # --------------------------------------------------------------------------
    #                     Abstract methods to be implemented
    # --------------------------------------------------------------------------

    @abc.abstractmethod
    def build_effective_operators(self, measurement_mode=False):
        """
        Build the complete effective operator on each
        of the links. Now assumes `self.eff_op` is set.
        """

    @abc.abstractmethod
    def _convert_singvals(self, dtype, device):
        """Convert the singular values of the tensor network to dtype/device."""

    @abc.abstractmethod
    def get_bipartition_link(self, pos_src, pos_dst):
        """
        Returns two sets of sites forming the bipartition of the system for
        a loopless tensor network. The link is specified via two positions
        in the tensor network.
        """

    @abc.abstractmethod
    def get_pos_links(self, pos):
        """
        Return a list of positions where all links are leading to. Number
        of entries is equal to number of links. Each entry contains the position
        as accessible in the actual tensor network.
        """

    @abc.abstractmethod
    def get_rho_i(self, idx):
        """
        Get the reduced density matrix of the site at index idx

        Parameters
        ----------
        idx : int
            Index of the site
        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def iso_towards(self, new_iso, keep_singvals=False, trunc=False, conv_params=None):
        """
        Shift the isometry center to the tensor at the
        corresponding position, i.e., move the isometry to a
        specific tensor, that might not be a physical.

        Parameters
        ----------
        new_iso :
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

        """

    @abc.abstractmethod
    def _iter_tensors(self):
        """Iterate over all tensors forming the tensor network (for convert etc)."""

    @abc.abstractmethod
    def norm(self):
        """
        Calculate the norm of the state.
        """

    @abc.abstractmethod
    def scale(self, factor):
        """
        Multiply the tensor network state by a scalar factor.

        Parameters
        ----------
        factor : float
            Factor for multiplication of current tensor network state.
        """

    @abc.abstractmethod
    def set_singvals_on_link(self, pos_a, pos_b, s_vals):
        """Update or set singvals on link via two positions."""

    @abc.abstractmethod
    def site_canonize(self, idx, keep_singvals=False):
        """
        Shift the isometry center to the tensor containing the
        corresponding site, i.e., move the isometry to a specific
        Hilbert space. This method can be implemented independent
        of the tensor network structure.

        Parameters
        ----------
        idx : int
            Index of the physical site which should be isometrized.
        keep_singvals : bool, optional
            If True, keep the singular values even if shifting the iso with a
            QR decomposition. Default to False.
        """

    @abc.abstractmethod
    def _update_eff_ops(self, id_step):
        """
        Update the effective operators after the iso shift

        Parameters
        ----------
        id_step : List[int]
            List with information of the iso moving path

        Returns
        -------
        None
            Updates the effective operators in place
        """

    @abc.abstractmethod
    def _partial_iso_towards_for_timestep(self, pos, next_pos, no_rtens=False):
        """
        Move by hand the iso for the evolution backwards in time

        Parameters
        ----------
        pos : Tuple[int] | int
            Position of the tensor evolved
        next_pos : Tuple[int] | int
            Position of the next tensor to evolve

        Returns
        -------
        QTeaTensor
            The R tensor of the iso movement
        Tuple[int]
            The position of the partner (the parent in TTNs)
        int
            The link of the partner pointing towards pos
        List[int]
            The update path to pass to _update_eff_ops
        """

    @abc.abstractmethod
    def default_sweep_order(self):
        """
        Default sweep order to be used in the ground state search/time evolution.

        Returns
        -------
        List[int] | List[Tuple[int]]
            The generator that you can sweep through
        """
        raise NotImplementedError("This method is ansatz-specific")

    def default_sweep_order_back(self):
        """Default sweep order backwards, e.g., for second-order methods."""
        return self.default_sweep_order()[::-1]

    @abc.abstractmethod
    def get_pos_partner_link_expansion(self, pos):
        """
        Get the position of the partner tensor to use in the link expansion
        subroutine

        Parameters
        ----------
        pos : int | Tuple[int]
            Position w.r.t. which you want to compute the partner

        Returns
        -------
        int | Tuple[int]
            Position of the partner
        int
            Link of pos pointing towards the partner
        int
            Link of the partner pointing towards pos
        """

    @abc.abstractmethod
    def write(self, filename, cmplx=True):
        """Write the TN in python format into a FORTRAN compatible format."""

    # --------------------------------------------------------------------------
    #                        Methods that can be inherited
    # --------------------------------------------------------------------------

    def checkpoint_copy_simulation_attr(self, src):
        """Copy attributes linked to the simulation, like convergence parameters."""
        self._log_file = src.log_file
        self.convergence_parameters = src.convergence_parameters
        self.solver = src.solver

        if src.comm is not None:
            raise ValueError("Checkpoints and MPI are not yet enabled.")

    def checkpoint_store(
        self,
        folder_name_output,
        dyn_checkpoint_file,
        int_str,
        checkpoint_indicator_file,
        is_dyn=False,
        jdic=None,
    ):
        """
        Store the tensor network as checkpoint.

        **Arguments**

        folder_name_output : str
            Name of the output folder, where we store checkpoints.

        dyn_checkpoint_file : str or `None`
            Name of the previous checkpoint file, which can be deleted after
            creating the new checkpoint.

        int_str : str
            Identifier containing integers as string to identify the checkpoint
            when loading in a potential future run.

        checkpoint_indicator_file: str
            Path to file which indicates if checkpoints exists.

        is_dyn : bool, optional
            Flag to indicate if checkpoint is for statics (False) or
            dynamics (True).
            Default to `False`.

        jdic : json-compatible structure or `None`, optional
            Store additional information as json.
            Default to `None` (store nothing).
        """
        prev_checkpoint_file = dyn_checkpoint_file
        dyn_stat_switch = "dyn" if is_dyn else "stat"
        dyn_checkpoint_file = os.path.join(
            folder_name_output, f"TTN_{dyn_stat_switch}_{int_str}"
        )
        self.save_pickle(dyn_checkpoint_file)

        if jdic is not None:
            with open(dyn_checkpoint_file + ".json", "w+") as fh:
                json.dump(jdic, fh, cls=QteaJsonEncoder)

        # Delete previous checkpoint
        if prev_checkpoint_file is not None:
            ext = ".pkl" + self.extension
            os.remove(prev_checkpoint_file + ext)

            if os.path.isfile(prev_checkpoint_file + ".json"):
                os.remove(prev_checkpoint_file + ".json")

        if not os.path.isfile(checkpoint_indicator_file):
            with open(checkpoint_indicator_file, "w+") as fh:
                pass

        return dyn_checkpoint_file

    def convert(self, dtype, device):
        """Convert data type and device inplace."""
        if isinstance(dtype, str):
            dtype = self.dtype_from_char(dtype)

        if (self.dtype == dtype) and (self.device == device):
            # Fast return, nothing to do
            self._convert_singvals(dtype, device)
            return

        for tensor in self._iter_tensors():
            tensor.convert(dtype, device)

        # Cannot update inplace in abstract class
        self._convert_singvals(dtype, device)

        if self.eff_op is not None:
            self.eff_op.convert(dtype, device)

    def dtype_from_char(self, dtype):
        """Resolve data type from chars C, D, S, Z and optionally H."""
        for tensor in self._iter_tensors():
            return tensor.dtype_from_char(dtype)

        raise Exception("Querying on empty tensor network.")

    def normalize(self):
        """
        Normalize the state depending on its current norm.
        """
        factor = 1.0 / self.norm()
        self.scale(factor)

    def log_close(self):
        """Close log file if open."""
        self._log_file.close()
        self._log_file = None

    def log_open(self, filename, mode="auto"):
        """Open a log file."""
        if mode == "auto":
            mode = "a" if os.path.isfile(filename) else "w+"

        # pylint: disable-next=consider-using-with
        self._log_file = open(filename, mode)

        if mode == "a":
            self.log_print("\n\n" + "=" * 80)
            self.log_print("APPENDING TO EXISTING LOG FILE")
            self.log_print("=" * 80 + "\n\n")

    def log_set_verbosity(self, verbosity):
        """Set the verbosity for print statements."""
        self._log_verbosity = verbosity

    def log_print(self, *args, verbosity_level=0):
        """Write to stdout or log file depending on setting."""
        if verbosity_level >= self._log_verbosity:
            return

        if self._log_file is None:
            print(*args)
        else:
            self._log_file.write(str(args))
            self._log_file.write("\n")

    def pre_timeevo_checks(self, raise_error=False):
        """Check if a TN ansatz is ready for time-evolution."""
        is_check_okay = True
        if not self.is_dtype_complex() and raise_error:
            raise Exception("Trying time evolution with real state.")

        if not self.is_dtype_complex():
            is_check_okay = False
            warn("Trying to run time evolution with real state.")

        return is_check_okay

    def _store_attr_for_pickle(self):
        """Return dictionary with attributes that cannot be pickled and unset them."""
        storage = {
            "conv_params": self._convergence_parameters,
            "log_file": self._log_file,
            "comm": self.comm,
            "solver": self._solver,
        }

        self._convergence_parameters = None
        self.comm = None
        self._log_file = None
        self._solver = None

        return storage

    def _restore_attr_for_pickle(self, storage):
        """Restore attributed removed for pickle from dictionary."""
        # Reset temporary removed attributes
        self._convergence_parameters = storage["conv_params"]
        self.comm = storage["comm"]
        self._log_file = storage["log_file"]
        self._solver = storage["solver"]

    def save_pickle(self, filename):
        """
        Save class via pickle-module.

        **Details**

        The following attributes have a special treatment and are not present
        in the copied object.

        * convergence_parameters
        * log file (filehandle)
        * MPI communicator
        """
        # Temporary remove objects which cannot be pickled which
        # included convergence parameters for lambda function and
        # parameterized variables, the log file as file handle and
        # the MPI communicator
        storage = self._store_attr_for_pickle()

        device = self.device
        if device != "cpu":
            # Assume pickle needs to be on host
            self.convert(None, "cpu")

        ext = "pkl" + self.extension
        if not filename.endswith(ext):
            filename += "." + ext

        with open(filename, "wb") as fh:
            pickle.dump(self, fh)

        # Check if we move back to the device where TN
        # was stored originally
        if device != "cpu":
            self.convert(None, device)

        self._restore_attr_for_pickle(storage)

    # pylint: disable-next=unused-argument
    def permute_spo_for_two_tensors(self, spo_list, theta, link_partner):
        """Returns permuted SPO list, permuted theta, and the inverse permutation."""
        return spo_list, theta, None

    # --------------------------------------------------------------------------
    #                                  Unsorted
    # --------------------------------------------------------------------------

    def _postprocess_singvals_cut(self, singvals_cut, conv_params=None):
        """
        Postprocess the singular values cut after the application of a
        tSVD based on the convergence parameters. Either take the sum of
        the singvals (if `conv_params.trunc_tracking_mode` is `"C"`) or the maximum
        (if `conv_params.trunc_tracking_mode` is `"M"`).

        Parameters
        ----------
        singvals_cut : np.ndarray
            Singular values cut in a tSVD
        conv_params : TNConvergenceParameters, optional
            Convergence parameters. If None, the convergence parameters
            of the tensor network class is used, by default None

        Returns
        -------
        float
            The processed singvals
        """
        if conv_params is None:
            conv_params = self._convergence_parameters
        # If no singvals was cut append a 0 to avoid problems
        if len(singvals_cut) == 0:
            return 0

        if conv_params.trunc_tracking_mode == "M":
            singvals_cut = singvals_cut.max()
        elif conv_params.trunc_tracking_mode == "C":
            singvals_cut = (singvals_cut**2).sum()
        else:
            raise Exception(f"Unkown trunc_tracking_mode {conv_params.trunc_method}")

        return singvals_cut

    #########################################
    ########## MEASUREMENT METHODS ##########
    #########################################

    def meas_local(self, op):
        """
        Measure a local observable along all sites of the MPS

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
        if op.ndim == 4:
            if op.shape[0] == 1 and op.shape[3] == 1:
                # Need copy, otherwise input tensor is modified ("passed-by-pointer")
                op = op.copy()
                op = op.remove_dummy_link(3).remove_dummy_link(0)

        # Always store on host
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

    def meas_magic(
        self, renyi_idx=2, num_samples=1000, return_probabilities=False, precision=14
    ):
        """
        Measure the magic of the state as defined
        in https://arxiv.org/pdf/2303.05536.pdf, with a given number of samples.
        To see how the procedure works see meas_unbiased_probabilities.

        Parameters
        ----------
        renyi_idx : int, optional
            Index of the renyi entropy you want to measure.
            If 1, measure the Von Neumann entropy. Default to 2.
        num_samples : int | List[int], optional
            Number of random number sampled for the unbiased probability measurement.
            If a List is passed, then the algorithm is run over several superiterations
            and each entry on num_samples is the number of samples of a superiteration.
            Default to 1000.
        return_probabilities : bool, optional
            If True, return the probability dict. Default to False.
        precision: int, optional
            Precision for the probability interval computation. Default to 14.
            For precision>15 mpmath is used, so a slow-down is expected.

        Returns
        -------
        float
            The magic of the state
        """
        if np.isscalar(num_samples):
            num_samples = [num_samples]

        # Sample the state probabilities
        opes_bound_probs = {}
        opes_probs = np.array([])
        for num_samp in num_samples:
            # Sample the numbers
            samples = np.random.rand(int(num_samp))
            # Do not perform the computation for the already sampled numbers
            probs, new_samples = _check_samples_in_bound_probs(
                samples, opes_bound_probs
            )
            opes_probs = np.hstack((opes_probs, probs))
            # Perform the sampling for the unseen samples
            bound_probs = self.meas_unbiased_probabilities(
                new_samples, mode="magic", precision=precision
            )
            opes_bound_probs.update(bound_probs)
            # Add the sampled probability to the numpy array
            probs, _ = _check_samples_in_bound_probs(new_samples, bound_probs)
            opes_probs = np.hstack((opes_probs, probs))

        # Compute the magic with the samples
        magic = -self.num_sites * np.log(2)
        # Pass from probability intervals to probability values
        if renyi_idx > 1:
            magic += np.log((opes_probs ** (renyi_idx - 1)).mean()) / (1 - renyi_idx)
        else:
            magic += -(np.log(opes_probs)).mean()

        if return_probabilities:
            return magic, opes_bound_probs
        else:
            return magic

    def meas_projective(
        self,
        nmeas=1024,
        qiskit_convention=False,
        seed=None,
        unitary_setup=None,
        do_return_probabilities=False,
    ):
        """
        Perform projective measurements along the computational basis state

        Parameters
        ----------
        nmeas : int, optional
            Number of projective measurements. Default to 1024.
        qiskit_convention : bool, optional
            If the sites during the measure are represented such that
            |201> has site 0 with value one (True, mimicks bits ordering) or
            with value 2 (False usually used in theoretical computations).
            Default to False.
        seed : int, optional
            If provided it sets the numpy seed for the random number generation.
            Default to None
        unitary_setup : `None` or :class:`UnitarySetupProjMeas`, optional
            If `None`, no local unitaries are applied during the projective
            measurements. Otherwise, the unitary_setup provides local
            unitaries to be applied before the projective measurement on
            each site.
            Default to `None`.
        do_return_probabilities : bool, optional
            If `False`, only the measurements are returned. If `True`,
            two arguments are returned where the first are the
            measurements and the second are their probabilities.
            Default to `False`

        Return
        ------
        measures : dict
            Dictionary where the keys are the states while the values the number of
            occurrences. The keys are separated by a comma if local_dim > 9.
        """
        if nmeas == 0:
            return {}

        if seed is not None and isinstance(seed, int):
            np.random.seed(seed)

        # Put in canonic form
        self.site_canonize(0)

        measures = []
        probabilities = []
        # Loop over number of measurements
        for _ in range(nmeas):
            state = np.zeros(self.num_sites, dtype=int)
            temp_tens = deepcopy(self.get_tensor_of_site(0))
            # Loop over tensors
            cumulative_prob = 1.0
            for ii in range(self.num_sites):
                target_prob = np.random.rand()
                measured_idx, temp_tens, prob_ii = self._get_child_prob(
                    temp_tens, ii, target_prob, unitary_setup, state, qiskit_convention
                )
                cumulative_prob *= prob_ii

                # Save the measured state either with qiskit or
                # theoretical convention
                if qiskit_convention:
                    state[self.num_sites - 1 - ii] = measured_idx
                else:
                    state[ii] = measured_idx

            if isinstance(self._local_dim, list):
                max_local_dim = np.max(self._local_dim)
            else:
                max_local_dim = self._local_dim.max()

            if max_local_dim < 10:
                measure_ii = np.array2string(
                    state, separator="", max_line_width=2 * self.num_sites
                )[1:-1]
            else:
                measure_ii = np.array2string(
                    state, separator=",", max_line_width=2 * self.num_sites
                )[1:-1]

            probabilities.append(cumulative_prob)

            # Come back to CPU if on GPU for list in measures (not needed since it is string)
            measures.append(measure_ii)

        measures = np.array(measures)
        states, counts = np.unique(measures, return_counts=True)
        probabilities = dict(zip(measures, probabilities))
        measures = dict(zip(states, counts))

        if do_return_probabilities:
            return measures, probabilities
        else:
            return measures

    def meas_unbiased_probabilities(
        self,
        num_samples,
        qiskit_convention=False,
        bound_probabilities=None,
        do_return_samples=False,
        precision=15,
        mode="projection_z",
    ):
        """
        Compute the probabilities of measuring a given state if its probability
        falls into the explored in num_samples values.
        The functions divide the probability space in small rectangles, draw
        num_samples random numbers and then follow the path until the end.
        The number of states in output is between 1 and num_samples.

        For a different way of computing the probability tree see the
        function :py:func:`meas_even_probabilities` or
        :py:func:`meas_greedy_probabilities`

        Parameters
        ----------
        num_samples : int
            Maximum number of states that could be measured.
        qiskit_convention : bool, optional
            If the sites during the measure are represented such that
            |201> has site 0 with value one (True, mimicks bits ordering) or
            with value 2 (False usually used in theoretical computations).
            Default to False.
        probability_bounds : dict, optional
            Bounds on the probability computed previously with this function,
            i.e. if a uniform random number has value
            `left_bound< value< right_bound` then you measure the state.
            The dict structure is `{'state' : (left_bound, right_bound)}`.
            If provided, it speed up the computations since the function will
            skip values in the intervals already known. By default None.
        do_return_samples : bool, optional
            Enables, if `True`, to return the random number used for sampling
            in addition to the `bound_probabilities`. If `False`, only the
            `bound_probabilities` are returned.
            Default to `False`
        precision : int, optional
            Decimal place precision for the mpmath package. It is only
            used inside the function, and setted back to the original after
            the computations. Default to 15.
            If it is 15 or smaller, it just uses numpy.
        mode : str, optional
            Mode of the unbiased sampling. Default is "projection_z", equivalent
            to sampling the basis states on the Z direction.
            Possibilities:
            - "projection_z"
            - "magic"

        Return
        ------
        bound_probabilities : dict
            Dictionary analogous to the `probability_bounds` parameter.
            The keys are separated by a comma if local_dim > 9.
        samples : np.ndarray
            Random numbers from sampling, only returned if activated
            by optional argument.
        """
        # Handle internal cache; keep if possible: if bound probabilities
        # are passed, it must be the same state and we can keep the
        # cache.
        do_clear_cache = bound_probabilities is None

        # Always set gauge to site=0; even if cache is not cleared,
        # the actual isometry center did not move
        self.site_canonize(0)

        # Normalize for quantum trajectories
        old_norm = self.norm()
        self.normalize()

        if mode == "projection_z":
            local_dim = self.local_dim
            get_children_prob = self._get_children_prob
            initial_tensor = self.get_tensor_of_site(0)
        elif mode == "magic":
            local_dim = np.repeat(4, self.num_sites)
            get_children_prob = self._get_children_magic
            tmp = self.get_tensor_of_site(0)
            initial_tensor = tmp.eye_like(tmp.links[0])
        else:
            raise ValueError(f"mode {mode} not available for unbiased sampling")

        # ==== Initialize variables ====
        # all_probs is a structure to keep track of already-visited nodes in
        # the probability tree. The i-th dictionary of the list correspond to
        # a state measured up to the i-th site. Each dictionary has the states
        # as keys and as value the list [state_prob, state_tens]
        all_probs = [{} for _ in range(self.num_sites)]
        # Initialize precision
        old_precision = mp.mp.dps
        # This precision is pretty much independent of the numpy-datatype as
        # it comes from multiplication. However, it is important when we sum
        # for the intervals
        mpf_wrapper, almost_equal = _mp_precision_check(precision)
        # Sample uniformly in 0,1 the samples, taking into account the already
        # sampled regions given by bound_probabilities
        if np.isscalar(num_samples):
            samples, bound_probabilities = _resample_for_unbiased_prob(
                num_samples, bound_probabilities
            )
        else:
            samples = num_samples
            bound_probabilities = (
                {} if bound_probabilities is None else bound_probabilities
            )
        # ==== Routine ====
        for idx, sample in enumerate(samples):
            # If the sample is in an already sampled area continue
            if idx > 0:
                if left_prob_bound < sample < left_prob_bound + cum_prob:
                    continue
            # Set the current state to no state
            curr_state = ""
            # Set the current tensor to be measured to the first one
            tensor = deepcopy(initial_tensor)
            # Initialize the probability to 1
            curr_prob = 1
            # Initialize left bound of the probability interval. Arbitrary precision
            left_prob_bound = mpf_wrapper(0.0)
            # Loop over the sites
            for site_idx in range(0, self.num_sites):
                # Initialize new possible states, adding the digits of the local basis to
                # the state measured up to now
                if site_idx > 0:
                    states = [
                        curr_state + f",{ii}" for ii in range(local_dim[site_idx])
                    ]
                else:
                    states = [curr_state + f"{ii}" for ii in range(local_dim[site_idx])]

                # Compute the children if we didn't already follow the branch
                if not np.all([ss in all_probs[site_idx] for ss in states]):
                    # Remove useless information after the first cycle. This operation is
                    # reasonable since the samples are ascending, i.e. if we switch path
                    # we will never follow again the old paths.
                    if idx > 0:
                        all_probs[site_idx:] = [
                            {} for _ in range(len(all_probs[site_idx:]))
                        ]

                    # Compute new probabilities
                    probs, tensor_list = get_children_prob(
                        tensor, site_idx, curr_state, do_clear_cache
                    )

                    # Clear cache only upon first iteration
                    do_clear_cache = False

                    # get probs to arbitrary precision
                    # if precision > 15:
                    #    probs = mp.matrix(probs)
                    # Multiply by the probability of being in the parent state
                    # Multiplication is safe from the precision point of view
                    probs = curr_prob * probs

                    # Update probability tracker for next branch, avoiding
                    # useless additional computations
                    for ss, prob, tens in zip(states, probs, tensor_list):
                        all_probs[site_idx][ss] = [prob, tens]

                # Retrieve values if already went down the path
                else:
                    probs = []
                    tensor_list = []
                    for prob, tens in all_probs[site_idx].values():
                        probs.append(prob)
                        tensor_list.append(tens)

                # Select the next branch if we didn't reach the leaves
                # according to the random number sampled
                if site_idx < self.num_sites - 1:
                    cum_probs = np.cumsum(probs)  # Compute cumulative
                    # Select first index where the sample is lower than the cumulative
                    try:
                        meas_idx = int(np.nonzero(sample < cum_probs)[0][0])
                    except IndexError:
                        break
                    # Update run-time values based on measured index
                    tensor = deepcopy(tensor_list[meas_idx])
                    curr_state = states[meas_idx]
                    curr_prob = probs[meas_idx]
                    # Update value of the sample based on the followed path
                    sample -= np.sum(probs[:meas_idx])
                    # Update left-boundary value with probability remaining on the left
                    # of the measured index
                    if meas_idx > 0:
                        left_prob_bound += cum_probs[meas_idx - 1]
                # Save values if we reached the leaves
                else:
                    cum_prob = mpf_wrapper(0.0)
                    for ss, prob in zip(states, probs):
                        if not almost_equal((prob, 0)):
                            bound_probabilities[ss] = (
                                left_prob_bound + cum_prob,
                                left_prob_bound + cum_prob + prob,
                            )
                        cum_prob += prob

            # For TTN with caching strategy (empy interface implemeted
            # also for any abstract tensor network)
            all_probs = self.clear_cache(all_probs=all_probs, current_key=curr_state)

        # Rewrite with qiskit convention and remove commas if needed
        bound_probabilities = postprocess_statedict(
            bound_probabilities,
            local_dim=self.local_dim,
            qiskit_convention=qiskit_convention,
        )

        self.scale(old_norm)
        mp.mp.dps = old_precision

        if do_return_samples:
            return bound_probabilities, samples

        return bound_probabilities

    def _get_children_prob(self, tensor, site_idx, curr_state, do_clear_cache):
        """
        Compute the probability and the relative tensor state of all the
        children of site `site_idx` in the probability tree

        Parameters
        ----------

        tensor : np.ndarray
            Parent tensor, with respect to which we compute the children

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
        # Cannot implement it here, it highly depends on the TN
        # geometry
        raise NotImplementedError("This function has to be overwritten.")

    def _get_children_magic(
        self, transfer_matrix, site_idx, curr_state, do_clear_cache
    ):
        """
        Compute the magic probability and the relative tensor state of all the
        children of site `site_idx` in the probability tree, conditioned on
        the transfer matrix

        Parameters
        ----------

        transfer_matrix : np.ndarray
            Parent tranfer matrix, with respect to which we compute the children

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
        # Cannot implement it here, it highly depends on the TN
        # geometry
        raise NotImplementedError("This function has to be overwritten.")

    def clear_cache(self, num_qubits_keep=None, all_probs=None, current_key=None):
        """
        Clear cache until cache size is below cache limit again. This function
        is empty and works for any tensor network without cache. If the inhereting
        tensor network has a cache, it has to be overwritten.

        **Arguments**

        all_probs : list of dicts
            Contains already calculated branches of probability tree. Each
            TTN has to decide if they need to be cleaned up as well.
        """
        if self is None:
            # Never true, but prevent linter warning (needs self when
            # cache is actually defined) and unused arguments
            print("Args", num_qubits_keep, all_probs, current_key)
            return None

        return all_probs

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
        # Cannot implement it here, it highly depends on the TN
        # geometry
        raise NotImplementedError("This function has to be overwritten.")

    def compute_energy(self, pos=None):
        """
        Compute the energy of the TTN through the effective operator
        at position pos.

        Parameters
        ----------
        pos : list, optional
            If a position is provided, the isometry is first shifted to
            that position and then the energy is computed. If None,
            the current isometry center is computed, by default None

        Returns
        -------
        float
            Energy of the TTN
        """

        if self.eff_op is None:
            warn("Tried to compute energy with no effective operators. Returning nan")
            return np.nan
        # Move the iso center if needed
        if pos is not None:
            self.iso_towards(pos)
        else:
            pos = self.iso_center
            if not np.isscalar(pos):
                pos = tuple(pos)

        # Retrieve the tensor at the isometry
        tens = self[self.iso_center]

        # Get the list of operators to contract
        pos_links = self.get_pos_links(pos)

        # Contract the tensor with the effective operators around
        vec = self.eff_op.contract_tensor_lists(tens, pos, pos_links)

        energy = tens.dot(vec)

        # Update internal storage
        self._prev_energy = energy

        return np.real(tens.get_of(energy))

    #########################################################################
    ######################### Optimization methods ##########################
    #########################################################################

    def optimize_single_tensor(self, pos):
        """
        Optimize the tensor at position `pos` based on the
        effective operators loaded in the TTN

        Parameters
        ----------
        pos : list of ints or int
            Position of the tensor in the TN

        Returns
        -------
        float
            Computed energy
        """
        tic = tictoc()
        self.log_print("-" * 50, verbosity_level=2)
        self.log_print(f"Optimizing tensor {pos}", verbosity_level=2)

        # Isometrise towards the desired tensor
        self.iso_towards(pos)
        pos_links = self.get_pos_links(pos)

        dim_problem = np.prod(self[pos].shape)
        if dim_problem == 1:
            # Nothing to do - ARPACK will fail
            eigenvalue = self.compute_energy()
            return eigenvalue

        # Retrieve the tensor
        eigenvalues, tensor = self[pos].eig_api(
            self.eff_op.contract_tensor_lists,
            self[pos].shape,
            self._convergence_parameters,
            args_func=(pos, pos_links),
        )

        self.log_print(f"New energy is E={np.real(eigenvalues[0])}", verbosity_level=2)
        self.log_print(f"Computational time {tictoc()-tic}", verbosity_level=2)
        self.log_print("-" * 50, verbosity_level=2)

        self[pos] = tensor

        # Update internal storage
        self._prev_energy = eigenvalues[0]

        return np.real(tensor.get_of(eigenvalues[0]))

    def optimize_link_expansion(
        self,
        pos,
        pos_partner,
        link_self,
        link_partner,
    ):
        """
        Optimize a tensor pair via a space-link expansion.

        **Arguments**

        pos : int, tuple of ints (depending on TN)
            position of tensor to be optimized

        pos_partner : int, tuple of ints (depending on TN)
            position of partner tensor, where link between
            tensor and partner tensor will be randomly
            expandend.

        link_self : int
            Link connecting to partner tensor (in tensor at `pos`)

        link_partner : int
            Link connecting to optimized tensors (in partner tensor).

        requires_singvals : bool
            Flag if calling methods upstream need singular values, i.e.,
            want to replace QR with SVDs

        Returns
        -------
        float
            Computed energy
        """
        if isinstance(pos, list):
            raise Exception("Passing list as position")
        if isinstance(pos_partner, list):
            raise Exception("Passing list as partner position")

        # Here it would be beneficial to implement the skip_exact_rgtensors, but
        # we would need to add a data structure to flag which tensors are converged.
        # After that, when moving the iso with svd we can easily understand if there
        # is truncation
        # _ = self._convergence_parameters.sim_params["skip_exact_rgtensors"]
        self.iso_towards(pos_partner)

        tensor = self[pos].copy()
        tensor_partner = self[pos_partner].copy()

        # If energy goes up and we want to reinstall original tensor
        if self._prev_energy is None:
            self._prev_energy = self.compute_energy()
        prev_tensor = tensor.copy()
        prev_tensor_partner = tensor_partner.copy()

        new_dim = (
            tensor.shape[link_self]
            + self._convergence_parameters.sim_params["min_expansion"]
        )

        self[pos], self[pos_partner] = tensor.expand_link_tensorpair(
            tensor_partner,
            link_self,
            link_partner,
            new_dim,
        )

        # Ideal implementation would be ...
        # First iso_towards to pos_partner, as well as pos_partner
        # after decision.

        # Update of eff operators (internal iso_towards in space link
        # expansion cannot truncate or update singvals)
        self.iso_towards(pos)

        # Random entries destroyed normalization, to get valid
        # eigenvalue in these intermediate steps, need to renormalize
        self.normalize()

        # Expansion cycles
        # ----------------

        # Same here, use QR as otherwise truncation kicks in potentially]
        # undoing the expansion. Final iso_towards with QR or SVD follows
        # after expansion cycles.
        requires_singvals = self._requires_singvals
        self._requires_singvals = False

        for _ in range(self._convergence_parameters.sim_params["expansion_cycles"]):
            self.iso_towards(pos_partner)
            energy = self.optimize_single_tensor(pos_partner)

            self.iso_towards(pos)
            energy = self.optimize_single_tensor(pos)

        # Reset value
        self._requires_singvals = requires_singvals

        # Decision on accepting update
        # ----------------------------

        expansion_drop = self._convergence_parameters.sim_params["expansion_drop"]

        if energy <= self._prev_energy or expansion_drop in ["f"]:
            # We improved in energy or accept higher energies to escape local
            # minima in this sweep
            self.iso_towards(
                pos_partner,
                keep_singvals=requires_singvals,
                trunc=True,
                conv_params=self._convergence_parameters,
            )
        elif expansion_drop in ["o"]:
            # Energy did not improve, but optimize locally
            self[pos] = prev_tensor
            self[pos_partner] = prev_tensor_partner

            # Iso center before copy was at pos_partner
            self.iso_center = pos_partner

            self.iso_towards(
                pos, trunc=requires_singvals, keep_singvals=requires_singvals
            )
            energy = self.optimize_single_tensor(pos)

        elif expansion_drop in ["d"]:
            # Energy did not improve, reinstall previous tensors, discard
            # step and do not optimize even locally
            self[pos] = prev_tensor
            self[pos_partner] = prev_tensor_partner

            # Iso center before copy was at pos_partner
            self.iso_center = pos_partner

        # iso_towards does not normalize (maybe it does inside the truncate methods ...)
        self.normalize()

        return energy

    #########################################################################
    ######################## Time evolution methods #########################
    #########################################################################

    def timestep_single_tensor(self, pos, next_pos, sc):
        """
        Time step for a single-tensor update on a single tensor `exp(sc*Heff*dt)`.

        Parameters
        ----------
        pos : Tuple[int] | int
            Position in the TN of the tensor to time-evolve
        next_pos: Tuple[int] | int
            Position in the TN of the next tensor to time-evolve
        sc : complex
            Multiplicative factor in the exponent `exp(sc*Heff*dt)`

        Return
        ------
        None
            Acts in place

        """
        self.log_print("Time-step at tensor", pos, next_pos, verbosity_level=3)
        self.log_print(
            "Time step at tensor's norm, scalar", self.norm(), sc, verbosity_level=5
        )

        # Isometrize towards the desired tensor
        self.iso_towards(pos)
        pos_links = self.get_pos_links(pos)

        krylov_solver = self._solver(
            self[pos],
            sc,
            self.eff_op.contract_tensor_lists,
            self._convergence_parameters,
            args_func=(pos, pos_links),
        )

        self[pos] = krylov_solver.solve()

        if next_pos is not None:
            # Have to evolve backwards
            # ------------------------
            #
            # This is a bit inconvenient, because we have to shift the isometry
            # center by hand as the r-tensor has to be evolved backwards in time.
            (
                rtens,
                pos_partner,
                link_partner,
                path_elem,
            ) = self._partial_iso_towards_for_timestep(pos, next_pos)

            # Retrieve operator from partner to iso center
            ops_a = self.eff_op[(pos_partner, pos)]

            # Path elem src layer-tensor-link, dst layer-tensor-link
            self._update_eff_ops(path_elem)

            # Needing just one operators, no idxs needed
            ops_b = self.eff_op[(pos, pos_partner)]

            # Assumed to be in the order of links
            ops_list_reverse = [ops_b, ops_a]

            krylov_solver = self._solver(
                rtens,
                -sc,
                self.eff_op.contract_tensor_lists,
                self._convergence_parameters,
                args_func=(None, None),
                kwargs_func={"custom_ops": ops_list_reverse},
            )

            rtens = krylov_solver.solve()

            tmp = rtens.tensordot(self[pos_partner], ([1], [link_partner]))
            if link_partner == 0:
                self[pos_partner] = tmp
            else:
                nn = self[pos_partner].ndim
                perm = (
                    list(range(1, link_partner + 1))
                    + [0]
                    + list(range(link_partner + 1, nn))
                )
                self[pos_partner] = tmp.transpose(perm)

            self.iso_center = pos_partner

        return

    def timestep_two_tensors(self, pos, next_pos, sc, skip_back):
        """
        Time step for a single-tensor update on two tensors `exp(sc*Heff*dt)`.

        Parameters
        ----------
        pos : Tuple[int] | int
            Position in the TN of the tensor to time-evolve
        next_pos: Tuple[int] | int
            Position in the TN of the next tensor to time-evolve
        sc : complex
            Multiplicative factor in the exponent `exp(sc*Heff*dt)`
        skip_back : bool
            Flag if backwards propagation of partner tensor can be skipped;
            used for last two tensors, partner tensor must be next position
            as well.

        Return
        ------
        None
            Acts in place

        """
        self.log_print("Time-step at tensor", pos, verbosity_level=3)

        # Isometrize towards the desired tensor
        self.iso_towards(pos)

        # pos_partner, link_pos, link_partner = self.get_pos_partner_link_expansion(pos)
        (
            link_pos,
            pos_partner,
            link_partner,
            path_elem,
        ) = self._partial_iso_towards_for_timestep(pos, next_pos, no_rtens=True)

        tens_a = self[pos]
        tens_b = self[pos_partner]
        is_a_outgoing = tens_a.are_links_outgoing[link_pos]

        theta = tens_a.tensordot(tens_b, ([link_pos], [link_partner]))

        # Build custom eff ops list
        custom_ops = []
        for ii, elem in enumerate(self.get_pos_links(pos)):
            if ii == link_pos:
                continue

            if elem is None:
                custom_ops.append(None)
            else:
                custom_ops.append(self.eff_op[(elem, pos)])

        for ii, elem in enumerate(self.get_pos_links(pos_partner)):
            if ii == link_partner:
                continue

            if elem is None:
                custom_ops.append(None)
            else:
                custom_ops.append(self.eff_op[(elem, pos_partner)])

        custom_ops, theta, inv_perm = self.permute_spo_for_two_tensors(
            custom_ops, theta, link_partner
        )
        krylov_solver = self._solver(
            theta,
            sc,
            self.eff_op.contract_tensor_lists,
            self._convergence_parameters,
            args_func=(None, None),
            kwargs_func={"custom_ops": custom_ops},
        )

        theta = krylov_solver.solve()

        if inv_perm is not None:
            theta.transpose_update(inv_perm)

        links_a = list(range(tens_a.ndim - 1))
        links_b = list(range(tens_a.ndim - 1, theta.ndim))

        tens_a, tens_b, svals, svals_cut = theta.split_svd(
            links_a,
            links_b,
            contract_singvals="R",
            conv_params=self._convergence_parameters,
            is_link_outgoing_left=is_a_outgoing,
        )

        svals_cut = self._postprocess_singvals_cut(
            singvals_cut=svals_cut, conv_params=self._convergence_parameters
        )
        svals_cut = theta.get_of(svals_cut)

        self.set_singvals_on_link(pos, pos_partner, svals)

        nn = tens_a.ndim
        perm_a = list(range(link_pos)) + [nn - 1] + list(range(link_pos, nn - 1))
        self[pos] = tens_a.transpose(perm_a)

        nn = tens_b.ndim
        perm_b = (
            list(range(1, link_partner + 1)) + [0] + list(range(link_partner + 1, nn))
        )
        self[pos_partner] = tens_b.transpose(perm_b)

        self._update_eff_ops(path_elem)
        self.iso_center = pos_partner

        if not skip_back:
            # Have to evolve backwards
            # ------------------------

            pos_links = self.get_pos_links(pos_partner)

            krylov_solver = self._solver(
                self[pos_partner],
                -sc,
                self.eff_op.contract_tensor_lists,
                self._convergence_parameters,
                args_func=(pos_partner, pos_links),
            )

            self[pos_partner] = krylov_solver.solve()
        elif pos_partner != next_pos:
            raise Exception("Sweep order incompatible with two-tensor update.")

        return

    def timestep_single_tensor_link_expansion(self, pos, next_pos, sc):
        """
        Time step for a single-tensor update on two tensors `exp(sc*Heff*dt)`.

        Parameters
        ----------
        pos : Tuple[int] | int
            Position in the TN of the tensor to time-evolve
        next_pos: Tuple[int] | int
            Position in the TN of the next tensor to time-evolve
        sc : complex
            Multiplicative factor in the exponent `exp(sc*Heff*dt)`

        Return
        ------
        None
            Acts in place

        """
        requires_singvals = True
        self.log_print(
            "Time-step with link expansion at tensor", pos, verbosity_level=3
        )

        if next_pos is None:
            self.timestep_single_tensor(pos, next_pos, sc)
            return

        self.iso_towards(
            next_pos, trunc=requires_singvals, keep_singvals=requires_singvals
        )

        (
            link_self,
            pos_partner,
            link_partner,
            _,
        ) = self._partial_iso_towards_for_timestep(pos, next_pos, no_rtens=True)

        tensor = self[pos].copy()
        tensor_partner = self[pos_partner].copy()

        # Expand the tensors
        option_a = (
            tensor.shape[link_self]
            + self._convergence_parameters.sim_params["min_expansion"]
        )
        option_b = 2 * tensor.shape[link_self]
        option_c = np.delete(list(tensor.shape), link_self).prod()

        new_dim = min(option_a, min(option_b, option_c))

        self[pos], self[pos_partner] = tensor.expand_link_tensorpair(
            tensor_partner, link_self, link_partner, new_dim, ctrl="Z"
        )

        # Update of eff operators (internal iso_towards in space link
        # expansion cannot truncate or update singvals)
        self.iso_towards(pos)

        # Expansion cycles
        # ----------------

        # Same here, use QR as otherwise truncation kicks in potentially]
        # undoing the expansion. Final iso_towards with QR or SVD follows
        # after expansion cycles.
        exp_cycles = self._convergence_parameters.sim_params["expansion_cycles"]

        sc_e = sc / exp_cycles
        for ii in range(exp_cycles):
            self.iso_towards(pos)
            self.timestep_single_tensor(pos, pos_partner, sc_e)

            if exp_cycles > 1:
                next_pos_partner = pos if ii < exp_cycles - 1 else None
                self.timestep_single_tensor(pos_partner, next_pos_partner, sc_e)

        # Evolve back the tensor at pos_partner
        if exp_cycles > 1:
            self.timestep_single_tensor(pos_partner, None, -sc)
            self.iso_towards(
                pos, trunc=requires_singvals, keep_singvals=requires_singvals
            )
            self.iso_towards(
                pos_partner, trunc=requires_singvals, keep_singvals=requires_singvals
            )

        return

    def timestep(self, dt, mode, sweep_order=None, sweep_order_back=None):
        """
        Evolve the Tensor network for one timestep.

        Parameters
        ----------
        mode : int
            Currently encoded are single-tensor TDVP first order (1), two-tensor
            TDVP first order (2), two-tensor TDVP second order (3), and single-tensor
            TDVP second order (4). A flex-TDVP as (5) is pending.
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`
        sweep_order_back : List[int] | None
            Order in which we iterate backwards through the network for the timestep.
            If None, use the default in `self.default_sweep_order()[::-1]`
        dt : float
            Timestep

        Returns
        -------
        None
            Acts in place

        Details
        -------

        Flex-TDVP in the fortran implementation was using two-tensor updates
        as long as the maximal bond dimension is not reached and then a ratio
        of 9 single-tensor updates to 1 two-tensor update step.
        """
        if mode == 1:
            self.timestep_mode_1(dt, sweep_order=sweep_order)
        elif mode == 2:
            self.timestep_mode_2(dt, sweep_order=sweep_order)
        elif mode == 3:
            self.timestep_mode_3(
                dt,
                sweep_order=sweep_order,
                sweep_order_back=sweep_order_back,
            )
        elif mode == 4:
            self.timestep_mode_4(
                dt,
                sweep_order=sweep_order,
                sweep_order_back=sweep_order_back,
            )
        elif mode == 5:
            self.timestep_mode_5(dt, sweep_order=sweep_order)
        else:
            raise ValueError(f"Time evolution mode {mode} not available.")

    def timestep_mode_1(self, dt, sweep_order=None):
        """
        Evolve the Tensor network for one timestep (single-tensor update
        1st order).

        Parameters
        ----------
        dt : float
            Timestep
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`

        Returns
        -------
        None
            Acts in place
        """
        if sweep_order is None:
            sweep_order = self.default_sweep_order()

        for ii, pos in enumerate(sweep_order):
            # 1st order update
            next_pos = None if (ii + 1 == len(sweep_order)) else sweep_order[ii + 1]
            self.timestep_single_tensor(pos, next_pos, -1j * dt)

    def timestep_mode_2(self, dt, sweep_order=None):
        """
        Evolve the Tensor network for one timestep (two-tensor update
        1st order).

        Parameters
        ----------
        dt : float
            Timestep
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`

        Returns
        -------
        None
            Acts in place
        """
        if sweep_order is None:
            sweep_order = self.default_sweep_order()

        for ii, pos in enumerate(sweep_order):
            # 1st order update
            next_pos = None if (ii + 1 == len(sweep_order)) else sweep_order[ii + 1]
            skip_back = ii + 2 == len(sweep_order)
            self.timestep_two_tensors(pos, next_pos, -1j * dt, skip_back)

            if skip_back:
                break

    def timestep_mode_3(self, dt, sweep_order=None, sweep_order_back=None):
        """
        Evolve the Tensor network for one timestep (two-tensor update
        2nd order).

        Parameters
        ----------
        dt : float
            Timestep
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`
        sweep_order_back : List[int] | None
            Order in which we iterate backwards through the network for the timestep.
            If None, use the default in `self.default_sweep_order()[::-1]`

        Returns
        -------
        None
            Acts in place
        """
        self.timestep_mode_2(0.5 * dt, sweep_order=sweep_order)

        if sweep_order_back is None:
            sweep_order_back = self.default_sweep_order_back()

        self.timestep_mode_2(0.5 * dt, sweep_order=sweep_order_back)

    def timestep_mode_4(self, dt, sweep_order=None, sweep_order_back=None):
        """
        Evolve the Tensor network for one timestep (single-tensor update
        2nd order).

        Parameters
        ----------
        dt : float
            Timestep
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`
        sweep_order_back : List[int] | None
            Order in which we iterate backwards through the network for the timestep.
            If None, use the default in `self.default_sweep_order()[::-1]`

        Returns
        -------
        None
            Acts in place
        """
        self.timestep_mode_1(0.5 * dt, sweep_order=sweep_order)

        if sweep_order_back is None:
            sweep_order_back = self.default_sweep_order_back()

        self.timestep_mode_1(0.5 * dt, sweep_order=sweep_order_back)

    def timestep_mode_5(self, dt, sweep_order=None, stride_two_tensor=10):
        """
        Evolve the Tensor network for one timestep (mixed two-tensor and
        one-tensor update, first order).

        Parameters
        ----------
        dt : float
            Timestep
        sweep_order : List[int] | None
            Order in which we iterate through the network for the timestep.
            If None, use the default in `self.default_sweep_order()`
        stride_two_tensor: int
            If maximum bond dimension is reached, do a two-tensor update
            every `stride_two_tensor` steps.

        Returns
        -------
        None
            Acts in place
        """
        if sweep_order is None:
            sweep_order = self.default_sweep_order()

        idx = self._timestep_mode_5_counter
        self._timestep_mode_5_counter += 1

        # For the main loop, we always evolve the R-tensor back in time
        skip_back = False

        for ii, pos in enumerate(sweep_order[:-2]):
            # Everything but the last two
            next_pos = sweep_order[ii + 1]

            link_pos, _, _, _ = self._partial_iso_towards_for_timestep(
                pos, next_pos, no_rtens=True
            )

            is_link_full = self[pos].is_link_full(link_pos)
            enforce_two_tensor = idx % stride_two_tensor == 0
            do_two_tensor = (not is_link_full) or enforce_two_tensor

            if do_two_tensor:
                self.timestep_two_tensors(pos, next_pos, -1j * dt, skip_back)
            else:
                self.timestep_single_tensor(pos, next_pos, -1j * dt)

        # Treat the last two tensors (cannot decide individually on update-scheme)
        pos = sweep_order[-2]
        next_pos = sweep_order[-1]
        link_pos, pos_partner, link_partner, _ = self._partial_iso_towards_for_timestep(
            pos, next_pos, no_rtens=True
        )

        is_link_full_a = self[pos].is_link_full(link_pos)
        is_link_full_b = self[pos_partner].is_link_full(link_partner)
        is_link_full = is_link_full_a or is_link_full_b
        enforce_two_tensor = idx % stride_two_tensor == 0
        do_two_tensor = (not is_link_full) or enforce_two_tensor

        if do_two_tensor:
            skip_back = True
            self.timestep_two_tensors(pos, next_pos, -1j * dt, True)
        else:
            self.timestep_single_tensor(pos, next_pos, -1j * dt)
            self.timestep_single_tensor(next_pos, None, -1j * dt)

    #########################################################################
    ########################## Observables methods ##########################
    #########################################################################
    def check_obs_input(self, ops, idxs=None):
        """
        Check if the observables are in the right
        format

        Parameters
        ----------
        ops : list of np.ndarray or np.ndarray
            Observables to measure
        idxs: list of ints, optional
            If has len>0 we expect a list of operators, otherwise just one.

        Return
        ------
        None
        """
        if np.isscalar(self.local_dim):
            local_dim = np.repeat(self.local_dim, self.num_sites)
        else:
            local_dim = self.local_dim
        if not np.all(np.array(local_dim) == local_dim[0]):
            raise RuntimeError("Measurement not defined for non-constant local_dim")

        if idxs is None:
            ops = [ops]

        # for op in ops:
        #    if list(op.shape) != [local_dim[0]] * 2:
        #        raise ValueError(
        #            "Input operator should be of shape (local_dim, local_dim)"
        #        )

        if idxs is not None:
            if len(idxs) != len(ops):
                raise ValueError(
                    "The number of indexes must match the number of operators"
                )

    #########################################################################
    ############################## MPI methods ##############################
    #########################################################################
    def _initialize_mpi(self):
        if (MPI is not None) and (MPI.COMM_WORLD.Get_size() > 1):
            self.comm = MPI.COMM_WORLD

    def mpi_send_tensor(self, tensor, to_):
        """
        Send the tensor in position `tidx` to the process
        `to_`.

        Parameters
        ----------
        tensor : xp.ndarray
            Tensor to send
        to_ : int
            Index of the process where to send the tensor

        Returns
        -------
        None
        """
        tensor.mpi_send(to_, self.comm, TN_MPI_TYPES)

    def mpi_receive_tensor(self, from_):
        """
        Receive the tensor from the process `from_`.


        Parameters
        ----------
        from_ : int
            Index of the process that sent the tensor

        Returns
        -------
        xp.ndarray
            Received tensor
        """
        return self._tensor_backend.tensor_cls.mpi_recv(
            from_, self.comm, TN_MPI_TYPES, self._tensor_backend
        )

    def reinstall_isometry_parallel(self, *args, **kwargs):
        """
        Reinstall the isometry in a parallel TN parallely
        """
        # Empty on porpouse: depends on TN ansatz and
        # it is used ONLY for MPI-distributed ansatzes

    def reinstall_isometry_serial(self, *args, **kwargs):
        """
        Reinstall the isometry in a parallel TN serially
        """
        # Empty on porpouse: depends on TN ansatz and
        # it is used ONLY for MPI-distributed ansatzes

    @staticmethod
    def matrix_to_tensorlist(
        matrix, n_sites, dim, conv_params, tensor_backend=TensorBackend()
    ):
        """
        For a given matrix returns dense MPO form decomposing with SVDs

        Parameters
        ----------
        matrix : ndarray
            Matrix to write in LPTN(MPO) format
        n_sites : int
            Number of sites
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
        List[QteaTensor]
            List of tensor, the MPO decomposition of the matrix
        """

        if not isinstance(matrix, tensor_backend.tensor_cls):
            matrix = tensor_backend.tensor_cls.from_elem_array(matrix)

        bond_dim = 1
        tensorlist = []
        work = matrix
        for ii in range(0, n_sites - 1):
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
                    dim ** (n_sites - 1 - ii),
                    dim,
                    dim ** (n_sites - 1 - ii),
                ),
            )
            tens_left, work, _, _ = work.split_svd(
                [0, 1, 3], [2, 4], contract_singvals="R", conv_params=conv_params
            )
            tensorlist.append(tens_left)
            bond_dim = deepcopy(work.shape[0])
        work = work.reshape((work.shape[0], dim, dim, 1))
        tensorlist.append(work)

        return tensorlist


def postprocess_statedict(state_dict, local_dim=2, qiskit_convention=False):
    """
    Remove commas from the states defined as keys of statedict
    and, if `qiskit_convention=True` invert the order of the
    digits following the qiskit convention

    Parameters
    ----------
    state_dict : dict
        State dictionary, which keys should be of the format
        'd,d,d,d,d,...,d' with d from 0 to local dimension
    local_dim : int or array-like of ints, optional
        Local dimension of the sites. Default to 2
    qiskit_convention : bool, optional
        If True, invert the digit ordering to follow qiskit
        convention

    Return
    ------
    dict
        The postprocessed state dictionary
    """
    # Check on parameter
    if np.isscalar(local_dim):
        local_dim = [local_dim]

    postprocecessed_state_dict = {}
    for key, val in state_dict.items():
        # If the maximum of the local_dim is <10
        # remove the comma, since the definition
        # is not confusing
        if np.max(local_dim) < 10:
            key = key.replace(",", "")
        # Invert the values if qiskit_convention == True
        if qiskit_convention:
            postprocecessed_state_dict[key[::-1]] = val
        else:
            postprocecessed_state_dict[key] = val

    return postprocecessed_state_dict


def _resample_for_unbiased_prob(num_samples, bound_probabilities):
    """
    Sample the `num_samples` samples in U(0,1) to use in the function
    :py:func:`meas_unbiased_probabilities`. If `bound_probabilities`
    is not None, then the function checks that the number of samples
    outside the ranges already computed in bound_probabilities are
    not in total num_samples. The array returned is sorted ascendingly

    Parameters
    ----------
    num_samples : int
        Number of samples to be drawn for :py:func:`meas_unbiased_probabilities`
    bound_probabilities : dict or None
        See :py:func:`meas_unbiased_probabilities`.

    Return
    ------
    np.ndarray
        Sorted samples in (0,1)
    dict
        Empty dictionary if bound_probabilities is None, otherwise the
        bound_probabilities input parameter.
    """
    if (bound_probabilities is None) or (len(bound_probabilities) == 0):
        # Contains the boundary probability of measuring the state, i.e. if a uniform
        # random number has value left_bound< value< right_bound then you measure the
        # state. The dict structure is {'state' : [left_bound, right_bound]}
        bound_probabilities = {}
        samples = np.random.uniform(0, 1, num_samples)
    else:
        # Prepare the functions to be used later on based on precision
        mpf_wrapper, almost_equal = _mp_precision_check(mp.mp.dps)
        # Go on and sample until you reach an effective number of num_samples,
        # withouth taking into account those already sampled in the given
        # bound_probabilities
        bounds_array = np.zeros((len(bound_probabilities), 2))
        for idx, bound in enumerate(bound_probabilities.values()):
            bounds_array[idx, :] = bound
        bounds_array = bounds_array[bounds_array[:, 0].argsort()]

        # Immediatly return if almost all the space has been measured
        if almost_equal(
            (np.sum(bounds_array[:, 1] - bounds_array[:, 0]), mpf_wrapper(1.0))
        ):
            return np.random.uniform(0, 1, 1), bound_probabilities

        # Sample unsampled areas. First, prepare array for sampling
        array_for_sampling = []
        last_bound = 0
        last_idx = 0
        while not almost_equal((last_bound, mpf_wrapper(1.0))):
            # Skip if interval already measured
            if last_idx < len(bounds_array) and almost_equal(
                (last_bound, bounds_array[last_idx, 0])
            ):
                last_bound = bounds_array[last_idx, 1]
                last_idx += 1
            # Save interval
            else:
                if 0 < last_idx < len(bounds_array):
                    array_for_sampling.append(
                        [bounds_array[last_idx - 1, 1], bounds_array[last_idx, 0]]
                    )
                    last_bound = bounds_array[last_idx, 0]
                elif last_idx == len(bounds_array):
                    array_for_sampling.append([bounds_array[last_idx - 1, 1], 1])
                    last_bound = 1
                else:  # Initial case
                    array_for_sampling.append([0, bounds_array[last_idx, 0]])
                    last_bound = bounds_array[last_idx, 0]

        nparray_for_sampling = np.array(array_for_sampling)
        # Sample from which intervals you will sample
        sample_prob = nparray_for_sampling[:, 1] - nparray_for_sampling[:, 0]
        sample_prob /= np.sum(sample_prob)
        intervals_idxs = np.random.choice(
            np.arange(len(array_for_sampling)),
            size=num_samples,
            replace=True,
            p=sample_prob,
        )
        intervals_idxs, num_samples_per_interval = np.unique(
            intervals_idxs, return_counts=True
        )

        # Finally perform uniform sampling
        samples = np.zeros(1)
        for int_idx, num_samples_int in zip(intervals_idxs, num_samples_per_interval):
            interval = nparray_for_sampling[int_idx, :]
            samples = np.hstack(
                (samples, np.random.uniform(*interval, size=num_samples_int))
            )
        samples = samples[1:]

    # Sort the array
    samples = np.sort(samples)

    return samples, bound_probabilities


def _projector(idxs, shape, xp=np):
    """
    Generate a projector of a given shape on the
    subspace identified by the indexes idxs

    Parameters
    ----------
    idxs : int or array-like of ints
        Indexes where the diagonal of the projector is 1,
        i.e. identifying the projector subspace
    shape : int or array-like of ints
        Dimensions of the projector. If an int, it is
        assumed a square matrix
    xp : module handle
        Module handle for the creation of the projector.
        Possible are np (cpu) or cp (cpu). Default to np.
    """
    if np.isscalar(idxs):
        idxs = [idxs]
    if np.isscalar(shape):
        shape = (shape, shape)

    idxs = np.array(idxs, dtype=int)
    projector = xp.zeros(shape)
    projector[idxs, idxs] = 1
    return projector


def _projector_for_rho_i(idxs, rho_i):
    """
    Generate a projector of a given shape on the
    subspace identified by the indexes idxs

    Parameters
    ----------
    idxs : int or array-like of ints
        Indexes where the diagonal of the projector is 1,
        i.e. identifying the projector subspace
    shape : int or array-like of ints
        Dimensions of the projector. If an int, it is
        assumed a square matrix
    xp : module handle
        Module handle for the creation of the projector.
        Possible are np (cpu) or cp (cpu). Default to np.
    """
    if np.isscalar(idxs):
        idxs = [idxs]

    projector = rho_i.zeros_like()
    for ii in idxs:
        projector.set_diagonal_entry(ii, 1.0)

    return projector


def _mp_precision_check(precision):
    """
    Based on the precision selected, gives
    a wrapper around the initialization of
    variables and almost equal check.
    In particolar, if `precision>15`,
    use mpmath library

    Parameters
    ----------
    precision : int
        Precision of the computations

    Return
    ------
    callable
        Initializer for variables
    callable
        Almost equal check for variables
    """
    if precision > 15:
        mpf_wrapper = lambda x: mp.mpf(x)
        almost_equal = lambda x: mp.almosteq(
            x[0], x[1], abs_eps=mp.mpf(10 ** (-precision))
        )
    else:
        mpf_wrapper = lambda x: x
        almost_equal = lambda x: np.isclose(x[0], x[1], atol=10 ** (-precision), rtol=0)

    return mpf_wrapper, almost_equal


def _check_samples_in_bound_probs(samples, bound_probabilities):
    """
    Check if the samples are falling in the probability intervals
    defined by the dictionary bound_probabilities, received as
    output by the OPES/unbiased sampling

    Parameters
    ----------
    samples : np.ndarray
        List of samples
    bound_probabilities : dict
        Dictionary of bound probabilities, where the key is the
        measure and the values the intervals of probability

    Returns
    -------
    np.ndarray(float)
        The probability sampled by samples, repeated the correct
        amount of times
    np.ndarray(float)
        The subset of the original samples not falling into the
        already measured intervals
    """
    if len(bound_probabilities) == 0:
        return [], samples

    bound_probs = np.array(list(bound_probabilities.values()))
    left_bound = bound_probs[:, 0]
    right_bound = bound_probs[:, 1]
    probs = bound_probs[:, 1] - bound_probs[:, 0]
    new_samples = []

    def get_probs(sample, new_samples):
        condition = np.logical_and(sample < right_bound, sample > left_bound)

        if not any(condition):
            new_samples.append(sample)
            return -1
        else:
            res = probs[condition]
            return res[0]

    # get_probs = np.vectorize(get_probs)
    probablity_sampled = np.array([get_probs(ss, new_samples) for ss in samples])

    probablity_sampled = probablity_sampled[probablity_sampled > 0].astype(float)

    return probablity_sampled, np.array(new_samples)
