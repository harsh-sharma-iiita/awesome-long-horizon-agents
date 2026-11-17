"""Comprehensive Statistical and Deeper Analysis Script for Phase G."""

import csv
import json
import numpy as np
import scipy.stats as stats
from pathlib import Path
from collections import defaultdict


def bootstrap_ci(diffs, n_boot=10000, ci=95, seed=42):
    rng = np.random.default_rng(seed)
    diffs = np.asarray(diffs)
    boot_means = rng.choice(diffs, size=(n_boot, len(diffs)), replace=True).mean(axis=1)
    alpha = (100 - ci) / 2
    low = np.percentile(boot_means, alpha)
    high = np.percentile(boot_means, 100 - alpha)
    return float(low), float(high)


def paired_permutation_test(a, b, n_perm=10000, seed=42):
    rng = np.random.default_rng(seed)
    diffs = np.asarray(a) - np.asarray(b)
    obs_mean = np.mean(diffs)
    signs = rng.choice([-1, 1], size=(n_perm, len(diffs)))
    perm_means = np.mean(signs * diffs, axis=1)
    p_val = np.mean(np.abs(perm_means) >= np.abs(obs_mean))
    return float(obs_mean), float(p_val)


def cohen_d_paired(diffs):
    diffs = np.asarray(diffs)
    mean_d = np.mean(diffs)
    std_d = np.std(diffs, ddof=1)
    return float(mean_d / std_d) if std_d > 0 else 0.0


