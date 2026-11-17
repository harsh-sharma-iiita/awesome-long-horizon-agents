# Research Paper Package

**Title:** Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead  
**Author:** Harsh Sharma (IIIT Allahabad)  
**Status:** LaTeX Source and Technical Review Complete.

## Contents
- `main.tex`: Master LaTeX document.
- `references.bib`: Verified BibTeX citations.
- `sections/`: Modular LaTeX section files (Abstract through Conclusion).
- `figures/`: Publication-quality figures (PNG and vector PDF).
- `technical_review.md`: Demanding technical peer review report.

## Compilation Instructions
The manuscript is formatted with standard LaTeX packages (`article`, `geometry`, `amsmath`, `graphicx`, `booktabs`, `natbib`, `hyperref`).

To compile with standard `pdflatex` or on Overleaf:
```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```
