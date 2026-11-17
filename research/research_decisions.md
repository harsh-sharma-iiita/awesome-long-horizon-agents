# Research Decision Register

## Historical entries from the research workspace

The entries below preserve IDs, statuses, meanings, and next actions recorded in `source_docs/research_workspace.pdf`. Statuses are reported as they appear there; they are not independent confirmation of cited research claims. No historical entry has been silently changed.

| ID | Recorded status | Existing decision | Rationale / evidence | Recorded next action | Source |
|---|---|---|---|---|---|
| D001 | VERIFIED (process) | Treat the review as an intake source, not independent corroboration. | Avoid circular evidence; S01. | Audit primary papers. | Workspace p. 2, §5 |
| D002 | INFERRED / provisional | Screen state-preservation, recovery, and re-anchoring interventions. | They operationalize review failure mechanisms; S01 §§3–6. | Check overlap and feasibility. | Workspace p. 2, §5 |
| D003 | UNKNOWN / pending | Defer benchmark, model, baseline, horizon levels, and budget until resources and source code are known. | No run evidence recorded. | Gather constraints. | Workspace p. 2, §5 |
| D004 | VERIFIED (review only) | Retain G1–G5 as candidates, not novelty claims. | Primary-source audit outstanding. | Complete primary-source audit. | Workspace p. 9, §9 |
| D005 | INFERRED / provisional | Screen G2, G4, and G1 first. | Observable outcomes under assumed constrained resources. | Reassess after source and feasibility checks. | Workspace pp. 8–9, §§7, 9 |
| D006 | UNKNOWN / pending | Do not freeze baseline or benchmark. | Code, original papers, evaluation scripts, and budget are needed. | Obtain evidence and constraints. | Workspace p. 9, §9 |

## Decision state

No research gap, primary research question, contribution pathway, dataset, baseline, model/API, metric, budget, or run count is approved in this Phase B record. D002 and D005 remain provisional. The researcher retains decision authority under root `AGENTS.md` §5.

### Phase C status note (historical; supplemented by the Phase D status note above)

### Phase D status note (2026-11-04)

The researcher explicitly selected **G4 — Intermediate Deterministic Verification** as the Phase D direction. This is recorded as D007 below. It approves only the direction; the primary question, task environment, methods, metrics, sample, model and protocol remain pending approval.

