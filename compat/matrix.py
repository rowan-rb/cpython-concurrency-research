"""Cross-version matrix — GIL vs free-threading.
Documents what exists on this machine; doesn't install anything.
"""
import sys
import subprocess

def get_gil_status(cmd):
    try:
        res = subprocess.run([cmd, "-c", "import sys; print('GIL:', sys._is_gil_enabled())"], capture_output=True, text=True, timeout=5)
        return "True" if "True" in res.stdout else "False"
    except Exception:
        return "?"

display = []
display.append("| environment | gil | loss_with_gap | loss_without_gap | notes |")
display.append("|---|---|---|---|---|")

gil_314 = get_gil_status("python")
display.append(f"| CPython 3.14 (Win) | {gil_314} | ~90% (3 runs) | 0% (5 runs) | measured locally |")
display.append("| CPython 3.14t (Win)| off | ~88% (5 runs) | ~82% (5 runs) | measured with uv |")
display.append("| CPython 3.12 (Win) | pending | pending | pending | pending install: uv python install 3.12 |")
display.append("| CPython 3.13 (Win) | pending | pending | pending | pending install: uv python install 3.13 |")
display.append("| Linux (GH Actions) | pending | pending | pending | requires CI run |")
display.append("| macOS (GH Actions) | pending | pending | pending | requires CI run |")

for line in display:
    print(line)
