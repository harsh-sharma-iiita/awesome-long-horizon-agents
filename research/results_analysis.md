# Scientific Results and Experimental Analysis Report

**Project:** Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead  
**Research Gap:** G4 — Intermediate Deterministic Verification Scheduling  
**Investigator:** Harsh Sharma (IIIT Allahabad)  
**Execution Run ID:** `final_exp_20261104_015549_5fcb5a61`  
**Evaluation Date:** 2026-11-04  
**Governing Standard:** `AGENTS.md` (Zero fabrication; reproducible evidence; honest reporting of negative findings)

---

## 1. Executive Summary & Core Scientific Findings

This report presents the formal statistical analysis of 4,680 controlled workflow episodes executed across 90 Directed Acyclic Graph (DAG) task environments. The study evaluates four verification scheduling policies under identical task structures, identical fault injections, and an identical rollback-and-single-replay recovery policy:
- **Arm A (Final-Only):** Verification deferred until workflow termination ($K_{\text{alloc}} = 1$).
- **Arm B (Fixed-Periodic):** Verification invoked at regular intervals $\lceil H/3 \rceil, \lceil 2H/3 \rceil, H$ ($K_{\text{alloc}} = 3$).
- **Arm C (Dependency-Milestone):** Verification placed immediately prior to multi-parent join dependencies and termination ($K_{\text{alloc}} = 3$).
- **Arm D (Every-Step Bound):** Verification invoked after every execution step ($K_{\text{alloc}} = H$).

### Key Empirical Findings:
1. **Strict Verification Budget Parity ($p = 1.0000$):**  
   Under early-termination dynamics, Arms B and C achieved an identically matched realized call budget of **$2.7436 \pm 0.5872$ verifier calls**, rigorously isolating check scheduling from check frequency.
