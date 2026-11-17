"""Pilot comparison runner across all four verification conditions on development graphs.

Tests Arm A (Final-Only), Arm B (Fixed-Periodic), Arm C (Dependency Milestones),
and Arm D (Every-Step) on identical development workflows.
"""

import copy
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath("."))

from src.evaluation.evaluator import IndependentEvaluator
from src.evaluation.metrics import MetricCalculator
from src.evaluation.statistical_analysis import StatisticalAnalysis
from src.execution.executor import WorkflowExecutor
from src.execution.fault_injection import FaultDescriptor, FaultInjector
from src.schedulers.every_step import EveryStepScheduler
from src.schedulers.final_only import FinalOnlyScheduler
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.schedulers.milestone_based import MilestoneBasedScheduler
from src.tasks.task_generator import TaskGenerator
from src.utils.logging_utils import RunTrajectoryLogger, setup_console_logger
from src.utils.reproducibility import generate_run_id, get_runtime_environment_metadata, set_seed


def run_comparative_pilot(
    num_graphs: int = 5,
    horizon: int = 12,
    output_dir: str = "runs",
    results_dir: str = "results"
):
    run_id = generate_run_id(prefix="pilot_4arms")
    logger = setup_console_logger("comparative_pilot")
    logger.info(f"Starting Comparative Pilot across 4 verification arms: {run_id}")

    os.makedirs(os.path.join(output_dir, "configurations"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "trajectories"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "raw"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "comparisons"), exist_ok=True)

    config = {
        "run_id": run_id,
        "phase": "F_pilot_comparison",
        "num_graphs": num_graphs,
        "horizon": horizon,
        "arms": ["final_only", "fixed_periodic", "milestone_based", "every_step"],
        "motifs": ["fork_join", "spine_join"],
        "allocated_slots": {
            "final_only": 1,
            "fixed_periodic": 3,
            "milestone_based": 3,
            "every_step": horizon
        },
        "environment": get_runtime_environment_metadata()
    }

    config_path = os.path.join(output_dir, "configurations", f"{run_id}_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    traj_logger = RunTrajectoryLogger(os.path.join(output_dir, "trajectories"), run_id)
    generator = TaskGenerator(seed=2000)

    # Storage for reports by arm
    arm_reports = {
        "final_only": [],
        "fixed_periodic": [],
        "milestone_based": [],
        "every_step": []
    }

    # For paired contrast B vs C by graph
    paired_tcf_by_graph = []

    start_time = time.time()
    total_episodes = 0

    fault_classes = [
        ("missing_field", "records", True),
        ("type_corruption", "records", True),
        ("numeric_corruption", "value", True),
        ("broken_reference", "record_id", True)
    ]

    for g_idx in range(num_graphs):
        graph_id = f"pilot_graph_{g_idx:02d}"
        motif = "fork_join" if g_idx % 2 == 0 else "spine_join"
        set_seed(2000 + g_idx)
        task_graph = generator.generate_task(graph_id, horizon=horizon, topology_motif=motif)
        evaluator = IndependentEvaluator(task_graph)

        topo = task_graph.topological_order
        n_len = len(topo)
        position_map = {
            "early": topo[1],
            "middle": topo[n_len // 2],
            "late": topo[-2]
        }

        # Enumerate 1 clean + 12 fault scenarios
        scenarios = [(None, None, None, None)]  # clean
        for pos_bin, target_nid in position_map.items():
            for f_type, f_field, is_viol in fault_classes:
                scenarios.append((pos_bin, target_nid, f_type, f_field))

        graph_tcf_diffs = []

        for sc_idx, (pos_bin, target_nid, f_type, f_field) in enumerate(scenarios):
            is_clean = (target_nid is None)

            # Build schedulers for this graph
            schedulers = {
                "final_only": FinalOnlyScheduler(horizon=horizon),
                "fixed_periodic": FixedPeriodicScheduler(horizon=horizon),
                "milestone_based": MilestoneBasedScheduler(task_graph),
                "every_step": EveryStepScheduler(horizon=horizon)
            }

            episode_outcomes = {}

            for arm_name, sched in schedulers.items():
                fault_desc = None
                injector = None
                if not is_clean:
                    fault_desc = FaultDescriptor(
                        fault_type=f_type,
                        target_node_id=target_nid,
                        position_bin=pos_bin,
                        parameter_field=f_field,
                        is_contract_violating=True
                    )
                    injector = FaultInjector(fault_desc)

                executor = WorkflowExecutor(task_graph, sched, condition=arm_name)
                ep_id = f"{run_id}_{graph_id}_sc{sc_idx}_{arm_name}"
                res = executor.execute(ep_id, fault_injector=injector, event_logger=traj_logger)
                report = evaluator.evaluate_episode(res, fault_desc)

                arm_reports[arm_name].append(report)
                episode_outcomes[arm_name] = report
                total_episodes += 1

                traj_logger.log_evaluator_event("episode_summary", report.to_dict())

            # Track paired difference C - B on eligible fault episodes
            rep_b = episode_outcomes["fixed_periodic"]
            rep_c = episode_outcomes["milestone_based"]
            if rep_b.is_eligible_for_tcf and rep_c.is_eligible_for_tcf:
                if rep_b.taint_consumption_fraction is not None and rep_c.taint_consumption_fraction is not None:
                    diff = rep_c.taint_consumption_fraction - rep_b.taint_consumption_fraction
                    graph_tcf_diffs.append(diff)

        if graph_tcf_diffs:
            paired_tcf_by_graph.append(float(sum(graph_tcf_diffs) / len(graph_tcf_diffs)))

    elapsed = time.time() - start_time
    logger.info(f"Completed {total_episodes} comparative pilot episodes in {elapsed:.3f} seconds.")

    # Calculate summary metrics per arm
    arm_summaries = {}
    for arm_name, reps in arm_reports.items():
        arm_summaries[arm_name] = MetricCalculator.calculate_summary_metrics(reps)

    # Save summary metrics
    raw_path = os.path.join(results_dir, "raw", f"{run_id}_arm_summaries.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(arm_summaries, f, indent=2)

    # Statistical test between B and C on pilot graphs
    obs_mean_diff, p_val = StatisticalAnalysis.paired_permutation_test(paired_tcf_by_graph, num_permutations=5000, seed=42)
    ci_low, ci_high = StatisticalAnalysis.bootstrap_confidence_interval(paired_tcf_by_graph, num_bootstrap=5000, seed=42)

    comparison_result = {
        "run_id": run_id,
        "contrast": "Arm C (Milestone) vs Arm B (Periodic)",
        "num_graphs": len(paired_tcf_by_graph),
        "mean_paired_tcf_diff_C_minus_B": obs_mean_diff,
        "two_sided_p_value": p_val,
        "bootstrap_95_ci": [ci_low, ci_high],
        "arm_metrics": arm_summaries
    }

    comp_path = os.path.join(results_dir, "comparisons", f"{run_id}_contrast_B_vs_C.json")
    with open(comp_path, "w", encoding="utf-8") as f:
        json.dump(comparison_result, f, indent=2)

    logger.info("=" * 60)
    logger.info("PILOT EXPERIMENT SUMMARY (4 ARMS)")
    logger.info("=" * 60)
    for arm_name, s in arm_summaries.items():
        logger.info(f"[{arm_name.upper()}] Allocated Slots: {config['allocated_slots'][arm_name]}")
        logger.info(f"   Mean TCF: {s.get('mean_taint_consumption_fraction'):.4f}")
        logger.info(f"   Detection Coverage: {s.get('fault_detection_coverage_all'):.2%}")
        logger.info(f"   Mean Realized Calls: {s.get('mean_realized_verifier_calls'):.2f}")
        logger.info(f"   Task Completion: {s.get('task_completion_rate_overall'):.2%}")
        logger.info(f"   False Positive Rate: {s.get('false_positive_rate_task'):.2%}")
    logger.info("=" * 60)
    logger.info(f"Primary Paired Contrast (C - B): Mean Delta TCF = {obs_mean_diff:.4f}, p = {p_val:.4f}, 95% CI = [{ci_low:.4f}, {ci_high:.4f}]")
    logger.info("=" * 60)

    return comparison_result


if __name__ == "__main__":
    run_comparative_pilot()
