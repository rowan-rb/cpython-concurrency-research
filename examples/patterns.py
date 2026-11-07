"""Patterns where this bug typically appears in production.
This is NOT real code from a production repo. It is a list of
patterns to help you recognize the bug in YOUR code.
For detection on your own code: tools/interleave_detector.py
For real measurements, see demo_counter.py and demo_cache.py.
"""
from __future__ import annotations
import threading, sys
sys.setswitchinterval(1e-6)

class MetricsCounter:
    """Metrics counter — loses updates without lock."""
    def __init__(self):
        self.value = 0

    def increment(self):
        cur = self.value
        # Realistic window: brief computation simulation
        _ = sum(i for i in range(50))
        self.value = cur + 1

def buggy():
    mc = MetricsCounter()
    barrier = threading.Barrier(12)
    def w():
        barrier.wait()
        for _ in range(50000):
            mc.increment()
    ts = [threading.Thread(target=w) for _ in range(12)]
    for t in ts: t.start()
    for t in ts: t.join()
    lost = (12 * 50000 - mc.value) / (12 * 50000)
    print(f"buggy: value={mc.value}, loss_rate={lost:.0%}")

class FixedMetricsCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    def increment(self):
        with self.lock:
            self.value += 1

def fixed():
    mc = FixedMetricsCounter()
    barrier = threading.Barrier(12)
    def w():
        barrier.wait()
        for _ in range(50000):
            mc.increment()
    ts = [threading.Thread(target=w) for _ in range(12)]
    for t in ts: t.start()
    for t in ts: t.join()
    assert mc.value == 12 * 50000
    print("fixed: value=600000, loss_rate=0%")

if __name__ == "__main__":
    buggy()
    fixed()
