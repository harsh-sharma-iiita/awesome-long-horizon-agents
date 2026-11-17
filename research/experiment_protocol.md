# Experimental Protocol — G4 (proposed, not frozen)

**Phase D design proposal.** No implementation or experiments are authorized by this document. The selected direction is G4; all design parameters below remain pending human approval.

## 1. Aim and scope

Compare where deterministic workflow checks are scheduled, holding the verifier and call-slot allowance constant for the primary fixed-periodic (B) vs dependency-milestone (C) comparison. The deterministic core estimates workflow-level effects under controlled generated tasks and injected faults. It does not establish LLM-agent planning reliability. A small LLM-executor extension is optional and conditional on actual access/budget.

## 2. Task environment

### Proposed custom task family

Generate structured-data transformation workflow DAGs. Each node is a deterministic operation with declared input types, output schema, and checkable contracts. Candidate operations: parse/validate, filter, normalize, aggregate, keyed join, serialize. Goal is a terminal artifact satisfying its public contract and hidden independent evaluator checks.

- **Initial state:** generated input records, public task specification, dependency DAG, operation contracts.
- **Goal state:** all required nodes executed in valid topological order; terminal artifact passes independent acceptance evaluator.
- **Execution step:** execute one ready DAG node using only predecessor outputs and its operation specification. Use stable topological tie-breaking.
- **Dependency structures:** chain; fan-out/fan-in join; mixed chain + joins. Tasks are designed to contain two internal dependency integration boundaries; their positions vary by graph and are exposed in the task DAG.
- **Horizon levels:** H=12, 24, 36 execution nodes (proposed). All conditions use identical graph instances and node order.
- **Checks/assertions:** required-field/schema checks; allowed type/state transition; key/reference integrity at joins; public numerical conservation/range invariants; terminal output schema. Register assertions before final evaluation.
- **Task generation:** seeded deterministic generator with graph ID and seed stored in manifest. Balance topology across horizons. If generator seeds produce invalid or trivially easy graphs, reject using development-only rules before validation/final splits.
- **Split:** proposed 5 development graphs per horizon, 5 validation graphs per horizon, 30 final graphs per horizon (10 per topology per horizon). Use disjoint seeds/task IDs. Do not tune using final results. Pilot may revise sample size or generator before the protocol is frozen; no power claim is made.
- **External benchmark:** not selected. LIBERO is embodied and resource-heavy for this custom deterministic fault/scheduling question; using it would make controlled fault placement and identical checker comparison difficult. This is a feasibility judgment, not evidence that no benchmark is suitable.

### Task quality controls

Before locking final tasks, demonstrate on development/validation only that (a) dependencies are real and downstream nodes consume predecessor outputs, (b) milestone positions differ from periodic positions in a prespecified share of graphs, (c) faults can propagate, (d) checker assertions are public and non-oracular, and (e) all task conditions run with the same stable node order. Report the share and criteria; do not pick final tasks based on outcome favorability.

## 3. Four comparison conditions

Use one checker implementation, one assertion catalog, one deterministic executor, one fault injector, and one recovery response across all arms. The checker runs the same registered assertions over all completed artifacts at each invocation; only invocation placement changes.

| Arm | Scheduling logic / when | Verifier input and pass rule | Failed check response | Calls and expected overhead | Advantages / limitations |
|---|---|---|---|---|---|
| **A. Final-only** | Invoke once after H nodes at terminal acceptance. | Public task/DAG/contracts + all completed state. Pass iff all registered applicable assertions pass. | Common rollback/replay policy below. | 1 original-pass call; lowest reference overhead. | Clear endpoint reference; provides no intermediate containment. Not call-budget matched to B/C. |
| **B. Fixed-periodic** | H has two equally spaced checkpoints, at ceil(H/3), ceil(2H/3), then final H; 3 slots total. | Same as above, restricted to completed/current state. | Same common policy. | 3 maximum original-pass calls. | Simple reproducible schedule; timing ignores graph joins. Primary comparator. |
| **C. Dependency milestones** | Two graph-derived integration boundaries (from public DAG, e.g. completion of declared join inputs before downstream join/use) plus final H; 3 slots total. | Same checker/input/pass rule as B. | Same common policy. | 3 maximum original-pass calls. | Aligns checks with dependency integration; schedule algorithm must not use evaluator labels/outcomes. Primary candidate. |
| **D. Every-step** | Check after each of H node executions, including final. | Same checker/input/pass rule. | Same common policy. | H original-pass calls; highest expected check overhead. | High-frequency reference; not a matched-budget comparison. |

