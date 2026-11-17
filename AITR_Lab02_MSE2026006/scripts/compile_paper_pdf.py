"""Compile academic research paper into PDF format using ReportLab."""

import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas for two-pass page numbering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#444444"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Verification Scheduling in Long-Horizon Agent Workflows — Research Paper")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "Harsh Sharma (IIIT Allahabad)")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "Postgraduate Research Assignment Submission — IIIT Allahabad")
        self.setStrokeColor(colors.HexColor("#cccccc"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()


def clean_latex(text: str) -> str:
    """Clean LaTeX markup for ReportLab Paragraph rendering."""
    # First handle math mode by replacing with plain text or simple italic
    text = re.sub(r'\\mathcal\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathbf\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathit\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\quad', r' ', text)
    text = re.sub(r'\\ge', r'>=', text)
    text = re.sub(r'\\le', r'<=', text)
    text = re.sub(r'\\neq', r'!=', text)
    text = re.sub(r'\\approx', r'~', text)
    text = re.sub(r'\\in', r'in', text)
    text = re.sub(r'\\forall', r'for all', text)
    text = re.sub(r'\\to', r'->', text)
    text = re.sub(r'\\pm', r'±', text)
    text = re.sub(r'\\times', r'x', text)
    text = re.sub(r'\\mu', r'μ', text)
    text = re.sub(r'\\Delta', r'Δ', text)
    text = re.sub(r'\\theta', r'θ', text)
    text = re.sub(r'\\pi', r'π', text)
    text = re.sub(r'\\lceil\s*', r'[', text)
    text = re.sub(r'\\rceil\s*', r']', text)
    text = re.sub(r'\\lfloor\s*', r'[', text)
    text = re.sub(r'\\rfloor\s*', r']', text)
    text = re.sub(r'\\cap', r'∩', text)
    text = re.sub(r'\\cup', r'∪', text)
    text = re.sub(r'\\subseteq', r'⊆', text)
    text = re.sub(r'\\circ', r'o', text)

    # Strip math delimiters
    text = re.sub(r'\$([^$]+)\$', r'<i>\1</i>', text)
    text = re.sub(r'\\\[([^\]]+)\\\]', r'\1', text)
    text = re.sub(r'\\\(', r'', text)
    text = re.sub(r'\\\)', r'', text)

    # Clean macros
    text = re.sub(r'\\cite[pt]?\{([^}]+)\}', r'[\1]', text)
    text = re.sub(r'\\ref\{([^}]+)\}', r'[\1]', text)
    text = re.sub(r'\\label\{([^}]+)\}', r'', text)
    text = re.sub(r'\\textbf\{([^}]+)\}', r'<b>\1</b>', text)
    text = re.sub(r'\\emph\{([^}]+)\}', r'<i>\1</i>', text)
    text = re.sub(r'\\texttt\{([^}]+)\}', r'<font face="Courier">\1</font>', text)
    text = re.sub(r'\\section\*?\{([^}]+)\}', r'', text)
    text = re.sub(r'\\subsection\*?\{([^}]+)\}', r'', text)
    text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'', text)
    text = re.sub(r'\\paragraph\{([^}]+)\}', r'<b>\1</b>', text)
    text = re.sub(r'\\begin\{[^}]+\}', r'', text)
    text = re.sub(r'\\end\{[^}]+\}', r'', text)
    text = re.sub(r'\\item\s*', r'&bull; ', text)
    text = text.replace('---', '—').replace('--', '–').replace('``', '"').replace("''", '"')
    text = text.replace(r'\%', '%').replace(r'\&', '&amp;').replace(r'\_', '_').replace(r'\{', '{').replace(r'\}', '}')

    # Fix any illegal tag interleaving like <b>...<i>...</b>...</i>
    # Simply remove nested tags if malformed
    text = re.sub(r'<([bi])>([^<]*)<([bi])>([^<]*)</\1>([^<]*)</\3>', r'<\1>\2<\3>\4</\3>\5</\1>', text)

    return text.strip()


def build_pdf():
    pdf_path = Path("paper/paper_compiled_preview.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#111111"),
        spaceAfter=10
    )
    author_style = ParagraphStyle(
        "DocAuthor",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceAfter=14
    )
    abstract_style = ParagraphStyle(
        "DocAbstract",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        leftIndent=24,
        rightIndent=24,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        "DocH1",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#002244"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#113355"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
        alignment=4,  # Justified
        spaceAfter=6
    )
    caption_style = ParagraphStyle(
        "DocCaption",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#444444"),
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    # Title & Metadata
    title = "Verification Scheduling in Long-Horizon Agent Workflows:<br/>A Controlled Study of Error Detection, Propagation and Computational Overhead"
    story.append(Paragraph(title, title_style))
    author_text = "<b>Harsh Sharma</b><br/>Department of Information Technology, Indian Institute of Information Technology (IIIT), Allahabad<br/>Prayagraj, Uttar Pradesh, India &nbsp;|&nbsp; <i>harsh.sharma@iiita.ac.in</i>"
    story.append(Paragraph(author_text, author_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#002244"), spaceAfter=12))

    # Abstract
    with open("paper/sections/01_abstract.tex", "r", encoding="utf-8") as f:
        abs_text = clean_latex(f.read().replace(r"\begin{abstract}", "").replace(r"\end{abstract}", ""))
    story.append(Paragraph("<b>Abstract</b>—" + abs_text, abstract_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaaaaa"), spaceAfter=14))

    # Sections to process
    sections = [
        ("02_introduction.tex", "1. Introduction"),
        ("03_related_work.tex", "2. Related Work"),
        ("04_problem_formulation.tex", "3. Problem Formulation & Research Questions"),
        ("05_methodology.tex", "4. Methodology"),
        ("06_experimental_setup.tex", "5. Experimental Setup"),
        ("07_results.tex", "6. Experimental Results"),
        ("08_discussion.tex", "7. Discussion"),
        ("09_threats_to_validity.tex", "8. Threats to Validity"),
        ("10_limitations.tex", "9. Limitations"),
        ("11_conclusion.tex", "10. Conclusion & Future Work")
    ]

    for fname, sec_heading in sections:
        sec_path = Path("paper/sections") / fname
        if not sec_path.exists():
            continue
        with open(sec_path, "r", encoding="utf-8") as f:
            raw = f.read()

        # Split into paragraphs and headings
        lines = raw.split("\n\n")
        for para in lines:
            para = para.strip()
            if not para:
                continue

            # Heading checks
            if para.startswith(r"\section{"):
                story.append(Paragraph(sec_heading, h1_style))
                continue
            elif para.startswith(r"\subsection{"):
                sub_title = re.search(r'\\subsection\{([^}]+)\}', para).group(1)
                story.append(Paragraph(sub_title, h2_style))
                continue
            elif para.startswith(r"\subsubsection{"):
                sub_title = re.search(r'\\subsubsection\{([^}]+)\}', para).group(1)
                story.append(Paragraph(f"<b>{sub_title}</b>", h2_style))
                continue

            # Skip raw LaTeX table environments (we inject formatted ReportLab tables)
            if r"\begin{table" in para or r"\end{table" in para:
                continue
            if r"\begin{figure" in para or r"\end{figure" in para:
                continue

            cleaned = clean_latex(para)
            if cleaned:
                story.append(Paragraph(cleaned, body_style))

        # Inset Key Figures and Tables at natural points
        if "06_experimental_setup.tex" in fname:
            # Add Experimental Design Table
            t_data = [
                ["Factor", "Evaluated Parameter Levels"],
                ["Horizons (H)", "12, 24, 36 nodes"],
                ["Topological Motifs", "Fork-Join, Spine-Join, Hierarchical Reduction"],
                ["Graphs per Condition", "10 unique seeds × 3 motifs × 3 horizons = 90 graphs"],
                ["Scenarios per Graph", "1 Clean Control + 12 Fault Injections = 13 scenarios"],
                ["Experimental Arms", "Arm A (Final-Only), Arm B (Periodic), Arm C (Milestone), Arm D (Every-Step)"],
                ["Total Episodes", "90 graphs × 13 scenarios × 4 arms = 4,680 episodes"]
            ]
            t = Table(t_data, colWidths=[150, 350])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#002244")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ]))
            story.append(Spacer(1, 6))
            story.append(t)
            story.append(Paragraph("<b>Table 1:</b> Factorial Experimental Design Summary.", caption_style))
            story.append(Spacer(1, 8))

        elif "07_results.tex" in fname:
            # Add Main Results Table
            t_data2 = [
                ["Arm", "Alloc Slots", "Realized Calls", "Mean TCF", "FDC", "Delay (Steps)", "Completion"],
                ["Arm A: Final-Only", "1", "1.00", "1.0000 ± 0.00", "33.3%", "12.17", "38.5%"],
                ["Arm B: Periodic", "3", "2.74 ± 0.59", "0.8614 ± 0.29", "33.3%", "5.50", "38.5%"],
                ["Arm C: Milestone", "3", "2.74 ± 0.59", "0.9005 ± 0.25", "33.3%", "7.81", "38.5%"],
                ["Arm D: Every-Step", "H", "21.03 ± 11.08", "0.7236 ± 0.43", "33.3%", "2.50", "38.5%"]
            ]
            t2 = Table(t_data2, colWidths=[110, 60, 75, 95, 45, 65, 55])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#002244")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#eef4fc")),  # Highlight Arm B
            ]))
            story.append(Spacer(1, 6))
            story.append(t2)
            story.append(Paragraph("<b>Table 2:</b> Main Results across Verification Scheduling Conditions (N=4,680 episodes).", caption_style))
            story.append(Spacer(1, 8))

            # Embed Figure 5 (Paired contrast distribution)
            fig5_p = Path("paper/figures/fig5_paired_contrast_distribution.png")
            if fig5_p.exists():
                story.append(Image(str(fig5_p), width=5.8 * inch, height=3.2 * inch))
                story.append(Paragraph("<b>Figure 1:</b> Distribution of paired cluster differences (TCF_C - TCF_B) across N=90 graph clusters. Mean difference = +0.0391 (p < 0.0001, 95% bootstrap CI [+0.0366, +0.0414]).", caption_style))
                story.append(Spacer(1, 8))

            # Embed Figure 3 (Pareto overhead vs propagation)
            fig3_p = Path("paper/figures/fig3_tradeoff_overhead_vs_propagation.png")
            if fig3_p.exists():
                story.append(Image(str(fig3_p), width=5.8 * inch, height=3.2 * inch))
                story.append(Paragraph("<b>Figure 2:</b> Pareto frontier: Realized Verification Calls vs. Downstream TCF. Arm B strictly dominates Arm C on the K=2.74 budget parity line.", caption_style))
                story.append(Spacer(1, 8))

            # Embed Figure 1 (Horizon Sensitivity)
            fig1_p = Path("paper/figures/fig1_tcf_by_horizon.png")
            if fig1_p.exists():
                story.append(Image(str(fig1_p), width=5.8 * inch, height=3.2 * inch))
                story.append(Paragraph("<b>Figure 3:</b> Downstream Error Propagation (TCF) by Task Horizon level (H=12, 24, 36).", caption_style))
                story.append(Spacer(1, 8))

    # Bibliography Section
    story.append(Paragraph("References", h1_style))
    bib_entries = [
        "[afoud2026vreact] A. Afoud and J. J. Wu, 'VReAct: Verification as an Architectural Layer for LLM Agents: A V-Model Design, and a Pilot Study of Its Deterministic Core,' arXiv:2609.31937, 2026.",
        "[chen2026horizon] M. Chen, L. Wang, and B. Qu, 'The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents,' arXiv:2608.06663, 2026.",
        "[pushkin2026lead] D. Pushkin and E. Abbe, 'LEAD: Breaking the No-Recovery Bottleneck in Long-Horizon Reasoning,' arXiv:2603.06870, 2026.",
        "[shinn2023reflexion] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, 'Reflexion: Language Agents with Verbal Reinforcement Learning,' in NeurIPS, 2023.",
        "[shoham2026jevact] I. Shoham et al., 'JevAct: Think Before You Act: Decision Gate for LLM Agents,' arXiv:2610.38620, 2026.",
        "[sinha2025illusion] A. Sinha, A. Arun, S. Goel, S. Staab, and J. Geiping, 'The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs,' arXiv:2509.09677, 2025.",
        "[venkataramani2026masprove] V. Venkataramani et al., 'MAS-ProVe: Understanding the Process Verification of Multi-Agent Systems,' in ICML, arXiv:2602.03053, 2026.",
        "[wang2026reasoning] Z. Wang, F. Wu, H. Wang, et al., 'Why Reasoning Fails to Plan: A Planning-Centric Analysis of Long-Horizon Decision Making in LLM Agents,' arXiv:2601.22311, 2026.",
        "[yang2025agenticrobot] Z. Yang et al., 'Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents,' arXiv:2505.23450, 2025.",
        "[yao2023tot] S. Yao, D. Yu, J. Zhao, et al., 'Tree of Thoughts: Deliberate Problem Solving with Large Language Models,' in NeurIPS, 2023.",
        "[yi2026adacom] L. Yi, R. Lei, L. Yao, et al., 'Learning Agent-Compatible Context Management for Long-Horizon Tasks,' arXiv:2605.30785, 2026.",
        "[yu2026rir] Y. Yu et al., 'Rollback the World, Keep the Reflection,' arXiv:2609.18304, 2026.",
        "[zhao2026scienceflow] M. Zhao, J. Dong, K. Xu, et al., 'ScienceFlow: A Long-Horizon Agent for ML Research, Scientific Discovery and Beyond,' arXiv:2608.14354, 2026.",
        "[zhou2024lats] A. Zhou, K. Yan, M. Shlapentokh-Rothman, et al., 'Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models,' in ICML, 2024.",
        "[zhuang2026agentrewind] Y. Zhuang et al., 'AgentRewind: Recoverable Execution for Long-Horizon LLM Agents,' arXiv:2608.14380, 2026."
    ]

    for bib in bib_entries:
        story.append(Paragraph(bib, ParagraphStyle("Bib", parent=body_style, fontSize=8.5, leading=12, leftIndent=18, firstLineIndent=-18, spaceAfter=4)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Compiled PDF successfully generated at {pdf_path} ({pdf_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_pdf()
