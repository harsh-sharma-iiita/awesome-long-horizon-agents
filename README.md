# Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead

**Author:** Harsh Sharma  
**Institution:** Indian Institute of Information Technology (IIIT), Allahabad  
**Research Topic:** Planning-Quality Degradation in Long-Horizon Autonomous Research Agents  
**Investigated Research Gap:** G4 — Intermediate Deterministic Verification Scheduling  
**Evaluation Run ID:** `final_exp_20261104_015549_5fcb5a61` (4,680 episodes across 90 DAG task clusters)  
**Status:** **PHASE I — FINAL POSTGRADUATE RESEARCH SUBMISSION (VERIFIED COMPLETE)**

---

## 1. Executive Summary & Core Scientific Findings

When autonomous language agents execute multi-step workflows across software engineering, scientific modeling, or data analysis, planning degradation and compounding errors frequently lead to uncontained failure cascades. While intermediate verification and rollback recovery can intercept errors before trajectory completion, verification calls incur significant computational and latency overhead. Under realistic constraints where an orchestrator operates with a scarce verification budget ($K \ll H$), the central architectural question is: **where should verification checkpoints be placed?**

This project presents the first controlled, budget-matched empirical investigation comparing two prominent scheduling paradigms:
- **Arm B (Fixed-Periodic Baseline):** Uniformly spaced temporal intervals ($\lceil H/3 \rceil, \lceil 2H/3 \rceil, H$) with allocated budget $K_{\text{alloc}} = 3$.
- **Arm C (Dependency-Milestone Intervention):** Graph-derived synchronization boundaries placed immediately prior to multi-parent join operations and termination with allocated budget $K_{\text{alloc}} = 3$.
- **Reference Baselines:** Arm A (Final-Only, $K_{\text{alloc}}=1$) and Arm D (Every-Step Upper Bound, $K_{\text{alloc}}=H$).

### Key Empirical Findings:
1. **Strict Verification Budget Parity ($p = 1.0000$):**  
   Under runtime early termination, Arms B and C achieved an identical realized mean of **$2.7436 \pm 0.5872$ verifier calls**, confirmed by an exact 100% pairwise call match across all 1,170 evaluation units.
