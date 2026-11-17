"""Execution script for running the Phase E primary baseline on development graphs.

Runs the Fixed-Periodic verification scheduler (Arm B) across a small development
sample of DAG workflows with clean controls and controlled fault injections.
Saves configuration, console logs, JSONL trajectories, and summary metrics.
"""

import json
import os
import sys
import time

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath("."))

from src.evaluation.evaluator import IndependentEvaluator
from src.evaluation.metrics import MetricCalculator
from src.execution.executor import WorkflowExecutor
from src.execution.fault_injection import FaultDescriptor, FaultInjector
from src.schedulers.fixed_periodic import FixedPeriodicScheduler
from src.tasks.task_generator import TaskGenerator
from src.utils.logging_utils import RunTrajectoryLogger, setup_console_logger
from src.utils.reproducibility import generate_run_id, get_runtime_environment_metadata, set_seed


def run_baseline_pilot(
    num_graphs: int = 5,
    horizon: int = 12,
    topology_motif: str = "fork_join",
    output_dir: str = "runs",
    results_dir: str = "results/raw"
):
    run_id = generate_run_id(prefix="baseline_dev")
    logger = setup_console_logger("baseline_runner")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "configurations"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "trajectories"), exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

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
    tee.log(f"Starting Phase E Baseline Pilot Run: {run_id}")
    tee.log(f"Configuration: num_graphs={num_graphs}, horizon={horizon}, motif={topology_motif}")

    config = {
        "run_id": run_id,
        "phase": "E_development_baseline",
        "condition": "fixed_periodic",
        "allocated_slots": 3,
        "num_graphs": num_graphs,
        "horizon": horizon,
        "topology_motif": topology_motif,
        "fault_types": ["missing_field", "type_corruption", "numeric_corruption", "broken_reference"],
        "fault_positions": ["early", "middle", "late"],
        "environment": get_runtime_environment_metadata()
    }

    config_path = os.path.join(output_dir, "configurations", f"{run_id}_config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    tee.log(f"Saved configuration to {config_path}")

    traj_logger = RunTrajectoryLogger(os.path.join(output_dir, "trajectories"), run_id)
    
    generator = TaskGenerator(seed=1000)
    all_reports = []
    
    start_time = time.time()
    total_episodes_run = 0

    for g_idx in range(num_graphs):
        graph_id = f"dev_graph_{g_idx:02d}"
        set_seed(1000 + g_idx)
        task_graph = generator.generate_task(graph_id, horizon=horizon, topology_motif=topology_motif)
        evaluator = IndependentEvaluator(task_graph)
        scheduler = FixedPeriodicScheduler(horizon=horizon)

        # 1. Clean Episode
        executor = WorkflowExecutor(task_graph, scheduler)
        clean_res = executor.execute(f"{run_id}_{graph_id}_clean", fault_injector=None, event_logger=traj_logger)
        clean_report = evaluator.evaluate_episode(clean_res, None)
        all_reports.append(clean_report)
        total_episodes_run += 1
        traj_logger.log_evaluator_event("episode_summary", clean_report.to_dict())

        # 2. Injected Fault Episodes
        # Determine candidate nodes for early, middle, late positions
        topo = task_graph.topological_order
        n_len = len(topo)
        early_target = topo[1]  # n_01
        mid_target = topo[n_len // 2]  # middle
        late_target = topo[-2]  # before terminal

        position_map = {
            "early": early_target,
            "middle": mid_target,
            "late": late_target
        }

        fault_classes = [
            ("missing_field", "records", True),
            ("type_corruption", "records", True),
            ("numeric_corruption", "value", True),
            ("broken_reference", "record_id", True)
        ]

        for pos_bin, target_nid in position_map.items():
            for f_type, f_field, is_viol in fault_classes:
                fault_desc = FaultDescriptor(
                    fault_type=f_type,
                    target_node_id=target_nid,
                    position_bin=pos_bin,
                    parameter_field=f_field,
                    is_contract_violating=is_viol
                )
                injector = FaultInjector(fault_desc)
                executor = WorkflowExecutor(task_graph, scheduler)
                ep_id = f"{run_id}_{graph_id}_{pos_bin}_{f_type}"
                
                exec_res = executor.execute(ep_id, fault_injector=injector, event_logger=traj_logger)
                report = evaluator.evaluate_episode(exec_res, fault_desc)
                all_reports.append(report)
                total_episodes_run += 1

                traj_logger.log_evaluator_event("episode_summary", report.to_dict())

    elapsed = time.time() - start_time
    tee.log(f"Completed {total_episodes_run} episodes in {elapsed:.3f} seconds.")

    # Calculate summary metrics
    summary = MetricCalculator.calculate_summary_metrics(all_reports)
    summary_path = os.path.join(results_dir, f"{run_id}_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    tee.log("=" * 60)
    tee.log("PHASE E BASELINE PILOT EXECUTION SUMMARY")
    tee.log("=" * 60)
    for k, v in summary.items():
        tee.log(f"{k}: {v}")
    tee.log("=" * 60)
    tee.log(f"Summary metrics saved to {summary_path}")

    tee.close()
    return summary


if __name__ == "__main__":
    run_baseline_pilot()
