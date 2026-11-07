# Phase 9 — Self-review with evidence

- [x] The bug is called "atomicity violation / lost update" — `README.md:9`, `demo_counter.py:4`, `analysis/bytecode.md`
- [x] Demo fails on EVERY run (calibrated) — `env/REPRO.md` (real data), `demo_counter.py` assert fails, `demo_cache.py` assert fails
- [x] There is a decision with discarded alternative — README "Key decisions", `benchmark/results.md` compares mechanisms (not correct vs broken)
- [x] Real numbers present — `env/REPRO.md`, `benchmark/results.md`, `demo_counter.py:66` (60798 vs 600000)
- [x] Test that fails pre-fix without git stash — `tests/test_cache.py` with `exec()`, `tests/test_counter.py` with `broken` fixture
- [x] Ladder documented — `ladder.md`
- [x] README understood in 30s and runs in 3 commands — `README.md:57-59`
- [x] Observability without `print()` — `observability/logging_demo.py`
- [x] Honest limitations (2 specific bullets) — `README.md:69-72`
- [x] Pre-mortem not generic — `README.md:74-78`
- [x] "GIL, so no race" does not appear — reviewed in all files; correct distinction present (GIL serializes bytecode, not sequences)
- [x] `sleep()` does not appear as synchronization — `demo_counter.py:35` uses `barrier.wait()`, `env/REPRO.md` documents it
- [x] `itertools.count` not presented as semantic equivalent — `solutions/counter_atomic.py` explicitly documents NOT drop-in and PEP 703
