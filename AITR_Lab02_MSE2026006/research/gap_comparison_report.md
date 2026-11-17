# Gap Comparison Report — Phase C

**Status: comparative recommendation only. No gap, novelty claim, research question, metric, model, baseline, benchmark, budget, or protocol is approved.** Online sources accessed 2026-11-04 (Asia/Kolkata). See `source_audit.md` for URLs and section-level details. G1–G5 and historical priority are retained.

| Criterion | G2 | G4 | G1 |
|---|---|---|---|
| Literature support | Strong: LEAD decomposition/lookahead; ScienceFlow executable states; AgentRewind rollback; RIR rollback plus reflection. | Strong: review proposes checks; JevAct verifies tool actions; adjacent work studies fault replay and trace verification. | Strong: ScienceFlow ESTRA, AdaCoM, goal-drift steering and RIR. |
| Closest existing work | AgentRewind and RIR; also LEAD and ScienceFlow. | JevAct action checks; AgentCheck fault replay; VeriHarness evidence/outcome checks. | ScienceFlow matched re-anchoring; Learning to Steer; AdaCoM invocation discussion. |
| Candidate distinction | Diagnostic-state preservation vs summary handoff under matched faults/budgets; overlap uncertain. | Matched final-only vs milestone vs every-step checks measuring detection and propagation. | Fixed-interval vs event-triggered cadence under same anchor policy and intervention cost. |
| Implementation difficulty | Medium–high: snapshots, safe rollback, fault taxonomy, diagnostics; model interface if LLM. | Low–medium if inspectable task/checker exists; harder to avoid oracle milestones. | Medium: trigger signals, re-anchoring, budget matching and logging. |
| Compute requirements | Deterministic pilot may need little compute; LLM adds model/API costs. Unknown. | Likely CPU-capable for a small deterministic task; model need depends on question. Unknown. | Depends on model agent and repeated interventions. Unknown. |
| Evaluation difficulty | Ground-truth faults, external recovery checks, multi-fault rules and side effects. | Independent fault truth, check validity/false alarms, propagation and overhead. | Observable non-oracle trigger and matched state/cost. |
| Main risks | Direct overlap; deterministic-only overclaim; external effects persist after rollback; synthetic faults. | Oracle checks; semantic errors missed; deterministic environment may not generalize to LLM planning. | Existing overlap; trigger leakage; unmatched cost; noisy drift labels. |
| Overall feasibility | **Conditional/uncertain:** feasible mechanism, needs narrowing and resource facts. | **Provisionally highest** under a small CPU harness if meaningful non-oracle task exists. | **Conditional:** feasible controller, overlap and cost controls unresolved. |

## Evidence-based comparison

G2 has mechanistic motivation but strong overlap: AgentRewind evaluates context/environment rewind and recovery, RIR addresses timing, restore location and retained reflection, while LEAD and ScienceFlow cover related recovery/state mechanisms. It should not proceed unchanged without identifying what a diagnostic-state comparison adds.

G4 offers a controllable variable (verification schedule) and observable outcomes (detection time, propagation, completion, overhead). JevAct shows runtime verification is already active research; the possible distinction is schedule plus propagation. Feasibility requires checks that do not expose hidden answer state.

G1 is plausible but close to ScienceFlow’s matched re-anchoring and newer goal-drift steering. It must isolate cadence rather than repeat anchor/direction selection.

These are **INFERRED** judgments from checked methods and unknown constraints. They do not imply novelty. Candidate G2 formulas are in `gap_matrix.md`; none is approved.

## Recommendation boundary

See research_direction_recommendation.md. G4 was subsequently selected by the researcher for Phase D (D007, direction only); the specific question and design remain pending.

## Phase D addendum

Agentic Robot §3.4 already compares periodic verification intervals and reports task success/runtime, while VReAct proposes an integration verifier but its pilot does not evaluate that layer. MAS-ProVe studies model-based process verification, not deterministic schedule placement. The candidate must therefore be described as a possible controlled extension: equal available check slots, dependency-derived vs periodic placement, common assertions, and injected-fault propagation. No novelty conclusion follows.
