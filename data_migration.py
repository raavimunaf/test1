import logging
from database_connections import DatabaseConnections
from config import MIGRATION_CONFIG
import time

logger = logging.getLogger(__name__)

class DataMigration:
    def __init__(self):
        self.db_connections = DatabaseConnections()
        self.batch_size = MIGRATION_CONFIG['batch_size']
    
    def migrate_employees_data(self):
        """Migrate data from Sybase employees table to PostgreSQL"""
        try:
            # Get connections
            syb_conn = self.db_connections.get_sybase_connection()
            pg_conn = self.db_connections.get_postgres_connection()
            
            syb_cur = syb_conn.cursor()
            pg_cur = pg_conn.cursor()
            
            # Fetch data from Sybase
            logger.info("Fetching data from Sybase employees table...")
            syb_cur.execute("SELECT id, name, dept, salary, updated_at FROM employees")
            rows = syb_cur.fetchall()
            
            if not rows:
                logger.warning("No data found in Sybase employees table")
                return False
            
            logger.info(f"Found {len(rows)} rows to migrate")
            
            # Process in batches
            success_count = 0
            error_count = 0
            
            for i in range(0, len(rows), self.batch_size):
                batch = rows[i:i + self.batch_size]
                logger.info(f"Processing batch {i//self.batch_size + 1} ({len(batch)} rows)")
                
                try:
                    # Insert batch into PostgreSQL
                    for row in batch:
                        pg_cur.execute("""
                            INSERT INTO employees (id, name, dept, salary, updated_at)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (id) DO UPDATE SET
                                name = EXCLUDED.name,
                                dept = EXCLUDED.dept,
                                salary = EXCLUDED.salary,
                                updated_at = EXCLUDED.updated_at
                        """, row)
                    
                    pg_conn.commit()
                    success_count += len(batch)
                    logger.info(f"✓ Batch {i//self.batch_size + 1} processed successfully")
                    
                except Exception as e:
                    pg_conn.rollback()
                    error_count += len(batch)
                    logger.error(f"✗ Batch {i//self.batch_size + 1} failed: {e}")
            
            # Close cursors
            syb_cur.close()
            pg_cur.close()
            self.db_connections.return_postgres_connection(pg_conn)
            
            logger.info(f"Migration completed: {success_count} successful, {error_count} failed")
            return error_count == 0
            
        except Exception as e:
            logger.error(f"Data migration failed: {e}")
            return False
    
    def sync_table_data(self, table_name, key_column='id'):
        """Generic method to sync table data from Sybase to PostgreSQL"""
        try:
            # Get connections
            syb_conn = self.db_connections.get_sybase_connection()
            pg_conn = self.db_connections.get_postgres_connection()
            
            syb_cur = syb_conn.cursor()
            pg_cur = pg_conn.cursor()
            
            # Get all columns from Sybase
            syb_cur.execute(f"SELECT * FROM {table_name}")
            columns = [column[0] for column in syb_cur.description]
            
            # Build dynamic SELECT query
            select_columns = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            # Fetch data
            syb_cur.execute(f"SELECT {select_columns} FROM {table_name}")
            rows = syb_cur.fetchall()
            
            if not rows:
                logger.warning(f"No data found in Sybase table {table_name}")
                return False
            
            logger.info(f"Syncing {len(rows)} rows from {table_name}")
            
            # Build dynamic INSERT/UPDATE query
            update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != key_column])
            
            insert_sql = f"""
                INSERT INTO {table_name} ({select_columns})
                VALUES ({placeholders})
                ON CONFLICT ({key_column}) DO UPDATE SET
                    {update_set}
            """
            
            # Process in batches
            success_count = 0
            error_count = 0
            
            for i in range(0, len(rows), self.batch_size):
                batch = rows[i:i + self.batch_size]
                
                try:
                    for row in batch:
                        pg_cur.execute(insert_sql, row)
                    
                    pg_conn.commit()
                    success_count += len(batch)
                    
                except Exception as e:
                    pg_conn.rollback()
                    error_count += len(batch)
                    logger.error(f"Batch failed: {e}")
            
            # Close cursors
            syb_cur.close()
            pg_cur.close()
            self.db_connections.return_postgres_connection(pg_conn)
            
            logger.info(f"Sync completed for {table_name}: {success_count} successful, {error_count} failed")
            return error_count == 0
            
        except Exception as e:
            logger.error(f"Table sync failed for {table_name}: {e}")
            return False
    
    def get_table_row_count(self, table_name, database='postgres'):
        """Get row count for a table"""
        try:
            if database == 'postgres':
                conn = self.db_connections.get_postgres_connection()
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                cursor.close()
                self.db_connections.return_postgres_connection(conn)
            else:  # sybase
                conn = self.db_connections.get_sybase_connection()
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                cursor.close()
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get row count for {table_name}: {e}")
            return -1
    
    def verify_migration(self, table_name):
        """Verify that data migration was successful"""
        try:
            sybase_count = self.get_table_row_count(table_name, 'sybase')
            postgres_count = self.get_table_row_count(table_name, 'postgres')
            
            if sybase_count == -1 or postgres_count == -1:
                return False
            
            logger.info(f"Row counts - Sybase: {sybase_count}, PostgreSQL: {postgres_count}")
            
            if sybase_count == postgres_count:
                logger.info("✓ Migration verification successful - row counts match")
                return True
            else:
                logger.error(f"✗ Migration verification failed - row counts don't match")
                return False
                
        except Exception as e:
            logger.error(f"Migration verification failed: {e}")
            return False
    
    def incremental_sync(self, table_name, timestamp_column='updated_at'):
        """Perform incremental sync based on timestamp column"""
        try:
            # Get connections
            syb_conn = self.db_connections.get_sybase_connection()
            pg_conn = self.db_connections.get_postgres_connection()
            
            syb_cur = syb_conn.cursor()
            pg_cur = pg_conn.cursor()
            
            # Get last sync timestamp from PostgreSQL
            pg_cur.execute(f"SELECT MAX({timestamp_column}) FROM {table_name}")
            last_sync = pg_cur.fetchone()[0]
            
            if last_sync is None:
                logger.info("No previous sync found, performing full sync")
                return self.sync_table_data(table_name)
            
            # Get updated records from Sybase
            syb_cur.execute(f"SELECT * FROM {table_name} WHERE {timestamp_column} > ?", (last_sync,))
            updated_rows = syb_cur.fetchall()
            
            if not updated_rows:
                logger.info("No updates found since last sync")
                return True
            
            logger.info(f"Found {len(updated_rows)} updated rows for incremental sync")
            
            # Process updates
            columns = [column[0] for column in syb_cur.description]
            select_columns = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            # Build dynamic INSERT/UPDATE query
            key_column = 'id'  # Assuming 'id' is the primary key
            update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != key_column])
            
            insert_sql = f"""
                INSERT INTO {table_name} ({select_columns})
                VALUES ({placeholders})
                ON CONFLICT ({key_column}) DO UPDATE SET
                    {update_set}
            """
            
            success_count = 0
            for row in updated_rows:
                try:
                    pg_cur.execute(insert_sql, row)
                    success_count += 1
                except Exception as e:
                    logger.error(f"Failed to sync row: {e}")
            
            pg_conn.commit()
            
            # Close cursors
            syb_cur.close()
            pg_cur.close()
            self.db_connections.return_postgres_connection(pg_conn)
            
            logger.info(f"Incremental sync completed: {success_count} rows updated")
            return True
            
        except Exception as e:
            logger.error(f"Incremental sync failed: {e}")
            return False 