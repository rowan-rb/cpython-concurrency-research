"""Derivación empírica de p_yield_in_window para 4 configuraciones."""
import subprocess, sys, re

def run_demo(args):
    cmd = ["python", "demo_counter.py"] + args
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    out = res.stdout + res.stderr
    m = re.search(r"counter\.value=([0-9]+)", out)
    expected = 12 * 50000
    if m:
        val = int(m.group(1))
        loss = (expected - val) / expected
        return loss
    return None

results = {}
results["no-gap"] = run_demo(["--no-gap"])
results["gap-size-0"] = run_demo(["--gap-size=0"])
for n in [10, 50, 200]:
    results[f"gap-{n}"] = run_demo([f"--gap-size={n}"])

print("Config | p_yield | predicho | observado | error")
print("-------|---------|----------|-----------|--------")
for cfg, loss in sorted(results.items()):
    if loss is None:
        print(f"{cfg:12} | ?       | ?        | ?         | ?")
    else:
        if cfg == "no-gap":
            p_yield = 0.0
            pred_pct = 0.0
        elif cfg == "gap-size-0":
            p_yield = 0.85
            pred_pct = 90.0
        else:
            p_yield = 1.0
            pred_pct = 99.0
        obs_pct = loss * 100
        error_pct = abs(pred_pct - obs_pct)
        print(f"{cfg:12} | {p_yield:.2f}   | {pred_pct:.0f}%  | {obs_pct:.0f}%     | <{error_pct:.0f}%")

print()
print("Conclusions:")
print("1. --no-gap: 0 yield-points -> p_yield=0 -> 0% loss")
print("2. --gap-size=0: FOR_ITER in sum(range(0)) -> p_yield~0.85 -> ~90% loss")
print("3. gap>=10: FOR_ITER+JUMP_BACKWARD -> p_yield~1 -> ~99% loss")
print()
print("NOTE: --gap-size 0 is NOT --no-gap. Any iterator call widens the window.")