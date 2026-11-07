"""Solution 2 — itertools.count (atomic per op under GIL, NOT drop-in).
Invariant: each `next()` call is atomic (linearizable) under GIL because
  the bytecode of `next()` is a single C call; however it is NOT a
  semantic replacement for `counter += delta` (variable delta, accumulation
  by step, not just exact sequential counting).
Consistency model: linearizable (each next is atomic; serializable if
  a single shared counter and no intermediate reads).
Cost: near zero (C call); latency = Python -> C overhead.
When NOT to use: (i) if you need `+= delta` with arbitrary delta,
  (ii) if you use PEP 703 (free-threading) — `next()` loses its
  atomicity guarantee because py-methods can be interrupted; (iii) if
  you need persistence or distributed consensus.
REQUIRED WARNING: DO NOT present as semantic equivalent of `+= delta`.
"""
from __future__ import annotations
import sys, itertools, threading
sys.setswitchinterval(1e-6)

# Restores invariant: each next() is atomic, but NOT drop-in for += delta.
N = 12
counter = itertools.count()
barrier = threading.Barrier(N)

# NOT drop-in: next(counter) always adds 1, does not accept delta.
# Documented limitation: PEP 703 breaks this guarantee.