**Budget fairness:** B and C receive exactly three available check slots per original task pass. A and D are reference conditions with different call allowances and must not be described as matched-budget. If a failed check halts the original pass early, realized calls may be fewer than three; log both allocated slots and actual calls. B/C comparison is therefore equal maximum/allocated original-pass calls, not forced equal realized calls after early stopping.

**Milestone derivation:** Milestones are generated from the public DAG/task spec before any fault is assigned. They are not provided future output values or evaluator truth. The initial task generator is constrained to exactly two milestone boundaries plus final check so the B/C slot count is identical. If a DAG has multiple qualifying boundaries, a deterministic tie-break rule must be documented and frozen before final evaluation.

## 4. Fault injection

Use one fault per injected episode. Fault type and location are generated from a preregistered manifest. Injection occurs once immediately after the designated node produces its artifact. The evaluator records ground truth in a separate evaluator-only file; the verifier and executor do not see the fault label, location, or injection seed.

| Fault type | Injection point and example | Expected consequence | Verifier-visible trigger? | Recoverability |
|---|---|---|---|---|
| Missing field | After producing a structured record, remove a required field. | Direct consumers may fail schema checks or propagate incomplete data. | Yes if public schema assertion applies; test detection at next scheduled check. | One-shot replay can restore. |
| Type/transition corruption | Replace a declared numeric/string type or create disallowed state transition. | Operation may error, coerce, or pass malformed value downstream. | Yes if assertion is checked. | One-shot replay may restore; deterministic exception is logged. |
| Numeric corruption | Perturb a value so a public conservation/range invariant is violated. | Aggregates/outputs may become wrong; taint flows through descendants. | Yes only where registered invariant can observe it; do not expose exact expected hidden output. | Replay may restore. |
| Broken dependency reference | Corrupt a join key/reference to a nonexistent or wrong record. | Join result incomplete/incorrect; downstream consumers may use it. | Yes if key/reference integrity assertion applies. | Replay may restore. |

Positions: early, middle, late by topological execution index (predefine bins from H, e.g. first, middle, final third); avoid placing a fault at a node with no downstream descendants for the primary propagation metric. Keep such cases only as separately labeled detection-only cases if desired.

Run clean no-fault task episodes for false-positive measurement. Also report faults that violate independent final acceptance but evade the checker, because deterministic assertions do not cover every semantic error.

## 5. Response to failed verification

**Proposed common policy: restore and replay once.** Save a lightweight snapshot at every node boundary for every arm (equal snapshot instrumentation/storage mechanism). On failed check, stop the current pass, restore the most recent checkpoint whose verifier result passed (initial state is the fallback), and replay the suffix once with the one-shot fault injector disarmed. Use the exact same executor. Do not invoke additional scheduled checks during replay; the final evaluator assesses terminal artifact. If replay raises an execution error or fails external acceptance, mark task failed. No method-specific repair logic or extra retries.

**Alternatives considered:** (1) halt/report failure is simplest and isolates detection/propagation, but leaves faulted-task completion uninformative; (2) reject and retry only the current node is cheap but can preserve corrupted upstream state or repeat a persistent fault; (3) common rollback/replay gives every arm the same recovery behavior and permits completion measurement, but combines schedule placement with restore distance and is optimistic for one-shot transient faults. Recommend (3) for review, with those limitations disclosed. Researcher approval pending.

