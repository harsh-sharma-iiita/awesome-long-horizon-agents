# Main Experimental Results: Verification Scheduling Comparison (final_exp_20261104_015549_5fcb5a61)

| Verification Arm | Allocated Slots | Realized Calls | Mean TCF (Primary) | Fault Coverage | Detection Delay | Task Completion | False Positive Rate | Workflow Time (ms) | Verifier Time (ms) |
|---|---|---|---|---|---|---|---|---|---|
| Final Only | 1 | 1.0 | 1.0000 ± 0.0000 | 33.3% | 12.17 | 38.5% | 0.0% | 25.00 | 0.102 |
| Fixed Periodic | 3 | 2.74 | 0.8614 ± 0.2893 | 33.3% | 5.5 | 38.5% | 0.0% | 23.01 | 0.185 |
| Milestone Based | 3 | 2.74 | 0.9005 ± 0.2482 | 33.3% | 7.81 | 38.5% | 0.0% | 23.22 | 0.175 |
| Every Step | H | 21.03 | 0.7236 ± 0.4346 | 33.3% | 2.5 | 38.5% | 0.0% | 28.31 | 1.015 |


### Primary Statistical Contrast: Arm C (Milestone) vs. Arm B (Periodic)

- **Mean TCF Difference (C - B):** `0.0391`
- **Two-Sided Permutation Test p-value:** `0.0000`
- **95% Bootstrap Confidence Interval:** `[0.0366, 0.0415]`
- **Statistical Conclusion:** Statistically significant increase in taint consumption.
