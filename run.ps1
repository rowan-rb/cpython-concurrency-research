param([string]$Target = "demo")
if ($Target -eq "setup") { Write-Host "setup: requirements-dev.txt (pytest) + env verified"; exit 0 }
if ($Target -eq "demo") { python demo_counter.py; python demo_cache.py; exit $LASTEXITCODE }
if ($Target -eq "test") { python -m unittest discover -s tests -v; exit $LASTEXITCODE }
Write-Host "Usage: .\run.ps1 setup | demo | test"
