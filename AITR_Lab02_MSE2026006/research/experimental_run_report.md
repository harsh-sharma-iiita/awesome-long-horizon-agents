# Experimental Run Report — Phase F (Full Comparative Investigation)

**Date:** 2026-11-04  
**Project:** Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead (G4)  
**Institution:** Indian Institute of Information Technology, Allahabad  
**Student:** Harsh Sharma  
**Status:** PHASE F COMPLETE — EXPERIMENTS EXECUTED AND AUDITED  
**Governing Rule:** `AGENTS.md` (Research Integrity: Genuine Execution Evidence)

---

## 1. Executive Summary

This report documents the experimental investigation of **Research Gap G4 (Intermediate Deterministic Verification Scheduling)**. Four verification scheduling policies were evaluated across controlled multi-step structured-data workflow DAGs:
- **Arm A (Final-Only Verification):** Single terminal acceptance check ($K_{\text{alloc}} = 1$).
- **Arm B (Fixed-Periodic Verification):** Cadence checkpoints at steps $\lceil H/3 \rceil$, $\lceil 2H/3 \rceil$, and $H$ ($K_{\text{alloc}} = 3$).
- **Arm C (Dependency-Milestone Verification):** Checkpoints at the completion of inputs to Join 1, Join 2, and $H$ ($K_{\text{alloc}} = 3$).
- **Arm D (Every-Step Verification):** High-frequency check after every step ($K_{\text{alloc}} = H$).

The entire final campaign of **4,680 episodes** was executed deterministically on the student execution host in **121.52 seconds** (average 25.97 ms per episode), without any fabricated runs or missing data.

---

## 2. Experimental Configuration and Frozen Protocol

All final experimental runs adhered to the frozen Phase D/D.1 protocol:

| Parameter | Specification | Verification Status |
|---|---|---|
| **Campaign Run ID** | `final_exp_20261104_015549_5fcb5a61` | VERIFIED |
| **Horizons Evaluated** | $H \in \{12, 24, 36\}$ execution nodes | VERIFIED |
| **Dependency Motifs** | 3 balanced motifs: Fork-Join, Spine-Join, Hierarchical Reduction | VERIFIED |
| **Final Task Graphs** | 30 graphs per horizon $\times$ 3 horizons = **90 distinct graphs** | VERIFIED |
| **Fault Scenarios per Graph** | 1 Clean Control + 12 Fault Scenarios (4 classes $\times$ 3 positions: early, mid, late) = **13 scenarios** | VERIFIED |
| **Fault Classes** | Missing Field, Type Corruption, Numeric Invariant Violation, Broken Join Reference | VERIFIED |
| **Arms Evaluated** | 4 arms (A: Final-Only, B: Fixed-Periodic, C: Milestone-Based, D: Every-Step) | VERIFIED |
| **Total Final Episodes** | $90 \times 13 \times 4 =$ **4,680 episodes** | VERIFIED |
| **Allocated Call Budget** | Arm A: 1; Arm B: 3; Arm C: 3; Arm D: $H$ | VERIFIED |
| **Budget Parity** | Arm B and Arm C allocated strictly identical budgets ($K_{\text{alloc}} = 3$) | VERIFIED |
| **Recovery Policy** | Restore last verified snapshot, disarm fault injector, replay once with **zero verifier calls** | VERIFIED |
| **Primary Estimand** | Downstream Taint-Consumption Fraction ($\text{TCF}_e$) on eligible episodes ($|\text{Desc}_g(j)| \ge 1$) | VERIFIED |
| **Primary Test** | Nonparametric two-sided paired permutation test on graph-level means ($N=90$ clusters, $\alpha=0.05$) | VERIFIED |

---

## 3. Main Experimental Results

The overall performance metrics across all 4,680 episodes are presented below:

