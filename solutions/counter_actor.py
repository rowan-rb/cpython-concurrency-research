"""Solution 3 — queue.Queue + 1 worker (actor / single-writer).
Invariant: all updates go through a single writer, so write order is serial (serializable).
Consistency model: serializable (single thread writes). Happens-before
  by order of reception in the queue.
Cost: latency = time in queue + processing; throughput limited by 1 worker.
When NOT to use: high contention with many writes; doesn't scale; if
  the worker dies, pending updates are lost (no persistence).
"""
from __future__ import annotations
import sys, threading, queue
sys.setswitchinterval(1e-6)

# Restores invariant: serializable writes via single writer; not linearizable.
N = 12; M = 50000
q = queue.Queue()
counter = 0

def worker_writer():
    global counter
    while True:
        delta = q.get()
        if delta is None:
            break
        counter += delta

tw = threading.Thread(target=worker_writer, daemon=True)
tw.start()
barrier = threading.Barrier(N)

def task():
    barrier.wait()
    for _ in range(M):
        q.put(1)

threads = [threading.Thread(target=task) for _ in range(N)]
for t in threads: t.start()
for t in threads: t.join()
q.put(None); tw.join()
print(f"actor: {counter} expected={N*M}")
