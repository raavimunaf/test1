import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sybase Configuration
SYBASE_CONFIG = {
    'driver': os.getenv('SYBASE_DRIVER', 'Adaptive Server Enterprise'),
    'server': os.getenv('SYBASE_SERVER', 'DESKTOP-NM4NO11'),
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
    'password': os.getenv('PG_PASSWORD', 'StrongPass2'),
    'port': os.getenv('PG_PORT', '5432')
}

# Migration Settings
MIGRATION_CONFIG = {
    'batch_size': int(os.getenv('BATCH_SIZE', '1000')),
    'sync_interval_minutes': int(os.getenv('SYNC_INTERVAL_MINUTES', '5')),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'enable_logging': os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
} 