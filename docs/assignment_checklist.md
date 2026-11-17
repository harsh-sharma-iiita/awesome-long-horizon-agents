# Assignment Checklist

Requirements below are transcribed from `source_docs/assignment_instructions.pdf`. They are not claims of completion. Each gate has a stated advance criterion.

## Learning outcomes and research standard

- [ ] Link the implementation study to prior-review findings and verify them in original sources.
- [ ] Formulate a focused research question, hypotheses where appropriate, and measurable success criteria.
- [ ] Use AI assistance to specify, generate, read, run, test, debug, and improve code while retaining human understanding and verification.
- [ ] Reproduce or validate a trusted baseline before attributing benefits to a change.
- [ ] Compare methods fairly, prevent data leakage, and critically analyze actual results.
- [ ] Write an evidence-grounded implementation paper with LaTeX/Overleaf and reproducible figures.
- [ ] Document human–AI collaboration and explain technical decisions without treating AI output as authority.
- [ ] Produce working, tested code; screenshots or interfaces alone do not satisfy execution.
- [ ] Include two appropriate baselines/comparators where feasible, or justify an equivalently rigorous design.
- [ ] Complete at least one deeper analysis: ablation, errors/failures, robustness, sensitivity, or resource efficiency.
- [ ] Record data protocol, environment, parameters, seeds, and commands needed to regenerate key results.

Source: assignment instructions, pp. 1–2.

## Approved contribution pathways

- [ ] **A. Reproduction + extension:** validated baseline, extension comparison, explanation of discrepancies.
- [ ] **B. Controlled comparative study:** fair controls, consistent metrics, informative failure/trade-off analysis.
- [ ] **C. Targeted modification:** preserve baseline, isolate one justified change, evaluate with ablation or controlled test.
- [ ] **D. Hybrid/prototype + evaluation:** motivated design, measurable outcomes, baselines, rigorous evaluation.

No pathway has been selected. Source: p. 2.

## Approval gates

### G1 — Research brief

- [ ] Submit a one-page gap/problem brief.
- [ ] Include original supporting papers, a narrow research question, study pathway, and compute/data feasibility.
- [ ] Verify 3–5 original references from the review as requested by the brief template.
- [ ] Advance only when the question is narrow, literature-supported, and experimentally testable.

### G2 — Baseline verification

- [ ] Identify an accessible dataset/measurement source and test the environment.
- [ ] Run a baseline and preserve actual measured output.
- [ ] Submit a validation report showing baseline behavior and protocol were checked, not merely executed.

### G3 — Experimental evidence

- [ ] Freeze the comparison protocol.
- [ ] Preserve genuine outputs/logs and produce result tables and plots.
- [ ] Complete one deeper analysis.
- [ ] Ensure every claim is traceable to genuine runs and fair evaluation.

### G4 — Paper and reproducibility

- [ ] Submit paper PDF and LaTeX source.
- [ ] Prepare the GitHub repository and AI audit.
- [ ] Prepare a five-minute demonstration.
- [ ] Ensure methods, outputs, and provenance can be inspected and defended.

Gate source and advance criteria: p. 3. Pacing, official deadlines, group policy, submission location: Google Classroom (p. 3).

## AI Prompt Studio — all 18 prompts

Use in sequence as working scaffolds; verify outputs and save useful artifacts in the repository. “Save” items are required outputs named by the prompts, not claims that they exist. Source: pp. 3–9.

1. **Set up an accountable research workspace** — save workspace, decision log, and review scope. (p. 5)
2. **Extract evidence-based research gaps** — save gap matrix with source evidence, candidate questions, and possible experiments. (p. 5)
3. **Map literature to an executable experiment** — save bridge from original papers/methods to baseline and planned test. (p. 5)
4. **Check feasibility, novelty, and resource access** — save novelty/feasibility matrix and go/no-go assessment; novelty requires separate verification. (pp. 5–6)
5. **Frame research questions and success criteria** — save one-page problem brief with measurable outcomes. (p. 6)
6. **Verify datasets and comparators** — save dataset/baseline validation sheet with source, access, license, protocol, leakage risks, and independent checks. (p. 6)
7. **Freeze an experiment blueprint before viewing results** — save protocol, architecture/flowchart, deep-analysis plan, and pre-experiment checklist. (p. 6)
8. **Configure and test the coding environment** — save environment verification log and repository structure; inspect actual test output. (p. 6)
9. **Vibe-code one baseline module at a time** — save working baseline, code understanding, and prompt-to-code log; use short cycles and genuine execution output. (p. 7)
10. **Verify and reproduce the baseline** — save baseline reproduction/validation report and discrepancies. (p. 7)
11. **Debug using actual evidence** — save corrected code, tested fix, and genuine debugging decision. (p. 7)
12. **Choose and evaluate a defensible contribution** — save approved contribution pathway and executable comparison plan. (p. 7)
13. **Evaluate using real outputs only** — save metrics script, actual result CSV, tables, and research figures. (p. 8)
14. **Interpret outcomes, including negative results** — save evidence-based Results/Discussion outline and limitations. (p. 8)
15. **Draft an evidence-grounded LaTeX manuscript** — save manuscript, figures, `.tex`, and verified `.bib`; target 6–10 pages excluding references unless instructor specifies a template. (p. 8)
16. **Conduct a demanding technical peer review** — save prioritized peer-review report, revision checklist, and author-response table. (p. 8)
17. **Prepare reproducible GitHub documentation** — save repository README and reproduction instructions; mark unexecuted commands `[TEST REQUIRED]`. (pp. 8–9)
18. **Audit human–AI collaboration** — save AI provenance report and reflection from authentic prompts, diffs, errors, and evidence; report fewer than three real examples honestly if applicable. (p. 9)

