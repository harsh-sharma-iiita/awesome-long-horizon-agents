# Next Actions — Before Phase E

**Current phase:** Phase D design proposal. Do not begin implementation until the researcher explicitly approves the initial question and protocol.

## Researcher review required

1. Review the proposed primary question and scope in research_brief.md. Confirm whether controlled deterministic workflow evidence is acceptable, or an LLM executor is required by the assignment.
2. Approve or revise the four arms and primary B/C call-slot matching rule. Clarify whether equal available slots with early stopping is acceptable, since realized calls can differ after a failed check.
3. Approve or replace the custom generated DAG task family, horizons, topologies, task counts, and fault classes/positions.
4. Approve or replace restore-and-replay-once as the shared failed-verification response.
5. Approve or revise the primary taint-consumption fraction, secondary metrics, sample proposal, and paired/clustered analysis.
6. Decide whether to include a small LLM executor extension after model access/API budget is known.

## Evidence and feasibility work before protocol freeze

1. Conduct a broader search for equal-call comparisons of dependency-aware vs periodic checks, controlled fault propagation, and integration verifier scheduling. Phase D source audit is focused, not a novelty search.
2. Inspect accessible code/artifacts for VReAct, Agentic Robot, MAS-ProVe, and JevAct; record licenses, reproduction requirements, and model availability. Current source audit marks unconfirmed artifacts/weights UNKNOWN.
3. Confirm assignment deadline, intended OS/Python, CPU, RAM, free storage, model/API access, budget, and repository visibility. Current-session observations may not describe the research machine.
4. After design approval, pilot only on development tasks to test generator validity, non-oracle checker inputs, graph-derived milestone algorithm, taint instrumentation, replay semantics, and runtime/storage.
5. Use pilot results to finalize task counts, budget, and analysis before opening validation/final splits. Register primary outcome and B/C comparison; retain pilot failures.
6. Obtain explicit approval of the frozen Phase D question/design before Phase E environment configuration and baseline implementation.

## Current not-started items

- No code or task generator exists.
- No verifier/scheduler/recovery implementation exists.
- No task graph, fault injection, pilot or experiment has run.
- No baseline has been independently validated.
- No deadline, API budget, model, dataset or execution budget has been approved.
