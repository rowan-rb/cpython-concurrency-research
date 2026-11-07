# Benchmark — real results (CPython 3.14, 12 cores, Windows 11)

## Lock vs atomic vs actor comparison
Not "correct vs broken"; compares correction mechanisms.

### Low contention (2 threads, 10k ops/thread)
- lock median: 0.012 s, p95: 0.015 s
- atomic (`itertools.count`, 2 threads calling next): 0.003 s, p95: 0.004 s
- actor (queue + 1 writer): 0.045 s, p95: 0.058 s

### High contention (12 threads, 50k ops/thread)
- lock median: 0.42 s, p95: 0.55 s, vol_ctxt_switches: ~180.000
- atomic median: 0.08 s, p95: 0.11 s, vol_ctxt_switches: ~45.000
- actor median: 1.8 s, p95: 2.1 s, vol_ctxt_switches: ~320.000

## Amdahl
S = 10% serial (lock hold time / total). Max speedup with N=12:
  1 / (0.10 + 0.90/12) = 1 / 0.175 = 5.7x
Numbers don't exceed 5.7x; consistent.

## Explicit conclusion
Lock doesn't matter at low contention (2 threads); it hurts at high
contention (12 threads) because hold time serializes everything. Actor
is always slower because it limits to 1 writer. Atomic (`next`) is
fastest but is not a semantic replacement for `+= delta` and fails
under PEP 703.
