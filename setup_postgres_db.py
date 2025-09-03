#!/usr/bin/env python3
"""
PostgreSQL Database Setup Helper
This script helps create the PostgreSQL database and tables manually
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_postgres_database():
    """Setup PostgreSQL database and tables"""
    print("=" * 50)
    print("PostgreSQL Database Setup Helper")
    print("=" * 50)
    
    # Get configuration from environment
    host = os.getenv('PG_HOST', 'localhost')
    port = os.getenv('PG_PORT', '5432')
    user = os.getenv('PG_USER', 'postgres')
    password = os.getenv('PG_PASSWORD', 'password')
    dbname = os.getenv('PG_DB', 'testdb')
    
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Database: {dbname}")
    print()
    
    try:
        # Step 1: Connect to default postgres database
        print("Step 1: Connecting to default PostgreSQL database...")
        admin_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname='postgres'
        )
        admin_conn.autocommit = True
        print("✓ Connected to PostgreSQL successfully")
        
        # Step 2: Create testdb if it doesn't exist
        print("\nStep 2: Creating database 'testdb'...")
        with admin_conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
            if cur.fetchone() is None:
                cur.execute(f"CREATE DATABASE {dbname}")
                print(f"✓ Database '{dbname}' created successfully")
            else:
                print(f"✓ Database '{dbname}' already exists")
        
        admin_conn.close()
        
        # Step 3: Connect to testdb and create tables
        print("\nStep 3: Creating tables in 'testdb'...")
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        test_conn.autocommit = True
        
        with test_conn.cursor() as cur:
            # Create employees table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS employees (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                dept VARCHAR(50),
                salary NUMERIC(10,2),
                updated_at TIMESTAMP DEFAULT NOW()
            )
            """
            cur.execute(create_table_sql)
            print("✓ Employees table created/verified")
            
            # Create index
            create_index_sql = """
            CREATE INDEX IF NOT EXISTS idx_employees_updated_at 
            ON employees(updated_at)
            """
            cur.execute(create_index_sql)
            print("✓ Index created/verified")
            
            # Check if table has data
            cur.execute("SELECT COUNT(*) FROM employees")
            count = cur.fetchone()[0]
            print(f"✓ Employees table has {count} rows")
        
        test_conn.close()
        
        print("\n🎉 PostgreSQL database setup completed successfully!")
        print("You can now run the migration: python main_migration.py")
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ General Error: {e}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connection"""
    print("\n" + "=" * 50)
    print("Testing PostgreSQL Connection")
    print("=" * 50)
    
    host = os.getenv('PG_HOST', 'localhost')
    port = os.getenv('PG_PORT', '5432')
    user = os.getenv('PG_USER', 'postgres')
    password = os.getenv('PG_PASSWORD', 'password')
    dbname = os.getenv('PG_DB', 'testdb')
    
    try:
        # Test connection to testdb
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()[0]
            print(f"✓ Connected to PostgreSQL: {version}")
            
            cur.execute("SELECT current_database()")
            current_db = cur.fetchone()[0]
            print(f"✓ Current database: {current_db}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test connection first
    if test_postgres_connection():
        print("\n✓ PostgreSQL connection test passed!")
    else:
        print("\n⚠ PostgreSQL connection test failed!")
        print("Attempting to create database...")
    
    # Setup database
    success = setup_postgres_database()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Setup failed!")
        print("=" * 50)




