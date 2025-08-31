import logging
from database_connections import DatabaseConnections
from config import MIGRATION_CONFIG

logger = logging.getLogger(__name__)

class SchemaMigration:
    def __init__(self):
        self.db_connections = DatabaseConnections()
    
    def create_sample_table_sybase(self):
        """Create the sample employees table in Sybase"""
        try:
            conn = self.db_connections.get_sybase_connection()
            cursor = conn.cursor()
            
            # Create table
            create_table_sql = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
            CREATE TABLE employees (
                id int primary key,
                name varchar(100),
                dept varchar(50),
                salary numeric(10,2),
                updated_at datetime default getdate()
            )
            """
            cursor.execute(create_table_sql)
            
            # Insert sample data
            insert_data_sql = """
            IF NOT EXISTS (SELECT * FROM employees WHERE id = 1)
            INSERT INTO employees (id, name, dept, salary) VALUES
            (1, 'Alice', 'HR', 55000.00),
            (2, 'Bob', 'IT', 75000.00),
            (3, 'Charlie', 'Finance', 62000.00)
            """
            cursor.execute(insert_data_sql)
            
            conn.commit()
            cursor.close()
            logger.info("✓ Sample table created in Sybase successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create sample table in Sybase: {e}")
            return False
    
    def create_table_postgres(self, table_name, columns_sql):
        """Create table in PostgreSQL"""
        conn = None
        try:
            conn = self.db_connections.get_postgres_connection()
            cursor = conn.cursor()
            
            # Drop table if exists
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            
            # Create table
            create_sql = f"CREATE TABLE {table_name} ({columns_sql})"
            cursor.execute(create_sql)
            
            conn.commit()
            cursor.close()
            logger.info(f"✓ Table {table_name} created in PostgreSQL successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create table {table_name} in PostgreSQL: {e}")
            return False
        finally:
            if conn:
                self.db_connections.return_postgres_connection(conn)
    
    def migrate_employees_schema(self):
        """Migrate the employees table schema to PostgreSQL"""
        columns_sql = """
            id INT PRIMARY KEY,
            name VARCHAR(100),
            dept VARCHAR(50),
            salary NUMERIC(10,2),
            updated_at TIMESTAMP DEFAULT NOW()
        """
        
        return self.create_table_postgres('employees', columns_sql)
    
    def get_sybase_table_schema(self, table_name):
        """Get table schema from Sybase"""
        try:
            conn = self.db_connections.get_sybase_connection()
            cursor = conn.cursor()
            
            # Get column information
            schema_query = """
            SELECT 
                c.name as column_name,
                t.name as data_type,
                c.length,
                c.prec,
                c.scale,
                c.isnullable,
                CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END as is_primary_key
            FROM syscolumns c
            JOIN systypes t ON c.usertype = t.usertype
            LEFT JOIN sysindexkeys pk ON c.id = pk.id AND c.colid = pk.colid AND pk.indid = 1
            WHERE c.id = object_id(?)
            ORDER BY c.colid
            """
            
            cursor.execute(schema_query, (table_name,))
            columns = cursor.fetchall()
            
            cursor.close()
            return columns
            
        except Exception as e:
            logger.error(f"Failed to get schema for table {table_name}: {e}")
            return []
    
    def convert_sybase_to_postgres_type(self, sybase_type, length, precision, scale):
        """Convert Sybase data type to PostgreSQL equivalent"""
        type_mapping = {
            'int': 'INTEGER',
            'smallint': 'SMALLINT',
            'bigint': 'BIGINT',
            'tinyint': 'SMALLINT',
            'decimal': f'NUMERIC({precision},{scale})',
            'numeric': f'NUMERIC({precision},{scale})',
            'float': 'DOUBLE PRECISION',
            'real': 'REAL',
            'money': 'NUMERIC(19,4)',
            'smallmoney': 'NUMERIC(10,4)',
            'char': f'CHAR({length})',
            'varchar': f'VARCHAR({length})',
            'text': 'TEXT',
            'nchar': f'CHAR({length})',
            'nvarchar': f'VARCHAR({length})',
            'ntext': 'TEXT',
            'binary': f'BYTEA',
            'varbinary': f'BYTEA',
            'image': 'BYTEA',
            'bit': 'BOOLEAN',
            'datetime': 'TIMESTAMP',
            'smalldatetime': 'TIMESTAMP',
            'date': 'DATE',
            'time': 'TIME',
            'timestamp': 'TIMESTAMP'
        }
        
        return type_mapping.get(sybase_type.lower(), 'TEXT')
    
    def generate_postgres_schema(self, table_name):
        """Generate PostgreSQL CREATE TABLE statement from Sybase schema"""
        try:
            columns = self.get_sybase_table_schema(table_name)
            if not columns:
                return None
            
            column_definitions = []
            primary_keys = []
            
            for col in columns:
                col_name = col[0]
                data_type = col[1]
                length = col[2]
                precision = col[3]
                scale = col[4]
                is_nullable = col[5]
                is_pk = col[6]
                
                # Convert data type
                pg_type = self.convert_sybase_to_postgres_type(data_type, length, precision, scale)
                
                # Build column definition
                col_def = f"{col_name} {pg_type}"
                
                if not is_nullable:
                    col_def += " NOT NULL"
                
                column_definitions.append(col_def)
                
                if is_pk:
                    primary_keys.append(col_name)
            
            # Add primary key constraint if exists
            if primary_keys:
                pk_constraint = f"PRIMARY KEY ({', '.join(primary_keys)})"
                column_definitions.append(pk_constraint)
            
            return f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(column_definitions) + "\n)"
            
        except Exception as e:
            logger.error(f"Failed to generate PostgreSQL schema: {e}")
            return None 