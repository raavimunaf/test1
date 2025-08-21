#!/usr/bin/env python3
"""
Main Migration Script: Sybase to PostgreSQL
This script orchestrates the complete migration process including:
1. Schema creation
2. Data migration
3. Verification
4. Incremental sync testing
"""

import logging
import sys
import time
from datetime import datetime
from database_connections import DatabaseConnections
from schema_migration import SchemaMigration
from data_migration import DataMigration
from config import MIGRATION_CONFIG

# Configure logging
def setup_logging():
    """Setup logging configuration"""
    log_level = getattr(logging, MIGRATION_CONFIG['log_level'].upper())
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('migration.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main migration function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Sybase to PostgreSQL Migration")
    logger.info("=" * 60)
    
    try:
        # Initialize components
        db_connections = DatabaseConnections()
        schema_migration = SchemaMigration()
        data_migration = DataMigration()
        
        # Test database connections
        logger.info("Testing database connections...")
        if not db_connections.test_connections():
            logger.error("Database connection test failed. Exiting.")
            return False
        
        # Step 1: Create sample table in Sybase
        logger.info("\n" + "=" * 40)
        logger.info("Step 1: Creating sample table in Sybase")
        logger.info("=" * 40)
        
        if not schema_migration.create_sample_table_sybase():
            logger.error("Failed to create sample table in Sybase")
            return False
        
        # Step 2: Create table schema in PostgreSQL
        logger.info("\n" + "=" * 40)
        logger.info("Step 2: Creating table schema in PostgreSQL")
        logger.info("=" * 40)
        
        if not schema_migration.migrate_employees_schema():
            logger.error("Failed to create table schema in PostgreSQL")
            return False
        
        # Step 3: Migrate data from Sybase to PostgreSQL
        logger.info("\n" + "=" * 40)
        logger.info("Step 3: Migrating data from Sybase to PostgreSQL")
        logger.info("=" * 40)
        
        if not data_migration.migrate_employees_data():
            logger.error("Failed to migrate data")
            return False
        
        # Step 4: Verify migration
        logger.info("\n" + "=" * 40)
        logger.info("Step 4: Verifying migration")
        logger.info("=" * 40)
        
        if not data_migration.verify_migration('employees'):
            logger.error("Migration verification failed")
            return False
        
        # Step 5: Test incremental sync
        logger.info("\n" + "=" * 40)
        logger.info("Step 5: Testing incremental sync")
        logger.info("=" * 40)
        
        # Simulate an update in Sybase
        try:
            syb_conn = db_connections.get_sybase_connection()
            syb_cur = syb_conn.cursor()
            
            # Update Bob's salary
            syb_cur.execute("UPDATE employees SET salary = 80000 WHERE id = 2")
            syb_conn.commit()
            syb_cur.close()
            
            logger.info("✓ Updated Bob's salary to 80000 in Sybase")
            
        except Exception as e:
            logger.error(f"Failed to update Sybase data: {e}")
        
        # Test incremental sync
        if data_migration.incremental_sync('employees'):
            logger.info("✓ Incremental sync test successful")
        else:
            logger.error("✗ Incremental sync test failed")
        
        # Final verification
        logger.info("\n" + "=" * 40)
        logger.info("Final verification")
        logger.info("=" * 40)
        
        if data_migration.verify_migration('employees'):
            logger.info("✓ Final verification successful")
        else:
            logger.error("✗ Final verification failed")
        
        # Display final results
        logger.info("\n" + "=" * 60)
        logger.info("Migration Summary")
        logger.info("=" * 60)
        
        sybase_count = data_migration.get_table_row_count('employees', 'sybase')
        postgres_count = data_migration.get_table_row_count('employees', 'postgres')
        
        logger.info(f"Sybase employees table: {sybase_count} rows")
        logger.info(f"PostgreSQL employees table: {postgres_count} rows")
        logger.info(f"Migration status: {'SUCCESS' if sybase_count == postgres_count else 'FAILED'}")
        
        logger.info("\n" + "=" * 60)
        logger.info("Migration completed successfully!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Migration failed with error: {e}")
        return False
    
    finally:
        # Clean up connections
        try:
            db_connections.close_all()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")

def run_scheduled_sync():
    """Run scheduled synchronization"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting scheduled synchronization...")
    
    try:
        data_migration = DataMigration()
        
        # Sync employees table
        if data_migration.incremental_sync('employees'):
            logger.info("✓ Scheduled sync completed successfully")
        else:
            logger.error("✗ Scheduled sync failed")
            
    except Exception as e:
        logger.error(f"Scheduled sync failed: {e}")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 