def run_full_analysis():
    raw_csv = Path("results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv")
    with open(raw_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} rows for deep statistical analysis.")

    # 1. Global Metrics per Arm
    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    arm_metrics = {}

    for arm in arms:
        arm_rows = [r for r in rows if r["condition"] == arm]
        fault_rows = [r for r in arm_rows if r["is_clean_control"] == "False"]
        clean_rows = [r for r in arm_rows if r["is_clean_control"] == "True"]
        tcf_rows = [r for r in arm_rows if r["is_eligible_for_tcf"] == "True"]

        # Dual Fault Coverage
        fdc_total = sum(1 for r in fault_rows if r["fault_detected_by_verifier"] == "True") / len(fault_rows)
        cv_faults = [r for r in fault_rows if r["is_contract_violating"] == "True"]
        fdc_contract = sum(1 for r in cv_faults if r["fault_detected_by_verifier"] == "True") / len(cv_faults)

        # Detection Delay (among detected faults)
        detected_rows = [r for r in fault_rows if r["fault_detected_by_verifier"] == "True" and r["detection_delay_nodes"] != ""]
        delays = [float(r["detection_delay_nodes"]) for r in detected_rows]
        mean_delay = float(np.mean(delays)) if delays else 0.0
        std_delay = float(np.std(delays, ddof=1)) if len(delays) > 1 else 0.0

        # TCF
        tcfs = [float(r["taint_consumption_fraction"]) for r in tcf_rows]
        mean_tcf = float(np.mean(tcfs))
        std_tcf = float(np.std(tcfs, ddof=1))
        median_tcf = float(np.median(tcfs))
        iqr_tcf = float(np.percentile(tcfs, 75) - np.percentile(tcfs, 25))

        # Completion Rate
        completion_rate = sum(1 for r in arm_rows if r["final_acceptance_passed"] == "True") / len(arm_rows)
        fault_completion = sum(1 for r in fault_rows if r["final_acceptance_passed"] == "True") / len(fault_rows)
        clean_completion = sum(1 for r in clean_rows if r["final_acceptance_passed"] == "True") / len(clean_rows)

        # False Positive Rate
        fps = sum(1 for r in clean_rows if r["false_positive_check"] == "True")
        fpr = fps / len(clean_rows) if clean_rows else 0.0

        # Calls and Runtime
        calls = [float(r["realized_verifier_calls"]) for r in arm_rows]
        workflow_times = [float(r["total_workflow_time"]) * 1000 for r in arm_rows]
        verifier_times = [float(r["total_verifier_time"]) * 1000 for r in arm_rows]
        replays = [float(r["replay_nodes_executed"]) for r in arm_rows]
        rollbacks = sum(1 for r in arm_rows if r["rollback_occurred"] == "True") / len(arm_rows)

        arm_metrics[arm] = {
            "n_episodes": len(arm_rows),
            "fdc_total": fdc_total,
            "fdc_contract": fdc_contract,
            "mean_delay": mean_delay,
            "std_delay": std_delay,
            "mean_tcf": mean_tcf,
            "std_tcf": std_tcf,
            "median_tcf": median_tcf,
            "iqr_tcf": iqr_tcf,
            "completion_overall": completion_rate,
            "completion_clean": clean_completion,
            "completion_fault": fault_completion,
            "false_positive_rate": fpr,
            "mean_calls": float(np.mean(calls)),
            "std_calls": float(np.std(calls, ddof=1)),
            "mean_workflow_time_ms": float(np.mean(workflow_times)),
            "std_workflow_time_ms": float(np.std(workflow_times, ddof=1)),
            "mean_verifier_time_ms": float(np.mean(verifier_times)),
            "std_verifier_time_ms": float(np.std(verifier_times, ddof=1)),
            "mean_replay_nodes": float(np.mean(replays)),
            "rollback_rate": rollbacks,
            "api_cost_usd": 0.00
        }

    # 2. Paired Analysis per Graph Cluster (N=90) between Arm B and Arm C
    graph_ids = sorted(list(set(r["graph_id"] for r in rows)))
    paired_clusters = []
    cluster_diffs_tcf = []
    cluster_diffs_delay = []
    cluster_diffs_calls = []

    for gid in graph_ids:
        b_g = [r for r in rows if r["graph_id"] == gid and r["condition"] == "fixed_periodic" and r["is_eligible_for_tcf"] == "True"]
        c_g = [r for r in rows if r["graph_id"] == gid and r["condition"] == "milestone_based" and r["is_eligible_for_tcf"] == "True"]
        
        b_tcf = np.mean([float(r["taint_consumption_fraction"]) for r in b_g])
        c_tcf = np.mean([float(r["taint_consumption_fraction"]) for r in c_g])

        b_det = [float(r["detection_delay_nodes"]) for r in rows if r["graph_id"] == gid and r["condition"] == "fixed_periodic" and r["fault_detected_by_verifier"] == "True"]
        c_det = [float(r["detection_delay_nodes"]) for r in rows if r["graph_id"] == gid and r["condition"] == "milestone_based" and r["fault_detected_by_verifier"] == "True"]
        b_delay = np.mean(b_det) if b_det else 0.0
        c_delay = np.mean(c_det) if c_det else 0.0

        b_calls = np.mean([float(r["realized_verifier_calls"]) for r in rows if r["graph_id"] == gid and r["condition"] == "fixed_periodic"])
        c_calls = np.mean([float(r["realized_verifier_calls"]) for r in rows if r["graph_id"] == gid and r["condition"] == "milestone_based"])

        diff_tcf = c_tcf - b_tcf
        diff_delay = c_delay - b_delay
        diff_calls = c_calls - b_calls

        cluster_diffs_tcf.append(diff_tcf)
        cluster_diffs_delay.append(diff_delay)
        cluster_diffs_calls.append(diff_calls)

        paired_clusters.append({
            "graph_id": gid,
            "b_tcf": float(b_tcf),
            "c_tcf": float(c_tcf),
            "diff_tcf": float(diff_tcf),
            "b_delay": float(b_delay),
            "c_delay": float(c_delay),
            "diff_delay": float(diff_delay),
            "b_calls": float(b_calls),
            "c_calls": float(c_calls),
            "diff_calls": float(diff_calls)
        })

    obs_diff_tcf, p_val_tcf = paired_permutation_test([p["c_tcf"] for p in paired_clusters], [p["b_tcf"] for p in paired_clusters])
    ci_low_tcf, ci_high_tcf = bootstrap_ci(cluster_diffs_tcf)
    d_tcf = cohen_d_paired(cluster_diffs_tcf)

    obs_diff_delay, p_val_delay = paired_permutation_test([p["c_delay"] for p in paired_clusters], [p["b_delay"] for p in paired_clusters])
    ci_low_delay, ci_high_delay = bootstrap_ci(cluster_diffs_delay)
    d_delay = cohen_d_paired(cluster_diffs_delay)

    obs_diff_calls, p_val_calls = paired_permutation_test([p["c_calls"] for p in paired_clusters], [p["b_calls"] for p in paired_clusters])
    ci_low_calls, ci_high_calls = bootstrap_ci(cluster_diffs_calls)

    primary_contrast = {
        "n_clusters": len(paired_clusters),
        "primary_metric": "Downstream Taint-Consumption Fraction (TCF)",
        "mean_b": float(np.mean([p["b_tcf"] for p in paired_clusters])),
        "mean_c": float(np.mean([p["c_tcf"] for p in paired_clusters])),
        "mean_diff_c_minus_b": obs_diff_tcf,
        "p_value_two_sided": p_val_tcf,
        "ci_95": [ci_low_tcf, ci_high_tcf],
        "cohens_d": d_tcf,
        "delay_contrast": {
            "mean_b": float(np.mean([p["b_delay"] for p in paired_clusters])),
            "mean_c": float(np.mean([p["c_delay"] for p in paired_clusters])),
            "mean_diff": obs_diff_delay,
            "p_value": p_val_delay,
            "ci_95": [ci_low_delay, ci_high_delay],
            "cohens_d": d_delay
        },
        "calls_contrast": {
            "mean_b": float(np.mean([p["b_calls"] for p in paired_clusters])),
            "mean_c": float(np.mean([p["c_calls"] for p in paired_clusters])),
            "mean_diff": obs_diff_calls,
            "p_value": p_val_calls,
            "ci_95": [ci_low_calls, ci_high_calls]
        }
    }

    # 3. Stratified Sensitivity Analyses
    # 3.1 Horizon Sensitivity (H=12, 24, 36)
    by_horizon = {}
    for h in [12, 24, 36]:
        by_horizon[str(h)] = {}
        h_rows = [r for r in rows if int(r["horizon"]) == h]
        for arm in arms:
            a_rows = [r for r in h_rows if r["condition"] == arm and r["is_eligible_for_tcf"] == "True"]
            tcfs = [float(r["taint_consumption_fraction"]) for r in a_rows]
            a_det = [float(r["detection_delay_nodes"]) for r in h_rows if r["condition"] == arm and r["fault_detected_by_verifier"] == "True"]
            by_horizon[str(h)][arm] = {
                "mean_tcf": float(np.mean(tcfs)),
                "std_tcf": float(np.std(tcfs, ddof=1)),
                "mean_delay": float(np.mean(a_det)) if a_det else 0.0,
                "n_episodes": len(a_rows)
            }

    # 3.2 Position Sensitivity (early, middle, late)
    by_position = {}
    for pos in ["early", "middle", "late"]:
        by_position[pos] = {}
        pos_rows = [r for r in rows if r["fault_type"] != "" and r["target_node_id"] != ""]
        # Find position bin from target node
        # In generator: early = [1, H//3], mid = [H//3+1, 2H//3], late = [2H//3+1, H]
        # Let's filter by matching scenario_idx or target node
        for arm in arms:
            # Match rows for arm with this position
            a_pos_rows = []
            for r in rows:
                if r["condition"] == arm and r["is_eligible_for_tcf"] == "True":
                    # Determine position bin from node index
                    nid = r["target_node_id"]
                    idx = int(nid.split("_")[1])
                    h = int(r["horizon"])
                    if idx <= h // 3:
                        p_bin = "early"
                    elif idx <= (2 * h) // 3:
                        p_bin = "middle"
                    else:
                        p_bin = "late"
                    if p_bin == pos:
                        a_pos_rows.append(r)
            tcfs = [float(r["taint_consumption_fraction"]) for r in a_pos_rows]
            a_det = [float(r["detection_delay_nodes"]) for r in a_pos_rows if r["fault_detected_by_verifier"] == "True"]
            by_position[pos][arm] = {
                "mean_tcf": float(np.mean(tcfs)),
                "std_tcf": float(np.std(tcfs, ddof=1)),
                "mean_delay": float(np.mean(a_det)) if a_det else 0.0,
                "n_episodes": len(a_pos_rows)
            }

    # 3.3 Fault Type Sensitivity
    by_fault_type = {}
    f_types = ["missing_field", "type_corruption", "numeric_corruption", "broken_reference"]
    for ft in f_types:
        by_fault_type[ft] = {}
        for arm in arms:
            ft_rows = [r for r in rows if r["condition"] == arm and r["fault_type"] == ft and r["is_eligible_for_tcf"] == "True"]
            tcfs = [float(r["taint_consumption_fraction"]) for r in ft_rows]
            det_rows = [r for r in ft_rows if r["fault_detected_by_verifier"] == "True"]
            by_fault_type[ft][arm] = {
                "mean_tcf": float(np.mean(tcfs)),
                "std_tcf": float(np.std(tcfs, ddof=1)),
                "fdc": len(det_rows) / len(ft_rows) if ft_rows else 0.0,
                "mean_delay": float(np.mean([float(r["detection_delay_nodes"]) for r in det_rows])) if det_rows else 0.0,
                "n_episodes": len(ft_rows)
            }

    # 3.4 Failure Case / Recovery Analysis
    # How many rollbacks occurred, how many succeeded in passing final acceptance?
    recovery_stats = {}
    for arm in arms:
        arm_rows = [r for r in rows if r["condition"] == arm]
        fault_rows = [r for r in arm_rows if r["is_clean_control"] == "False"]
        rollbacks = [r for r in fault_rows if r["rollback_occurred"] == "True"]
        succeeded_after_rollback = [r for r in rollbacks if r["final_acceptance_passed"] == "True"]
        failed_after_rollback = [r for r in rollbacks if r["final_acceptance_passed"] == "False"]
        no_rollback_succeeded = [r for r in fault_rows if r["rollback_occurred"] == "False" and r["final_acceptance_passed"] == "True"]

        recovery_stats[arm] = {
            "total_fault_episodes": len(fault_rows),
            "rollbacks_triggered": len(rollbacks),
            "recovered_passed_acceptance": len(succeeded_after_rollback),
            "failed_after_rollback": len(failed_after_rollback),
            "passed_without_rollback": len(no_rollback_succeeded),
            "final_acceptance_rate": len(succeeded_after_rollback) / len(fault_rows)
        }

    # Save to disk
    out_dir = Path("results/processed")
    with open(out_dir / "final_exp_20261104_015549_5fcb5a61_deep_metrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "arm_metrics": arm_metrics,
            "primary_contrast": primary_contrast,
            "by_horizon": by_horizon,
            "by_position": by_position,
            "by_fault_type": by_fault_type,
            "recovery_stats": recovery_stats
        }, f, indent=2)

    print("Deep metrics successfully computed and saved to results/processed/final_exp_20261104_015549_5fcb5a61_deep_metrics.json")


if __name__ == "__main__":
    run_full_analysis()