2. **Rejection of Milestone Superiority ($\Delta \text{TCF} = +0.0391, p < 0.0001$):**  
   Contrary to prevailing intuition in agent literature, milestone verification performed worse on downstream error containment, permitting $3.91\%$ greater downstream taint propagation ($\mu_{\text{TCF}} = 0.9005$ vs. $0.8614$; two-sided paired permutation $p < 0.0001$; 95% bootstrap CI $[+0.0366, +0.0414]$; Cohen's $d = 3.35$).
3. **Detection Latency Advantage:**  
   Fixed-periodic verification caught contract-violating faults $2.31$ steps earlier than milestone verification ($5.50$ vs. $7.81$ steps, $p < 0.0001$).
4. **The Structural Clumping Phenomenon:**  
   In computational DAGs, parallel branches must finish transformations before joining, causing dependency integration milestones to naturally cluster in middle and late workflow stages. Periodic checking enforces an early temporal boundary at $\lceil H/3 \rceil$, catching early branch corruptions before they integrate.
5. **Containment vs. Completion Decoupling:**  
   Under single-replay recovery with fault disarming, task completion was identical across all arms ($38.46\%$), but periodic verification reduced recovery re-execution waste by $38.9\%$ relative to final-only verification, saving an average of $2.87$ re-executed nodes per episode.

---

## 2. Repository Structure

```text
├── paper/                       # Complete second research paper package
│   ├── main.tex                 # Master two-column IEEE/ACM-style LaTeX document
│   ├── references.bib           # 15 verified primary bibliography citations
│   ├── sections/                # 10 modular LaTeX sections (Abstract to Conclusion)
│   ├── figures/                 # Embedded publication figures (vector PDF and 300 DPI PNG)
│   ├── technical_review.md      # Demanding technical peer review report (Rating: 9/10)
│   ├── paper_compiled_preview.pdf # Fully compiled 8-page companion research paper PDF
│   └── README.md                # Paper package overview and compilation instructions
├── research/                    # Approved research briefs, protocols, decisions, and reports
│   ├── research_brief.md        # Gate 1 One-Page Research Brief
│   ├── hypotheses_and_metrics.md# Formal metric definitions and statistical testing plan
│   ├── experiment_protocol.md   # Frozen experimental protocol across four arms
│   ├── baseline_validation.md   # Phase E Baseline Validation Report (28 tests, 65 dev episodes)
│   ├── experimental_run_report.md# Phase F Experimental Run Report (4,680 episodes)
│   ├── results_analysis.md      # Phase G Deep Scientific Results & Sensitivity Analysis
│   ├── final_evidence_audit.md  # Phase G.1 Comprehensive Evidence & Reproducibility Audit
│   ├── human_decisions.md       # Chronological log of human-approved research decisions (D001–D011)
│   └── research_decisions.md    # Evidence register and historical decision tracking
├── results/                     # Quantitative experimental outputs
│   ├── raw/                     # Raw CSV dataset (final_exp_*_all_episodes.csv, 4,680 rows, 1.0 MB)
│   ├── processed/               # Stratified JSON metrics (by horizon, position, fault type, and deep metrics)
│   ├── tables/                  # Formatted Markdown and CSV publication tables
│   └── comparisons/             # Primary statistical contrast JSON (p-value, bootstrap CI, Cohen's d)
├── figures/                     # Generated publication-quality figures
│   ├── experiments/             # fig1 (TCF by Horizon), fig2 (Detection Delay), fig3 (Pareto Trade-off)
│   └── analysis/                # fig4 (Fault Type Sensitivity), fig5 (Paired Contrast), fig6 (Replay Overhead)
├── runs/                        # Complete execution logs and trajectories
│   ├── configurations/          # Pinned JSON run configuration files
│   ├── logs/                    # Timestamped execution console logs
│   └── trajectories/            # public_trace.jsonl (160,440 steps) and evaluator_truth.jsonl (4,680 summaries)
├── src/                         # Modular Python implementation source code
│   ├── tasks/                   # TaskGraph, TaskGenerator, TaskValidator (Fork-Join, Spine-Join, Reduction)
│   ├── execution/               # WorkflowExecutor, FaultInjector, FaultDescriptor (one-shot rollback recovery)
│   ├── verification/            # DeterministicVerifier, VerificationResult (schema, type, range, reference contracts)
│   ├── schedulers/              # FinalOnlyScheduler, FixedPeriodicScheduler, MilestoneScheduler, EveryStepScheduler
│   ├── evaluation/              # IndependentEvaluator, MetricCalculator, StatisticalAnalysis
│   └── utils/                   # JSONL logging, seed controls, reproducibility utilities
├── tests/                       # Comprehensive verification test suite (30 tests, 100% passing)
├── scripts/                     # Executable reproduction and audit scripts
│   ├── check_environment.py     # Host hardware, OS, and Python diagnostic
│   ├── run_baseline_pilot.py    # Phase E baseline pilot runner
│   ├── run_comparative_pilot.py # Phase F 4-arm comparative pilot runner (260 episodes)
│   ├── run_final_experiments.py # Phase F 4,680-episode full experimental campaign runner
│   ├── analyze_results.py       # Phase G deep statistical analysis and metric aggregation
│   ├── generate_publication_figures.py # Phase G publication figure generator
│   ├── compile_paper_pdf.py     # Phase H companion PDF compiler
│   ├── audit_data.py            # Phase G data integrity audit
│   ├── audit_hypothesis_calculation.py # Phase G.1 H1 recalculation audit
│   ├── audit_budget_fairness.py # Phase G.1 budget parity audit
│   ├── audit_detection_and_completion.py # Phase G.1 mechanical root-cause audit
│   ├── audit_paper_readiness.py # Phase G.1 table and figure verification audit
│   └── verify_reconciliation.py # Phase G.1 / I two-way directory hash reconciliation
├── demo/                        # Five-minute presentation script and viva preparation
│   └── demo_plan.md             # Timed 0:00–5:00 oral presentation script and 5 technical viva Q&As
├── docs/                        # Assignment checklists and submission documentation
│   └── final_submission_checklist.md # 13-point master deliverables verification matrix
├── ai_logs/                     # Genuine human-AI collaboration documentation
│   ├── ai_assistance_log.md     # Chronological log of AI tasks, human decisions, and verified outcomes
│   ├── prompt_history.md        # Prompt Studio prompts and scaffolding records
│   └── debugging_log.md         # Genuine debugging entries (join false alarm, aggregate key pass-through)
├── requirements.txt             # Minimal pinned dependencies (numpy, scipy, networkx, pytest, matplotlib, reportlab)
└── AGENTS.md                    # Research assignment governing rules and integrity standard
```

---

## 3. Quick Start & Reproducibility Guide

### Step 1: Environment Setup
Clone the repository and activate a Python 3.14 virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify the environment diagnostic:
```powershell
python scripts/check_environment.py
```
*Expected: 8-core CPU, >= 8 GB RAM, Windows 11, Python 3.14+, 0 GPU/API requirement.*

---

### Step 2: Run Verification Test Suite
Execute the 30-test unit and integration suite:
```powershell
python -m pytest -v tests/
```
*Expected: 30 passed in ~0.45s.*

---

### Step 3: Run Comparative 4-Arm Pilot
Execute the pre-evaluation comparative pilot across 20 development workflows (260 episodes):
```powershell
python scripts/run_comparative_pilot.py
```
*Expected: Executes in ~1.5s. Achieves 0.00% false alarms on clean controls and demonstrates intermediate detection.*

---

### Step 4: Inspect or Re-Run the Final Experimental Campaign
The repository includes the full, authentic 4,680-episode evaluation dataset in `results/raw/final_exp_20261104_015549_5fcb5a61_all_episodes.csv`.

To re-run the complete factorial experiment from scratch (90 graphs × 13 scenarios × 4 arms):
```powershell
python scripts/run_final_experiments.py
```
*Runtime: ~120 seconds on an 8-core CPU.*

---

### Step 5: Regenerate Metrics, Tables, and Figures
Run the deep statistical analysis and figure generation scripts:
```powershell
# 1. Compute stratified metrics and paired contrast
python scripts/analyze_results.py

# 2. Render all 6 publication figures (PNG and PDF)
python scripts/generate_publication_figures.py

# 3. Compile the companion research paper PDF
python scripts/compile_paper_pdf.py
```

---

### Step 6: Verify Data Integrity and Reproducibility
Execute the independent evidence and budget audits:
```powershell
python scripts/audit_data.py
python scripts/audit_hypothesis_calculation.py
python scripts/audit_budget_fairness.py
python scripts/audit_detection_and_completion.py
python scripts/audit_paper_readiness.py
python scripts/verify_reconciliation.py
```
*Expected: 100% checks pass, 0 discrepancies, 123/123 files SHA-256 match.*

---

## 4. Verified Execution Command Matrix

| Command | Purpose | Verification Status | Observed Execution Runtime |
|---|---|---|---|
| `python scripts/check_environment.py` | Host hardware & Python diagnostic | **VERIFIED TESTED** | 0.08s |
| `python -m pytest -v tests/` | Full 30-test verification suite | **VERIFIED TESTED** | 0.45s (30/30 passed) |
| `python scripts/run_baseline_pilot.py` | Phase E baseline development pilot (65 eps) | **VERIFIED TESTED** | 0.39s |
| `python scripts/run_comparative_pilot.py` | Phase F 4-arm comparative pilot (260 eps) | **VERIFIED TESTED** | 1.54s |
| `python scripts/run_final_experiments.py` | Full final campaign (4,680 eps, 90 graphs) | **VERIFIED TESTED** | 121.52s |
| `python scripts/analyze_results.py` | Deep metrics & cluster statistical contrast | **VERIFIED TESTED** | 0.35s |
| `python scripts/generate_publication_figures.py` | Render 6 publication figures (PNG/PDF) | **VERIFIED TESTED** | 4.82s |
| `python scripts/compile_paper_pdf.py` | Compile companion academic paper PDF | **VERIFIED TESTED** | 1.25s |
| `python scripts/audit_data.py` | Data completeness & identifier audit | **VERIFIED TESTED** | 0.22s |
| `python scripts/audit_hypothesis_calculation.py` | Recalculate H1 permutation & bootstrap tests | **VERIFIED TESTED** | 0.31s |
| `python scripts/audit_budget_fairness.py` | Exact pairwise realized call budget audit | **VERIFIED TESTED** | 0.18s |
| `python scripts/audit_detection_and_completion.py` | Root-cause audit of detection & completion | **VERIFIED TESTED** | 0.19s |
| `python scripts/audit_paper_readiness.py` | Table & figure cross-verification audit | **VERIFIED TESTED** | 0.20s |
| `python scripts/verify_reconciliation.py` | SHA-256 two-way directory reconciliation | **VERIFIED TESTED** | 0.25s (123/123 match) |

*Untested Commands:* **None.** Every single execution, analysis, audit, and plotting command listed above has been executed and verified in the active project environment.

---

## 5. Main Results Summary Table

| Arm | $K_{\text{alloc}}$ | $K_{\text{realized}}$ | Mean TCF (Primary) $\downarrow$ | FDC$_{\text{total}}$ | Detection Delay $\downarrow$ | Task Completion | False Alarm Rate | Replay Nodes |
|---|---|---|---|---|---|---|---|---|
| **Arm A (Final-Only)** | 1 | $1.00 \pm 0.00$ | $1.0000 \pm 0.0000$ | 33.33\% | $12.17 \pm 10.31$ | 38.46\% | **0.00\%** | $7.38 \pm 11.23$ |
| **Arm B (Fixed-Periodic)** | 3 | **$2.74 \pm 0.59$** | **$0.8614 \pm 0.2893$** | 33.33\% | **$5.50 \pm 5.36$** | 38.46\% | **0.00\%** | $4.51 \pm 7.15$ |
| **Arm C (Milestone-Based)** | 3 | **$2.74 \pm 0.59$** | $0.9005 \pm 0.2482$ | 33.33\% | $7.81 \pm 7.03$ | 38.46\% | **0.00\%** | $3.57 \pm 5.56$ |
| **Arm D (Every-Step Bound)** | $H$ | $21.03 \pm 11.08$ | $0.7236 \pm 0.4346$ | 33.33\% | $2.50 \pm 4.98$ | 38.46\% | **0.00\%** | $3.28 \pm 4.97$ |

### Primary Contrast Statistics (Arm C vs. Arm B, $N=90$ Graph Clusters):
- **Mean TCF Difference ($\Delta \text{TCF} = C - B$):** **$+0.0391$ ($+3.91\%$)**
- **Two-Sided Paired Permutation Test ($10^4$ resamples):** **$p < 0.0001$**
- **95% Bootstrap Confidence Interval:** **$[+0.0366, +0.0414]$**
- **Paired $t$-Test:** $t = 31.78, p = 2.35 \times 10^{-50}$ (Cohen's $d = 3.35$)
- **Fault Detection Delay Difference:** **$+2.31$ execution steps** ($p < 0.0001$, 95% CI $[+1.94, +2.68]$)

---

## 6. AI Collaboration & Research Integrity Statement

In accordance with Section 11 of `AGENTS.md`, AI assistance was used as an interactive research software engineering collaborator, while all substantive research decisions, hypothesis pre-registrations, and evaluation criteria remained strictly under human authority:
- **AI Activities:** Scaffolded implementation modules under human specification, generated pytest verification fixtures, wrote data audit routines, generated publication plotting scripts, drafted ReportLab PDF compilation routines, and conducted preliminary peer-review checks.
- **Human Authority:** The investigator selected Research Gap G4, approved the primary research question and metric formulas, approved the two-sided statistical hypothesis, authorized the 4,680-episode campaign, and approved the final paper manuscript structure.
- **Integrity Compliance:** Zero fabricated results, zero invented citations, zero artificial p-values, zero data leakage, and full disclosure of the empirical contradiction of hypothesis $H_1$.
- **Detailed Collaboration Logs:** See [`ai_logs/ai_assistance_log.md`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/ai_logs/ai_assistance_log.md), [`ai_logs/debugging_log.md`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/ai_logs/debugging_log.md), and [`research/human_decisions.md`](file:///c:/Users/HARSH%20SHARMA/Desktop/atr-paper/research/human_decisions.md).

---

## 7. License & Academic Attribution
This project was completed as an implementation-based research assignment at the Indian Institute of Information Technology (IIIT), Allahabad. All original source code is released under the MIT License.
