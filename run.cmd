@echo off
REM SENTRY launcher for cmd.exe / PowerShell on Windows.
REM
REM   run.cmd start                              start the mock sites
REM   run.cmd run --goal "..." --variant 1       run the agent
REM   run.cmd run --goal "..." --headed          headed (watchable) run
REM   run.cmd test                               full test suite
REM   run.cmd test -k "not live"                 fast unit tests only
REM   run.cmd dash                               start mocks + judge console
REM
REM Why this exists: `python` is often NOT on PATH on Windows (Store stub or a
REM PATH-less install), and PowerShell does not support bash's backslash line
REM continuation. This wrapper finds a Python that actually has playwright+flask
REM and forwards every argument unchanged.

setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "PYEXE="
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PYEXE (
  for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if not defined PYEXE if exist "%%~fD\python.exe" set "PYEXE=%%~fD\python.exe"
  )
)
if not defined PYEXE (
  for %%P in (python.exe) do if not defined PYEXE set "PYEXE=%%~$PATH:P"
)

if not defined PYEXE (
  echo [run.cmd] No Python found on this machine.
  echo           Install Python 3.11+, then: python -m pip install -r requirements.txt
  exit /b 1
)

"%PYEXE%" -c "import playwright, flask" >nul 2>&1
if errorlevel 1 (
  echo [run.cmd] %PYEXE% is missing playwright/flask.
  echo           "%PYEXE%" -m pip install -r requirements.txt
  echo           "%PYEXE%" -m playwright install chromium
  exit /b 1
)

REM NOTE: `shift` does NOT update %* — so we rebuild the argument tail by hand.
call :_tail %*
set "TAIL=%TAIL%"

set "SUB=%~1"
if /i "%SUB%"=="start" (
  "%PYEXE%" mocks\serve.py --port 8000 %TAIL%
  exit /b %ERRORLEVEL%
)
if /i "%SUB%"=="dash" (
  "%PYEXE%" harness\console\app.py --port 8765 %TAIL%
  exit /b %ERRORLEVEL%
)
if /i "%SUB%"=="run" (
  "%PYEXE%" -m agent run %TAIL%
  exit /b %ERRORLEVEL%
)
if /i "%SUB%"=="test" (
  "%PYEXE%" -m pytest harness\regression -q %TAIL%
  exit /b %ERRORLEVEL%
)
if /i "%SUB%"=="py" (
  "%PYEXE%" %TAIL%
  exit /b %ERRORLEVEL%
)

echo [run.cmd] usage: run.cmd start ^| dash ^| run ^<agent args^> ^| test [pytest args] ^| py ^<script^>
exit /b 1

:_tail
REM drop the first argument (the subcommand), keep the rest with quoting intact
set "TAIL="
shift
:tail_loop
if "%~1"=="" goto :eof
set "TAIL=%TAIL% "%~1""
shift
goto tail_loop

