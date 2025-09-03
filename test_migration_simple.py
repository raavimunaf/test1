#!/usr/bin/env python3
"""
Simple test to check if main_migration.py can run
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing import of main_migration...")
    import main_migration
    print("✓ Import successful")
    
    print("Testing import of database_connections...")
    from database_connections import DatabaseConnections
    print("✓ Database connections import successful")
    
    print("Testing import of schema_migration...")
    from schema_migration import SchemaMigration
    print("✓ Schema migration import successful")
    
    print("Testing import of data_migration...")
    from data_migration import DataMigration
    print("✓ Data migration import successful")
    
    print("Testing import of config...")
    from config import MIGRATION_CONFIG
    print("✓ Config import successful")
    
    print("\n✓ All imports successful! The script should run.")
    
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()




