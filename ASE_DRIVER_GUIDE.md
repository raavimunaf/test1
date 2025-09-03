# Sybase ASE Driver Configuration Guide

This guide explains how to configure and use the **Adaptive Server Enterprise (ASE)** driver instead of FreeTDS for connecting to Sybase databases.

## 🚀 Why Use ASE Driver?

The ASE driver provides:
- **Native Sybase connectivity** - Direct connection without TDS layer
- **Better performance** - Optimized for Sybase ASE
- **Full feature support** - Access to all Sybase-specific features
- **Windows compatibility** - Built-in driver on Windows systems

## 📋 Prerequisites

### Windows
- **Built-in driver**: Windows typically includes "Adaptive Server Enterprise" driver
- **Sybase ASE client**: Install Sybase ASE client for full functionality
- **ODBC Data Source Administrator**: Available in Windows Control Panel

### Linux/macOS
- **Sybase ASE client libraries**: Install from Sybase website
- **ODBC driver manager**: Install unixODBC or iODBC

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file with ASE driver configuration:

```bash
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
PG_PASSWORD=your_postgres_password
PG_PORT=5432

# Migration Settings
BATCH_SIZE=1000
SYNC_INTERVAL_MINUTES=5
LOG_LEVEL=INFO
ENABLE_LOGGING=true
```

### 2. Driver Names

Common ASE driver names:
- **Windows**: `Adaptive Server Enterprise`
- **Linux**: `Sybase ASE ODBC Driver`
- **Alternative**: `Sybase ASE`

## 🔧 Connection String Format

The ASE driver uses this connection string format:

```
DRIVER={Adaptive Server Enterprise};
SERVER=localhost;
PORT=5000;
UID=sa;
PWD=password;
DATABASE=testdb
```

## 🧪 Testing ASE Connection

### 1. Test Available Drivers

```bash
python test_ase_connection.py
```

This script will:
- List all available ODBC drivers
- Test the ASE driver connection
- Verify database connectivity
- Show connection details

### 2. Manual Driver Verification

Check available drivers in Windows:
1. Open **ODBC Data Source Administrator**
2. Go to **Drivers** tab
3. Look for "Adaptive Server Enterprise"

## 🚨 Common Issues & Solutions

### 1. Driver Not Found

**Error**: `Driver not found`

**Solutions**:
- Install Sybase ASE client
- Check driver name spelling
- Verify ODBC installation

### 2. Connection Refused

**Error**: `Connection refused`

**Solutions**:
- Verify Sybase server is running
- Check port number (default: 5000)
- Verify firewall settings

### 3. Authentication Failed

**Error**: `Login failed`

**Solutions**:
- Verify username/password
- Check user permissions
- Ensure database exists

### 4. Database Not Found

**Error**: `Database not found`

**Solutions**:
- Verify database name
- Check user permissions
- Create database if needed

## 📊 Performance Tuning

### 1. Connection Pooling

The migration tool automatically uses connection pooling for PostgreSQL. For Sybase, connections are managed per request.

### 2. Batch Size

Adjust batch size in `.env`:
```bash
BATCH_SIZE=1000  # Increase for better performance
```

### 3. Timeout Settings

Add timeout parameters if needed:
```
DRIVER={Adaptive Server Enterprise};
SERVER=localhost;
PORT=5000;
UID=sa;
PWD=password;
DATABASE=testdb;
TIMEOUT=30;
QUERY_TIMEOUT=60
```

## 🔄 Migration Process with ASE

### 1. Test Connection
```bash
python test_ase_connection.py
```

### 2. Run Test Setup
```bash
python test_setup.py
```

### 3. Execute Migration
```bash
python main_migration.py
```

### 4. Start Continuous Sync
```bash
python scheduled_sync.py
```

## 🛠️ Troubleshooting

### Check ODBC Drivers
```python
import pyodbc
drivers = pyodbc.drivers()
for driver in drivers:
    print(driver)
```

### Test Simple Connection
```python
import pyodbc
conn = pyodbc.connect("DRIVER={Adaptive Server Enterprise};SERVER=localhost;PORT=5000;UID=sa;PWD=password")
print("Connected successfully!")
conn.close()
```

### Verify Sybase Server
```bash
# Check if Sybase is running
netstat -an | findstr :5000
```

## 📁 File Changes Made

The following files were updated to use ASE driver:

1. **`env_example.txt`** - Updated driver configuration
2. **`config.py`** - Removed TDS version handling
3. **`database_connections.py`** - Updated connection logic
4. **`README.md`** - Updated installation instructions
5. **`MIGRATION_GUIDE.md`** - Updated configuration examples
6. **`test_ase_connection.py`** - New ASE connection test
7. **`run_migration.bat`** - Added ASE connection test

## 🎯 Next Steps

1. **Configure your `.env` file** with correct database credentials
2. **Test ASE connection**: `python test_ase_connection.py`
3. **Run test setup**: `python test_setup.py`
4. **Execute migration**: `python main_migration.py`

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Sybase server is running
3. Ensure correct driver name and credentials
4. Check the logs for detailed error messages

---

**Happy migrating with ASE driver! 🚀**
