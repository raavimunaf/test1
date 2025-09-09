import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sybase Configuration
SYBASE_CONFIG = {
    'driver': os.getenv('SYBASE_DRIVER', 'Adaptive Server Enterprise'),
    'server': os.getenv('SYBASE_SERVER', 'localhost'),
    'port': os.getenv('SYBASE_PORT', '5000'),
    'uid': os.getenv('SYBASE_UID', 'sa'),
    'pwd': os.getenv('SYBASE_PWD', 'password'),
    'database': os.getenv('SYBASE_DB', 'testdb')
}

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    'host': os.getenv('PG_HOST', 'localhost'),
    'dbname': os.getenv('PG_DB', 'testdb'),
    'user': os.getenv('PG_USER', 'postgres'),
    'password': os.getenv('PG_PASSWORD', 'password'),
    'port': os.getenv('PG_PORT', '5432')
}

# Migration Settings
MIGRATION_CONFIG = {
    'batch_size': int(os.getenv('BATCH_SIZE', '1000')),
    'sync_interval_minutes': int(os.getenv('SYNC_INTERVAL_MINUTES', '5')),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'enable_logging': os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
}

# Bulk Migration Settings
BULK_MIGRATION_CONFIG = {
    'bulk_batch_size': int(os.getenv('BULK_BATCH_SIZE', '10000')),
    'max_records_per_test': int(os.getenv('MAX_RECORDS_PER_TEST', '1000000')),
    'performance_monitoring': os.getenv('PERFORMANCE_MONITORING', 'true').lower() == 'true',
    'memory_threshold_mb': int(os.getenv('MEMORY_THRESHOLD_MB', '2048')),
    'cpu_threshold_percent': int(os.getenv('CPU_THRESHOLD_PERCENT', '80')),
    'enable_parallel_processing': os.getenv('ENABLE_PARALLEL_PROCESSING', 'false').lower() == 'true',
    'parallel_workers': int(os.getenv('PARALLEL_WORKERS', '4'))
} 