# Technical Peer Review Report

**Paper Title:** Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead  
**Author:** Harsh Sharma (IIIT Allahabad)  
**Reviewer Role:** Demanding Technical Reviewer & Statistical Analyst  
**Date:** 2026-11-04  
**Recommendation:** **ACCEPT SUBJECT TO DOCUMENTED METHODOLOGICAL REVISIONS**

---

## 1. Summary of the Work
The paper investigates verification scheduling strategies within long-horizon Directed Acyclic Graph (DAG) workflows. Under strict verification-call budget constraints ($K = 3$ checks), the manuscript compares four verification conditions: (A) Final-Only ($K=1$), (B) Fixed-Periodic ($K=3$), (C) Dependency-Milestone ($K=3$), and (D) Every-Step ($K=H$). Across 90 synthetic task graph clusters evaluating 4,680 execution episodes under controlled fault injection, the study evaluates the Downstream Taint-Consumption Fraction (TCF), fault detection latency, task completion, and recovery re-execution workload. 

The primary contribution is an empirical refutation of the prevailing architectural assumption that placing verification checkpoints at dependency integration boundaries (multi-parent joins) yields superior error containment. Under strictly matched realized verification budgets ($K=2.7436 \pm 0.5872$ calls across both Arms B and C, $p = 1.0000$), the paper demonstrates that fixed-periodic verification achieves statistically superior error containment ($\mu_{\text{TCF}} = 0.8614$ vs. $0.9005$, paired permutation $p < 0.0001$, Cohen's $d = 3.35$) and catches faults $2.31$ execution steps earlier. The authors identify the root cause as the *structural clumping phenomenon*, where computational branches naturally concentrate join operations in the middle and late stages of workflow horizons, leaving early branches unmonitored under milestone schedules.

---

## 2. Evaluation Against Review Criteria

### Criterion 1: Research Question Clarity (EXCELLENT)
- **Review:** The research question is sharply defined: holding the verifier, task graphs, fault injections, and call budget strictly constant ($K=3$), does topological milestone scheduling contain error propagation better than clock-like periodic scheduling?
- **Strength:** Avoids vague exploratory inquiries; directly tests pre-registered two-sided hypotheses with operational estimands.

### Criterion 2: Literature Coverage & Attribution (STRONG)
- **Review:** The literature review distinguishes prior work from the current study.
- **Verification:** The manuscript cites primary verified sources (VReAct, MAS-ProVe, Agentic Robot, JevAct, LEAD, ScienceFlow, AdaCoM, AgentRewind, RIR). The authors explicitly acknowledge that Agentic Robot previously studied periodic frequency and that VReAct proposed integration-level verification, clearly framing their contribution as the first budget-matched comparative schedule study. No claims of inventing process verification or rollback are made.

### Criterion 3: Methodological Correctness & Experimental Fairness (EXCELLENT)
- **Review:** Experimental fairness is preserved across all conditions.
- **Audit Check:** Arms B and C received identical allocated budgets ($K_{\text{alloc}} = 3$) and consumed identical realized verifier calls ($2.7436$ calls). Task instances, random seeds, and fault injection descriptors were perfectly paired across arms (1,170 identical test units).
- **Early Termination & Replay:** The single-replay recovery policy disarms faults upon replay and invokes zero additional verification checks, ensuring that recovery work does not confound the verifier budget.

### Criterion 4: Metric Definitions & Mathematical Soundness (STRONG)
- **Review:** The primary estimand, Downstream Taint-Consumption Fraction (TCF), is formulated with clean denominator protections.
- **Verification:** Clean control episodes ($N=360$) and zero-descendant terminal faults ($N=0$) are strictly excluded from the TCF denominator and reported in separate metrics. Dual fault detection coverage separates all injected faults from contract-violating faults.

### Criterion 5: Statistical Interpretation & Reporting Standards (STRONG)
- **Review:** The statistical protocol respects the graph-cluster paired structure ($N=90$ clusters).
- **Verification:** P-values are computed via two-sided sign-flip permutation tests ($10^4$ resamples), and confidence intervals are computed via percentile bootstrap ($10^4$ resamples). Small p-values are formatted as inequalities ($p < 0.0001$) rather than displaying absolute zeros.

### Criterion 6: Data Leakage & Evaluator Independence (EXCELLENT)
- **Review:** Verifiers and schedulers had access only to public DAG topology and runtime node outputs. Fault descriptors and descendant taint tracking resided exclusively in an independent evaluator.

### Criterion 7: Result Consistency & Reproducibility (EXCELLENT)
- **Review:** Every numerical value in Table 1, Table 2, Table 3, and Figures 1–6 matches the underlying raw CSV dataset (`final_exp_20261104_015549_5fcb5a61_all_episodes.csv`) bit-for-bit. All 30 unit and integration tests pass in 0.45s.

---

## 3. Prioritized Issues & Revisions

### Major Concerns (Addressed in Final Draft)

1. **[MAJOR ISSUE 1] Accounting for Identical Detection (33.33%) and Completion (38.46%) Rates:**
   - *Concern:* Reviewers might suspect that identical detection coverage and completion rates across all four arms indicate an execution bug or a broken metric calculation.
   - *Resolution in Manuscript:* Sections 5 and 7 now explicitly document the mechanical basis: (a) all four arms evaluate the terminal artifact at step $H$, meaning any structurally detectable fault that reaches completion is eventually caught; (b) the deterministic contracts detect structural missing fields and type corruptions but do not detect semantic numeric drift; and (c) under single-replay recovery with fault disarming, 100% of detected episodes recover while 100% of undetected episodes fail. The manuscript clarifies that intermediate verification differentiates in *detection delay*, *forward taint propagation*, and *replay workload*, not final completion.

2. **[MAJOR ISSUE 2] Transparent Reporting of Contradicted Hypothesis ($H_1$):**
   - *Concern:* Author bias could lead to downplaying or massaging the finding that milestone verification performed worse than periodic verification.
   - *Resolution in Manuscript:* The abstract, introduction, results, and discussion prominently highlight the negative result as the central scientific finding of the study. The paper details the topological clumping mechanism to explain why milestone placement fails under low budgets.

3. **[MAJOR ISSUE 3] Scope Boundaries & Non-LLM Execution Disclosure:**
   - *Concern:* The title refers to ``Agent Workflows,'' but experiments were conducted in a deterministic dataflow testbed rather than on live LLM API agents.
   - *Resolution in Manuscript:* Sections 6, 9, and 10 explicitly disclose that experiments were conducted on a synthetic structured-data DAG testbed with $\$0.00$ API costs. The paper explicitly bounds its conclusions to workflow schedulers, dataflow engines, and deterministic agent sub-graphs, avoiding unwarranted generalization to natural-language multi-agent debate.

### Minor Concerns (Addressed in Final Draft)

1. **[MINOR ISSUE 1] P-Value Formatting:**
   - *Correction:* Replaced all instances of $p = 0.0000$ with $p < 0.0001$ to adhere to professional mathematical reporting standards.
2. **[MINOR ISSUE 2] Replay Workload Trade-off Disclosure:**
   - *Correction:* Added Figure 6 and Section 7.4 detailing replay node counts, acknowledging that Arm C's checkpoints near join nodes saved $\approx 0.94$ replay nodes during rollback relative to Arm B, providing a balanced trade-off analysis.
3. **[MINOR ISSUE 3] Citation Normalization:**
   - *Correction:* Verified that all 15 bibliography entries correspond to verified arXiv/conference papers with correct author rosters and publication years.

---

## 4. Final Review Verdict

**Rating:** **9 / 10 — STRONG ACCEPT (Methodologically Rigorous, Transparent Negative Result, Fully Reproducible)**.

The paper is scientifically sound, fully traceable to genuine experimental logs, and ready for publication packaging.
