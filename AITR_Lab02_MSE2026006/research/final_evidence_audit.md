# Phase G.1 — Final Experimental Evidence and Reproducibility Audit

**Audit Date:** 2026-11-04  
**Auditor:** Statistical Analyst & Experimental Research Reviewer  
**Governing Standard:** `AGENTS.md` (Integrity, Evidence Classification, Zero Fabrication, Transparent Negative Results)  
**Evaluated Campaign Run ID:** `final_exp_20261104_015549_5fcb5a61`  
**Dataset Scale:** 4,680 episodes across 90 DAG task clusters ($160,440$ execution trace steps)  
**Audit Classification:** **READY FOR PHASE H**

---

## 1. Executive Summary & Audit Classification

An exhaustive, multi-dimensional reproducibility and evidence audit was conducted on the Phase F and Phase G experimental outputs. The audit confirms:
1. **Mathematical Accuracy of Contradicted Hypothesis:** The primary directional hypothesis $H_1$ (predicting that milestone verification would reduce downstream error propagation relative to periodic verification) is **empirically contradicted** ($\Delta \text{TCF} = +0.0391$, paired permutation $p < 0.0001$, paired $t = 31.78, p = 2.35 \times 10^{-50}$, 95% bootstrap CI $[+0.0366, +0.0414]$). Under matched budgets, fixed-periodic verification achieves statistically superior error containment.
2. **Absolute Verification Budget Parity:** Both Arm B (Fixed-Periodic) and Arm C (Milestone-Based) allocated exactly $K_{\text{alloc}} = 3$ check slots and consumed an identical realized mean of **$2.7436 \pm 0.5872$ verifier calls**. Pair-by-pair contrast across all $1,170$ evaluation scenarios revealed **100.0% exact call matching** between paired episodes.
3. **Mechanical Basis for Identical Detection and Completion Rates:** The identical $33.33\%$ fault detection coverage and $38.46\%$ task completion rate across all four arms are not aggregation artifacts or code bugs, but direct mathematical consequences of:
   - Complete terminal contract evaluation at step $H$ across all conditions.
   - Deterministic structural visibility boundaries (100% detection of missing fields, 33.33% detection of type corruptions, and 0% detection of semantic numeric/reference drifts).
   - Single-replay recovery policy with injector disarming.
4. **Complete Directory Reconciliation:** 103 out of 103 key project files across root `atr-paper/` and `AITR_Lab02_MSE2026006/` match bit-for-bit with identical SHA-256 hashes.
5. **Publication Asset Fidelity:** All six publication figures and result tables match the underlying raw CSV dataset with zero discrepancies.

**Audit Verdict:** **READY FOR PHASE H (Reproducibility & Manuscript Preparation)**. No experimental reruns are needed or warranted.

---

## 2. Canonical Project Directory Reconciliation

### Directory Structure & Roles
- **Root Directory (`atr-paper/`):** Workspace root used by agent tooling and repository versioning.
- **Assignment Subdirectory (`AITR_Lab02_MSE2026006/`):** Official institutional submission directory containing course deliverables, demonstration materials, student metadata, virtual environment (`.venv`), and mirrored source code.

### File Hash Audit & Two-Way Reconciliation
A recursive SHA-256 hash comparison across all key directories was executed via [`scripts/verify_reconciliation.py`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/scripts/verify_reconciliation.py):

| Directory Category | Checked Files | Identical Files (SHA-256 Match) | Discrepancies |
|---|---|---|---|
| **Research Documentation (`research/`)** | 16 | 16 | 0 |
| **Raw & Processed Data (`results/`)** | 8 | 8 | 0 |
| **Result Tables (`results/tables/`)** | 4 | 4 | 0 |
| **Statistical Contrasts (`results/comparisons/`)** | 2 | 2 | 0 |
| **Run Configurations (`runs/configurations/`)** | 5 | 5 | 0 |
| **Run Logs & Trajectories (`runs/logs/`, `runs/trajectories/`)** | 6 | 6 | 0 |
| **Publication Figures (`figures/experiments/`, `figures/analysis/`)** | 12 | 12 | 0 |
| **Source Implementation (`src/`)** | 16 | 16 | 0 |
| **Test Suite (`tests/`)** | 8 | 8 | 0 |
| **Analysis & Audit Scripts (`scripts/`)** | 8 | 8 | 0 |
| **AI Logs (`ai_logs/`)** | 3 | 3 | 0 |
| **Total Key Files** | **103** | **103** | **0 (100% Parity)** |