Execution cap: at most H original node executions + H replay executions. Check cap: A=1, B=C=3, D=H on original attempt; replay adds zero verifier calls. Common acceptance evaluation is not counted as a verifier call.

## 6. Proposed sample and pairing

- **Final task graphs:** 30 per horizon × 3 horizons = 90 graphs, balanced over 3 dependency motifs (10 per motif/horizon).
- **Fault variants per graph:** 4 fault types × 3 positions = 12; plus one clean episode. Thus 1,080 fault scenarios + 90 clean scenarios = 1,170 scenario instances.
- **Arms:** each scenario is run once under A–D, giving 4,680 initial episodes before replay. B/C pairs share task graph, fault type, position, seed and input. Deterministic execution does not require repeated stochastic seeds; graph seeds provide independent generated instances. Replay is part of each episode, not a separate replicate.
- **Pilot split:** separate 5 development + 5 validation graphs per horizon (30 graphs total); final 30/horizon remain untouched. Pilot checks task quality, logging and runtime; freeze all protocols before final split is opened.
- **Feasibility:** this count is an initial practical proposal, not a power calculation. Review after pilot graph-level variability/runtime and adjust before any final outcomes are examined. If resources are too limited, fallback is 10 final graphs per horizon, balanced across motifs, with all 12 fault variants and clean controls; treat resulting estimates as exploratory and report wide uncertainty.

Estimated first-pass deterministic node executions: 4 × 390 scenario instances/horizon? Specifically 390 scenarios per horizon (30 graphs ×13), so 4 × 390 × (12+24+36) = 112,320 node executions, plus at most one replay of the executed suffix per triggered episode. API calls/cost are zero for this deterministic core; wall time and disk use cannot be estimated until implementation and host capacity are measured.

## 7. Configuration and logging

- One config per protocol version: horizons, DAG generator version, task/fault seeds, assertion catalog, schedule parameters, retry policy, and split IDs.
- Pre-final manifest enumerates all graph/fault scenarios. Hash task specs, configs, code revision, and assertion definitions.
- Append-only JSONL event traces; distinct evaluator-only labels file with restricted access. Never expose ground-truth labels in verifier inputs.
- Record run ID, timestamp, code revision, Python/package versions, OS, random/task seed, command, task/fault IDs, condition, every node input/output hash, taint lineage, check call/inputs/results/timing, snapshots, replay, final evaluator result, runtime and memory/storage.
- Preserve error logs and unsuccessful runs; no overwrites.
- No model fields in the deterministic experiment other than “not applicable.” If LLM extension approved, also log exact model/version, provider, prompt/config hash, temperature, request IDs, token counts, prices/date, timeout/retry behavior, and raw response under data policy.

## 8. Deeper analyses

Recommend two prespecified analyses: (1) horizon sensitivity across H=12/24/36; (2) fault-location sensitivity across early/middle/late positions. Add topology as a stratified descriptive analysis. Do not add a “milestone ablation” that is simply another equal-frequency schedule unless its intervention is predeclared; B is already the equal-slot periodic comparator. A secondary topology-matched/equally frequent but non-dependency placement can be explored only as a separately approved arm because it adds conditions and multiplicity.

Failure analysis should enumerate undetected fault classes, first violated contract, affected descendant nodes, false alarms on clean tasks, and replay failures. These are descriptive and useful even if H1 is unsupported.

## 9. Analysis plan

Primary paired contrast: B vs C on identical graph × fault scenarios. Average paired taint-consumption differences within each task graph, then estimate across graph clusters. Report effect size and 95% graph-cluster bootstrap interval; use paired permutation on graph-level means as a nonparametric primary test if approved. Do not assume normality. Binary outcomes use paired risk differences and graph-cluster bootstrap intervals. Delay, runtime, replay, and storage show medians/IQR and graph-cluster intervals. Stratified analyses are secondary/exploratory; adjust/report multiplicity if formal tests are made. No statistical significance claim without the approved test and assumptions.

## 10. Deterministic vs LLM evaluation

