# Sybase to PostgreSQL Migration Guide

This document provides a comprehensive guide for migrating data from Sybase to PostgreSQL using the provided Python tools.

## Quick Start

1. **Setup Environment**
   ```bash
   # Copy environment template
   cp env_example.txt .env
   
   # Edit .env with your database credentials
   nano .env
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Test Setup**
   ```bash
   python test_setup.py
   ```

3. **Run Migration**
   ```bash
   python main_migration.py
   ```

4. **Start Continuous Sync**
   ```bash
   python scheduled_sync.py
   ```

## Database Setup

### Sybase Setup

```sql
-- Connect to Sybase
isql -U sa -P StrongPass1 -S localhost:5000

-- Run setup script
source sybase_setup.sql
```

### PostgreSQL Setup

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d postgres

# Run setup script
\i postgres_setup.sql
```

## Migration Process

### 1. Schema Migration

The system automatically:
- Analyzes Sybase table structure
- Converts data types to PostgreSQL equivalents
- Creates tables with proper constraints

### 2. Data Migration

- Extracts data from Sybase in configurable batches
- Inserts/updates data in PostgreSQL using UPSERT
- Handles conflicts gracefully
- Provides detailed logging and progress tracking

### 3. Incremental Sync

- Monitors `updated_at` timestamp column
- Syncs only changed records
- Maintains data consistency between databases

### 4. Verification

- Compares row counts between databases
- Validates data integrity
- Reports migration status

## Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Sybase Configuration
SYBASE_DRIVER=Adaptive Server Enterprise
SYBASE_SERVER=localhost
SYBASE_PORT=5000
SYBASE_UID=sa
SYBASE_PWD=StrongPass1
SYBASE_DB=testdb

# PostgreSQL Configuration
PG_HOST=localhost
PG_DB=testdb
PG_USER=postgres
PG_PASSWORD=StrongPass2
PG_PORT=5432

# Migration Settings
BATCH_SIZE=1000
SYNC_INTERVAL_MINUTES=5
LOG_LEVEL=INFO
ENABLE_LOGGING=true
```

## Backup and Restore

### Create Backup
```bash
python backup_restore.py --backup
```

### Full Restore
```bash
python backup_restore.py --restore backup_file.dump
```

### Crash-Safe Restore
```bash
# Restore specific sections
python backup_restore.py --restore backup_file.dump --crash-safe --sections pre-data data post-data
```

## Monitoring and Logging

- **Migration logs**: `migration.log`
- **Sync logs**: `sync.log`
- **Console output**: Real-time progress updates
- **Error tracking**: Detailed error messages and stack traces

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify database credentials in `.env`
   - Check network connectivity
   - Ensure Sybase ASE client is properly installed and configured

2. **Data Type Conversion Issues**
   - Review type mapping in `schema_migration.py`
   - Check for unsupported Sybase data types

3. **Performance Issues**
   - Adjust `BATCH_SIZE` in configuration
   - Monitor database performance metrics
   - Consider indexing strategies

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

## Advanced Features

### Multi-Table Migration

Extend the migration scripts to handle multiple tables:

```python
# In scheduled_sync.py
tables = ['employees', 'departments', 'projects']
for table in tables:
    data_migration.incremental_sync(table)
```

### Custom Data Transformations

Add data transformation logic in `data_migration.py`:

```python
def transform_data(self, row):
    """Apply custom transformations to data"""
    # Example: Convert salary to different currency
    if row[3]:  # salary column
        row[3] = row[3] * 1.1  # 10% increase
    return row
```

### Error Recovery

The system includes error recovery mechanisms:
- Automatic retry for failed batches
- Transaction rollback on errors
- Detailed error logging for debugging

## Performance Optimization

### Batch Processing
- Adjust `BATCH_SIZE` based on available memory
- Monitor database performance during migration
- Use appropriate batch sizes for large tables

### Connection Pooling
- PostgreSQL connections are pooled for efficiency
- Sybase connections are managed per operation
- Connections are automatically cleaned up

### Indexing Strategy
- Create indexes after data migration for better performance
- Use `updated_at` index for incremental sync
- Consider dropping indexes during bulk operations

## Security Considerations

1. **Credentials Management**
   - Use environment variables for sensitive data
   - Never commit `.env` files to version control
   - Use strong passwords for database accounts

2. **Network Security**
   - Use SSL connections when possible
   - Restrict database access to necessary IPs
   - Monitor connection logs

3. **Data Privacy**
   - Implement data masking for sensitive fields
   - Use encryption for data in transit
   - Follow data protection regulations

## Scaling Considerations

- **Large Tables**: Use appropriate batch sizes and parallel processing
- **Multiple Tables**: Extend the migration scripts for multiple tables
- **High Frequency Updates**: Adjust sync intervals and use change data capture
- **Network Latency**: Consider connection pooling and timeout settings

## Support and Maintenance

### Regular Maintenance
- Monitor log files for errors
- Check database performance metrics
- Update dependencies regularly
- Test backup and restore procedures

### Monitoring
- Set up alerts for migration failures
- Monitor sync lag between databases
- Track performance metrics
- Review error logs regularly

---

**Happy Migrating! 🚀**

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Verify your configuration
4. Test database connectivity