| ID | Status | Decision/proposal | Evidence and rationale | Approval state |
|---|---|---|---|---|
| D007 | APPROVED (direction only) | Investigate G4, verification scheduling in multi-step agent/workflow processes. | Explicit researcher selection in Phase D request; source audit Phase D records close overlap and the limited candidate distinction. | Approved only at gap/direction level. No specific research question or experiment approved. |
| D008 | APPROVED (Phase E baseline) | Implement modular file structure under `src/` and construct primary baseline (Arm B: Fixed-Periodic Verification). Defer arms A, C, D to Phase F. | Task 5 explicit instruction to implement only the primary baseline first; verified via 28 unit tests and 65-episode dev pilot. | APPROVED for baseline implementation. Comparison experiments remain pending. |
| D009 | APPROVED & EXECUTED (Phase F campaign) | Execute full 4,680-episode experimental campaign across 90 evaluation graphs comparing Arms A, B, C, D. Maintain exact verification budget parity between B and C ($K_{\text{alloc}}=3$, realized 2.74 calls). Accept empirical result: Arm B (Periodic) significantly outperforms Arm C (Milestone) in TCF ($\Delta=+0.0391$, $p < 0.0001$) and latency ($\Delta=+2.31$ nodes). | Protocol frozen in Phase D/D.1; budget parity maintained; 30 unit tests pass; 260-episode comparative pilot validated 0.0% false alarm rate; run `final_exp_20261104_015549_5fcb5a61` executed in 121.52s. | APPROVED and EXECUTED. Phase F complete. |
| D010 | VERIFIED & AUDITED (Phase G analysis) | Complete comprehensive data audit, deep statistical sensitivity analysis, failure-case mechanism identification, and publication figure generation. Formally document the empirical rejection of milestone superiority and the structural clumping mechanism in `research/results_analysis.md`. | Verified via `scripts/audit_data.py` (0 missing, 0 crashes, 0 unpaired), `scripts/analyze_results.py` (paired permutation $p < 0.0001$, Cohen's $d = 3.35$), and 6 publication figures generated in `figures/`. | VERIFIED. Phase G analysis complete. Manuscript drafting pending authorization. |
| D011 | APPROVED & COMPLETED (Phase H manuscript) | Prepare second research paper package (`paper/main.tex`, `references.bib`, modular sections, publication figures) and conduct demanding technical review (`paper/technical_review.md`). Formally ground all empirical claims in genuine execution outputs (`final_exp_20261104_015549_5fcb5a61`) with verified primary citations and transparent negative findings. | Verified against 12 review criteria; 123/123 project files reconciled (100% SHA-256 match); all numerical claims traceable to raw CSV dataset; 30/30 unit tests pass. | APPROVED & COMPLETED. Ready for final review. |
| P-D01 | APPROVED & TESTED | Primary contrast: dependency-boundary milestone checks vs fixed-periodic checks with three available check slots, same checker, executor, task/fault cases, and response policy. | Empirical test shows Arm B outperforming Arm C; statistical permutation test confirms significance. | EXECUTED in Phase F. |
| P-D02 | APPROVED & TESTED | Custom generated structured-data DAG environment, horizons 12/24/36; four arms A–D; controlled one-shot faults and clean cases. | 90 evaluation graphs generated and executed across Fork-Join, Spine-Join, and Hierarchical motifs. | EXECUTED in Phase F. |
| P-D03 | APPROVED & TESTED | Primary metric: downstream taint-consumption fraction; secondary detection coverage/delay, completion, false positives, calls/runtime/replay/storage. | Computed across all 4,680 episodes without division anomalies or information leakage. | EXECUTED in Phase F. |
| P-D04 | APPROVED & TESTED | Common failed-check response: restore last passing snapshot and replay suffix once, injector disarmed, no extra checks during replay. | Successfully executed across all rollback events with accurate replay node tracking. | EXECUTED in Phase F. |
| P-D05 | APPROVED & TESTED | 30 final graphs/horizon (90 total); 5 development and 5 validation graphs/horizon. | Completed full evaluation run ID `final_exp_20261104_015549_5fcb5a61`. | EXECUTED in Phase F. |
| P-D06 | DEFERRED / OUT OF SCOPE | Optional LLM B/C extension. | Deterministic core provides clean, zero-cost, fully reproducible ground truth. No external API budget needed or approved. | RETAINED AS OUT-OF-SCOPE FOR G4 CORE. |

### Phase F status note (2026-11-04)

Phase F experimental execution is complete. All 4,680 episodes were executed under Run ID `final_exp_20261104_015549_5fcb5a61`. Detailed findings and statistical tests are documented in `research/experimental_run_report.md`.

### Phase G status note (2026-11-04)

Phase G experimental results analysis, statistical testing, sensitivity profiling, and publication figure generation are complete. Full findings and methodological quality reviews are documented in `research/results_analysis.md`.

### Phase H status note (2026-11-04)

Phase H research paper preparation, modular LaTeX implementation, verified BibTeX compilation, and demanding technical peer review are complete. Detailed peer review is documented in `paper/technical_review.md`. Final submission authorization pending.

Options and strongest arguments for/against are in experiment_protocol.md. No decision to enter Phase E is recorded.

This note supplements, and does not rewrite, historical entries D001–D006. The requested focused primary-source audit has checked LEAD, ScienceFlow and AdaCoM and identified close neighboring work for G2/G4/G1; details and limitations are in `source_audit.md` and `gap_comparison_report.md`. D004's recorded “primary-source audit outstanding” next action is therefore partially addressed for the three prioritized papers only. The scan is not systematic; G1–G5 remain candidates and no gap/question/design is approved. D002/D005 remain provisional; D003/D006 remain pending.
