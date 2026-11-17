# Candidate Gap Matrix

**Status:** Candidate questions only. Source passages are verified as content in the supplied review/workspace, not as independently confirmed findings from cited originals. G1–G5 and their provisional ranking are preserved from `research_workspace.pdf`; no gap is finalized or claimed novel.

| ID | Candidate gap and source evidence | Candidate question / comparison | Outcomes proposed in workspace | Main threats and verification still needed |
|---|---|---|---|---|
| G1 | Event-triggered goal re-anchoring. Review discussion of goal drift and state serialization: literature review §§3.4, 4.2, 6.1; workspace p. 6, §5.1. Refs [2], [8], [16]. | At matched budget, does an observable drift trigger improve completion relative to fixed-interval re-anchoring? Arms: none, fixed interval, event triggered. | Completion by horizon, constraint violations, redundant actions, re-anchor count, tokens, wall time, failure traces, uncertainty intervals. | Prevent oracle leakage; equalize trigger/tool budget; control horizon/difficulty. Verify AdaCoM [16] and harness [8] for equivalent comparisons. |
| G2 | Recovery-aware subtask decomposition. Review §3.5 describes the proposed no-recovery bottleneck; §6.3 discusses rollbacks. Workspace pp. 6–7, §5.2. Refs [10], [14], [5]. | How does diagnostic-state preservation change error localization and recovery? Arms: isolated subtasks, summary handoff, structured checkpoint + rollback under controlled faults. | Recovery success, localization accuracy, final completion, extra steps, execution overhead, trace failure categories. | Make faults realistic and not trivially detectable; match token/tool budget; synthetic tasks may not generalize. Verify LEAD [10], LATS [13–14], ScienceFlow [5] interfaces/ablations. |
| G3 | Context fidelity versus reliability. Review §3.3 covers context pathologies; §4.2 adaptive management/state retention. Workspace p. 7, §5.3. Refs [7], [8], [16]. | Does structured retention of task-critical state preserve planning quality better than generic summaries or truncation? Compare full history, truncation, generic summary, structured state under a common model/task and token budget where feasible. | Completion, state-retention probes, constraint violations, missed dependencies, tokens/cost by horizon. | Summary quality varies; full history may exceed budget; recall is not identical to planning. Verify AdaCoM [16] and Goal2Skill [8] comparisons. |
| G4 | Intermediate deterministic verification. Review §4.4 proposes cheap verification; §6.2 discusses sparse outcome feedback. Workspace p. 7, §5.4. Refs [7], [8]. | Is milestone verification a better completion/overhead trade-off than final-only or every-step checks? | First-error detection latency, propagated errors, completion, tool overhead, cost, false alarms. | Milestones may leak privileged knowledge; checks cost resources and may miss semantic errors. Verify whether source papers or later work compare schedules. |
| G5 | Reversible versus greedy experimental commitment. Review §5.2 discusses commit-or-discard, risk aversion, and anchoring; §4.1 covers lookahead/search. Workspace pp. 7–8, §5.5. Refs [1], [11–14]. | At equal experiment budget, can reversible branches escape plateaus more effectively than greedy commitment? Compare greedy commit/discard, bounded temporary regression, and checkpoint branching on delayed-reward tasks. | Final objective, exploration diversity, plateau frequency, recovery after poor choices, trials, compute. | Reward landscape must not favor branching; equalize search capacity; synthetic tasks may not transfer. Verify behavioral case study [11] and Flare/LATS comparisons. |

## Provisional prioritization (not a decision)

Workspace p. 8, §7 ranks **G2 first**, **G4 second**, and **G1 third**, under an explicit assumption of limited compute and a lightweight harness. It labels this qualitative, not measured; actual hardware/API access is UNKNOWN. G3 remains an alternative if context tooling is available. G5 needs carefully designed delayed-reward tasks and strict budget matching. Ranking may change after primary-source and feasibility audits.

## Cross-cutting unresolved checks

- Inspect original papers and released artifacts before attributing limitations or asserting novelty.
- Define each metric operationally, including numerator, denominator, and correctness criteria.
- Confirm equivalent resource budgets and prevent leakage/oracle signals.

## Phase C update — source-verified overlap (2026-11-04)

The original candidate IDs and Phase B provisional priority G2 > G4 > G1 are retained as historical workspace content. This is a reassessment, not a gap selection or novelty claim.

