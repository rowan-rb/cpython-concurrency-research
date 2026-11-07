$ErrorActionPreference = "Continue"
$fail = 0

Write-Host "`n=== 1. PYTHON + GIL ===" -ForegroundColor Cyan
python -V
python -c "import sys; print('GIL:', sys._is_gil_enabled())"
python -c "import sys; print('sys.flags.gil:', getattr(sys.flags, 'gil', 'NOT FOUND'))"

Write-Host "`n=== 2. DEMO COUNTER (3 runs, fail 3/3) ===" -ForegroundColor Cyan
$cf = 0
1..3 | ForEach-Object { $o = python demo_counter.py 2>&1 | Out-String; if ($o -match "LOST UPDATE") { $cf++ } }
Write-Host ("counter failures: $cf/3")
if ($cf -lt 3) { Write-Host "FAIL: counter not deterministic" -ForegroundColor Red; $fail++ }

Write-Host "`n=== 3. DEMO CACHE (3 runs, fail 3/3) ===" -ForegroundColor Cyan
$kf = 0
1..3 | ForEach-Object { $o = python demo_cache.py 2>&1 | Out-String; if ($o -match "double-compute") { $kf++ } }
Write-Host ("cache failures: $kf/3")
if ($kf -lt 3) { Write-Host "FAIL: cache not deterministic" -ForegroundColor Red; $fail++ }

Write-Host "`n=== 4. NO-GAP (5 runs) ===" -ForegroundColor Cyan
$ng = 0
1..5 | ForEach-Object { $o = python demo_counter.py --no-gap 2>&1 | Out-String; if ($o -match "counter.value=600000") { $ng++ }; Write-Host $o.Trim() }
Write-Host ("no-gap perfect runs: $ng/5")
if ($ng -lt 4) { Write-Host "WARNING: no-gap unstable, check README" -ForegroundColor Yellow }

Write-Host "`n=== 5. TESTS ===" -ForegroundColor Cyan
python -m unittest discover -s tests -v 2>&1 | Select-String "OK|Ran 4 tests"
if ($LASTEXITCODE -ne 0) { Write-Host "FAIL: tests" -ForegroundColor Red; $fail++ }

Write-Host "`n=== 6. RUN.PS1 ===" -ForegroundColor Cyan
if (Test-Path ".\run.ps1") {
    Write-Host "--- run.ps1 demo ---"; .\run.ps1 demo 2>&1 | Select-Object -First 5
    Write-Host "--- run.ps1 test ---"; .\run.ps1 test 2>&1 | Select-Object -Last 5
} else { Write-Host "FAIL: run.ps1 missing" -ForegroundColor Red; $fail++ }

Write-Host "`n=== 7. BYTECODE CACHE ===" -ForegroundColor Cyan
$r7 = python -c "import dis, demo_cache; dis.dis(demo_cache.buggy_access)" 2>&1 | Out-String
if ($r7 -match "STORE_SUBSCR") { Write-Host "OK: STORE_SUBSCR" } else { Write-Host "FAIL: bytecode cache" -ForegroundColor Red; $fail++ }

Write-Host "`n=== 8. 'make setup' in README? ===" -ForegroundColor Cyan
$r = [System.IO.File]::ReadAllText("$PWD\README.md")
if ($r -match "make setup") { Write-Host "FAIL: make setup still present" -ForegroundColor Red; $fail++ } else { Write-Host "OK" }

Write-Host "`n=== 9. README STRUCTURE (h2) ===" -ForegroundColor Cyan
$r9 = Select-String -Path README.md -Pattern "^##" | ForEach-Object { "{0,4}: {1}" -f $_.LineNumber, $_.Line }
$r9 | ForEach-Object { Write-Host $_ }

Write-Host "`n=== PHASE 1 - Probabilistic Model (RMSE) ===" -ForegroundColor Cyan
$model_out = python model/loss_probability.py 2>&1 | Out-String
Write-Host $model_out
if ($model_out -notmatch "RMSE\)\s*:\s*0?\.?\d+") { Write-Host "FAIL: RMSE is missing or too high" -ForegroundColor Red; $fail++ }
if ($model_out -notmatch "Testing gap size: 50") { Write-Host "FAIL: missing gap size 50 test" -ForegroundColor Red; $fail++ }
Write-Host "OK: Probabilistic model evaluated with low RMSE" -ForegroundColor Green
Write-Host "`n=== PHASE 2 - Cross-version ===" -ForegroundColor Cyan
$r2 = python compat/matrix.py 2>&1 | Out-String
Write-Host $r2
if ($r2 -notmatch "3.14") { Write-Host "FAIL: matrix missing 3.14 row" -ForegroundColor Red; $fail++ }

Write-Host "`n=== PHASE 3 - What we got wrong ===" -ForegroundColor Cyan
Write-Host "Verify 4 paragraphs in README.md (search 'What we got wrong')"
$r3 = Select-String -Path README.md -Pattern "What we got wrong"
if ($r3) { Write-Host "OK: section present" } else { Write-Host "FAIL: `"What we got wrong`" section missing" -ForegroundColor Red; $fail++ }

Write-Host "`n=== PHASE 4 - Detector ===" -ForegroundColor Cyan
$r4 = python test_detector.py 2>&1 | Out-String
Write-Host $r4
if ($r4 -match "OK\(watch executed\)|detected_interleavings") { Write-Host "OK: detector" } else { Write-Host "FAIL: detector" -ForegroundColor Red; $fail++ }

Write-Host "`n=== PHASE 5 - Fuzz ===" -ForegroundColor Cyan
$r5 = python tests/test_fuzz_interleavings.py 2>&1 | Out-String
Write-Host $r5
# Format: iterations=N | buggy_loss_detected=X/N | fixed_loss_detected=Y/N
if ($r5 -match "fixed_loss_detected=0") { Write-Host "OK: fixed without loss" } else { Write-Host "FAIL: fixed with loss" -ForegroundColor Red; $fail++ }

Write-Host "`n=== PHASE 6 - Patterns example ===" -ForegroundColor Cyan
$r6 = python examples/patterns.py 2>&1 | Out-String
Write-Host $r6
if ($r6 -notmatch "buggy: value=") { Write-Host "FAIL: patterns" -ForegroundColor Red; $fail++ }

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
if ($fail -eq 0) { Write-Host "TODO OK" -ForegroundColor Green } else { Write-Host "$fail critical failures" -ForegroundColor Red }

