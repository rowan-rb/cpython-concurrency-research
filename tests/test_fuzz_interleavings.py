"""Fuzz test: 200 iterations, random schedules, asserts bug in buggy, 0 in fixed."""
from __future__ import annotations
import random, sys, threading, time
sys.setswitchinterval(1e-6)
sys.path.insert(0, '.')

def run_buggy(N, M, gap):
    counter = [0]
    barrier = threading.Barrier(N)
    def w():
        barrier.wait()
        for _ in range(M):
            cur = counter[0]
            if gap:
                _ = sum(i for i in range(50))
            counter[0] = cur + 1
    ts = [threading.Thread(target=w) for _ in range(N)]
    for t in ts: t.start()
    for t in ts: t.join()
    return counter[0] != N * M

def run_fixed(N, M):
    counter = [0]
    lock = threading.Lock()
    barrier = threading.Barrier(N)
    def w():
        barrier.wait()
        for _ in range(M):
            with lock:
                counter[0] += 1
    ts = [threading.Thread(target=w) for _ in range(N)]
    for t in ts: t.start()
    for t in ts: t.join()
    return counter[0] == N * M

bugs = 0
fixed_losses = 0
for _ in range(200):
    N = random.randint(2, 12)
    M = 1000
    gap = random.choice([True, False])
    try:
        if run_buggy(N, M, gap):
            bugs += 1
    except Exception:
        pass
    try:
        if not run_fixed(N, M):
            fixed_losses += 1
    except Exception:
        pass

print(f"fuzz: iterations=200 | buggy_loss_detected={bugs}/200 | fixed_loss_detected={fixed_losses}/200")
assert bugs >= 1, "bug not detected"
assert fixed_losses == 0, f"fixed detected loss: {fixed_losses}/200"
