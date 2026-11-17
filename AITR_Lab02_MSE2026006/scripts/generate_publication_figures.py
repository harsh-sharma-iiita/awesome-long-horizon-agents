"""Generate publication-quality figures for Phase G based strictly on verified experimental data."""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Styling settings for academic publication
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "lines.linewidth": 1.5,
    "grid.alpha": 0.4,
    "grid.linestyle": "--"
})

COLORS = {
    "final_only": "#7f7f7f",       # Grey
    "fixed_periodic": "#1f77b4",   # Deep Blue (Primary Baseline)
    "milestone_based": "#ff7f0e",  # Orange (Intervention Arm C)
    "every_step": "#2ca02c"        # Green (Upper Bound)
}

ARM_LABELS = {
    "final_only": "Arm A (Final-Only, K=1)",
    "fixed_periodic": "Arm B (Periodic, K=3)",
    "milestone_based": "Arm C (Milestone, K=3)",
    "every_step": "Arm D (Every-Step, K=H)"
}


def load_data():
    with open("results/processed/final_exp_20261104_015549_5fcb5a61_deep_metrics.json", "r", encoding="utf-8") as f:
        return json.load(f)


def plot_fig1_tcf_by_horizon(data, out_dir):
    """Figure 1: Downstream Taint-Consumption Fraction across Horizon levels."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    horizons = ["12", "24", "36"]
    x = np.arange(len(horizons))
    width = 0.2

    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    for i, arm in enumerate(arms):
        means = [data["by_horizon"][h][arm]["mean_tcf"] for h in horizons]
        stds = [data["by_horizon"][h][arm]["std_tcf"] for h in horizons]
        # Standard error: std / sqrt(n=360)
        sems = [s / np.sqrt(360) for s in stds]
        
        offset = (i - 1.5) * width
        rects = ax.bar(x + offset, means, width, yerr=sems, capsize=3,
                       label=ARM_LABELS[arm], color=COLORS[arm], alpha=0.9, edgecolor="black", linewidth=0.8)

    ax.set_ylabel("Downstream Taint-Consumption Fraction (TCF)")
    ax.set_xlabel("Workflow Horizon ($H$ Nodes)")
    ax.set_title("Downstream Error Propagation by Task Horizon")
    ax.set_xticks(x)
    ax.set_xticklabels([f"H = {h}" for h in horizons])
    ax.set_ylim(0.5, 1.05)
    ax.grid(axis="y")
    ax.legend(frameon=True, facecolor="white", loc="lower right")

    plt.tight_layout()
    fig.savefig(out_dir / "fig1_tcf_by_horizon.png")
    fig.savefig(out_dir / "fig1_tcf_by_horizon.pdf")
    plt.close(fig)
    print("Saved Figure 1 (TCF by Horizon).")


def plot_fig2_detection_delay_by_position(data, out_dir):
    """Figure 2: Fault Detection Delay across Injection Positions."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    positions = ["early", "middle", "late"]
    x = np.arange(len(positions))
    width = 0.2

    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    for i, arm in enumerate(arms):
        delays = [data["by_position"][p][arm]["mean_delay"] for p in positions]
        offset = (i - 1.5) * width
        ax.bar(x + offset, delays, width, label=ARM_LABELS[arm],
               color=COLORS[arm], alpha=0.9, edgecolor="black", linewidth=0.8)

    ax.set_ylabel("Mean Detection Delay (Execution Steps)")
    ax.set_xlabel("Fault Injection Position Bin")
    ax.set_title("Fault Detection Latency Across Workflow Stages")
    ax.set_xticks(x)
    ax.set_xticklabels(["Early (1 to H/3)", "Middle (H/3 to 2H/3)", "Late (2H/3 to H)"])
    ax.set_ylim(0, 25)
    ax.grid(axis="y")
    ax.legend(frameon=True, facecolor="white", loc="upper right")

    plt.tight_layout()
    fig.savefig(out_dir / "fig2_detection_delay_comparison.png")
    fig.savefig(out_dir / "fig2_detection_delay_comparison.pdf")
    plt.close(fig)
    print("Saved Figure 2 (Detection Delay Comparison).")


