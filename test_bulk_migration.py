#!/usr/bin/env python3
"""
Bulk Migration Test Script
Tests migration performance with large datasets (1 crore records)
"""

import sys
import os
import time
import psutil
import logging
from datetime import datetime
from typing import List, Dict, Tuple

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bulk_data_generator import BulkDataGenerator
from database_connections import DatabaseConnections
from schema_migration import SchemaMigration
from data_migration import DataMigration
from config import MIGRATION_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bulk_migration_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BulkMigrationTester:
    """Test bulk migration performance with large datasets"""
    
    def __init__(self):
        self.db_connections = DatabaseConnections()
        self.schema_migration = SchemaMigration()
        self.data_migration = DataMigration()
        self.performance_metrics = {}
        
    def get_system_info(self) -> Dict:
        """Get system information for performance analysis"""
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else 0,
            'python_version': sys.version,
            'platform': sys.platform
        }
    
    def measure_memory_usage(self) -> Dict:
        """Measure current memory usage"""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            'rss_mb': round(memory_info.rss / (1024**2), 2),
            'vms_mb': round(memory_info.vms / (1024**2), 2),
            'percent': process.memory_percent()
        }
    
    def test_schema_creation(self) -> bool:
        """Test schema creation performance"""
        logger.info("Testing schema creation performance...")
        
        start_time = time.time()
        start_memory = self.measure_memory_usage()
        
        try:
            # Create sample table in Sybase
            if not self.schema_migration.create_sample_table_sybase():
                logger.error("Failed to create sample table in Sybase")
                return False
            
            # Create table schema in PostgreSQL
            if not self.schema_migration.migrate_employees_schema():
                logger.error("Failed to create table schema in PostgreSQL")
                return False
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            duration = end_time - start_time
            
            self.performance_metrics['schema_creation'] = {
                'duration_seconds': round(duration, 2),
                'start_memory': start_memory,
                'end_memory': end_memory,
                'memory_delta_mb': round(end_memory['rss_mb'] - start_memory['rss_mb'], 2)
            }
            
            logger.info(f"Schema creation completed in {duration:.2f} seconds")
            logger.info(f"Memory usage: {start_memory['rss_mb']}MB → {end_memory['rss_mb']}MB")
            
            return True
            
        except Exception as e:
            logger.error(f"Schema creation test failed: {e}")
            return False
    
    def test_data_generation(self, record_count: int = 1000000) -> Tuple[bool, List[Dict]]:
        """Test data generation performance"""
        logger.info(f"Testing data generation performance for {record_count:,} records...")
        
        start_time = time.time()
        start_memory = self.measure_memory_usage()
        
        try:
            generator = BulkDataGenerator(record_count)
            generator.batch_size = 10000  # Smaller batches for testing
            
            # Generate sample data
            sample_data = generator.generate_sample_data(record_count)
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            duration = end_time - start_time
            
            self.performance_metrics['data_generation'] = {
                'record_count': record_count,
                'duration_seconds': round(duration, 2),
                'records_per_second': round(record_count / duration, 2),
                'start_memory': start_memory,
                'end_memory': end_memory,
                'memory_delta_mb': round(end_memory['rss_mb'] - start_memory['rss_mb'], 2)
            }
            
            logger.info(f"Data generation completed in {duration:.2f} seconds")
            logger.info(f"Speed: {record_count / duration:,.0f} records/second")
            logger.info(f"Memory usage: {start_memory['rss_mb']}MB → {end_memory['rss_mb']}MB")
            
            return True, sample_data
            
        except Exception as e:
            logger.error(f"Data generation test failed: {e}")
            return False, []
    
    def test_bulk_insert_sybase(self, data: List[Dict]) -> bool:
        """Test bulk insert performance in Sybase"""
        logger.info(f"Testing bulk insert performance in Sybase for {len(data):,} records...")
        
        start_time = time.time()
        start_memory = self.measure_memory_usage()
        
        try:
            syb_conn = self.db_connections.get_sybase_connection()
            syb_cur = syb_conn.cursor()
            
            # Clear existing data
            syb_cur.execute("DELETE FROM employees")
            syb_conn.commit()
            
            # Insert data in batches
            batch_size = 1000
            total_inserted = 0
            
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                # Prepare batch insert
                placeholders = ','.join(['?' for _ in batch[0].keys()])
                columns = ','.join(batch[0].keys())
                sql = f"INSERT INTO employees ({columns}) VALUES ({placeholders})"
                
                # Execute batch insert
                batch_values = [tuple(record.values()) for record in batch]
                syb_cur.executemany(sql, batch_values)
                
                total_inserted += len(batch)
                if i % 10000 == 0:
                    logger.info(f"Inserted {total_inserted:,} records...")
            
            syb_conn.commit()
            syb_cur.close()
            syb_conn.close()
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            duration = end_time - start_time
            
            self.performance_metrics['sybase_bulk_insert'] = {
                'record_count': len(data),
                'duration_seconds': round(duration, 2),
                'records_per_second': round(len(data) / duration, 2),
                'batch_size': batch_size,
                'start_memory': start_memory,
                'end_memory': end_memory,
                'memory_delta_mb': round(end_memory['rss_mb'] - start_memory['rss_mb'], 2)
            }
            
            logger.info(f"Sybase bulk insert completed in {duration:.2f} seconds")
            logger.info(f"Speed: {len(data) / duration:,.0f} records/second")
            
            return True
            
        except Exception as e:
            logger.error(f"Sybase bulk insert test failed: {e}")
            return False
    
    def test_bulk_migration(self, data: List[Dict]) -> bool:
        """Test bulk migration performance from Sybase to PostgreSQL"""
        logger.info(f"Testing bulk migration performance for {len(data):,} records...")
        
        start_time = time.time()
        start_memory = self.measure_memory_usage()
        
        try:
            # Perform data migration
            if not self.data_migration.migrate_employees_data():
                logger.error("Bulk migration failed")
                return False
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            duration = end_time - start_time
            
            self.performance_metrics['bulk_migration'] = {
                'record_count': len(data),
                'duration_seconds': round(duration, 2),
                'records_per_second': round(len(data) / duration, 2),
                'start_memory': start_memory,
                'end_memory': end_memory,
                'memory_delta_mb': round(end_memory['rss_mb'] - start_memory['rss_memory'], 2)
            }
            
            logger.info(f"Bulk migration completed in {duration:.2f} seconds")
            logger.info(f"Speed: {len(data):,} records in {duration:.2f} seconds")
            logger.info(f"Rate: {len(data) / duration:,.0f} records/second")
            
            return True
            
        except Exception as e:
            logger.error(f"Bulk migration test failed: {e}")
            return False
    
    def test_verification(self, table_name: str = 'employees') -> bool:
        """Test data verification performance"""
        logger.info("Testing data verification performance...")
        
        start_time = time.time()
        start_memory = self.measure_memory_usage()
        
        try:
            # Verify migration
            if not self.data_migration.verify_migration(table_name):
                logger.error("Data verification failed")
                return False
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            duration = end_time - start_time
            
            self.performance_metrics['verification'] = {
                'duration_seconds': round(duration, 2),
                'start_memory': start_memory,
                'end_memory': end_memory,
                'memory_delta_mb': round(end_memory['rss_mb'] - start_memory['rss_mb'], 2)
            }
            
            logger.info(f"Data verification completed in {duration:.2f} seconds")
            
            return True
            
        except Exception as e:
            logger.error(f"Data verification test failed: {e}")
            return False
    
    def run_full_test(self, record_count: int = 1000000) -> bool:
        """Run complete bulk migration test"""
        logger.info("=" * 80)
        logger.info(f"Starting Bulk Migration Test with {record_count:,} records")
        logger.info("=" * 80)
        
        # Record system info
        system_info = self.get_system_info()
        logger.info(f"System Info: {system_info}")
        
        test_start_time = time.time()
        
        try:
            # Test database connections
            logger.info("\n1. Testing database connections...")
            if not self.db_connections.test_connections():
                logger.error("Database connection test failed")
                return False
            
            # Test schema creation
            logger.info("\n2. Testing schema creation...")
            if not self.test_schema_creation():
                return False
            
            # Test data generation
            logger.info("\n3. Testing data generation...")
            success, test_data = self.test_data_generation(record_count)
            if not success:
                return False
            
            # Test Sybase bulk insert
            logger.info("\n4. Testing Sybase bulk insert...")
            if not self.test_bulk_insert_sybase(test_data):
                return False
            
            # Test bulk migration
            logger.info("\n5. Testing bulk migration...")
            if not self.test_bulk_migration(test_data):
                return False
            
            # Test verification
            logger.info("\n6. Testing data verification...")
            if not self.test_verification():
                return False
            
            test_end_time = time.time()
            total_duration = test_end_time - test_start_time
            
            # Generate performance report
            self.generate_performance_report(total_duration)
            
            logger.info("\n" + "=" * 80)
            logger.info("BULK MIGRATION TEST COMPLETED SUCCESSFULLY!")
            logger.info(f"Total test duration: {total_duration:.2f} seconds")
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"Bulk migration test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_performance_report(self, total_duration: float):
        """Generate comprehensive performance report"""
        logger.info("\n" + "=" * 60)
        logger.info("PERFORMANCE REPORT")
        logger.info("=" * 60)
        
        for test_name, metrics in self.performance_metrics.items():
            logger.info(f"\n{test_name.upper().replace('_', ' ')}:")
            for key, value in metrics.items():
                if isinstance(value, dict):
                    logger.info(f"  {key}:")
                    for sub_key, sub_value in metrics[key].items():
                        logger.info(f"    {sub_key}: {sub_value}")
                else:
                    logger.info(f"  {key}: {value}")
        
        logger.info(f"\nTOTAL TEST DURATION: {total_duration:.2f} seconds")
        
        # Calculate overall performance metrics
        total_records = 0
        total_migration_time = 0
        
        for test_name, metrics in self.performance_metrics.items():
            if 'record_count' in metrics:
                total_records += metrics['record_count']
            if 'bulk_migration' in test_name and 'duration_seconds' in metrics:
                total_migration_time += metrics['duration_seconds']
        
        if total_records > 0 and total_migration_time > 0:
            overall_rate = total_records / total_migration_time
            logger.info(f"OVERALL MIGRATION RATE: {overall_rate:,.0f} records/second")
            logger.info(f"TOTAL RECORDS PROCESSED: {total_records:,}")

def main():
    """Main function to run bulk migration tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test bulk migration performance')
    parser.add_argument('--records', type=int, default=1000000, 
                       help='Number of records to test with (default: 1M)')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick test with smaller dataset')
    
    args = parser.parse_args()
    
    if args.quick:
        record_count = min(args.records, 100000)  # Max 100K for quick test
        logger.info(f"Running quick test with {record_count:,} records")
    else:
        record_count = args.records
    
    # Initialize tester
    tester = BulkMigrationTester()
    
    # Run the test
    success = tester.run_full_test(record_count)
    
    if success:
        logger.info("✓ All tests passed successfully!")
        sys.exit(0)
    else:
        logger.error("✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

