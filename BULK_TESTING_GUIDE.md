# Bulk Migration Testing Guide

## Overview
This guide explains how to test the Sybase to PostgreSQL migration system with large datasets (up to 1 crore/10 million records) using the bulk testing framework.

## Components

### 1. Bulk Data Generator (`bulk_data_generator.py`)
Generates realistic employee data for testing migration performance.

**Features:**
- Generates up to 10 million records (1 crore)
- Memory-efficient batch processing
- Realistic Indian employee data
- Multiple output formats (CSV, JSON)
- Configurable batch sizes

**Usage:**
```bash
# Generate sample data (100K records)
python bulk_data_generator.py --sample 100000 --output sample_employees.csv

# Generate full dataset (10M records)
python bulk_data_generator.py --total 10000000 --output bulk_employees.csv

# Custom batch size
python bulk_data_generator.py --total 1000000 --batch-size 50000 --output medium_employees.csv
```

### 2. Bulk Migration Tester (`test_bulk_migration.py`)
Comprehensive testing framework for bulk migration operations.

**Features:**
- End-to-end migration testing
- Performance metrics collection
- Memory and CPU monitoring
- Batch processing validation
- Detailed performance reports

**Usage:**
```bash
# Quick test (100K records)
python test_bulk_migration.py --quick --records 100000

# Medium test (1M records)
python test_bulk_migration.py --records 1000000

# Large test (10M records - 1 crore)
python test_bulk_migration.py --records 10000000
```

### 3. Performance Monitor (`performance_monitor.py`)
Real-time system resource monitoring during migration operations.

**Features:**
- CPU, memory, and disk monitoring
- Process-specific metrics
- Background monitoring threads
- Export to JSON/CSV formats
- Performance trend analysis

**Usage:**
```bash
# Start continuous monitoring
python performance_monitor.py --monitor

# Show current system status
python performance_monitor.py --status

# Custom monitoring interval
python performance_monitor.py --monitor --interval 1.0
```

### 4. Batch Test Runner (`run_bulk_test.bat`)
Windows batch file for easy test execution.

**Features:**
- Interactive menu system
- Predefined test scenarios
- Safety confirmations for large tests
- Integrated performance monitoring

## Testing Scenarios

### Scenario 1: Quick Validation (100K records)
**Purpose:** Basic functionality testing and performance baseline
**Duration:** 5-15 minutes
**Resource Usage:** Low to moderate

```bash
python test_bulk_migration.py --quick --records 100000
```

### Scenario 2: Medium Load Testing (1M records)
**Purpose:** Performance testing and optimization validation
**Duration:** 30 minutes - 2 hours
**Resource Usage:** Moderate to high

```bash
python test_bulk_migration.py --records 1000000
```

### Scenario 3: Full Production Load (10M records - 1 crore)
**Purpose:** Production readiness validation and stress testing
**Duration:** 2-8 hours (depending on system performance)
**Resource Usage:** High to very high

```bash
python test_bulk_migration.py --records 10000000
```

## Performance Monitoring

### Real-time Monitoring
Start performance monitoring before running tests:

```bash
# Terminal 1: Start monitoring
python performance_monitor.py --monitor

# Terminal 2: Run migration test
python test_bulk_migration.py --records 1000000
```

### Metrics Collected
- **CPU Usage:** Percentage and frequency
- **Memory Usage:** RSS, VMS, and percentage
- **Disk I/O:** Read/write operations
- **Network I/O:** Bytes sent/received
- **Process Metrics:** Thread count, memory allocation

### Performance Thresholds
Configure in `config.py`:
```python
BULK_MIGRATION_CONFIG = {
    'memory_threshold_mb': 2048,        # 2GB memory warning
    'cpu_threshold_percent': 80,        # 80% CPU warning
    'performance_monitoring': True,     # Enable monitoring
}
```

## Configuration

### Environment Variables
Create `.env` file with your database settings:

```env
# Sybase Configuration
SYBASE_DRIVER=Adaptive Server Enterprise
SYBASE_SERVER=localhost
SYBASE_PORT=5000
SYBASE_UID=sa
SYBASE_PWD=your_password
SYBASE_DB=testdb

# PostgreSQL Configuration
PG_HOST=localhost
PG_DB=testdb
PG_USER=postgres
PG_PASSWORD=your_password
PG_PORT=5432

# Bulk Migration Settings
BULK_BATCH_SIZE=10000
MAX_RECORDS_PER_TEST=10000000
PERFORMANCE_MONITORING=true
MEMORY_THRESHOLD_MB=2048
CPU_THRESHOLD_PERCENT=80
```

### Batch Size Optimization
Adjust batch sizes based on your system:

