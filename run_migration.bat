@echo off
REM Sybase to PostgreSQL Migration Runner
REM This batch file helps run the migration on Windows

echo ========================================
echo Sybase to PostgreSQL Migration Tool
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found
    echo Creating .env file from template...
    copy env_example.txt .env
    echo Please edit .env file with your database credentials
    echo Then run this script again
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt

REM Run test setup first
echo.
echo Running test setup...
python test_setup.py
if errorlevel 1 (
    echo Test setup failed. Please fix the issues and try again.
    pause
    exit /b 1
)

REM Run main migration
echo.
echo Running main migration...
python main_migration.py
if errorlevel 1 (
    echo Migration failed. Please check the logs.
    pause
    exit /b 1
)

echo.
echo Migration completed successfully!
echo You can now run scheduled sync with: python scheduled_sync.py
pause 