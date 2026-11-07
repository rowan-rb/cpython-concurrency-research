"""Cache test — demonstrates failure without pytest.
Does NOT cover persistence, multiprocess, distributed consensus.
"""
import sys, unittest
sys.path.insert(0, '.')

class CacheBroken(unittest.TestCase):
    def test_broken_no_lock(self):
        import subprocess, sys
        # Intentar varias veces; con calibración alta falla >99%
        failed = False
        for _ in range(3):
            res = subprocess.run([sys.executable, "demo_cache.py"], capture_output=True, text=True, timeout=15)
            if res.returncode != 0 and "BUG" in res.stderr:
                failed = True
                break
        self.assertTrue(failed, "BUG NOT REPRODUCED: demo_cache.py should fail with double-compute in at least one run")

if __name__ == "__main__":
    unittest.main()
