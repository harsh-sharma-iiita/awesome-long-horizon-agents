# Five-Minute Research Demonstration Script & Technical Viva Preparation

**Project:** Verification Scheduling in Long-Horizon Agent Workflows: A Controlled Study of Error Detection, Propagation and Computational Overhead  
**Investigator:** Harsh Sharma  
**Institution:** Indian Institute of Information Technology, Allahabad  
**Governing Standard:** `AGENTS.md` (Integrity, Evidence Classification, Zero Fabrication, Transparent Negative Results)  

---

## Part 1: Five-Minute Demonstration Script

### Segment 1: Research Problem & Motivation (0:00 – 0:45)
- **Visual:** Slide / diagram illustrating cascading failure in a multi-step execution graph (e.g., Fork-Join motif with corrupted intermediate state propagating to terminal summary).
- **Spoken Script:**  
  *"Good morning. Autonomous language agents frequently suffer from severe planning-quality degradation when executing multi-step workflows. An error introduced early in an unverified execution sequence compounds across subsequent steps, poisoning downstream inferences and causing catastrophic workflow failures.  
  While runtime verification and rollback can intercept corrupted state before task completion, verification is computationally expensive. When an orchestrator operates under a strict verification budget—say, only 3 check slots across a 36-step workflow—a fundamental architectural question arises: **Where should verification checkpoints be placed?**  
  Intuitive architectural literature, such as VReAct, suggests that placing verification checkpoints at dependency integration boundaries (joins) should prevent cross-branch contamination. In this project, we conduct the first budget-matched empirical study to test whether milestone verification truly outperforms clock-like periodic verification."*

---

### Segment 2: Proposed Methodology & Architecture (0:45 – 1:30)
- **Visual:** Architecture diagram showing DAG Generator (Fork-Join, Spine-Join, Hierarchical Reduction) $\to$ Workflow Executor with Checkpoint Store $\to$ Deterministic Contract Suite $\to$ Independent Evaluator.
- **Spoken Script:**  
  *"To isolate the pure effect of checkpoint placement without confounding verification frequency, we designed a controlled factorial evaluation across 90 DAG task clusters evaluated across 4,680 episodes under controlled one-shot fault injection.  
  We contrast four experimental arms:
  - **Arm A (Final-Only):** Verification deferred strictly until terminal step $H$ ($K_{\text{alloc}}=1$).
  - **Arm B (Fixed-Periodic Baseline):** Checks scheduled at uniform intervals: $\lceil H/3 \rceil, \lceil 2H/3 \rceil, H$ ($K_{\text{alloc}}=3$).
  - **Arm C (Dependency-Milestone Intervention):** Checks scheduled immediately prior to multi-parent join boundaries and termination ($K_{\text{alloc}}=3$).
  - **Arm D (Every-Step Bound):** Verification invoked at every step ($K_{\text{alloc}}=H$).  
  Our primary estimand is the **Downstream Taint-Consumption Fraction (TCF)**, which measures what fraction of topologically reachable descendant nodes consumed corrupted data before verifier detection. Crucially, the evaluator ground truth is strictly isolated from the executor to prevent data leakage."*

---

### Segment 3: Working Implementation Demonstration (1:30 – 2:30)
- **Visual:** Live terminal execution in PowerShell.
- **Commands to Run:**
  ```powershell
  # 1. Run the test suite proving all 30 verification tests pass
  .\.venv\Scripts\python.exe -m pytest -v tests/
  
  # 2. Run the comparative pilot script showing 4-arm execution and budget parity
  .\.venv\Scripts\python.exe scripts/run_comparative_pilot.py
  ```
- **Spoken Script:**  
  *"Let us observe the implementation in action. Running our test suite validates 30 comprehensive unit and integration tests across task generation, fault injection, taint lineage tracking, scheduler budget parity, and single-replay recovery in under half a second.  
  Next, executing our comparative pilot runs all four scheduling conditions across development tasks. Notice the terminal output: on clean runs, all four conditions achieve a 0.00% false positive rate. Under identical fault injection at node n_01, both Arm B (Periodic) and Arm C (Milestone) receive exactly 3 allocated check slots and consume an identical number of realized verifier calls. Notice that Arm B catches early branch faults at step 4, whereas Arm C must wait until the join boundary is reached."*

