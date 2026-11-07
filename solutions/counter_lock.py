"""Solution 1 — threading.Lock (mutual exclusion).
Invariant restored: no update is lost (counter final == N*M).
Consistency model: linearizable (each += is atomic; happens-before through
  lock release/acquire).
Cost: hold time = duration of `self.value += 1` (~microseconds); added latency = wait time in lock queue.
When NOT to use: high contention with long operations inside the lock; doesn't scale to multiprocess or distributed node.
"""
from __future__ import annotations
import threading, sys
sys.setswitchinterval(1e-6)

# Restores invariant: no lost updates (linearizable under GIL).
N, M = 12, 50000
counter = 0
lock = threading.Lock()
barrier = threading.Barrier(N)
