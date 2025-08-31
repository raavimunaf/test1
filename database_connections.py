import pyodbc
import psycopg2
from psycopg2 import pool
import logging
from config import SYBASE_CONFIG, POSTGRES_CONFIG

logger = logging.getLogger(__name__)

class DatabaseConnections:
    def __init__(self):
        self.sybase_conn = None
        self.postgres_pool = None
        self._ensure_postgres_database()
        self._setup_postgres_pool()
    
    def _ensure_postgres_database(self):
        """Ensure the target PostgreSQL database exists before creating the pool"""
        try:
            admin_dsn = (
                f"host={POSTGRES_CONFIG['host']} "
                f"port={POSTGRES_CONFIG['port']} "
                f"dbname=postgres "
                f"user={POSTGRES_CONFIG['user']} "
                f"password={POSTGRES_CONFIG['password']}"
            )
            target_db = POSTGRES_CONFIG['dbname']
            with psycopg2.connect(admin_dsn, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
                    if cur.fetchone() is None:
                        cur.execute(f"CREATE DATABASE {target_db}")
                        logger.info(f"Created PostgreSQL database '{target_db}'")
        except Exception as e:
            # Non-fatal; pool creation may still fail which will be reported
            logger.warning(f"Could not ensure PostgreSQL database exists: {e}")
    
    def _setup_postgres_pool(self):
        """Setup PostgreSQL connection pool (psycopg2)"""
        try:
            dsn = (
                f"host={POSTGRES_CONFIG['host']} "
                f"port={POSTGRES_CONFIG['port']} "
                f"dbname={POSTGRES_CONFIG['dbname']} "
                f"user={POSTGRES_CONFIG['user']} "
                f"password={POSTGRES_CONFIG['password']}"
            )
            self.postgres_pool = pool.SimpleConnectionPool(1, 10, dsn)
            logger.info("PostgreSQL connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL connection pool: {e}")
            raise
    
    def get_sybase_connection(self):
        """Get Sybase connection (pyodbc + FreeTDS)"""
        try:
            if self.sybase_conn is None or self.sybase_conn.closed:
                tds_part = f";TDS_Version={SYBASE_CONFIG['tds_version']}" if SYBASE_CONFIG.get('tds_version') else ""
                connection_string = (
                    f"DRIVER={{{SYBASE_CONFIG['driver']}}};"
                    f"SERVER={SYBASE_CONFIG['server']};"
                    f"PORT={SYBASE_CONFIG['port']};"
                    f"UID={SYBASE_CONFIG['uid']};"
                    f"PWD={SYBASE_CONFIG['pwd']};"
                    f"DATABASE={SYBASE_CONFIG['database']}"
                    f"{tds_part}"
                )
                self.sybase_conn = pyodbc.connect(connection_string)
                logger.info("Sybase connection established successfully")
            
            return self.sybase_conn
        except Exception as e:
            logger.error(f"Failed to connect to Sybase: {e}")
            raise
    
    def get_postgres_connection(self):
        """Get PostgreSQL connection from pool"""
        try:
            if self.postgres_pool is None:
                self._setup_postgres_pool()
            conn = self.postgres_pool.getconn()
            if conn is None:
                raise Exception("Failed to get connection from pool")
            return conn
        except Exception as e:
            logger.error(f"Failed to get PostgreSQL connection: {e}")
            raise
    
    def return_postgres_connection(self, conn):
        """Return PostgreSQL connection to pool"""
        try:
            if conn is not None:
                self.postgres_pool.putconn(conn)
        except Exception as e:
            logger.error(f"Error returning connection to pool: {e}")
    
    def close_all(self):
        """Close all connections"""
        try:
            if self.sybase_conn and not self.sybase_conn.closed:
                self.sybase_conn.close()
                logger.info("Sybase connection closed")
            
            if self.postgres_pool:
                self.postgres_pool.closeall()
                logger.info("PostgreSQL connection pool closed")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")
    
    def test_connections(self):
        """Test both database connections"""
        try:
            # Test Sybase
            syb_conn = self.get_sybase_connection()
            syb_cur = syb_conn.cursor()
            syb_cur.execute("SELECT 1")
            syb_cur.fetchone()
            syb_cur.close()
            logger.info("✓ Sybase connection test successful")
            
            # Test PostgreSQL
            pg_conn = self.get_postgres_connection()
            with pg_conn.cursor() as pg_cur:
                pg_cur.execute("SELECT 1")
                pg_cur.fetchone()
            self.return_postgres_connection(pg_conn)
            logger.info("✓ PostgreSQL connection test successful")
            
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False 