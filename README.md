[![GIL Concurrency Tests](https://github.com/rowan-rb/cpython-concurrency-research/actions/workflows/ci.yml/badge.svg)](https://github.com/rowan-rb/cpython-concurrency-research/actions/workflows/ci.yml)

# The GIL doesn't save you: Silent Lost Updates in CPython

[![Python 3.14](https://img.shields.io/badge/Python-3.12_|_3.13_|_3.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A deep-dive engineering analysis into CPython concurrency. This project proves that `counter += 1` is **not atomic**, even with the Global Interpreter Lock (GIL) active. We demonstrate this using bytecode disassembly, probabilistic modeling, and empirical benchmarks, including evidence from **PEP 703 (Free-Threading)**.

## Executive Summary
In distributed and multi-threaded systems, the GIL prevents memory corruption but does not provide transactional guarantees. A Read-Modify-Write (RMW) operation consists of multiple bytecodes. If a thread switch occurs between the `LOAD_ATTR` and the `STORE_ATTR`, updates are silently lost. 

This repository serves as an **AI Code Evaluation Artifact**: it provides the methodology and tools to detect and quantify concurrency vulnerabilities in Python code that might otherwise look perfectly safe to an LLM or a Junior Developer.

## Key Findings (The Data)
- **The Illusion of Safety:** A bare `counter += 1` loses **0 updates in short CI tests**. This is why this bug passes code reviews and explodes in production.
- **The `eval_breaker` Discovery:** We proved that an empty C-level loop (`sum(range(0))`) is enough to trigger a context switch. The thread yield does not happen due to Python's `FOR_ITER`, but because CPython's C-loops check `eval_breaker` in `ceval.c`.
- **The PEP 703 Catastrophe:** Measured on Python 3.14t (Free-Threading). Without the GIL, the exact same code that had 0% loss now loses **~82% of updates** without any artificial help.
- **Predictive Accuracy:** Built a probabilistic model that predicts the exact loss rate based on thread contention and window size, achieving an **RMSE of 0.0051** (99.5% accuracy).

## Architecture & Methodology
1. **Bytecode-Level Proof:** We use `dis` to show the exact `LOAD_ATTR`, `BINARY_OP`, `STORE_ATTR` sequence and explain why the GIL is not a transaction.
2. **Controlled Reproduction:** We introduce a `--gap-size` flag to artificially widen the execution window (simulating GC pauses or I/O). This allows us to deterministically reproduce the race condition.
3. **Probabilistic Modeling:** The `model/loss_probability.py` script runs thousands of iterations to compare theoretical probabilities against empirical reality.
4. **Cross-Version Benchmarking:** Automated testing across Python 3.12, 3.13, and 3.14 (with and without GIL).

## How to Run & Evaluate
1. Install dependencies (none required, stdlib only):
   pip install -e .
2. Run the deterministic bug reproduction:
   python demo_counter.py
3. Run the probabilistic mathematical model:
   python model/loss_probability.py --all
4. Run the full automated verification suite:
   .\verify.ps1

## Limitations & Open Questions
- **Hardware Dependence:** Context switch frequency depends heavily on OS schedulers (Windows vs Linux) and CPU cache.
- **Micro-benchmarking:** The 90% loss figure requires an artificial gap. In production, the loss rate is lower but completely unpredictable (triggered by GC or I/O).
- **Open Question:** Does PEP 703 require a complete rewrite of all `itertools` and `collections` documentation to warn about the loss of implicit atomicity?

## Relevance for AI Evaluation
LLMs constantly generate code with implicit RMW operations (e.g., updating a shared dictionary or a global counter) assuming the GIL makes it safe. This repository provides the **exact rebuttal** to that hallucination, proving that AI-generated code must use explicit locks or atomic data structures.
