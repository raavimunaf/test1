#!/usr/bin/env python3
"""
Demo script for the bulk migration testing system
Shows how to use all components step by step
"""

import sys
import os
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n{step_num}. {description}")
    print("-" * 40)

def demo_data_generation():
    """Demonstrate data generation capabilities"""
    print_header("DATA GENERATION DEMO")
    
    try:
        from bulk_data_generator import BulkDataGenerator
        
        print_step(1, "Creating data generator for 100K records")
        generator = BulkDataGenerator(100000)
        
        print_step(2, "Generating sample data")
        start_time = time.time()
        sample_data = generator.generate_sample_data(1000)  # Start with 1K for demo
        end_time = time.time()
        
        duration = end_time - start_time
        speed = len(sample_data) / duration if duration > 0 else 0
        
        print(f"✓ Generated {len(sample_data):,} records in {duration:.2f} seconds")
        print(f"  Speed: {speed:,.0f} records/second")
        
        print_step(3, "Sample data preview")
        if sample_data:
            first_record = sample_data[0]
            print(f"  First record:")
            for key, value in list(first_record.items())[:5]:  # Show first 5 fields
                print(f"    {key}: {value}")
            print(f"    ... and {len(first_record) - 5} more fields")
        
        print_step(4, "Saving to file")
        output_file = "demo_sample.csv"
        generator.save_to_file(output_file, sample_data, 'csv')
        print(f"✓ Data saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import BulkDataGenerator: {e}")
        print("  Make sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Data generation demo failed: {e}")
        return False

def demo_performance_monitoring():
    """Demonstrate performance monitoring capabilities"""
    print_header("PERFORMANCE MONITORING DEMO")
    
    try:
        from performance_monitor import PerformanceMonitor
        
        print_step(1, "Creating performance monitor")
        monitor = PerformanceMonitor(monitoring_interval=1.0)
        
        print_step(2, "Getting current system status")
        monitor.print_current_status()
        
        print_step(3, "Starting monitoring for 5 seconds")
        print("  Starting monitoring...")
        monitor.start_monitoring()
        
        # Monitor for 5 seconds
        for i in range(5):
            time.sleep(1)
            print(f"  Monitoring... {i+1}/5 seconds")
        
        monitor.stop_monitoring()
        print("  Monitoring stopped")
        
        print_step(4, "Performance summary")
        summary = monitor.get_summary_stats()
        if summary:
            print(f"  Total samples: {summary.get('total_samples', 0)}")
            print(f"  Duration: {summary.get('monitoring_duration_seconds', 0):.2f} seconds")
            
            cpu = summary.get('cpu', {})
            print(f"  CPU Usage: Avg {cpu.get('avg_percent', 0)}%, Max {cpu.get('max_percent', 0)}%")
            
            memory = summary.get('memory', {})
            print(f"  Memory Usage: Avg {memory.get('avg_percent', 0)}%, Max {memory.get('max_percent', 0)}%")
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import PerformanceMonitor: {e}")
        print("  Make sure you have installed psutil:")
        print("  pip install psutil")
        return False
    except Exception as e:
        print(f"✗ Performance monitoring demo failed: {e}")
        return False

def demo_bulk_testing():
    """Demonstrate bulk testing capabilities"""
    print_header("BULK TESTING DEMO")
    
    print_step(1, "Checking available test options")
    print("  Available test scenarios:")
    print("    • Quick test (100K records): --quick --records 100000")
    print("    • Medium test (1M records): --records 1000000")
    print("    • Large test (10M records): --records 10000000")
    
    print_step(2, "Test execution commands")
    print("  Command line usage:")
    print("    python test_bulk_migration.py --quick --records 100000")
    print("    python test_bulk_migration.py --records 1000000")
    print("    python test_bulk_migration.py --records 10000000")
    
    print_step(3, "Batch file usage")
    print("  Windows users can use:")
    print("    run_bulk_test.bat")
    print("  This provides an interactive menu for easy testing")
    
    print_step(4, "Performance monitoring integration")
    print("  For comprehensive testing with monitoring:")
    print("    # Terminal 1: Start monitoring")
    print("    python performance_monitor.py --monitor")
    print("    # Terminal 2: Run migration test")
    print("    python test_bulk_migration.py --records 1000000")
    
    return True

def demo_configuration():
    """Demonstrate configuration options"""
    print_header("CONFIGURATION DEMO")
    
    try:
        from config import BULK_MIGRATION_CONFIG
        
        print_step(1, "Current bulk migration configuration")
        for key, value in BULK_MIGRATION_CONFIG.items():
            print(f"  {key}: {value}")
        
        print_step(2, "Environment variable configuration")
        print("  Create a .env file with these settings:")
        print("    BULK_BATCH_SIZE=10000")
        print("    MAX_RECORDS_PER_TEST=10000000")
        print("    PERFORMANCE_MONITORING=true")
        print("    MEMORY_THRESHOLD_MB=2048")
        print("    CPU_THRESHOLD_PERCENT=80")
        
        print_step(3, "Batch size optimization")
        print("  Recommended batch sizes:")
        print("    • High-memory systems (16GB+): 50000")
        print("    • Moderate systems (8GB): 10000")
        print("    • Low-memory systems (4GB): 5000")
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import configuration: {e}")
        return False

def main():
    """Main demo function"""
    print_header("BULK MIGRATION TESTING SYSTEM DEMO")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    demos = [
        ("Data Generation", demo_data_generation),
        ("Performance Monitoring", demo_performance_monitoring),
        ("Bulk Testing", demo_bulk_testing),
        ("Configuration", demo_configuration)
    ]
    
    success_count = 0
    total_demos = len(demos)
    
    for demo_name, demo_func in demos:
        try:
            if demo_func():
                success_count += 1
                print(f"✓ {demo_name} demo completed successfully")
            else:
                print(f"✗ {demo_name} demo failed")
        except Exception as e:
            print(f"✗ {demo_name} demo failed with error: {e}")
    
    print_header("DEMO SUMMARY")
    print(f"Completed: {success_count}/{total_demos} demos successfully")
    
    if success_count == total_demos:
        print("\n🎉 All demos completed successfully!")
        print("The bulk testing system is ready for use.")
        
        print("\nNext steps:")
        print("1. Test data generation: python test_bulk_generator.py")
        print("2. Run quick migration test: python test_bulk_migration.py --quick --records 100000")
        print("3. Start performance monitoring: python performance_monitor.py --monitor")
        print("4. Use batch file: run_bulk_test.bat")
        
    else:
        print(f"\n⚠ {total_demos - success_count} demo(s) failed.")
        print("Please check the error messages above and ensure all dependencies are installed.")
        print("\nInstallation command:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()

