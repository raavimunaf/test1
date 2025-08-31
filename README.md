# Sybase to PostgreSQL Migration Tool

A comprehensive Python-based solution for migrating data from Sybase to PostgreSQL with ongoing synchronization capabilities.

## 🚀 Features

- **Schema Migration**: Automatic conversion of Sybase data types to PostgreSQL equivalents
- **Data Migration**: Batch processing with conflict resolution using UPSERT
- **Incremental Sync**: Continuous synchronization based on timestamp columns
- **Crash-Safe Restore**: Section-based PostgreSQL backup and restore
- **Connection Pooling**: Efficient database connection management
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Configurable**: Environment-based configuration for different environments

## 📋 Prerequisites

### System Requirements
- Python 3.7+
- Sybase ASE or compatible database
- PostgreSQL 10+
- FreeTDS driver (for Sybase connectivity)

### Database Setup
- Sybase server running on `localhost:5000`
- PostgreSQL server running on `localhost:5432`
- Appropriate user credentials and permissions

## 🛠️ Installation

1. **Clone or download the project files**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your database credentials
   nano .env
   ```

4. **Install FreeTDS driver (for Sybase connectivity):**
   - **Windows**: Download from [FreeTDS website](https://www.freetds.org/)
   - **Linux**: `sudo apt-get install freetds-dev` (Ubuntu/Debian)
   - **macOS**: `brew install freetds`

## 🗄️ Database Setup

### 1. Setup Sybase Database

```bash
# Connect to Sybase
isql -U sa -P password -S localhost:5000

# Run the setup script
source sybase_setup.sql
```

### 2. Setup PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d postgres

# Run the setup script
\i postgres_setup.sql
```

## 🚀 Usage

### 1. Run Complete Migration

```bash
python main_migration.py
```

This will:
- Create the sample table in Sybase
- Create the corresponding table in PostgreSQL
- Migrate all data from Sybase to PostgreSQL
- Verify the migration
- Test incremental synchronization

### 2. Run Scheduled Synchronization

```bash
python scheduled_sync.py
```

This runs continuously and syncs changes every 5 minutes (configurable).

### 3. Backup and Restore Operations

```bash
# Create backup
python backup_restore.py --backup

# Full restore
python backup_restore.py --restore backup_file.dump

# Crash-safe restore
python backup_restore.py --restore backup_file.dump --crash-safe

# Resume failed restore
python backup_restore.py --restore backup_file.dump --resume-data
python backup_restore.py --restore backup_file.dump --resume-post-data

# Restore specific sections
python backup_restore.py --restore backup_file.dump --sections pre-data data
```

## 📁 Project Structure

```
├── config.py                 # Configuration management
├── database_connections.py   # Database connection handling
├── schema_migration.py       # Schema creation and migration
├── data_migration.py         # Data migration and synchronization
├── main_migration.py         # Main migration orchestration
├── scheduled_sync.py         # Continuous synchronization service
├── backup_restore.py         # Backup and restore operations
├── requirements.txt          # Python dependencies
├── env_example.txt           # Environment configuration example
├── sybase_setup.sql          # Sybase database setup
├── postgres_setup.sql        # PostgreSQL database setup
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env_example.txt`:

```bash
# Sybase Configuration
SYBASE_SERVER=localhost
SYBASE_PORT=5000
SYBASE_UID=sa
SYBASE_PWD=password
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

### Migration Settings

- `BATCH_SIZE`: Number of rows to process in each batch
- `SYNC_INTERVAL_MINUTES`: Minutes between synchronization runs
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENABLE_LOGGING`: Enable/disable logging

## 🔄 Migration Process

### 1. Schema Migration
- Analyzes Sybase table structure
- Converts data types to PostgreSQL equivalents
- Creates tables with proper constraints

### 2. Data Migration
- Extracts data from Sybase in batches
- Inserts/updates data in PostgreSQL using UPSERT
- Handles conflicts gracefully

### 3. Incremental Sync
- Monitors `updated_at` timestamp column
- Syncs only changed records
- Maintains data consistency

### 4. Verification
- Compares row counts between databases
- Validates data integrity
- Reports migration status

## 🛡️ Crash-Safe Restore

The backup and restore system provides crash-safe restoration:

1. **Pre-data**: Schema, functions, procedures
2. **Data**: Table data
3. **Post-data**: Indexes, constraints, triggers

If any step fails, you can resume from that point without losing progress.

## 📊 Monitoring and Logging

- **Migration logs**: `migration.log`
- **Sync logs**: `sync.log`
- **Console output**: Real-time progress updates
- **Error tracking**: Detailed error messages and stack traces

## 🔧 Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify database credentials
   - Check network connectivity
   - Ensure FreeTDS is properly configured

2. **Data Type Conversion Issues**
   - Review the type mapping in `schema_migration.py`
   - Check for unsupported Sybase data types

3. **Performance Issues**
   - Adjust `BATCH_SIZE` in configuration
   - Monitor database performance metrics
   - Consider indexing strategies

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

## 📈 Scaling Considerations

- **Large Tables**: Use appropriate batch sizes
- **Multiple Tables**: Extend the migration scripts
- **High Frequency Updates**: Adjust sync intervals
- **Network Latency**: Consider connection pooling settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and production use.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Verify your configuration
4. Check database connectivity

## 🔮 Future Enhancements

- [ ] Support for more database types
- [ ] Web-based monitoring dashboard
- [ ] Automated testing suite
- [ ] Performance optimization tools
- [ ] Multi-table migration support
- [ ] Real-time change data capture

---

**Happy Migrating! 🚀** 