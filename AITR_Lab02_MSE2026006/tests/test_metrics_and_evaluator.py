"""Unit tests for independent evaluator, taint propagation, metrics, and statistical tests."""

import pytest
from src.evaluation.evaluator import IndependentEvaluator
from src.evaluation.metrics import MetricCalculator
from src.evaluation.statistical_analysis import StatisticalAnalysis
from src.execution.executor import WorkflowExecutor
from src.execution.fault_injection import FaultDescriptor, FaultInjector
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.tasks.task_generator import TaskGenerator


def test_evaluator_taint_propagation_and_tcf():
    """Verify taint propagation along DAG and primary TCF computation on eligible episode."""
    gen = TaskGenerator(seed=300)
    graph = gen.generate_task("test_eval_1", horizon=12, topology_motif="fork_join")
    scheduler = FixedPeriodicScheduler(horizon=12)
    executor = WorkflowExecutor(graph, scheduler)

    # Inject numeric corruption at n_02
    target_nid = "n_02"
    fault_desc = FaultDescriptor(
        fault_type="numeric_corruption",
        target_node_id=target_nid,
        position_bin="early"
    )
    injector = FaultInjector(fault_desc)
    exec_res = executor.execute("run_eval_test", fault_injector=injector)

    evaluator = IndependentEvaluator(graph)
    report = evaluator.evaluate_episode(exec_res, fault_desc)

    assert report.is_clean_control is False
    assert report.is_eligible_for_tcf is True
    assert report.num_topological_descendants > 0
    # TCF is between 0.0 and 1.0
    assert 0.0 <= report.taint_consumption_fraction <= 1.0
    assert report.fault_detected_by_verifier is True
    assert report.final_acceptance_passed is True  # Replay restored clean artifact


def test_evaluator_terminal_fault_exclusion_from_tcf():
    """Verify faults at terminal node with 0 descendants are excluded from primary TCF."""
    gen = TaskGenerator(seed=301)
    graph = gen.generate_task("test_eval_term", horizon=12, topology_motif="fork_join")
    scheduler = FixedPeriodicScheduler(horizon=12)
    executor = WorkflowExecutor(graph, scheduler)

    term_nid = graph.terminal_node_id
    fault_desc = FaultDescriptor(
        fault_type="missing_field",
        target_node_id=term_nid,
        position_bin="late",
        parameter_field="status"
    )
    injector = FaultInjector(fault_desc)
    exec_res = executor.execute("run_term_test", fault_injector=injector)

    evaluator = IndependentEvaluator(graph)
    report = evaluator.evaluate_episode(exec_res, fault_desc)

    # Terminal node has 0 descendants
    assert report.num_topological_descendants == 0
    assert report.is_eligible_for_tcf is False
    assert report.taint_consumption_fraction is None


def test_metric_calculator_dual_coverage_and_summary():
    """Verify MetricCalculator computes FDC_all, FDC_contract, and TCF properly."""
    gen = TaskGenerator(seed=302)
    graph = gen.generate_task("test_met_g", horizon=12, topology_motif="fork_join")
    scheduler = FixedPeriodicScheduler(horizon=12)
    evaluator = IndependentEvaluator(graph)

    # Episode 1: Clean
    e1 = WorkflowExecutor(graph, scheduler).execute("r1")
    rep1 = evaluator.evaluate_episode(e1, None)

    # Episode 2: Contract-violating fault detected
    f2 = FaultDescriptor("missing_field", "n_01", "early", parameter_field="records", is_contract_violating=True)
    e2 = WorkflowExecutor(graph, scheduler).execute("r2", FaultInjector(f2))
    rep2 = evaluator.evaluate_episode(e2, f2)

    # Episode 3: Non-contract-violating fault undetected
    f3 = FaultDescriptor("type_corruption", "n_02", "early", is_contract_violating=False)
    e3 = WorkflowExecutor(graph, scheduler).execute("r3")  # No injection executed
    rep3 = evaluator.evaluate_episode(e3, f3)

    metrics = MetricCalculator.calculate_summary_metrics([rep1, rep2, rep3])
    assert metrics["num_total_episodes"] == 3
    assert metrics["num_clean_episodes"] == 1
    assert metrics["num_fault_episodes"] == 2
    assert metrics["false_positive_rate_task"] == 0.0
    # FDC_all: 1 detected / 2 total faults = 0.5
    assert metrics["fault_detection_coverage_all"] == 0.5
    # FDC_contract: 1 detected / 1 contract-violating fault = 1.0
    assert metrics["fault_detection_coverage_contract"] == 1.0


def test_statistical_permutation_and_bootstrap():
    """Verify two-sided paired permutation test and bootstrap CI calculations."""
    diffs = [-0.15, -0.20, -0.10, -0.25, -0.18, -0.12, -0.05, -0.22, -0.19, -0.14]
    obs_mean, p_val = StatisticalAnalysis.paired_permutation_test(diffs, num_permutations=1000, seed=42)

    assert obs_mean < 0.0
    assert 0.0 <= p_val <= 1.0

    lower, upper = StatisticalAnalysis.bootstrap_confidence_interval(diffs, num_bootstrap=1000, ci_level=0.95, seed=42)
    assert lower <= obs_mean <= upper
