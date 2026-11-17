# AI Detection Evaluation Report: Rewritten ('Humanized') Literature Review Audit

**Target Document:** Planning-Quality Degradation in Long-Horizon Autonomous Research Agents (Rewritten / Humanized PDF Upload)  
**Detector Model:** `desklib/ai-text-detector-v1.01` (DeBERTa-v3-large (304M parameters))  
**Benchmark Standing:** Ranked #1 on RAID detection benchmark  
**Execution Timestamp:** 2026-11-17 12:41:12  
**Audit Duration:** 105.44 seconds  

---

## 1. Executive Summary

- **Overall AI Score:** **`38.0%`**
- **Aggregate Model Verdict:** **`LIKELY HUMAN`**
- **Sentence Breakdown:** 33 AI-leaning (29.2%) | 80 Human-leaning (70.8%) | 4 Skipped
- **Sentence Length Dynamics (SDSL):** Mean = 32.5 words, StdDev = 17.5, CV = 0.54

## 2. Section-by-Section Score Breakdown

| Section | Words | AI Score (%) | Verdict | AI Sentences | Human Sentences | Scored Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Abstract** | 194 | **32.0%** | `LIKELY HUMAN` | 1 | 3 | 4 |
| **1. Introduction** | 290 | **27.0%** | `LIKELY HUMAN` | 2 | 5 | 7 |
| **2. Background & Lit Review** | 552 | **30.5%** | `LIKELY HUMAN` | 3 | 11 | 14 |
| **3. Thematic & Tech Discussion** | 942 | **33.5%** | `LIKELY HUMAN` | 7 | 31 | 38 |
| **4. Current Approaches** | 696 | **37.9%** | `LIKELY HUMAN` | 8 | 19 | 27 |
| **5. Research Challenges** | 479 | **33.5%** | `LIKELY HUMAN` | 3 | 9 | 12 |
| **6. Research Gaps & Future** | 317 | **67.6%** | `LIKELY AI` | 5 | 3 | 8 |
| **7. Conclusion** | 157 | **13.4%** | `LIKELY HUMAN` | 0 | 3 | 3 |


## 3. Comparative Analysis: Original Literature Review vs. Rewritten/Humanized PDF

| Metric | Original Literature Review | Rewritten ('Humanized') PDF | Delta / Impact |
| :--- | :---: | :---: | :--- |
| **Overall AI Score** | **`37.3%`** | **`38.0%`** | +0.7% |
| **Overall Verdict** | `LIKELY HUMAN` | `LIKELY HUMAN` | Both within safe human band |
| **Human Sentence Ratio** | **72.5%** (121/167) | **70.8%** (80/113) | -1.7% |
| **Mean Sentence Length** | 22.9 words | 32.5 words | +9.6 words |


## 4. Linguistic Diagnostics & Artifacts of 'Humanization'

The detector mapped notable increases in colloquial insertions and filler phrases added during rewriting:

| Diagnostic Pattern Category | Occurrences in Paper | Interpretation |
| :--- | :---: | :--- |
| `ai_slop` | 3 | Syntactic pattern detected |
| `flaggy_adverb` | 2 | Syntactic pattern detected |
| `formal_verb` | 2 | Syntactic pattern detected |
| `missing_contraction` | 1 | Syntactic pattern detected |


## 5. Highest AI Probability Sentences (Rewritten Version)

1. **AI Probability: `100.0%`**
   > "## 2 Background and Literature Review
### 2.1 Evolution of Autonomous Agent Architectures
My point is, the architectural strategy for LLM-based autonomous agents has progressed through the three separate developmental stages [2]:
1."

2. **AI Probability: `100.0%`**
   > "And these interventions fall into the four primary methods:
### 4.1 Search-Based and Deliberate Planning Frameworks
Or better yet than hinging on reflexive autoregressive generation, search-based structures are expanding decision making into the clear state space search [12], in many respects."

3. **AI Probability: `99.8%`**
   > "### 2.2 Disambiguating Horizon, Context, and Memory
A primary source of vagueness in literature is the conflation of three separate system properties [7]:
• Long-Horizon: A structural feature of the task, set out by the minimum number of Horizon length is normally autonomous of whether the resulting trajectory fits, within a model's context window [7], in real-world scenarios."

4. **AI Probability: `99.7%`**
   > "### 4.3 Multi-Tiered Runtime Harnesses and Executable Workspaces
Modern automated research platforms are isolating long-horizon planning, across the physical and operational boundaries [5], in actual application."

5. **AI Probability: `99.7%`**
   > "### 6.2 Process-Level Credit Assignment and Granular Reward Models
Outcome-based evaluation signals (such as binary pass/fail test checks or final accuracy scores) are growing uninformative over long task horizons [7], to a significant degree."



## 6. Highest Human Probability Sentences (Rewritten Version)

1. **Human Probability: `99.4%`** (AI: `0.6%`)
   > "With a doubling of task duration quadrupling the probability of failure [8], after roughly 35 minutes of human-equivalent operational time; this non-linear compounding of departure exposes a essential mismatch - single-step token-level reasoning doesn't inherently produce long-horizon strategic planning [1], on the whole; in fact, the distance between single-step execution accuracy and trustworthy long-horizon task completion is formalised as the horizon gap [7]; this gap is showing as built-in planning degradation in long-running autonomous research, to a significant degree."

2. **Human Probability: `99.3%`** (AI: `0.7%`)
   > "We formalize the theoretical distance between single-step model capability and multi-step task completion, named as the horizon gap, and assess the coring technical processes driving performance decay, covering compounding execution errors, autoregressive self-conditioning, local greedy policy myopia, context window pollution ("reasoning debris"), goal drift, and the no-recovery bottleneck caused by extreme task decomposition, and survey architectural and algorithmic interventions designed to ease degradation, including state- space search algorithms (Tree-of-Thoughts, Language Agent Tree Search), adaptive context managers, progressive memory compression, and multi-tiered runtime harnesses, and review empirical performance across the research benchmarks, highlight key setup and verification holdups, and map out critical future research directions toward the solid, long-horizon autonomous science."

3. **Human Probability: `99.2%`** (AI: `0.8%`)
   > "But instead, it's driven by compounding execution errors, self-conditioning loops, local greedy policy myopia, context pollution, and the absence of value propagation across the execution states [1]; as, showed by state-space search architectures, dynamic context managers, and workspace-grounded execution environments, keeping up planning quality over long horizons demands separating reasoning traces, enforcing closed-loop deterministic verification, allowing workspace state rollbacks, and decoupling state preservation from model context windows [5]."

4. **Human Probability: `98.7%`** (AI: `1.3%`)
   > "Global coherence is lost by agents, engage in unnecessary tool execution, drift from primary research objectives, commit to flawed hyperparameter or algorithmic choices early in execution, and struggle to recover from intermediate software or experimental failures [1]; understanding and solving planning-quality breaking down is therefore the central engineering and theoretical holdup preventing autonomous agents from hitting durable, open-ended scientific discovery [5]."

5. **Human Probability: `98.0%`** (AI: `2.0%`)
   > "If an atomic step makes a subtly flawed intermediate output (such as an incorrectly formatted data array or a partial software patch) that fulfills local syntactic checks, downstream subagents receive corrupted inputs without the contextual history needed to diagnose the root cause [10]; in fact, the execution harness becomes unable to backtrack, across the atomic boundaries, reshaping minor execution errors into the terminal pipeline failures [10]."


