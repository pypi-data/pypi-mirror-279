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
The setup for a simulation with the aTTN or TTN network bringing together all
pieces, e.g., the model, and the observables.
"""

import os


import os.path
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess
import multiprocessing as mprc
from collections import OrderedDict
from warnings import warn

# Time is not precise, but perf_counter likely does not
# include calls to subprocess
from time import time as tictoc
from time import sleep

import numpy as np

import qtealeaves as qtl
from qtealeaves import write_nml
import qtealeaves.emulator as qtltn
from qtealeaves.tooling import _ParameterizedClass, QteaJsonEncoder
from qtealeaves.mpos import SparseMatrixProductOperator as spo_cls


__all__ = ["QuantumGreenTeaSimulation", "ATTNSimulation", "DynamicsQuench"]


class DisentanglerPositionException(Exception):
    """
    Class of exceptions raised when aTTN disentanglers are
    placed on the invalid position. Raised within the
    `check_disentangler_position` function.
    """


class QuantumGreenTeaSimulation(_ParameterizedClass):
    """
    Simulation class containing the model, the operators, the convergence
    settings, and the observables.

    **Arguments**

    model : instance of ``RydbergModel``
        Defines the model, e.g., the Hamiltonian of the system.

    operators : instance of ``TNOperators``
        Defines the operators used in the model and the observables.

    convergence : instance of ``TNConvergenceParameters``
        Specifies the convergence parameters for the simulation,
        for example the bond dimension.

    observables : instance of ``TNObservables``
        Defines the observables of the simulation. For details,
        check the corresponding class.

    folder_name_input : str, or callable; optional
        Specifies the folder where the input is stored. Will be created
        if not existing. Path can contain subfolders.
        default to ``input``

    folder_name_output : str, or callable; optional
        Specifies the folder where the output is stored. Will be created
        if not existing. Path can contain subfolders.
        default to ``output``

    tn_type : int, optional
        Specifies whether TTNs (1) or aTTNs (2) are used. The integer 0
        is reserved for running ED simulations within in the python
        frontend. LPTN can be called via (3) and an MPS via LPTN as (4).
        The python backends can be used with non-symmetric TTNs (5),
        non-symmetric MPS (6).
        Additionally, for aTTN python backend choose (7), but only correlation
        measurement and no groundstate search is so far implemented.
        default to 1

    tensor_backend : int, optional
        Choosing the underlying tensor, where the AbelianSymTensors are ``1``,
        and the Tensors are ``2``.
        default to 1

    mpo_mode : int, optional
        Choosing the MPO representation inside the simulation, where
        the value -1 enables an auto-selection.
        The other values are TPO via iTPO (0), iTPO (1), iTPO with
        update (2, for quenches), iTPO with compression (3), and sparse
        MPO (10, partially enabled), indexed sparse MPO (11, partially enabled)
        Default to -1.

    disentangler : None or np.ndarray, optional
        If the aTTN is used, the disentangler positions can be passed
        as a 2d numpy array with 2 rows and n columns, where n is the
        number of disentanglers. The indices must be passed as python
        indices starting from 0 in the mapped 1d system. The other option is
        to set it to None, in that case the disentangler positions are automatically
        selected if the tensor network is aTTN.
        Default to None.

    disentangler_file : str, optional
        If disentanglers are present, their positions are passed
        to fortran via this file. It will be located inside the
        input folder.
        default to ``disentangler.dat``

    has_log_file : bool, optional
        Flag if log file should be created instead of writing
        the output to standard out. If False, all output will
        go to standard out.
        Default to False (no log file)

    store_checkpoints : bool, optional
        If True, the state will be written to a file after each
        sweep in the ground state search and after each time step
        in a time evolution. Ground state searches have the option
        to write checkpoints also after each tensor optimization,
        which the algorithm can decide on without control by the
        user.
        If `True`, `delete_existing_folder` must be `False`.
        Default to True

    verbosity : int, optional
        Sets the output level inside the python functions. Does
        not have any effect on fortran simulations.
        Default to 1.

    qgreentea_exe : str, optional
        Set name of the executable to be used for calls to
        quantum green tea. Allows to customize beyond executables
        in the local folder.
        Default to `./MainaTTN`

    **Reserved keywords of the simulation dictionary**

    The following keywords cannot be used for adapting simulations to the
    needs by the user, but have a predefined meaning. Additional predefined
    keywords may be imported, e.g., when using a specific model or a specific
    set of operators.

    * `continue_file` : load file at the beginning of the simulation.
    * `use_mpo_from_continue_file` : bool (Python only). Use MPO stored
      in continue file.
    * `seed` : seed for random number generators.
    * `magic_number` : for debugging / developing to pass something to
       fortran.
    * `SymmetrySector`
    * `SymmetryGenerators`
    * `SymmetryTypes`
    * `Quenches`
    * `ed_sparse` : bool, use in exact state emulator to
      switch between sparse and dense Hamiltonian.
    * `sweep_order` : defines the sweep order for the statics (python only)
    * `exclude_from_hash` : dictionary entries that will be excluded from hash.

    **Details**

    1) Checkpoints vs continue files: checkpointing is used to restart the same
       simulation. Continue files can be used to set the input state across
       simulations, but the simulation will start always at the beginning with
       this user-provided input state.
    2) Hashing: hashes are generated to identify that a simulation setup did
       not change. For example, changes in a simulation which uses checkpoints
       can be detected this way.
    """

    def __init__(
        self,
        model,
        operators,
        convergence,
        observables,
        folder_name_input="input",
        folder_name_output="output",
        file_name_input="TTN.in",
        tn_type=1,
        tensor_backend=1,
        mpo_mode=-1,
        disentangler=None,
        disentangler_file="disentangler.dat",
        has_log_file=False,
        store_checkpoints=True,
        verbosity=1,
        qgreentea_exe="./MainaTTN",
    ):
        if tensor_backend != 2 and tn_type in (5, 6, 7):
            raise ValueError(
                "Only non-symmetric tensors can be used in python. Set tensor_backend=2."
            )
        self.model = model
        self.operators = operators
        self.convergence = convergence
        self.observables = observables

        self.file_name_input = file_name_input
        self.folder_name_input = folder_name_input
        self.folder_name_output = folder_name_output

        self.version_input_processor = 3
        self.tn_type = tn_type
        self.tensor_backend = tensor_backend
        self.mpo_mode = mpo_mode

        self.disentangler = disentangler
        self.disentangler_file = disentangler_file

        self.has_log_file = has_log_file
        self.store_checkpoints = store_checkpoints
        self.verbosity = verbosity

        self.qgreentea_exe = qgreentea_exe

    def vprint(self, *args, verbosity_level=1):
        """
        Control verbose print via levels and class variable.

        **Arguments**

        verbosity_level : int, optional
            If the verbosity level pass here is smaller than the
            verbosity level in the class, the ``*args`` will be
            passed to the print function.
            Default to 1
        """
        if verbosity_level <= self.verbosity:
            print(*args)

    @staticmethod
    def checkpoint_params_hash(params):
        """Generate hash of a simulation to identify if checkpointed simulation."""
        exclude_from_hash = params.get("exclude_from_hash", [])

        if len(exclude_from_hash) == 0:
            dict_for_hash = params
        else:
            dict_for_hash = {}
            for key, value in params.items():
                if key in exclude_from_hash:
                    continue

                dict_for_hash[key] = value

        params_str = json.dumps(dict_for_hash, sort_keys=True, cls=QteaJsonEncoder)
        return hashlib.sha256(params_str.encode("utf-8")).hexdigest()

    def get_groundstate_energy(self, params):
        """
        (DEPRECATED) Rudimentary way to extract the ground state energy via the
        convergence file.

        **Arguments**

        params : dict
            The parameter dictionary, which is required to obtain
            the output folder.

        **Details**

        Use ``get_static_obs`` in future.
        """
        warn("`get_groundstate_energy` is deprecated.")

        num_trajectories = self.observables.get_num_trajectories(params=params)
        if num_trajectories > 1:
            raise Exception(
                "`get_groundstate_energy` not available for quantum trajectories."
            )

        folder_name_output = self.eval_str_param(self.folder_name_output, params)
        line = None
        # pylint: disable-next=no-member
        with open(os.path.join(folder_name_output, "convergence.log"), "r") as fh:
            for line in fh:
                pass

        if line is None:
            raise Exception("Reading ground state energy from empty file.")

        return float(line.split()[1])

    def get_static_obs(self, params):
        """
        Return a dictionary with all observables of the static simulation,
        e.g., the ground state search. For evolutions in temperature,
        i.e., LPTNs, a list of dictionaries is returned.

        **Arguments**

        params : dict
            The parameter dictionary, which is required to obtain
            the output folder.
        """
        folder_name_output = self.eval_str_param(self.folder_name_output, params)

        tn_type = self.eval_numeric_param(self.tn_type, params)
        if tn_type == 3:
            # LPTN statics have multiple measurements in temperature
            static_obs_list = []

            max_iter = self.convergence.eval_numeric_param(
                self.convergence.max_iter, params
            )

            meas_freq = self.convergence.eval_numeric_param(
                self.convergence.measure_obs_every_n_iter, params
            )

            for ii in range(max_iter):
                if (ii + 1 != max_iter) and ((ii + 1) % meas_freq != 0):
                    # no measurement took place
                    continue

                obs_dict = self.observables.read(
                    "static_obs_%08d.dat" % (ii + 1), folder_name_output, params
                )
                static_obs_list.append(obs_dict)

            return static_obs_list

        # Simulations with one final measurement at the end of the statics
        results = self.observables.read("static_obs.dat", folder_name_output, params)

        return results

    def get_dynamic_obs(self, params):
        """
        Return dictionaries with all observables of the static simulation,
        e.g., the dynamics. You obtain a nested list, the outer list is
        iterating over the quenches; the inner list over the time steps
        of each quench.

        **Arguments**

        params : dict
            The parameter dictionary, which is required to obtain
            the output folder.

        """
        folder_name_output = self.eval_str_param(self.folder_name_output, params)

        all_results = []

        idx = 0
        for _, quench in enumerate(params["Quenches"]):
            quench_results = []
            warning_count = 0

            # According to the convention in iter_params_dts we have
            # three cases
            #
            # * dt > 0: step belonging to the time evolution
            # * dt == 0: measurement
            # * dt < 0: skipped measurement (nothing to read)
            for dt in quench.iter_params_dts(params):
                if dt > 0.0:
                    # Evolution step, no measurement
                    continue

                idx += 1

                if np.isclose(dt, 0.0):
                    # Only dt == 0 are measurements by convention - time
                    # evolution step treated with continue in 1st if-case
                    file_name = "dyn_obs%08d_%08d.dat" % (1, idx)

                    # Try to read, and warn if the file does not exist.
                    # Do not warn more than three times for each quench.
                    # Cannot test with a single `os.path.isfile` as
                    # observables might be split into trajectories.
                    try:
                        quench_results.append(
                            self.observables.read(file_name, folder_name_output, params)
                        )

                    except FileNotFoundError:
                        if warning_count < 3:
                            warn(
                                f"File {folder_name_output}/{file_name} not found. Skipping."
                            )
                        if warning_count == 3:
                            warn("Further warnings will be suppressed.")
                        warning_count += 1
                        # If the folder is missing append None
                        # instead of the result dictionary.
                        quench_results.append(None)

            all_results.append(quench_results)

        return all_results

    def extend_params(self, params):
        """
        Extend the parameters list and if the number of quantum trajectories
        is > 1, add to params the trajectory id and seed.

        **Arguments**

        params : dict or list of dicts
            The parameter dictionary or dictionaries, which is required
            to obtain the output folder.
        """
        if isinstance(params, dict):
            # convert params into a list
            params = [params]

        params_ext = []
        for elem in params:
            num_trajectories = self.observables.get_num_trajectories(params=elem)
            if num_trajectories == 1:
                params_ext.append(elem)
            else:
                for ii in range(num_trajectories):
                    tmp = deepcopy(elem)
                    tmp["trajectory_id"] = self.observables.get_id_trajectories(ii)
                    tmp["seed"] = self.observables.get_seed_trajectories(tmp)
                    params_ext.append(tmp)
        return params_ext

    def run(self, params, delete_existing_folder=False, nthreads=1):
        """
        Run a simulation or multiple simulations possibly via threading.

        **Arguments**

        params : dict or list of dicts
            The parameter dictionary or dictionaries, which is required
            to obtain the output folder.

        delete_existing_folder : bool, optional
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
            Default to False

        nthreads : int, optional
            If number of threads greater is one, we launch serial
            simulations. If greater than one, multiple threads
            are started to run simulations in parallel.
            Default to 1.

        **Details**

        If you run the threaded version, set the OMP_NUM_THREADS
        and MKL_NUM_THREADS (executable compiled with ifort)
        accordingly. The number of threads defined here times
        the OMP_NUM_THREADS should not exceed the number of your
        processors.

        If running the TTN time evolution, workflow is the following:

        #1 Loading the initial TTN state :
            This can be either a random TTN, or the TTN read from a
            user-set file.
        #2 Groundstate search to set the initial condition :
            There are two options - initial condition is the groundstate
            of the specified Hamiltonian, or initial condition is a TTN
            from file set by a user.
            The groundstate is found by iterative search, therefore if
            the initial condition is set by user, put `max_iter=0` in
            convergence parameters. Otherwise, set `max_iter>0`.
        #3 Perform a time evolution starting from the obtained
            initial condition.
        """
        # create a new list for the parameter to add different
        # entries in the case of quantum trajectories
        params_ext = self.extend_params(params=params)

        # Check that we don't accidentally delete the current or
        # parent directory
        if delete_existing_folder:
            for elem in params_ext:
                folder_name_input = self.observables.get_folder_trajectories(
                    self.folder_name_input, elem
                )
                folder_name_output = self.observables.get_folder_trajectories(
                    self.folder_name_output, elem
                )

                # pylint: disable-next=no-member
                current_path = Path(os.getcwd())
                # pylint: disable-next=no-member
                input_path = Path(os.path.abspath(folder_name_input))
                # pylint: disable-next=no-member
                output_path = Path(os.path.abspath(folder_name_output))

                inout_folder_danger = []
                # True if in/out folder is the same as the current folder
                inout_folder_danger.append(input_path == current_path)
                inout_folder_danger.append(output_path == current_path)
                # True if in/out folder is a parent folder of the current folder
                inout_folder_danger.append(input_path in current_path.parents)
                inout_folder_danger.append(output_path in current_path.parents)

                inout_folder_is_dangerous = any(inout_folder_danger)
                if inout_folder_is_dangerous:
                    raise ValueError(
                        "Preventing the deleting of current/parent folder. "
                        "If delete_existing_folder is True, input or output "
                        "folders cannot be set to the current folder or any "
                        "parent folder."
                    )

        # Now we have a list
        if nthreads == 1:
            for elem in params_ext:
                self.run_single(elem, delete_existing_folder=delete_existing_folder)
        else:
            self.run_threaded(
                params_ext,
                delete_existing_folder=delete_existing_folder,
                nthreads=nthreads,
            )
        return

    def status(self, params):
        """
        Returns tuple of three integers containing the number of simulations
        not started, number of simulation started but not finished, and the
        number of finished simulations.

        **Arguments**

        params : dict or list of dicts
            The parameter dictionary or dictionaries, which is required
            to obtain the output folder.
        """
        # create a new list for the parameter to add different
        # entries in the case of quantum trajectories
        params_ext = self.extend_params(params=params)

        num_unstarted = 0
        num_interrupted = 0
        num_finished = 0

        for elem in params_ext:
            folder_name_output = self.observables.get_folder_trajectories(
                self.folder_name_output, elem
            )

            finished_json = os.path.join(folder_name_output, "has_finished.json")
            if os.path.isfile(finished_json):
                num_finished += 1
                continue

            dyn_checkpoints = os.path.join(
                folder_name_output, "has_dyn_checkpoints.txt"
            )
            if os.path.isfile(dyn_checkpoints):
                # Dynamics started, but did not finish
                num_interrupted += 1
                continue

            stat_checkpoints = os.path.join(
                folder_name_output, "has_stat_checkpoints.txt"
            )
            if os.path.isfile(stat_checkpoints):
                # Statics started, but did not finish
                num_interrupted += 1
                continue

            # Did not reach first checkpoint of statics, consider it as simulation
            # which did not start yet
            num_unstarted += 1

        return num_unstarted, num_interrupted, num_finished

    def write_input(
        self, params, delete_existing_folder=False, do_return_params_ext=False
    ):
        """
        Write input for a simulation or multiple simulations.

        **Arguments**

        params : dict or list of dicts
            The parameter dictionary or dictionaries, which is required
            to obtain the output folder.

        delete_existing_folder : bool, optional
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
            Default to False

        do_return_params_ext : bool, optional
            Return additionally the full list of simulations, e.g., potentially
            extended with quantum trajectories.
            Default to False.

        **Returns**

        exec_list : list of strings
            Commands to be executed to run the simulations written.

        params_ext : list of dicts
            Only returned as second return value if `do_return_params_ext=True`.
            Contains the full list of simulation parameter dictionaries.
        """
        # create a new list for the parameter to add different
        # entries in the case of quantum trajectories
        params_ext = self.extend_params(params=params)

        # Now we have a list
        exec_list = []
        for elem in params_ext:
            cmd_arg = self.write_input_single(elem, delete_existing_folder)
            exec_list.append(self.qgreentea_exe + " " + cmd_arg)

        if do_return_params_ext:
            return exec_list, params_ext

        return exec_list

    def write_input_mpi(
        self,
        params,
        delete_existing_folder=False,
        submit_dir=None,
        use_rsync=False,
        mpi_input_file="mpi_exec_list.txt",
    ):
        """
        Write input for a multiple simulations with MPI. This function is targeted
        at HPC clusters and can also handling the copies of data between submit
        and scratch directories.

        **Arguments**

        params : dict or list of dicts
            The parameter dictionary or dictionaries, which is required
            to obtain the output folder.

        delete_existing_folder : bool, optional
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
            Default to False

        submit_dir : str or `None`, optional
            If `None`, the path to the input and output folder is accesible
            from the current working directory. If a string is specified,
            the string will be used as a prefix to the input and output
            directory and they will be copied on runtime (by fortran) to the
            current working directory.
            Default to `None`

        use_rsync : bool, optional
            Set which command should be used for copy. By default, `cp` is used
            with `use_rsync=False`. If `True`, rsync will be used.
            The flag has only an effect if `submit_dir is not None`.
            Default to `False`.

        mpi_input_file : str, optional
            Allows to specify custom filename for job list. Existing files
            will be overwritten.
            Default to `"mpi_exec_list.txt"`

        **Returns**

        mpi_input_file : str
            Input file to call the MPI executable with.

        **Details**

        The approach to run from a temporary scratch directory directly
        below the node is to specify the submit directory. The scratch
        directory is the working directory in this case and this way the
        input and output folder specified in the nml are still correct.

        The other way round, i.e., the current working directory as submit
        directory, needs an update of the input and output folder specified
        in the nml file. This update is not possible if we access environment
        variables as `$SCRATCH` as fortran would have to do the string
        handling (while for the copying, the shell will substitute any
        environment variables automatically).
        """
        exec_list, params_ext = self.write_input(
            params,
            delete_existing_folder=delete_existing_folder,
            do_return_params_ext=True,
        )
        nn = len(exec_list)

        # Always zero right now for data parallelism
        mpi_approach = 0

        # submit_dir approach for copying input and output
        submit_dir_approach = 0 if (submit_dir is None) else 1
        if (submit_dir_approach == 1) and (use_rsync):
            submit_dir_approach = 2

        with open(mpi_input_file, "w+") as fh:
            fh.write("%d\n" % (mpi_approach))
            fh.write("%d\n" % (nn))
            fh.write("%d\n" % (submit_dir_approach))

            for ii, elem in enumerate(exec_list):
                nml_file = elem.split()[1]
                # nml_file += ' ' * (1024 - len(nml_file))

                if submit_dir_approach in [1, 2]:
                    input_dir = self.observables.get_folder_trajectories(
                        self.folder_name_input, params_ext[ii]
                    )
                    output_dir = self.observables.get_folder_trajectories(
                        self.folder_name_output, params_ext[ii]
                    )

                    input_run_dir = input_dir
                    # pylint: disable-next=no-member
                    input_dir = os.path.join(submit_dir, input_dir)

                    output_run_dir = output_dir
                    # pylint: disable-next=no-member
                    output_dir = os.path.join(submit_dir, output_dir)

                if submit_dir_approach in [1, 2]:
                    fh.write(input_dir + "\n")
                    fh.write(output_dir + "\n")
                    fh.write(input_run_dir + "\n")
                    fh.write(output_run_dir + "\n")

                fh.write(nml_file + "\n")

        return mpi_input_file

    @staticmethod
    def combine_mpi_inputs(*args, mpi_input_file="mpi_exec_list.txt"):
        """
        Combine different MPI inputs to one job list. Approaches for MPI
        and submit directory handling must match.

        **Arguments**

        mpi_input_file : str, optional
            Allows to specify custom filename for job list. Existing files
            will be overwritten.
            Default to `"mpi_exec_list.txt"`

        **Returns**

        mpi_input_file : str or `None`
            New file to run with MPI, `None` in the case of empty
            argument list.
        """
        if len(args) == 0:
            # No input at all
            return None

        if len(args) == 1:
            # Nothing to combine
            return args[0]

        dst_buffer = []

        # Parse first files
        with open(args[0], "r") as src:
            for ii, line in enumerate(src):
                if ii == 0:
                    dst_mpi_approach = int(line.strip())
                elif ii == 1:
                    dst_nn = int(line.strip())
                elif ii == 2:
                    dst_submit_dir_approach = int(line.strip())

                dst_buffer.append(line)

        for mpi_file in args[1:]:
            with open(mpi_file, "r") as src:
                for ii, line in enumerate(src):
                    if ii == 0:
                        mpi_approach = int(line.strip())
                        if dst_mpi_approach != mpi_approach:
                            raise Exception(
                                "Cannot combine files with different approach"
                            )
                        continue

                    if ii == 1:
                        nn = int(line.strip())
                        dst_nn += nn
                        continue

                    if ii == 2:
                        submit_dir_approach = int(line.strip())
                        if dst_submit_dir_approach != submit_dir_approach:
                            raise Exception(
                                "Cannot combine files with different approach"
                            )
                        continue

                    dst_buffer.append(line)

        dst_buffer[1] = "%d\n" % (dst_nn)
        with open(mpi_input_file, "w+") as dst:
            for line in dst_buffer:
                dst.write(line)

        return mpi_input_file

    def write_input_single(self, params, delete_existing_folder):
        """
        Write the input files for a simulation.

        **Arguments**

        params : dict
            The parameter dictionary, which is required to obtain
            the output folder.

        delete_existing_folder : bool
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
        """
        folder_name_input = self.observables.get_folder_trajectories(
            self.folder_name_input, params
        )
        folder_name_output = self.observables.get_folder_trajectories(
            self.folder_name_output, params
        )
        sim_hash_file = os.path.join(folder_name_input, "sim_hash.json")
        tn_type = self.eval_numeric_param(self.tn_type, params)

        if self.store_checkpoints and delete_existing_folder:
            raise ValueError("Cannot delete folders and rely on checkpoints.")

        sim_hash = self.checkpoint_params_hash(params)

        # There are three options:
        #
        # * delete_existing_folder=True, store_checkpoints=False
        # * delete_existing_folder=False, store_checkpoints=False
        # * delete_existing_folder=False, store_checkpoints=True
        if delete_existing_folder:
            # Delete existing folder, checkpoints cannot be activated.

            # pylint: disable-next=no-member
            if os.path.isdir(folder_name_input):
                shutil.rmtree(folder_name_input)

            # pylint: disable-next=no-member
            if os.path.isdir(folder_name_output):
                shutil.rmtree(folder_name_output)

        elif not self.store_checkpoints:
            # No checkpoints and not deleting existing folders
            # pylint: disable-next=no-member
            if os.path.isdir(folder_name_input) or os.path.isdir(folder_name_output):
                raise ValueError(
                    "Folder exists, but neither checkpoints nor deleting activated."
                )

        # pylint: disable-next=no-member
        elif os.path.isdir(folder_name_input) and os.path.isdir(folder_name_output):
            with open(sim_hash_file, "r") as fh:
                jdic = json.load(fh)
                previous_sim_hash = jdic["sim_hash"]

            if previous_sim_hash != sim_hash:
                # This is not a simulation which is continued
                raise Exception("Trying to continue simulation with different params.")
            if tn_type in [0, 5, 6, 7]:
                # python simulation can restart via `simulation.run`
                return None

            # Looks like a fortran simulation, need to construct
            # nml file name
            return self.get_full_fortran_nml(params)

        # pylint: disable-next=no-member
        if os.path.isdir(folder_name_input) or os.path.isdir(folder_name_output):
            # raise error, this can only happen if user was interfering by hand
            raise ValueError("Input / output folder: one exists, one does not exist.")

        # pylint: disable-next=no-member
        if not os.path.isdir(folder_name_output):
            # pylint: disable-next=no-member
            os.makedirs(folder_name_output)
        # pylint: disable-next=no-member
        if not os.path.isdir(folder_name_input):
            # pylint: disable-next=no-member
            os.makedirs(folder_name_input)

        # Store the simulation hash
        sim_hash_jdic = {"sim_hash": sim_hash}
        with open(sim_hash_file, "w+") as fh:
            json.dump(sim_hash_jdic, fh)

        if tn_type in [0, 5, 6, 7]:
            # It is a python simulation, we do not write any input
            return None
        if self.version_input_processor == 3:
            # Fortran simulation with input processor 3 (only 3 valid by now)
            nml_file = self.write_input_3(params)
            return nml_file

        if self.version_input_processor in [1, 2]:
            raise Exception("Version of input processor not supported anymore.")

        raise Exception("Unknwon version of f90 input processor.")

    def run_single(self, params, delete_existing_folder=False):
        """
        Run simulation specified via the parameter dictionary.

        **Arguments**

        params : dict
            The parameter dictionary, which is required to obtain
            the output folder.

        delete_existing_folder : bool, optional
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
            Default to False
        """
        tic = tictoc()

        cmd_arg = self.write_input_single(params, delete_existing_folder)

        tn_type = self.eval_numeric_param(self.tn_type, params)
        if tn_type == 0:
            # Run ED simulation
            qtltn.run_ed_simulation(self, params)
        elif tn_type in (5, 6, 7):
            # Run pyTN simulation (TTN or MPS)
            qtltn.tn_simulation.run_tn_simulation(self, params)

        else:
            # All input version processor for TN simulations
            cmd = self.qgreentea_exe + " " + cmd_arg

            self.vprint("Will be running " + cmd)
            status = subprocess.call(cmd, shell=True)

            if status != 0:
                raise Exception("Fortran error during simulation.")

            # Only for fortran on purpose - python has to handle itself
            toc = tictoc()
            self.vprint("Simulation time is %2.4f." % (toc - tic))

        return

    def run_threaded(self, params, delete_existing_folder=False, nthreads=4):
        """
        Run simulation specified via the parameter dictionary.

        **Arguments**

        params : list
            List of the parameter dictionaries, which is required to obtain
            the output folder.

        delete_existing_folder : bool, optional
            If flag is True, existing folder with potential results
            will be overwritten without warning. If False, an error
            is raised if the folders already exist.
            If `True`, `store_checkpoints` must be `False`.
            Default to False

        nthreads : int, optional
            Number of threads to start multiple simulations in
            parallel.
            Default to 4.
        """
        if nthreads == 1:
            # Route back to serial code ...
            self.run(
                params, delete_existing_folder=delete_existing_folder, nthreads=nthreads
            )
            return

        # number of threads should not exceed length of parameter list
        nthreads = min(nthreads, len(params))

        # Fill list with the first nthreads simulations
        job_list = []
        for ii in range(nthreads):
            next_args = (self, params[ii], delete_existing_folder)
            next_simulation = mprc.Process(target=_run_single_thread, args=next_args)

            next_simulation.start()
            job_list.append(next_simulation)

        # Replace jobs whenever one finishes ...
        next_check = -1
        ii = nthreads
        while ii < len(params):
            for jj in range(nthreads):
                next_check += 1
                if next_check == nthreads:
                    next_check = 0

                if not job_list[next_check].is_alive():
                    next_args = (self, params[ii], delete_existing_folder)
                    next_simulation = mprc.Process(
                        target=_run_single_thread, args=next_args
                    )

                    next_simulation.start()
                    job_list[next_check] = next_simulation
                    ii += 1

                    break

                if jj + 1 == nthreads:
                    # None of the jobs was finished; wait for 10s
                    sleep(10)

        # All jobs launched ... now order does not matter for join
        for ii in range(nthreads):
            job_list[ii].join()

        return

    @staticmethod
    def write_symmetries(folder_name_input, params):
        """
        Returns number of symmetries and input file.

        **Arguments**

        folder_name_input : str
            Name of the input folders where the symmetry file should
            be written to.

        params : dict
            Dictionary with the simulation parameters.
        """
        sectors = params.get("SymmetrySectors", [0])
        nn_sym = len(sectors)

        # pylint: disable-next=no-member
        full_filename = os.path.join(folder_name_input, "symmetry_sectors.dat")
        with open(full_filename, "w+") as fh:
            fh.write(str(nn_sym) + "\n")

            for elem in sectors:
                fh.write(str(elem) + "\n")

            fh.write("\n")

        return nn_sym, full_filename

    def autoselect_disentangler(self, params):
        """
        Given a number of sites and Hamiltonian, the function
        automatically chooses the positions for aTTN disentanglers.
        The function will try to place as many disentanglers as possible
        which do not violate the restrictions we have on the disentangler
        positions (for more info on the restrictions, look at the function
        `check_disentangler_position`).

        Parameters
        ----------
        params : dict
            Dictionary with the simulation parameters.

        Return
        ------
        auto_dis : np.array
            Disentangler positions.
        """
        if self.tn_type == 7:
            raise NotImplementedError(
                "Automatic disentangler selection not yet implemented for"
                " python backend aTTNs."
            )
        # Total number of sites in the system
        ll_1d_mapped = self.model.get_number_of_sites(params)
        # The array in which the disentangler positions will be added
        auto_dis = np.array([[], []], dtype=int)

        # To find the positions on which we can place the disentanglers, we
        # iterate over all the pairs of sites in the system.

        # We want the disentanglers to support the links of the highest bond
        # dimension, which are in general the ones in the highest layers of the TTN.
        # Therefore, we first iterate over the pairs which are on the opposite
        # halves of the system, then over the pairs which are on the different
        # quarters, and so on.

        # We have to iterate over sites of different halves, or quarters,
        # or etc. `division` variable tells how many sites are within a group.
        # We start from the halves, i.e. groups of `division` = `ll_1d_mapped`/2 sites.
        # Later in the loop, in each iteration `division` is reduced to half
        # of its value.
        division = ll_1d_mapped // 2
        # when the division of the TTN reaches the groups of 2 sites, we stop.
        for _ in range(int(np.log2(ll_1d_mapped)) - 1):
            # `num_groups` tells how many groups we have for a certain division. For
            # example, if the division is in quarters, there will be 4 groups.
            num_groups = ll_1d_mapped // division
            for group in range(0, num_groups, 2):
                # We iterate over combinations of pairs where first and second site
                # belong to different groups.

                # Remark: if e.g. we have 4 groups, the
                # iterations will go over pairs belonging to group0-group1, and
                # group2-group3. We exclude group1-group2 because its combinations
                # are already covered within the previous division, where the
                # system was divided in halves.

                # The first loop starts from `division - 1` and goes backwards
                # because this way, the priority is given to the disentanglers
                # connected to the sites which are physically closer, i.e. cover
                # more entanglement.
                for ii in range(division - 1, -1, -1):
                    for jj in range(division):
                        # find the indices of sites within the first and second group
                        ii_shift = group * division + ii
                        jj_shift = (group + 1) * division + jj

                        # these are the indices of the sites of new potential disentangler
                        position = np.array([[ii_shift], [jj_shift]], dtype=int)

                        # Append the new disentangler to the disentangler list,
                        # and try if it is on a valid position.
                        auto_dis = np.append(auto_dis, position, axis=1)
                        try:
                            self.check_disentangler_position(params, auto_dis)
                            # If this new disentangler passes the checks, it remains in
                            # the disentangler list.
                        except DisentanglerPositionException:
                            # If it doesn't pass the checks, remove the disentangler
                            # from the list
                            auto_dis = auto_dis[:, :-1]
            division = division // 2

        return auto_dis

    def check_disentangler_position(self, params, disentangler_pos=None):
        """
        This function checks if the disentangler position input is valid.

        Arguments
        ---------
        params: dict
            Dictionary with the simulation parameters.
        disentangler_pos : np.array of shape [2, num_disentanglers], optional
            An array containing the disentangler positions. Each column
            represents one disentangler. The first row indicates the
            position of the first site of the disentangler, and the
            second row indicates the position of the second site.
            If None, the disentangler positions are read from the `self`.
            Default to None.
        """
        if disentangler_pos is None:
            disentangler_pos = self.eval_numeric_param(self.disentangler, params)
        ll_1d_mapped = self.model.get_number_of_sites(params)
        lattice_size = self.model.eval_lvals(params)

        if not isinstance(disentangler_pos, np.ndarray):
            raise DisentanglerPositionException(
                "Disentangler positions must be numpy array."
            )

        if len(disentangler_pos.shape) != 2:
            raise DisentanglerPositionException(
                "Disentangler positions must be rank-2."
            )

        if disentangler_pos.shape[0] != 2:
            raise DisentanglerPositionException(
                "Disentangler positions must be 2 rows."
            )

        if np.min(disentangler_pos) < 0:
            raise DisentanglerPositionException(
                "Disentangler positions must be greater than -1."
            )

        if np.max(disentangler_pos) >= ll_1d_mapped:
            raise DisentanglerPositionException(
                "Disentangler positions must be smaller than system size."
            )

        if any(
            (np.min(dis) % 2 == 0) and (np.max(dis) - np.min(dis) == 1)
            for dis in np.transpose(disentangler_pos)
        ):
            raise DisentanglerPositionException(
                "Disentangler cannot be attached to only one tensor."
            )

        if any(dis[0] == dis[1] for dis in np.transpose(disentangler_pos)):
            raise DisentanglerPositionException(
                "Disentangler cannot be placed on only one site."
            )

        # Check if MPO is connected to different disentanglers:

        # Create array with num_sites elements, assign each disentangler a value
        # and put these values to the corresponding disentangler positions.
        # The values are 1,2,3, ..., num_disentangler
        lattice_array = np.zeros(ll_1d_mapped, dtype=int)
        ind_count = 1
        for dis in np.transpose(disentangler_pos):
            if any(lattice_array[dis] > 0):
                raise DisentanglerPositionException(
                    "A single physical link cannot have more than one"
                    " disentangler attached to it."
                )
            lattice_array[dis] += ind_count
            ind_count += 1

        # Iterate through interaction terms within Hamiltonian and check if
        # two-body interaction MPO is connected to two different disentanglers.
        # We check if MPO is connected to different disentanglers by checking
        # the values on lattice_array on these sites - from the definition of
        # lattice_array above, there are two different disentanglers if the
        # lattice sites have a different value>0

        for term in self.model.hterms:
            if not isinstance(term, qtl.modeling.localterm.LocalTerm):
                all_interactions = term.get_interactions(lattice_size, params)
                for single_interaction in all_interactions:
                    # single_interaction[1] contains the 1d coordinates of each
                    # two-body term on the lattice
                    one_term = lattice_array[single_interaction[1]]
                    if len(np.unique(one_term[one_term > 0])) > 1:
                        raise DisentanglerPositionException(
                            f"MPO on sites {single_interaction[1]} connected to "
                            "different disentanglers."
                        )

                    # If there are no multiple disentanglers on a single interaction
                    # term, check also for the cases when disentangler position yields
                    # a 4-link MPO, which creates an error on fortran side. No
                    # further loop over the disentanglers is necessary due to this
                    # fact!
                    if len(one_term) > 3 and np.count_nonzero(one_term) >= 1:
                        # reorder the sites in interaction term
                        order = np.argsort(single_interaction[1])
                        one_term = one_term[order]
                        single_int = np.array(single_interaction[1])[order]

                        # index of disentangler in `one_term`
                        term_dis_ind = np.nonzero(one_term)[0]
                        # index of the disentangler in `disentangler_pos`
                        ind = np.unique(one_term[term_dis_ind])[0] - 1
                        # access the position of that disentangler in TTN
                        dis = np.transpose(disentangler_pos)[ind]

                        # One can show that the 4-link MPO will appear if MPO sites
                        # on one side of the disentangler are in both L and R environment.

                        # We check this by defining the array `env` of size of the 1D mapped lattice
                        # we will fill it with different values according to whether they
                        # belong to the left or right environment: if the site can belong to
                        # either left or right environment, the value is 0. If it
                        # belongs to left environment, the value is 3 and if it belongs to
                        # right environment, the value is 4.
                        env = np.zeros(ll_1d_mapped, dtype=int)

                        # this part of the code finds the position of L and R
                        # environment
                        div = int(ll_1d_mapped / 2)
                        while dis[0] // div == dis[1] // div:
                            div = int(div / 2)

                        cut1 = (dis[0] // div) * div
                        cut2 = (dis[1] // div) * div

                        # mark the regions of different environments with
                        # different values
                        env[:cut1] = 0  # can be either L or R
                        env[cut1 : cut1 + div] = 2  # L
                        env[cut2 : cut2 + div] = 3  # R
                        env[cut2 + div :] = 0  # can be either L or R

                        # The disentangler is on a valid position only if it does
                        # not divide the left or right environment into two pieces.

                        # In terms of this check, the above criterion is satisfied
                        # only if the sites in the `env`` array on the left and
                        # right of the disentangler surely belong to L and R, i.e.
                        # when abs(env[left site] - env[right site]) = 1 [from the values
                        # of `env` array in the code above].

                        # take only the part of `env` where the interaction term is, i.e.,
                        # convert something like 00022330000 for the whole lattice to
                        # 0223 for the site of the MPO.
                        env_term = env[single_int]

                        # iterate over the disentangler sites of one disentangler which are
                        # on this term.
                        for de_ind in term_dis_ind:
                            # flag if in bulk with respect to whole MPO (not left /
                            # right environment).
                            disentangler_in_bulk = de_ind not in (0, len(env_term) - 1)

                            # If not in bulk with respect to the whole MPO, it must
                            # be valid (also on the edge of left/right environment)
                            if not disentangler_in_bulk:
                                continue

                            # Now we have for sure a disentangler site in the bulk
                            # Does it cut any possible left/right environment into two?
                            # The sequences like 0223 are only one iff we are at the
                            # boundary between 2 and 3 which is a valid position.
                            if abs(env_term[de_ind - 1] - env_term[de_ind + 1]) != 1:
                                raise DisentanglerPositionException(
                                    "Disentangler configuration resulting in a 4-linkID MPO"
                                )

        return

    def write_disentangler(self, folder_name_input, params):
        """
        Write the disentangler file. Disentanglers are based on a
        1D system or a system mapped to a 1d system. The two coordinates
        correspond to the two 1d positions.

        Python indices go into the function, fortran indices will go out.

        **Arguments**

        folder_name_input : str
            Name of the input folders where the symmetry file should
            be written to.

        params : dict
            Dictionary with the simulation parameters.
        """
        full_filename = self.eval_str_param(self.disentangler_file, params)
        disentangler_pos = self.eval_numeric_param(self.disentangler, params)

        tn_type = self.eval_numeric_param(self.tn_type, params)
        if tn_type not in [2, 7]:
            # No aTTN, return empty filename
            full_filename = ""
            return full_filename

        # pylint: disable-next=no-member
        full_filename = os.path.join(folder_name_input, full_filename)
        if disentangler_pos is None:
            # User expects auto-selection
            disentangler_pos = self.autoselect_disentangler(params)

        if self.tn_type == 7:  # because python indexing is different!!
            disentangler_pos = np.transpose(disentangler_pos)
        self.check_disentangler_position(params, disentangler_pos=disentangler_pos)

        with open(full_filename, "w+") as fh:
            fh.write("%d\n" % (disentangler_pos.shape[1]))

            for ii in range(disentangler_pos.shape[1]):
                fh.write(
                    "%d, %d\n"
                    % (
                        disentangler_pos[0, ii] + 1,
                        disentangler_pos[1, ii] + 1,
                    )
                )

            fh.write("\n")

        if self.tn_type == 7:  # because python indexing is different!!
            disentangler_pos = np.transpose(disentangler_pos)

        return full_filename

    def get_full_fortran_nml(self, params):
        """Return the fortran nml filename serving as entry point for simulations."""
        folder_name_input = self.observables.get_folder_trajectories(
            self.folder_name_input, params
        )

        file_name_input = self.eval_str_param(self.file_name_input, params)
        if not file_name_input.endswith(".nml"):
            file_name_input += ".nml"

        # pylint: disable-next=no-member
        full_nml = os.path.join(folder_name_input, file_name_input)

        return full_nml

    def write_input_3(self, params):
        """
        Write all the input files for the input processor version 3. This
        version supports for example parameterization of models.

        **Arguments**

        params : dict
            Dictionary with the simulation parameters.
        """
        folder_name_input = self.observables.get_folder_trajectories(
            self.folder_name_input, params
        )
        folder_name_output = self.observables.get_folder_trajectories(
            self.folder_name_output, params
        )

        # pylint: disable-next=no-member
        if not os.path.isdir(folder_name_input):
            # pylint: disable-next=no-member
            os.makedirs(folder_name_input)

        required_operators = []
        required_operators += self.model.collect_operators()
        required_operators += self.observables.collect_operators()
        required_operators = list(set(required_operators))

        conv_in = self.convergence.write_input(folder_name_input, params)
        operator_in, operator_map = self.operators.write_input(
            folder_name_input, params, self.tensor_backend, required_operators
        )
        model_in = self.model.write_input(
            folder_name_input, params, operator_map, self.mpo_mode, spo_cls
        )
        obs_in = self.observables.write(folder_name_input, params, operator_map)

        task_params = OrderedDict()
        task_params["input_folder"] = folder_name_input
        task_params["output_folder"] = folder_name_output

        if "continue_file" in params:
            tmp_continue_file = self.eval_str_param(params["continue_file"], params)
        else:
            tmp_continue_file = ""

        task_params["continue_file"] = tmp_continue_file
        task_params["do_continue"] = tmp_continue_file != ""
        task_params["tn_type"] = self.eval_numeric_param(self.tn_type, params)
        task_params["tensor_backend"] = self.tensor_backend
        task_params["version_input_processor"] = self.version_input_processor
        task_params["operator_file"] = operator_in
        task_params["model_file"] = model_in
        task_params["observable_file"] = obs_in
        task_params["convergence_file"] = conv_in

        nx_ny_nz = self.model.get_number_of_sites_xyz(params)
        task_params["dimensions"] = len(nx_ny_nz)
        nx_ny_nz = nx_ny_nz + [1] * (3 - task_params["dimensions"])
        task_params["number_sites_x"] = nx_ny_nz[0]
        task_params["number_sites_y"] = nx_ny_nz[1]
        task_params["number_sites_z"] = nx_ny_nz[2]

        nn_sym, file_sym = self.write_symmetries(folder_name_input, params)
        task_params["number_symmetries"] = nn_sym
        task_params["symmetry_file"] = file_sym

        task_params["disentangler_file"] = self.write_disentangler(
            folder_name_input, params
        )

        task_params["has_log_file"] = self.has_log_file
        # task_params['log_file'] = # THIS IS PENDING
        task_params["store_checkpoints"] = self.store_checkpoints

        if "Quenches" in params:
            # assumes all quenches have the same time evolution mode
            quench = params["Quenches"][0]

            task_params["time_evolution_mode"] = params["Quenches"][
                0
            ].time_evolution_mode
            if task_params["time_evolution_mode"] == 0:
                # in write method, this can only be a fortran simulation with TN, never ED
                # set to 1
                task_params["time_evolution_mode"] = 1

            task_params["time_evolution_mode"] = quench.time_evolution_mode
            task_params["oqs_mode"] = quench.oqs_mode
        else:
            task_params["time_evolution_mode"] = 0
            task_params["oqs_mode"] = 0

        task_params["mpo_mode"] = self.eval_numeric_param(self.mpo_mode, params)
        task_params["magic_number"] = params.get("magic_number", 0)

        seed = list(params.get("seed", [11, 13, 17, 19]))
        if len(seed) != 4:
            raise Exception("List for seed must be of length four.")
        if np.any(np.array(seed) > 4095):
            raise Exception("Entries for seed must be smaller than 4096.")
        if np.any(np.array(seed) < 1):
            raise Exception("Entries for seed must be bigger than 0.")
        if seed[3] % 2 == 0:
            raise Exception("Last entry of seed must be odd.")

        # Nml does not support lists (?)
        task_params["seed1"] = seed[0]
        task_params["seed2"] = seed[1]
        task_params["seed3"] = seed[2]
        task_params["seed4"] = seed[3]

        full_nml = self.get_full_fortran_nml(params)
        write_nml("TASK_VARS", task_params, full_nml)

        return full_nml


class ATTNSimulation(QuantumGreenTeaSimulation):
    """
    For backwards compatibility.
    """

    def __init__(self, *args, **kwargs):
        warn("Deprecated ATTNSimulation; switch to QuantumGreenTeaSimulation.")

        version_input_processor = kwargs.get("version_input_processor", None)
        if version_input_processor is not None:
            warn("Deprecated argument input processor.")
            del kwargs["version_input_processor"]

        super().__init__(*args, **kwargs)

        if version_input_processor is not None:
            self.version_input_processor = version_input_processor


def _run_single_thread(obj, params, delete_existing_folder):
    """
    Internal function to launch a single thread of a threaded simulation.

    **Arguments**

    obj : instance of :class:``ATTNSimulation``.
        Simulation class to be run.

    params : dict
        The parameter dictionary, which is required to obtain
        the output folder.

    delete_existing_folder : bool, optional
        If flag is True, existing folder with potential results
        will be overwritten without warning. If False, an error
        is raised if the folders already exist.
        If `True`, `store_checkpoints` must be `False`.
        Default to False
    """
    obj.run_single(params, delete_existing_folder=delete_existing_folder)
    return


class DynamicsQuench(dict):
    """
    Describing a quench of parameters for the dynamics part of
    a TN simulation. The parameters must be defined as a function
    taking the time and the simulation dictionary as arguments.

    **Arguments**

    dt_grid : numpy.ndarray, str, callable
        Contains the list of time steps, which can differ. Moreover,
        it can be parameterized and be a callable or string.

    time_evolution_mode : int, optional
        Defines the time evolution mode.
        0 : automatic selector
            (Defaults to 1 for tensor networks.
            For exact diagonalization,
            defaults to 10 for systems smaller than 10 sites and 11 for others.)
        1 : one-tensor TDVP
        2 : two-tensor TDVP
        3 : two-tensor TDVP (2nd order)
        4 : single-tensor TDVP (2nd order)
        5 : 9 steps of one-site and one step of two-site TDVP
        10 : exact diagonalization with full Hamiltonian matrix generated
        11 : exact diagonalization with Krylov
        Not every network type might support all time evolution modes.
        Default to 0.

    measurement_period : int, str, callable, optional
        Allows to define a measurement period every n time steps. It
        considers only the time steps, not the time passed. There
        is always a measurement at the end of the quench.
        Default to 1.

    oqs_mode : int, optional
        Controls the open quantum system evolution, where no open
        quantum is 0, quantum trajectories with jumps is 1 (not enabled yet),
        and quantum trajectories with norm only is 2.
        Default to 0.

    check_superfluous : bool, optional
        If ``True``, a warning is raised whenever a dictionary key is
        not in the required parameters.
        Default to True

    **Details**

    Open systems implement the Lindblad equation as

    .. math::

        \\frac{d}{dt} \\rho = -i [H, \\rho]
             + \\sum \\gamma (L \\rho L^{\\dagger}
             - \\frac{1}{2} \\{ L^{\\dagger} L, \\rho \\})

    """

    def __init__(
        self,
        dt_grid,
        time_evolution_mode=0,
        measurement_period=1,
        oqs_mode=0,
        check_superfluous=True,
    ):
        super().__init__()
        self.dt_grid = dt_grid
        self.time_evolution_mode = time_evolution_mode
        self.measurement_period = measurement_period
        self.oqs_mode = oqs_mode
        self.check_superfluous = check_superfluous

    def __len__(self):
        """
        Overload length, now defined via number of time steps.
        """
        if isinstance(self.dt_grid, str) or hasattr(self.dt_grid, "__call__"):
            raise Exception("Cannot support length for non-ndarray.")

        return len(self.dt_grid)

    def get_length(self, params):
        """
        Calculate the length of the time grid even for parameterized
        grids.

        **Arguments**

        params : dict
            The parameter dictionary, which will be passed to callables
            and used to evaluate string parameters.
        """
        dt_grid = self.eval_numeric_param(self.dt_grid, params)
        return len(dt_grid)

    def get_dt_grid(self, params):
        """
        Evaluate the dt grid and return it.

        **Arguments**

        params : dict
            The parameter dictionary, which will be passed to callables
            and used to evaluate string parameters.
        """
        return self.eval_numeric_param(self.dt_grid, params)

    def eval_numeric_param(self, elem, params):
        """
        Evaluate a numeric parameter which might be defined via the
        parameter dictionary.

        **Arguments**

        elem : callable, string, or int/float
            Defines the parameter either via a function which return
            the value, a string being an entry in the parameter
            dictionary, or directly as the numeric value.

        params : dict
            The parameter dictionary, which will be passed to callables
            and used to evaluate string parameters.
        """
        if isinstance(elem, list):
            return [self.eval_numeric_param(subelem, params) for subelem in elem]

        if hasattr(elem, "__call__"):
            val = elem(params)
        elif isinstance(elem, str):
            val = params[elem]
        else:
            val = elem

        return val

    def iter_params(self, required_params, params, time_at_start=0.0):
        """
        Iterate over the all time steps and the required parameters
        within. Function returns the time-dependent parameters
        evaluated at mid-timestep. Moreover, we return the
        time-dependent parameters at the end of each time step
        to allow for measurements.

        **Arguments**

        required_params : OrderedDict
            Keys are the required parameters, values are the
            default values if no function is present.

        params : dict
            Simulation parameter dictionary.

        time_at_start : float, optional
            Time at the beginning of the quench, which allows
            to take into account previous quenches.
            Default to 0.0
        """
        dt_grid = self.eval_numeric_param(self.dt_grid, params)
        tnow = time_at_start

        if self.check_superfluous:
            for key in self:
                if key not in required_params:
                    warn("Detected superfluous function `%s` in quench." % (key))

        for dt_ii in dt_grid:
            tmid = tnow + 0.5 * dt_ii

            for key in required_params.keys():
                if key in self:
                    yield self[key](tmid, params)
                else:
                    yield required_params[key]

            tnow += dt_ii

            for key in required_params.keys():
                if key in self:
                    yield self[key](tnow, params)
                else:
                    yield required_params[key]

    def iter_params_dts(self, params):
        """
        Iterate over parameters's time steps. Coupling with a time-step dt
        greater than zero, are intended for the time evolution. Every second
        parameter is 0 or -99 and indicating the values are at the end point
        for the measurements, i.e., doing measurements (zero) or doing
        no measurement (-99), respectively. Up to now, no other values
        less or equal to zero are associated with some special meaning.

        **Arguments**

        params : dict
            Simulation parameter dictionary.
        """
        dt_grid = self.eval_numeric_param(self.dt_grid, params)
        meas_period = self.eval_numeric_param(self.measurement_period, params)

        for ii, dt in enumerate(dt_grid[:-1]):
            yield dt

            if ((ii + 1) % meas_period) == 0:
                yield 0.0
            else:
                yield -99.0

        yield dt_grid[-1]
        yield 0.0

    def iter_dts(self):
        """
        Generator yielding all the time steps dt within
        this quench. It returns the delta, not the current
        time in total.
        """
        if isinstance(self.dt_grid, str) or hasattr(self.dt_grid, "__call__"):
            raise Exception("Cannot support iter_dts for non-ndarray.")

        for dt in self.dt_grid:
            yield dt
