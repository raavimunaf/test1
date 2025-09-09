#!/usr/bin/env python3
"""
Performance Monitor for Bulk Migration
Monitors system resources during migration operations
"""

import psutil
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitors system performance during migration operations"""
    
    def __init__(self, monitoring_interval: float = 1.0):
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitor_thread = None
        self.performance_data = []
        self.start_time = None
        self.end_time = None
        
    def start_monitoring(self):
        """Start performance monitoring in background thread"""
        if self.is_monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.is_monitoring = True
        self.start_time = datetime.now()
        self.performance_data = []
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.is_monitoring:
            logger.warning("Monitoring is not running")
            return
        
        self.is_monitoring = False
        self.end_time = datetime.now()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect performance metrics
                metrics = self._collect_metrics()
                self.performance_data.append(metrics)
                
                # Sleep for monitoring interval
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_metrics(self) -> Dict:
        """Collect current system performance metrics"""
        timestamp = datetime.now()
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_metrics = {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'percent': memory.percent,
            'free_gb': round(memory.free / (1024**3), 2)
        }
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_metrics = {
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent': disk.percent
        }
        
        # Network metrics
        network = psutil.net_io_counters()
        network_metrics = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
        # Process metrics (current process)
        process = psutil.Process()
        process_memory = process.memory_info()
        process_metrics = {
            'rss_mb': round(process_memory.rss / (1024**2), 2),
            'vms_mb': round(process_memory.vms / (1024**2), 2),
            'percent': process.memory_percent(),
            'cpu_percent': process.cpu_percent(),
            'num_threads': process.num_threads()
        }
        
        return {
            'timestamp': timestamp.isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'freq_mhz': round(cpu_freq.current, 2) if cpu_freq else None
            },
            'memory': memory_metrics,
            'disk': disk_metrics,
            'network': network_metrics,
            'process': process_metrics
        }
    
    def get_current_metrics(self) -> Dict:
        """Get current performance metrics (without storing)"""
        return self._collect_metrics()
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of collected performance data"""
        if not self.performance_data:
            return {}
        
        # CPU statistics
        cpu_percentages = [m['cpu']['percent'] for m in self.performance_data if m['cpu']['percent'] is not None]
        memory_percentages = [m['memory']['percent'] for m in self.performance_data]
        process_memory = [m['process']['rss_mb'] for m in self.performance_data]
        
        summary = {
            'total_samples': len(self.performance_data),
            'monitoring_duration_seconds': (self.end_time - self.start_time).total_seconds() if self.end_time else 0,
            'cpu': {
                'avg_percent': round(sum(cpu_percentages) / len(cpu_percentages), 2) if cpu_percentages else 0,
                'max_percent': max(cpu_percentages) if cpu_percentages else 0,
                'min_percent': min(cpu_percentages) if cpu_percentages else 0
            },
            'memory': {
                'avg_percent': round(sum(memory_percentages) / len(memory_percentages), 2) if memory_percentages else 0,
                'max_percent': max(memory_percentages) if memory_percentages else 0,
                'min_percent': min(memory_percentages) if memory_percentages else 0
            },
            'process_memory': {
                'avg_mb': round(sum(process_memory) / len(process_memory), 2) if process_memory else 0,
                'max_mb': max(process_memory) if process_memory else 0,
                'min_mb': min(process_memory) if process_memory else 0
            }
        }
        
        return summary
    
    def print_current_status(self):
        """Print current system status"""
        metrics = self.get_current_metrics()
        
        print("\n" + "=" * 60)
        print("CURRENT SYSTEM STATUS")
        print("=" * 60)
        print(f"Timestamp: {metrics['timestamp']}")
        
        print(f"\nCPU:")
        print(f"  Usage: {metrics['cpu']['percent']}%")
        print(f"  Cores: {metrics['cpu']['count']}")
        if metrics['cpu']['freq_mhz']:
            print(f"  Frequency: {metrics['cpu']['freq_mhz']} MHz")
        
        print(f"\nMemory:")
        print(f"  Total: {metrics['memory']['total_gb']} GB")
        print(f"  Used: {metrics['memory']['used_gb']} GB ({metrics['memory']['percent']}%)")
        print(f"  Available: {metrics['memory']['available_gb']} GB")
        
        print(f"\nDisk:")
        print(f"  Total: {metrics['disk']['total_gb']} GB")
        print(f"  Used: {metrics['disk']['used_gb']} GB ({metrics['disk']['percent']}%)")
        print(f"  Free: {metrics['disk']['free_gb']} GB")
        
        print(f"\nProcess:")
        print(f"  Memory: {metrics['process']['rss_mb']} MB (RSS)")
        print(f"  CPU: {metrics['process']['cpu_percent']}%")
        print(f"  Threads: {metrics['process']['num_threads']}")
        
        print("=" * 60)
    
    def save_metrics_to_file(self, filename: str, format_type: str = 'json'):
        """Save collected metrics to file"""
        if not self.performance_data:
            logger.warning("No performance data to save")
            return
        
        if format_type.lower() == 'json':
            self._save_to_json(filename)
        elif format_type.lower() == 'csv':
            self._save_to_csv(filename)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'")
    
    def _save_to_json(self, filename: str):
        """Save metrics to JSON file"""
        data = {
            'monitoring_info': {
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': self.end_time.isoformat() if self.end_time else None,
                'monitoring_interval': self.monitoring_interval,
                'total_samples': len(self.performance_data)
            },
            'summary_stats': self.get_summary_stats(),
            'performance_data': self.performance_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Performance metrics saved to {filename}")
    
    def _save_to_csv(self, filename: str):
        """Save metrics to CSV file"""
        import csv
        
        if not self.performance_data:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Flatten the nested structure for CSV
            fieldnames = [
                'timestamp', 'cpu_percent', 'cpu_count', 'cpu_freq_mhz',
                'memory_total_gb', 'memory_used_gb', 'memory_available_gb', 'memory_percent',
                'disk_total_gb', 'disk_used_gb', 'disk_free_gb', 'disk_percent',
                'process_rss_mb', 'process_vms_mb', 'process_percent', 'process_cpu_percent', 'process_threads'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for metrics in self.performance_data:
                row = {
                    'timestamp': metrics['timestamp'],
                    'cpu_percent': metrics['cpu']['percent'],
                    'cpu_count': metrics['cpu']['count'],
                    'cpu_freq_mhz': metrics['cpu']['freq_mhz'],
                    'memory_total_gb': metrics['memory']['total_gb'],
                    'memory_used_gb': metrics['memory']['used_gb'],
                    'memory_available_gb': metrics['memory']['available_gb'],
                    'memory_percent': metrics['memory']['percent'],
                    'disk_total_gb': metrics['disk']['total_gb'],
                    'disk_used_gb': metrics['disk']['used_gb'],
                    'disk_free_gb': metrics['disk']['free_gb'],
                    'disk_percent': metrics['disk']['percent'],
                    'process_rss_mb': metrics['process']['rss_mb'],
                    'process_vms_mb': metrics['process']['vms_mb'],
                    'process_percent': metrics['process']['percent'],
                    'process_cpu_percent': metrics['process']['cpu_percent'],
                    'process_threads': metrics['process']['num_threads']
                }
                writer.writerow(row)
        
        logger.info(f"Performance metrics saved to {filename}")

class MigrationPerformanceTracker:
    """Tracks performance during specific migration operations"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.operation_metrics = {}
    
    def start_tracking(self, operation_name: str):
        """Start tracking performance for a specific operation"""
        logger.info(f"Starting performance tracking for: {operation_name}")
        self.monitor.start_monitoring()
        self.operation_metrics[operation_name] = {
            'start_time': datetime.now(),
            'monitor': self.monitor
        }
    
    def stop_tracking(self, operation_name: str):
        """Stop tracking performance for a specific operation"""
        if operation_name not in self.operation_metrics:
            logger.warning(f"No tracking found for operation: {operation_name}")
            return
        
        logger.info(f"Stopping performance tracking for: {operation_name}")
        self.monitor.stop_monitoring()
        
        self.operation_metrics[operation_name]['end_time'] = datetime.now()
        self.operation_metrics[operation_name]['summary'] = self.monitor.get_summary_stats()
        
        # Save metrics
        filename = f"performance_{operation_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.monitor.save_metrics_to_file(filename, 'json')
        
        logger.info(f"Performance tracking completed for: {operation_name}")
        logger.info(f"Metrics saved to: {filename}")
    
    def get_operation_summary(self, operation_name: str) -> Dict:
        """Get performance summary for a specific operation"""
        if operation_name not in self.operation_metrics:
            return {}
        
        return self.operation_metrics[operation_name].get('summary', {})
    
    def print_all_summaries(self):
        """Print performance summaries for all tracked operations"""
        print("\n" + "=" * 80)
        print("PERFORMANCE SUMMARIES FOR ALL OPERATIONS")
        print("=" * 80)
        
        for operation_name, metrics in self.operation_metrics.items():
            print(f"\n{operation_name.upper()}:")
            summary = metrics.get('summary', {})
            
            if summary:
                print(f"  Duration: {summary.get('monitoring_duration_seconds', 0):.2f} seconds")
                print(f"  Samples: {summary.get('total_samples', 0)}")
                
                cpu = summary.get('cpu', {})
                print(f"  CPU Usage: Avg {cpu.get('avg_percent', 0)}%, Max {cpu.get('max_percent', 0)}%")
                
                memory = summary.get('memory', {})
                print(f"  Memory Usage: Avg {memory.get('avg_percent', 0)}%, Max {memory.get('max_percent', 0)}%")
                
                process_memory = summary.get('process_memory', {})
                print(f"  Process Memory: Avg {process_memory.get('avg_mb', 0)}MB, Max {process_memory.get('max_mb', 0)}MB")
            else:
                print("  No performance data available")
        
        print("=" * 80)

def main():
    """Main function to demonstrate performance monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor system performance during migration')
    parser.add_argument('--monitor', action='store_true', help='Start continuous monitoring')
    parser.add_argument('--status', action='store_true', help='Show current system status')
    parser.add_argument('--interval', type=float, default=2.0, help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(args.interval)
    
    if args.status:
        monitor.print_current_status()
    
    elif args.monitor:
        try:
            print("Starting performance monitoring... Press Ctrl+C to stop")
            monitor.start_monitoring()
            
            while True:
                time.sleep(5)
                monitor.print_current_status()
                
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
            monitor.stop_monitoring()
            
            # Print summary
            summary = monitor.get_summary_stats()
            if summary:
                print("\nMonitoring Summary:")
                print(f"Total samples: {summary['total_samples']}")
                print(f"Duration: {summary['monitoring_duration_seconds']:.2f} seconds")
                print(f"Avg CPU: {summary['cpu']['avg_percent']}%")
                print(f"Avg Memory: {summary['memory']['avg_percent']}%")
            
            # Save metrics
            filename = f"performance_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            monitor.save_metrics_to_file(filename, 'json')
            print(f"Metrics saved to: {filename}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
