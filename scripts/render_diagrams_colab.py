"""Helper script to run and immediately display all diagrams and figures in Google Colab / Jupyter."""

import subprocess
import sys
from pathlib import Path

def run_and_render():
    print("=" * 60)
    print("Generating all research figures and architecture diagrams...")
    print("=" * 60)
    
    # 1. Run figure generation script
    res1 = subprocess.run([sys.executable, "scripts/generate_publication_figures.py"], capture_output=True, text=True)
    print(res1.stdout)
    if res1.stderr:
        print("Error:", res1.stderr)
        
    # 2. Run architecture diagram generator
    res2 = subprocess.run([sys.executable, "scripts/generate_architecture_diagram.py"], capture_output=True, text=True)
    print(res2.stdout)
    if res2.stderr:
        print("Error:", res2.stderr)

    # 3. Check for IPython display in Colab
    try:
        from IPython.display import Image, display
        print("\n" + "=" * 60)
        print("RENDERING ALL GENERATED FIGURES IN COLAB:")
        print("=" * 60)
        
        figures_to_show = [
            ("Figure 0: Conceptual Architecture Flowchart", "figures/architecture/fig_conceptual_architecture.png"),
            ("Figure 1: Downstream Error Propagation (TCF) by Horizon", "figures/experiments/fig1_tcf_by_horizon.png"),
            ("Figure 2: Fault Detection Latency by Workflow Stage", "figures/experiments/fig2_detection_delay_comparison.png"),
            ("Figure 3: Pareto Frontier (Overhead vs Propagation)", "figures/experiments/fig3_tradeoff_overhead_vs_propagation.png"),
            ("Figure 4: Fault Type Sensitivity", "figures/analysis/fig4_fault_type_sensitivity.png"),
            ("Figure 5: Paired Cluster Contrast Distribution (C - B)", "figures/analysis/fig5_paired_contrast_distribution.png"),
            ("Figure 6: Replay Re-execution Computational Overhead", "figures/analysis/fig6_replay_overhead.png"),
        ]
        
        for title, rel_path in figures_to_show:
            p = Path(rel_path)
            if p.exists():
                print(f"\n▶ {title} ({p.name})")
                display(Image(filename=str(p)))
            else:
                print(f"Warning: {rel_path} not found.")
                
    except ImportError:
        print("IPython not available; figures saved to disk in figures/.")

if __name__ == "__main__":
    run_and_render()
