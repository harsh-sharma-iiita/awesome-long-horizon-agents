"""Aggregated metric calculations for G4 experimental protocol.

Calculates primary and secondary estimands across sets of EpisodeEvaluationReports,
rigorously separating denominators and preserving graph clusters.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from src.evaluation.evaluator import EpisodeEvaluationReport


class MetricCalculator:
    """Computes summary statistics and formal experimental metrics."""

    @staticmethod
    def calculate_summary_metrics(reports: List[EpisodeEvaluationReport]) -> Dict[str, Any]:
        """Compute complete metric portfolio for a set of evaluation reports."""
        if not reports:
            return {}

        fault_reports = [r for r in reports if not r.is_clean_control]
        clean_reports = [r for r in reports if r.is_clean_control]

        # 1. Primary Metric: Downstream Taint-Consumption Fraction (TCF) on eligible episodes
        eligible_tcf_reports = [r for r in fault_reports if r.is_eligible_for_tcf and r.taint_consumption_fraction is not None]
        tcf_values = [r.taint_consumption_fraction for r in eligible_tcf_reports]
        mean_tcf = float(np.mean(tcf_values)) if tcf_values else 0.0
        std_tcf = float(np.std(tcf_values)) if tcf_values else 0.0

        # Ineligible (terminal/sink) fault count
        ineligible_fault_reports = [r for r in fault_reports if not r.is_eligible_for_tcf]

        # 2. All-Fault Detection Coverage (FDC_all)
        total_faults = len(fault_reports)
        detected_all = sum(1 for r in fault_reports if r.fault_detected_by_verifier)
        fdc_all = (detected_all / total_faults) if total_faults > 0 else 0.0

        # 3. Contract-Violating Fault Detection Coverage (FDC_contract)
        contract_viol_reports = [r for r in fault_reports if r.is_contract_violating]
        total_contract_viol = len(contract_viol_reports)
        detected_contract = sum(1 for r in contract_viol_reports if r.fault_detected_by_verifier)
        fdc_contract = (detected_contract / total_contract_viol) if total_contract_viol > 0 else 0.0

        # 4. Detection Delay
        delays = [r.detection_delay_nodes for r in fault_reports if r.detection_delay_nodes is not None]
        mean_delay = float(np.mean(delays)) if delays else 0.0
        median_delay = float(np.median(delays)) if delays else 0.0

        # 5. Task Completion Rate
        completed_all = sum(1 for r in reports if r.final_acceptance_passed)
        cr_all = completed_all / len(reports)
        cr_clean = (sum(1 for r in clean_reports if r.final_acceptance_passed) / len(clean_reports)) if clean_reports else 1.0
        cr_faulted = (sum(1 for r in fault_reports if r.final_acceptance_passed) / len(fault_reports)) if fault_reports else 1.0

        # 6. False Positive Check Rate (FPR) on clean runs
        fp_count = sum(1 for r in clean_reports if r.false_positive_check)
        fpr_task = (fp_count / len(clean_reports)) if clean_reports else 0.0

        # 7. Recovery Work & Realized Calls
        realized_calls = [r.realized_verifier_calls for r in reports]
        mean_calls = float(np.mean(realized_calls)) if realized_calls else 0.0

        replay_nodes = [r.replay_nodes_executed for r in reports]
        mean_replay_nodes = float(np.mean(replay_nodes)) if replay_nodes else 0.0

        # 8. Overhead & Runtimes
        workflow_times = [r.total_workflow_time for r in reports]
        verifier_times = [r.total_verifier_time for r in reports]
        mean_wf_time = float(np.mean(workflow_times)) if workflow_times else 0.0
        mean_vf_time = float(np.mean(verifier_times)) if verifier_times else 0.0

        return {
            "num_total_episodes": len(reports),
            "num_fault_episodes": total_faults,
            "num_clean_episodes": len(clean_reports),
            "num_tcf_eligible_episodes": len(eligible_tcf_reports),
            "num_tcf_ineligible_terminal_episodes": len(ineligible_fault_reports),
            "mean_taint_consumption_fraction": mean_tcf,
            "std_taint_consumption_fraction": std_tcf,
            "fault_detection_coverage_all": fdc_all,
            "fault_detection_coverage_contract": fdc_contract,
            "mean_detection_delay_nodes": mean_delay,
            "median_detection_delay_nodes": median_delay,
            "task_completion_rate_overall": cr_all,
            "task_completion_rate_clean": cr_clean,
            "task_completion_rate_faulted": cr_faulted,
            "false_positive_rate_task": fpr_task,
            "mean_realized_verifier_calls": mean_calls,
            "mean_replay_nodes_executed": mean_replay_nodes,
            "mean_total_workflow_time_seconds": mean_wf_time,
            "mean_verifier_time_seconds": mean_vf_time,
        }
