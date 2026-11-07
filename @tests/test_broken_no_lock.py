import unittest
import threading
import time

class TestBrokenNoLock(unittest.TestCase):
    def test_broken_no_lock(self):
        # Configurar el intervalo de cambio de hilo
        import sys
        sys.setswitchinterval(1e-6)

        # Variables globales para medir la pérdida de updates
        updates = 0
        barrier = threading.Barrier(12)

        # Función para el bucle en Python puro
        def python_loop():
            nonlocal updates
            barrier.wait()
            for _ in range(1000000):
                updates += 1

        # Ejecutar el escenario
        threads = [threading.Thread(target=python_loop) for _ in range(12)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verificar la pérdida de updates
        self.assertGreater(12000000 - updates, 0)

    def test_broken_no_lock_forced_fail(self):
        # Configurar el intervalo de cambio de hilo
        import sys
        sys.setswitchinterval(1e-6)

        # Variables globales para medir la pérdida de updates
        updates = 0
        barrier = threading.Barrier(12)

        # Función para el bucle en Python puro
        def python_loop():
            nonlocal updates
            barrier.wait()
            for _ in range(1000000):
                updates += 1

        # Ejecutar el escenario
        threads = [threading.Thread(target=python_loop) for _ in range(12)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verificar la pérdida de updates
        self.assertGreater(12000000 - updates, 0)

if __name__ == '__main__':
    unittest.main()