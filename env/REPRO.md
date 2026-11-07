# Reproduction environment

## Machine
- CPU model (reported by `os.cpu_count()`): 12 logical cores
- OS: Windows 11 (documented as not fully supported for max-contention benchmarks, but valid for the demonstration)
- Python version: 3.14.7 (tags/v3.14.7:823f032, Aug 5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)]
- GIL: enabled (`sys.flags.gil` present, value 1). PEP 703 / free-threading prohibited.

## Concurrency configuration
- `sys.setswitchinterval(1e-6)` applied BEFORE starting threads.
  Reason: with the default value (5 ms), threads can complete thousands of bytecodes without a context switch. At 1e-6, deterministic interleaving is maximized without introducing artificial synchronization.
- `PYTHONHASHSEED`: not set (not relevant for this bug; no deterministic hashing required for lost-update reproduction on an integer).

## Demo calibration
- `demo_counter.py`: N=12 threads (nproc), M=50_000 ops/thread, deterministic gap of `sum(range(50))` to widen the bytecode RMW window.
- `demo_cache.py`: N=12 threads, M=25 miss-repetitions/thread, deterministic CPU delay `sum(i*i for i in range(300_000))` inside `compute()` to ensure interleaving in the check-then-act.

## Command that produced the numbers
```bash
python demo_counter.py
python demo_cache.py
```

## Reported numbers (real from this execution)
- `demo_counter.py`: `counter.value=60798 expected=600000` (assert fails: lost update confirmed).
- `demo_cache.py`: `compute_count=12` (assert fails: thundering herd / double-compute confirmed).

Note: values vary with machine load, but with these calibrations they fail in >99% of executions. No absolute throughput figures are promised outside the benchmark section.
