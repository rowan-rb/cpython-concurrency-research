import sys
import os
import threading

# ESTA ES LA LÍNEA CLAVE QUE FALTABA: Fuerza al GIL a cambiar de hilo constantemente
sys.setswitchinterval(1e-6) 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.interleave_detector import watch

class BuggyCounter:
    def __init__(self): self.value = 0
    def inc(self):
        cur = self.value
        sum(range(50)) # artificial gap
        self.value = cur + 1

class SafeCounter:
    def __init__(self): 
        self.value = 0
        self.lock = threading.Lock()
    def inc(self):
        with self.lock:
            cur = self.value
            sum(range(50)) # artificial gap inside lock
            self.value = cur + 1

def run_accuracy_test():
    print("--- DETECTOR ACCURACY BENCHMARK (100 runs) ---")
    false_positives = 0
    false_negatives = 0
    true_positives = 0
    true_negatives = 0

    n_threads = 12
    
    for i in range(100):
        # 1. Test Buggy
        c_buggy = BuggyCounter()
        with watch(classes=[BuggyCounter]) as w:
            # Create threads INSIDE the watch block
            threads = [threading.Thread(target=lambda: [c_buggy.inc() for _ in range(100)]) for _ in range(n_threads)]
            for t in threads: t.start()
            for t in threads: t.join()
            
        if w.detected_interleavings > 0:
            true_positives += 1
        else:
            false_negatives += 1

        # 2. Test Safe
        c_safe = SafeCounter()
        with watch(classes=[SafeCounter]) as w:
            threads = [threading.Thread(target=lambda: [c_safe.inc() for _ in range(100)]) for _ in range(n_threads)]
            for t in threads: t.start()
            for t in threads: t.join()
            
        if w.detected_interleavings > 0:
            false_positives += 1
        else:
            true_negatives += 1

    print(f"True Positives (Bug caught):   {true_positives}/100")
    print(f"False Negatives (Bug missed):  {false_negatives}/100")
    print(f"True Negatives (Safe cleared): {true_negatives}/100")
    print(f"False Positives (False alarm): {false_positives}/100")
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    print(f"\nPrecision: {precision*100:.1f}%")

if __name__ == "__main__":
    run_accuracy_test()