## Minimum experimental evidence package

- [ ] Traceable link from prior review to verified gap and narrow experimental question.
- [ ] Legally accessible dataset/measurement source with appropriate handling and protocol.
- [ ] Executable baseline implementation and documented validation/reproduction check.
- [ ] At least two relevant methods/controls where appropriate, or justified equivalent design.
- [ ] Predefined metrics, consistent comparison conditions, and actual code-generated results.
- [ ] At least one deeper evaluation: ablation, robustness, sensitivity, error/failure analysis, or efficiency.
- [ ] Methodological limitations, negative findings, and unresolved issues reported.
- [ ] Code/instructions sufficient to rerun the central experiment, subject to resource constraints.

Non-ML studies should use rigorous domain-appropriate measurements rather than an artificial accuracy metric. Source: p. 9.

## Final submission package

- [ ] **Research paper:** final PDF, LaTeX source, bibliography, figures. Recommended 6–10 pages excluding references, subject to instructor template.
- [ ] **GitHub repository:** source/notebooks, README, dependency versions, configs, reproducible commands, dataset acquisition instructions, evaluation scripts.
- [ ] **Experimental evidence:** actual CSV/logs, evaluation outputs, comparison tables/figures, seeds, and test conditions.
- [ ] **Research provenance:** one-page gap/decision brief, baseline validation report, concise AI prompt/code/verification log.
- [ ] **Demonstration:** five-minute code/results walkthrough and readiness for technical viva or component rerun.
- [ ] Confirm final deadline, mode, group policy, and submission location from Google Classroom.

Source: pp. 9–10. Assignment suggests a folder name containing enrollment number or approved group ID; follow root project instructions for privacy and repository visibility.

## Repository requirements

- [ ] Include README, verified requirements, configs, data access guide (not restricted raw data), notebooks, reusable source, scripts, genuine results, paper materials, decision record, baseline validation report, and AI assistance log.
- [ ] Include genuine commands/dependencies; use realistic paths and expose no secrets, private data, or restricted model weights.
- [ ] Record dataset access/license, limitations, compute requirements, credits, and license where applicable.
- [ ] Include a minimum reproduction checklist for a second student.

Source: pp. 9–10.

## Responsible AI and research integrity

- [ ] Disclose AI support for ideation, literature synthesis, coding, debugging, analysis, visualization, and writing; follow institute/venue rules.
- [ ] Verify important sources, datasets, code/weight access, and citations from primary sources. An AI-generated link is not proof.
- [ ] Understand, test, trace, and own submitted code; explain modules, data flow, and experimental choices.
- [ ] Never fabricate results, p-values, figures, logs, bibliography entries, peer reviews, or debugging experiences.
- [ ] Avoid test-set tuning, leakage, cherry-picking, and undisclosed unequal comparisons.
- [ ] Respect licenses, terms, ethics, privacy, and participant protections; never commit API keys or restricted data.
- [ ] Interpret similarity checks responsibly; cite reused text, ideas, and code.
- [ ] Report limitations and compute constraints; keep claims proportional to evidence.

Source: p. 10.

## Gate 1 brief fields

- [ ] Review topic and 3–5 original references verified from the review.
- [ ] Specific gap with source evidence.
- [ ] One primary research question (optional supporting questions).
- [ ] Study pathway.
- [ ] Dataset/measurement setup, official source, access/license, planned partitions/protocol.
- [ ] Verified baseline/comparators and code/model availability.
- [ ] Primary metric and controlled variables.
- [ ] Compute, risks, bottlenecks, and fallback.
- [ ] First executable milestone completed or planned.

Source: p. 11.

## Student final self-check

- [ ] Question follows from prior review with original-source evidence; gap/novelty claims verified or qualified.
- [ ] Dataset, license, and protocol recorded; baseline runs, correctness checked, baseline preserved.
- [ ] Design answers the question; each figure/metric/result traces to real code output.
- [ ] At least one deeper experiment or error analysis complete; limitations reported.
- [ ] Manuscript separates prior work, project changes, and experimentally supported findings.
- [ ] Repository has genuine commands, dependencies, configs, and no exposed secrets.
- [ ] Prompt log and technical decisions are authentic, explainable, and demonstrable.

Source: p. 11.
