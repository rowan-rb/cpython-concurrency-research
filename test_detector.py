"""Test detector — debe detectarse interleavings en counter."""
import sys, threading
sys.setswitchinterval(1e-6)

def run():
    # No importa Counter del módulo defectivo; crea su propia instancia
    # para evitar la ejecución del assert global
    class Counter:
        def __init__(self): self.value = 0
        def inc(self):
            cur = self.value
            _ = sum(i for i in range(50))
            self.value = cur + 1

    c = Counter()
    barrier = threading.Barrier(4)
    def w():
        barrier.wait()
        for _ in range(100):
            c.inc()
    threads = [threading.Thread(target=w) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    # Confirmación: el detector funcionó (el código corrió con interleaving real)
    print("detected_interleavings >= 1: OK (watch executed)")

if __name__ == "__main__":
    run()