---

### Segment 4: Actual Experimental Comparison (2:30 – 3:30)
- **Visual:** Display Figure 3 (Overhead vs. Propagation Pareto Trade-off) and Table 2 (Main Results).
- **Spoken Script:**  
  *"Moving to our final 4,680-episode evaluation campaign across 90 DAG clusters:  
  First, we achieved **strict verification budget parity**. Both Arm B (Periodic) and Arm C (Milestone) consumed an identical realized mean of **$2.7436 \pm 0.5872$ calls**, confirmed by a 100% pairwise match across all 1,170 evaluation units.  
  Second, our primary hypothesis test revealed a surprising and decisive result: **Arm B significantly outperformed Arm C on error containment**. Milestone verification permitted $3.91\%$ greater downstream taint propagation ($\mu_{\text{TCF}} = 0.9005$ vs. $0.8614$; paired permutation $p < 0.0001$; 95% bootstrap CI $[+0.0366, +0.0414]$; Cohen's $d = 3.35$).  
  Furthermore, periodic verification caught contract-violating faults with a mean delay of $5.50$ steps, compared to $7.81$ steps for milestone verification—a $2.31$-step latency advantage ($p < 0.0001$)."*

---

### Segment 5: Main Findings & Failure-Case Analysis (3:30 – 4:30)
- **Visual:** Display Figure 2 (Detection Delay by Position) and diagram of the *Structural Clumping Phenomenon*.
- **Spoken Script:**  
  *"Why did topological milestone verification fail to deliver superior containment?  
  Through detailed failure-case analysis, we identified the **structural clumping phenomenon**. In computational DAGs, parallel branches must complete their work before converging into an aggregation or join node. Consequently, join milestones naturally cluster in the middle and late phases of the workflow horizon.  
  This creates an early-stage blindspot for milestone scheduling: early branch corruptions cascade across multiple transformations before the join is evaluated. In contrast, fixed-periodic checking enforces an early boundary at $\lceil H/3 \rceil$, catching early faults before they spread.  
  Additionally, we observed that while all four arms achieved identical final completion rates ($38.46\%$) under our single-replay recovery policy, intermediate periodic verification reduced recovery re-execution waste by $38.9\%$ relative to final-only verification, saving an average of $2.87$ re-executed nodes per episode."*

---

### Segment 6: Limitations & Conclusion (4:30 – 5:00)
- **Visual:** Summary slide with key takeaways and GitHub repository structure.
- **Spoken Script:**  
  *"To conclude, this study provides the first controlled evidence refuting the assumption that dependency milestones are inherently superior to periodic intervals under low verification budgets.  
  Our limitations are clear: we evaluated deterministic dataflow workflows at $\$0.00$ API cost, and our contract suite checked structural integrity rather than semantic value drift.  
  For architects of compound AI systems, our guidance is straightforward: under tight verification budgets, rely on a clock-like periodic backbone to bound worst-case error propagation rather than waiting for complex multi-branch joins.  
  Thank you. I welcome your questions."*

---

## Part 2: Technical Viva Questions & Defensible Answers

### Question 1: Methodological Justification
**Question:** *"Why did you evaluate your scheduling policies on synthetic dataflow DAGs instead of live LLM agents executing open-ended tasks like SWE-bench?"*  
**Defensible Answer:**  
*"Evaluating on synthetic dataflow DAGs was an intentional, pre-registered methodological decision governed by `AGENTS.md` and research integrity principles. Live LLMs introduce high stochasticity, non-deterministic token sampling, prompt sensitivity, and substantial monetary costs (often exceeding thousands of dollars). By utilizing deterministic dataflow DAGs with formal relational contracts, we eliminated evaluation noise, guaranteed zero data leakage, and achieved $\$0.00$ API cost. Most importantly, it allowed us to mathematically track ground-truth taint propagation ($\text{TCF}$) across $160,440$ execution trace steps. The topological mechanics we identified—specifically how branch convergence causes join milestones to cluster in late stages—are fundamental graph properties that apply directly to compound agent frameworks like LangGraph and AutoGen."*

---

### Question 2: Direction of Hypothesis Refutation
**Question:** *"Your primary hypothesis H1 predicted that milestone verification would be superior, but your results showed it was inferior ($\Delta \text{TCF} = +0.0391$). Does this mean your research failed?"*  
**Defensible Answer:**  
*"On the contrary, this is a textbook demonstration of scientific progress through empirical refutation. In Phase D.1, we specifically pre-registered a conservative two-sided hypothesis ($H_1: \mu_{\text{TCF}, C} \neq \mu_{\text{TCF}, B}$) precisely to guard against confirmation bias. The prevailing intuition in agent literature was that semantic integration boundaries must be superior. Our empirical result ($p < 0.0001, t = 31.78, \text{Cohen's } d = 3.35$) rigorously falsified that intuition and allowed us to discover the 'structural clumping phenomenon.' In science, an honest, statistically rigorous negative finding that corrects architectural assumptions is far more valuable than a fabricated or massaged positive result."*

---

### Question 3: Verification Budget Fairness
**Question:** *"How can you claim that Arm B and Arm C had a fair comparison when realized calls depended on runtime early termination?"*  
**Defensible Answer:**  
*"We established fairness at two levels: allocation and realization. Both Arms B and C were allocated exactly $K_{\text{alloc}} = 3$ check slots *a priori*. At runtime, whenever an intermediate check failed, execution halted immediately to trigger rollback. Because early faults truncated execution, both arms consumed fewer than 3 calls on detected episodes. Crucially, across all 1,170 paired scenarios, both Arm B and Arm C realized an identical mean of **$2.7436 \pm 0.5872$ calls**, with an exact 100% pairwise match on every single episode. Furthermore, our replay protocol disarmed the fault and invoked zero additional checks, ensuring that recovery work did not inflate the budget."*

---

### Question 4: Identical Detection & Completion Rates
**Question:** *"Why are the fault detection coverage ($33.33\%$) and task completion rate ($38.46\%$) exactly identical across all four arms? Does this indicate a flaw in your implementation?"*  
**Defensible Answer:**  
*"We audited this thoroughly in Phase G.1 and proved that it is a direct mathematical consequence of our experimental design:  
1. All four arms evaluate the terminal artifact at step $H$. Any fault that violates a registered contract and persists to the end is eventually caught by Arm A just as it was by Arms B, C, and D.  
2. Our contract suite verified structural schema conformance and type integrity, catching 100% of missing fields ($270/270$) and 33.3% of type corruptions ($90/270$), but did not check semantic numeric drift ($0/270$). Thus, exactly $360$ faults out of $1,080$ ($33.33\%$) were detectable across all arms.  
3. Under our single-replay recovery policy, detecting a fault triggers rollback and disarms the fault during replay, resulting in 100% recovery for detected episodes. Undetected episodes never trigger rollback and fail final acceptance.  
Therefore, the true value of intermediate verification is not *whether* a fault is caught, but **WHEN** it is caught ($5.50$ vs. $12.17$ steps delay), **HOW MUCH TAINT** it spreads ($0.8614$ vs. $1.0000$ TCF), and **HOW MUCH REPLAY WORKLOAD** is saved ($4.51$ vs. $7.38$ re-executed nodes)."*

---

### Question 5: Statistical Validity & Pseudo-Replication
**Question:** *"With 4,680 episodes, did you commit pseudo-replication by treating every episode as independent?"*  
**Defensible Answer:**  
*"No. We explicitly guarded against pseudo-replication by conducting all inferential statistical tests at the **$N = 90$ graph-cluster level**. The 12 fault scenarios executed on a single graph share the same topology and node operations, so they are not independent. In our protocol, we computed the cluster-level mean difference $d_g = \bar{\text{TCF}}_{C, g} - \bar{\text{TCF}}_{B, g}$ for each of the 90 independent graph seeds. Our two-sided permutation test ($10^4$ sign flips) and percentile bootstrap confidence interval ($[+0.0366, +0.0414]$) operate strictly on these 90 cluster-level paired differences."*
