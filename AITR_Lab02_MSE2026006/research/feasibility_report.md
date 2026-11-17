# Feasibility Report

**STATUS: PENDING — To be completed in the relevant research phase.**

## Known from the supplied workspace

- The workspace provisionally assumes limited compute and a lightweight harness when ranking gaps. This is a screening assumption, not a measured description of the researcher's resources (workspace p. 8, §7).
- Hardware, API budget, timeline, permitted models, target venue, existing repository, and reproducible baseline are UNKNOWN (workspace pp. 2, 4).
- Original papers/repositories for LEAD [10], ScienceFlow [5], and AdaCoM [16], plus current compute/API constraints, were explicitly requested (workspace p. 9, §9).
- Candidate gap ranking: G2 recovery-aware decomposition, G4 process verification, then G1 adaptive re-anchoring. The workspace describes G2/G4 as high qualitative significance/feasibility with low–medium resource demand; G1 as high significance, medium feasibility and medium demand. G3 is an alternative; G5 requires carefully designed delayed-reward tasks and strict budget matching. This assessment is provisional and unmeasured (workspace p. 8).

## Required constraints

| Constraint | Current status | Evidence still required |
|---|---|---|
| Assignment deadline | UNKNOWN | Google Classroom announcement. |
| API budget | UNKNOWN | Researcher/institution information. |
| Available model access | UNKNOWN | Model/provider, version, terms, and access limits. |
| Operating system | UNKNOWN | Confirm target execution environment. |
| Python version | UNKNOWN | Confirm target interpreter. |
| CPU | UNKNOWN | Hardware details. |
| GPU | UNKNOWN | Hardware/model and access. |
| RAM | UNKNOWN | Hardware details. |
| Storage | UNKNOWN | Workspace and dataset capacity. |
| Dataset/benchmark access and license | UNKNOWN | Official source, terms, and data protocol. |
| Existing repository/baseline | UNKNOWN | Repository URL/files, revision, and logs. |
| Target venue/template | UNKNOWN | Instructor direction, if applicable. |

## Gate 1 feasibility work remaining

1. Collect the constraints above without guessing.
2. Verify primary methods and artifact access for candidate gaps.
3. Identify an accessible task/dataset/measurement protocol and lawful use terms.
4. Estimate calls, runtime, storage, and fallback for the smallest credible baseline and comparison.
5. Compare resource burden and validity threats across candidate questions.
6. Present options and a recommendation for researcher approval; do not freeze a design here.

## Phase C literature-based reassessment (2026-11-04)

The earlier qualitative G2 > G4 > G1 ranking remains historical (workspace p. 8); it was not based on measured resources.

- **G2:** Snapshots and injected faults are technically plausible, but LEAD, ScienceFlow, AgentRewind and RIR closely cover decomposition correction, restoration, rollback and retained recovery information. A narrower diagnostic-state contrast needs overlap checking. LLM execution adds API/model variability and cost; deterministic-only execution tests mechanism feasibility, not LLM-agent reliability.
- **G4:** A small deterministic verifier may run on CPU if an inspectable task exists. Main burden is designing non-oracle milestones and faults with observable propagation. JevAct and related runtime verification overlap generally; exact schedule comparison remains a candidate distinction, not a novelty finding.
- **G1:** A cadence controller is plausible, but ScienceFlow matched re-anchoring, AdaCoM scheduling, goal-drift steering and RIR create substantial overlap. Matching intervention count/cost without changing task conditions is difficult.

### G2 evaluation levels (options for researcher decision)

| Level | Measures | Cannot establish | Difficulty/resources | Reproducibility/contribution |
|---|---|---|---|---|
| A. Deterministic feasibility | Snapshot correctness, restore fidelity/time, recovery under known faults. | LLM planning, model-driven detection, general agent reliability. | Lowest; potentially CPU/no paid API; needs suitable task/harness. | Highly repeatable; feasibility evidence only. |
| B. LLM executor | Model-driven detection/localization/recovery under controlled tasks. | Broad claims from one model/task. | Higher; model/API access, version controls, budget and stochastic reruns. | Directly tests agent behavior, with cost/variability. |
| C. Hybrid | Validate recovery machinery deterministically, then bounded LLM evaluation. | Broad generalization; small sample remains exploratory. | Medium; two-layer setup and some API/local-model resources. | Separates mechanism from model behavior, but adds integration effort. |

