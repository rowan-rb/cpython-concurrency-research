"""Benchmark — interleave detector overhead.

Measures worker loop N runs WITHOUT and WITH Watch().
Produces overhead_ratio = median(t_with) / median(t_without).
Also reports p95 for both.

The detector uses sys.settrace (fallback) or sys.monitoring (3.12+).
sys.settrace fires on EVERY line event → high overhead.
"""
from __future__ import annotations
import sys, time, statistics, threading
sys.setswitchinterval(1e-6)
sys.path.insert(0, '.')

from tools.interleave_detector import Watch

N = 12
M = 10000
global_counter = 0

def run_workers():
    """Run N threads × M increments without watch."""
    results = []
    def worker():
        global global_counter
        for _ in range(M):
            global_counter += 1
    threads = [threading.Thread(target=worker) for _ in range(N)]
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    return time.perf_counter() - start, global_counter

def measure(fn, runs=10):
    times = []
    for _ in range(runs):
        elapsed, _ = fn()
        times.append(elapsed)
    return times

if __name__ == "__main__":
    without = measure(run_workers)
    
    def run_with_watch():
        global global_counter
        def worker():
            global global_counter
            for _ in range(M):
                with Watch():
                    global_counter += 1
        threads = [threading.Thread(target=worker) for _ in range(N)]
        start = time.perf_counter()
        for t in threads: t.start()
        for t in threads: t.join()
        return time.perf_counter() - start, global_counter

    with_watch = measure(run_with_watch)
    
    med_without = statistics.median(without)
    med_with = statistics.median(with_watch)
    ratio = med_with / med_without if med_without > 0 else float('inf')
    
    p95_wo = statistics.quantiles(without, n=100)[94] if len(without) >= 100 else max(without)
    p95_w  = statistics.quantiles(with_watch, n=100)[94] if len(with_watch) >= 100 else max(with_watch)
    
    print(f"Without detector: median={med_without:.4f}s, p95={p95_wo:.4f}s")
    print(f"With detector:      median={med_with:.4f}s, p95={p95_w:.4f}s")
    print(f"Overhead ratio: {ratio:.2f}× (median) — p95 ratio: {p95_w/p95_wo:.2f}×")
    print(f"Runs per measurement: 10")
    print(f"Python: {sys.version.split()[0]} | GIL: {sys._is_gil_enabled()}")