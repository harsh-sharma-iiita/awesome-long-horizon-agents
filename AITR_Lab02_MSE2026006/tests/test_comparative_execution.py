"""Integration tests comparing all four verification schedules on identical development tasks."""

import pytest
from src.evaluation.evaluator import IndependentEvaluator
from src.execution.executor import WorkflowExecutor
from src.execution.fault_injection import FaultDescriptor, FaultInjector
from src.schedulers.every_step import EveryStepScheduler
from src.schedulers.final_only import FinalOnlyScheduler
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.schedulers.milestone_based import MilestoneBasedScheduler
from src.tasks.task_generator import TaskGenerator


def test_four_conditions_clean_control():
    """Verify all four conditions pass on clean tasks with 0 false alarms."""
    gen = TaskGenerator(seed=500)
    graph = gen.generate_task("test_4arms_clean", horizon=12, topology_motif="fork_join")
    evaluator = IndependentEvaluator(graph)

    schedulers = {
        "final_only": FinalOnlyScheduler(horizon=12),
        "fixed_periodic": FixedPeriodicScheduler(horizon=12),
        "milestone_based": MilestoneBasedScheduler(graph),
        "every_step": EveryStepScheduler(horizon=12),
    }

    results = {}
    reports = {}
    for name, sched in schedulers.items():
        executor = WorkflowExecutor(graph, sched, condition=name)
        res = executor.execute(f"run_clean_{name}")
        rep = evaluator.evaluate_episode(res, None)
        results[name] = res
        reports[name] = rep

        assert res.status == "ACCEPTED"
        assert res.rollback_occurred is False
        assert rep.false_positive_check is False
        assert rep.final_acceptance_passed is True

    # Check allocated budget differences
    assert results["final_only"].allocated_verifier_slots == 1
    assert results["fixed_periodic"].allocated_verifier_slots == 3
    assert results["milestone_based"].allocated_verifier_slots == 3
    assert results["every_step"].allocated_verifier_slots == 12

    # Check realized verifier calls on clean run equals allocated slots
    assert results["final_only"].realized_verifier_calls == 1
    assert results["fixed_periodic"].realized_verifier_calls == 3
    assert results["milestone_based"].realized_verifier_calls == 3
    assert results["every_step"].realized_verifier_calls == 12


def test_four_conditions_fault_detection_and_budget_parity():
    """Verify error containment under identical early fault across all four arms."""
    gen = TaskGenerator(seed=501)
    graph = gen.generate_task("test_4arms_fault", horizon=12, topology_motif="fork_join")
    evaluator = IndependentEvaluator(graph)

    # Injected fault: missing_field at n_01
    fault_desc = FaultDescriptor(
        fault_type="missing_field",
        target_node_id="n_01",
        position_bin="early",
        parameter_field="records"
    )

    schedulers = {
        "final_only": FinalOnlyScheduler(horizon=12),
        "fixed_periodic": FixedPeriodicScheduler(horizon=12),
        "milestone_based": MilestoneBasedScheduler(graph),
        "every_step": EveryStepScheduler(horizon=12),
    }

    reports = {}
    for name, sched in schedulers.items():
        # Clean injector clone for each arm
        import copy
        f_clone = copy.deepcopy(fault_desc)
        injector = FaultInjector(f_clone)
        executor = WorkflowExecutor(graph, sched, condition=name)
        res = executor.execute(f"run_fault_{name}", fault_injector=injector)
        rep = evaluator.evaluate_episode(res, f_clone)
        reports[name] = rep

    # Arm D (Every-Step) catches fault immediately at step 2 (detection delay = 0)
    assert reports["every_step"].fault_detected_by_verifier is True
    assert reports["every_step"].detection_delay_nodes == 0

    # Arm A (Final-Only) detects only at step 12
    assert reports["final_only"].fault_detected_by_verifier is True
    assert reports["final_only"].detecting_check_slot == 1

    # Arm B and Arm C both detect the fault at an intermediate checkpoint
    assert reports["fixed_periodic"].fault_detected_by_verifier is True
    assert reports["milestone_based"].fault_detected_by_verifier is True

    # Arm B and C must have identical allocated budgets (3)
    assert schedulers["fixed_periodic"].allocated_slots == 3
    assert schedulers["milestone_based"].allocated_slots == 3
