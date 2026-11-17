# Hypotheses and Metrics — G4 design proposal

**Status: proposed, not frozen.** G4 was selected by the researcher; hypotheses, estimands, operational definitions, tests, and priorities still require approval before final evaluation.

## Candidate hypotheses

The primary directional hypothesis is a proposal derived from the candidate mechanism, not an established result:

- **H1:** In matched task/fault pairs, dependency-boundary checks produce a lower mean downstream taint-consumption fraction than fixed-periodic checks with the same three available check slots.
- **H0:** The paired mean difference in that fraction is zero.

Exploratory questions (not confirmatory hypotheses until approved): horizon/fault position may moderate the schedule effect; schedules may differ in detection coverage, completion, and verifier/replay runtime. Do not manufacture directional hypotheses for these secondary outcomes.

## Variables

- **Independent variable:** scheduling rule (A final-only, B fixed-periodic, C dependency-based milestones, D every-step).
- **Primary contrast:** B vs C. The available call-slot budget is three checks per original pass for both; A and D are reference points with different budgets.
- **Controlled:** same task instance, fault type/position, executor and operation order, checker assertions, inputs/specification, retry response, execution cap, machine/software, and evaluator.
- **Primary outcome:** downstream taint-consumption fraction per injected-fault episode.

## Operational definitions and formulas

Let task graph instance be g; task execution nodes V_g; fault episode e=(g,f,j), where f is a predefined one-shot fault type and j is its injection node. Let Desc_g(j) be the set of downstream nodes whose dependency paths use j's corrupted artifact. The evaluator tracks taint lineage independently of the verifier.

| Metric | Formula / numerator and denominator | Unit; direction | Logs, edge cases, interpretation |
|---|---|---|---|
| **Primary: taint-consumption fraction** | For episode e, TCF_e = C_e / max(1, |Desc_g(j)|), where C_e is the number of distinct downstream node executions that consume an artifact marked tainted before the first failed check triggers halt/replay or before original attempt termination. Paired schedule effect: mean_g,episodes(TCF_C − TCF_B), first average episodes within graph g, then average over graphs. | [0,1]; lower is better. Negative C−B favors milestones. | Requires evaluator-only taint lineage. A downstream node counts once even if it reads multiple tainted inputs. If no descendants, exclude that injection position from this metric and report separately. Retry executions are not included in first-attempt C_e; report replay separately. A low value means fewer downstream consumers in this generated DAG, not generally lower agent error. |
| Fault detection coverage | DRate = N(injected episodes with failed verifier check before original attempt termination) / N(eligible injected-fault episodes). Report B/C paired risk difference. | proportion; higher is better. | Log injection ID/time, check time and verdict. Report all injected faults and a secondary subset that violates at least one declared verifier-visible contract. Never omit undetected faults. |
| Fault detection delay | For episode e with fault after node j and first detection after node t, Delay_e = t−j (number of later executor nodes completed before detection); an immediate check yields 0. If never detected, assign sentinel H−j+1, one more than all possible subsequent executed nodes. | execution nodes; lower is better. | Report coverage beside delay; sentinel is a penalty coding, not an estimated latent delay. Also show detected-only distribution, clearly conditional and subject to survivor bias. |
| Task completion | CR = N(task episodes whose independent evaluator accepts terminal artifact within original + one replay cap) / N(task episodes started). Report clean and faulted separately, then combined only with declared weighting. | proportion; higher is better. | Evaluator uses hidden expected values/labels, not sent to checker. Completion can be zero after replay failure or an undetected corrupt terminal result. Count retries within same episode, not as new task starts. |
| False-positive check rate | FPR_check = N(failed check calls on clean tasks) / N(check calls on clean tasks). Also FPR_task = clean episodes with at least one failed check / clean episodes started. | proportion; lower is better. | Clean runs must use same schedules. A replay after false alarm is logged; denominator remains original scheduled check calls actually made. If zero checks in a run, it contributes to task-level but not call-level denominator. |
| Verification calls | Actual verifier invocations per episode; separately report allocated maximum slots (A=1, B=C=3, D=H on the original pass) and calls on replay (proposed policy: none). | calls; lower cost, but fewer is not inherently better. | Early stop can make realized calls differ despite equal B/C slot caps. Record every request, verdict, and timestamp. Main comparison is equal available slots; report realized use. |
| Verifier execution time | Sum of wall-clock time inside verifier assertions per episode, measured with monotonic clock; also per call. | seconds; lower is less overhead. | Separate checker time from executor, scheduling, snapshot and replay time. Report median/IQR and paired graph-level distributions. |
| Total workflow time | End-to-end elapsed monotonic time from first task step through accepted result or terminal failure, including checks, snapshotting, rollback and replay. | seconds; lower is faster, subject to completion. | Also show time conditional on accepted completion and failure. Hardware/load fixed where possible; no cross-host comparison. |
| Execution overhead | Absolute: O_abs = mean(T_schedule − T_final-only) on paired instances. Relative: O_rel = 100 × O_abs / mean(T_final-only), where T is total workflow time. Main B/C comparison also reports T_C−T_B directly. | seconds and percent; lower is less overhead. | Denominator may be zero/nearly zero; in that case report absolute only. Final-only is a reference, not a matched-call arm, so this does not isolate schedule placement alone. |
| Replay work | Number of executor nodes re-executed after rollback; plus rollback distance from last passing snapshot to failed check. | nodes; lower is less recovery work. | Same snapshots stored at every node in every condition; only latest verified state is eligible as restore point. No replay checks are issued. |
| Storage | Snapshot bytes written and retained per episode; snapshot/restore time separately. | bytes, seconds; lower is cheaper. | Measure same snapshot mechanism in every arm; report actual representation/compression. |
| API/token cost | Not applicable to deterministic primary study. If an approved LLM extension is run: sum provider-recorded input/output tokens and dated charges per episode and per accepted task. | tokens/currency; lower cost. | Model/version and tariff date required. Never estimate money solely from tokens. |

