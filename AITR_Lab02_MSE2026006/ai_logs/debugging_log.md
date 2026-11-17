# Debugging Log — G4 Implementation

**Governing Rule:** `AGENTS.md` §11 (Never fabricate debugging examples or AI limitations).

---

## Entry 1: Pytest Test Module Import Path (`ModuleNotFoundError: No module named 'src'`)
- **Date:** 2026-11-04
- **Phase:** Phase E — Unit Test Execution
- **Symptom:** Running `pytest -v tests/` directly failed during collection with `ModuleNotFoundError: No module named 'src'`.
- **Root Cause:** When running pytest directly via binary executable without an installed editable package or explicit `PYTHONPATH`, Python 3.14 did not place the project root on `sys.path`.
- **Resolution:** Executed pytest using the virtual environment interpreter module syntax: `.\.venv\Scripts\python.exe -m pytest -v tests/`. This automatically prepends the current working directory to `sys.path`.
- **Outcome:** VERIFIED. All 28 test modules imported successfully.

---

## Entry 2: False Positive on Clean Join in Reference Integrity Contract
- **Date:** 2026-11-04
- **Phase:** Phase E — Baseline Executor Test
- **Symptom:** `test_executor_clean_execution` failed with `AssertionError: assert True is False` (`rollback_occurred` was unexpectedly `True` on a clean run with 0 faults).
- **Root Cause:** In `src/verification/verifier.py`, the `reference_integrity` assertion checked whether each output record's `record_id` existed in *every* parent node's dataset (`for p_id in node.parents: if k_val not in parent_keys: fail`). In the Fork-Join motif, Branch A filters records (keeping only `value > 50`), while Branch B normalizes all records. The join combines records from both branches. Because filtered records from Branch B did not exist in Branch A, the verifier incorrectly flagged clean valid records as broken references, triggering a false alarm and premature rollback.
- **Resolution:** Updated `_evaluate_rule` in `src/verification/verifier.py` to aggregate all valid parent reference keys into a union set (`parent_keys_all.update(...)`) and verify that every joined record key exists in *at least one* parent dataset.
- **Outcome:** VERIFIED. False positive rate on clean runs dropped to 0.0%, and `test_executor_clean_execution` passed.

---

## Entry 3: Unhandled TypeError Under Type Corruption Fault Injection
- **Date:** 2026-11-04
- **Phase:** Phase E — Baseline Pilot Execution (`scripts/run_baseline_pilot.py`)
- **Symptom:** Execution crashed during pilot episode 13 (`dev_graph_00_early_type_corruption`) with `TypeError: 'int' object is not iterable` in `src/verification/verifier.py:146`.
- **Root Cause:** The `type_corruption` fault injected an integer (`123456789`) in place of the `records` list at node `n_01`. When the downstream join node was evaluated, `parent_out.get("records")` returned an integer. The verifier's loop `for r in parent_records` attempted to iterate over the integer, raising a `TypeError` instead of gracefully failing the contract check.
- **Resolution:** Added defensive type validation in `verifier.py` (`if isinstance(parent_records, list):`) and in `executor.py` across all node operations (`filter`, `normalize`, `aggregate`, `join`) to ensure non-list corrupted inputs are handled safely without crashing the executor.
- **Outcome:** VERIFIED. Corrupted type was cleanly detected by the contract schema assertion, triggering expected rollback without interpreter crashes.

---

## Entry 4: Chained Aggregate Missing 'records' Key in Spine-Join
- **Date:** 2026-11-04
- **Phase:** Phase F — Comparative Pilot Execution (`scripts/run_comparative_pilot.py`)
- **Symptom:** Clean control run in `pilot_graph_01` (Spine-Join topology) produced an unexpected false positive (`c_n_05_schema missing required keys ['summary']`).
- **Root Cause:** In the Spine-Join topology, side branch 1 chained two `aggregate` nodes in series. The second aggregate looked for `records` in its parent output, but the upstream aggregate produced only `summary`. Consequently, `summary` was empty `{}` and dropped by the downstream `join`.
- **Resolution:** Enhanced `aggregate` in `src/execution/executor.py` to preserve and pass through parent `summary` if `records` is absent, and ensured `join` always attaches `summary` when any parent had a summary.
- **Outcome:** VERIFIED. Clean false positive rate dropped to exactly 0.0% across all 260 pilot episodes and all 4,680 final evaluation episodes.

---

## Entry 5: Table Generation KeyError in `run_final_experiments.py`
- **Date:** 2026-11-04
- **Phase:** Phase F — Final Experiment Execution (`scripts/run_final_experiments.py`)
- **Symptom:** At the very end of `run_final_experiments.py` (after all 4,680 episodes had completed and raw CSV/JSON files were already saved), line 349 threw `KeyError: 'Fault Coverage'` when formatting Markdown tables.
- **Root Cause:** In `scripts/run_final_experiments.py`, the metric dictionary key was named `"Fault Coverage (FDC)"` while the Markdown table string formatter looked for `r['Fault Coverage']`.
- **Resolution:** Corrected key lookup in `scripts/run_final_experiments.py` and created `scripts/generate_tables.py`, which parsed the saved `results/processed/` JSONs and cleanly generated all Markdown and CSV summary tables in `results/tables/`.
- **Outcome:** VERIFIED. Tables generated completely and accurately without affecting raw simulation data.
