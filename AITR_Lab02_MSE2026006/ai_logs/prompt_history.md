# Prompt History

## 2026-11-04 — Phase B source-document analysis

**User task:** Read root `AGENTS.md`, analyze all three supplied PDFs, preserve D001–D006, extract assignment requirements and the 18 prompts, establish current research status, update specified research documentation, identify inconsistencies, and stop before Phase C.

**AI action:** Extracted page text locally with PowerShell/Python; prepared source-linked summaries and documentation. No web search, implementation code, experiment, or new research decision.

## 2026-11-04 — Phase C original literature audit

**User task:** Verify LEAD, ScienceFlow and AdaCoM; investigate neighboring work and G2/G4/G1; assess G2 evaluation levels and candidate metrics; inspect constraints; update specified records; recommend without deciding; stop before Phase D.

**Actions:** Browsed original arXiv records and HTML papers; checked Apple MLR page for LEAD’s publication label and ScienceFlow project/code references; reviewed papers closest to rollback recovery, verification and drift. Recorded metadata, URLs, relevant sections, candidate comparisons, and constraints unknowns in project research files.

**Limits:** Targeted scan, not systematic; cannot establish novelty or absence of prior work. Reported metrics remain author-reported and were not reproduced. No code or experiments were run. No substantive human decision was recorded.

## 2026-11-04 — Phase D G4 design proposal

**User task:** Treat G4 as selected; verify named work including VReAct and MAS-ProVe; refine questions; propose comparison conditions, task/fault design, recovery policy, metrics, sample/statistics, deterministic vs LLM options, threats, feasibility and decision table; stop before Phase E.

**Actions:** Re-read parent/project AGENTS.md, Phase C outputs and constraints. Checked primary arXiv/OpenReview pages for VReAct, MAS-ProVe, Agentic Robot and JevAct. Drafted a controlled structured-data DAG proposal with matched available B/C call slots. Inspected current-session OS/Python/processor count; WMI hardware query was denied.

**Human decision:** Researcher selected G4 (direction only); no exact question, protocol, budget, model, sample or metrics were approved.

**Limits:** Targeted scan, not systematic. No runtime/cost measurement, code, dependency installation, baseline validation, or experiment. Current-session resources do not establish the target research machine.

## 2026-11-04 — Phase D.1 final experimental design review before implementation

**User task:** Perform final scientific consistency review of Phase D proposal across 8 areas (DAG topologies/milestones, primary metric/lineage, hypothesis/test consistency, fault coverage denominators, budget accounting, recovery policy, sample size arithmetic/feasibility, deterministic vs LLM boundaries). Produce `research/phase_d_final_review.md` with severity levels, corrections, remaining unknowns, final configuration, and human approval table. Stop before implementation.

**Actions:** Audited candidate protocol documents (`experiment_protocol.md`, `hypotheses_and_metrics.md`, `research_brief.md`, `feasibility_report.md`, `human_decisions.md`, `research_decisions.md`). Identified BLOCKER in DAG topology/milestone integration, MAJOR issues in metric denominator filtering, hypothesis-test consistency, recovery mechanics, and LLM scope. Created `research/phase_d_final_review.md` with detailed corrections and approval table.

**Human decision:** All design options pending explicit human approval.

**Limits:** No implementation code written; no dependencies installed; no experiments executed; protocol not frozen. G4 direction preserved.

## 2026-11-04 — Phase E environment configuration and baseline implementation

**User task:** Act as research software engineer for G4 project. Inspect approved research documents. Inspect environment with `scripts/check_environment.py`, save diagnostic in `reproducibility/environment.md`. Create virtual environment and pinned `requirements.txt`. Build modular architecture under `src/` (tasks, execution, verification, schedulers, evaluation, utils). Implement primary baseline (Fixed-Periodic Scheduler, Arm B), leaving remaining schedulers deferred. Implement 28-test verification suite across all components. Run baseline pilot on development graphs, save configurations, trajectories, and summary metrics. Document baseline validation report, execution commands, debugging log, and AI assistance log. Stop before Phase F.

**Actions:** Ran diagnostic script (measured 8-core CPU, 21.8GB RAM, Windows 11, Python 3.14.6, 0 GPU/API). Configured `.venv` with `numpy==2.5.4`, `scipy==1.18.1`, `networkx==3.7`, `pytest==9.2.0`. Implemented full modular architecture. Resolved reference integrity union check and type corruption non-list guard during debugging. All 28 tests passed. Ran baseline development pilot (65 episodes across 5 graphs in 0.392s). Produced `baseline_validation.md`, `environment.md`, `execution_commands.md`, `debugging_log.md`, `README.md`.

**Human decision:** Approved baseline implementation and file structure. Schedulers A, C, D deferred to Phase F.

**Limits:** Only primary baseline (Arm B) was executed. No comparison experiments or statistical claims across conditions were made. Phase F full experimental run is pending human approval.
