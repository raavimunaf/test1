#!/usr/bin/env python3
"""
Basic import test to isolate the segmentation fault
"""

print("Starting basic import test...")

try:
    print("1. Testing basic Python imports...")
    import sys
    import os
    print("✓ Basic imports successful")
    
    print("2. Testing dotenv...")
    from dotenv import load_dotenv
    print("✓ Dotenv import successful")
    ``
    print("3. Testing psycopg2...")
    import psycopg2
    print("✓ Psycopg2 import successful")
    
    print("4. Testing pyodbc...")
    import pyodbc
    print("✓ Pyodbc import successful")
    
    print("5. Testing schedule...")
    import schedule
    print("✓ Schedule import successful")
    
    print("\n✓ All imports successful!")
    
except Exception as e:
    print(f"✗ Import failed at step: {e}")
    import traceback
    traceback.print_exc()



