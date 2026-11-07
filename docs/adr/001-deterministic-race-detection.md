# ADR 001: Deterministic Race Detection

## Context
Our regression tests (`test_broken_no_lock`) need to verify that the un-locked counter loses updates. Initially, the test relied on the OS scheduler to naturally interleave threads during a bare `counter.value += 1`. However, due to CPython 3.14's optimizations and the GIL, this RMW (Read-Modify-Write) often completes in 0% loss without an artificial gap. This made the test flaky.

## Decision
We force the race condition deterministically by injecting a known C-level yield point (`sum(range(50))`) between the `LOAD_ATTR` and `STORE_ATTR` instructions. The test invokes the script via `subprocess` with the `--gap-size 50` flag, guaranteeing a lost update.

## Consequences
- **Positive:** The test is 100% deterministic and no longer depends on OS scheduling luck. It passes on any machine, every time.
- **Negative:** The test measures a calibrated race, not a naturally occurring one. We must clearly document this distinction (see `docs/execution-model.md`).