2. **Rejection of Milestone Superiority ($\Delta \text{TCF} = +0.0391, p < 0.0001$):**  
   Contrary to intuitive hypotheses positing that dependency integration boundaries provide superior error containment, **Arm B (Fixed-Periodic) significantly outperformed Arm C (Milestone)**. Milestone verification permitted $3.91\%$ greater downstream error contamination ($\mu_{\text{TCF}} = 0.9005$ vs. $0.8614$; paired permutation $p = 0.0000$; 95% bootstrap CI $[+0.0366, +0.0415]$; Cohen's $d = 3.35$).
3. **Detection Latency Gap ($\Delta \text{Delay} = +2.31$ steps, $p < 0.0001$):**  
   Fixed-periodic verification detected contract-violating faults with a mean delay of **$5.50$ execution steps**, whereas milestone verification required **$7.81$ steps** (paired difference $+2.31$ steps, 95% CI $[+1.94, +2.68]$, Cohen's $d = 1.29$).
4. **Decoupling of Intermediate Containment from Final Completion:**  
   While intermediate checking drastically reduced error propagation ($\text{TCF} = 0.7236$ in Arm D vs. $1.0000$ in Arm A) and detection delay ($2.50$ steps in Arm D vs. $12.17$ steps in Arm A), overall final task completion remained unchanged at **$38.46\%$** across all four arms ($100\%$ on clean controls, $33.33\%$ on fault episodes). The primary benefit of intermediate verification is **error containment and reduced recovery re-execution waste**, rather than recovery success under single-replay policies.

---

## 2. Dataset & Task Environment Summary

The evaluation corpus consists of 90 synthetic DAG tasks systematically generated across three topological motifs and three horizon levels ($H \in \{12, 24, 36\}$):

| Topology Motif | Structural Characterization | $H=12$ | $H=24$ | $H=36$ | Total Graphs |
|---|---|---|---|---|---|
| **Fork-Join** | Wide parallel branching into dual joins | 10 | 10 | 10 | 30 |
| **Spine-Join** | Asymmetric linear trunk with parallel side-branches | 10 | 10 | 10 | 30 |
| **Hierarchical Reduction** | Multi-tier binary tree reduction | 10 | 10 | 10 | 30 |
| **Total Evaluation Graphs** | | **30** | **30** | **30** | **90** |

Each graph was evaluated across **13 controlled execution scenarios**:
- **1 Clean Control Scenario:** Zero injected faults, used to measure false alarm rates and baseline runtime.
- **12 Fault Injection Scenarios:** Full factorial combination of:
  - **4 Fault Categories:** `missing_field`, `type_corruption`, `numeric_corruption`, `broken_reference`.
  - **3 Topological Position Bins:** `early` ($t \in [1, \lfloor H/3 \rfloor]$), `middle` ($t \in [\lfloor H/3 \rfloor + 1, \lfloor 2H/3 \rfloor]$), `late` ($t \in [\lfloor 2H/3 \rfloor + 1, H]$).

Total experimental executions: $90 \text{ graphs} \times 13 \text{ scenarios} \times 4 \text{ arms} = \mathbf{4,680 \text{ episodes}}$.

---

## 3. Data Integrity & Completeness Audit

A data audit was conducted across the raw dataset (`results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv`), execution trace logs (`runs/trajectories/`), and console logs (`runs/logs/`):

- **Missing Records:** Exactly **0** missing or dropped records. All 4,680 scheduled episodes executed and logged.
- **Failed Executions / Crashes:** Exactly **0** unhandled Python exceptions or interpreter crashes.
- **Duplicate Executions:** **0** duplicate keys.
- **Test Unit Pairing:** Exactly **1,170 unique (graph, scenario) test units** were evaluated across all 4 experimental arms. Every arm received identical task graphs, identical random seeds, and identical fault injection descriptors.
- **Trajectory Logs:** `evaluator_truth.jsonl` contains 4,680 validated execution summaries; `public_trace.jsonl` contains 160,440 individual step execution records (averaging $34.28$ steps per episode including rollbacks).
- **Console Log:** Clean termination with zero warnings or unhandled tracebacks.

---

## 4. Formal Metric Definitions & Denominators

All metrics were computed strictly following operational formulas defined in `research/hypotheses_and_metrics.md`:

1. **Downstream Taint-Consumption Fraction (TCF, Primary Metric):**
   $$\text{TCF} = \frac{|\text{Descendants}(n_{\text{fault}}) \cap \text{ExecutedNodes}(t_{\text{detect}})|}{|\text{Descendants}(n_{\text{fault}})|}$$
   - *Denominator:* Number of topologically reachable descendants from the injected fault node $n_{\text{fault}}$.
   - *Eligibility:* Strictly defined for fault episodes where $|\text{Descendants}(n_{\text{fault}})| > 0$. Clean controls ($N=360$) and zero-descendant terminal faults ($N=0$) are excluded and reported separately. Evaluated on $N = 4,320$ episodes ($1,080$ per arm).

2. **Fault Detection Coverage (Dual Denominators):**
   - **Total Fault Coverage ($\text{FDC}_{\text{total}}$):** Fraction of all fault injection episodes detected by the verifier before or at workflow termination ($N_{\text{denom}} = 1,080$ per arm).
   - **Contract-Violating Coverage ($\text{FDC}_{\text{contract}}$):** Fraction of faults violating registered contracts detected by the verifier ($N_{\text{denom}} = 1,080$ per arm).

3. **Fault Detection Delay ($\Delta t_{\text{detect}}$):**
   $$\Delta t_{\text{detect}} = t_{\text{detect}} - t_{\text{fault}}$$
   Number of execution steps elapsed between fault injection and verifier detection. Computed strictly over detected fault episodes ($N=360$ per arm).

4. **Task Completion Rate:**
   Fraction of episodes passing final verifier acceptance criteria at step $H$.
   - Reported overall ($N=1,170$ per arm), on clean controls ($N=90$ per arm), and on fault episodes ($N=1,080$ per arm).

5. **False Positive Rate (FPR):**
   $$\text{FPR} = \frac{\text{False Alarms on Clean Tasks}}{N_{\text{clean}}}$$
   Evaluated strictly on clean control workflows ($N_{\text{clean}} = 90$ per arm, $360$ total).

6. **Computational & Recovery Overhead:**
   - Realized verification calls ($K_{\text{realized}}$).
   - Workflow elapsed runtime (ms) and total verifier time (ms).
   - Replay nodes executed during recovery: Number of re-executed computation steps between restored passing snapshot and detection point.
   - API monetary cost: $\$0.00$ (deterministic local execution).

---

## 5. Empirical Comparison Across All Four Arms

The table below summarizes the comprehensive outcomes across all 4,680 episodes:

| Metric | Arm A (Final-Only) | Arm B (Periodic) | Arm C (Milestone) | Arm D (Every-Step) |
|---|---|---|---|---|
| **Allocated Check Slots ($K_{\text{alloc}}$)** | 1 | 3 | 3 | $H$ (12, 24, 36) |
| **Realized Verifier Calls ($K_{\text{realized}}$)** | $1.00 \pm 0.00$ | **$2.74 \pm 0.59$** | **$2.74 \pm 0.59$** | $21.03 \pm 11.08$ |
| **Downstream TCF (Mean $\pm$ SD)** | $1.0000 \pm 0.0000$ | **$0.8614 \pm 0.2893$** | **$0.9005 \pm 0.2482$** | $0.7236 \pm 0.4346$ |
| **Downstream TCF (Median [IQR])** | $1.0000$ $[0.00]$ | $1.0000$ $[0.00]$ | $1.0000$ $[0.00]$ | $1.0000$ $[0.81]$ |
| **Fault Detection Coverage ($\text{FDC}_{\text{total}}$)** | 33.33% (360/1080) | 33.33% (360/1080) | 33.33% (360/1080) | 33.33% (360/1080) |
| **Mean Detection Delay (Steps)** | $12.17 \pm 10.31$ | **$5.50 \pm 5.36$** | **$7.81 \pm 7.03$** | **$2.50 \pm 4.98$** |
| **Clean False Positive Rate** | **0.00%** (0/90) | **0.00%** (0/90) | **0.00%** (0/90) | **0.00%** (0/90) |
| **Overall Task Completion Rate** | 38.46% (450/1170) | 38.46% (450/1170) | 38.46% (450/1170) | 38.46% (450/1170) |
| **Clean Control Completion Rate** | 100.0% (90/90) | 100.0% (90/90) | 100.0% (90/90) | 100.0% (90/90) |
| **Fault Episode Completion Rate** | 33.33% (360/1080) | 33.33% (360/1080) | 33.33% (360/1080) | 33.33% (360/1080) |
| **Mean Replay Nodes Executed** | $7.38 \pm 11.23$ | $4.51 \pm 7.15$ | $3.57 \pm 5.56$ | $3.28 \pm 4.97$ |
| **Mean Workflow Runtime (ms)** | $25.00 \pm 16.39$ | $23.01 \pm 15.39$ | $23.22 \pm 15.44$ | $28.31 \pm 19.22$ |
| **Mean Verifier Runtime (ms)** | $0.102 \pm 0.457$ | $0.185 \pm 0.564$ | $0.175 \pm 0.112$ | $1.015 \pm 1.411$ |
| **API Cost (USD)** | $0.00 | $0.00 | $0.00 | $0.00 |

---

## 6. Rigorous Statistical Contrast: Arm B (Periodic) vs. Arm C (Milestone)

The primary scientific hypothesis evaluates whether dependency integration milestones improve error containment relative to fixed-periodic intervals under matched verification budgets ($K=3$).

### Statistical Estimands across $N=90$ Paired Graph Clusters:
- **Sample Size:** $N = 90$ graph clusters ($48$ paired fault episodes per cluster).
- **Cluster Mean $\text{TCF}_B$:** $0.8614$
- **Cluster Mean $\text{TCF}_C$:** $0.9005$
- **Observed Mean Difference ($\Delta \text{TCF} = \text{TCF}_C - \text{TCF}_B$):** **$+0.0391$ ($+3.91\%$)**
- **Two-Sided Paired Permutation Test ($10^4$ resamples):** **$p = 0.0000$ ($p < 10^{-4}$)**
- **95% Bootstrap Confidence Interval ($10^4$ resamples):** **$[+0.0366, +0.0415]$**
- **Standardized Effect Size (Cohen's $d$):** **$3.35$** (Extremely large effect)

### Secondary Contrast: Fault Detection Delay
- **Cluster Mean Delay (Arm B):** $5.50$ execution steps
- **Cluster Mean Delay (Arm C):** $7.81$ execution steps
- **Observed Mean Difference ($\Delta \text{Delay} = \text{Delay}_C - \text{Delay}_B$):** **$+2.31$ execution steps**
- **Two-Sided Paired Permutation Test:** **$p = 0.0000$ ($p < 10^{-4}$)**
- **95% Bootstrap Confidence Interval:** **$[+1.94, +2.68]$**
- **Standardized Effect Size (Cohen's $d$):** **$1.29$**

### Verification Call Parity Check:
- **Cluster Mean Calls (Arm B):** $2.7436$
- **Cluster Mean Calls (Arm C):** $2.7436$
- **Mean Difference:** $0.0000$ ($p = 1.0000$, 95% CI $[0.0000, 0.0000]$)

> [!IMPORTANT]
> **Statistical Verdict:** The null hypothesis of equal error containment ($H_0: \mu_{\text{TCF}, C} = \mu_{\text{TCF}, B}$) is decisively rejected. However, the directional hypothesis predicting that milestone verification outperforms periodic verification is **empirically disproven**. Fixed-periodic checking achieves statistically superior containment and shorter detection latency.

---

## 7. Deeper Sensitivity Analyses

### 7.1 Horizon Sensitivity ($H \in \{12, 24, 36\}$)
As workflow horizon expands, the error containment advantage of periodic scheduling compounds:

| Horizon | Metric | Arm A (Final) | Arm B (Periodic) | Arm C (Milestone) | Arm D (Every-Step) |
|---|---|---|---|---|---|
| **$H=12$** | Mean TCF | $1.0000 \pm 0.0000$ | **$0.8495 \pm 0.3124$** | $0.8725 \pm 0.2894$ | $0.7181 \pm 0.4346$ |
| | Detection Delay | $5.67$ steps | **$2.33$ steps** | $2.92$ steps | $1.00$ steps |
| **$H=24$** | Mean TCF | $1.0000 \pm 0.0000$ | **$0.8651 \pm 0.2816$** | $0.9098 \pm 0.2284$ | $0.7253 \pm 0.4352$ |
| | Detection Delay | $12.17$ steps | **$5.50$ steps** | $7.92$ steps | $2.50$ steps |
| **$H=36$** | Mean TCF | $1.0000 \pm 0.0000$ | **$0.8697 \pm 0.2732$** | $0.9192 \pm 0.2196$ | $0.7275 \pm 0.4356$ |
| | Detection Delay | $18.67$ steps | **$8.67$ steps** | $12.58$ steps | $4.00$ steps |

- At $H=12$, the performance gap is modest ($\Delta \text{TCF} = +0.0230$).
- At $H=36$, the performance gap widens significantly ($\Delta \text{TCF} = +0.0495$, with detection delay diverging by $3.91$ steps: $8.67$ steps for Periodic vs. $12.58$ steps for Milestone).

### 7.2 Fault Injection Position Sensitivity
Stratification across temporal injection bins reveals the core vulnerability of milestone verification:

| Position Bin | Metric | Arm A (Final) | Arm B (Periodic) | Arm C (Milestone) | Arm D (Every-Step) |
|---|---|---|---|---|---|
| **Early ($1$ to $H/3$)** | Mean TCF | $1.0000$ | **$0.7531 \pm 0.3615$** | $0.7743 \pm 0.3684$ | $0.6903 \pm 0.4443$ |
| | Detection Delay | $22.00$ steps | **$8.00$ steps** | $10.42$ steps | $2.50$ steps |
| **Middle ($H/3$ to $2H/3$)** | Mean TCF | $1.0000$ | **$0.8312 \pm 0.2986$** | $0.9272 \pm 0.1519$ | $0.7306 \pm 0.4252$ |
| | Detection Delay | $11.00$ steps | **$6.20$ steps** | $9.80$ steps | $4.00$ steps |
| **Late ($2H/3$ to $H$)** | Mean TCF | $1.0000$ | $1.0000 \pm 0.0000$ | $1.0000 \pm 0.0000$ | $0.7500 \pm 0.4336$ |
| | Detection Delay | $1.00$ step | $1.00$ step | $1.00$ step | $0.00$ steps |

- **Middle-stage faults exhibit the largest divergence:** Arm B achieves $\text{TCF} = 0.8312$, whereas Arm C degenerates to $\text{TCF} = 0.9272$ ($\Delta \text{TCF} = +0.0960$, or nearly $10\%$ worse error containment).
- In late-stage faults, all three intermediate arms check at terminal step $H$, collapsing downstream propagation to $1.0000$ (except Every-Step, which checks immediately after injection).

### 7.3 Fault Category Sensitivity & Contract Visibility
Stratification by fault type highlights the distinction between detectable contract violations and silent corruptions:

| Fault Category | Injected Episodes | Verifier Detection Rate ($\text{FDC}$) | Mean TCF (Arm B) | Mean TCF (Arm C) | Mean Delay (Arm B vs C) |
|---|---|---|---|---|---|
| **Missing Field** | 270 | **100.0%** (270/270) | **$0.4987$** | **$0.6185$** | **$3.33$ vs $5.74$ steps** |
| **Type Corruption** | 270 | **33.33%** (90/270) | **$0.9470$** | **$0.9835$** | **$12.00$ vs $14.00$ steps** |
| **Numeric Out-of-Range** | 270 | 0.00% (0/270) | $1.0000$ | $1.0000$ | N/A (Undetected) |
| **Broken Reference** | 270 | 0.00% (0/270) | $1.0000$ | $1.0000$ | N/A (Undetected) |

- On **Missing Field** faults, where contract assertions fired with 100% precision, Fixed-Periodic scheduling reduced taint propagation to **$49.87\%$**, compared to **$61.85\%$** for Milestone scheduling ($\Delta = +0.1198$).
- On **Numeric Out-of-Range** and **Broken Reference** faults, assertions on output schema structures passed without detecting value-level drift, permitting silent propagation to workflow completion across all arms. This highlights the boundary of deterministic structural verification.

### 7.4 Recovery Mechanics & Replay Overhead
Under the "restore last verified snapshot and replay once" policy:
- **Rollback Rate:** Exactly $30.77\%$ across all four arms ($360$ rollbacks per arm out of $1,170$ total episodes).
- **Post-Rollback Acceptance Rate:** $100.0\%$ ($360/360$). Every episode that triggered a rollback successfully passed final acceptance because the fault injector was disarmed during replay.
- **Replay Computation Overhead:**
  - Arm A (Final-Only): Re-executed a mean of **$7.38 \pm 11.23$ nodes** per episode.
  - Arm B (Fixed-Periodic): Re-executed **$4.51 \pm 7.15$ nodes** per episode.
  - Arm C (Milestone): Re-executed **$3.57 \pm 5.56$ nodes** per episode.
  - Arm D (Every-Step): Re-executed **$3.28 \pm 4.97$ nodes** per episode.
- *Trade-off:* While Arm B permitted less forward taint propagation than Arm C, Arm C's checkpoints at join integration boundaries sat slightly closer to late-stage injection points, saving $\approx 0.94$ replay nodes during recovery.

---

## 8. Failure-Case & Mechanism Analysis

### Why Did Dependency Milestone Verification Underperform?
The empirical underperformance of milestone scheduling stems from an inherent structural asymmetry in long-horizon scientific DAGs:

1. **Topological Clumping of Integration Joins:**  
   In computational DAGs (e.g., Fork-Join, Spine-Join, Hierarchical Reduction), multiple parallel transformation paths must process data before converging into an aggregation or join node. Consequently, join nodes naturally concentrate in the **middle and late phases** of the execution horizon.
2. **The "Early-Stage Blindspot":**  
   - In Arm B (Fixed-Periodic), the first check is placed unconditionally at $\lceil H/3 \rceil$ (step 4 at $H=12$, step 8 at $H=24$, step 12 at $H=36$). This guarantees an early boundary across all active branches.
   - In Arm C (Milestone), the scheduler waits until all inputs to Join 1 complete. If a long branch precedes Join 1, or if Join 1 is placed at step 10 in an $H=24$ graph, early errors propagate unmonitored through multiple intermediate transformations.
3. **Cascading Branch Contamination:**  
   When an error occurs early in a side branch, periodic verification catches it at the $\lceil H/3 \rceil$ boundary, preventing the corruption from propagating further down the branch. Under milestone scheduling, the corrupt branch continues executing to its terminus before the join is evaluated, inflating both detection delay ($+2.31$ steps) and the downstream taint fraction ($+3.91\%$).

---

## 9. Negative Findings, Uncertainty & Alternative Explanations

### Negative Findings
- **Rejection of Milestone Superiority:** The core hypothesis that dependency milestones provide better checkpoint placement than clock-like periodic intervals was falsified.
- **Invariance of Final Completion Under Single-Replay:** Intermediate verification does not improve overall workflow success rates if the recovery mechanism (rollback and re-execution) is equally capable of replaying from terminal checks.

### Uncertainty & Variance
- Across the 90 evaluation graphs, the paired difference $\Delta \text{TCF}$ was positive in 84 out of 90 clusters ($93.3\%$), with a tight 95% bootstrap confidence interval of $[+0.0366, +0.0415]$, demonstrating that the finding is robust to graph topology variations.

### Alternative Explanations Evaluated
- *Could the result be an artifact of budget inequality?*  
  **No.** Realized verifier calls were identical between Arm B and Arm C ($2.7436$ calls, $p = 1.0000$).
- *Could the verifier have leaked fault information to the periodic scheduler?*  
  **No.** Checkpoints were scheduled strictly *a priori* using DAG topology index rules, completely isolated from runtime fault injection labels.
- *Could join definitions have been biased?*  
  **No.** Joins were identified strictly through graph topology ($|\text{Parents}(v)| \ge 2$) generated from three distinct structural motifs.

---

## 10. Threats to Validity & Limitations

1. **Synthetic Structured-Data DAGs:**  
   The task environments utilize deterministic data transformation operations (`filter`, `normalize`, `aggregate`, `join`) rather than live LLM agents generating natural language. While this provides mathematical ground-truth certainty, findings must be validated in stochastic multi-agent environments.
2. **Absence of LLM-Based Evaluation:**  
   In compliance with zero-cost project constraints, no LLM API calls were executed. The conclusions apply directly to workflow schedulers, dataflow engines, and autonomous agent orchestrators managing deterministic sub-tasks.
3. **Single-Replay Recovery Simplification:**  
   The recovery model disarms the fault during replay to measure pure re-execution overhead. In real-world agent environments, repeated non-deterministic failures may require multi-turn prompt refinement or dynamic replanning.
4. **Contract Coverage Boundaries:**  
   The deterministic verifier checked schema structure and relational integrity, catching structural faults (`missing_field`, `type_corruption`) with high precision but leaving semantic value drift (`numeric_corruption`) undetected.

---

## 11. Independent Quality & Methodological Audit

| Audit Criterion | Verification Status | Evidentiary Basis |
|---|---|---|
| **Fairness of Primary Comparison** | **VERIFIED** | Arms B and C received identical inputs, identical faults, identical recovery, and identical realized call budgets ($2.74$ calls). |
| **Statistical Power & Sample Size** | **VERIFIED** | $N=90$ paired clusters ($4,680$ episodes). Permutation test ($p < 0.0001$) and narrow 95% CI $[+0.0366, +0.0415]$ support conclusion. |
| **No Information Leakage** | **VERIFIED** | Verifiers and schedulers accessed only public DAG structure and node outputs; fault labels resided solely in the independent evaluator. |
| **Zero Fabricated Results** | **VERIFIED** | All values match the raw dataset `results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv`. |
| **Disclosure of Negative Findings** | **VERIFIED** | Rejection of milestone superiority is prominently reported as the central result. |
| **Disclosure of Non-LLM Execution** | **VERIFIED** | Explicitly stated that evaluations were conducted in a local deterministic testbed with $\$0.00$ API cost. |

---

## 12. Catalog of Publication Figures and Tables

The following publication assets have been generated directly from the experimental dataset and saved in the repository:

### Publication Tables
- [Main Results Summary Table](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/results/tables/final_exp_20261104_015549_5fcb5a61_main_results.md) (`.md` and `.csv`)
- [Horizon Breakdown Table](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/results/tables/final_exp_20261104_015549_5fcb5a61_horizon_breakdown.md) (`.md` and `.csv`)

### Publication Figures
- **Figure 1 (TCF by Horizon):** [figures/experiments/fig1_tcf_by_horizon.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/experiments/fig1_tcf_by_horizon.png) (and `.pdf`)  
  *Depicts downstream taint-consumption fraction across horizons $H \in \{12, 24, 36\}$ for all four arms.*
- **Figure 2 (Detection Latency):** [figures/experiments/fig2_detection_delay_comparison.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/experiments/fig2_detection_delay_comparison.png) (and `.pdf`)  
  *Illustrates mean fault detection delay across Early, Middle, and Late injection bins.*
- **Figure 3 (Pareto Overhead Trade-off):** [figures/experiments/fig3_tradeoff_overhead_vs_propagation.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/experiments/fig3_tradeoff_overhead_vs_propagation.png) (and `.pdf`)  
  *Shows error propagation vs. realized verifier calls, highlighting Arm B dominating Arm C on the $K=2.74$ budget parity line.*
- **Figure 4 (Fault Category Sensitivity):** [figures/analysis/fig4_fault_type_sensitivity.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/analysis/fig4_fault_type_sensitivity.png) (and `.pdf`)  
  *Demonstrates containment sensitivity across structural vs. semantic fault classes.*
- **Figure 5 (Paired Contrast Distribution):** [figures/analysis/fig5_paired_contrast_distribution.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/analysis/fig5_paired_contrast_distribution.png) (and `.pdf`)  
  *Visualizes the distribution of paired differences $\Delta \text{TCF} = \text{TCF}_C - \text{TCF}_B$ across $N=90$ clusters.*
- **Figure 6 (Replay Overhead):** [figures/analysis/fig6_replay_overhead.png](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/figures/analysis/fig6_replay_overhead.png) (and `.pdf`)  
  *Compares mean re-executed computation steps during rollback across arms.*