| Verification Arm | Allocated Slots | Realized Calls | Mean TCF (Primary) | Fault Coverage (FDC) | Detection Delay (Nodes) | Task Completion | False Positive Rate | Total Workflow Time | Verifier Time |
|---|---|---|---|---|---|---|---|---|---|
| **Arm A (Final-Only)** | 1 | 1.00 | $1.0000 \pm 0.0000$ | 33.3% | 12.17 | 38.5% | 0.0% | 25.00 ms | 0.102 ms |
| **Arm B (Fixed-Periodic)** | 3 | 2.74 | $0.8614 \pm 0.2893$ | 33.3% | 5.50 | 38.5% | 0.0% | 23.01 ms | 0.185 ms |
| **Arm C (Milestone-Based)** | 3 | 2.74 | $0.9005 \pm 0.2482$ | 33.3% | 7.81 | 38.5% | 0.0% | 23.22 ms | 0.175 ms |
| **Arm D (Every-Step)** | $H$ | 21.03 | $0.7236 \pm 0.4346$ | 33.3% | 2.50 | 38.5% | 0.0% | 28.31 ms | 1.015 ms |

---

## 4. Primary Statistical Contrast: Arm C vs. Arm B

The central research hypothesis tested whether graph-derived dependency milestone verification (Arm C) reduces downstream taint consumption compared to fixed-periodic verification (Arm B) under an identical 3-slot budget:

- **Cluster Unit:** 90 independent task graphs ($N = 90$).
- **Allocated Check Budget:** Exactly 3 slots for both arms ($K_{\text{alloc}} = 3$).
- **Mean Realized Calls:** Exactly 2.74 calls for both arms (paired difference = $0.00$, $p = 1.0000$).
- **Observed Mean TCF Difference ($\Delta \text{TCF} = \text{TCF}_C - \text{TCF}_B$):** `+0.0391` ($+3.91\%$).
- **Two-Sided Permutation Test p-value:** `p = 0.0000` ($p < 0.0001$).
- **95% Bootstrap Confidence Interval:** `[+0.0366, +0.0415]`.
- **Detection Delay Difference ($\Delta \text{Delay}$):** `+2.31 nodes` (95% CI: `[+1.94, +2.68]`, $p < 0.0001$).

### Scientific Interpretation
The null hypothesis $H_0: \mu_{C-B} = 0$ is rejected at $\alpha = 0.05$. However, the directional outcome contradicts the naive mechanistic intuition: **Fixed-Periodic verification (Arm B) achieved significantly lower downstream taint consumption and shorter fault detection delay than Dependency-Milestone verification (Arm C)** under identical budgets.

**Mechanistic Explanation:**
In complex multi-step workflow DAGs, dependency integration boundaries (multi-parent joins) naturally cluster in the middle and later stages of execution as parallel pipelines converge. Consequently, milestone checkpoints occur later in the graph, leaving early branch mutations unmonitored for longer. In contrast, fixed-periodic cadence places an early check at exactly $\lceil H/3 \rceil$, which intercepts early branch corruptions before they integrate into the main pipeline.

---

## 5. Horizon Sensitivity Breakdown

Stratified performance across the three task horizons ($H = 12, 24, 36$):

| Horizon | Verification Arm | Realized Calls | Mean TCF | Fault Coverage | Detection Delay | Task Completion | Workflow Time |
|---|---|---|---|---|---|---|---|
| **$H=12$** | Final Only | 1.00 | 1.0000 | 33.3% | 5.67 | 38.5% | 8.31 ms |
| | Fixed Periodic | 2.74 | 0.8495 | 33.3% | 2.33 | 38.5% | 7.89 ms |
| | Milestone Based | 2.74 | 0.8725 | 33.3% | 2.92 | 38.5% | 7.88 ms |
| | Every Step | 10.56 | 0.7181 | 33.3% | 1.00 | 38.5% | 9.95 ms |
| **$H=24$** | Final Only | 1.00 | 1.0000 | 33.3% | 12.17 | 38.5% | 24.51 ms |
| | Fixed Periodic | 2.74 | 0.8651 | 33.3% | 5.50 | 38.5% | 22.67 ms |
| | Milestone Based | 2.74 | 0.9098 | 33.3% | 7.92 | 38.5% | 22.72 ms |
| | Every Step | 21.03 | 0.7253 | 33.3% | 2.50 | 38.5% | 27.98 ms |
| **$H=36$** | Final Only | 1.00 | 1.0000 | 33.3% | 18.67 | 38.5% | 42.17 ms |
| | Fixed Periodic | 2.74 | 0.8697 | 33.3% | 8.67 | 38.5% | 38.48 ms |
| | Milestone Based | 2.74 | 0.9192 | 33.3% | 12.58 | 38.5% | 39.05 ms |
| | Every Step | 31.49 | 0.7275 | 33.3% | 4.00 | 38.5% | 46.99 ms |

