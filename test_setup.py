#!/usr/bin/env python3
"""
Test Setup Script
This script tests the basic functionality of the migration system.
Run this to verify your setup before running the full migration.
"""

import logging
import sys
from database_connections import DatabaseConnections
from config import SYBASE_CONFIG, POSTGRES_CONFIG

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    
    print(f"Sybase Config: {SYBASE_CONFIG}")
    print(f"PostgreSQL Config: {POSTGRES_CONFIG}")
    
    # Check required fields
    required_sybase = ['server', 'port', 'uid', 'pwd', 'database']
    required_postgres = ['host', 'dbname', 'user', 'password', 'port']
    
    for field in required_sybase:
        if not SYBASE_CONFIG.get(field):
            print(f"❌ Missing Sybase configuration: {field}")
            return False
    
    for field in required_postgres:
        if not POSTGRES_CONFIG.get(field):
            print(f"❌ Missing PostgreSQL configuration: {field}")
            return False
    
    print("✅ Configuration loaded successfully")
    return True

def test_database_connections():
    """Test database connections"""
    print("\nTesting database connections...")
    
    try:
        db_connections = DatabaseConnections()
        
        # Test connections
        if db_connections.test_connections():
            print("✅ Database connections successful")
            return True
        else:
            print("❌ Database connections failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False
    finally:
        try:
            db_connections.close_all()
        except:
            pass

def test_imports():
    """Test that all modules can be imported"""
    print("\nTesting module imports...")
    
    try:
        from schema_migration import SchemaMigration
        from data_migration import DataMigration
        from backup_restore import BackupRestore
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False

def main():
    """Main test function"""
    setup_logging()
    
    print("=" * 50)
    print("Sybase to PostgreSQL Migration - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Module Imports", test_imports),
        ("Database Connections", test_database_connections),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready for migration.")
        print("You can now run: python main_migration.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 