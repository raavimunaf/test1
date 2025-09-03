#!/usr/bin/env python3
"""
Test ASE Driver Connection
This script tests the connection to Sybase using the ASE driver
"""

import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ase_connection():
    """Test connection to Sybase using ASE driver"""
    print("=" * 50)
    print("Testing Sybase ASE Driver Connection")
    print("=" * 50)
    
    # Get configuration from environment
    driver = os.getenv('SYBASE_DRIVER', 'Adaptive Server Enterprise')
    server = os.getenv('SYBASE_SERVER', 'localhost')
    port = os.getenv('SYBASE_PORT', '5000')
    uid = os.getenv('SYBASE_UID', 'sa')
    pwd = os.getenv('SYBASE_PWD', 'password')
    database = os.getenv('SYBASE_DB', 'testdb')
    
    print(f"Driver: {driver}")
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"Database: {database}")
    print(f"User: {uid}")
    print()
    
    try:
        # Build connection string
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"PORT={port};"
            f"UID={uid};"
            f"PWD={pwd};"
            f"DATABASE={database}"
        )
        
        print("Connection string:")
        print(connection_string)
        print()
        
        # Test connection
        print("Attempting to connect...")
        conn = pyodbc.connect(connection_string)
        
        print("✓ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT @@version")
        version = cursor.fetchone()
        
        if version:
            print(f"✓ Sybase version: {version[0]}")
        else:
            print("✓ Connected but couldn't get version info")
        
        # Close connection
        cursor.close()
        conn.close()
        print("✓ Connection closed successfully")
        
        return True
        
    except pyodbc.Error as e:
        print(f"✗ ODBC Error: {e}")
        return False
    except Exception as e:
        print(f"✗ General Error: {e}")
        return False

def list_available_drivers():
    """List all available ODBC drivers"""
    print("\n" + "=" * 50)
    print("Available ODBC Drivers")
    print("=" * 50)
    
    drivers = pyodbc.drivers()
    if drivers:
        for i, driver in enumerate(drivers, 1):
            print(f"{i}. {driver}")
    else:
        print("No ODBC drivers found")
    
    print()

if __name__ == "__main__":
    # List available drivers first
    list_available_drivers()
    
    # Test ASE connection
    success = test_ase_connection()
    
    if success:
        print("\n🎉 ASE driver connection test passed!")
        print("You can now run the main migration: python main_migration.py")
    else:
        print("\n❌ ASE driver connection test failed!")
        print("Please check your configuration and try again")
    
    print("\n" + "=" * 50)
