# RESEARCH WORKSPACE & DECISION REGISTER
## Stage 01 | Review intake, governance and research planning
**Project:** Planning-Quality Degradation in Long-Horizon Autonomous Research Agents  
**Date:** 22 October 2026  
**Document status:** Living research record; no experimental results claimed  
**Source:** S01 — Overleaf_Final_Paper(4).pdf, uploaded review, 11 pages

---

## 1. Purpose and evidence contract
This workspace turns a completed literature review into an accountable implementation-based research project. It is not a manuscript, a reproduction report, or proof of novelty. Every proposed claim must be linked to a passage, primary publication, source file, executable artifact, or experiment output before being promoted into the final paper.

**VERIFIED:** Directly observed in the named source or output. A claim appearing in a review is verified only *as review content*, not as a fact independently established by the cited paper.  
**INFERRED:** Reasoned synthesis, design choice, or hypothesis that still requires testing.  
**UNKNOWN:** Missing evidence, unresolved methodological choice, or unverified external claim.

**Non-negotiable integrity rules**
- Never invent papers, datasets, repository URLs, executions, measurements or comparative results.
- Preserve failed and inconclusive experiments alongside successful ones.
- Record model version, prompts, seeds, task versions, code revision, costs and failures.
- Separate benchmark-reported scores from scores reproduced by this project.
- Do not describe a candidate gap as novel until a separate current-literature search is complete.

## 2. Review intake and scope
**VERIFIED (S01, §§2–6):** The review distinguishes long-horizon tasks (sequential causal decisions), long-context capacity (token processing) and long-term memory (persistent agent state). It discusses compounding errors and self-conditioning; local greedy policy myopia; context pollution and attention dilution; goal drift; and no-recovery after extreme subtask decomposition. It surveys Tree-of-Thoughts, Language Agent Tree Search, Flare, AdaCoM, progressive compression, persistent research workspaces and verification-driven feedback. It discusses AI Scientist, ScienceFlow and FARS, and benchmark results attributed to MLE-Bench, PaperBench, SciReplicate-Bench, CORE-Bench and ML-Dev-Bench.

**INFERRED:** Runtime controls that retain verifiable state, support recovery and restore goal alignment are experimentally tractable ways to study planning degradation without training a foundation model.

**UNKNOWN:** Which cited claims survive original-publication checks; which implementations are accessible; which benchmark is affordable; whether any intervention is genuinely underexplored.

## 3. Research problem boundaries
**Target phenomenon:** Deterioration in goal-aligned decision making across a sequence of dependent actions.  
**Potential unit of analysis:** One complete agent trajectory, with action-level annotations and task-level outcomes.  
**Do not conflate:** Longer context with longer task horizon; memory recall with correct planning; successful final output with valid intermediate reasoning; simulation success with end-to-end scientific discovery.

A useful controlled setting should vary the horizon while holding model, prompt policy, task family and execution budget as stable as practicable. Task difficulty and horizon may be correlated: this must be measured or disclosed rather than ignored.

## 4. Source register and provenance
| ID | Source / artifact | What is established | Verification still needed |
|---|---|---|---|
| S01 | Overleaf_Final_Paper(4).pdf | Uploaded review inspected, 11 pages | Original cited publications |
| S02 | Overleaf_Final_Paper(5).pdf | Second uploaded review, 11 pages | Whether substantive content differs |
| P01 | Original LEAD paper [10] | UNKNOWN | Obtain and inspect methods/limitations |
| P02 | Original ScienceFlow paper [5] | UNKNOWN | Obtain and inspect experiments/code |
| P03 | Original AdaCoM paper [16] | UNKNOWN | Obtain and inspect ablations/code |
| A01 | Research repository | UNKNOWN | Obtain URL/files and commit identifier |
| E01 | Baseline execution logs | UNKNOWN | Run and preserve logs, config and metrics |

## 5. Initial decisions
| ID | Status | Decision and rationale | Evidence | Next action |
|---|---|---|---|---|
| D001 | VERIFIED (process) | Treat review as intake source, not independent corroboration. Avoid circular evidence. | S01 | Audit primary papers |
| D002 | INFERRED / provisional | Screen state-preservation, recovery and re-anchoring interventions because they operationalize the review's failure mechanisms. | S01 §§3–6 | Check overlap and feasibility |
| D003 | UNKNOWN / pending | Defer benchmark, model, baseline, horizon levels and budget until resources and source code are known. | No run evidence | Gather constraints |

## 6. Evidence audit checklist
- Match every bibliography entry to its actual publication, authors, date and version.
- Inspect primary methods, experimental settings, author-stated limitations and released artifacts.
- Check reported benchmark denominators, metrics, model variants and budgets.
- Verify the review's numerical claims: 35-minute threshold, quadrupled failure probability, 25–30 tool calls, and benchmark scores.
- Audit the mathematical assumptions behind S(H) = p^H and nonstationary products; do not treat a heuristic model as a universal empirical law.
- Reconcile duplicate LATS entries [13], [14] and [17] after source inspection.
- Record negative evidence: unavailable code, non-reproducible setup and mismatched protocols.

## 7. Stage-gated execution plan
| Gate | Deliverable | Evidence required to advance |
|---|---|---|
| 1 — Gap identification | Claim/source matrix and candidate gaps | Review passages + primary-source audit |
| 2 — Literature-to-experiment | Falsifiable questions and comparator designs | Explicit controls, outcomes, confounds |
| 3 — Feasibility | Resource/time budget and task choice | Hardware/API access and pilot estimate |
| 4 — Verified baseline | Reproducible reference run | Code revision, config, logs and score |
| 5 — Implementation | Intervention and unit tests | Diff, tests and failure handling |
| 6 — Evaluation | Paired trials and ablations | Raw trajectories, metrics and uncertainty |
| 7 — Manuscript | Evidence-backed claims | Figure/data provenance and limitations |
| 8 — Reproducibility | Portable artifact package | README, environment, seeds and scripts |

## 8. Proposed project directory
```text
research_project/
  research_decisions.md
  gap_matrix.md
  sources/README.md
  protocols/experiment_protocol.md
  configs/
  src/
  tests/
  data/README.md
  runs/
  analysis/
  figures/
  manuscript/
  reproducibility/README.md
```
Keep credentials and private datasets out of version control. Store checksums or access instructions when source data cannot be redistributed.

## 9. Open questions / evidence requests
**UNKNOWN:** Available CPU/GPU, RAM, storage, API budget, timeline, permitted models and target venue.  
**UNKNOWN:** Whether the user has a pre-existing repository or reproducible baseline.  
**REQUEST:** Original PDFs or source repositories for LEAD [10], ScienceFlow [5] and AdaCoM [16]; available compute and model access; any existing code.  
**NEXT:** Complete primary-source audit, then choose one gap and freeze a preregistered pilot protocol.

## 10. Change log
| Date | Entry |
|---|---|
| 2026-10-22 | Stage 1 review intake and decisions D001–D003 recorded |
| 2026-10-22 | Expanded into portable, evidence-labeled workspace; no new empirical findings added |
