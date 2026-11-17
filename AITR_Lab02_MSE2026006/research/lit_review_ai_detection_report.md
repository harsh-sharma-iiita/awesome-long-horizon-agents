# AI Detection Evaluation Report: Literature Review Audit

**Target Document:** Planning-Quality Degradation in Long-Horizon Autonomous Research Agents (Literature Review)  
**Source File:** `source_docs/literature_review.pdf`  
**Detector Model:** `desklib/ai-text-detector-v1.01` (DeBERTa-v3-large (304M parameters))  
**Benchmark Standing:** Ranked #1 on RAID detection benchmark  
**Execution Timestamp:** 2026-11-04 19:12:28  
**Audit Duration:** 106.03 seconds  

---

## 1. Executive Summary

- **Overall Literature Review AI Score:** **`37.3%`**
- **Aggregate Model Verdict:** **`LIKELY HUMAN`**
- **Sentence Breakdown:** 46 AI-leaning (27.5%) | 121 Human-leaning (72.5%) | 140 Skipped (titles/short lines)
- **Sentence Length Dynamics (SDSL):** Mean = 22.9 words, StdDev = 16.9, CV = 0.74 (`N/A`)

## 2. Section-by-Section Score Breakdown

| Section | Words | AI Score (%) | Verdict | AI Sentences | Human Sentences | Scored Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Abstract** | 184 | **39.0%** | `LIKELY HUMAN` | 3 | 5 | 8 |
| **1. Introduction** | 264 | **38.1%** | `LIKELY HUMAN` | 3 | 9 | 12 |
| **2. Background & Literature Review** | 538 | **32.4%** | `LIKELY HUMAN` | 4 | 19 | 23 |
| **3. Thematic & Technical Discussion** | 897 | **33.9%** | `LIKELY HUMAN` | 9 | 31 | 40 |
| **4. Current Approaches & Developments** | 582 | **32.6%** | `LIKELY HUMAN` | 7 | 22 | 29 |
| **5. Research Challenges & Limitations** | 572 | **38.5%** | `LIKELY HUMAN` | 7 | 13 | 20 |
| **6. Research Gaps & Future Directions** | 411 | **38.9%** | `LIKELY HUMAN` | 3 | 9 | 12 |
| **7. Conclusion** | 145 | **36.8%** | `LIKELY HUMAN` | 2 | 4 | 6 |


## 3. Comparative Comparison: Paper 1 (Literature Review) vs. Paper 2 (Experimental Study)

| Metric | Paper 1: Literature Review | Paper 2: Experimental Paper | Delta / Contrast |
| :--- | :---: | :---: | :--- |
| **Overall AI Score** | **`37.3%`** | **`38.5%`** | -1.2% |
| **Overall Verdict** | `LIKELY HUMAN` | `LIKELY HUMAN` | Both within calibrated human/mixed band |
| **Human Sentence Ratio** | **72.5%** (121/167) | **73.9%** (164/222) | -1.4% |
| **Mean Sentence Length** | 22.9 words | 24.7 words | -1.8 words |
| **Sentence CV (SDSL)** | 0.74 | 0.43 | Both demonstrate natural length variation |


## 4. Linguistic Pattern Diagnostics

The DeBERTa-v3 detector maps structural patterns characteristic of formal synthesis papers:

| Diagnostic Pattern Category | Occurrences in Paper | Impact / Interpretation |
| :--- | :---: | :--- |
| `ai_slop` | 9 | Academic survey styling pattern |
| `missing_contraction` | 6 | Academic survey styling pattern |
| `formal_verb` | 5 | Academic survey styling pattern |
| `flaggy_adverb` | 3 | Academic survey styling pattern |
| `formal_transition` | 2 | Academic survey styling pattern |


## 5. Sentences with Highest AI Probability Flag

The following sentences received the highest AI probability scores from DeBERTa-v3:

1. **AI Probability: `96.1%`**
   > "The Age of AI Agents Demands A New Scientific Paradigm To Sustain Trustworthy Science."
   > *Pattern Notes:* `ai_slop` (replace with plain English)

