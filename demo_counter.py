"""demo_counter.py — lost update / atomicity violation.

BUG CLASS (NOT data race — GIL serialises bytecode) — lost update via
read-modify-write of a single integer under no mutual exclusion.

Bytecode exact (CPython 3.14, GIL, LOAD_ATTR version from ``self.value += 1``):
  5 LOAD_FAST_BORROW 0 (self)
  6 COPY 1
  7 LOAD_ATTR 0 (value)
  8 LOAD_SMALL_INT 1
  9 BINARY_OP 13 (+=)     # cur+1 computed in C
 10 SWAP 2
 11 STORE_ATTR 0 (value)  # writes back
 12 LOAD_CONST 1 (None)
 13 RETURN_VALUE
Interleaving between 9 (BINARY_OP) and 11 (STORE_ATTR) causes lost update.
The GIL serialises bytecode, NOT compound sequences: three events = three
potential switch points under ``setswitchinterval(1e-6)``.
"""
from __future__ import annotations

import sys
import threading
import dis

import argparse
sys.setswitchinterval(1e-6)  # aggressive context switch for determinism

parser = argparse.ArgumentParser()
parser.add_argument("--no-gap", action="store_true", help="disable CPU gap")
parser.add_argument("--gap-size", type=int, default=50, help="gap bytecode count")
if __name__ == "__main__":
    args = parser.parse_args()
else:
    args = parser.parse_args([])
NO_GAP = args.no_gap

N = 12         # threads = nproc
M = 50_000     # ops/thread (calibrated for reproducible interleaving with CPU gap)
EXPECTED = N * M

class Counter:
    def __init__(self):
        self.value = 0
    def inc(self):
        cur = self.value
        if not args.no_gap:
            _ = sum(i for i in range(args.gap_size))
        self.value = cur + 1



def main():
    # ----- bytecode evidence -----
    dis.dis(Counter().inc)
    # ----- bytecode evidence ends -----

    counter_obj = Counter()
    barrier = threading.Barrier(N)

    def worker(counter_obj_local):
        barrier.wait()
        for _ in range(M):
            counter_obj_local.inc()

    threads = []
    for _ in range(N):
        t = threading.Thread(target=worker, args=(counter_obj,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    if NO_GAP:
        print(f"no-gap: counter.value={counter_obj.value} expected={EXPECTED}")
    else:
        print(f"counter.value={counter_obj.value} expected={EXPECTED}")
        assert counter_obj.value == EXPECTED, f"LOST UPDATE: {counter_obj.value} vs {EXPECTED}"

if __name__ == "__main__":
    main()