*Reconciliation Actions Completed:*  
- Synchronized `research/experiment_protocol.md` (updated Phase D proposal text in subfolder to "FROZEN AND EXECUTED" version).
- Mirrored all newly generated Phase G scripts (`audit_data.py`, `analyze_results.py`, `generate_publication_figures.py`, `verify_reconciliation.py`) and processed artifacts (`deep_metrics.json`) into `AITR_Lab02_MSE2026006/`.

---

## 3. Primary Research Hypothesis Audit ($H_1$)

### Hypothesis Statement
- **Original $H_1$ (Proposed in Phase D):** Intermediate deterministic verification scheduled at dependency-integration milestones (Arm C) will reduce the downstream taint-consumption fraction ($\text{TCF}$) relative to fixed-periodic verification (Arm B) under matched verification budgets:
  $$H_1: \mu_{\text{TCF}, C} < \mu_{\text{TCF}, B} \implies \mu_{\text{TCF}, C} - \mu_{\text{TCF}, B} < 0$$
- **Null Hypothesis ($H_0$):**
  $$H_0: \mu_{\text{TCF}, C} = \mu_{\text{TCF}, B}$$

### Verification of Calculation from Raw Data
The calculation was audited via [`scripts/audit_hypothesis_calculation.py`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/scripts/audit_hypothesis_calculation.py):
1. **Pairing Integrity:** Exactly 1,080 eligible fault scenarios per arm across 90 DAG clusters were confirmed with a 1-to-1 match on `(graph_id, scenario_idx)`.
2. **Formula Integrity:** Every eligible row satisfied $\text{TCF} = \frac{\text{downstream\_taint\_consumed\_count}}{\text{num\_topological\_descendants}}$ with $|\text{Descendants}| \ge 1$.
3. **Cluster-Level Aggregation:**
   - Mean TCF for Arm B (Periodic): **$0.861414$**
   - Mean TCF for Arm C (Milestone): **$0.900503$**
   - Observed Mean Difference ($\Delta \text{TCF} = C - B$): **$+0.039089$ ($+3.91\%$)**
4. **Inferential Tests:**
   - **Two-Sided Paired Permutation Test ($10^4$ sign flips):** $p < 0.0001$ (0 out of $10,000$ resamples exceeded $|+0.0391|$).
   - **95% Bootstrap Confidence Interval ($10^4$ cluster resamples):** $[+0.036619, +0.041414]$. The interval is strictly positive and bounded away from zero.
   - **Paired $t$-Test (Parametric cross-check):** $t = 31.78, p = 2.35 \times 10^{-50}$.
   - **Standardized Effect Size:** Cohen's $d = 3.35$.

### Verdict on $H_1$
**$H_1$ is explicitly contradicted by the empirical data.** Milestone verification does not reduce error propagation; it increases downstream taint consumption by $3.91\%$ relative to periodic scheduling under an identical call budget. Per `AGENTS.md` §3, this finding is reported directly without revision or embellishment.

---

## 4. Verification Budget Fairness Audit

### Budget Allocation vs. Realization
The verification call budget was audited via [`scripts/audit_budget_fairness.py`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/scripts/audit_budget_fairness.py):

| Arm | $K_{\text{alloc}}$ | Realized Calls Distribution | Realized Mean |
|---|---|---|---|
| **Arm A (Final-Only)** | 1 | 1 call: 1,170 episodes (100.0%) | **$1.0000 \pm 0.0000$** |
| **Arm B (Fixed-Periodic)** | 3 | 1 call: 90 eps (7.7%) \| 2 calls: 120 eps (10.3%) \| 3 calls: 960 eps (82.1%) | **$2.7436 \pm 0.5872$** |
| **Arm C (Milestone-Based)** | 3 | 1 call: 90 eps (7.7%) \| 2 calls: 120 eps (10.3%) \| 3 calls: 960 eps (82.1%) | **$2.7436 \pm 0.5872$** |
| **Arm D (Every-Step)** | $H$ | Calls range from 2 to 36 | **$21.0256 \pm 11.0837$** |

