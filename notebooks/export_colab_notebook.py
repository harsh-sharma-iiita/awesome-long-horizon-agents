import json
from pathlib import Path
import csv
import numpy as np

base_dir = Path(__file__).resolve().parent.parent

# Read deep metrics json
deep_metrics_path = base_dir / "results" / "processed" / "final_exp_20261104_015549_5fcb5a61_deep_metrics.json"
with open(deep_metrics_path, "r", encoding="utf-8") as f:
    deep_metrics_data = json.load(f)

# Read cluster diffs from CSV if possible
csv_path = base_dir / "results" / "raw" / "final_exp_20261104_015549_5fcb5a61_all_episodes.csv"
cluster_diffs = []
if csv_path.exists():
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    graph_ids = sorted(list(set(r["graph_id"] for r in rows)))
    for gid in graph_ids:
        b_vals = [float(r["taint_consumption_fraction"]) for r in rows if r["graph_id"] == gid and r["condition"] == "fixed_periodic" and r["is_eligible_for_tcf"] == "True"]
        c_vals = [float(r["taint_consumption_fraction"]) for r in rows if r["graph_id"] == gid and r["condition"] == "milestone_based" and r["is_eligible_for_tcf"] == "True"]
        if b_vals and c_vals:
            cluster_diffs.append(round(float(np.mean(c_vals) - np.mean(b_vals)), 6))

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Verification Scheduling in Long-Horizon Agent Workflows\n",
                "## Publication Figures & Architecture Diagrams (Google Colab Ready)\n",
                "\n",
                "**Student:** Harsh Sharma  \n",
                "**Institution:** Indian Institute of Information Technology (IIIT), Allahabad  \n",
                "**Project:** Implementation-Based Research Assignment  \n",
                "**Dataset:** `final_exp_20261104_015549_5fcb5a61` (4,680 episodes, 90 DAG clusters)  \n",
                "\n",
                "This notebook reproduces **all diagrams and figures** from the research assignment directly inside Google Colab:\n",
                "1. **Figure 0:** Conceptual Architecture Flowchart (Planning Degradation & Control Harness Loop)\n",
                "2. **Figure 1:** Downstream Taint-Consumption Fraction (TCF) across Horizons ($H=12, 24, 36$)\n",
                "3. **Figure 2:** Fault Detection Delay across Stages (Early, Middle, Late)\n",
                "4. **Figure 3:** Pareto Frontier: Verification Overhead vs. Error Propagation\n",
                "5. **Figure 4:** Error Containment Sensitivity across Injected Fault Types\n",
                "6. **Figure 5:** Paired Contrast Distribution ($C - B$) across $N=90$ Graph Clusters\n",
                "7. **Figure 6:** Replay Re-execution Computational Overhead Upon Rollback"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Setup Dependencies and Styling\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import matplotlib.patches as patches\n",
                "import json\n",
                "from pathlib import Path\n",
                "\n",
                "# Academic publication formatting (IEEE/ACM style)\n",
                "plt.rcParams.update({\n",
                "    'font.family': 'serif',\n",
                "    'font.size': 11,\n",
                "    'axes.labelsize': 12,\n",
                "    'axes.titlesize': 13,\n",
                "    'xtick.labelsize': 10,\n",
                "    'ytick.labelsize': 10,\n",
                "    'legend.fontsize': 10,\n",
                "    'figure.titlesize': 14,\n",
                "    'figure.dpi': 150,\n",
                "    'savefig.dpi': 300,\n",
                "    'lines.linewidth': 1.5,\n",
                "    'grid.alpha': 0.4,\n",
                "    'grid.linestyle': '--'\n",
                "})\n",
                "\n",
                "COLORS = {\n",
                "    'final_only': '#7f7f7f',       # Grey (Arm A: Final-Only)\n",
                "    'fixed_periodic': '#1f77b4',   # Deep Blue (Arm B: Primary Baseline)\n",
                "    'milestone_based': '#ff7f0e',  # Orange (Arm C: Intervention)\n",
                "    'every_step': '#2ca02c'        # Green (Arm D: Upper Bound)\n",
                "}\n",
                "\n",
                "ARM_LABELS = {\n",
                "    'final_only': 'Arm A (Final-Only, K=1)',\n",
                "    'fixed_periodic': 'Arm B (Periodic, K=3)',\n",
                "    'milestone_based': 'Arm C (Milestone, K=3)',\n",
                "    'every_step': 'Arm D (Every-Step, K=H)'\n",
                "}\n",
                "print('Dependencies loaded and academic plot styling active!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 2. Load Verified Experimental Metrics (Embedded for standalone execution)\n",
                f"DEEP_METRICS = {json.dumps(deep_metrics_data, indent=2)}\n",
                f"CLUSTER_DIFFS = {json.dumps(cluster_diffs)}\n",
                "\n",
                "print('Experimental data successfully loaded into memory!')\n",
                "print(f'N = {DEEP_METRICS[\"overall\"][\"eligible_count\"]} eligible episodes across {len(CLUSTER_DIFFS)} graph clusters.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Diagram 0: Conceptual View of Planning Degradation and Control Harness"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(6.5, 8.5), dpi=150)\n",
                "ax.set_xlim(0, 10)\n",
                "ax.set_ylim(0, 12)\n",
                "ax.axis('off')\n",
                "\n",
                "boxes = [\n",
                "    ('Research goal', 'Objective and success criteria', 10.5, '#f8f9fa', '#2b2d42'),\n",
                "    ('Planning', 'Choose next action or branch', 9.1, '#f8f9fa', '#2b2d42'),\n",
                "    ('Execution', 'Tools, code, and experiments', 7.7, '#f8f9fa', '#2b2d42'),\n",
                "    ('Observation', 'Outputs and environment state', 6.3, '#f8f9fa', '#2b2d42'),\n",
                "    ('Checkpoint / recovery', 'Rollback or re-anchor', 4.9, '#f8f9fa', '#2b2d42'),\n",
                "    ('Verification', 'Tests, assertions, evidence checks', 3.5, '#f8f9fa', '#2b2d42'),\n",
                "    ('Memory / context', 'Stable state and working context', 2.1, '#f8f9fa', '#2b2d42'),\n",
                "]\n",
                "\n",
                "box_w = 4.8\n",
                "box_h = 0.95\n",
                "box_x = 2.6\n",
                "\n",
                "for title, subtitle, y_center, fill_color, text_color in boxes:\n",
                "    rect = patches.FancyBboxPatch(\n",
                "        (box_x, y_center - box_h / 2), box_w, box_h,\n",
                "        boxstyle='round,pad=0.15,rounding_size=0.2',\n",
                "        facecolor=fill_color, edgecolor='#495057', linewidth=1.4, zorder=3\n",
                "    )\n",
                "    ax.add_patch(rect)\n",
                "    ax.text(box_x + box_w / 2, y_center + 0.12, title, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color, zorder=4)\n",
                "    ax.text(box_x + box_w / 2, y_center - 0.18, subtitle, ha='center', va='center', fontsize=8.5, color='#6c757d', zorder=4)\n",
                "\n",
                "for i in range(len(boxes) - 1):\n",
                "    y_top = boxes[i][2] - box_h / 2\n",
                "    y_bot = boxes[i+1][2] + box_h / 2\n",
                "    ax.annotate('', xy=(box_x + box_w / 2, y_bot), xytext=(box_x + box_w / 2, y_top),\n",
                "                arrowprops=dict(arrowstyle='-|>', color='#495057', lw=1.5, mutation_scale=12), zorder=2)\n",
                "\n",
                "loop_x = 1.3\n",
                "y_start = 2.1\n",
                "y_end = 9.1\n",
                "ax.plot([box_x - 0.2, loop_x, loop_x, box_x - 0.2], [y_start, y_start, y_end, y_end], color='#1d3557', lw=1.8, zorder=2)\n",
                "ax.annotate('', xy=(box_x, y_end), xytext=(box_x - 0.2, y_end),\n",
                "            arrowprops=dict(arrowstyle='-|>', color='#1d3557', lw=1.8, mutation_scale=14), zorder=2)\n",
                "ax.text(loop_x - 0.22, (y_start + y_end) / 2, 'Feedback loop', ha='center', va='center', rotation=90, fontsize=9.5, fontweight='bold', color='#1d3557')\n",
                "ax.text(box_x + box_w / 2, 0.9, 'Control preserves progress and enables recovery.', ha='center', va='center', fontsize=9, fontstyle='italic', color='#495057')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig_conceptual_architecture.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 1: Downstream Error Propagation (TCF) by Task Horizon ($H=12, 24, 36$)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(7.5, 4.8))\n",
                "horizons = ['12', '24', '36']\n",
                "x = np.arange(len(horizons))\n",
                "width = 0.2\n",
                "arms = ['final_only', 'fixed_periodic', 'milestone_based', 'every_step']\n",
                "\n",
                "for i, arm in enumerate(arms):\n",
                "    means = [DEEP_METRICS['by_horizon'][h][arm]['mean_tcf'] for h in horizons]\n",
                "    stds = [DEEP_METRICS['by_horizon'][h][arm]['std_tcf'] for h in horizons]\n",
                "    sems = [s / np.sqrt(360) for s in stds]\n",
                "    offset = (i - 1.5) * width\n",
                "    ax.bar(x + offset, means, width, yerr=sems, capsize=3,\n",
                "           label=ARM_LABELS[arm], color=COLORS[arm], alpha=0.9, edgecolor='black', linewidth=0.8)\n",
                "\n",
                "ax.set_ylabel('Downstream Taint-Consumption Fraction (TCF)')\n",
                "ax.set_xlabel('Workflow Horizon ($H$ Nodes)')\n",
                "ax.set_title('Downstream Error Propagation by Task Horizon')\n",
                "ax.set_xticks(x)\n",
                "ax.set_xticklabels([f'H = {h}' for h in horizons])\n",
                "ax.set_ylim(0.5, 1.05)\n",
                "ax.grid(axis='y')\n",
                "ax.legend(frameon=True, facecolor='white', loc='lower right')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig1_tcf_by_horizon.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 2: Fault Detection Latency Across Workflow Stages (Early, Middle, Late)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(7.5, 4.8))\n",
                "positions = ['early', 'middle', 'late']\n",
                "x = np.arange(len(positions))\n",
                "width = 0.2\n",
                "arms = ['final_only', 'fixed_periodic', 'milestone_based', 'every_step']\n",
                "\n",
                "for i, arm in enumerate(arms):\n",
                "    delays = [DEEP_METRICS['by_position'][p][arm]['mean_delay'] for p in positions]\n",
                "    offset = (i - 1.5) * width\n",
                "    ax.bar(x + offset, delays, width, label=ARM_LABELS[arm],\n",
                "           color=COLORS[arm], alpha=0.9, edgecolor='black', linewidth=0.8)\n",
                "\n",
                "ax.set_ylabel('Mean Detection Delay (Execution Steps)')\n",
                "ax.set_xlabel('Fault Injection Position Bin')\n",
                "ax.set_title('Fault Detection Latency Across Workflow Stages')\n",
                "ax.set_xticks(x)\n",
                "ax.set_xticklabels(['Early (1 to H/3)', 'Middle (H/3 to 2H/3)', 'Late (2H/3 to H)'])\n",
                "ax.set_ylim(0, 25)\n",
                "ax.grid(axis='y')\n",
                "ax.legend(frameon=True, facecolor='white', loc='upper right')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig2_detection_delay_comparison.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 3: Verification Overhead vs. Error Propagation Pareto Frontier"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(7.5, 4.8))\n",
                "arms = ['final_only', 'fixed_periodic', 'milestone_based', 'every_step']\n",
                "calls = [DEEP_METRICS['arm_metrics'][arm]['mean_calls'] for arm in arms]\n",
                "tcfs = [DEEP_METRICS['arm_metrics'][arm]['mean_tcf'] for arm in arms]\n",
                "labels = ['Arm A (Final-Only)', 'Arm B (Periodic)', 'Arm C (Milestone)', 'Arm D (Every-Step)']\n",
                "\n",
                "for arm, call, tcf, label in zip(arms, calls, tcfs, labels):\n",
                "    ax.scatter(call, tcf, s=200, color=COLORS[arm], edgecolors='black', linewidth=1.2, zorder=5, label=label)\n",
                "\n",
                "ax.annotate('Arm A (1.00, 1.000)', (calls[0], tcfs[0]), textcoords='offset points', xytext=(-20, 10), ha='center', fontsize=9)\n",
                "ax.annotate('Arm B: Periodic\\n(2.74, 0.861)', (calls[1], tcfs[1]), textcoords='offset points', xytext=(-55, -22), ha='center', fontsize=9, fontweight='bold', color='#1f77b4')\n",
                "ax.annotate('Arm C: Milestone\\n(2.74, 0.901)', (calls[2], tcfs[2]), textcoords='offset points', xytext=(55, 10), ha='center', fontsize=9, fontweight='bold', color='#d95f02')\n",
                "ax.annotate('Arm D: Every-Step\\n(21.03, 0.724)', (calls[3], tcfs[3]), textcoords='offset points', xytext=(-10, 12), ha='center', fontsize=9)\n",
                "\n",
                "ax.axvline(x=2.7436, color='purple', linestyle=':', alpha=0.7, label='Matched Budget Parity (K = 2.74)')\n",
                "ax.set_xlabel('Realized Verification Calls ($K_{\\\\text{realized}}$)')\n",
                "ax.set_ylabel('Downstream Taint-Consumption Fraction (TCF)')\n",
                "ax.set_title('Verification Overhead vs. Error Propagation Trade-off')\n",
                "ax.set_xlim(0, 24)\n",
                "ax.set_ylim(0.65, 1.05)\n",
                "ax.grid(True)\n",
                "ax.legend(frameon=True, facecolor='white', loc='lower right')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig3_tradeoff_overhead_vs_propagation.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 4: Sensitivity of Downstream TCF Across Fault Categories"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(8.5, 4.8))\n",
                "fault_types = ['missing_field', 'type_corruption', 'numeric_corruption', 'broken_reference']\n",
                "x = np.arange(len(fault_types))\n",
                "width = 0.2\n",
                "arms = ['final_only', 'fixed_periodic', 'milestone_based', 'every_step']\n",
                "\n",
                "for i, arm in enumerate(arms):\n",
                "    means = [DEEP_METRICS['by_fault_type'][ft][arm]['mean_tcf'] for ft in fault_types]\n",
                "    offset = (i - 1.5) * width\n",
                "    ax.bar(x + offset, means, width, label=ARM_LABELS[arm],\n",
                "           color=COLORS[arm], alpha=0.9, edgecolor='black', linewidth=0.8)\n",
                "\n",
                "ax.set_ylabel('Mean Taint-Consumption Fraction (TCF)')\n",
                "ax.set_xlabel('Injected Fault Category')\n",
                "ax.set_title('Error Containment Sensitivity by Fault Type')\n",
                "ax.set_xticks(x)\n",
                "ax.set_xticklabels(['Missing Field', 'Type Corruption', 'Numeric Out-of-Range', 'Broken Reference'])\n",
                "ax.set_ylim(0, 1.1)\n",
                "ax.grid(axis='y')\n",
                "ax.legend(frameon=True, facecolor='white', loc='lower right')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig4_fault_type_sensitivity.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 5: Paired Difference Distribution (TCF_C - TCF_B) Across N=90 Clusters"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(7.5, 4.8))\n",
                "diffs = CLUSTER_DIFFS\n",
                "n, bins, patches = ax.hist(diffs, bins=15, color='#ff7f0e', alpha=0.7, edgecolor='black', linewidth=0.8)\n",
                "\n",
                "mean_diff = np.mean(diffs)\n",
                "ci_low, ci_high = np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)\n",
                "\n",
                "ax.axvline(0, color='black', linestyle='--', linewidth=1.2, label='Null Effect Line (C = B)')\n",
                "ax.axvline(mean_diff, color='red', linestyle='-', linewidth=2, label=f'Mean Difference: +{mean_diff:.4f}')\n",
                "ax.axvspan(ci_low, ci_high, color='red', alpha=0.15, label=f'Empirical 95% Interval: [{ci_low:.4f}, {ci_high:.4f}]')\n",
                "\n",
                "ax.set_xlabel('Paired Cluster Difference $\\\\Delta \\\\text{TCF} = \\\\text{TCF}_C - \\\\text{TCF}_B$')\n",
                "ax.set_ylabel('Number of Graph Clusters ($N=90$)')\n",
                "ax.set_title('Distribution of Paired Scheduling Contrast ($C - B$)')\n",
                "ax.grid(axis='y')\n",
                "ax.legend(frameon=True, facecolor='white', loc='upper left')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig5_paired_contrast_distribution.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Figure 6: Replay Re-execution Computational Overhead Upon Rollback"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, ax = plt.subplots(figsize=(6.5, 4.2))\n",
                "arms = ['final_only', 'fixed_periodic', 'milestone_based', 'every_step']\n",
                "replays = [DEEP_METRICS['arm_metrics'][arm]['mean_replay_nodes'] for arm in arms]\n",
                "labels = ['Arm A\\nFinal-Only', 'Arm B\\nPeriodic', 'Arm C\\nMilestone', 'Arm D\\nEvery-Step']\n",
                "\n",
                "bars = ax.bar(labels, replays, color=[COLORS[a] for a in arms], alpha=0.9, edgecolor='black', width=0.55)\n",
                "for bar in bars:\n",
                "    yval = bar.get_height()\n",
                "    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.15, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)\n",
                "\n",
                "ax.set_ylabel('Mean Replay Nodes Executed per Episode')\n",
                "ax.set_title('Computational Re-execution Overhead Upon Rollback')\n",
                "ax.set_ylim(0, 9)\n",
                "ax.grid(axis='y')\n",
                "plt.tight_layout()\n",
                "plt.savefig('fig6_replay_overhead.png', dpi=300)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Download All Figures as a ZIP File\n",
                "Run the cell below in Google Colab to download all generated PNG figures in a single `.zip` file."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import zipfile\n",
                "import os\n",
                "try:\n",
                "    from google.colab import files\n",
                "    in_colab = True\n",
                "except ImportError:\n",
                "    in_colab = False\n",
                "\n",
                "with zipfile.ZipFile('publication_figures.zip', 'w') as zipf:\n",
                "    for f in Path('.').glob('fig*.png'):\n",
                "        zipf.write(f)\n",
                "        print(f'Added {f} to publication_figures.zip')\n",
                "\n",
                "if in_colab:\n",
                "    files.download('publication_figures.zip')\n",
                "    print('Download started in browser!')\n",
                "else:\n",
                "    print('Saved publication_figures.zip locally.')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 2
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

nb_dir1 = base_dir / "notebooks"
nb_dir2 = base_dir / "AITR_Lab02_MSE2026006" / "notebooks"

for d in [nb_dir1, nb_dir2]:
    d.mkdir(parents=True, exist_ok=True)
    nb_file = d / "generate_all_figures_colab.ipynb"
    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)
    print(f"Exported Colab notebook to {nb_file}")