2. **AI Probability: `95.4%`**
   > "The metric Horizon Length (Hs ) defines
the maximum step count at which an agent maintains a mean
completion accuracy above threshold s∈ 0≤𝑠≤ 1 [9]:

(
𝑘∈ N|𝑃
 𝑘Û
𝑖=1
𝑎𝑖 =𝑎*𝑖
!"
   > *Pattern Notes:* `formal_verb` (try 'keeps')

3. **AI Probability: `94.4%`**
   > "2.3 Automated Research Agents in Practice
The development of automated scientific research systems represents a demanding benchmark for long-horizon planning [3]."
   > *Pattern Notes:* `formal_verb` (try 'is' or rephrase)

4. **AI Probability: `93.9%`**
   > "If an atomic step generates a subtly flawed intermediate output (such as an incorrectly formatted data array or a partial
software patch) that satisfies local syntactic checks, downstream
subagents receive corrupted inputs without the contextual history
needed to diagnose the root cause [10]."

5. **AI Probability: `93.6%`**
   > "2 Background and Literature Review
2.1 Evolution of Autonomous Agent
Architectures
The architectural paradigm for LLM-based autonomous agents has
progressed through three distinct developmental stages [2]:
1."
   > *Pattern Notes:* `ai_slop` (replace with plain English)

6. **AI Probability: `92.5%`**
   > "Rather than using fixed token boundaries, context management should be driven by dynamic reinforcement learning agents (e.g., AdaCoM) that monitor context entropy,
task progress, and model-specific reliability thresholds to dynamically compress or restore execution history [16]."

7. **AI Probability: `89.1%`**
   > "While agents achieve high accuracy on benchmark
tasks requiring fewer than 10 sequential turns, performance decays rapidly as task duration and decision complexity increase [1]."

8. **AI Probability: `89.1%`**
   > ""Reflexion: Language Agents with Verbal Reinforcement Learning"."

9. **AI Probability: `88.7%`**
   > "While human researchers review scientific literature at human reading speeds, autonomous agents can execute thousands of experimental variations
and generate dozens of synthetic manuscripts overnight [6]."

10. **AI Probability: `87.8%`**
   > "7 Conclusion
Planning-quality degradation remains the primary bottleneck preventing autonomous research agents from realizing reliable, multiday scientific discovery [5]."



## 6. Sentences with Highest Human Probability Flag

The following sentences received the strongest Human classification from DeBERTa-v3:

1. **Human Probability: `99.9%`** (AI: `0.1%`)
   > "Benchmark Target domain Evaluation metric Scale Baseline model Baseline accuracy
Harness-enhanced
SOTA
Primary failure mode
MLE-Bench [3, 5] Applied ML/Kaggle tasks Any-medal rate (24h budget) 75 tasks OpenAI o1-preview 16.90% 70.22% (ScienceFlow)
[5]
Multi-turn debugging
and resource management [3]
PaperBench [3] ICML paper replication End-to-end replication accuracy
8,316 tasks OpenAI o1-high 26.00% N/A Complex code implementation gap [3]
SciReplicate-Bench
[3]
NLP code generation Executable reproduction rate 100 tasks Claude 3.7 Sonnet 39.00% N/A Error accumulation in
pipeline assembly [3]
CORE-Bench [3] CS/Med paper reproduction Task completion pass rate 270 tasks OpenAI GPT-4o 55.56% N/A Environment configuration failure [3]
ML-Dev-Bench [3] Software engineering/ML Full repository pass rate 30 tasks Claude 3.5 Sonnet 50.00% N/A Long-horizon context
drift [3]
environments allow git-based state resets and workspace restoration, real-world tool execution (such as web API calls, database
writes, or physical resource allocation) often alters environment
state irreversibly [17]."

2. **Human Probability: `99.9%`** (AI: `0.1%`)
   > "Framework Primary mechanism Memory/state representation Context management Mitigation target
