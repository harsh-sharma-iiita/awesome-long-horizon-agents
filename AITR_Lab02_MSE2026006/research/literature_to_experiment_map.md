# Literature-to-Experiment Map

**STATUS: PENDING — To be completed in the relevant research phase.**

The supplied review is the intake source. Its bibliography and method descriptions are not independently verified here. The workspace developed the candidate mappings below; none is an approved design.

| Review topic / method | Review location | Possible experimental connection in workspace | Verification required before design |
|---|---|---|---|
| Compounding error, self-conditioning, horizon length | Literature review §3.1, pp. 2–3 | Motivation for measuring outcomes across increasing task horizons; workspace frames task-level trajectory analysis (p. 2). | Verify cited mathematical/empirical claims and define horizon/task family. |
| Greedy policy myopia; search/lookahead (ToT, LATS, Flare) | §§3.2, 4.1, pp. 3–4 | G5 reversible versus greedy commitment (workspace pp. 7–8); possible comparator context for other questions. | Check algorithms, released code, costs, and whether Flare is accurately attributed. |
| Context pollution, adaptive context control, compression, re-anchoring (AdaCoM, Goal2Skill, CORP-GEN) | §§3.3–3.4, 4.2, pp. 3–4 | G1 event-triggered re-anchoring and G3 state-aware versus generic context retention (workspace pp. 6–7). | Verify methods, access, ablations, budgets, and overlap. |
| Subtask decomposition, state recovery, executable workspace (ScienceFlow, FARS) | §3.5, §4.3, pp. 3–4 | G2 recovery-aware decomposition and checkpoints (workspace pp. 6–7). | Inspect originals and recovery interfaces; check access and feasibility. |
| Reflection and cheap deterministic verification | §4.4, p. 4 | G4 schedule of final-only, every-step, or milestone checks (workspace p. 7). | Verify prior comparisons and define checks that do not expose oracle information. |
| Commit-or-discard hill-climbing, risk aversion, anchoring | §5.2, p. 5 | G5 greedy versus reversible experimental commitments (workspace pp. 7–8). | Verify original trace study, task assumptions, and fair budget. |
| Implementation/verification gaps in research benchmarks | §§2.3, 5.1, 5.3, pp. 2, 5 | Candidate evaluation setting; no benchmark is selected. | Verify benchmark datasets, metrics, scores, licenses, and comparability from primary sources. |

## Pathways for later comparison

The assignment permits reproduction + extension, controlled comparison, targeted modification, or hybrid/prototype evaluation (assignment instructions, p. 2). The workspace suggests checking tractability and overlap before selecting a pathway (workspace pp. 5–9). No pathway, method, dataset, baseline, metric, or experiment is selected in Phase B.

## Phase C: verified literature-to-experiment links (2026-11-04)

| Candidate | Closest primary methods checked | Overlap and possible contrast | Evidence not yet available |
|---|---|---|---|
| G2 recovery-aware decomposition | LEAD §§3–6; ScienceFlow §§2.3–2.4, 3.1.3; AgentRewind §§4–5; RIR §§4–5. | LEAD uses lookahead/overlapping rollouts on puzzles; ScienceFlow restores research states; AgentRewind aligns context/environment checkpoints; RIR couples rollback depth with retained reflection and adaptive review. Diagnostic-state vs summary-handoff comparison needs protocol-level comparison and a specific fault taxonomy. | Artifact access/reproduction; task suite/license; realistic fault model; side-effect boundaries; model/budget constraints; exact baseline/ablation equivalence. |
| G4 intermediate deterministic verification | JevAct §§3–5; AgentCheck (EMNLP 2026 demo); Agent-Trident (Findings EMNLP 2026); VeriHarness (arXiv:2610.00972). | JevAct gates selected actions with executable checks plus model judgments; AgentCheck injects/replays faults; trace work diagnoses errors; VeriHarness checks evidence/outcomes. Candidate contrast: compare schedules and propagation at matched check overhead. | Verify artifacts/protocols; no hidden answer state in checks; define meaningful fault propagation and task relevance. |
| G1 event-triggered re-anchoring | ScienceFlow §§2.3, 3.1.3; AdaCoM §§3–5 and inference-overhead discussion; Learning to Steer (arXiv:2610.22316); RIR §4.2. | Existing work re-anchors live/archive states, steers detected drift, or adapts intervention timing. Possible contrast: cadence (fixed vs event) while holding anchor policy and total intervention budget constant. | Establish original triggers, cost normalization and artifact feasibility for matched comparison. |

No benchmark, dataset, model, baseline, metric or protocol is selected. These are mappings for later decision, not implementation recommendations.

## Phase D G4 design mapping (2026-11-04)

| Source | What it contributes to design | What it does not establish for this proposal |
|---|---|---|
| Supplied review §4.4 p. 4; §6.2, §6.4 pp. 5–6 | Motivation for deterministic checks and earlier verification; review-content evidence only. | Independent validity of the review's claims or efficacy of a particular schedule. |
| Agentic Robot, arXiv:2505.23450v2 §3.4 and §4 | Direct prior periodic-frequency comparison (10/20/50 steps) with task success/runtime reports; establishes that cadence-vs-cost analysis exists. | Equal-call comparison of dependency-derived milestones vs periodic checks under controlled injected faults; its verifier is visual/embodied. |
| VReAct, arXiv:2609.31937v3 §§3–5, 7–8 | Verification levels include integration/dependency composition; pilot uses unit/acceptance only and identifies integration as untested. | Empirical comparison of fixed vs dependency-based schedule or controlled corrupted-state propagation. |
| MAS-ProVe, arXiv:2602.03053 §§3–6 | Process verification can be high variance and not consistently beneficial; supports measuring rather than assuming effectiveness. | Deterministic assertions, fault-injected DAGs or matched schedule timing. |
| JevAct, arXiv:2610.38620 §§3–5 | Executable action-state checks and bounded correction. | Schedule-level matched comparison over a long workflow. |

Candidate experimental mapping: generated DAG task and public contracts → same executor and deterministic checker → four schedules with B/C slot cap matched → independent evaluator tracks hidden fault lineage → metrics in hypotheses_and_metrics.md. This mapping is proposed and not an implementation plan approval.
