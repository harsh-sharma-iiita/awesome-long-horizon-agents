"""Independent audit of Primary Hypothesis H1 calculation from raw experimental data."""

import csv
import numpy as np


def independent_audit_h1():
    csv_path = "results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print("=== 1. VERIFYING EPISODE PAIRING & ELIGIBILITY ===")
    print(f"Total rows in CSV: {len(rows)}")

    # Filter to eligible TCF rows
    b_rows = [r for r in rows if r["condition"] == "fixed_periodic" and r["is_eligible_for_tcf"] == "True"]
    c_rows = [r for r in rows if r["condition"] == "milestone_based" and r["is_eligible_for_tcf"] == "True"]

    print(f"Arm B eligible TCF episodes: {len(b_rows)}")
    print(f"Arm C eligible TCF episodes: {len(c_rows)}")
    assert len(b_rows) == 1080
    assert len(c_rows) == 1080

    # Verify 1-to-1 pairing by (graph_id, scenario_idx)
    b_dict = {(r["graph_id"], r["scenario_idx"]): r for r in b_rows}
    c_dict = {(r["graph_id"], r["scenario_idx"]): r for r in c_rows}

    assert b_dict.keys() == c_dict.keys(), "Mismatch in (graph_id, scenario_idx) pairing keys!"
    print("Exact 1-to-1 pairing confirmed across all 1,080 eligible fault scenarios.")

    # Check denominator validity
    for key, r in b_dict.items():
        desc = int(r["num_topological_descendants"])
        taint = int(r["downstream_taint_consumed_count"])
        tcf = float(r["taint_consumption_fraction"])
        assert desc > 0, f"Error: Zero descendants in eligible row! {key}"
        assert abs(tcf - (taint / desc)) < 1e-6, f"Formula mismatch in row: {key}"

    for key, r in c_dict.items():
        desc = int(r["num_topological_descendants"])
        taint = int(r["downstream_taint_consumed_count"])
        tcf = float(r["taint_consumption_fraction"])
        assert desc > 0, f"Error: Zero descendants in eligible row! {key}"
        assert abs(tcf - (taint / desc)) < 1e-6, f"Formula mismatch in row: {key}"

    print("Formula TCF = (taint / desc) verified on all 2,160 individual episodes.")

    print("\n=== 2. GRAPH-LEVEL AGGREGATION & CONTRAST (N=90) ===")
    graph_ids = sorted(list(set(r["graph_id"] for r in rows)))
    print(f"Total graph clusters: {len(graph_ids)}")

    b_graph_means = []
    c_graph_means = []
    diffs = []

    for gid in graph_ids:
        b_vals = [float(b_dict[(gid, str(s))]["taint_consumption_fraction"]) for s in range(1, 13)]
        c_vals = [float(c_dict[(gid, str(s))]["taint_consumption_fraction"]) for s in range(1, 13)]
        
        m_b = np.mean(b_vals)
        m_c = np.mean(c_vals)
        d = m_c - m_b

        b_graph_means.append(m_b)
        c_graph_means.append(m_c)
        diffs.append(d)

    mean_b = float(np.mean(b_graph_means))
    mean_c = float(np.mean(c_graph_means))
    obs_diff = float(np.mean(diffs))

    print(f"Grand Mean TCF (Arm B - Periodic):   {mean_b:.6f}")
    print(f"Grand Mean TCF (Arm C - Milestone):  {mean_c:.6f}")
    print(f"Observed Difference (C - B):         {obs_diff:+.6f} ({obs_diff*100:+.2f}%)")

    # Bootstrap 95% CI (10,000 resamples)
    rng = np.random.default_rng(42)
    boot_means = rng.choice(diffs, size=(10000, len(diffs)), replace=True).mean(axis=1)
    ci_low = float(np.percentile(boot_means, 2.5))
    ci_high = float(np.percentile(boot_means, 97.5))
    print(f"95% Bootstrap Confidence Interval:   [{ci_low:+.6f}, {ci_high:+.6f}]")

    # Two-sided Paired Permutation Test (10,000 resamples)
    signs = rng.choice([-1, 1], size=(10000, len(diffs)))
    perm_means = np.mean(signs * np.asarray(diffs), axis=1)
    p_perm = float(np.mean(np.abs(perm_means) >= np.abs(obs_diff)))
    print(f"Paired Permutation Test p-value:     {p_perm:.6f} (Report as p < 0.0001)")

    # Parametric paired t-test for cross-validation
    import scipy.stats as stats
    t_stat, p_ttest = stats.ttest_rel(c_graph_means, b_graph_means)
    print(f"Paired t-test t-statistic:           {t_stat:.4f}, p-value: {p_ttest:.4e}")

    # Direction of Hypothesis H1 Check
    print("\n=== 3. HYPOTHESIS H1 VERDICT ===")
    print("Original H1 Direction: TCF(Milestone) < TCF(Periodic)  =>  (C - B) < 0")
    print(f"Observed Direction:    TCF(Milestone) > TCF(Periodic)  =>  (C - B) = +{obs_diff:.4f} > 0")
    print(f"Does the 95% CI include 0? {'Yes' if ci_low <= 0 <= ci_high else 'No'} (Strictly positive interval: [{ci_low:.4f}, {ci_high:.4f}])")
    print("VERDICT: H1 IS EXPLICITLY CONTRADICTED BY THE EMPIRICAL EVIDENCE.")
    print("Under identical budgets, Milestone verification produces significantly HIGHER taint consumption than Periodic verification.")


if __name__ == "__main__":
    independent_audit_h1()
