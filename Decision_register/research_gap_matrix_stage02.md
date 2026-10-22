# EVIDENCE-BASED GAP MATRIX
## Stage 02 | Literature-to-experiment screening
**Project:** Planning-Quality Degradation in Long-Horizon Autonomous Research Agents  
**Date:** 22 October 2026  
**Source:** S02 — Overleaf_Final_Paper(5).pdf, 11 pages  
**Status:** Candidate questions only; originality and primary-source verification pending

---

## 1. Reading protocol and scope
**VERIFIED** means that a claim appears in the uploaded review, not that its cited original publication has been inspected. **INFERRED** identifies our candidate experimental interpretation. **UNKNOWN** means missing evidence. Do not promote any candidate into a novelty claim without a separate literature search and a direct comparison with the originals.

The review's core distinction is important: task horizon, model context length and persistent memory are not interchangeable (S02 §2.2). An evaluation should avoid measuring only context length and then calling the result planning quality.

## 2. Central methods in the review
| Method | Mechanism described in S02 | Review location / ref | Original-source status |
|---|---|---|---|
| Tree-of-Thoughts | BFS/DFS exploration of reasoning states | §4.1, [12] | UNKNOWN |
| LATS | MCTS with feedback, reflection and rollback | §4.1, [13–14] | UNKNOWN |
| Flare | Lookahead, value propagation, limited commitment | §4.1, [1] | UNKNOWN |
| AdaCoM | Learned external context controller | §4.2, [16] | UNKNOWN |
| Goal2Skill | Lossless state, compressed reasoning traces | §4.2, [8] | UNKNOWN |
| ScienceFlow | Recoverable executable workspaces | §4.3, [5] | UNKNOWN |
| FARS | Hierarchical research-stage isolation | §4.3, [6] | UNKNOWN |
| Reflexion | Feedback-driven verbal correction | §4.4, [15] | UNKNOWN |

## 3. Benchmarks and reported measurements
The following numbers are **VERIFIED AS REPORTED IN S02 TABLE 2 (§5.1)** only. They are not reproduced scores and may not be directly comparable.

| Benchmark | Review-reported scale | Review-reported baseline | Review-reported score |
|---|---|---|---|
| MLE-Bench | 75 tasks | o1-preview | 16.90% |
| PaperBench | 8,316 tasks | o1-high | 26.00% |
| SciReplicate-Bench | 100 tasks | Claude 3.7 Sonnet | 39.00% |
| CORE-Bench | 270 tasks | GPT-4o | 55.56% |
| ML-Dev-Bench | 30 tasks | Claude 3.5 Sonnet | 50.00% |

S02 also reports 70.22% for ScienceFlow on MLE-Bench. **UNKNOWN:** identical task subset, metric, budget, agent configuration and evaluation protocol. Verify [3] and [5] before making a cross-system comparison.

## 4. Reported limitations: provenance caution
**VERIFIED (review content):** S02 §§3 and 5 discuss compounding errors, context pollution, goal drift, no-recovery, implementation failure, greedy hill-climbing and verification gaps. Section 6 proposes dynamic control, process-level credit assignment, reversible state and scalable verification.  
**UNKNOWN (author-reported attribution):** We have not inspected the original authors' limitation sections. Until then, these are *limitations described by the review*, not confirmed admissions or unaddressed gaps in each original publication.

## 5. Five candidate computational gaps

### G1 — Event-triggered goal re-anchoring
**Source evidence (VERIFIED in review):** S02 §3.4, lines 232–244 discusses goal drift; §4.2, lines 288–308 describes state serialization/re-anchoring; §6.1, lines 468–475 motivates dynamic control. Cited refs [2], [8], [16].  
**Candidate gap (INFERRED):** Compare event-triggered re-anchoring with fixed schedules, rather than assuming either is better.  
**Question:** At matched budget, does an observable drift trigger improve task completion relative to fixed-interval re-anchoring?  
**Design:** Same task/model/prompt; arms = no re-anchor, fixed-interval, event-triggered. Predefine drift signal and threshold on development tasks, not the test set.  
**Evidence:** Completion by horizon, constraint violations, redundant actions, re-anchor count, tokens, wall time, failure traces and uncertainty intervals.  
**Threats:** Detector may leak oracle information; trigger calls may increase budget; task difficulty may covary with horizon.  
**UNKNOWN / verify:** Whether AdaCoM [16] or the harness described in [8] already performs equivalent comparisons.

### G2 — Recovery-aware subtask decomposition
**Source evidence (VERIFIED in review):** S02 §3.5, lines 247–257 describes no-recovery across isolated subtasks; §6.3, lines 488–495 discusses rollback; refs [10], [14], [5].  
**Candidate gap (INFERRED):** Quantify the effect of preserved diagnostic state on recovery from errors at subtask boundaries.  
**Question:** How does diagnostic-state preservation change error localization and successful recovery?  
**Design:** Same decomposed tasks and controlled injected faults; arms = isolated subtasks, summary handoff, structured checkpoint + rollback. Fix fault types, injection points and recovery budgets.  
**Evidence:** Recovery success, localization accuracy, final completion, additional steps, execution overhead and trace-level failure categories.  
**Threats:** Faults must be realistic and not trivially detectable; richer state may imply higher token or tool budget; synthetic tasks may not generalize to research agents.  
**UNKNOWN / verify:** Existing LEAD [10], LATS [13–14] and ScienceFlow [5] ablations and exact recovery interfaces.

