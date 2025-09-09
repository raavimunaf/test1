@echo off
echo ========================================
echo Bulk Migration Test Runner
echo ========================================
echo.

echo Available test options:
echo 1. Quick test (100K records)
echo 2. Medium test (1M records) 
echo 3. Large test (10M records - 1 crore)
echo 4. Custom record count
echo 5. Performance monitoring only
echo 6. Data generation only
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Running quick test with 100K records...
    python test_bulk_migration.py --quick --records 100000
    goto end
)

if "%choice%"=="2" (
    echo Running medium test with 1M records...
    python test_bulk_migration.py --records 1000000
    goto end
)

if "%choice%"=="3" (
    echo Running large test with 10M records (1 crore)...
    echo This will take significant time and resources!
    set /p confirm="Are you sure? (y/N): "
    if /i "%confirm%"=="y" (
        python test_bulk_migration.py --records 10000000
    ) else (
        echo Test cancelled.
    )
    goto end
)

if "%choice%"=="4" (
    set /p record_count="Enter number of records: "
    echo Running test with %record_count% records...
    python test_bulk_migration.py --records %record_count%
    goto end
)

if "%choice%"=="5" (
    echo Starting performance monitoring...
    python performance_monitor.py --monitor
    goto end
)

if "%choice%"=="6" (
    echo Running data generation only...
    python bulk_data_generator.py --sample 100000 --output sample_employees.csv
    goto end
)

echo Invalid choice. Please run the script again.

:end
echo.
echo Test completed. Check the log files for details.
pause