### Mechanical Basis of Exact Budget Parity
1. **Identical Slot Counts:** Both Arms B and C allocate exactly 3 check slots *a priori*.
2. **Early Termination Dynamics:**
   - In both Arms B and C, when a check detects a fault, execution immediately halts, triggering rollback.
   - 90 faults were detected at Slot 1 $\implies$ realized calls = 1.
   - 120 faults were detected at Slot 2 $\implies$ realized calls = 2.
   - 150 faults were detected at Slot 3 $\implies$ realized calls = 3.
   - 720 undetected faults + 90 clean runs reached workflow completion $\implies$ realized calls = 3.
   - Total verifier calls: $90 \times 1 + 120 \times 2 + (150 + 810) \times 3 = 3,210$ calls.
   - Grand Mean: $\frac{3,210}{1,170} = 2.743589...$ calls.
3. **Pair-by-Pair Concordance:** On **1,170 out of 1,170 paired episodes (100.0%)**, the realized call count for Arm B and Arm C was identical (difference = 0).
4. **Replay Invariance:** Replay execution disarms the fault and invokes **zero additional verifier calls**, ensuring that rollback does not inflate the verifier budget.

> [!NOTE]
> The identical realized budget mean ($2.7436$) is not a statistical artifact; it reflects structurally identical early-termination slot distributions across the 1,170 scenarios.

---

## 5. Investigation of Identical Detection (33.33%) & Completion (38.46%) Rates

The audit verified why all four methods yielded identical detection and completion rates using [`scripts/audit_detection_and_completion.py`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/scripts/audit_detection_and_completion.py):

### Detection Rate Breakdown (360 / 1,080 = 33.33%)
- **`missing_field` (270 episodes):** Detected in **100.0%** (270/270) of episodes across all four arms. Arm D catches it at step 0; Arm B at slot 1, 2, or 3; Arm C at slot 1, 2, or 3; and Arm A at terminal step $H$. Because Arm A verifies the final artifact against schema rules, it catches the missing field at completion.
- **`type_corruption` (270 episodes):** Detected in **33.33%** (90/270) of episodes across all four arms. The 90 episodes that violate schema assertions are caught at or before step $H$. The remaining 180 undergo lossy type coercion downstream and pass structural checks.
- **`numeric_corruption` (270 episodes):** Detected in **0.0%** (0/270) of episodes across all four arms. Contracts verified schema structure and presence, but not value-level semantic drift.
- **`broken_reference` (270 episodes):** Detected in **0.0%** (0/270) of episodes across all four arms.
- **Total Detected:** $270 + 90 + 0 + 0 = 360$ out of $1,080$ ($33.33\%$).

### Task Completion Rate Breakdown (450 / 1,170 = 38.46%)
- **Clean Controls (90 episodes):** 100.0% completion (90/90) across all arms (0 false alarms).
- **Detected Fault Episodes (360 episodes):** 100.0% completion (360/360) across all arms. Every detected fault triggers rollback to the last verified snapshot. Under the approved single-replay policy, the fault injector is disarmed during replay, allowing the repaired branch to reach successful completion.
- **Undetected Fault Episodes (720 episodes):** 0.0% completion (0/720) across all arms. Because intermediate and terminal checks fail to detect the corruption, no rollback is triggered, and the tainted artifact fails ground-truth final acceptance.
- **Overall Completion:** $\frac{90 + 360}{1,170} = \frac{450}{1,170} = \mathbf{38.46\%}$.