### G3 — Context fidelity versus reliability
**Source evidence (VERIFIED in review):** S02 §3.3, lines 207–227 covers context pathologies; §4.2, lines 288–308 describes adaptive management and lossless state with compressed reasoning; refs [7], [8], [16].  
**Candidate gap (INFERRED):** Test whether structured retention of task-critical state differs from generic compression at matched context budgets.  
**Question:** Does state-aware compression better preserve planning quality than generic summaries or truncation?  
**Design:** Full-history reference, truncation, generic summarization, structured-state summary; use common model, tasks and target token budget where applicable.  
**Evidence:** Completion, state-retention probes, violated constraints, missed dependencies, tokens and cost by horizon.  
**Threats:** Summary quality varies; full history may exceed budget; improved recall does not automatically imply improved planning.  
**UNKNOWN / verify:** AdaCoM [16] ablations and any equivalent Goal2Skill evaluation.

### G4 — Intermediate deterministic verification
**Source evidence (VERIFIED in review):** S02 §4.4, lines 328–341 discusses cheap verification; §6.2, lines 478–485 discusses sparse outcome feedback; refs [7], [8].  
**Candidate gap (INFERRED):** Estimate how verification schedule changes error propagation under fixed resources.  
**Question:** Is milestone-based checking a better completion/overhead trade-off than final-only or every-step checks?  
**Design:** Same agent and tasks; final-only, every-step and predeclared milestone verification. Use deterministic tests or assertions and log every failure.  
**Evidence:** First-error detection latency, propagated errors, final completion, tool overhead, total cost and false alarms.  
**Threats:** Milestones may encode privileged knowledge; frequent checks consume resources; checks may miss semantic planning errors.  
**UNKNOWN / verify:** Whether source publications or subsequent work already compare schedules.

### G5 — Reversible versus greedy experimental commitment
**Source evidence (VERIFIED in review):** S02 §5.2, lines 425–443 describes commit-or-discard, risk aversion and anchoring; §4.1, lines 266–283 surveys lookahead/search; refs [1], [11–14].  
**Candidate gap (INFERRED):** Compare greedy acceptance with branch retention when a temporary regression can lead to later gain.  
**Question:** At an equal experiment budget, can reversible branches escape plateaus more effectively than greedy commitment?  
**Design:** Greedy commit/discard, bounded temporary regression and checkpoint-based branching on delayed-reward tasks; predefine selection rule.  
**Evidence:** Final objective, exploration diversity, plateau frequency, recovery from poor choices, number of trials and compute.  
**Threats:** Task reward landscape may unfairly favor branching; branching may receive more search capacity; synthetic delayed rewards may not transfer.  
**UNKNOWN / verify:** Scope of the behavioural case study [11] and existing Flare/LATS comparisons.

## 6. Gap-to-experiment summary matrix
| Gap | Source evidence | Candidate question | Minimal comparison | Primary outcomes |
|---|---|---|---|---|
| G1 | §§3.4, 4.2, 6.1 | When should an agent re-anchor? | None vs fixed vs triggered | Completion, drift, cost |
| G2 | §§3.5, 6.3 | What state enables recovery? | Isolation vs summary vs rollback | Recovery, localization |
| G3 | §§3.3, 4.2 | Which context representation survives long horizons? | Truncate vs generic vs structured | Completion, state retention |
| G4 | §§4.4, 6.2 | How frequently should steps be verified? | Final vs every-step vs milestones | Detection, propagation, cost |
| G5 | §§4.1, 5.2 | Does reversibility reduce myopia? | Greedy vs bounded vs branching | Final score, diversity |

## 7. Provisional prioritization
**Assumption:** Limited compute and a lightweight agent harness. Actual hardware/API access is UNKNOWN. The following is a qualitative planning assessment, not measured performance.

| Rank | Gap | Significance | Implementation feasibility | Resource demand | Why screen it |
|---|---|---|---|---|---|
| 1 | G2 Recovery-aware decomposition | High | High | Low–Medium | Controlled faults and observable recovery |
| 2 | G4 Process verification | High | High | Low–Medium | Deterministic tests and interpretable cost |
| 3 | G1 Adaptive re-anchoring | High | Medium | Medium | Central planning question; trigger harder |

G3 remains a useful alternative if context tooling is available. G5 needs carefully designed delayed-reward tasks and strict budget matching. Rankings may change after primary-source and feasibility audits.

## 8. Priority verification flags
- Verify reported 35-minute degradation threshold and quadrupling of failure probability against [8].
- Verify the 25–30-tool-call claim against [8].
- Examine assumptions behind stationary S(H)=p^H, nonstationary products and the phrase “super-exponential decay” against [9].
- Verify all Table 2 scales, scores, definitions, versions and comparability against original benchmark sources.
- Inspect AdaCoM [16], LEAD [10] and ScienceFlow [5] for overlapping ablations before claiming a gap.
- Reconcile repeated LATS bibliography entries [13], [14], [17].
- Distinguish an original author's stated limitation from this review's interpretation.

## 9. Decision entries and next gate
| ID | Status | Decision | Rationale / next action |
|---|---|---|---|
| D004 | VERIFIED (review only) | Retain G1–G5 as candidates, not novelty claims. | Primary-source audit outstanding |
| D005 | INFERRED / provisional | Screen G2, G4 and G1 first. | Observable outcomes under likely constrained resources |
| D006 | UNKNOWN / pending | Do not freeze baseline or benchmark. | Need code, original papers, evaluation scripts and budget |

**REQUEST:** Attach original PDFs or verifiable source materials for LEAD [10], ScienceFlow [5] and AdaCoM [16], plus current compute/API constraints.  
**NEXT GATE:** Complete claim-to-primary-source audit; choose one falsifiable question; document protocol and baseline before coding.

## 10. Change log
| Date | Entry |
|---|---|
| 2026-10-22 | Five candidate gaps and provisional ranking recorded |
| 2026-10-22 | Expanded evidence matrix and experimental controls; no results or novelty invented |
