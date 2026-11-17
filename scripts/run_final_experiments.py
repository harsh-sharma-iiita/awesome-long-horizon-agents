"""Final experimental execution engine for G4 research project.

Executes the approved experimental protocol across:
- 3 Horizons (H=12, 24, 36)
- 3 Dependency motifs (fork_join, spine_join, hierarchical_reduction)
- 30 final graphs per horizon (90 graphs total, disjoint from pilot)
- 13 scenarios per graph (1 clean + 12 fault scenarios: 4 types x 3 positions)
- 4 verification arms (A: Final-Only, B: Fixed-Periodic, C: Milestone-Based, D: Every-Step)
- Total episodes: 4,680 episodes

Saves raw logs, processed tables, stratified breakdowns, and statistical paired tests.
"""

import copy
import csv
import json
import os
import sys
import time
from typing import Any, Dict, List

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


def run_final_experiments(
    graphs_per_horizon: int = 30,
    horizons: List[int] = [12, 24, 36],
    output_dir: str = "runs",
    results_dir: str = "results"
):
    run_id = generate_run_id(prefix="final_exp")
    logger = setup_console_logger("final_runner")
    logger.info(f"============================================================")
    logger.info(f"STARTING FINAL EXPERIMENTAL CAMPAIGN: {run_id}")
    logger.info(f"Horizons: {horizons}, Graphs/Horizon: {graphs_per_horizon}, Total Graphs: {len(horizons) * graphs_per_horizon}")
    logger.info(f"============================================================")

    # Prepare directories
    os.makedirs(os.path.join(output_dir, "configurations"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "trajectories"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "raw"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "processed"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "tables"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "comparisons"), exist_ok=True)

    log_file = os.path.join(output_dir, "logs", f"{run_id}_console.log")
    
    class TeeLogger:
        def __init__(self, filepath):
            self.file = open(filepath, "w", encoding="utf-8")
        def log(self, msg):
            logger.info(msg)
            self.file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
            self.file.flush()
        def close(self):
            self.file.close()

    tee = TeeLogger(log_file)
    tee.log(f"Final Experiment Campaign: {run_id}")

    config = {
        "run_id": run_id,
        "phase": "F_final_evaluation",
        "graphs_per_horizon": graphs_per_horizon,
        "horizons": horizons,
        "total_graphs": len(horizons) * graphs_per_horizon,
        "arms": ["final_only", "fixed_periodic", "milestone_based", "every_step"],
        "motifs": ["fork_join", "spine_join", "hierarchical_reduction"],
        "fault_types": ["missing_field", "type_corruption", "numeric_corruption", "broken_reference"],
        "fault_positions": ["early", "middle", "late"],
        "scenarios_per_graph": 13,
        "expected_total_episodes": len(horizons) * graphs_per_horizon * 13 * 4,
        "allocated_slots": {
            "final_only": 1,
            "fixed_periodic": 3,
            "milestone_based": 3,
            "every_step": "H"
        },
        "recovery_policy": "restore_last_verified_and_replay_once",
        "environment": get_runtime_environment_metadata()
    }

    config_path = os.path.join(output_dir, "configurations", f"{run_id}_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    tee.log(f"Frozen configuration saved to {config_path}")

    traj_logger = RunTrajectoryLogger(os.path.join(output_dir, "trajectories"), run_id)
    generator = TaskGenerator(seed=50000)

    # Master raw records
    raw_episodes_data: List[Dict[str, Any]] = []
    arm_reports: Dict[str, List[Any]] = {
        "final_only": [],
        "fixed_periodic": [],
        "milestone_based": [],
        "every_step": []
    }

    # Tracking paired differences by graph for statistical testing
    paired_tcf_by_graph: List[float] = []
    paired_delay_by_graph: List[float] = []
    paired_calls_by_graph: List[float] = []

    start_wall_time = time.time()
    total_episodes_executed = 0

    fault_classes = [
        ("missing_field", "records", True),
        ("type_corruption", "records", True),
        ("numeric_corruption", "value", True),
        ("broken_reference", "record_id", True)
    ]

    motifs = ["fork_join", "spine_join", "hierarchical_reduction"]

    for horizon in horizons:
        tee.log(f"--- Executing Horizon H={horizon} ({graphs_per_horizon} graphs) ---")
        for g_idx in range(graphs_per_horizon):
            graph_id = f"final_h{horizon}_g{g_idx:02d}"
            motif = motifs[g_idx % len(motifs)]
            graph_seed = 50000 + horizon * 1000 + g_idx
            set_seed(graph_seed)

            task_graph = generator.generate_task(graph_id, horizon=horizon, topology_motif=motif)
            evaluator = IndependentEvaluator(task_graph)

            topo = task_graph.topological_order
            n_len = len(topo)
            early_node = topo[1]
            mid_node = topo[n_len // 2]
            late_node = topo[-2]

            position_map = {
                "early": early_node,
                "middle": mid_node,
                "late": late_node
            }

            scenarios = [(None, None, None, None)]  # clean
            for pos_bin, target_nid in position_map.items():
                for f_type, f_field, is_viol in fault_classes:
                    scenarios.append((pos_bin, target_nid, f_type, f_field))

            graph_diffs_tcf = []
            graph_diffs_delay = []
            graph_diffs_calls = []

            for sc_idx, (pos_bin, target_nid, f_type, f_field) in enumerate(scenarios):
                is_clean = (target_nid is None)

                schedulers = {
                    "final_only": FinalOnlyScheduler(horizon=horizon),
                    "fixed_periodic": FixedPeriodicScheduler(horizon=horizon),
                    "milestone_based": MilestoneBasedScheduler(task_graph),
                    "every_step": EveryStepScheduler(horizon=horizon)
                }

                scenario_reports = {}

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

                    exec_res = executor.execute(ep_id, fault_injector=injector, event_logger=traj_logger)
                    report = evaluator.evaluate_episode(exec_res, fault_desc)

                    arm_reports[arm_name].append(report)
                    scenario_reports[arm_name] = report
                    total_episodes_executed += 1

                    # Record flat dictionary for CSV/JSON raw dataset
                    ep_dict = report.to_dict()
                    ep_dict["horizon"] = horizon
                    ep_dict["motif"] = motif
                    ep_dict["graph_seed"] = graph_seed
                    ep_dict["scenario_idx"] = sc_idx
                    ep_dict["allocated_slots"] = sched.allocated_slots
                    raw_episodes_data.append(ep_dict)

                    traj_logger.log_evaluator_event("episode_summary", ep_dict)

                # Collect paired contrasts between Arm B and Arm C on eligible fault episodes
                rep_b = scenario_reports["fixed_periodic"]
                rep_c = scenario_reports["milestone_based"]
                if rep_b.is_eligible_for_tcf and rep_c.is_eligible_for_tcf:
                    if rep_b.taint_consumption_fraction is not None and rep_c.taint_consumption_fraction is not None:
                        diff_tcf = rep_c.taint_consumption_fraction - rep_b.taint_consumption_fraction
                        graph_diffs_tcf.append(diff_tcf)
                    if rep_b.detection_delay_nodes is not None and rep_c.detection_delay_nodes is not None:
                        diff_delay = rep_c.detection_delay_nodes - rep_b.detection_delay_nodes
                        graph_diffs_delay.append(diff_delay)
                    diff_calls = rep_c.realized_verifier_calls - rep_b.realized_verifier_calls
                    graph_diffs_calls.append(diff_calls)

            if graph_diffs_tcf:
                paired_tcf_by_graph.append(float(sum(graph_diffs_tcf) / len(graph_diffs_tcf)))
            if graph_diffs_delay:
                paired_delay_by_graph.append(float(sum(graph_diffs_delay) / len(graph_diffs_delay)))
            if graph_diffs_calls:
                paired_calls_by_graph.append(float(sum(graph_diffs_calls) / len(graph_diffs_calls)))

    total_duration = time.time() - start_wall_time
    tee.log(f"============================================================")
    tee.log(f"CAMPAIGN COMPLETED: Executed {total_episodes_executed} episodes in {total_duration:.2f} seconds ({total_duration/total_episodes_executed*1000:.2f} ms/episode).")
    tee.log(f"============================================================")

    # 1. Save Raw CSV & JSONL Dataset
    raw_csv_path = os.path.join(results_dir, "raw", f"{run_id}_all_episodes.csv")
    fieldnames = list(raw_episodes_data[0].keys())
    with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(raw_episodes_data)
    tee.log(f"Saved raw episode CSV to {raw_csv_path}")

    # 2. Compute Overall Summary Metrics per Arm
    overall_arm_metrics = {}
    for arm_name, reps in arm_reports.items():
        overall_arm_metrics[arm_name] = MetricCalculator.calculate_summary_metrics(reps)

    overall_metrics_path = os.path.join(results_dir, "processed", f"{run_id}_overall_metrics.json")
    with open(overall_metrics_path, "w", encoding="utf-8") as f:
        json.dump(overall_arm_metrics, f, indent=2)
    tee.log(f"Saved processed overall metrics to {overall_metrics_path}")

    # 3. Stratified Metrics by Horizon
    horizon_metrics = {}
    for h in horizons:
        horizon_metrics[f"H_{h}"] = {}
        for arm_name, reps in arm_reports.items():
            h_reps = [r for r in reps if raw_episodes_data[arm_reports[arm_name].index(r) * 4]["horizon"] == h]
            horizon_metrics[f"H_{h}"][arm_name] = MetricCalculator.calculate_summary_metrics(h_reps)

    horizon_metrics_path = os.path.join(results_dir, "processed", f"{run_id}_by_horizon.json")
    with open(horizon_metrics_path, "w", encoding="utf-8") as f:
        json.dump(horizon_metrics, f, indent=2)

    # 4. Stratified Metrics by Fault Position
    pos_metrics = {}
    for pos in ["early", "middle", "late"]:
        pos_metrics[pos] = {}
        for arm_name, reps in arm_reports.items():
            p_reps = [r for r in reps if not r.is_clean_control and r.fault_type is not None]
            pos_metrics[pos][arm_name] = MetricCalculator.calculate_summary_metrics(p_reps)

    pos_metrics_path = os.path.join(results_dir, "processed", f"{run_id}_by_position.json")
    with open(pos_metrics_path, "w", encoding="utf-8") as f:
        json.dump(pos_metrics, f, indent=2)

    # 5. Primary Statistical Hypothesis Testing: Arm C (Milestone) vs Arm B (Periodic)
    obs_mean_tcf_diff, p_val_tcf = StatisticalAnalysis.paired_permutation_test(paired_tcf_by_graph, num_permutations=10000, seed=42)
    ci_low_tcf, ci_high_tcf = StatisticalAnalysis.bootstrap_confidence_interval(paired_tcf_by_graph, num_bootstrap=10000, seed=42)

    obs_mean_delay_diff, p_val_delay = StatisticalAnalysis.paired_permutation_test(paired_delay_by_graph, num_permutations=10000, seed=42)
    ci_low_delay, ci_high_delay = StatisticalAnalysis.bootstrap_confidence_interval(paired_delay_by_graph, num_bootstrap=10000, seed=42)

    obs_mean_calls_diff, p_val_calls = StatisticalAnalysis.paired_permutation_test(paired_calls_by_graph, num_permutations=10000, seed=42)

    primary_contrast = {
        "run_id": run_id,
        "primary_contrast": "Arm C (Milestone-Based) minus Arm B (Fixed-Periodic)",
        "unit_of_clustering": "Task Graph",
        "num_clusters_N": len(paired_tcf_by_graph),
        "primary_metric_TCF": {
            "mean_difference": obs_mean_tcf_diff,
            "two_sided_permutation_p_value": p_val_tcf,
            "bootstrap_95_percentile_ci": [ci_low_tcf, ci_high_tcf],
            "significance_at_05": p_val_tcf < 0.05,
            "interpretation": (
                "Statistically significant reduction in taint consumption" if (p_val_tcf < 0.05 and obs_mean_tcf_diff < 0)
                else ("Statistically significant increase in taint consumption" if (p_val_tcf < 0.05 and obs_mean_tcf_diff > 0)
                      else "No statistically significant difference in taint consumption")
            )
        },
        "secondary_metric_delay": {
            "mean_difference": obs_mean_delay_diff,
            "two_sided_p_value": p_val_delay,
            "bootstrap_95_ci": [ci_low_delay, ci_high_delay]
        },
        "secondary_metric_calls": {
            "mean_difference": obs_mean_calls_diff,
            "two_sided_p_value": p_val_calls
        }
    }

    contrast_path = os.path.join(results_dir, "comparisons", f"{run_id}_primary_contrast.json")
    with open(contrast_path, "w", encoding="utf-8") as f:
        json.dump(primary_contrast, f, indent=2)
    tee.log(f"Saved primary statistical contrast to {contrast_path}")

    # 6. Generate Publication-Ready Comparison Tables (Markdown & CSV)
    table_csv_path = os.path.join(results_dir, "tables", f"{run_id}_main_results.csv")
    table_md_path = os.path.join(results_dir, "tables", f"{run_id}_main_results.md")

    table_rows = []
    for arm_name in ["final_only", "fixed_periodic", "milestone_based", "every_step"]:
        s = overall_arm_metrics[arm_name]
        row = {
            "Verification Arm": arm_name.replace("_", " ").title(),
            "Allocated Slots": config["allocated_slots"][arm_name],
            "Mean Realized Calls": round(s["mean_realized_verifier_calls"], 2),
            "Mean TCF (Primary)": f"{s['mean_taint_consumption_fraction']:.4f} ± {s['std_taint_consumption_fraction']:.4f}",
            "Fault Coverage (FDC)": f"{s['fault_detection_coverage_all']*100:.1f}%",
            "Detection Delay (Nodes)": round(s["mean_detection_delay_nodes"], 2),
            "Task Completion": f"{s['task_completion_rate_overall']*100:.1f}%",
            "False Positive Rate": f"{s['false_positive_rate_task']*100:.1f}%",
            "Workflow Time (s)": f"{s['mean_total_workflow_time_seconds']*1000:.2f} ms",
            "Verifier Time (s)": f"{s['mean_verifier_time_seconds']*1000:.3f} ms",
        }
        table_rows.append(row)

    with open(table_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(table_rows[0].keys()))
        writer.writeheader()
        writer.writerows(table_rows)

    with open(table_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Main Experimental Results: Verification Scheduling Comparison ({run_id})\n\n")
        f.write("| Verification Arm | Allocated Slots | Realized Calls | Mean TCF (Primary) | Fault Coverage | Detection Delay | Task Completion | False Positive Rate | Workflow Time | Verifier Time |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for r in table_rows:
            f.write(f"| {r['Verification Arm']} | {r['Allocated Slots']} | {r['Mean Realized Calls']} | {r['Mean TCF (Primary)']} | {r['Fault Coverage (FDC)']} | {r['Detection Delay (Nodes)']} | {r['Task Completion']} | {r['False Positive Rate']} | {r['Workflow Time (s)']} | {r['Verifier Time (s)']} |\n")
        f.write("\n\n### Primary Statistical Contrast: Arm C (Milestone) vs. Arm B (Periodic)\n\n")
        f.write(f"- **Mean TCF Difference (C - B):** `{obs_mean_tcf_diff:.4f}`\n")
        f.write(f"- **Two-Sided Permutation Test p-value:** `{p_val_tcf:.4f}`\n")
        f.write(f"- **95% Bootstrap Confidence Interval:** `[{ci_low_tcf:.4f}, {ci_high_tcf:.4f}]`\n")
        f.write(f"- **Statistical Conclusion:** {primary_contrast['primary_metric_TCF']['interpretation']}.\n")

    tee.log(f"Generated results tables at {table_md_path}")

    # Console Summary
    tee.log("=" * 70)
    tee.log("FINAL EXPERIMENTAL RESULTS SUMMARY")
    tee.log("=" * 70)
    for r in table_rows:
        tee.log(f"[{r['Verification Arm']}] Slots={r['Allocated Slots']}, Realized={r['Mean Realized Calls']}, TCF={r['Mean TCF (Primary)']}, Delay={r['Detection Delay (Nodes)']}, CR={r['Task Completion']}")
    tee.log("=" * 70)
    tee.log(f"PRIMARY CONTRAST (C - B): Mean Delta TCF = {obs_mean_tcf_diff:.4f}, p = {p_val_tcf:.4f}, 95% CI = [{ci_low_tcf:.4f}, {ci_high_tcf:.4f}]")
    tee.log(f"Result Interpretation: {primary_contrast['primary_metric_TCF']['interpretation']}")
    tee.log("=" * 70)

    tee.close()
    return primary_contrast


if __name__ == "__main__":
    run_final_experiments()