### Key Horizon Insights:
1. **Widening Milestone Deficit:** As horizon length increases from $H=12$ to $H=36$, the delay penalty of milestone verification compounds from $+0.59$ nodes at $H=12$ to $+3.91$ nodes at $H=36$.
2. **Computational Overhead:** Verifier execution time scaled gracefully from 8 ms per episode at $H=12$ to 39 ms at $H=36$. Every-Step verification incurred a $5.8\times$ check overhead increase without improving completion rates.

---

## 6. Artifact and Output Traceability

All experimental artifacts have been preserved in the repository with complete traceability:

- **Raw Episode Dataset:** [`results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv) (1.00 MB, 4,680 rows).
- **Execution Trajectories (Public):** [`runs/trajectories/final_exp_20261104_015549_5fcb5a61_public_trace.jsonl`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/runs/trajectories/final_exp_20261104_015549_5fcb5a61_public_trace.jsonl).
- **Ground-Truth Evaluations:** [`runs/trajectories/final_exp_20261104_015549_5fcb5a61_evaluator_truth.jsonl`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/runs/trajectories/final_exp_20261104_015549_5fcb5a61_evaluator_truth.jsonl).
- **Statistical Contrast Report:** [`results/comparisons/final_exp_20261104_015549_5fcb5a61_primary_contrast.json`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/results/comparisons/final_exp_20261104_015549_5fcb5a61_primary_contrast.json).
- **Main Results Table (Markdown):** [`results/tables/final_exp_20261104_015549_5fcb5a61_main_results.md`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/results/tables/final_exp_20261104_015549_5fcb5a61_main_results.md).
- **Main Results Table (CSV):** [`results/tables/final_exp_20261104_015549_5fcb5a61_main_results.csv`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/results/tables/final_exp_20261104_015549_5fcb5a61_main_results.csv).
- **Horizon Breakdown Table:** [`results/tables/final_exp_20261104_015549_5fcb5a61_horizon_breakdown.md`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/AITR_Lab02_MSE2026006/results/tables/final_exp_20261104_015549_5fcb5a61_horizon_breakdown.md).

---

## 7. Evidence Classification of Findings

| Finding | Classification | Evidence |
|---|---|---|
| Complete 4,680-Episode Dataset | **VERIFIED** | CSV on disk with 4,680 verified rows, run metadata, timestamps. |
| Zero False Alarms on Clean Workflows | **VERIFIED** | Clean FPR = 0.0% across all 4 arms on all 90 task graphs. |
| Budget Equivalence of Arm B & C | **VERIFIED** | Realized calls = 2.74 for both B and C ($p = 1.0000$). |
| Superior Containment of Periodic Baseline | **VERIFIED** | Arm B TCF = 0.8614 vs. Arm C TCF = 0.9005 ($p < 0.0001$, CI $[+0.0366, +0.0415]$). |
| Shorter Detection Latency for Periodic Baseline | **VERIFIED** | Arm B delay = 5.50 vs. Arm C delay = 7.81 ($p < 0.0001$). |
| Extension to Embodied/Language Agents | **UNKNOWN** | Results establish workflow scheduling principles on structured computation DAGs; external transfer to unstructured natural language reasoning remains unverified. |
