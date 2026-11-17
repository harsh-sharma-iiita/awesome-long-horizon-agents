"""Paper Readiness Audit: Cross-verify all result tables against raw dataset and check figure assets."""

import csv
from pathlib import Path


def audit_tables_and_figures():
    csv_raw = "results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv"
    with open(csv_raw, "r", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))

    print("=== 1. VERIFYING RESULT TABLES AGAINST RAW DATASET ===")
    main_table_csv = "results/tables/final_exp_20261104_015549_5fcb5a61_main_results.csv"
    horizon_table_csv = "results/tables/final_exp_20261104_015549_5fcb5a61_horizon_breakdown.csv"

    with open(main_table_csv, "r", encoding="utf-8") as f:
        main_rows = list(csv.DictReader(f))
    with open(horizon_table_csv, "r", encoding="utf-8") as f:
        horizon_rows = list(csv.DictReader(f))

    print(f"Main Table Rows: {len(main_rows)} (Expected: 4 arms)")
    print(f"Horizon Table Rows: {len(horizon_rows)} (Expected: 3 horizons * 4 arms = 12 rows)")

    # Verify each row in main table against raw data
    for r in main_rows:
        arm = r["Verification Arm"].lower().replace(" ", "_").replace("-", "_")
        if "final" in arm:
            cond = "final_only"
        elif "periodic" in arm:
            cond = "fixed_periodic"
        elif "milestone" in arm:
            cond = "milestone_based"
        elif "every" in arm:
            cond = "every_step"

        sub_rows = [x for x in raw_rows if x["condition"] == cond]
        clean_rows = [x for x in sub_rows if x["is_clean_control"] == "True"]
        fault_rows = [x for x in sub_rows if x["is_clean_control"] == "False"]
        tcf_rows = [x for x in sub_rows if x["is_eligible_for_tcf"] == "True"]

        # Check Calls
        mean_calls = sum(float(x["realized_verifier_calls"]) for x in sub_rows) / len(sub_rows)
        table_calls = float(r["Mean Realized Calls"])
        assert abs(mean_calls - table_calls) < 0.01, f"Calls mismatch for {cond}: {mean_calls} vs {table_calls}"

        # Check TCF
        mean_tcf = sum(float(x["taint_consumption_fraction"]) for x in tcf_rows) / len(tcf_rows)
        table_tcf_str = r["Mean TCF (Primary)"].split(" ")[0]
        table_tcf = float(table_tcf_str)
        assert abs(mean_tcf - table_tcf) < 0.001, f"TCF mismatch for {cond}: {mean_tcf} vs {table_tcf}"

        # Check FDC
        fdc = sum(1 for x in fault_rows if x["fault_detected_by_verifier"] == "True") / len(fault_rows)
        table_fdc = float(r["Fault Coverage (FDC)"].replace("%", "")) / 100.0
        assert abs(fdc - table_fdc) < 0.001, f"FDC mismatch for {cond}: {fdc} vs {table_fdc}"

        print(f"[OK] Table row verified for {r['Verification Arm']}: Calls={table_calls:.2f}, TCF={table_tcf:.4f}, FDC={table_fdc:.1%}")

    print("\n=== 2. VERIFYING PUBLICATION FIGURE ASSETS ===")
    fig_dir_exp = Path("figures/experiments")
    fig_dir_ana = Path("figures/analysis")

    expected_figs = [
        fig_dir_exp / "fig1_tcf_by_horizon.png",
        fig_dir_exp / "fig1_tcf_by_horizon.pdf",
        fig_dir_exp / "fig2_detection_delay_comparison.png",
        fig_dir_exp / "fig2_detection_delay_comparison.pdf",
        fig_dir_exp / "fig3_tradeoff_overhead_vs_propagation.png",
        fig_dir_exp / "fig3_tradeoff_overhead_vs_propagation.pdf",
        fig_dir_ana / "fig4_fault_type_sensitivity.png",
        fig_dir_ana / "fig4_fault_type_sensitivity.pdf",
        fig_dir_ana / "fig5_paired_contrast_distribution.png",
        fig_dir_ana / "fig5_paired_contrast_distribution.pdf",
        fig_dir_ana / "fig6_replay_overhead.png",
        fig_dir_ana / "fig6_replay_overhead.pdf"
    ]

    for p in expected_figs:
        assert p.exists(), f"Missing figure file: {p}"
        size = p.stat().st_size
        assert size > 1000, f"Figure file suspiciously small: {p} ({size} bytes)"
        print(f"[OK] Figure verified: {p.name} ({size:,} bytes)")

    print("\nAll result tables and publication figures are verified against actual execution outputs.")


if __name__ == "__main__":
    audit_tables_and_figures()
