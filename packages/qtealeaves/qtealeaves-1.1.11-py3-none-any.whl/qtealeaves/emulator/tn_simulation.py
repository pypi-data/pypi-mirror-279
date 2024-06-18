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
The module contains a light-weight execution of a tensor network simulations for:

- MPS
- TTN
- aTTN (only correlation measurements)

"""

# pylint: disable=too-many-locals
# pylint: disable=too-many-lines
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

# pylint: disable-next=no-member, no-name-in-module
import os
import os.path
import json
from copy import deepcopy
from time import time as tictoc
from warnings import warn
import numpy as np

from qtealeaves.solvers import KrylovSolverH, KrylovSolverNH
from qtealeaves.tensors import QteaTensor, TensorBackend
from qtealeaves.mpos import (
    TensorProductOperator,
    DenseMPOList,
    SparseMPO,
    ITPO,
)
from .abstract_tn import _AbstractTN
from .ttn_simulator import TTN
from .mps_simulator import MPS
from .attn_simulator import ATTN


__all__ = ["run_tn_simulation", "update_time_dependent_terms", "optimize"]

TN_TYPE = {6: MPS, 5: TTN, 7: ATTN}
AVAIL_DTYPES = {
    "A": np.complex128,
    "Z": np.complex128,
    "C": np.complex64,
    "D": np.float64,
    "S": np.float32,
    "H": np.float16,  # Problems with eigensolver, mixed-precision for linalg
}

# Store intrasweep checkpoints beyond 24 h / sweep (time in sec)
QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS = int(
    os.environ.get("QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS", 3600 * 24)
)


def run_tn_simulation(simulation, params):
    """
    Run a full simulation with the python tensor network.

    **Arguments**

    simulation : instance of ``ATTNSimulation``
        Represents all the information on the simulation.

    params : dict
        Dictionary containing the current parameters for the
        simulation.
    """
    tic = tictoc()
    seed = params.get("seed", [11, 13, 17, 19])
    np.random.seed(seed)
    sim_hash = simulation.checkpoint_params_hash(params)

    # Collect some information
    lvals = simulation.model.eval_lvals(params)
    num_sites = np.prod(lvals)
    folder_name_input = simulation.observables.get_folder_trajectories(
        simulation.folder_name_input, params
    )
    folder_name_output = simulation.observables.get_folder_trajectories(
        simulation.folder_name_output, params
    )

    # This is the only one going actually to standard out
    if simulation.verbosity > 0:
        print("Starting simulation %s" % (folder_name_input))

    # Tensor types for simulation
    tensor_cls = QteaTensor
    base_tensor_cls = QteaTensor

    conv_params_init = simulation.convergence.resolve_params_copy(params, idx=0)
    dtype = AVAIL_DTYPES[conv_params_init.data_type]
    device = conv_params_init.sim_params["device"]

    tensor_backend = TensorBackend(
        tensor_cls=tensor_cls,
        base_tensor_cls=base_tensor_cls,
        device=device,
        dtype=dtype,
    )

    if simulation.tensor_backend != 1:
        sectors = {}
    else:
        raise Exception("Symmetric tensor are not supported on the python backend.")

    # Select the desired ansatz. Either TTN (5) or MPS (6)
    tn_type = simulation.eval_numeric_param(simulation.tn_type, params)
    if tn_type in [5, 6, 7]:
        # TTN or MPS simulation
        ansatz = TN_TYPE[tn_type]
    else:
        raise Exception(f"The tn_type {tn_type} is not available.")

    # Prepare operators
    # -----------------

    operators = base_tensor_cls.convert_operator_dict(
        simulation.operators,
        params=params,
        symmetries=[],
        generators=[],
        base_tensor_cls=base_tensor_cls,
        dtype=dtype,
        device=device,
    )

    # Prepare state
    # -------------

    requires_singvals = False
    if len(simulation.observables.obs_list["TNObsCorr"]) > 0:
        requires_singvals = True

    # If `continue_file` is present, use it to initialize the state
    if "continue_file" in params:
        if isinstance(params["continue_file"], ansatz):
            # state is passed directly from python
            state = params["continue_file"]

        else:
            # state is passed as a file
            ext = params["continue_file"].split(".")[-1]

            if ext == "pkl" + ansatz.extension:
                state = ansatz.read_pickle(params["continue_file"])
            elif ext == ansatz.extension:
                state = ansatz.read(params["continue_file"], tensor_backend)
            else:
                msg = f"""No approach available to read `{params["continue_file"]}`."""
                msg += f" Default extension / ansatz is `{ansatz.extension}`."
                raise Exception(msg)

            state.convert(dtype, device)

        state.convergence_parameters = simulation.convergence
        # Set flag for QR vs SVD here
        # pylint: disable-next=protected-access
        state._requires_singvals = requires_singvals

        if state.iso_center is None:
            state.iso_towards(state.default_iso_pos)

        de_sites_sim = simulation.eval_numeric_param(simulation.disentangler, params)
        if ansatz.has_de and de_sites_sim is not None:
            warn(
                "Ignoring disentangler position from QuantumGreenTeaSimulation "
                " and taking the positions from continue_file."
            )

    else:
        # if aTTN, set disentangler positions
        if ansatz.has_de:
            de_initialize = "random"
            if de_sites_sim is None:
                de_sites = simulation.autoselect_disentangler(params)

                # Will be in fortran-compatible format, so convert
                de_sites = de_sites.T
            else:
                de_sites = de_sites_sim
        else:
            de_initialize = None
            de_sites = None

        # initialize a random state
        state = ansatz(
            num_sites,
            conv_params_init,
            local_dim=[operators["id"].links[1]] * num_sites,
            requires_singvals=requires_singvals,
            initialize="random",
            tensor_backend=tensor_backend,
            sectors=sectors,
            de_sites=de_sites,
            de_initialize=de_initialize,
        )

        # Set parameterized convergence parameters now, but
        # ansatz has no way to resolve parameterization
        state.convergence_parameters = simulation.convergence

    iso_pos = state.default_iso_pos

    state.log_set_verbosity(simulation.verbosity)
    if simulation.has_log_file:
        # pylint: disable-next=no-member
        state.log_open(os.path.join(folder_name_output, "sim.log"))

    # Prepare system Hamiltonian
    # --------------------------

    dense_mpo_list = DenseMPOList.from_model(
        simulation.model, params, tensor_backend=tensor_backend
    )
    dense_mpo_list.initialize(operators, params)

    mpo_mode = simulation.eval_numeric_param(simulation.mpo_mode, params)
    if params.get("use_mpo_from_continue_file", False):
        if "continue_file" not in params:
            raise Exception("No continue file was used.")
        mpo = state.eff_op
    elif mpo_mode == 0:
        mpo = ITPO(num_sites, do_indexing=False)
        mpo.add_dense_mpo_list(dense_mpo_list)
    elif mpo_mode in [-1, 1]:
        # Auto-select goes to iTPO
        mpo = ITPO(num_sites)
        mpo.add_dense_mpo_list(dense_mpo_list)
    elif mpo_mode in [2]:
        mpo = ITPO(num_sites, enable_update=True)
        mpo.add_dense_mpo_list(dense_mpo_list)
    elif mpo_mode in [3]:
        mpo = ITPO(num_sites, do_compress=True)
        mpo.add_dense_mpo_list(dense_mpo_list)
    elif mpo_mode in [4]:
        mpo = ITPO(num_sites, do_compress=True, enable_update=True)
        mpo.add_dense_mpo_list(dense_mpo_list)
    elif mpo_mode == 10:
        if isinstance(params.get("_sparse_mpo", None), SparseMPO):
            # Allow user defined SparseMPO as not many rules are supported
            # Then, delete from dictionary otherwise deepcopy is prevented
            mpo = params["_sparse_mpo"]
            del params["_sparse_mpo"]
        else:
            mpo = SparseMPO(num_sites, operators, do_vecs=True)
            mpo.add_dense_mpo_list(dense_mpo_list, params, indexed_spo=False)
    elif mpo_mode == 11:
        if isinstance(params.get("_sparse_mpo", None), SparseMPO):
            # Allow user defined SparseMPO as not many rules are supported
            mpo = params["_sparse_mpo"]
            del params["_sparse_mpo"]
        else:
            mpo = SparseMPO(num_sites, operators, do_vecs=True)
            mpo.add_dense_mpo_list(dense_mpo_list, params)
    elif mpo_mode == 21:
        mpo = TensorProductOperator.from_mpo_list_num_sites(dense_mpo_list, num_sites)

    else:
        raise Exception(f"The mpo_mode {mpo_mode} is not available.")

    # Statics
    # -------

    # If dynamics checkpoints are available, call to statics is not necessary
    checkpoint_indicator_file = os.path.join(
        folder_name_output, "has_dyn_checkpoints.txt"
    )
    load_dyn_from_checkpoint = os.path.isfile(checkpoint_indicator_file)

    # pylint: disable-next=protected-access
    state._requires_singvals = requires_singvals

    # Initialize effective operators
    if not params.get("use_mpo_from_continue_file", False):
        mpo.setup_as_eff_ops(state)

    if not load_dyn_from_checkpoint:
        # Minimization of the energy
        sweep_order = params.get("sweep_order", None)
        state, _, needs_measurement = optimize(
            state,
            params,
            folder_name_output,
            simulation.store_checkpoints,
            sweep_order=sweep_order,
        )

        if needs_measurement:
            # Measurements
            # pylint: disable-next=no-member
            full_file_path = os.path.join(folder_name_output, "static_obs.dat")

            observables = deepcopy(simulation.observables)
            observables = run_tn_measurements(
                state,
                observables,
                operators,
                params,
                tensor_backend,
                tn_type,
            )
            observables.write_results(full_file_path, state.is_measured, params)

    # Dynamics
    # --------
    if "Quenches" in params:
        state.pre_timeevo_checks()

        dyn_checkpoint_file = None
        params_ii = None

        # pylint: disable-next=no-member
        qtrand = np.random.RandomState()
        qtrand.seed(params.get("seed", [11, 13, 17, 19]))
        _ = qtrand.random(1000)
        qtjump_threshold = qtrand.random()

        time = 0
        kk = 0
        for _, quench in enumerate(params["Quenches"]):
            dt_grid = quench.get_dt_grid(params)
            tevo_mode = quench.time_evolution_mode
            oqs_mode = quench.oqs_mode
            if oqs_mode in [0]:
                state.solver = KrylovSolverH
            elif oqs_mode in [1, 2]:
                state.solver = KrylovSolverNH
                if ("seed" not in params) and (oqs_mode == 1):
                    raise Exception("No seed, but quantum trajectory.")
            else:
                raise Exception("OQS mode unknown")

            # By convention, coupling parameters in the Hamiltonian which
            # do not appear in the quench, are taken from the ground state.
            # The following line will enforce this by passing params_ii=None
            # and force_rebuild_mpo=True.
            state, params_ii = update_time_dependent_terms(
                state,
                time,
                params,
                None,
                quench,
                mpo_mode,
                iso_pos,
                force_rebuild_mpo=True,
            )

            for _, dt in enumerate(dt_grid):
                kk += 1

                # Target implementation would be `"%08d_%08d" % (ii, jj)`, but for
                # compatability with current postprocessing
                int_str_ij = "%08d_%08d" % (1, kk)

                if load_dyn_from_checkpoint:
                    dyn_checkpoint_file = os.path.join(
                        folder_name_output, f"TTN_dyn_{int_str_ij}"
                    )
                    dyn_checkpoint_file_pkl = (
                        dyn_checkpoint_file + ".pkl" + ansatz.extension
                    )
                    if os.path.isfile(dyn_checkpoint_file_pkl):
                        # Found checkpoint
                        state.log_print(f"Loading checkpoint from time step {kk}.")
                        old_state = state
                        state = ansatz.read_pickle(dyn_checkpoint_file_pkl)
                        state.checkpoint_copy_simulation_attr(old_state)
                        load_dyn_from_checkpoint = False

                    time += dt
                    continue

                if int(simulation.verbosity) > 0:
                    state.log_print("Starting time-step %d" % (kk), verbosity_level=2)

                # Time-step (evaluate mid-time-step)
                time += 0.5 * dt
                state.iso_towards(iso_pos, keep_singvals=requires_singvals, trunc=True)
                state, params_ii = update_time_dependent_terms(
                    state, time, params, params_ii, quench, mpo_mode, iso_pos
                )
                state.timestep(dt, tevo_mode)

                if (oqs_mode in [1]) and (state.norm() ** 2 < qtjump_threshold):
                    # Apply quantum jumps
                    apply_quantum_jump(
                        state,
                        simulation.model,
                        operators,
                        quench,
                        time,
                        params_ii,
                        qtrand,
                    )

                    qtjump_threshold = qtrand.random()

                # Measurement
                time += 0.5 * dt
                state.iso_towards(iso_pos, keep_singvals=requires_singvals, trunc=True)
                state, params_ii = update_time_dependent_terms(
                    state,
                    time,
                    params,
                    params_ii,
                    quench,
                    mpo_mode,
                    iso_pos,
                )

                observables = deepcopy(simulation.observables)
                observables = run_tn_measurements(
                    state,
                    observables,
                    operators,
                    params,
                    tensor_backend,
                    tn_type,
                    int_str_ij,
                    time=time,
                )

                filename = "dyn_obs%08d_%08d.dat" % (1, kk)
                # pylint: disable-next=no-member
                full_file_path = os.path.join(folder_name_output, filename)

                observables.write_results(
                    full_file_path,
                    state.is_measured,
                    params,
                )

                if simulation.store_checkpoints:
                    dyn_checkpoint_file = state.checkpoint_store(
                        folder_name_output,
                        dyn_checkpoint_file,
                        int_str_ij,
                        checkpoint_indicator_file,
                        is_dyn=True,
                    )

            if load_dyn_from_checkpoint:
                msg = "No checkpoint found, although checkpoint indicator file exists."
                raise Exception(msg)

    if simulation.verbosity > 0:
        mpo.print_summary(state.log_file)

    toc = tictoc()
    if simulation.verbosity > 0:
        state.log_print("Simulation time is %2.4f." % (toc - tic))

    if simulation.has_log_file:
        state.log_close()

    # Create indicator file for finished simulation
    finished_jdic = {"cpu_time": toc - tic, "sim_hash": sim_hash}
    finished_json = os.path.join(folder_name_output, "has_finished.json")
    with open(finished_json, "w+") as fh:
        json.dump(finished_jdic, fh)

    return


def optimize(state, params, folder_name_output, store_checkpoints, sweep_order=None):
    """
    Optimize the tensor network by optimizing each tensor
    in the TN a number of times equal to num_sweeps.
    If not specified in sweep_order,
    the optimization is defined by `state.default_sweep_order` method.
    The number of sweeps and the other details
    are controlled in :py:class:`TNConvergenceParameters`

    Parameters
    ----------

    state : instance of :class:`_AbstractTN`
        State to be optimized.
    params : dict
        Contains parameters for simulation to resolve parameterization.
    folder_name_input : str
        Folder path for output and storing checkpoints.
    store_checkpoints : bool
        Flag if checkpoints should be stored (`True`) or not (`False`).
    sweep_order : List[int] | List[Tuple[int]] | None, optional
        PATH for the optimization, passed as the
        integer index of the tensor.
        Default to `None`.

    Returns
    -------

    :class:`_AbstractTN`
        State after optimization (in-place update not posisble for checkpoints).

    List[float]
        Energy after each sweep

    bool
        Status if measurement is required (True) because the state
        was updated. In case of a loaded checkpoint which returns without
        additional optimizations, `False` is returned.
    """
    needs_measurement = True
    energies = []
    if sweep_order is None:
        sweep_order = state.default_sweep_order()

    # Retrieve the convergence parameters to keep parameterization
    conv_params_parameterized = state.convergence_parameters
    conv_params = conv_params_parameterized.resolve_params_copy(params)

    # For checkpointing
    ansatz = type(state)
    intra_sweep_last = False
    stat_checkpoint_file = None
    if folder_name_output is None:
        # Some unittests run without output folder
        checkpoint_indicator_file = None
        load_stat_from_checkpoint = False
    else:
        checkpoint_indicator_file = os.path.join(
            folder_name_output, "has_stat_checkpoints.txt"
        )
        load_stat_from_checkpoint = os.path.isfile(checkpoint_indicator_file)

    # Set solver for imaginary time evolution via TDVP
    state.solver = KrylovSolverH

    # Cycle over sweeps
    for ii in range(conv_params.max_iter):
        int_str_i = "%08d" % (ii)
        outer_loop_continue = False

        # Resolve convergence parameters
        state.convergence_parameters = conv_params_parameterized.resolve_params_copy(
            params, idx=ii
        )
        update_method = state.convergence_parameters.sim_params["statics_method"]

        # Logic for convert
        # .................

        dtype = state.convergence_parameters.sim_params["data_type"]
        device = state.convergence_parameters.sim_params["device"]

        if dtype == "A":
            # Automatic converts to double complex for now, later choose
            # based on H being real or complex and tolerance for this iteration
            dtype = "Z"

        if device == "auto":
            # Automatic converts to cpu for now, later choose based on
            # devices present and bond dimension (?).
            device = "cpu"

        state.convergence_parameters.sim_params["arnoldi_tolerance"] = (
            10 * state.dtype_eps
        )

        # skipped internally if not necessary
        state.convert(dtype, device)

        if state.convergence_parameters.sim_params["random_sweep"]:
            # Shuffle works in place
            np.random.shuffle(sweep_order)

        # Cycle over optimization path
        for jj, pos in enumerate(sweep_order):
            int_str_ij = "%08d_%08d" % (ii, jj)
            tic = tictoc()

            if load_stat_from_checkpoint and (jj == 0):
                # Check for end of sweep with int_str_i
                state, energies, cp_status = _query_if_checkpoint(
                    state, folder_name_output, ansatz, int_str_i
                )

                if (cp_status == 2) or (ii + 1 == conv_params.max_iter):
                    return state, energies, False

                if cp_status == 1:
                    # do not continue loop over j, found checkpoint at end
                    outer_loop_continue = True
                    load_stat_from_checkpoint = False
                    break

                continue

            if load_stat_from_checkpoint:
                # Check for intra-sweep checkpoint
                state, energies, cp_status = _query_if_checkpoint(
                    state, folder_name_output, ansatz, int_str_ij
                )

                if cp_status == 1:
                    # found checkpoint
                    load_stat_from_checkpoint = False

                    if jj + 1 == len(sweep_order):
                        # Was the last one in the sweep ... and still not
                        # saved as checkpoint after sweep? (dj)
                        outer_loop_continue = True

                continue

            # Energy minimization with single tensor update
            if update_method in (0, 1):
                energy = state.optimize_single_tensor(pos)

            # Energy minimization with single tensor update and subspace expansion
            elif update_method == 2:
                (
                    pos_partner,
                    link_state,
                    link_partner,
                ) = state.get_pos_partner_link_expansion(pos)
                energy = state.optimize_link_expansion(
                    pos,
                    pos_partner,
                    link_state,
                    link_partner,
                )

            # Energy minimization with imaginary time evolution single-site TDVP
            elif update_method in (4, 5):
                if update_method == 5:
                    upd_fun = state.timestep_single_tensor
                else:
                    upd_fun = state.timestep_single_tensor_link_expansion
                next_pos = None if (jj + 1 == len(sweep_order)) else sweep_order[jj + 1]
                upd_fun(
                    pos,
                    next_pos,
                    -state.convergence_parameters.sim_params["imag_evo_dt"],
                )
                state.normalize()
                # Compute energy if end sweep
                if jj == len(sweep_order) - 1:
                    energy = state.compute_energy(pos)

            # Checkpoints inside the sweep are only enabled for optimization
            # taking longer than 24h per sweep
            toc = tictoc()
            opt_time = toc - tic
            predicted_sweep_time = opt_time * len(sweep_order)
            intrasweep_checkpoint = (
                predicted_sweep_time > QTEA_TIMELIMIT_INTRASWEEP_CHECKPOINTS
            )
            intra_sweep_last = jj + 1 == len(sweep_order)
            if store_checkpoints and intrasweep_checkpoint and (not intra_sweep_last):
                # Long computation time, store intra-sweep checkpoint. By default,
                # mid-sweep checkpoints are not converged states (always False)
                stat_checkpoint_file = state.checkpoint_store(
                    folder_name_output,
                    stat_checkpoint_file,
                    int_str_ij,
                    checkpoint_indicator_file,
                    jdic={"energies": energies, "converged": False},
                )

        if outer_loop_continue or load_stat_from_checkpoint:
            continue

        # Stopping criterion
        exit_by_criterion = False
        if ii > state.convergence_parameters.n_points_conv_check:
            exit_by_criterion = bool(
                np.isclose(
                    energies[-1],
                    energies[-2],
                    rtol=state.convergence_parameters.rel_deviation,
                    atol=state.convergence_parameters.abs_deviation,
                )
            )

        # Save energy and checkpoint at the end of the sweep (last intrasweep
        # is never stored)
        energies.append(energy)
        if store_checkpoints:
            stat_checkpoint_file = state.checkpoint_store(
                folder_name_output,
                stat_checkpoint_file,
                int_str_i,
                checkpoint_indicator_file,
                jdic={"energies": energies, "converged": exit_by_criterion},
            )
        intra_sweep_last = False

        # Stopping criterion
        if exit_by_criterion:
            break

    if load_stat_from_checkpoint:
        msg = "No checkpoint found, although checkpoint indicator file exists."
        raise Exception(msg)

    # Reset convergence parameters

    return state, energies, needs_measurement


def apply_quantum_jump(state, model, operators, quench, time, params, qtrand):
    """Apply a quantum jump."""
    state.normalize()
    terms_oqs = []
    weights = []

    for term in model:
        if not term.is_oqs:
            continue

        weight = term.quantum_jump_weight(state, operators, quench, time, params)
        terms_oqs.append(term)
        weights.append(weight)

    weights = np.cumsum(np.array(weights))
    weights /= weights[-1]

    rand = qtrand.random()
    idx = weights.shape[0] - 1
    for ii in range(idx):
        if rand < weights[ii]:
            idx = ii
            break

    terms_oqs[idx].quantum_jump_apply(state, operators, params, qtrand)


def update_time_dependent_terms(
    state, time, params, params_ii, quench, mpo_mode, pos, force_rebuild_mpo=False
):
    """
    Update the MPO layer according to the time-dependent couplings.

    **Arguments**

    state : :class:`_AbtractTN`

    time : float
        Time of the current step.

    params : dict
        Used as initial starting point if params_ii is None

    params_ii : dict
        Parameters of the system in the last call.

    quench :
        Quench instance contains the time-dependent functions.

    mpo_mode : int
        MPO mode required to decide on how to update the
        effective operators.

    pos : int | tuple of ints
        Default position of isometry center.

    force_rebuild_mpo : bool, optional
        Force method to re-calculate the MPO

    **Returns**

    state : state itself (updated inplace anyway)

    params_ii : updated params dict (to check for time evolution
        with constant checks)
    """
    # Default value should come from ground state search, which is solved
    # with a call to this method upfront starting every quench with params_ii=None

    # If not time dependent and not forced to rebuild, skip updating MPOs
    # as in sudden quench scenarios
    is_time_dependent = force_rebuild_mpo

    if (params_ii is None) and state.eff_op.has_oqs:
        # First call to OQS must be flagged as time-dependent as Lindblad
        # couplings are always zero in statics for MPS, TTN even if
        # the params dictionary has a non-zero value
        params_ii = deepcopy(params)
        is_time_dependent = True
    elif params_ii is None:
        params_ii = deepcopy(params)

    for key in quench.keys():
        coupl = quench[key](time, params)

        is_time_dependent = is_time_dependent or (coupl != params_ii[key])
        params_ii[key] = coupl

    if not is_time_dependent:
        return state, params_ii

    if mpo_mode in [2, 4]:
        # Update scheme without recalculating
        state.iso_towards(pos)
        state.eff_op.do_update = True
        state.eff_op.update_couplings(params_ii)
        state.build_effective_operators()
        state.eff_op.do_update = False
    else:
        mpo = state.eff_op
        mpo.update_couplings(params_ii)
        state.eff_op = None
        mpo.setup_as_eff_ops(state)

    return state, params_ii


def run_tn_measurements(
    state,
    observables,
    operators,
    params,
    tensor_backend,
    tn_type,
    postfix=None,
    time=None,
):
    """
    Run all the measurements for a tensor network.

    **Arguments**

    state : instance of _AbstractTN
        Tensor network to be measured.

    simulation : instance of ``ATTNSimulation``
        Represents all the information on the simulation.

    params : dict
        Dictionary containing the current parameters for the
        simulation.

    tensor_backend; instance of `TensorBackend`
        Tensor backend of the simulation

    tn_type: int
        Identifier for the TN ansatz (MPS, TTN)

    postfix : str or ``None``, optional
        Postfix to be attached to filename etc. If ``None``, no
        postfix is attached.
        Default to empty string via ``None``.

    time : float or ``None``, optional
        The current time during the evolution if float. If a
        time cannot be specified, e.g., for statics, pass
        ``None`` or do not pass argument.
        Default to ``None``.

    **Returns**

    Instance of ``TNObservables``. If we run in parallel, we better
    make a copy before using the buffer of the TNObservables.
    """
    # We probably need params in the future - avoid unused argument error
    _ = len(params)

    # Need iso center at default position (trunc=True to be safe
    # for close-to-degeneracies)
    iso_pos = state.default_iso_pos

    if postfix is None:
        postfix = ""
    if not isinstance(state, _AbstractTN):
        raise TypeError(f"state must be an instance of _AbstractTN, not {type(state)}.")

    observables.results_buffer["energy"] = state.compute_energy()

    # We need the square norm (not implemented on TTN level as own function)
    # `get_norm` returns the value required for a renormalization, i.e.,
    # sqrt(<psi|psi>), while we expect <psi|psi>
    observables.results_buffer["norm"] = state.norm() ** 2
    if time is not None:
        observables.results_buffer["time"] = time

    # Local observables
    # -----------------
    if state.is_measured[0]:
        local_obs = observables.obs_list["TNObsLocal"]

        for jj, name_jj in enumerate(local_obs.name):
            operator = operators.ops[local_obs.operator[jj]]

            local_obs.results_buffer[name_jj] = state.meas_local(operator)

    # Correlation measurements
    # ------------------------
    # Optmize correlators with either get_rho_ij or a better meas_tensor_product
    corr_obs = observables.obs_list["TNObsCorr"]
    if state.is_measured[1] and len(corr_obs.name) > 0:
        # Measure diagonal entries first (otherwise overwriting results
        # in measurement mode error/warning)
        corr_diag = []
        for kk, name_kk in enumerate(corr_obs.name):
            op_a = operators.ops[corr_obs.operators[kk][0]]
            op_b = operators.ops[corr_obs.operators[kk][1]]

            corr_diag_ii = np.zeros(state.num_sites, dtype=np.complex128)

            if op_a.ndim == 2:
                op_ab = op_a @ op_b
            else:
                # Assume rank-4 (but delta charge both times to the right
                op_ab = op_a.tensordot(op_b, ([2], [1]))
                op_ab.flip_links_update([0, 2])
                op_ab.trace_one_dim_pair([0, 3])
                op_ab.trace_one_dim_pair([1, 3])
            for ii, elem in enumerate(state.meas_local(op_ab)):
                # if aTTN, then diagonal entries on sites
                # with disentanglers are not local anymore, so skip
                if hasattr(state, "de_layer") and (ii in state.de_layer.de_sites):
                    continue
                corr_diag_ii[ii] = elem

            corr_diag.append(corr_diag_ii)

        state.iso_towards(iso_pos, keep_singvals=True, trunc=True)

        h_iso_center = deepcopy(state.iso_center)
        hmpo = state.eff_op
        # convert the correlation matrix to itpo for measurement
        if hasattr(state, "de_layer"):
            # include the disentanglers into the itpo
            itpo = corr_obs.to_itpo(
                operators, tensor_backend, state.num_sites, de_layer=state.de_layer
            )
            itpo = state.de_layer.contract_de_layer(itpo, tensor_backend)
        else:
            itpo = corr_obs.to_itpo(
                operators, tensor_backend, state.num_sites, de_layer=None
            )

        itpo.set_meas_status(do_measurement=True)
        state.eff_op = None
        itpo.setup_as_eff_ops(state, measurement_mode=True)

        # Retrieve results from itpo measurement
        dict_by_tpo_id = itpo.collect_measurements()
        idx = -1
        for kk, name_kk in enumerate(corr_obs.name):
            corr_mat = np.zeros((state.num_sites, state.num_sites), dtype=np.complex128)

            for ii in range(state.num_sites):
                for jj in range(state.num_sites):
                    # skip the diag terms (for aTTN diag terms without the disentangler)
                    if ii == jj and not (
                        hasattr(state, "de_layer") and (ii in state.de_layer.de_sites)
                    ):
                        continue
                    idx += 1
                    corr_mat[ii, jj] = dict_by_tpo_id[idx]

            # get the diagonal terms from local measurements
            for ii in range(state.num_sites):
                if hasattr(state, "de_layer") and (ii in state.de_layer.de_sites):
                    continue
                corr_mat[ii, ii] = corr_diag[kk][ii]

            corr_obs.results_buffer[name_kk] = corr_mat

        # Migrate counter if same MPO type
        if isinstance(hmpo, ITPO):
            hmpo.add_contraction_counters(state.eff_op)

        if (np.array(state.iso_center) != np.array(h_iso_center)).any():
            raise Exception("Iso center moved.! Cannot re-install Hamiltonian MPO.")
        state.eff_op = hmpo

    # Distance measurement (TNDistance2Pure)
    # --------------------------------------
    if state.is_measured[2]:
        dist_obs = observables.obs_list["TNDistance2Pure"]

        for jj, name_jj in enumerate(dist_obs.name):
            path_jj = dist_obs.path_to_state[jj]

            psi_tn = TN_TYPE[tn_type].read(path_jj)

            dist_obs.results_buffer[name_jj] = state.dot(psi_tn)

    # State2File measurement
    # ----------------------
    # we will store numpy arrays now independent of the flag
    if state.is_measured[3]:
        file_obs = observables.obs_list["TNState2File"]

        for jj, name_jj in enumerate(file_obs.name):
            filename_tmp = observables.eval_str_param(name_jj, params)
            filename_tmp += postfix + ".pkl" + state.extension

            if file_obs.formatting[jj] == "U":
                state.save_pickle(filename_tmp)
            elif file_obs.formatting[jj] == "F":
                filename_tmp = filename_tmp.replace(".pkl", ".")
                state.write(filename_tmp)
            elif file_obs.formatting[jj] == "D":
                state_dense = state.to_dense()
                state_dense.save_pickle(filename_tmp)

            file_obs.results_buffer[name_jj] = filename_tmp

    # TNObsTensorProduct measurement
    # ----------------------------
    if state.is_measured[4]:
        tp_obs = observables.obs_list["TNObsTensorProduct"]
        for name, ops, sites in zip(tp_obs.name, tp_obs.operators, tp_obs.sites):
            sites = [site[0] for site in sites]
            tp_operators = [operators.ops[ii] for ii in ops]
            tp_obs.results_buffer[name] = np.complex128(
                state.meas_tensor_product(tp_operators, sites)
            )

    # TNObsWeightedSum measurement
    # ----------------------------
    if state.is_measured[5]:
        ws_obs = observables.obs_list["TNObsWeightedSum"]
        if ws_obs.use_itpo and len(ws_obs.name) > 0:
            state.iso_towards(iso_pos, keep_singvals=True, trunc=True)
            h_iso_center = deepcopy(state.iso_center)
            hmpo = state.eff_op

            itpo = ws_obs.to_itpo(operators, tensor_backend, state.num_sites)

            state.eff_op = None
            itpo.setup_as_eff_ops(state, measurement_mode=True)

            # Retrieve the results
            dict_by_tpo_id = itpo.collect_measurements()
            cnt = 0
            for name, coeffs in zip(ws_obs.name, ws_obs.coeffs):
                values = np.array(
                    [dict_by_tpo_id[ii] for ii in range(cnt, cnt + len(coeffs))]
                )
                ws_obs.results_buffer[name] = np.complex128(values.sum())
                cnt += len(coeffs)

            if (np.array(state.iso_center) != np.array(h_iso_center)).any():
                raise Exception("Iso center moved.! Cannot re-install Hamiltonian MPO.")
            state.eff_op = hmpo
        else:
            # Cycle over weighted sum observables
            for name, coef, tp_ops in zip(
                ws_obs.name, ws_obs.coeffs, ws_obs.tp_operators
            ):
                op_string = []
                idxs_string = []
                if isinstance(tp_ops, list):
                    tp_op = tp_ops[0]
                else:
                    tp_op = tp_ops
                # Cycle over the TPO of a single weighted sum
                for ops, sites in zip(tp_op.operators, tp_op.sites):
                    sites = [site[0] for site in sites]
                    tp_operators = [operators.ops[ii] for ii in ops]
                    idxs_string.append(sites)
                    op_string.append(tp_operators)

                ws_obs.results_buffer[name] = np.complex128(
                    state.meas_weighted_sum(op_string, idxs_string, coef)
                )

    # TNObsProjective measurement
    # ---------------------------
    if state.is_measured[6]:
        pj_obs = observables.obs_list["TNObsProjective"]
        for name, qk_conv in zip(pj_obs.name, pj_obs.qiskit_convention):
            pj_obs.results_buffer[name] = state.meas_projective(
                nmeas=pj_obs.num_shots, qiskit_convention=qk_conv
            )

    # TNObsProbabilities measurement
    # ------------------------------
    if state.is_measured[7]:
        prob_obs = observables.obs_list["TNObsProbabilities"]
        for name, prob_type, prob_param, qk_conv in zip(
            prob_obs.name,
            prob_obs.prob_type,
            prob_obs.prob_param,
            prob_obs.qiskit_convention,
        ):
            if isinstance(name, list):
                name = name[0]
            if prob_type == "U":
                if np.isscalar(prob_param):
                    prob_param = [prob_param]
                prob_obs.results_buffer[name] = {}
                for prob_p in prob_param:
                    prob_obs.results_buffer[name] = state.meas_unbiased_probabilities(
                        prob_p,
                        qiskit_convention=qk_conv,
                        bound_probabilities=prob_obs.results_buffer[name],
                    )
            elif prob_type == "E":
                prob_obs.results_buffer[name] = state.meas_even_probabilities(
                    prob_param, qk_conv
                )
            elif prob_type == "G":
                prob_obs.results_buffer[name] = state.meas_greedy_probabilities(
                    prob_param, qk_conv
                )

    # TNObsBondEntropy measurement
    # ----------------------------
    if state.is_measured[8]:
        be_obs = observables.obs_list["TNObsBondEntropy"]
        if len(be_obs.name) == 1:
            bond_entropy = state.meas_bond_entropy()
            be_obs.results_buffer[be_obs.name[0]] = bond_entropy

    # TNObsTZeroCorr measurement
    # --------------------------
    if state.is_measured[9]:
        _ = observables.obs_list["TNObsTZeroCorr"]

    # TNObsCorr4 measurement
    # ----------------------
    if state.is_measured[10]:
        _ = observables.obs_list["TNObsCorr4"]

    # TNObsCustom measurement
    # ----------------------
    if state.is_measured[11]:
        _ = observables.obs_list["TNObsCustom"]

    return observables


def _query_if_checkpoint(state, folder_name_output, ansatz, int_str):
    """
    Queries checkpoint and returns state, energies, and status, where
    status is either 0 (no checkpoint found), 1 (checkpoint found but
    not yet converged), or 2 (checkpoint found and converged).
    """
    energies = []

    stat_checkpoint_file = os.path.join(folder_name_output, f"TTN_stat_{int_str}")
    stat_checkpoint_json = stat_checkpoint_file + ".json"
    stat_checkpoint_file_pkl = stat_checkpoint_file + ".pkl" + ansatz.extension

    cp_status = 0
    if os.path.isfile(stat_checkpoint_file_pkl):
        # Found file for the end of the ii-th sweep
        state.log_print(f"Loading checkpoint for sweeps with id {int_str}.")

        old_state = state
        state = ansatz.read_pickle(stat_checkpoint_file_pkl)
        state.checkpoint_copy_simulation_attr(old_state)

        with open(stat_checkpoint_json, "r") as fh:
            jdic = json.load(fh)
            energies = jdic["energies"]

            cp_status = 2 if jdic["converged"] else 1

    return state, energies, cp_status
