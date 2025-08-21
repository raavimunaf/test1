#!/usr/bin/env python3
"""
Backup and Restore Script for PostgreSQL
Provides crash-safe backup and restore operations with section-based restoration
"""

import logging
import sys
import os
import subprocess
import argparse
from datetime import datetime
from database_connections import DatabaseConnections
from config import POSTGRES_CONFIG

logger = logging.getLogger(__name__)

class BackupRestore:
    def __init__(self):
        self.db_connections = DatabaseConnections()
        self.backup_dir = "backups"
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"Created backup directory: {self.backup_dir}")
    
    def create_backup(self, filename=None):
        """Create a PostgreSQL backup"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"backup_{timestamp}.dump"
            
            filepath = os.path.join(self.backup_dir, filename)
            
            # Build pg_dump command
            cmd = [
                'pg_dump',
                '-Fc',  # Custom format
                '-h', POSTGRES_CONFIG['host'],
                '-p', str(POSTGRES_CONFIG['port']),
                '-U', POSTGRES_CONFIG['user'],
                '-d', POSTGRES_CONFIG['dbname'],
                '-f', filepath
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = POSTGRES_CONFIG['password']
            
            logger.info(f"Creating backup: {filepath}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✓ Backup created successfully: {filepath}")
                return filepath
            else:
                logger.error(f"✗ Backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return None
    
    def restore_backup(self, backup_file, target_db=None, sections=None, crash_safe=False):
        """Restore PostgreSQL backup"""
        try:
            if not os.path.exists(backup_file):
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            if target_db is None:
                target_db = POSTGRES_CONFIG['dbname']
            
            logger.info(f"Restoring backup: {backup_file} to database: {target_db}")
            
            if crash_safe:
                return self._crash_safe_restore(backup_file, target_db, sections)
            else:
                return self._full_restore(backup_file, target_db)
                
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    def _full_restore(self, backup_file, target_db):
        """Perform full restore"""
        try:
            # Drop and recreate database
            self._recreate_database(target_db)
            
            # Restore backup
            cmd = [
                'pg_restore',
                '-h', POSTGRES_CONFIG['host'],
                '-p', str(POSTGRES_CONFIG['port']),
                '-U', POSTGRES_CONFIG['user'],
                '-d', target_db,
                '--clean',
                '--if-exists',
                backup_file
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = POSTGRES_CONFIG['password']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✓ Full restore completed successfully")
                return True
            else:
                logger.error(f"✗ Full restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Full restore failed: {e}")
            return False
    
    def _crash_safe_restore(self, backup_file, target_db, sections=None):
        """Perform crash-safe restore with sections"""
        try:
            if sections is None:
                sections = ['pre-data', 'data', 'post-data']
            
            logger.info(f"Starting crash-safe restore with sections: {sections}")
            
            # Step 1: Pre-data (schema, functions, procedures)
            if 'pre-data' in sections:
                logger.info("Restoring pre-data section...")
                if not self._restore_section(backup_file, target_db, 'pre-data'):
                    logger.error("Pre-data restore failed")
                    return False
            
            # Step 2: Data (table data)
            if 'data' in sections:
                logger.info("Restoring data section...")
                if not self._restore_section(backup_file, target_db, 'data'):
                    logger.error("Data restore failed")
                    return False
            
            # Step 3: Post-data (indexes, constraints, triggers)
            if 'post-data' in sections:
                logger.info("Restoring post-data section...")
                if not self._restore_section(backup_file, target_db, 'post-data'):
                    logger.error("Post-data restore failed")
                    return False
            
            logger.info("✓ Crash-safe restore completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Crash-safe restore failed: {e}")
            return False
    
    def _restore_section(self, backup_file, target_db, section):
        """Restore a specific section"""
        try:
            cmd = [
                'pg_restore',
                '-h', POSTGRES_CONFIG['host'],
                '-p', str(POSTGRES_CONFIG['port']),
                '-U', POSTGRES_CONFIG['user'],
                '-d', target_db,
                f'--section={section}',
                '--clean',
                '--if-exists',
                backup_file
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = POSTGRES_CONFIG['password']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✓ {section} section restored successfully")
                return True
            else:
                logger.error(f"✗ {section} section restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"{section} section restore failed: {e}")
            return False
    
    def _recreate_database(self, db_name):
        """Drop and recreate database"""
        try:
            # Connect to postgres database to drop/recreate target database
            admin_dsn = (
                f"host={POSTGRES_CONFIG['host']} "
                f"port={POSTGRES_CONFIG['port']} "
                f"dbname=postgres "
                f"user={POSTGRES_CONFIG['user']} "
                f"password={POSTGRES_CONFIG['password']}"
            )
            
            with self.db_connections.get_postgres_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    # Terminate connections to target database
                    cur.execute(f"""
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE datname = '{db_name}' AND pid <> pg_backend_pid()
                    """)
                    
                    # Drop database if exists
                    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
                    
                    # Create new database
                    cur.execute(f"CREATE DATABASE {db_name}")
                    
            logger.info(f"Database {db_name} recreated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to recreate database {db_name}: {e}")
            return False
    
    def list_backups(self):
        """List available backups"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.endswith('.dump'):
                    filepath = os.path.join(self.backup_dir, file)
                    size = os.path.getsize(filepath)
                    modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    backups.append({
                        'filename': file,
                        'size': size,
                        'modified': modified
                    })
            
            if backups:
                logger.info("Available backups:")
                for backup in sorted(backups, key=lambda x: x['modified'], reverse=True):
                    logger.info(f"  {backup['filename']} ({backup['size']} bytes, {backup['modified']})")
            else:
                logger.info("No backups found")
                
            return backups
            
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='PostgreSQL Backup and Restore Tool')
    parser.add_argument('--backup', action='store_true', help='Create a backup')
    parser.add_argument('--restore', metavar='FILE', help='Restore from backup file')
    parser.add_argument('--list', action='store_true', help='List available backups')
    parser.add_argument('--crash-safe', action='store_true', help='Use crash-safe restore')
    parser.add_argument('--sections', nargs='+', choices=['pre-data', 'data', 'post-data'],
                       help='Specify sections for crash-safe restore')
    parser.add_argument('--target-db', help='Target database for restore')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    backup_restore = BackupRestore()
    
    try:
        if args.backup:
            filename = backup_restore.create_backup()
            if filename:
                logger.info(f"Backup created: {filename}")
            else:
                logger.error("Backup failed")
                sys.exit(1)
        
        elif args.restore:
            success = backup_restore.restore_backup(
                args.restore,
                target_db=args.target_db,
                sections=args.sections,
                crash_safe=args.crash_safe
            )
            if not success:
                sys.exit(1)
        
        elif args.list:
            backup_restore.list_backups()
        
        else:
            parser.print_help()
            
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 