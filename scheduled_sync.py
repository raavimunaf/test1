#!/usr/bin/env python3
"""
Scheduled Synchronization Script
This script runs continuous synchronization between Sybase and PostgreSQL
"""

import logging
import sys
import time
import schedule
from datetime import datetime
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
            logging.FileHandler('sync.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def sync_job():
    """Job function to run synchronization"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 40)
    logger.info(f"Starting scheduled sync at {datetime.now()}")
    logger.info("=" * 40)
    
    try:
        data_migration = DataMigration()
        
        # Sync employees table
        if data_migration.incremental_sync('employees'):
            logger.info("✓ Employees table sync completed successfully")
        else:
            logger.error("✗ Employees table sync failed")
        
        # Add more tables here as needed
        # if data_migration.incremental_sync('other_table'):
        #     logger.info("✓ Other table sync completed successfully")
        # else:
        #     logger.error("✗ Other table sync failed")
        
        logger.info("=" * 40)
        logger.info(f"Scheduled sync completed at {datetime.now()}")
        logger.info("=" * 40)
        
    except Exception as e:
        logger.error(f"Scheduled sync failed: {e}")

def main():
    """Main function to run scheduled synchronization"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting scheduled synchronization service...")
    logger.info(f"Sync interval: {MIGRATION_CONFIG['sync_interval_minutes']} minutes")
    
    # Schedule the sync job
    schedule.every(MIGRATION_CONFIG['sync_interval_minutes']).minutes.do(sync_job)
    
    # Run initial sync
    logger.info("Running initial sync...")
    sync_job()
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("Scheduled sync service stopped by user")
    except Exception as e:
        logger.error(f"Scheduled sync service failed: {e}")

if __name__ == "__main__":
    main() 