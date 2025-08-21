@echo off
setlocal
cd /d %~dp0

echo === Sybase -> PostgreSQL Migration ===

if not exist .env (
  echo No .env found. Creating from env_example.txt ...
  copy /Y env_example.txt .env >nul
  echo Created .env. Review and edit credentials if needed.
)

echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed.
  exit /b 1
)

echo.
echo Verifying setup...
python test_setup.py
if errorlevel 1 (
  echo Setup verification failed. Fix issues above and re-run.
  exit /b 1
)

echo.
echo Running migration...
python main_migration.py
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% NEQ 0 (
  echo Migration failed with exit code %EXITCODE%.
  exit /b %EXITCODE%
) else (
  echo Migration finished successfully.
)

endlocal 