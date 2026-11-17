# Reproducibility: Environment Diagnostic and Specification

**Date of Diagnostic:** 2026-11-04  
**Project:** Verification Scheduling in Long-Horizon Agent Workflows (G4)  
**Institution:** Indian Institute of Information Technology, Allahabad  
**Student:** Harsh Sharma  
**Diagnostic Script:** `scripts/check_environment.py`

---

## 1. Operating System and Hardware

All measurements were directly obtained via `scripts/check_environment.py` on the execution host:

| Attribute | Measured Value | Verification Status |
|---|---|---|
| **Operating System** | Microsoft Windows 11 Pro / Enterprise (64-bit) | VERIFIED |
| **OS Version / Build** | 10.0.26300 (SP0) | VERIFIED |
| **Platform** | `Windows-11-10.0.26300-SP0` | VERIFIED |
| **CPU Architecture** | `AMD64` (Family 26 Model 96 Stepping 0, AuthenticAMD) | VERIFIED |
| **Physical CPU Cores** | 8 | VERIFIED |
| **Logical CPU Threads** | 16 | VERIFIED |
| **CPU Base Frequency** | 2000.0 MHz | VERIFIED |
| **Total Physical RAM** | 21.79 GB | VERIFIED |
| **Available RAM** | 3.89 GB (at diagnostic invocation) | VERIFIED |
| **RAM Utilization** | 82.2% | VERIFIED |
| **Primary Disk** | Drive `C:\` | VERIFIED |
| **Total Disk Capacity** | 951.65 GB | VERIFIED |
| **Free Disk Capacity** | 668.31 GB | VERIFIED |
| **Hardware Accelerator / GPU** | No CUDA-capable GPU detected (CPU-only build: `torch 2.14.0+cpu`, `cuda_available: False`, `device_count: 0`) | VERIFIED |

---

## 2. Python Runtime and Virtual Environment

| Attribute | Specification | Verification Status |
|---|---|---|
| **Python Version** | Python 3.14.6 (MSC v.1944 64 bit AMD64) | VERIFIED |
| **Base Python Binary** | `C:\Python314\python.exe` | VERIFIED |
| **Project Virtual Env** | `AITR_Lab02_MSE2026006\.venv` | VERIFIED |
| **Venv Python Binary** | `AITR_Lab02_MSE2026006\.venv\Scripts\python.exe` | VERIFIED |
| **Package Installer** | `pip 26.1.2` | VERIFIED |

---

## 3. Dependency Inventory and Versions

The project follows a strict minimal-dependency philosophy. For Phase E baseline implementation, the required libraries and their exact pinned versions in the virtual environment are:

| Package | Pinned Version | Purpose in G4 Implementation | Verification Status |
|---|---|---|---|
| `numpy` | `2.5.4` | Matrix computations, numeric invariants, and array indexing | VERIFIED |
| `scipy` | `1.18.1` | Nonparametric bootstrap resampling and statistical hypothesis testing | VERIFIED |
| `networkx` | `3.7` | DAG topology representation, topological sorting, and descendant reachability | VERIFIED |
| `pytest` | `9.2.0` | Comprehensive unit and integration test suite | VERIFIED |
| `colorama` | `0.4.6` | Terminal test runner formatting | VERIFIED |
| `iniconfig` | `2.3.1` | Test configuration parser | VERIFIED |
| `packaging` | `26.3` | Version specification handling | VERIFIED |
| `pluggy` | `1.7.0` | Plugin management for pytest | VERIFIED |
| `pygments` | `2.21.0` | Syntax highlighting for test tracebacks | VERIFIED |

*Note: All core workflow execution, schema contract validation, snapshot serialization, and logging modules use Python's built-in standard library (`json`, `dataclasses`, `typing`, `hashlib`, `math`, `time`, `logging`, `copy`, `uuid`) to maximize speed, eliminate memory leaks, and ensure complete portability across operating systems.*

---

## 4. API and External Model Credentials

An audit of the process environment variables confirmed that **no external LLM API keys are configured**:
- `OPENAI_API_KEY`: NOT SET
- `ANTHROPIC_API_KEY`: NOT SET
- `GEMINI_API_KEY`: NOT SET
- `GOOGLE_API_KEY`: NOT SET

**Scientific Consequence:** The experimental study is strictly and purely scoped to the **deterministic core**, which requires zero external model calls, incurs zero financial cost, and provides 100% deterministic reproducibility.