**Provisional recommendation:** consider C only if a model is available and narrowed G2 survives overlap review. Without model/API access, A is a feasibility pilot only and cannot support LLM-reliability claims. G2 may still be set aside due to overlap. This is not an approved design.

### Resource-aware fallback

1. If paid API/model access is unavailable, avoid designs requiring repeated closed-model calls; assess a CPU-only pilot and label its inference boundary.
2. If an approved local model exists, fix its version and log hardware/runtime; do not silently substitute.
3. If no model exists, do not imply an LLM experiment was run; revisit the candidate or seek instructor approval for a non-LLM pathway.
4. Keep repository private until visibility is decided; exclude secrets and restricted data.

Deadline, API budget, model access, OS, Python, CPU/GPU, RAM, storage, repo visibility, data permissions and executable baseline remain UNKNOWN. No resource-specific final ranking is defensible yet.

## Phase D — G4 proposal feasibility (2026-11-04)

### Observed execution host vs target environment

Read-only inspection of the current agent execution session found Microsoft Windows build 10.0.26300, Python 3.14.6 at C:\\Python314\\python.exe, and 16 logical processors reported by .NET. A WMI query for exact OS/hardware/physical RAM/GPU/disk details returned Access denied; the available-space result was unusable. These are observations about the current session, not confirmation of the student's eventual machine. Target OS/Python/CPU model, RAM, GPU and free storage remain UNKNOWN. API budget, available local/API model, deadline and repository visibility remain UNKNOWN. requirements.txt is still a pending placeholder; no dependency was installed.

### Proposed workload and resource estimate

- **Deterministic core:** proposed 90 final graph instances (30 each at horizons 12/24/36), 12 fault variants plus one clean variant per graph = 1,170 scenarios; four arms = 4,680 initial episodes. The maximum planned first-pass node executions are 112,320 (4 × 390 scenarios per horizon × (12+24+36) nodes), plus replay suffixes. Snapshot and trace storage volume and runtime have not been measured; do not invent estimates. Pure deterministic checks require no paid API or GPU in principle, subject to actual implementation/environment.
- **API cost for deterministic core:** zero model/API calls by design. This is not yet an execution result or verified cost.
- **Optional LLM slice:** no model is selected. A candidate minimal exploratory slice is one graph per horizon, one clean plus a predeclared small fault subset, B/C only and 2–3 repetitions. Cost formula requires model calls per executed node + verifier calls + replay work, multiplied by the provider's applicable dated rates. Dollar cost UNKNOWN until model, provider, tokenization and budget are known. Do not start this extension without confirmation.
- **Dependencies:** none selected for a proposed pure-Python graph/task generator; use standard library if sufficient. Requirements file remains pending. Any later dependency choice needs license/version review and environment lock before Phase E.

### Feasibility recommendation and fallback

The custom DAG study appears implementable as a small CPU-only deterministic study and gives exact injected-fault ground truth. Its scientific claim is correspondingly narrow. Recommend the deterministic core as the only resource-independent plan currently supportable; treat LLM evaluation as optional and unresolved rather than assuming it makes the experiment stronger. If pilot time/storage is constrained, proposed fallback is 10 final graphs per horizon (30 total), balanced across motifs, with all fault/clean conditions and all arms; report this as exploratory with graph-cluster uncertainty and no power claim. If even this is infeasible, reduce the task generator/scope before final evaluation rather than selecting instances after seeing outcomes.

### What remains dependent on researcher constraints

Deadline determines whether the proposed 4,680 episodes and analysis are reasonable. OS/Python compatibility determines reproducible setup. RAM/storage affect snapshot/trace retention. API/model access determines whether an LLM slice is possible. Repository visibility affects release/privacy choices. These all need confirmation before protocol freeze and Phase E.
