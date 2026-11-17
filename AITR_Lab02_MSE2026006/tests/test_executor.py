"""Integration tests for deterministic executor, snapshotting, rollback, and replay."""

import pytest
from src.execution.executor import WorkflowExecutor
from src.execution.fault_injection import FaultDescriptor, FaultInjector
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.tasks.task_generator import TaskGenerator


def test_executor_clean_execution():
    """Verify clean workflow executes to completion with 3 passing verification slots."""
    gen = TaskGenerator(seed=200)
    graph = gen.generate_task("test_exec_clean", horizon=12, topology_motif="fork_join")
    scheduler = FixedPeriodicScheduler(horizon=12)
    executor = WorkflowExecutor(graph, scheduler)

    res = executor.execute(run_id="run_clean_test")

    assert res.status == "ACCEPTED"
    assert res.rollback_occurred is False
    assert res.rollback_distance == 0
    assert res.replay_nodes_executed == 0
    assert res.forward_steps_executed == 12
    assert res.realized_verifier_calls == 3
    assert all(v.passed for v in res.verification_results)
    assert res.terminal_artifact is not None
    assert res.terminal_artifact.get("status") == "COMPLETED"


def test_executor_fault_and_rollback_recovery():
    """Verify fault triggers rollback to verified snapshot and single-pass clean replay."""
    gen = TaskGenerator(seed=201)
    graph = gen.generate_task("test_exec_fault", horizon=12, topology_motif="fork_join")
    scheduler = FixedPeriodicScheduler(horizon=12)
    executor = WorkflowExecutor(graph, scheduler)

    # Inject missing_field at n_01 (step 2)
    # The first scheduled check is at step 4 (slot 1)
    fault_desc = FaultDescriptor(
        fault_type="missing_field",
        target_node_id="n_01",
        position_bin="early",
        parameter_field="records"
    )
    injector = FaultInjector(fault_desc)

    res = executor.execute(run_id="run_fault_test", fault_injector=injector)

    assert res.status == "ACCEPTED"
    assert res.rollback_occurred is True
    # At step 4, check failed; latest verified snapshot was step 0 (initial state)
    # So rollback distance = 4 - 0 = 4 nodes
    assert res.rollback_distance == 4
    assert res.restored_checkpoint_step == 0
    # Replay executed nodes from step 0 to horizon (12 nodes)
    assert res.replay_nodes_executed == 12
    # Only 1 check was realized during forward pass before halt
    assert res.realized_verifier_calls == 1
    assert res.verification_results[0].passed is False
    # Injector was disarmed on replay
    assert injector.fault_descriptor.disarmed is True


def test_executor_operation_error_handling():
    """Negative test: verify executor catches and reports node execution exceptions."""
    gen = TaskGenerator(seed=202)
    graph = gen.generate_task("test_exec_err", horizon=12, topology_motif="fork_join")
    # Mutate a node to an unsupported operation
    graph.nodes["n_01"].op_type = "invalid_op_code"

    scheduler = FixedPeriodicScheduler(horizon=12)
    executor = WorkflowExecutor(graph, scheduler)
    res = executor.execute(run_id="run_error_test")

    assert res.status == "ERROR"
    assert "Unsupported operation type: invalid_op_code" in str(res.error_message)