| ID | Current candidate and overlap | Possible distinction | Status / missing evidence |
|---|---|---|---|
| G2 | LEAD studies decomposition/lookahead recovery; ScienceFlow restores archived research states; AgentRewind evaluates aligned context/environment rollback; RIR combines rollback localization and retained reflection. | Diagnostic-state preservation vs summary handoff under matched injected faults/budgets may differ, but exact overlap is not exhaustively checked. | High overlap; novelty not established. Need artifacts, task licenses, fault model, side-effect boundaries, and resource constraints. |
| G4 | JevAct verifies selected tool actions; AgentCheck injects/replays tool faults; other work covers trace diagnosis and evidence/outcome verification. | Matched final-only vs milestone vs every-step deterministic checks, measuring first-error detection and downstream propagation. | Plausible distinction, not novelty. Need non-oracle checks, fault injection, propagation definition, overhead, and artifact/protocol audit. |
| G1 | ScienceFlow ESTRA selects live/archive anchors and continue/redirect; AdaCoM discusses periodic/context-threshold invocation; goal-drift steering and RIR address adaptive intervention. | Fixed-interval vs event-triggered cadence with same anchor policy and matched intervention budget. | High conceptual overlap; exact cadence comparison unresolved. Check triggers, frequency controls, and cost matching in originals. |

### Candidate formulas for G2 (proposals only; not frozen)

Let an eligible fault episode be one deliberately injected, independently logged execution fault with known source/location. Let task completion mean passing an external deterministic acceptance test within the assigned total budget. Multiple simultaneous faults must be grouped by a predeclared rule.

- **Task completion rate:** `tasks passing acceptance test within budget / tasks started`.
- **Recovery success rate:** `fault episodes followed by acceptance-test-passing completion within recovery budget / eligible fault episodes`.
- **Error localization, strict exact match:** predicted location set must exactly equal ground-truth location set; `exact-set matches / episodes requiring localization`. Partial localization receives no credit in this strict score; optionally report separately named micro precision/recall/F1 with multiple-label handling fixed before evaluation.
- **Recovery steps:** agent/tool actions from first fault observation to verified restored state or terminal failure. Report distribution across all episodes and recovered-only values separately to avoid survivor bias.
- **Failed attempts:** `recovery attempts that exhaust per-attempt budget without verified recovery / recovery attempts begun`; also report attempts per episode.
- **Execution overhead:** for resource X (tool calls, tokens, or wall time), report paired absolute difference `mean(X_recovery - X_control)` and relative difference `100 × (mean(X_recovery)-mean(X_control))/mean(X_control)`. Define zero-denominator handling; report checkpoint storage/restore time and bytes separately.
- **Token/API cost if applicable:** sum actual input/output tokens per task, stratified by model. Monetary cost is the sum of provider-recorded charges under a dated rate schedule; do not infer price from tokens.

These are candidate operational definitions. Fault units, partial-credit rule, pairing and budget boundaries need approval in Phase D.

## Phase D update — selected G4 direction and refined distinction (2026-11-04)

G4 is selected by the researcher as the direction for Phase D. This records the user's explicit direction choice; it does not approve the exact question, task environment, metrics, budget, or protocol.

| Primary source | New overlap evidence | Refined G4 boundary |
|---|---|---|
| Agentic Robot, arXiv:2505.23450v2, §3.4 | Directly compares fixed 10/20/50-step verification; reports LIBERO-Long success sensitivity and runtime cost. Its verifier is visual, and it does not compare dependency milestones under equal call slots or inject controlled faults. | The frequency-vs-performance trade-off is already studied. Candidate extension: deterministic dependency-boundary placement vs periodic placement with equal call slots, shared assertions, controlled injected faults, and taint propagation outcomes. |
| VReAct, arXiv:2609.31937v3, §§3–5, 7–8 | Defines unit/integration/acceptance layers and integration checks for dependency composition; pilot only evaluates unit and acceptance checks and identifies integration as omitted. | Dependency/integration verification itself is not new. A schedule comparison for integration gates with controlled fault propagation would be an empirical extension; verify exact overlap more broadly. |
| MAS-ProVe, arXiv:2602.03053, §§3–6 | Empirically compares learned process-verifier paradigms and agent-/iteration-level granularity across six multi-agent frameworks; reports inconsistent benefits and high variance. | Process-level verification itself is not new; MAS-ProVe is not deterministic assertion checking or the candidate fault/schedule design. |
| JevAct, arXiv:2610.38620, §§3–5 | Runtime gates selected tool actions and bounded repairs. | Adjacent action-level gate, not equal-call scheduling comparison. |

The prior G4 wording is therefore narrowed but **not finalized as a novel gap**. Strongest overlap threat: Agentic Robot already studies periodic frequency and task success/runtime; VReAct explicitly anticipates integration verification. A defensible study would need to clearly position itself as a controlled, deterministic, call-budget-matched schedule comparison and avoid agent-reliability claims unless an LLM executor is actually evaluated.
- Resolve whether any candidate can be tested with legally accessible tasks and available compute.
