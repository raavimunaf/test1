#!/usr/bin/env python3
"""
Test Setup Script
This script helps verify the environment and test migration components
"""

import logging
import sys
import os
from database_connections import DatabaseConnections
from schema_migration import SchemaMigration
from data_migration import DataMigration
from config import SYBASE_CONFIG, POSTGRES_CONFIG, MIGRATION_CONFIG

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_environment():
    """Test the environment setup"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("Testing Environment Setup")
    logger.info("=" * 50)
    
    # Test Python version
    logger.info(f"Python version: {sys.version}")
    
    # Test required packages
    required_packages = ['pyodbc', 'psycopg2', 'python-dotenv', 'schedule']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✓ {package} is installed")
        except ImportError:
            logger.error(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.error("Please install missing packages: pip install -r requirements.txt")
        return False
    
    # Test environment variables
    logger.info("\nTesting environment variables:")
    env_vars = {
        'SYBASE_SERVER': SYBASE_CONFIG['server'],
        'SYBASE_PORT': SYBASE_CONFIG['port'],
        'SYBASE_UID': SYBASE_CONFIG['uid'],
        'SYBASE_DB': SYBASE_CONFIG['database'],
        'PG_HOST': POSTGRES_CONFIG['host'],
        'PG_PORT': POSTGRES_CONFIG['port'],
        'PG_USER': POSTGRES_CONFIG['user'],
        'PG_DB': POSTGRES_CONFIG['dbname']
    }
    
    for var, value in env_vars.items():
        if value:
            logger.info(f"✓ {var}: {value}")
        else:
            logger.warning(f"⚠ {var}: Not set")
    
    return True

def test_database_connections():
    """Test database connections"""
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 50)
    logger.info("Testing Database Connections")
    logger.info("=" * 50)
    
    try:
        db_connections = DatabaseConnections()
        
        # Test connections
        if db_connections.test_connections():
            logger.info("✓ All database connections successful")
            return True
        else:
            logger.error("✗ Database connection test failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Database connection test failed: {e}")
        return False

def test_schema_migration():
    """Test schema migration"""
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 50)
    logger.info("Testing Schema Migration")
    logger.info("=" * 50)
    
    try:
        schema_migration = SchemaMigration()
        
        # Test Sybase table creation
        logger.info("Testing Sybase table creation...")
        if schema_migration.create_sample_table_sybase():
            logger.info("✓ Sybase table creation successful")
        else:
            logger.error("✗ Sybase table creation failed")
            return False
        
        # Test PostgreSQL table creation
        logger.info("Testing PostgreSQL table creation...")
        if schema_migration.migrate_employees_schema():
            logger.info("✓ PostgreSQL table creation successful")
        else:
            logger.error("✗ PostgreSQL table creation failed")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Schema migration test failed: {e}")
        return False

def test_data_migration():
    """Test data migration"""
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 50)
    logger.info("Testing Data Migration")
    logger.info("=" * 50)
    
    try:
        data_migration = DataMigration()
        
        # Test data migration
        logger.info("Testing data migration...")
        if data_migration.migrate_employees_data():
            logger.info("✓ Data migration successful")
        else:
            logger.error("✗ Data migration failed")
            return False
        
        # Test verification
        logger.info("Testing migration verification...")
        if data_migration.verify_migration('employees'):
            logger.info("✓ Migration verification successful")
        else:
            logger.error("✗ Migration verification failed")
            return False
        
        # Test incremental sync
        logger.info("Testing incremental sync...")
        if data_migration.incremental_sync('employees'):
            logger.info("✓ Incremental sync successful")
        else:
            logger.error("✗ Incremental sync failed")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Data migration test failed: {e}")
        return False

def show_row_counts():
    """Show row counts in both databases"""
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 50)
    logger.info("Row Counts")
    logger.info("=" * 50)
    
    try:
        data_migration = DataMigration()
        
        sybase_count = data_migration.get_table_row_count('employees', 'sybase')
        postgres_count = data_migration.get_table_row_count('employees', 'postgres')
        
        logger.info(f"Sybase employees table: {sybase_count} rows")
        logger.info(f"PostgreSQL employees table: {postgres_count} rows")
        
        if sybase_count == postgres_count:
            logger.info("✓ Row counts match")
        else:
            logger.warning("⚠ Row counts don't match")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to get row counts: {e}")
        return False

def main():
    """Main test function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting comprehensive test setup...")
    
    tests = [
        ("Environment", test_environment),
        ("Database Connections", test_database_connections),
        ("Schema Migration", test_schema_migration),
        ("Data Migration", test_data_migration),
        ("Row Counts", show_row_counts)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Summary")
    logger.info("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            logger.info(f"✓ {test_name}: PASSED")
            passed += 1
        else:
            logger.error(f"✗ {test_name}: FAILED")
            failed += 1
    
    logger.info(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Your migration environment is ready.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 