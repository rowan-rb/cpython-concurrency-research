import subprocess
import sys
import unittest
import os

class CounterCorrected(unittest.TestCase):
    def test_broken_no_lock(self):
        """
        Confirms failure without lock.
        We force the gap (--gap-size 50) so the failure is 100% deterministic
        and does not depend on the OS scheduler luck.
        """
        # Run the script as a subprocess to avoid import side-effects
        cmd = [sys.executable, "demo_counter.py", "--gap-size", "50"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        # The script must fail (exit code != 0)
        self.assertNotEqual(res.returncode, 0, "The script should fail (exit code != 0)")
        
        # And it must print the specific assertion
        output = res.stdout + res.stderr
        self.assertIn("LOST UPDATE", output, "The output must contain 'LOST UPDATE'")

    def test_liveness(self):
        pass

    def test_property_lock(self):
        pass

if __name__ == "__main__":
    unittest.main()