### Scientific Takeaway
Intermediate verification schedules do not alter **whether** a detectable fault is eventually identified or **whether** single-replay recovery succeeds. Rather, intermediate verification differentiates itself through:
1. **Detection Latency:** $2.50$ steps (Every-Step) vs. $5.50$ steps (Periodic) vs. $7.81$ steps (Milestone) vs. $12.17$ steps (Final-Only).
2. **Error Propagation (TCF):** $0.7236$ (Every-Step) vs. $0.8614$ (Periodic) vs. $0.9005$ (Milestone) vs. $1.0000$ (Final-Only).
3. **Re-execution Waste:** Saving up to $3.81$ re-executed nodes per episode during rollback.

---

## 6. Metric Implementations & Mathematical Soundness

The metric calculation code was audited against `research/hypotheses_and_metrics.md`:

| Metric | Source Code Location | Mathematical Formulation | Denominator & Edge-Case Protection | Status |
|---|---|---|---|---|
| **Downstream TCF** | `src/evaluation/evaluator.py:108-122` | $\frac{|\text{TaintedDescendants}|}{|\text{TotalDescendants}|}$ | Excludes clean runs and zero-descendant terminal faults ($N=4,320$ eligible episodes). | **VERIFIED** |
| **Fault Coverage (All)** | `src/evaluation/metrics.py:34-36` | $\frac{\text{DetectedFaults}}{N_{\text{fault}}}$ | $N_{\text{fault}} = 1,080$ per arm; protected against empty sets. | **VERIFIED** |
| **Fault Coverage (Contract)** | `src/evaluation/metrics.py:39-42` | $\frac{\text{DetectedContractFaults}}{N_{\text{contract\_fault}}}$ | $N_{\text{contract}} = 1,080$ per arm. | **VERIFIED** |
| **Detection Delay** | `src/evaluation/evaluator.py:130-140` | $\max(0, t_{\text{detect}} - t_{\text{inject}})$ | Evaluated strictly on detected fault episodes ($N=360$ per arm). | **VERIFIED** |
| **Task Completion** | `src/evaluation/metrics.py:50-54` | $\frac{\text{PassedFinalAcceptance}}{N_{\text{episodes}}}$ | Reported overall, clean, and faulted separately. | **VERIFIED** |
| **False Positive Rate** | `src/evaluation/metrics.py:56-57` | $\frac{\text{FalseAlarmsOnClean}}{N_{\text{clean}}}$ | Evaluated strictly on clean controls ($N=90$ per arm). | **VERIFIED** |
| **Replay Workload** | `src/execution/executor.py:180-195` | Count of node executions during replay pass | Replay nodes tracked distinctly with `_replay` suffixes. | **VERIFIED** |
| **Permutation Test** | `src/evaluation/statistical_analysis.py:12-37` | Sign-flip permutation on graph cluster diffs | $10^4$ resamples; exact two-sided definition. | **VERIFIED** |
| **Bootstrap CI** | `src/evaluation/statistical_analysis.py:40-60` | Percentile bootstrap on graph cluster diffs | $10^4$ resamples; 95% level ($2.5\%$ to $97.5\%$). | **VERIFIED** |

---

## 7. Statistical Reporting & Multiplicity Standards

The following statistical reporting standards are established for the paper manuscript:
1. **P-Value Format:** No $p$-value will be reported as an exact zero ($p = 0.0000$). All extreme permutation test outcomes will be reported as **$p < 0.0001$** or **$p < 10^{-4}$**.
2. **Cluster-Level Aggregation:** All paired tests are conducted at the **$N=90$ graph-cluster level** rather than treating individual episodes as independent, preventing pseudo-replication.
3. **Confidence Intervals:** 95% percentile bootstrap intervals are reported alongside all point estimates ($[+0.0366, +0.0414]$ for TCF difference; $[+1.94, +2.68]$ for delay difference).
4. **Standardized Effect Sizes:** Cohen's $d$ is reported using the standard deviation of paired differences ($d = 3.35$ for TCF; $d = 1.29$ for delay).
5. **Multiplicity Disclosure:** Stratified analyses across horizons, positions, and fault types are exploratory breakdowns contextualizing the pre-registered primary estimand.

---

## 8. Test Suite Quality Audit

The test suite consists of **30 comprehensive unit and integration tests** across 8 test modules:

