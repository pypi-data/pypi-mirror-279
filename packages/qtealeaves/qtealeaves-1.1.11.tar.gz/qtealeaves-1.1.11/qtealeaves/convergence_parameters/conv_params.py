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
Module defining the convergence parameters for tensor network simulations.
"""

import os
from copy import deepcopy
from collections import OrderedDict
from qtealeaves import write_nml, StrBuffer
from qtealeaves.tooling import _ParameterizedClass


__all__ = ["TNConvergenceParameters"]


class TNConvergenceParameters(_ParameterizedClass):
    """
    Handling of the convergence parameters for the tensor network
    simulations.

    **Arguments**

    max_iter : integer, optional
        Maximum number of sweeps in the ground state search.
        Default to 20.

    abs_deviation : float, optional
        Exit criterion for ground state search if the energy of the
        current sweep has an absolute deviation from the previous
        data points below this threshold.
        Default to 4e-12.

    rel_deviation : float, optional
        Exit criterion for ground state search if the energy of the
        current sweep has a relative deviation from the previous data
        points below this threshold.
        Default to 1e-12.

    n_points_conv_check : int, optional
        Number of data points used when checking convergence, e.g.,
        for the ground state search. Exit criteria are not checked
        until this many sweeps have been performed, and are never
        checked if `n_points_conv_check > max_iter`.
        Default to 4.

    max_bond_dimension : int, optional
        The maximal bond dimension used during the simulations.
        The default value is purely a starting point for testing
        simulations.
        Default to 5.

    trunc_method : str, optional
        Python only
        Method use to truncate the singular values. Default to "R".
        Available:
        - "R": use cut_ratio
        - "N": use maximum norm

    cut_ratio : float, optional (python side only)
        Python only
        If trunc_method="r":
            Cut ratio :math:`\\epsilon` after which the singular values are
            neglected, i.e. if :math:`\\lambda_1` is the bigger singular values
            then after an SVD we neglect all the singular values such that
            :math:`\\lambda_i/\\lambda_1\\leq\\epsilon`.
        If trunc_method="n":
            Maximum value of the norm neglected for the singular values during
            the trunctation.
        Default to 1e-9.

    increase_precision
        TBA

    measure_obs_every_n_iter : int
        Modulo for measuring statics every n iterations. Not
        propagated through yet on the fortran side.

    svd_ctrl : character, optional
        Control for the SVD algorithm. Available:
        - "A" : automatic. Some heuristic is run to choose the best mode for the algorithm.
                The heuristic can be seen in tensors/tensors.py in the function _process_svd_ctrl.
        - "V" : gesvd. Safe but slow method. Recommended in Fortran simulation
        - "D" : gesdd. Fast iterative method. It might fail. Resort to gesvd if it fails
        - "E" : eigenvalue decomposition method. Faster on GPU. Available only when
                contracting the singular value to left or right
        - "X" : sparse eigenvalue decomposition method. Used when you reach the maximum
                bond dimension. Only python.
        - "R" : random SVD method. Used when you reach the maximum bond dimension.
                Only python.
        Default to 'V'.

    random_sweep : bool, optional
        Use random sweep scheme instead of default scheme.
        Default to False.

    skip_exact_rgtensors : logical, optional
        Allows to skip space expansion if the tensors has already
        reached the maximal bond dimension of the underlying
        local Hilbert spaces, i.e., full Hilbert space is captured
        without truncation of entanglement. Only applies to
        sweep with space expansion.
        Default to False.

    svd_threshold : float
        TBA (only first accessed if array on fortran side)

    min_expansion : int, optional
        Bond dimension expansion used in the fortran code for a single
        site optimization. The bond dimension is increased of this integer.
        It is also used in the python simulation to increase the
        bond dimension when doing an expanding QR. In that case,
        the integer represent the percentage.
        Default to 20.

    expansion_cycles : int
        For space link expansion, the link between a tensor and its predefined
        partner tensor are expanded. Then, each tensor and partner tensors
        are optimized `expansion_cycles` times.
        Default to 1.

    expansion_drop : character out of ["f", "o", "d"]
        Behavior what to do if space link expansion leads to worse energy
        than before with options expansion_drop="f" for false (accept
        worse energies to escape local minima), "o" for optimize single
        tensor (reinstall original tensors, but optimize as in a single
        tensor update), and "d" for discarding step (reinstall original
        tensors and skip optimization).
        Not passed through to Fortran backend.
        Default to "f".

    arnoldi_initial_tolerance
        Fortran: TBA
        python: unused so far

    arnoldi_min_tolerance
        Fortran: TBA
        python: unused so far

    arnoldi_max_tolerance
        TBA (Fortran only)

    arnoldi_maxiter : int
        Python only : right now, evaluated in qtealeaves-eigensolver (not Arpack)
        Maximum number of Lanczos vectors to be used.

    krylov_maxiter : int
        Python only : right now, evaluated in KrylovSolver, time evolution only.
        Default to 32.

    krylov_tol : float
        Python only : right now, evaluated in KrylovSolver, time evolution only.
        Default to 1e-7.

    aggression_tolerance
        TBA

    aggression_expansion
        TBA

    statics_method : integer, optional
        Method to run ground state search for this/all iteration.
        0 : default (2)
        1 : sweep
        2 : sweep with space expansion (can still be reduced to sweep
            during the simulation based on a energy condition)
        3 : imaginary time evolution with two-tensor TDVP (Fortran only)
        4 : imaginary time evolution with TDVP space expansion (python-only)
        5 : imaginary time evolution with TDVP single-site (python-only)
        33 : imaginary nearest-neighbor TEBD.

    imag_evo_dt : float, optional
        Time-step size for the imaginary time evolution.
        Default to 0.1.

    filename_conv : str, optional
        The convergence parameters are saved under this filename
        inside the input folder.
        Default to ``ConvergenceInput.dat``.

    trunc_tracking_mode : str, optional
        Python only:
        Modus for storing truncation, 'M' for maximum, 'C' for
        cumulated of the singvals squared (Norm truncated) (default).

    data_type : str, optional
        Data type of the TN.
        "A" : automatic ("Z")
        "Z" : double precision complex
        "C" : single precision complex
        "D" : double precision real
        "S" : single precision real

    ini_bond_dimension : int, optional
        Python only.
        The initial bond dimension used during the simulations when
        the initialization is random.
        Using subspace expansion or two-site updates the bond dimension
        can grow.
        Default to max_bond_dimension.

    device : str, optional
        Device where to run the optimization.
        "cpu" : run on cpu with numpy
        "gpu" : run on gpu with cupy

    min_bond_dimension : int, optional
        [python-only] Set the minimum bond dimension. One value
        independent of the sweeps.
        Default to 1.

    """

    def __init__(
        self,
        max_iter=20,
        abs_deviation=4e-12,
        rel_deviation=1e-12,
        n_points_conv_check=4,
        max_bond_dimension=5,
        trunc_method="R",
        cut_ratio=1e-9,
        increase_precision=False,
        measure_obs_every_n_iter=1,
        svd_ctrl="V",
        random_sweep=False,
        skip_exact_rgtensors=False,
        svd_threshold=1e-15,
        min_expansion=20,
        expansion_cycles=1,
        expansion_drop="f",
        arnoldi_initial_tolerance=1e-2,
        arnoldi_min_tolerance=0.0,
        arnoldi_max_tolerance=1e-2,
        arnoldi_maxiter=32,
        krylov_maxiter=32,
        krylov_tol=1e-7,
        aggression_tolerance=1.0,
        aggression_expansion=1.0,
        statics_method=2,
        imag_evo_dt=0.1,
        filename_conv="ConvergenceInput.dat",
        trunc_tracking_mode="C",
        data_type="A",
        ini_bond_dimension=None,
        min_bond_dimension=1,
        device="cpu",
    ):
        self.filename_conv = filename_conv

        # Convergence parameters for statics / decision on convergence
        self.max_iter = max_iter
        self.abs_deviation = abs_deviation
        self.rel_deviation = rel_deviation
        self.n_points_conv_check = n_points_conv_check
        self.measure_obs_every_n_iter = measure_obs_every_n_iter
        self.svd_ctrl = svd_ctrl
        self.min_bond_dimension = min_bond_dimension
        if ini_bond_dimension is None:
            self.ini_bond_dimension = max_bond_dimension
        else:
            self.ini_bond_dimension = ini_bond_dimension

        # Consumed in python
        self.trunc_method = trunc_method.upper()
        self.cut_ratio = cut_ratio
        self.arnoldi_maxiter = arnoldi_maxiter
        self.krylov_maxiter = krylov_maxiter
        self.krylov_tol = krylov_tol
        self.trunc_tracking_mode = trunc_tracking_mode.upper()

        # Settings for one or all iterations
        self.sim_params = {}
        self.sim_params["max_bond_dimension"] = max_bond_dimension
        self.sim_params["increase_precision"] = increase_precision
        self.sim_params["random_sweep"] = random_sweep
        self.sim_params["skip_exact_rgtensors"] = skip_exact_rgtensors
        self.sim_params["svd_threshold"] = svd_threshold
        self.sim_params["min_expansion"] = min_expansion
        self.sim_params["expansion_cycles"] = expansion_cycles
        self.sim_params["expansion_drop"] = expansion_drop
        self.sim_params["arnoldi_initial_tolerance"] = arnoldi_initial_tolerance
        self.sim_params["arnoldi_min_tolerance"] = arnoldi_min_tolerance
        self.sim_params["arnoldi_max_tolerance"] = arnoldi_max_tolerance
        self.sim_params["aggression_tolerance"] = aggression_tolerance
        self.sim_params["aggression_expansion"] = aggression_expansion
        self.sim_params["statics_method"] = statics_method
        self.sim_params["imag_evo_dt"] = imag_evo_dt
        self.sim_params["data_type"] = data_type
        self.sim_params["device"] = device

        # For python side, consumed in qtealeaves-solver, can be set
        # by algorithm, but not by user so far
        self.sim_params["arnoldi_tolerance"] = 0.0

    def resolve_params(self, params, idx=None):
        """Resolve parameterized values (inplace-update)."""

        attr_numeric = [
            "max_iter",
            "abs_deviation",
            "rel_deviation",
            "n_points_conv_check",
            "measure_obs_every_n_iter",
            "cut_ratio",
            "krylov_maxiter",
            "arnoldi_maxiter",
            "min_bond_dimension",
            "ini_bond_dimension",
        ]
        attr_str = ["svd_ctrl", "trunc_method", "trunc_tracking_mode"]
        self._resolve_params_attr(params, attr_numeric, attr_str)

        # Settings for one or all iterations in dictionary
        str_params = ["data_type", "expansion_drop", "device"]

        new_dict = {}
        for key, value in self.sim_params.items():
            if key not in str_params:
                value = self.eval_numeric_param(value, params)
                if hasattr(value, "__len__") and idx is not None:
                    value = value[idx]
            else:
                value = self.eval_str_param(value, params)
                if not isinstance(value, str):
                    if hasattr(value, "__len__") and idx is not None:
                        value = value[idx]

            new_dict[key] = value

        self.sim_params = new_dict

    def resolve_params_copy(self, params, idx=None):
        """
        Return a copy of the convergence parameters with all parameterized
        values resolved.
        """
        resolved = deepcopy(self)
        resolved.resolve_params(params, idx=idx)

        return resolved

    def prepare_parameters_for_iteration(self, params):
        """
        Preparation to write parameters for each iteration. It checks
        if a list of convergence settings has to be written and builds
        a dictionary with the resolved entries for each parameters,
        which is either a the value or a list of values.

        **Arguments**

        params : dict
            Dictionary with the simulation parameters.

        **Results**

        has_vector_of_settings : bool
            True if settings change over the iterations and
            the parameters have to be written for each iteration.

        sim_param_all : dict
            Contains the resolved convergence parameters, i.e.,
            strings and functions are resolved with the actual values.
        """
        max_iter = self.eval_numeric_param(self.max_iter, params)

        sim_params_all = {}
        has_vector_of_settings = False

        str_params = ["data_type", "expansion_drop", "device"]

        for key, value in self.sim_params.items():
            if isinstance(value, str):
                # Have to catch strings first as they have a length
                # attribute
                if key in str_params:
                    # String parameters
                    entry = self.eval_str_param(value, params)
                else:
                    # Numeric parameters
                    entry = self.eval_numeric_param(value, params)
            elif hasattr(value, "__len__"):
                # List of any kind
                if key in str_params:
                    # String parameters
                    entry = [
                        self.eval_str_param(value[ii], params)
                        for ii in range(len(value))
                    ]
                else:
                    # Numeric parameters
                    entry = [
                        self.eval_numeric_param(value[ii], params)
                        for ii in range(len(value))
                    ]
            else:
                # Scalar values (cannot be a str parameter, which
                # would go into the first if)
                entry = self.eval_numeric_param(value, params)

            if isinstance(entry, str):
                # String never activates list
                pass
            elif hasattr(entry, "__len__"):
                has_vector_of_settings = True
                if len(entry) != max_iter:
                    raise Exception(
                        "Length of convergence parameter list for "
                        + "%s must match " % (key)
                        + "max_iter=%d." % (max_iter)
                    )

            sim_params_all[key] = entry

        return has_vector_of_settings, sim_params_all

    @property
    def max_bond_dimension(self):
        """
        Provide the getter method for this property important to
        the MPS emulator. It allows to get values without a
        dictionary, but prevents doing it if the values is not
        an integer.
        """
        value = self.sim_params["max_bond_dimension"]
        if hasattr(value, "__len__"):
            value = value[0]

        if isinstance(value, int):
            return value

        raise Exception("Try to use getter on non-int bond dimension.")

    @property
    def data_type(self):
        """
        Provide the getter method for this property important to
        the MPS emulator. It allows to get values without a
        dictionary, but prevents doing it if the values is not
        an integer. (Not queried from the MPS for now).
        """
        value = self.sim_params["data_type"]
        if isinstance(value, str):
            # Value is string itself, return first
            return value

        if hasattr(value, "__len__"):
            value = value[0]
            return value

        raise Exception("Try to use getter on non-str data type.")

    @property
    def min_expansion_qr(self):
        """
        Provide the getter method for this property important to
        the python emulator. It is the percentage of the bond dimension
        increase in the qr
        """
        value = self.sim_params["min_expansion"]
        if hasattr(value, "__len__"):
            value = value[0]

        if isinstance(value, int):
            return value / 100

        raise Exception("Try to use getter on non-valid min_expansion")

    def get_chi(self, params):
        """
        Shortcut to evaluate the bond dimension as numeric parameter.

        **Arguments**

        params : dict
            The parameter dictionary for the simulation.
        """
        return self.eval_numeric_param(self.sim_params["max_bond_dimension"], params)

    def write_input(self, folder_name, params):
        """
        Write convergence parameters for input version 2 and 3.

        **Arguments**

        folder_name : str
            Name of the input folder, where the file with the convergence
            parameters is written to.

        params : dict
            Dictionary with the simulation parameters.
        """
        # First build a dictionary which allows listed entries
        has_vector_of_settings, sim_params_all = self.prepare_parameters_for_iteration(
            params
        )

        filename_conv = self.eval_str_param(self.filename_conv, params)
        # pylint: disable-next=no-member
        full_nml = os.path.join(folder_name, filename_conv)
        if not full_nml.endswith(".nml"):
            full_nml += ".nml"

        conv_params = OrderedDict()
        conv_params["num_cpoints"] = self.eval_numeric_param(
            self.n_points_conv_check, params
        )

        conv_params["max_iterations"] = self.eval_numeric_param(self.max_iter, params)

        conv_params["abs_dev"] = self.eval_numeric_param(self.abs_deviation, params)

        conv_params["rel_dev"] = self.eval_numeric_param(self.rel_deviation, params)

        conv_params["has_vector_of_settings"] = has_vector_of_settings

        conv_params["measure_obs_every_n_iter"] = self.eval_numeric_param(
            self.measure_obs_every_n_iter, params
        )

        if self.svd_ctrl in ["S", "V", "D", "E", "X"]:
            # Single characters are vulnerable to having some Hamiltonian
            # parameter named V etc
            conv_params["svd_ctrl"] = self.svd_ctrl
        else:
            conv_params["svd_ctrl"] = self.eval_str_param(self.svd_ctrl, params)

        file_content = StrBuffer()
        write_nml("CONV_VARS", conv_params, file_content)

        # Some parameters in the dictionary are python-only and will crash
        # the nml-file reading on the fortran side
        python_only_keys = [
            "expansion_drop",
            "device",
            "arnoldi_tolerance",
        ]

        # Require maximum(1, ...) for skipping statics
        for ii in range(max(1, conv_params["max_iterations"])):
            sim_params_ii = OrderedDict()

            for key in self.sim_params:
                if key in python_only_keys:
                    continue

                entry = sim_params_all[key]

                if isinstance(entry, str):
                    sim_params_ii[key] = entry
                elif hasattr(entry, "__len__"):
                    sim_params_ii[key] = entry[ii]
                else:
                    sim_params_ii[key] = entry

            write_nml("SIM_PARAMS", sim_params_ii, file_content)

            if not has_vector_of_settings:
                break

        with open(full_nml, "w+") as fh:
            fh.write(file_content())

        return full_nml
