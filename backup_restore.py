#!/usr/bin/env python3
"""
Backup and Restore Module for PostgreSQL
Provides crash-safe restore capabilities with section-based restoration.
"""

import os
import subprocess
import logging
import tempfile
from datetime import datetime
from config import POSTGRES_CONFIG

logger = logging.getLogger(__name__)

class BackupRestore:
    def __init__(self):
        self.pg_host = POSTGRES_CONFIG['host']
        self.pg_port = POSTGRES_CONFIG['port']
        self.pg_user = POSTGRES_CONFIG['user']
        self.pg_password = POSTGRES_CONFIG['password']
        self.pg_db = POSTGRES_CONFIG['dbname']
    
    def _get_pg_env(self):
        """Get PostgreSQL environment variables"""
        env = os.environ.copy()
        env['PGPASSWORD'] = self.pg_password
        return env
    
    def create_backup(self, output_file=None, format='custom'):
        """
        Create a PostgreSQL backup
        
        Args:
            output_file: Output file path (optional)
            format: Backup format ('custom', 'plain', 'directory')
        
        Returns:
            str: Path to backup file
        """
        try:
            if output_file is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"backup_{self.pg_db}_{timestamp}.dump"
            
            # Build pg_dump command
            cmd = [
                'pg_dump',
                f'--host={self.pg_host}',
                f'--port={self.pg_port}',
                f'--username={self.pg_user}',
                f'--dbname={self.pg_db}',
                f'--format={format}',
                f'--file={output_file}',
                '--verbose'
            ]
            
            logger.info(f"Creating backup: {output_file}")
            logger.info(f"Command: {' '.join(cmd)}")
            
            # Execute backup
            result = subprocess.run(
                cmd,
                env=self._get_pg_env(),
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info("✓ Backup created successfully")
            logger.info(f"Backup file: {output_file}")
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
    
    def restore_backup(self, backup_file, target_db=None, sections=None):
        """
        Restore PostgreSQL backup with optional section-based restoration
        
        Args:
            backup_file: Path to backup file
            target_db: Target database name (optional)
            sections: List of sections to restore (optional)
        
        Returns:
            bool: True if successful
        """
        try:
            if target_db is None:
                target_db = self.pg_db
            
            if sections is None:
                # Full restore
                return self._restore_full(backup_file, target_db)
            else:
                # Section-based restore
                return self._restore_sections(backup_file, target_db, sections)
                
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
    
    def _restore_full(self, backup_file, target_db):
        """Perform full restore"""
        try:
            cmd = [
                'pg_restore',
                f'--host={self.pg_host}',
                f'--port={self.pg_port}',
                f'--username={self.pg_user}',
                f'--dbname={target_db}',
                '--verbose',
                '--clean',
                '--if-exists',
                backup_file
            ]
            
            logger.info(f"Performing full restore to database: {target_db}")
            logger.info(f"Command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                env=self._get_pg_env(),
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info("✓ Full restore completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Full restore failed: {e}")
            logger.error(f"stderr: {e.stderr}")
            raise
    
    def _restore_sections(self, backup_file, target_db, sections):
        """Perform section-based restore"""
        try:
            logger.info(f"Performing section-based restore to database: {target_db}")
            logger.info(f"Sections: {', '.join(sections)}")
            
            success_sections = []
            failed_sections = []
            
            for section in sections:
                try:
                    if self._restore_section(backup_file, target_db, section):
                        success_sections.append(section)
                        logger.info(f"✓ Section '{section}' restored successfully")
                    else:
                        failed_sections.append(section)
                        logger.error(f"✗ Section '{section}' restore failed")
                except Exception as e:
                    failed_sections.append(section)
                    logger.error(f"✗ Section '{section}' restore failed: {e}")
            
            # Summary
            logger.info(f"Section restore completed:")
            logger.info(f"  Successful: {', '.join(success_sections)}")
            if failed_sections:
                logger.error(f"  Failed: {', '.join(failed_sections)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Section-based restore failed: {e}")
            raise
    
    def _restore_section(self, backup_file, target_db, section):
        """Restore a specific section"""
        try:
            cmd = [
                'pg_restore',
                f'--host={self.pg_host}',
                f'--port={self.pg_port}',
                f'--username={self.pg_user}',
                f'--dbname={target_db}',
                f'--section={section}',
                '--verbose',
                backup_file
            ]
            
            result = subprocess.run(
                cmd,
                env=self._get_pg_env(),
                capture_output=True,
                text=True,
                check=True
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Section '{section}' restore failed: {e}")
            return False
    
    def get_backup_contents(self, backup_file):
        """Get list of contents in backup file"""
        try:
            cmd = [
                'pg_restore',
                '--list',
                backup_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.splitlines()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list backup contents: {e}")
            return []
    
    def create_toc_file(self, backup_file, toc_file=None):
        """Create a table of contents file for the backup"""
        try:
            if toc_file is None:
                toc_file = backup_file.replace('.dump', '.toc')
            
            cmd = [
                'pg_restore',
                '--list',
                f'--file={toc_file}',
                backup_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"✓ TOC file created: {toc_file}")
            return toc_file
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create TOC file: {e}")
            return None
    
    def restore_with_toc(self, backup_file, toc_file, target_db):
        """Restore using a TOC file for selective restoration"""
        try:
            cmd = [
                'pg_restore',
                f'--host={self.pg_host}',
                f'--port={self.pg_port}',
                f'--username={self.pg_user}',
                f'--dbname={target_db}',
                f'--use-list={toc_file}',
                '--verbose',
                backup_file
            ]
            
            logger.info(f"Restoring with TOC file: {toc_file}")
            
            result = subprocess.run(
                cmd,
                env=self._get_pg_env(),
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info("✓ TOC-based restore completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"TOC-based restore failed: {e}")
            return False
    
    def crash_safe_restore(self, backup_file, target_db):
        """
        Perform crash-safe restore with section-based approach
        
        This method implements the crash-safe restore strategy:
        1. Restore pre-data (schema, functions, etc.)
        2. Restore data
        3. Restore post-data (indexes, constraints, etc.)
        
        If any step fails, you can resume from that point.
        """
        try:
            logger.info("Starting crash-safe restore process...")
            
            # Step 1: Pre-data (schema, functions, etc.)
            logger.info("Step 1: Restoring pre-data section...")
            if not self._restore_section(backup_file, target_db, 'pre-data'):
                logger.error("Pre-data restore failed")
                return False
            
            # Step 2: Data
            logger.info("Step 2: Restoring data section...")
            if not self._restore_section(backup_file, target_db, 'data'):
                logger.error("Data restore failed")
                logger.info("You can resume from this point by running:")
                logger.info(f"  python backup_restore.py --resume-data {backup_file} {target_db}")
                return False
            
            # Step 3: Post-data (indexes, constraints, etc.)
            logger.info("Step 3: Restoring post-data section...")
            if not self._restore_section(backup_file, target_db, 'post-data'):
                logger.error("Post-data restore failed")
                logger.info("You can resume from this point by running:")
                logger.info(f"  python backup_restore.py --resume-post-data {backup_file} {target_db}")
                return False
            
            logger.info("✓ Crash-safe restore completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Crash-safe restore failed: {e}")
            return False
    
    def resume_data_restore(self, backup_file, target_db):
        """Resume data restoration if it failed during crash-safe restore"""
        return self._restore_section(backup_file, target_db, 'data')
    
    def resume_post_data_restore(self, backup_file, target_db):
        """Resume post-data restoration if it failed during crash-safe restore"""
        return self._restore_section(backup_file, target_db, 'post-data')

def main():
    """Command-line interface for backup and restore operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PostgreSQL Backup and Restore Tool')
    parser.add_argument('--backup', action='store_true', help='Create backup')
    parser.add_argument('--restore', help='Restore from backup file')
    parser.add_argument('--target-db', help='Target database for restore')
    parser.add_argument('--crash-safe', action='store_true', help='Perform crash-safe restore')
    parser.add_argument('--resume-data', action='store_true', help='Resume data restoration')
    parser.add_argument('--resume-post-data', action='store_true', help='Resume post-data restoration')
    parser.add_argument('--sections', nargs='+', help='Specific sections to restore')
    
    args = parser.parse_args()
    
    backup_restore = BackupRestore()
    
    try:
        if args.backup:
            backup_file = backup_restore.create_backup()
            print(f"Backup created: {backup_file}")
            
        elif args.restore:
            if args.crash_safe:
                success = backup_restore.crash_safe_restore(args.restore, args.target_db or backup_restore.pg_db)
            elif args.resume_data:
                success = backup_restore.resume_data_restore(args.restore, args.target_db or backup_restore.pg_db)
            elif args.resume_post_data:
                success = backup_restore.resume_post_data_restore(args.restore, args.target_db or backup_restore.pg_db)
            elif args.sections:
                success = backup_restore.restore_backup(args.restore, args.target_db, args.sections)
            else:
                success = backup_restore.restore_backup(args.restore, args.target_db)
            
            if success:
                print("Restore completed successfully")
            else:
                print("Restore failed")
                sys.exit(1)
                
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 