```python
# For high-memory systems (16GB+)
BULK_BATCH_SIZE=50000

# For moderate systems (8GB)
BULK_BATCH_SIZE=10000

# For low-memory systems (4GB)
BULK_BATCH_SIZE=5000
```

## Expected Performance Metrics

### Data Generation
- **Small datasets (100K):** 10,000-50,000 records/second
- **Medium datasets (1M):** 5,000-25,000 records/second
- **Large datasets (10M):** 2,000-15,000 records/second

### Migration Performance
- **Sybase to PostgreSQL:** 1,000-10,000 records/second
- **Memory usage:** 500MB - 4GB depending on batch size
- **CPU usage:** 20-80% depending on system configuration

### Verification Performance
- **Data count verification:** 100-1,000 records/second
- **Checksum verification:** 50-500 records/second

## Troubleshooting

### Common Issues

#### 1. Memory Errors
**Symptoms:** `MemoryError` or system becomes unresponsive
**Solutions:**
- Reduce batch size in configuration
- Close other applications
- Increase system swap space
- Use `--quick` flag for testing

#### 2. Database Connection Timeouts
**Symptoms:** Connection lost during long operations
**Solutions:**
- Increase database timeout settings
- Check network stability
- Use connection pooling
- Implement retry logic

#### 3. Slow Performance
**Symptoms:** Migration taking much longer than expected
**Solutions:**
- Check disk I/O performance
- Optimize database indexes
- Increase batch sizes
- Enable parallel processing

### Performance Tuning

#### Database Optimization
```sql
-- PostgreSQL optimization
ALTER TABLE employees SET (fillfactor = 90);
CREATE INDEX CONCURRENTLY idx_employees_dept ON employees(department);
VACUUM ANALYZE employees;

-- Sybase optimization
sp_helpindex employees
CREATE INDEX idx_employees_dept ON employees(department)
```

#### System Optimization
- **Windows:** Disable unnecessary services, optimize page file
- **Linux:** Tune I/O scheduler, optimize memory management
- **General:** Use SSD storage, ensure adequate RAM

## Best Practices

### 1. Start Small
- Begin with 100K records to validate setup
- Gradually increase to 1M, then 10M
- Monitor system resources at each step

### 2. Monitor Resources
- Use performance monitoring during all tests
- Set up alerts for resource thresholds
- Document performance baselines

### 3. Backup Data
- Backup databases before large tests
- Use test environments when possible
- Keep original data safe

### 4. Document Results
- Save performance reports
- Note system configurations
- Track optimization attempts

## Sample Test Execution

### Complete Test Run (1M records)
```bash
# 1. Start performance monitoring
python performance_monitor.py --monitor &

# 2. Run migration test
python test_bulk_migration.py --records 1000000

# 3. Check results
cat bulk_migration_test.log
ls -la performance_*.json
```

### Expected Output
```
==========================================
Starting Bulk Migration Test with 1,000,000 records
==========================================

1. Testing database connections...
✓ Database connections successful

2. Testing schema creation...
✓ Schema creation completed in 2.45 seconds

3. Testing data generation...
✓ Data generation completed in 45.23 seconds
Speed: 22,107 records/second

4. Testing Sybase bulk insert...
✓ Sybase bulk insert completed in 180.45 seconds
Speed: 5,543 records/second

5. Testing bulk migration...
✓ Bulk migration completed in 420.67 seconds
Rate: 2,377 records/second

6. Testing data verification...
✓ Data verification completed in 15.23 seconds

==========================================
BULK MIGRATION TEST COMPLETED SUCCESSFULLY!
Total test duration: 663.03 seconds
==========================================
```

## Advanced Features

### Parallel Processing
Enable parallel processing for better performance:

```python
BULK_MIGRATION_CONFIG = {
    'enable_parallel_processing': True,
    'parallel_workers': 4
}
```

### Custom Data Generation
Modify `BulkDataGenerator` class for different data types:
- Customer data
- Product catalog
- Financial transactions
- Log entries

### Integration with CI/CD
- Automated performance testing
- Performance regression detection
- Resource usage tracking
- Automated reporting

## Support and Maintenance

### Log Files
- `bulk_migration_test.log`: Main test execution logs
- `performance_*.json`: Performance metrics
- `migration.log`: General migration logs

### Monitoring
- Regular performance reviews
- System resource tracking
- Database performance analysis
- Optimization recommendations

### Updates
- Regular dependency updates
- Performance improvements
- Bug fixes and enhancements
- New feature additions

---

**Note:** This testing framework is designed for production-like scenarios. Always test in appropriate environments and ensure adequate system resources for large-scale tests.