Tree-of-Thoughts (ToT)
[12]
Heuristic tree search
(BFS/DFS)
Tree-structured intermediate
thoughts
Uncompressed local branch
context
Local policy myopia and lack
of lookahead
Language Agent Tree
Search (LATS) [13]
MCTS with external environment feedback
Tree nodes with value and reflection scores
Environment reset and state
backtracking
Cumulative execution failure
and missing rollbacks
Adaptive Context Management (AdaCoM) [16]
External RL-trained context
controller
Dynamic context filtering Dynamic pruning and stalecontent stripping
Context window saturation
and attention dilution
CORPGEN Harness [8] Temporal isolation and state
serialization
Structured external checkpoint storage
Clean context reinstantiation
via re-anchoring
Goal drift and context pollution
ScienceFlow [5] Workspace-grounded research segments
Executable filesystem snapshots and artifacts
Segment-isolated interaction
logs
Irreversible workspace corruption
Goal2Skill [8] Progressive dual-system compression
Lossless facts plus lossy reasoning traces
Structured task-log extraction Context memory decay and
context bloat
The following table summarizes empirical benchmark performance
across primary research tasks, detailing target domains, evaluation
metrics, and observed failure modes [3]."

3. **Human Probability: `95.1%`** (AI: `4.9%`)
   > "Standard prompting schemes (such as CoT) formalize inference as a step-wise greedy
policy [1]:

This greedy policy selects actions based on local next-step plausibility or high immediate generation likelihood [1]."

4. **Human Probability: `93.7%`** (AI: `6.3%`)
   > "Agents lose global coherence, engage in redundant tool
execution, drift from primary research objectives, commit to suboptimal hyperparameter or algorithmic choices early in execution,
and struggle to recover from intermediate software or experimental
failures [1]."

5. **Human Probability: `93.7%`** (AI: `6.3%`)
   > "Concurrently, search-based
inference paradigms such as Tree-of-Thoughts (ToT) [12] and Language Agent Tree Search (LATS) [13] integrated formal state-space
search (e.g., Breadth-First Search, Monte Carlo Tree Search) with
LLM heuristic evaluations."

6. **Human Probability: `93.7%`** (AI: `6.3%`)
   > "• Adaptive Context Management (AdaCoM): AdaCoM trains an
external controller via
reinforcement learning to dynamically modify, prune, and summarize the context window of a frozen primary agent [16]."

7. **Human Probability: `93.1%`** (AI: `6.9%`)
   > "Because step-wise greedy policies lack value propagation
mechanisms (such as Bellman backpropagation or Monte Carlo
tree rollouts), they make early myopic commitments [1]."

8. **Human Probability: `92.9%`** (AI: `7.1%`)
   > "Crucial intermediate experimental results, state variables, or negative debugging feedback located
in the middle of a long context are systematically ignored [10]."

9. **Human Probability: `92.3%`** (AI: `7.6%`)
   > "Context Engineering Stage (2023–2025): To extend operational
scope, architectures
incorporated structured memory, retrieval-augmented generation (RAG), and verbal reinforcement learning [ 2]."

10. **Human Probability: `92.2%`** (AI: `7.8%`)
   > "While operationally convenient, this commit-or-discard paradigm is structurally isomorphic to local greedy hill-climbing [11]."



## 7. Methodological Context & Technical Interpretation

1. **Literature Survey Nature:** Literature reviews naturally exhibit formal, structured academic synthesis (e.g., 'Techniques such as...', 'Frameworks like Reflexion enabled...'). Detectors trained on web corpora associate high syntactic regularity and absent contractions with model-generated text.
2. **Consistent Human Classification:** With an aggregate score of **`37.3%`** and over **72.5%** of sentences classified as human-leaning, the document firmly satisfies the 'LIKELY HUMAN' benchmark.
3. **100% Offline & Reproducible:** Audited using the local 304M DeBERTa-v3 checkpoint (`desklib/ai-text-detector-v1.01`), ensuring privacy and complete determinism.
