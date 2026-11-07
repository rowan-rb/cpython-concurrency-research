import sys
import threading
import time

sys.setswitchinterval(1e-6)

class Counter:
    def __init__(self):
        self.value = 0

def run_test(name, gap_type, n_threads=12, iterations=50000):
    counter = Counter()
    barrier = threading.Barrier(n_threads)

    def worker():
        barrier.wait()
        for _ in range(iterations):
            cur = counter.value
            if gap_type == "py_loop":
                for _ in range(5): pass
            elif gap_type == "sum_0":
                sum(range(0))
            elif gap_type == "sum_50":
                sum(range(50))
            counter.value = cur + 1

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    
    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    end = time.perf_counter()

    expected = n_threads * iterations
    lost = expected - counter.value
    
    print(f"[{name}] Updates esperados: {expected}")
    print(f"[{name}] Updates perdidos:  {lost}")
    print(f"[{name}] Tiempo: {end - start:.4f} segundos\n")

if __name__ == "__main__":
    print("--- DEMOSTRACION DEL MECANISMO DEL GIL ---\n")
    run_test("Python loop puro (FOR_ITER)", "py_loop")
    run_test("sum(range(0)) (C-loop vacio)", "sum_0")
    run_test("sum(range(50)) (C-loop lleno)", "sum_50")
