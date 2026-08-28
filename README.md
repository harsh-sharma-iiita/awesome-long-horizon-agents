# Awesome Long-Horizon LLM Agents

A curated academic repository on **long-horizon agents**: AI systems that plan, act, remember, execute tools, recover from failure, and sustain useful behavior across many sequential steps.

This repository connects an AI-assisted research paper with a verified literature collection, benchmarks/datasets, tools, implementations, and learning resources. The curation emphasizes **planning, memory/context management, execution reliability, recovery, evaluation, and autonomous research**.

> **Verification note:** Research-paper metadata was checked against arXiv, conference proceedings, publisher pages, or official project pages. The repository deliberately avoids uploading third-party copyrighted paper PDFs; it links to official/open-access sources instead.

## Contents

- [Overview](#overview)
- [AI-Assisted Research Paper](#ai-assisted-research-paper)
- [Survey and Review Papers](#survey-and-review-papers)
- [Foundational Papers](#foundational-papers)
- [Recent Research](#recent-research)
- [Benchmarks and Datasets](#benchmarks-and-datasets)
- [Tools and Libraries](#tools-and-libraries)
- [GitHub Implementations](#github-implementations)
- [Tutorials and Learning Resources](#tutorials-and-learning-resources)
- [Citation Integrity Audit](#citation-integrity-audit)
- [Repository Structure](#repository-structure)
- [License](#license)

## Overview

Long-horizon LLM agents go beyond one-shot question answering by maintaining a goal while interacting with tools and environments through many dependent actions. Their difficulty is not simply that a task is long. A long task also creates opportunities for **planning errors, state loss, context degradation, execution failures, goal drift, poor credit assignment, and irreversible early commitments**. Recent work therefore treats the agent as a system composed of a model plus a harness for planning, memory, execution, evaluation, and recovery.

Early approaches such as ReAct interleave reasoning and acting, while Plan-and-Solve and Tree of Thoughts make decomposition or search more explicit. Later systems add reflection, tree search, persistent skill libraries, multi-agent collaboration, and computer-use interfaces. Benchmarking work such as AgentBench, WebArena, GAIA, MLE-bench, and TheAgentCompany makes the problem concrete by requiring agents to complete multi-step tasks in interactive environments.

A newer research frontier is **autonomous scientific research**, where an agent proposes ideas, implements experiments, evaluates results, revises its direction, and writes a report. Current work suggests that long-horizon reliability depends as much on workflow architecture, state management, verification, and recovery as on raw model capability. The central question is therefore shifting from *Can an LLM reason?* to *Can an agent sustain a verified objective across a long sequence of actions?*

## AI-Assisted Research Paper

**Title:** *Long-Horizon LLM Agents: Planning, Memory, Execution, Recovery, and Autonomous Research*

**Description:** A compact literature synthesis prepared for this repository, connecting classical reasoning/acting methods with current research on long-horizon execution and AI-for-science systems.

- [Read the paper PDF](paper/AI_Assisted_Research_Paper.pdf)
- [Read the editable paper source](paper/AI_Assisted_Research_Paper.md)

> If an earlier course paper was already submitted, replace the companion paper above with that original PDF while keeping the repository structure unchanged.

## Survey and Review Papers

- **Towards Long-Horizon Agents: A Survey** — Dong et al., 2026. A broad survey organizing long-horizon agents across foundations, harnesses, optimization, applications, and frontier problems. [[Paper](https://long-horizon-agents.github.io/)]
- **AI for Auto-Research: Roadmap & User Guide** — Kong et al., 2026. Maps automation across creation, writing, validation, and dissemination while emphasizing the boundary between reliable assistance and unreliable autonomy. [[arXiv](https://arxiv.org/abs/2605.18661)]
- **The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents** — Chen et al., 2026. Distinguishes long-horizon tasks, long-context models, and persistent memory systems. [[arXiv](https://arxiv.org/abs/2608.06663)]

## Foundational Papers

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al., ICLR 2023. Introduces interleaved reasoning and action so agents can update plans using environment feedback. [[Paper](https://arxiv.org/abs/2210.03629)]
- **Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models** — Wang et al., ACL 2023. Separates planning from execution to reduce missing-step errors in multi-step reasoning. [[Paper](https://arxiv.org/abs/2305.04091)]
- **Tree of Thoughts: Deliberate Problem Solving with Large Language Models** — Yao et al., NeurIPS 2023. Explores multiple intermediate reasoning paths and supports lookahead/backtracking. [[Paper](https://arxiv.org/abs/2305.10601)]
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn et al., NeurIPS 2023. Uses linguistic feedback and episodic reflective memory instead of parameter updates. [[Paper](https://arxiv.org/abs/2303.11366)]
- **Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models** — Zhou et al., ICML 2024. Combines LLM reasoning, acting, Monte Carlo tree search, value estimation, and self-reflection. [[Paper](https://proceedings.mlr.press/v235/zhou24r.html)]
- **Voyager: An Open-Ended Embodied Agent with Large Language Models** — Wang et al., 2023. Demonstrates automatic curriculum, an executable skill library, and iterative self-improvement in Minecraft. [[Paper](https://arxiv.org/abs/2305.16291)]
- **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation** — Wu et al., COLM 2024. Provides a framework for composing multiple conversational agents with tools and human participation. [[Paper](https://arxiv.org/abs/2308.08155)]
- **Generative Agents: Interactive Simulacra of Human Behavior** — Park et al., UIST 2023. Shows how memory, reflection, and planning can support persistent agent behavior. [[Paper](https://arxiv.org/abs/2304.03442)]

## Recent Research

- **Why Reasoning Fails to Plan: A Planning-Centric Analysis of Long-Horizon Decision Making in LLM Agents** — Wang et al., 2026. Argues that step-wise reasoning can create myopic commitments; proposes FLARE for future-aware lookahead. [[arXiv](https://arxiv.org/abs/2601.22311)]
- **AI Scientists Fail Without Strong Implementation Capability** — Zhu et al., 2025. Identifies an implementation/verification bottleneck in AI-scientist systems. [[arXiv](https://arxiv.org/abs/2506.01372)]
- **AI for Auto-Research: Roadmap & User Guide** — Kong et al., 2026. Surveys the complete research lifecycle and highlights reliability gaps in scientific judgment and experiments. [[arXiv](https://arxiv.org/abs/2605.18661)]
- **ScienceFlow: A Long-Horizon Agent for ML Research, Scientific Discovery and Beyond** — Zhao et al., 2026. Uses research segments, recoverable executable states, re-anchoring, and resource-aware execution for autonomous research. [[arXiv](https://arxiv.org/abs/2608.14354)]
- **FARS: A Fully Automated Research System Deployed at Scale** — Tang et al., 2026. Reports a large public deployment of an automated research system spanning ideation, planning, experiments, and paper writing. [[arXiv](https://arxiv.org/abs/2606.31651)]
- **The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents** — Chen et al., 2026. Surveys the long-horizon lifecycle and identifies measurement and credit-assignment challenges. [[arXiv](https://arxiv.org/abs/2608.06663)]
- **The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs** — Sinha et al., 2025. Separates execution capability from reasoning and studies how errors compound over longer sequences. [[arXiv](https://arxiv.org/abs/2509.09677)]
- **LEAD: Breaking the No-Recovery Bottleneck in Long-Horizon Reasoning** — Pushkin & Abbe, 2026. Studies over-decomposition and introduces short-horizon validation with overlapping rollouts. [[arXiv](https://arxiv.org/abs/2603.06870)]
- **Long-Horizon Autonomous Architecture Research with a Language-Model Agent: A Behavioural Case Study** — Safdar & Saadeldin, 2026. Examines long-run architecture experimentation and workflow-induced greedy behavior. [[arXiv](https://arxiv.org/abs/2608.01995)]
- **Learning Agent-Compatible Context Management for Long-Horizon Tasks** — Yi et al., 2026. Introduces AdaCoM, an external learned context manager for a frozen agent. [[arXiv](https://arxiv.org/abs/2605.30785)]
- **AI Scientist via Synthetic Task Scaling** — Cai & Behl, 2026. Builds synthetic ML research tasks to train agents that learn from execution trajectories. [[arXiv](https://arxiv.org/abs/2603.17216)]
- **The Age of AI Agents Demands A New Scientific Paradigm To Sustain Trustworthy Science** — Mo, 2026. Argues for observable workflows, scalable verification, and clear attribution in AI-mediated science. [[arXiv](https://arxiv.org/abs/2607.26064)]
- **AgentBench: Evaluating LLMs as Agents** — Liu et al., ICLR 2024. Multi-environment evaluation showing long-term reasoning and decision-making remain major bottlenecks. [[Paper](https://arxiv.org/abs/2308.03688)]
- **WebArena: A Realistic Web Environment for Building Autonomous Agents** — Zhou et al., ICLR 2024. Provides a realistic, reproducible web environment with long-horizon tasks. [[Paper](https://arxiv.org/abs/2307.13854)]
- **GAIA: a benchmark for General AI Assistants** — Mialon et al., 2023. Tests multi-step assistants on reasoning, multimodality, browsing, and tool use. [[Paper](https://arxiv.org/abs/2311.12983)]
- **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** — Yang et al., 2024. Studies how specialized computer interfaces affect autonomous software-engineering execution. [[Paper](https://arxiv.org/abs/2405.15793)]
- **OpenHands: An Open Platform for AI Software Developers as Generalist Agents** — Wang et al., ICLR 2025. Provides a general agent platform with code execution, browsing, evaluation, and sandboxing. [[Paper](https://arxiv.org/abs/2407.16741)]
- **MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering** — Chan et al., ICLR 2025. Benchmarks ML engineering agents on 75 Kaggle competitions. [[Paper](https://arxiv.org/abs/2410.07095)]
- **TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks** — Xu et al., 2024. Evaluates agents as digital workers in a simulated software company. [[Paper](https://arxiv.org/abs/2412.14161)]

## Benchmarks and Datasets

- **WebArena** — Realistic, self-hostable web environment and benchmark for long-horizon browser tasks. [[Project](https://webarena.dev/)] [[Code](https://github.com/web-arena-x/webarena)]
- **MLE-bench** — 75 Kaggle competitions for evaluating machine-learning engineering agents. [[Project/Paper](https://arxiv.org/abs/2410.07095)] [[Code](https://github.com/openai/mle-bench)]
- **TheAgentCompany** — Self-contained software-company environment with consequential workplace tasks. [[Project](https://the-agent-company.com/)] [[Code](https://github.com/TheAgentCompany/TheAgentCompany)]
- **GAIA** — Benchmark for general assistants requiring reasoning, browsing, multimodality, and tool use. [[Benchmark](https://huggingface.co/gaia-benchmark)] [[Paper](https://arxiv.org/abs/2311.12983)]

## Tools and Libraries

- **LangGraph** — Low-level orchestration for long-running, stateful agents with persistence, branching, and human-in-the-loop control. [[Docs](https://docs.langchain.com/oss/python/langgraph/overview)] [[GitHub](https://github.com/langchain-ai/langgraph)]
- **AutoGen** — Multi-agent application framework for conversational coordination among agents, tools, and humans. [[Docs](https://microsoft.github.io/autogen/)] [[GitHub](https://github.com/microsoft/autogen)]
- **LlamaIndex** — Framework for building agentic applications with data connectors, retrieval, workflows, and agent abstractions. [[Docs](https://developers.llamaindex.ai/)] [[GitHub](https://github.com/run-llama/llama_index)]
- **CrewAI** — Framework for collaborative agents, crews, flows, memory, guardrails, and long-running workflow orchestration. [[Docs](https://docs.crewai.com/)] [[GitHub](https://github.com/crewAIInc/crewAI)]
- **smolagents** — Lightweight agent library with code agents and tool-calling agents, including multi-step execution patterns. [[Docs](https://huggingface.co/docs/smolagents/)] [[GitHub](https://github.com/huggingface/smolagents)]

## GitHub Implementations

- **Reflexion** — Official implementation of the verbal reinforcement learning / reflective-memory agent. [[GitHub](https://github.com/noahshinn024/reflexion)]
- **Language Agent Tree Search (LATS)** — Official implementation of LATS combining reasoning, acting, search, and reflection. [[GitHub](https://github.com/lapisrocks/LanguageAgentTreeSearch)]
- **Tree of Thoughts** — Official code and prompts for deliberate tree-structured reasoning. [[GitHub](https://github.com/princeton-nlp/tree-of-thought-llm)]
- **SWE-agent** — Research implementation for autonomous software engineering through a specialized agent-computer interface. [[GitHub](https://github.com/SWE-agent/SWE-agent)]
- **OpenHands** — Open platform for developing agents that write code, use terminals, browse, and work in sandboxes. [[GitHub](https://github.com/All-Hands-AI/OpenHands)]
- **WebArena** — Benchmark environment and reproduction resources for realistic browser-based agent evaluation. [[GitHub](https://github.com/web-arena-x/webarena)]
- **MLE-bench** — Benchmark construction and evaluation code for ML-engineering agents. [[GitHub](https://github.com/openai/mle-bench)]

## Tutorials and Learning Resources

- **Hugging Face Agents Course** — End-to-end course covering agent fundamentals, tools, the ReAct loop, smolagents, LlamaIndex, LangGraph, evaluation, and a GAIA project. [[Course](https://huggingface.co/learn/agents-course/en/unit0/introduction)]
- **LangGraph Documentation** — Official guides for state, graphs, loops, persistence, streaming, and durable agent orchestration. [[Docs](https://docs.langchain.com/oss/python/langgraph/overview)]
- **AutoGen Documentation** — Official tutorials and guides for multi-agent conversations, tools, code execution, and orchestration. [[Docs](https://microsoft.github.io/autogen/)]
- **CrewAI Documentation** — Official guides for agents, flows, memory, knowledge, guardrails, and long-running workflows. [[Docs](https://docs.crewai.com/)]
- **smolagents Documentation** — Official guides for code agents, tool use, multi-step execution, memory, RAG, browser agents, and human-in-the-loop patterns. [[Docs](https://huggingface.co/docs/smolagents/)]

## Citation Integrity Audit

The original source list contained several duplicates and two non-scholarly resources. A corrected audit is provided here:

- [Open the Citation Integrity Audit](citation-audit/Citation_Integrity_Audit.pdf)
- [Open the editable audit](citation-audit/Citation_Integrity_Audit.md)

## Repository Structure

```text
awesome-long-horizon-agents/
|-- README.md
|-- paper/
|   |-- AI_Assisted_Research_Paper.pdf
|   `-- AI_Assisted_Research_Paper.md
|-- citation-audit/
|   |-- Citation_Integrity_Audit.pdf
|   `-- Citation_Integrity_Audit.md
|-- references/
|   `-- references.md
|-- datasets/
|   `-- datasets.md
|-- tools/
|   `-- tools.md
|-- implementations/
|   `-- github-repositories.md
|-- tutorials/
|   `-- tutorials.md
`-- LICENSE
```

## License

This repository's original curation text and original summaries are released under the MIT License. Third-party papers, code, datasets, logos, and trademarks remain under their respective licenses.
