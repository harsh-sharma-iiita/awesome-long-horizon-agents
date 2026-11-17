# Reproducibility: Execution Commands

**Project:** Verification Scheduling in Long-Horizon Agent Workflows (G4)  
**Institution:** Indian Institute of Information Technology, Allahabad  
**Student:** Harsh Sharma  
**Date:** 2026-11-04  

---

## 1. Environment Diagnostics

To inspect the system execution host, verify hardware specifications, memory capacity, and confirm the absence of unverified credentials or GPU requirements:

```powershell
# From the repository root (AITR_Lab02_MSE2026006):
python scripts/check_environment.py
```

---

## 2. Environment Setup

```powershell
# Create project-specific virtual environment (if not already created):
python -m venv .venv

# Activate virtual environment:
.\.venv\Scripts\Activate.ps1

# Install exact pinned dependencies:
pip install -r requirements.txt
```

---

## 3. Unit and Integration Test Suite Execution

To run the complete test suite (30 tests verifying task generation, DAG structural properties, verifier assertions, all 4 scheduler slot limits, fault injection, snapshot/rollback mechanics, metrics, and JSONL logging):

```powershell
# Execute all tests with detailed verbosity:
.\.venv\Scripts\python.exe -m pytest -v tests/
```

Expected result:
```text
30 passed in ~0.45s
```

---

## 4. Phase E Baseline Pilot Run

To execute the Fixed-Periodic Verification baseline (Arm B, 3 allocated check slots) across development workflows with clean controls and four controlled fault classes:

```powershell
.\.venv\Scripts\python.exe scripts/run_baseline_pilot.py
```

Outputs:
- Run logs in `runs/logs/`
- Trajectories in `runs/trajectories/`
- Metrics in `results/raw/`

---

## 5. Phase F Comparative Pilot Run (4 Verification Arms)

To execute all four verification conditions (Arm A: Final-Only, Arm B: Fixed-Periodic, Arm C: Milestone-Based, Arm D: Every-Step) on 5 development workflows (260 episodes):

```powershell
.\.venv\Scripts\python.exe scripts/run_comparative_pilot.py
```

Outputs:
- Summary metrics: `results/raw/pilot_4arms_*_arm_summaries.json`
- Paired comparison: `results/comparisons/pilot_4arms_*_contrast_B_vs_C.json`

---

## 6. Phase F Final Experimental Campaign (4,680 Episodes)

To execute the complete frozen experimental campaign across 90 final graphs, 3 horizons ($H=12, 24, 36$), 3 dependency motifs, 13 scenarios per graph, and 4 verification arms:

```powershell
.\.venv\Scripts\python.exe scripts/run_final_experiments.py
```

Runtime: Approximately 120 seconds on an 8-core CPU.

Outputs generated:
- Master raw CSV dataset: `results/raw/final_exp_*_all_episodes.csv` (1.00 MB, 4,680 rows)
- Overall metrics: `results/processed/final_exp_*_overall_metrics.json`
- Horizon sensitivity: `results/processed/final_exp_*_by_horizon.json`
- Position sensitivity: `results/processed/final_exp_*_by_position.json`
- Primary statistical paired contrast: `results/comparisons/final_exp_*_primary_contrast.json`
- Markdown & CSV comparison tables: `results/tables/final_exp_*_main_results.md` and `.csv`
- Horizon breakdown tables: `results/tables/final_exp_*_horizon_breakdown.md` and `.csv`
- Execution logs and JSONL traces: `runs/logs/` and `runs/trajectories/`

To regenerate Markdown/CSV tables from existing processed results:
```powershell
.\.venv\Scripts\python.exe scripts/generate_tables.py
```
