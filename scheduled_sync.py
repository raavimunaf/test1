#!/usr/bin/env python3
"""
Scheduled Synchronization Script
This script runs continuously to keep PostgreSQL synchronized with Sybase changes.
It can be run as a service or scheduled task.
"""

import logging
import time
import schedule
import signal
import sys
from datetime import datetime
from database_connections import DatabaseConnections
from data_migration import DataMigration
from config import MIGRATION_CONFIG

# Global flag for graceful shutdown
running = True

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, MIGRATION_CONFIG['log_level'].upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('sync.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global running
    logger = logging.getLogger(__name__)
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    running = False

def sync_job():
    """Main synchronization job"""
    logger = logging.getLogger(__name__)
    logger.info("Starting scheduled synchronization job...")
    
    try:
        # Initialize components
        db_connections = DatabaseConnections()
        data_migration = DataMigration()
        
        # Test connections
        if not db_connections.test_connections():
            logger.error("Database connection test failed, skipping sync")
            return False
        
        # Sync employees table
        if data_migration.incremental_sync('employees'):
            logger.info("✓ Employees table sync completed successfully")
        else:
            logger.error("✗ Employees table sync failed")
        
        # Close connections
        db_connections.close_all()
        
        logger.info("Synchronization job completed")
        return True
        
    except Exception as e:
        logger.error(f"Synchronization job failed: {e}")
        return False

def run_scheduler():
    """Run the scheduler"""
    logger = logging.getLogger(__name__)
    
    # Schedule sync job
    interval_minutes = MIGRATION_CONFIG['sync_interval_minutes']
    schedule.every(interval_minutes).minutes.do(sync_job)
    
    logger.info(f"Scheduler started - sync every {interval_minutes} minutes")
    logger.info("Press Ctrl+C to stop")
    
    # Run initial sync
    sync_job()
    
    # Main loop
    while running:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(5)  # Wait before retrying
    
    logger.info("Scheduler stopped")

def main():
    """Main function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 50)
    logger.info("Sybase to PostgreSQL Synchronization Service")
    logger.info("=" * 50)
    
    try:
        run_scheduler()
    except Exception as e:
        logger.error(f"Service failed: {e}")
        return False
    
    logger.info("Service stopped gracefully")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 