## Fault and check interpretation

A fault episode is one evaluator-injected, one-shot corruption at a known DAG node. Candidate fault classes: (1) missing required field/schema violation; (2) wrong type/invalid transition; (3) numeric corruption violating a public conservation/range invariant; (4) broken key/reference at a join. Use one fault per episode in the initial design; multiple simultaneous faults are out of scope unless approved separately.

The verifier checks public contracts and invariants for completed outputs and dependencies. It receives no fault label, injection seed, future output, or hidden exact answer. Fault detectability is defined by whether the corrupted artifact violates at least one registered checker assertion; independently report faults that violate task acceptance but evade the checker. Define this mapping using development tasks only, before final evaluation.

## Statistical analysis proposal

- Pair B and C on identical graph × fault type × injection position instances. The graph is the resampling/independence cluster because many fault scenarios reuse a graph.
- Primary effect: per-graph mean of paired TCF differences (C−B); report mean, median, 95% graph-cluster bootstrap interval and a paired permutation test on graph-level means. No normality assumption.
- Binary detection/completion/FPR: report paired risk differences and graph-cluster bootstrap confidence intervals; avoid treating correlated fault variants from one graph as independent. Exact McNemar may be descriptive only if independence assumptions at the paired unit are defensible.
- Detection delay, runtime, replay nodes and storage: medians/IQR, paired graph-level differences and cluster-bootstrap intervals; show uncensored/sentinel-based delay plus coverage.
- Horizon/topology/fault-location analyses are secondary and stratified; report uncertainty, not an unqualified significance claim. If multiple secondary tests are used, label exploratory and control/report multiplicity (e.g. Holm) before interpreting p-values.
- Use two-sided alpha 0.05 for the single primary test only if approved before final evaluation. A sample count is not a power claim.

## Required event logs

Each event record: run_id, task_graph_id, task_seed, split, horizon, topology, condition, fault_episode_id/type/position (ground truth in evaluator-only file), executor node and inputs, input/output hashes, taint lineage (evaluator-only), check slot and timestamp, verifier-visible state/spec hash, assertion IDs/results, recovery snapshot ID, rollback distance, replay status, final evaluator verdict, per-stage wall time, memory/snapshot bytes, software/config revision, and model/token fields marked not applicable in deterministic runs. Keep verifier-facing and evaluator-only files access-separated.
