# Research Direction Recommendation — Phase C

**Status: PROVISIONAL RECOMMENDATION FOR REVIEW. Not a research decision.** No direction, question, model, baseline, metric, dataset, budget or protocol is finalized. Historical D001–D006 and G1–G5 remain unchanged.

## Recommended primary gap

**G4 — Intermediate deterministic verification**, narrowly as a comparison of verification schedules and downstream error propagation in a small inspectable environment.

### Candidate research question (not finalized)

“How do final-only, milestone-based, and every-step deterministic verification schedules compare in first-error detection, downstream error propagation, task completion, and verification overhead under matched execution conditions?” This is not approved and needs exact overlap review.

## Recommended backup gap

**G1 — Event-triggered goal re-anchoring**, only if separated from ScienceFlow ESTRA and goal-drift steering by comparing cadence under fixed anchor/action policy and matched intervention budget.

G2 is not recommended unchanged as primary because AgentRewind and RIR directly study rollback recovery and retained information, while LEAD/ScienceFlow cover related recovery/state mechanisms. Reconsider narrower G2 after protocol-level review.

## Supporting sources and evidence

- Supplied review proposes deterministic checks and scalable verification (literature_review.pdf §4.4 p. 4 and §6.4 p. 6); this verifies review content, not the underlying claim.
- JevAct checks selected tool actions with executable facts plus model judgments and bounded correction (arXiv:2610.38620 §§3–5). It confirms related work and raises the overlap bar.
- AgentCheck studies tool-fault injection/replay and pass/fail labeling; artifact/protocol needs more audit before design.
- Potential distinction is schedule comparison—final-only vs milestones vs every step—with detection, propagation and overhead measured on same instances. This does not claim runtime verification is new.
- G1 overlaps ScienceFlow live/archive anchoring and matched replay (§§2.3, 3.1.3); AdaCoM mentions periodic/context-threshold invocation; Learning to Steer trains drift interventions; RIR includes adaptive review.
- G2’s closest mechanisms appear in LEAD §§3–6, ScienceFlow §§2–3, AgentRewind §§4–5 and RIR §§4–5.

The focused scan is not systematic and cannot establish absence/novelty.

## Minimum viable experiment (concept only)

- One small deterministic, inspectable long-horizon task with independent acceptance checks and injected faults.
- Compare three candidate schedules on identical task/fault instances with fixed execution budget.
- Log first fault/detection, propagation before detection, externally checked completion, checks/time/cost, false alarms and failures.
- Separate development/validation from final instances and preserve traces.
- If non-oracle milestones or meaningful propagation are impossible, do not present this as a research experiment; revisit G1 or another approved candidate.

This could establish effects only in the deterministic environment, not improved LLM planning/reliability. A bounded LLM-executor extension needs confirmed model access and budget.

## Resources

A small deterministic verifier may be CPU-only and avoid paid APIs, but hardware is unconfirmed. An LLM-agent claim requires an accessible model/version, controls, API/local compute, repeated runs, token/runtime logging and budget. Deadline, API/model access, OS/Python, CPU/GPU/RAM/storage and repo visibility remain UNKNOWN in `docs/project_constraints.md`.

## Strongest argument in favor

Verification cadence is explicit and controllable, with externally checkable outcomes. A small deterministic task could enable paired fault conditions, transparent ground truth, and low-cost measurement of detection latency, propagation and check overhead.

## Strongest argument against

The schedule distinction may already be covered, and deterministic checks may miss semantic planning failures. A deterministic executor would not test LLM-agent reliability. If milestones require hidden task state, this becomes an oracle demonstration.

## Unresolved questions before Phase D

1. Does the researcher prefer G4, G1, narrowed G2, or another candidate?
2. What deadline, API budget, models, OS/Python, CPU/GPU/RAM/storage are available?
3. Is there an approved task environment, dataset, repository, and license/access permission?
4. Can G4 use verifier-visible information only, with independent fault labels?
5. Does a wider systematic search find a prior matched schedule/propagation comparison?
6. What implementation contribution and minimum LLM involvement does the instructor require?

No Phase C research direction was approved at the time of that recommendation.

## Phase D update

The researcher selected G4 as the direction for Phase D; D007 records that selection only. The G4 schedule proposal is now narrower than the Phase C recommendation: Agentic Robot already studies periodic verification frequency and cost, and VReAct already proposes dependency/integration-level checking. The proposed empirical distinction is equal available check slots for fixed-periodic vs graph-derived milestone placements, a common deterministic assertion set, and controlled fault/taint outcomes. This may be a limited extension and requires broader overlap checking; it is not a novelty claim or approval of the protocol.
