# SENTRY locked runtime (PowerShell edition). Run:  .\start.ps1
# Finds a Python with playwright+flask, starts mocks (:8000) + console (:8765)
# detached, verifies health, prints URLs. Reuses servers already running.
param([int]$MocksPort = 8000, [int]$ConsolePort = 8765)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

function Find-Python {
  foreach ($c in @($env:PYTHON, "python3", "python", "py")) {
    if (-not $c) { continue }
    try {
      & $c -c "import playwright, flask" 2>$null
      if ($LASTEXITCODE -eq 0) { return $c }
    } catch { }
  }
  foreach ($p in @("$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe",
                  "$env:HOME\AppData\Local\Programs\Python\Python3*\python.exe")) {
    $hit = Resolve-Path $p -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hit) {
      try {
        & $hit.Path -c "import playwright, flask" 2>$null
        if ($LASTEXITCODE -eq 0) { return $hit.Path }
      } catch { }
    }
  }
  return $null
}

function Test-Url($url) {
  try { (Invoke-WebRequest -Uri $url -TimeoutSec 3 -UseBasicParsing).StatusCode -eq 200 }
  catch { $false }
}

$py = Find-Python
if (-not $py) {
  Write-Host "No Python with playwright + flask found." -ForegroundColor Red
  Write-Host "  <python> -m pip install -r requirements.txt"
  exit 1
}
Write-Host "python: $py"

$jobs = @(
  @{ name = "mocks";   url = "http://127.0.0.1:$MocksPort/site_a/search.html"; args = "mocks/serve.py --port $MocksPort" },
  @{ name = "console"; url = "http://127.0.0.1:$ConsolePort/status";            args = "harness/console/app.py --port $ConsolePort" }
)
foreach ($j in $jobs) {
  if (Test-Url $j.url) { Write-Host "$($j.name) : already up, reusing"; continue }
  Start-Process -FilePath $py -ArgumentList $j.args -WorkingDirectory $PSScriptRoot `
    -WindowStyle Minimized -RedirectStandardOutput "logs/start-$($j.name).log" -RedirectStandardError "logs/start-$($j.name).err"
  Write-Host "$($j.name) : starting..."
}
$deadline = (Get-Date).AddSeconds(30)
while (-not ((Test-Url $jobs[0].url) -and (Test-Url $jobs[1].url))) {
  if ((Get-Date) -gt $deadline) {
    Write-Host "FAILED to bring up servers; see logs/start-*.log" -ForegroundColor Red
    exit 1
  }
  Start-Sleep -Seconds 1
}
Write-Host ""
Write-Host "DEMO READY  mocks http://127.0.0.1:$MocksPort/site_a/search.html  console http://127.0.0.1:$ConsolePort" -ForegroundColor Green