| Option | What it measures | Limits | Resource/reproducibility |
|---|---|---|---|
| A. Deterministic workflow (recommended core) | Controlled schedule effect with known task contracts/faults, exact provenance and deterministic replay. | Not LLM planning, natural-language fault interpretation, or general agent reliability. | No API/GPU required in principle; highly repeatable; actual host is only partially observed. |
| B. LLM executor | How a selected model performs workflow steps and responds to the same schedules/checker. | Model-specific; prompts and single executor may dominate; temp 0 is not guaranteed determinism; fault injection still artificial. | Model/API access and cost unknown; stochastic repetitions and raw traces needed. |
| C. Hybrid | Deterministic confirmatory mechanism study plus small matched LLM slice using identical B/C schedule policy. | LLM slice underpowered/exploratory; two systems add integration complexity; not automatic improvement in validity. | Conditional on local/API availability and approved cost. Candidate mini-slice: 1 graph per horizon, a small preregistered fault subset, B/C only, 2–3 repeats; estimate calls as number of execution nodes plus verifier invocations and price from actual provider tariff. Do not start unless resources are confirmed. |

**Recommendation:** deterministic core first; consider a small LLM extension only if an accessible model and budget are confirmed and the question remains important to the assignment. A hybrid is not currently resource-verified. If deterministic-only is used, present conclusions as controlled workflow scheduling evidence, not LLM-agent reliability.

If the optional LLM slice is approved, use the same fixed prompt template/model/settings for B and C: provide only the current node operation, declared public contract, and available predecessor outputs; require a schema-constrained result; do not include fault labels, injection location, future outputs, or evaluator expected values. Temperature 0 is a proposed control, not a determinism guarantee. Repeat each selected task/fault condition under a predeclared number of seeds and report all model/provider errors. Retries must follow the common protocol, not an arm-specific prompt or repair instruction.

## 11. Threats to validity and mitigation

| Threat | Mitigation / residual limitation |
|---|---|
| Internal validity / implementation differences | One executor/checker/recovery implementation with condition as config; paired task/fault inputs; config/code hashes; still vulnerable to bugs. |
| Construct validity | Taint-consumption and injected faults operationalize propagation; may not represent semantic planning errors or real research work. State this boundary. |
| Measurement validity | Independent evaluator and event instrumentation; validate evaluator and taint rules on hand-audited dev traces; instrumentation itself may alter runtime. |
| Task difficulty imbalance | Same graph paired across all arms; stratify horizon/topology; seed manifest and generation validity filters fixed before final evaluation. |
| Fault realism | Use four interpretable contract violations and clean controls; one-shot synthetic faults remain less realistic than naturally occurring errors. |
| Verifier limits | Public assertions, static catalog, checker mutation/coverage review on dev tasks; report faults not observable to checks. |
| Unequal budgets | B/C same three available call slots and H+H action/replay cap; report realized calls and replay work. A/D explicitly reference arms with different budgets. |
| Hidden information leakage | Separate verifier input from evaluator labels, expected terminal outputs and seeds; audit serialized inputs. |
| Model variability | Deterministic core avoids model variation; optional LLM slice fixes model/settings and repeats; conclusions remain model-specific. |
| Small sample / dependence | Graph-clustered inference and intervals; pilot-informed final N; no unsupported power/significance claims. |
| External validity | Generated data DAGs only; no claim of general agent or research-workflow transfer. Later replication on an independent task family would be needed. |
| Hardware/API constraints | Measure host and actual runtime before freeze; LLM study conditional on access/budget; deterministic fallback retains narrow claim. |
| Researcher/implementation bias | Predefine task generator, metrics, split, and analysis; retain configs/logs; blinded evaluator labels from verifier where practical. |

## 12. Final design review — approval table

