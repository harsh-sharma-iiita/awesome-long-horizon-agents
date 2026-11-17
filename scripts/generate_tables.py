"""Generate publication-ready Markdown and CSV tables from processed experiment outputs."""

import csv
import json
import os
import sys

def generate_tables(run_id="final_exp_20261104_015549_5fcb5a61", results_dir="results"):
    overall_path = os.path.join(results_dir, "processed", f"{run_id}_overall_metrics.json")
    horizon_path = os.path.join(results_dir, "processed", f"{run_id}_by_horizon.json")
    contrast_path = os.path.join(results_dir, "comparisons", f"{run_id}_primary_contrast.json")
    tables_dir = os.path.join(results_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    with open(overall_path, "r", encoding="utf-8") as f:
        overall = json.load(f)
    with open(horizon_path, "r", encoding="utf-8") as f:
        by_horizon = json.load(f)
    with open(contrast_path, "r", encoding="utf-8") as f:
        contrast = json.load(f)

    # 1. Main Table
    slots_map = {"final_only": 1, "fixed_periodic": 3, "milestone_based": 3, "every_step": "H"}
    table_rows = []
    for arm in ["final_only", "fixed_periodic", "milestone_based", "every_step"]:
        s = overall[arm]
        row = {
            "Verification Arm": arm.replace("_", " ").title(),
            "Allocated Slots": slots_map[arm],
            "Mean Realized Calls": round(s["mean_realized_verifier_calls"], 2),
            "Mean TCF (Primary)": f"{s['mean_taint_consumption_fraction']:.4f} ± {s['std_taint_consumption_fraction']:.4f}",
            "Fault Coverage (FDC)": f"{s['fault_detection_coverage_all']*100:.1f}%",
            "Detection Delay (Nodes)": round(s["mean_detection_delay_nodes"], 2),
            "Task Completion": f"{s['task_completion_rate_overall']*100:.1f}%",
            "False Positive Rate": f"{s['false_positive_rate_task']*100:.1f}%",
            "Workflow Time (ms)": f"{s['mean_total_workflow_time_seconds']*1000:.2f}",
            "Verifier Time (ms)": f"{s['mean_verifier_time_seconds']*1000:.3f}",
        }
        table_rows.append(row)

    main_csv = os.path.join(tables_dir, f"{run_id}_main_results.csv")
    with open(main_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(table_rows[0].keys()))
        writer.writeheader()
        writer.writerows(table_rows)

    main_md = os.path.join(tables_dir, f"{run_id}_main_results.md")
    with open(main_md, "w", encoding="utf-8") as f:
        f.write(f"# Main Experimental Results: Verification Scheduling Comparison ({run_id})\n\n")
        f.write("| Verification Arm | Allocated Slots | Realized Calls | Mean TCF (Primary) | Fault Coverage | Detection Delay | Task Completion | False Positive Rate | Workflow Time (ms) | Verifier Time (ms) |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for r in table_rows:
            f.write(f"| {r['Verification Arm']} | {r['Allocated Slots']} | {r['Mean Realized Calls']} | {r['Mean TCF (Primary)']} | {r['Fault Coverage (FDC)']} | {r['Detection Delay (Nodes)']} | {r['Task Completion']} | {r['False Positive Rate']} | {r['Workflow Time (ms)']} | {r['Verifier Time (ms)']} |\n")
        f.write("\n\n### Primary Statistical Contrast: Arm C (Milestone) vs. Arm B (Periodic)\n\n")
        tcf_c = contrast["primary_metric_TCF"]
        f.write(f"- **Mean TCF Difference (C - B):** `{tcf_c['mean_difference']:.4f}`\n")
        f.write(f"- **Two-Sided Permutation Test p-value:** `{tcf_c['two_sided_permutation_p_value']:.4f}`\n")
        f.write(f"- **95% Bootstrap Confidence Interval:** `[{tcf_c['bootstrap_95_percentile_ci'][0]:.4f}, {tcf_c['bootstrap_95_percentile_ci'][1]:.4f}]`\n")
        f.write(f"- **Statistical Conclusion:** {tcf_c['interpretation']}.\n")

    # 2. Horizon Breakdown Table
    h_rows = []
    for h_label in ["H_12", "H_24", "H_36"]:
        h_val = h_label.split("_")[1]
        for arm in ["final_only", "fixed_periodic", "milestone_based", "every_step"]:
            s = by_horizon[h_label][arm]
            h_rows.append({
                "Horizon H": h_val,
                "Verification Arm": arm.replace("_", " ").title(),
                "Mean Realized Calls": round(s["mean_realized_verifier_calls"], 2),
                "Mean TCF": f"{s['mean_taint_consumption_fraction']:.4f}",
                "Detection Coverage": f"{s['fault_detection_coverage_all']*100:.1f}%",
                "Detection Delay": round(s["mean_detection_delay_nodes"], 2),
                "Task Completion": f"{s['task_completion_rate_overall']*100:.1f}%",
                "Workflow Time (ms)": f"{s['mean_total_workflow_time_seconds']*1000:.2f}"
            })

    h_csv = os.path.join(tables_dir, f"{run_id}_horizon_breakdown.csv")
    with open(h_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(h_rows[0].keys()))
        writer.writeheader()
        writer.writerows(h_rows)

    h_md = os.path.join(tables_dir, f"{run_id}_horizon_breakdown.md")
    with open(h_md, "w", encoding="utf-8") as f:
        f.write(f"# Horizon Sensitivity Breakdown ({run_id})\n\n")
        f.write("| Horizon H | Verification Arm | Realized Calls | Mean TCF | Detection Coverage | Detection Delay | Task Completion | Workflow Time (ms) |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in h_rows:
            f.write(f"| {r['Horizon H']} | {r['Verification Arm']} | {r['Mean Realized Calls']} | {r['Mean TCF']} | {r['Detection Coverage']} | {r['Detection Delay']} | {r['Task Completion']} | {r['Workflow Time (ms)']} |\n")

    print(f"Successfully generated tables in {tables_dir}")

if __name__ == "__main__":
    generate_tables()
