#!/usr/bin/env python3
"""
Simple test script for bulk data generator
Tests basic functionality without requiring database connections
"""

import sys
import os
import time
import tempfile

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bulk_data_generator import BulkDataGenerator
    print("✓ BulkDataGenerator import successful")
except ImportError as e:
    print(f"✗ Failed to import BulkDataGenerator: {e}")
    sys.exit(1)

def test_data_generation():
    """Test basic data generation functionality"""
    print("\n" + "=" * 50)
    print("Testing Data Generation")
    print("=" * 50)
    
    # Test 1: Small sample generation
    print("\n1. Testing small sample generation (1K records)...")
    start_time = time.time()
    
    generator = BulkDataGenerator(1000)
    sample_data = generator.generate_sample_data(1000)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Generated {len(sample_data):,} records in {duration:.2f} seconds")
    print(f"  Speed: {len(sample_data) / duration:,.0f} records/second")
    
    # Test 2: Data structure validation
    print("\n2. Validating data structure...")
    if sample_data:
        first_record = sample_data[0]
        expected_fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone',
            'department', 'job_title', 'salary', 'hire_date', 'experience_years',
            'city', 'state', 'is_active', 'created_at', 'updated_at'
        ]
        
        missing_fields = [field for field in expected_fields if field not in first_record]
        if missing_fields:
            print(f"✗ Missing fields: {missing_fields}")
            return False
        else:
            print("✓ All expected fields present")
        
        # Check data types
        if isinstance(first_record['employee_id'], str) and first_record['employee_id'].startswith('EMP'):
            print("✓ Employee ID format correct")
        else:
            print("✗ Employee ID format incorrect")
            return False
        
        if isinstance(first_record['salary'], (int, float)) and first_record['salary'] > 0:
            print("✓ Salary format correct")
        else:
            print("✗ Salary format incorrect")
            return False
    
    # Test 3: Batch generation
    print("\n3. Testing batch generation...")
    batch_size = 5000
    total_records = 10000
    
    generator = BulkDataGenerator(total_records)
    generator.batch_size = batch_size
    
    batch_count = 0
    total_generated = 0
    
    for batch in generator.generate_all_data():
        batch_count += 1
        total_generated += len(batch)
        print(f"  Batch {batch_count}: {len(batch):,} records")
    
    print(f"✓ Generated {total_generated:,} records in {batch_count} batches")
    
    # Test 4: File output
    print("\n4. Testing file output...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        generator.save_to_file(temp_filename, sample_data[:100], 'csv')
        
        # Check if file was created and has content
        if os.path.exists(temp_filename):
            file_size = os.path.getsize(temp_filename)
            print(f"✓ CSV file created: {temp_filename}")
            print(f"  File size: {file_size:,} bytes")
            
            # Read first few lines to verify content
            with open(temp_filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # Header + at least one data row
                    print(f"✓ File contains {len(lines)} lines")
                    print(f"  Header: {lines[0].strip()}")
                else:
                    print("✗ File content insufficient")
                    return False
        else:
            print("✗ File was not created")
            return False
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    return True

def test_performance_scaling():
    """Test performance scaling with different record counts"""
    print("\n" + "=" * 50)
    print("Testing Performance Scaling")
    print("=" * 50)
    
    test_sizes = [1000, 10000, 100000]
    
    for size in test_sizes:
        print(f"\nTesting with {size:,} records...")
        
        start_time = time.time()
        generator = BulkDataGenerator(size)
        data = generator.generate_sample_data(size)
        end_time = time.time()
        
        duration = end_time - start_time
        speed = size / duration if duration > 0 else 0
        
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  Speed: {speed:,.0f} records/second")
        print(f"  Memory usage: ~{len(str(data)) / (1024*1024):.2f} MB (estimated)")
        
        # Performance threshold check
        if speed < 1000:  # Minimum 1000 records/second
            print(f"  ⚠ Warning: Performance below threshold ({speed:,.0f} records/second)")
        else:
            print(f"  ✓ Performance acceptable")

def main():
    """Main test function"""
    print("Bulk Data Generator Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    if not test_data_generation():
        print("\n✗ Basic functionality tests failed!")
        sys.exit(1)
    
    # Test performance scaling
    test_performance_scaling()
    
    print("\n" + "=" * 50)
    print("✓ All tests completed successfully!")
    print("The bulk data generator is ready for use.")
    print("=" * 50)
    
    # Provide usage examples
    print("\nUsage Examples:")
    print("1. Generate sample data:")
    print("   python bulk_data_generator.py --sample 100000 --output sample.csv")
    print("\n2. Generate full dataset:")
    print("   python bulk_data_generator.py --total 10000000 --output bulk.csv")
    print("\n3. Run bulk migration test:")
    print("   python test_bulk_migration.py --quick --records 100000")

if __name__ == "__main__":
    main()