def plot_fig3_overhead_vs_propagation(data, out_dir):
    """Figure 3: Pareto Trade-off between Realized Calls and Downstream TCF."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    calls = [data["arm_metrics"][arm]["mean_calls"] for arm in arms]
    tcfs = [data["arm_metrics"][arm]["mean_tcf"] for arm in arms]
    labels = ["Arm A (Final-Only)", "Arm B (Periodic)", "Arm C (Milestone)", "Arm D (Every-Step)"]

    for arm, call, tcf, label in zip(arms, calls, tcfs, labels):
        ax.scatter(call, tcf, s=180, color=COLORS[arm], edgecolors="black", linewidth=1.2, zorder=5, label=label)

    # Annotate coordinates
    ax.annotate(f"Arm A (1.00, 1.000)", (calls[0], tcfs[0]), textcoords="offset points", xytext=(-20, 10), ha="center", fontsize=9)
    ax.annotate(f"Arm B: Periodic\n(2.74, 0.861)", (calls[1], tcfs[1]), textcoords="offset points", xytext=(-55, -20), ha="center", fontsize=9, fontweight="bold", color="#1f77b4")
    ax.annotate(f"Arm C: Milestone\n(2.74, 0.901)", (calls[2], tcfs[2]), textcoords="offset points", xytext=(55, 10), ha="center", fontsize=9, fontweight="bold", color="#d95f02")
    ax.annotate(f"Arm D: Every-Step\n(21.03, 0.724)", (calls[3], tcfs[3]), textcoords="offset points", xytext=(-10, 12), ha="center", fontsize=9)

    # Highlight budget parity line
    ax.axvline(x=2.7436, color="purple", linestyle=":", alpha=0.7, label="Matched Budget Parity (K = 2.74)")

    ax.set_xlabel("Realized Verification Calls ($K_{\\text{realized}}$)")
    ax.set_ylabel("Downstream Taint-Consumption Fraction (TCF)")
    ax.set_title("Verification Overhead vs. Error Propagation Trade-off")
    ax.set_xlim(0, 24)
    ax.set_ylim(0.65, 1.05)
    ax.grid(True)
    ax.legend(frameon=True, facecolor="white", loc="lower right")

    plt.tight_layout()
    fig.savefig(out_dir / "fig3_tradeoff_overhead_vs_propagation.png")
    fig.savefig(out_dir / "fig3_tradeoff_overhead_vs_propagation.pdf")
    plt.close(fig)
    print("Saved Figure 3 (Trade-off Overhead vs Propagation).")


def plot_fig4_fault_type_sensitivity(data, out_dir):
    """Figure 4: Sensitivity of Downstream TCF Across Fault Categories."""
    fig, ax = plt.subplots(figsize=(8, 4.5))

    fault_types = ["missing_field", "type_corruption", "numeric_corruption", "broken_reference"]
    x = np.arange(len(fault_types))
    width = 0.2

    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    for i, arm in enumerate(arms):
        means = [data["by_fault_type"][ft][arm]["mean_tcf"] for ft in fault_types]
        offset = (i - 1.5) * width
        ax.bar(x + offset, means, width, label=ARM_LABELS[arm],
               color=COLORS[arm], alpha=0.9, edgecolor="black", linewidth=0.8)

    ax.set_ylabel("Mean Taint-Consumption Fraction (TCF)")
    ax.set_xlabel("Injected Fault Category")
    ax.set_title("Error Containment Sensitivity by Fault Type")
    ax.set_xticks(x)
    ax.set_xticklabels(["Missing Field", "Type Corruption", "Numeric Out-of-Range", "Broken Reference"])
    ax.set_ylim(0, 1.1)
    ax.grid(axis="y")
    ax.legend(frameon=True, facecolor="white", loc="lower right")

    plt.tight_layout()
    fig.savefig(out_dir / "fig4_fault_type_sensitivity.png")
    fig.savefig(out_dir / "fig4_fault_type_sensitivity.pdf")
    plt.close(fig)
    print("Saved Figure 4 (Fault Type Sensitivity).")


def plot_fig5_paired_contrast_distribution(out_dir):
    """Figure 5: Paired Difference Distribution (TCF_C - TCF_B) across N=90 Clusters."""
    # Recompute cluster diffs directly from CSV
    import csv
    with open("results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    graph_ids = sorted(list(set(r["graph_id"] for r in rows)))
    diffs = []
    for gid in graph_ids:
        b_vals = [float(r["taint_consumption_fraction"]) for r in rows if r["graph_id"] == gid and r["condition"] == "fixed_periodic" and r["is_eligible_for_tcf"] == "True"]
        c_vals = [float(r["taint_consumption_fraction"]) for r in rows if r["graph_id"] == gid and r["condition"] == "milestone_based" and r["is_eligible_for_tcf"] == "True"]
        diffs.append(np.mean(c_vals) - np.mean(b_vals))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    n, bins, patches = ax.hist(diffs, bins=15, color="#ff7f0e", alpha=0.7, edgecolor="black", linewidth=0.8)

    mean_diff = np.mean(diffs)
    ci_low, ci_high = np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)

    ax.axvline(0, color="black", linestyle="--", linewidth=1.2, label="Null Effect Line (C = B)")
    ax.axvline(mean_diff, color="red", linestyle="-", linewidth=2, label=f"Mean Difference: +{mean_diff:.4f}")
    ax.axvspan(ci_low, ci_high, color="red", alpha=0.15, label=f"Empirical 95% Interval: [{ci_low:.4f}, {ci_high:.4f}]")

    ax.set_xlabel("Paired Cluster Difference $\\Delta \\text{TCF} = \\text{TCF}_C - \\text{TCF}_B$")
    ax.set_ylabel("Number of Graph Clusters ($N=90$)")
    ax.set_title("Distribution of Paired Scheduling Contrast ($C - B$)")
    ax.grid(axis="y")
    ax.legend(frameon=True, facecolor="white", loc="upper left")

    plt.tight_layout()
    fig.savefig(out_dir / "fig5_paired_contrast_distribution.png")
    fig.savefig(out_dir / "fig5_paired_contrast_distribution.pdf")
    plt.close(fig)
    print("Saved Figure 5 (Paired Contrast Distribution).")


def plot_fig6_replay_overhead(data, out_dir):
    """Figure 6: Replay Re-execution Nodes Executed during Recovery."""
    fig, ax = plt.subplots(figsize=(6, 4))

    arms = ["final_only", "fixed_periodic", "milestone_based", "every_step"]
    replays = [data["arm_metrics"][arm]["mean_replay_nodes"] for arm in arms]
    labels = ["Arm A\nFinal-Only", "Arm B\nPeriodic", "Arm C\nMilestone", "Arm D\nEvery-Step"]

    bars = ax.bar(labels, replays, color=[COLORS[a] for a in arms], alpha=0.9, edgecolor="black", width=0.55)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.15, f"{yval:.2f}", ha="center", va="bottom", fontsize=10)

    ax.set_ylabel("Mean Replay Nodes Executed per Episode")
    ax.set_title("Computational Re-execution Overhead Upon Rollback")
    ax.set_ylim(0, 9)
    ax.grid(axis="y")

    plt.tight_layout()
    fig.savefig(out_dir / "fig6_replay_overhead.png")
    fig.savefig(out_dir / "fig6_replay_overhead.pdf")
    plt.close(fig)
    print("Saved Figure 6 (Replay Overhead).")


def main():
    data = load_data()

    exp_dir = Path("figures/experiments")
    analysis_dir = Path("figures/analysis")
    exp_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    plot_fig1_tcf_by_horizon(data, exp_dir)
    plot_fig2_detection_delay_by_position(data, exp_dir)
    plot_fig3_overhead_vs_propagation(data, exp_dir)
    plot_fig4_fault_type_sensitivity(data, analysis_dir)
    plot_fig5_paired_contrast_distribution(analysis_dir)
    plot_fig6_replay_overhead(data, analysis_dir)

    print("All publication figures successfully created.")


if __name__ == "__main__":
    main()
