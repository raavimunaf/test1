#!/usr/bin/env python3
"""
Sybase Database Setup Helper
This script helps create the proper database and tables in Sybase
"""

import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_sybase_database():
    """Setup Sybase database and tables"""
    print("=" * 50)
    print("Sybase Database Setup Helper")
    print("=" * 50)
    
    # Get configuration from environment
    driver = os.getenv('SYBASE_DRIVER', 'Adaptive Server Enterprise')
    server = os.getenv('SYBASE_SERVER', 'localhost')
    port = os.getenv('SYBASE_PORT', '5000')
    uid = os.getenv('SYBASE_UID', 'sa')
    pwd = os.getenv('SYBASE_PWD', 'password')
    
    print(f"Driver: {driver}")
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"User: {uid}")
    print()
    
    try:
        # Step 1: Connect to master database first
        print("Step 1: Connecting to master database...")
        master_conn_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"PORT={port};"
            f"UID={uid};"
            f"PWD={pwd};"
            f"DATABASE=master"
        )
        
        master_conn = pyodbc.connect(master_conn_string)
        print("✓ Connected to master database successfully")
        
        # Step 2: Create tables directly in master database
        print("\nStep 2: Creating tables in master database...")
        cursor = master_conn.cursor()
        
        # Check if employees table exists
        cursor.execute("SELECT COUNT(*) FROM sysobjects WHERE name = 'employees'")
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            # Create employees table
            create_table_sql = """
            CREATE TABLE employees (
                id int primary key,
                name varchar(100),
                dept varchar(50),
                salary numeric(10,2),
                updated_at datetime default getdate()
            )
            """
            cursor.execute(create_table_sql)
            print("✓ Employees table created successfully")
        else:
            print("✓ Employees table already exists")
        
        # Check if table has data
        cursor.execute("SELECT COUNT(*) FROM employees")
        row_count = cursor.fetchone()[0]
        
        if row_count == 0:
            # Insert sample data
            insert_data_sql = """
            INSERT INTO employees (id, name, dept, salary) VALUES
            (1, 'Alice', 'HR', 55000.00),
            (2, 'Bob', 'IT', 75000.00),
            (3, 'Charlie', 'Finance', 62000.00)
            """
            cursor.execute(insert_data_sql)
            print("✓ Sample data inserted successfully")
        else:
            print(f"✓ Employees table already has {row_count} rows")
        
        master_conn.commit()
        master_conn.close()
        
        print("\n🎉 Sybase database setup completed successfully!")
        print("You can now update your .env file to use SYBASE_DB=master")
        return True
        
        # Check if employees table exists
        cursor.execute("SELECT COUNT(*) FROM sysobjects WHERE name = 'employees'")
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            # Create employees table
            create_table_sql = """
            CREATE TABLE employees (
                id int primary key,
                name varchar(100),
                dept varchar(50),
                salary numeric(10,2),
                updated_at datetime default getdate()
            )
            """
            cursor.execute(create_table_sql)
            print("✓ Employees table created successfully")
        else:
            print("✓ Employees table already exists")
        
        # Check if table has data
        cursor.execute("SELECT COUNT(*) FROM employees")
        row_count = cursor.fetchone()[0]
        
        if row_count == 0:
            # Insert sample data
            insert_data_sql = """
            INSERT INTO employees (id, name, dept, salary) VALUES
            (1, 'Alice', 'HR', 55000.00),
            (2, 'Bob', 'IT', 75000.00),
            (3, 'Charlie', 'Finance', 62000.00)
            """
            cursor.execute(insert_data_sql)
            print("✓ Sample data inserted successfully")
        else:
            print(f"✓ Employees table already has {row_count} rows")
        
        testdb_conn.commit()
        testdb_conn.close()
        
        print("\n🎉 Sybase database setup completed successfully!")
        print("You can now update your .env file to use SYBASE_DB=testdb")
        return True
        
    except pyodbc.Error as e:
        print(f"\n❌ ODBC Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ General Error: {e}")
        return False

def test_connection_to_master():
    """Test connection to master database"""
    print("\n" + "=" * 50)
    print("Testing Connection to master database")
    print("=" * 50)
    
    driver = os.getenv('SYBASE_DRIVER', 'Adaptive Server Enterprise')
    server = os.getenv('SYBASE_SERVER', 'localhost')
    port = os.getenv('SYBASE_PORT', '5000')
    uid = os.getenv('SYBASE_UID', 'sa')
    pwd = os.getenv('SYBASE_PWD', 'password')
    
    try:
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"PORT={port};"
            f"UID={uid};"
            f"PWD={pwd};"
            f"DATABASE=master"
        )
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        print(f"✓ Connected to master database successfully")
        print(f"✓ Employees table has {count} rows")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Setup database
    success = setup_sybase_database()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Sybase setup completed successfully!")
        print("=" * 50)
        
        # Test connection to master
        if test_connection_to_master():
            print("\n🎉 Everything is working! Now update your .env file:")
            print("   Change: SYBASE_DB=tempdb")
            print("   To:     SYBASE_DB=master")
        else:
            print("\n⚠ master database connection test failed")
    else:
        print("\n" + "=" * 50)
        print("❌ Sybase setup failed!")
        print("=" * 50)
