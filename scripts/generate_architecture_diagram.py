"""Generate high-resolution Figure 1 Conceptual Architecture Diagram using matplotlib."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def generate_conceptual_architecture(out_dir):
    fig, ax = plt.subplots(figsize=(6.5, 8.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    boxes = [
        ("Research goal", "Objective and success criteria", 10.5, "#f8f9fa", "#2b2d42"),
        ("Planning", "Choose next action or branch", 9.1, "#f8f9fa", "#2b2d42"),
        ("Execution", "Tools, code, and experiments", 7.7, "#f8f9fa", "#2b2d42"),
        ("Observation", "Outputs and environment state", 6.3, "#f8f9fa", "#2b2d42"),
        ("Checkpoint / recovery", "Rollback or re-anchor", 4.9, "#f8f9fa", "#2b2d42"),
        ("Verification", "Tests, assertions, evidence checks", 3.5, "#f8f9fa", "#2b2d42"),
        ("Memory / context", "Stable state and working context", 2.1, "#f8f9fa", "#2b2d42"),
    ]

    box_w = 4.8
    box_h = 0.95
    box_x = 2.6

    for title, subtitle, y_center, fill_color, text_color in boxes:
        # Draw rounded rectangle
        rect = patches.FancyBboxPatch(
            (box_x, y_center - box_h / 2),
            box_w, box_h,
            boxstyle="round,pad=0.15,rounding_size=0.2",
            facecolor=fill_color,
            edgecolor="#495057",
            linewidth=1.4,
            zorder=3
        )
        ax.add_patch(rect)

        # Text
        ax.text(box_x + box_w / 2, y_center + 0.12, title,
                ha="center", va="center", fontsize=11, fontweight="bold", color=text_color, zorder=4)
        ax.text(box_x + box_w / 2, y_center - 0.18, subtitle,
                ha="center", va="center", fontsize=8.5, color="#6c757d", zorder=4)

    # Draw forward downward arrows between boxes
    for i in range(len(boxes) - 1):
        y_top = boxes[i][2] - box_h / 2
        y_bot = boxes[i+1][2] + box_h / 2
        ax.annotate(
            "",
            xy=(box_x + box_w / 2, y_bot),
            xytext=(box_x + box_w / 2, y_top),
            arrowprops=dict(arrowstyle="-|>", color="#495057", lw=1.5, mutation_scale=12),
            zorder=2
        )

    # Draw Feedback loop on the left
    loop_x = 1.3
    y_start = 2.1  # Memory / context level
    y_end = 9.1    # Planning level

    # Large bracket / arrow
    ax.plot([box_x - 0.2, loop_x, loop_x, box_x - 0.2], [y_start, y_start, y_end, y_end],
            color="#1d3557", lw=1.8, zorder=2)
    ax.annotate(
        "",
        xy=(box_x, y_end),
        xytext=(box_x - 0.2, y_end),
        arrowprops=dict(arrowstyle="-|>", color="#1d3557", lw=1.8, mutation_scale=14),
        zorder=2
    )

    # Vertical text on feedback loop
    ax.text(loop_x - 0.22, (y_start + y_end) / 2, "Feedback loop",
            ha="center", va="center", rotation=90, fontsize=9.5, fontweight="semibold", color="#1d3557")

    # Bottom caption
    ax.text(box_x + box_w / 2, 0.9, "Control preserves progress and enables recovery.",
            ha="center", va="center", fontsize=9, fontstyle="italic", color="#495057")

    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_p / "fig_conceptual_architecture.png", bbox_inches="tight")
    fig.savefig(out_p / "fig_conceptual_architecture.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated Conceptual Architecture Diagram in {out_p}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    generate_conceptual_architecture(base / "figures" / "architecture")
    generate_conceptual_architecture(base / "paper" / "figures")
