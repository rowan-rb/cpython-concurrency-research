"""demo_cache.py — TOCTOU / double-compute / stale-read on dict cache.

BUG CLASS (NOT data race): atomicity violation of a compound check-then-act on a
shared ``dict``. The miss path (key not present -> compute -> insert) is not
atomic. Interleaving yields:
  1) Double-compute: two threads compute same key.
  2) Stale-read: one thread reads after insert but before second write, or
     reads a partially constructed value.

The GIL makes each dict operation atomic (load/store), not the sequence.
Fixed form: ``with lock: if k not in d: d[k]=compute()`` ensures serialisable.
"""
from __future__ import annotations

import sys
import threading
import time
import logging

sys.setswitchinterval(1e-6)

N = 12        # threads = nproc (max contention)
M = 25        # miss attempts per thread (many chances for interleaving)
EXPECTED_UNIQUE = 1  # We expect only 1 compute for a given key; failure = >1

d = {}
barrier = threading.Barrier(N)
compute_count = 0  # observable counter of how many times compute() ran
compute_lock = threading.Lock()  # reference for comparison, NOT used in buggy path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)s %(levelname)s %(message)s")
log = logging.getLogger("cache")


def compute(key: str) -> str:
    global compute_count
    with compute_lock:
        compute_count += 1
        cur = compute_count
    # Deterministic CPU-intensive delay (no time.sleep) to widen interleaving window
    # without introducing artificial synchronization.
    _ = sum(i * i for i in range(300_000))
    result = f"value_for_{key}_count_{cur}"
    # Small deterministic window: force interleaving
    # We do NOT use time.sleep(); instead we rely on switchinterval to interleave.
    return result


def buggy_access(key: str):
    """Check-then-act: NOT atomic. TOCTOU."""
    global d, compute_count
    barrier.wait()
    # TOCTOU: check
    if key not in d:
        # ACT: compute (long relative to bytecode)
        val = compute(key)
        # Insert (two bytecode events, could interleave)
        d[key] = val
    return d.get(key)


def main():
    threads = []
    for _ in range(N):
        def task():
            barrier.wait()
            for _ in range(M):
                buggy_access("shared_key")
        t = threading.Thread(target=task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    # After all threads finish
    log.info("compute_count=%d d=%s", compute_count, d)
    # BUG IS VISIBLE WHEN compute_count > 1 (thundering herd / double compute).
    assert compute_count == 1, f"BUG: double-compute / thundering herd detected compute_count={compute_count} (expected 1, got >1)"

if __name__ == "__main__":
    main()