- `tests/test_comparative_execution.py` (2 tests): Validates 4-arm clean baseline and fault detection under identical graph instances.
- `tests/test_executor.py` (3 tests): Validates execution flow, state snapshotting, single-replay recovery, and operation exception handling.
- `tests/test_fault_injection.py` (5 tests): Validates all 4 fault types and one-shot disarm mechanics.
- `tests/test_logging.py` (2 tests): Validates JSONL schema and privacy separation between public trace and evaluator ground truth.
- `tests/test_metrics_and_evaluator.py` (4 tests): Validates taint propagation, TCF formula, exclusion rules, dual coverage, permutation tests, and bootstrap CIs.
- `tests/test_scheduler.py` (4 tests): Validates slot allocations across $H \in \{12, 24, 36\}$ and asserts exact budget parity between Arms B and C.
- `tests/test_tasks.py` (5 tests): Validates DAG generation, topology constraints, cycle rejection, and unreachable terminal detection.
- `tests/test_verifier.py` (5 tests): Validates schema validation, type checking, numeric range assertions, and clean state passes.

*Execution Verification:* All 30 tests pass in **$0.39$ seconds** on the local Python 3.14.6 environment.

---

## 9. Paper-Readiness & Asset Verification

### Tables Verified Against Raw Dataset
- **Main Results Table (`results/tables/*_main_results.csv`):** Verified bit-for-bit against raw dataset.
- **Horizon Breakdown Table (`results/tables/*_horizon_breakdown.csv`):** Verified across all 12 horizon-arm combinations.

### Figures Verified
All 6 figures in `figures/experiments/` and `figures/analysis/` are verified:
- `fig1_tcf_by_horizon`: Correctly renders TCF across $H \in \{12, 24, 36\}$ with standard error bars.
- `fig2_detection_delay_comparison`: Correctly renders detection delay across Early, Middle, and Late bins.
- `fig3_tradeoff_overhead_vs_propagation`: Correctly positions Arm B and Arm C on the $K=2.74$ vertical budget line.
- `fig4_fault_type_sensitivity`: Correctly breaks down TCF across structural vs. semantic fault types.
- `fig5_paired_contrast_distribution`: Correctly renders the cluster difference distribution with empirical 95% interval.
- `fig6_replay_overhead`: Correctly renders replay nodes executed across arms.

---

## 10. Remaining Limitations & Boundaries

1. **Synthetic Dataflow Workflows:**  
   Tasks are synthetic DAGs executing deterministic data operations (`filter`, `normalize`, `aggregate`, `join`). They isolate the topological effect of scheduling with mathematical precision, but do not model natural-language LLM hallucinations.
2. **No LLM Evaluation:**  
   In compliance with zero-cost project constraints, no LLM API calls were executed. Findings generalize to workflow schedulers, data pipelines, and deterministic agent sub-graphs.
3. **Recovery Policy Simplification:**  
   The recovery model disarms faults during replay. This measures pure rollback and re-execution overhead, but does not capture multi-turn prompt debugging.

---

## 11. Final Audit Classification & Recommendation

```
==================================================================
FINAL AUDIT CLASSIFICATION: READY FOR PHASE H
==================================================================
- Experimental Data:     VERIFIED & COMPLETE (4,680 episodes)
- Primary Hypothesis:    CONTRADICTED & HONESTLY REPORTED (C - B = +0.0391)
- Budget Fairness:       EXACT MATCH CONFIRMED (K = 2.74 calls, p = 1.0000)
- Identical Rates:       ROOT CAUSES MECHANICALLY VERIFIED
- Statistical Standards: ENFORCED (p < 0.0001, Bootstrap CIs, Cohen's d)
- Directory Sync:        100% PARITY (103/103 files SHA-256 match)
- Test Suite:            30/30 PASSING (0.39s)
- Publication Assets:    6 FIGURES & 2 TABLES VERIFIED
==================================================================
```

**Recommendation:** Proceed directly to **Phase H — Reproducibility Package, Artifact Finalization, and Manuscript Preparation**. No experimental reruns are needed.
