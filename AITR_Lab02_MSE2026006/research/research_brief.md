# Gate 1 Research Brief — G4 (Phase D proposal)

**Status: PROPOSED DESIGN FOR HUMAN REVIEW.** The researcher selected G4 for this phase. The exact research question, task generator, comparison budget, response policy, sample size, and any LLM evaluation below are recommendations, not approved experimental decisions. No novelty is claimed.

## Research problem

The supplied literature review discusses intermediate deterministic checks as a way to detect failures before they contaminate later workflow steps (literature review §4.4 p. 4; §6.2 and §6.4 pp. 5–6). That review claim is not independent validation. Primary sources now show relevant existing work: Agentic Robot compares fixed periodic verifier intervals and reports accuracy/runtime; VReAct proposes unit/integration/acceptance verification but its pilot omits the integration pair; MAS-ProVe evaluates model-based process verification at agent/iteration granularities. See source_audit.md Phase D.

The focused problem proposed here is where to place a fixed number of deterministic checks in a known multi-step dependency workflow when a transient intermediate fault may affect downstream consumers. It studies scheduling and fault propagation in a controlled workflow; it does not by itself study LLM planning quality.

## Proposed primary research question

**On controlled multi-step dependency workflows with one-shot injected contract violations, does dependency-boundary verification, compared with fixed-periodic verification using the same available check slots and the same deterministic verifier, reduce the proportion of downstream workflow steps that consume fault-tainted state before detection, under a common replay policy?**

This narrows the user's provisional question by naming the workflow, fault unit, primary outcome, comparison, and fairness controls. Its scope is deterministic workflow reliability unless an approved LLM executor is added.

## Supporting questions

1. How do task horizon, dependency topology, fault type, and fault position affect detection coverage and delay for the two matched-budget schedules?
2. What is the trade-off between verification schedule and total runtime, verifier time, realized call count, replay work, and checkpoint storage?
3. Do schedule conditions differ in externally evaluated task completion on clean and fault-injected instances, and how often does a valid state trigger a false alarm?

## Candidate contribution and positioning

**Candidate contribution (INFERRED):** a controlled, call-slot-matched comparison of periodic and graph-derived dependency-boundary checks, with the same executable assertions, injected faults, executor, and response policy, measuring downstream taint consumption as well as detection and cost. Existing periodic-frequency results and integration-verification proposals are close prior work. The candidate may constitute a narrow replication/extension; it is not established as novel or publication-worthy.

## Candidate task environment (not selected)

Prefer a custom generated structured-data workflow DAG over adopting LIBERO or a broad agent benchmark for the primary controlled experiment. Candidate operations include parse/schema validation, filtering, normalization, aggregation, keyed join, and serialization. Tasks have 12, 24, or 36 execution nodes, with linear, fan-out/fan-in, or mixed dependency motifs. Each generated task has two predeclared integration boundaries plus a terminal acceptance point; boundary positions vary by graph. That permits exactly three scheduled check slots in the primary B/C comparison (two internal checks and final acceptance) while allowing periodic and dependency-derived placements to differ. This is a design proposal; feasibility and task quality require a pilot.

Task specs expose inputs, operation contracts, dependency graph, output schemas, and checkable invariants. The verifier receives only this public task specification and current/completed state. A separate evaluator retains expected outputs, fault labels, and seeds. The verifier does not receive those labels, future outputs, or evaluator-only expected values. Contracts should be sufficient to catch some faults but should not be an exhaustive hidden-answer oracle.

## Input, output, variables, controls

| Element | Proposed definition |
|---|---|
| Input data | Generated task DAG/specification, initial records, injected fault type and position (held only by evaluator), and clean controls. |
| Output | Verification trace, task state/lineage, detected/undetected outcome, replay trace, final independent acceptance result, and resource log. |
| Independent variable | Schedule: final-only (A), fixed-periodic (B), dependency milestone (C), every-step (D). Primary contrast B vs C. |
| Dependent variables | Downstream taint-consumption fraction (primary); detection coverage/delay, completion, false alarms, calls, verifier/runtime overhead, replay work (secondary). |
| Controlled variables | Paired task graph and fault instance; executor implementation/order; verifier code and assertion set; task/recovery budgets; retry policy; data/specification; runtime environment; instrumentation. |
| Comparison | B and C each receive three scheduled call slots per original pass (two intermediate + final), with placement only differing. A and D are reference conditions, not equal-call comparisons. |
| Falsifying observation | No lower paired taint-consumption fraction for C than B, a higher rate of missed faults, or a completion/overhead trade-off that removes the practical benefit would fail to support the proposed directional claim. |
| Limitations | Deterministic executor and synthetic faults limit claims to this controlled workflow; known DAGs may favor milestone construction; checker contracts bound detectable errors; one-shot faults/replay may not represent persistent failures. |

## Proposed workflow sketch

~~~mermaid
flowchart TD
    A[Task specification and DAG\nPROPOSED] --> B[Generated task environment\nPROPOSED]
    B --> C[Deterministic executor\nPROPOSED]
    C --> D{Scheduled check\nSame verifier and contracts}
    D -->|Pass| E[Continue execution\nPROPOSED]
    D -->|Fail| F[Restore last passing snapshot\nand replay once\nPROPOSED]
    E --> C
    F --> G[Independent final evaluator\nPROPOSED]
    G --> H[Metrics and paired analysis\nPROPOSED]
~~~

No component in this diagram is implemented.