| Decision | Proposed recommendation | Evidence | Approval status |
|---|---|---|---|
| Primary research question | Matched periodic vs dependency-milestone placement and taint-consumption fraction | User's provisional RQ; Agentic Robot §3.4; VReAct §3.4 | Pending |
| Comparison conditions | A final-only, B periodic, C dependency milestones, D every-step; B/C primary matched three slots | User-required conditions; scheduling proposal | Pending |
| Main B-versus-C comparison | Same three slots, verifier, task/fault cases, executor, response policy | Fairness requirement; controlled design proposal | Pending |
| Task environment | Custom seeded structured-data DAG tasks, H=12/24/36, three motifs | Feasibility inference; no benchmark selected | Pending |
| Fault injection | Four one-shot contract-violating fault classes, three positions; plus clean controls | User's fault examples; proposed taxonomy | Pending |
| Verification response | Restore last passing snapshot and replay once with injector disarmed | Consistent across arms; isolates schedule from method-specific repair; replay limitation disclosed | Pending |
| Primary metric | Downstream taint-consumption fraction per eligible fault episode | Operational definition in hypotheses_and_metrics.md | Pending |
| Secondary metrics | Coverage, delay, completion, FPR, calls, runtime, replay work, storage | Operational definitions in hypotheses_and_metrics.md | Pending |
| Number of runs | Proposed 30 final graphs/horizon; 1,170 scenarios ×4 =4,680 initial episodes, plus replays | Practical estimate only; no power claim | Pending |
| Deeper analysis | Horizon and fault-position sensitivity; topology descriptive | User request; prespecified proposal | Pending |
| LLM evaluation | Deterministic core; optional small B/C LLM slice after access/cost confirmation | Model access and API budget UNKNOWN | Pending |
| Resource budget | No paid API in deterministic core; CPU/time/storage measured during pilot; total budget UNKNOWN | Current constraints record and limited host observation | Pending |

For each substantive choice, the strongest counterargument is the overlap/construct-validity risk: periodic frequency is already empirically compared, integration verification is already proposed, and deterministic synthetic workflows may not represent LLM planning. The strongest support is controlled pairing with equal B/C check slots and independently tracked fault propagation, allowing a narrow, reproducible test without expensive model calls.

### Strongest argument for and against each major recommendation

| Recommendation | Strongest argument for | Strongest argument against |
|---|---|---|
| Narrow RQ: equal-slot dependency vs periodic schedule | Isolates placement from check quantity with observable taint outcomes. | Agentic Robot already evaluates periodic cadence and VReAct anticipates integration verification; the extension may be too incremental. |
| Custom DAG environment | Exact dependencies, fault truth, pairing, and low likely compute cost are controllable. | Synthetic DAGs may be artificial and do not establish deployed LLM-agent behavior. |
| Four arms A–D, B/C primary | Provides low/high-frequency references while preserving a fair primary comparison. | A/D have different budgets; arm results can invite invalid across-budget causal claims unless clearly qualified. |
| Four injected fault classes + clean controls | Makes fault location/type reproducible and supports false-alarm estimates. | Injected contract faults may be easier and less realistic than semantic failures. |
| Restore/replay once | Gives a common, bounded recovery response and makes completion measurable. | Recovery benefits from one-shot faults and may conflate schedule placement with checkpoint distance. |
| Taint-consumption fraction primary | Directly measures downstream execution affected before detection. | Requires reliable evaluator-side data lineage and may not capture severity or semantic impact. |
| Proposed N=30 graphs/horizon | Balanced task graphs and repeated fault scenarios create paired evidence while staying deterministic. | No power analysis; many scenarios share 90 graphs, and runtime/storage are unmeasured. |
| Horizon/location analyses | Tests whether schedule effects depend on task length and when faults occur. | More strata reduce precision and increase multiple-comparison risk. |
| Deterministic core; optional LLM slice | Preserves controlled evidence and avoids assuming model access or API budget. | Core result cannot support LLM-agent reliability; a tiny LLM slice may be underpowered and expensive. |
| No final budget estimate before pilot | Avoids fabricated runtime/cost claims. | Prevents a definite feasibility decision until host and constraints are confirmed. |
