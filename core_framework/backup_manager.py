#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Backup Manager
==========================

Comprehensive backup and restore functionality for Ocean ERP.
"""

import os
import sys
import subprocess
import shutil
import gzip
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logger = logging.getLogger(__name__)

class BackupManager:
    """Backup Manager for Ocean ERP"""
    
    def __init__(self, config):
        """Initialize backup manager"""
        self.config = config
        self.logger = logging.getLogger('OceanERP.BackupManager')
        self.backup_path = Path(config.get('backup', {}).get('path', 'backups'))
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, backup_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create database backup"""
        try:
            self.logger.info(f"Starting backup: {backup_config.get('name', 'unnamed')}")
            
            # Validate backup configuration
            if not self._validate_backup_config(backup_config):
                return {'success': False, 'error': 'Invalid backup configuration'}
            
            # Generate backup filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = backup_config.get('name', f'backup_{timestamp}')
            backup_file = f"{backup_name}_{timestamp}.sql"
            
            # Add timestamp to config
            backup_config['backup_file'] = backup_file
            backup_config['backup_path'] = str(self.backup_path / backup_file)
            backup_config['start_time'] = datetime.now()
            
            # Create backup
            result = self._execute_backup(backup_config)
            
            if result['success']:
                # Update backup info
                backup_config['end_time'] = datetime.now()
                backup_config['duration'] = (backup_config['end_time'] - backup_config['start_time']).total_seconds() / 60
                backup_config['status'] = 'completed'
                
                # Get file size
                backup_file_path = Path(backup_config['backup_path'])
                if backup_file_path.exists():
                    backup_config['backup_size'] = backup_file_path.stat().st_size / (1024 * 1024)  # MB
                
                self.logger.info(f"Backup completed successfully: {backup_file}")
                return {'success': True, 'backup_config': backup_config}
            else:
                backup_config['status'] = 'failed'
                backup_config['error_message'] = result['error']
                return {'success': False, 'error': result['error'], 'backup_config': backup_config}
                
        except Exception as e:
            self.logger.error(f"Backup creation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def restore_backup(self, backup_config: Dict[str, Any]) -> Dict[str, Any]:
        """Restore database from backup"""
        try:
            self.logger.info(f"Starting restore: {backup_config.get('name', 'unnamed')}")
            
            # Validate backup file
            backup_file_path = Path(backup_config.get('backup_path', ''))
            if not backup_file_path.exists():
                return {'success': False, 'error': 'Backup file not found'}
            
            # Validate restore configuration
            if not self._validate_restore_config(backup_config):
                return {'success': False, 'error': 'Invalid restore configuration'}
            
            # Create restore log
            restore_log = {
                'start_time': datetime.now(),
                'backup_file': backup_config['backup_path'],
                'target_database': backup_config.get('target_database'),
                'restore_options': backup_config.get('restore_options', {})
            }
            
            # Execute restore
            result = self._execute_restore(backup_config)
            
            if result['success']:
                restore_log['end_time'] = datetime.now()
                restore_log['duration'] = (restore_log['end_time'] - restore_log['start_time']).total_seconds() / 60
                restore_log['status'] = 'completed'
                
                self.logger.info(f"Restore completed successfully")
                return {'success': True, 'restore_log': restore_log}
            else:
                restore_log['status'] = 'failed'
                restore_log['error'] = result['error']
                return {'success': False, 'error': result['error'], 'restore_log': restore_log}
                
        except Exception as e:
            self.logger.error(f"Restore error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_backup_config(self, config: Dict[str, Any]) -> bool:
        """Validate backup configuration"""
        required_fields = ['database_name']
        
        for field in required_fields:
            if not config.get(field):
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def _validate_restore_config(self, config: Dict[str, Any]) -> bool:
        """Validate restore configuration"""
        required_fields = ['backup_path', 'target_database']
        
        for field in required_fields:
            if not config.get(field):
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def _execute_backup(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute actual backup using pg_dump"""
        try:
            # Get database configuration
            db_config = self.config.get('database', {})
            database_name = config.get('database_name', db_config.get('name'))
            
            # Build pg_dump command
            cmd = ['pg_dump']
            
            # Add connection parameters
            if db_config.get('host'):
                cmd.extend(['-h', db_config['host']])
            if db_config.get('port'):
                cmd.extend(['-p', str(db_config['port'])])
            if db_config.get('user'):
                cmd.extend(['-U', db_config['user']])
            
            # Add backup options
            if config.get('include_schema', True):
                cmd.append('--schema-only')
            if config.get('include_data', True):
                cmd.append('--data-only')
            if config.get('include_indexes', True):
                cmd.append('--indexes')
            
            # Add format
            cmd.extend(['-f', config['backup_path']])
            
            # Add database name
            cmd.append(database_name)
            
            # Set environment variables
            env = os.environ.copy()
            if db_config.get('password'):
                env['PGPASSWORD'] = db_config['password']
            
            # Execute backup
            self.logger.info(f"Executing backup command: {' '.join(cmd)}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                # Compress if enabled
                if config.get('compression_enabled', True):
                    self._compress_backup(config['backup_path'])
                
                return {'success': True}
            else:
                error_msg = result.stderr or 'Unknown backup error'
                self.logger.error(f"Backup failed: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except subprocess.TimeoutExpired:
            error_msg = 'Backup timed out after 1 hour'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f'Backup execution error: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def _execute_restore(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute actual restore using psql or pg_restore"""
        try:
            # Get database configuration
            db_config = self.config.get('database', {})
            target_database = config.get('target_database')
            backup_path = config['backup_path']
            
            # Check if backup is compressed
            if backup_path.endswith('.gz'):
                # Decompress first
                decompressed_path = backup_path[:-3]  # Remove .gz
                self._decompress_backup(backup_path, decompressed_path)
                backup_path = decompressed_path
            
            # Build psql command for restore
            cmd = ['psql']
            
            # Add connection parameters
            if db_config.get('host'):
                cmd.extend(['-h', db_config['host']])
            if db_config.get('port'):
                cmd.extend(['-p', str(db_config['port'])])
            if db_config.get('user'):
                cmd.extend(['-U', db_config['user']])
            
            # Add database name
            cmd.extend(['-d', target_database])
            
            # Add backup file
            cmd.extend(['-f', backup_path])
            
            # Set environment variables
            env = os.environ.copy()
            if db_config.get('password'):
                env['PGPASSWORD'] = db_config['password']
            
            # Execute restore
            self.logger.info(f"Executing restore command: {' '.join(cmd)}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                return {'success': True}
            else:
                error_msg = result.stderr or 'Unknown restore error'
                self.logger.error(f"Restore failed: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except subprocess.TimeoutExpired:
            error_msg = 'Restore timed out after 1 hour'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f'Restore execution error: {str(e)}'
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def _compress_backup(self, backup_path: str):
        """Compress backup file"""
        try:
            compressed_path = f"{backup_path}.gz"
            
            with open(backup_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original file
            os.remove(backup_path)
            
            # Update path in config
            self.logger.info(f"Backup compressed: {compressed_path}")
            
        except Exception as e:
            self.logger.error(f"Compression error: {e}")
    
    def _decompress_backup(self, compressed_path: str, output_path: str):
        """Decompress backup file"""
        try:
            with gzip.open(compressed_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            self.logger.info(f"Backup decompressed: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Decompression error: {e}")
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        try:
            backups = []
            
            for backup_file in self.backup_path.glob('*.sql*'):
                stat = backup_file.stat()
                backups.append({
                    'name': backup_file.name,
                    'path': str(backup_file),
                    'size': stat.st_size / (1024 * 1024),  # MB
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'compressed': backup_file.suffix == '.gz'
                })
            
            return sorted(backups, key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"List backups error: {e}")
            return []
    
    def delete_backup(self, backup_path: str) -> bool:
        """Delete backup file"""
        try:
            backup_file = Path(backup_path)
            if backup_file.exists():
                backup_file.unlink()
                self.logger.info(f"Backup deleted: {backup_path}")
                return True
            else:
                self.logger.warning(f"Backup file not found: {backup_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Delete backup error: {e}")
            return False
    
    def verify_backup(self, backup_path: str) -> Dict[str, Any]:
        """Verify backup file integrity"""
        try:
            backup_file = Path(backup_path)
            
            if not backup_file.exists():
                return {'success': False, 'error': 'Backup file not found'}
            
            # Check if file is readable
            if not os.access(backup_path, os.R_OK):
                return {'success': False, 'error': 'Backup file not readable'}
            
            # Check file size
            file_size = backup_file.stat().st_size
            if file_size == 0:
                return {'success': False, 'error': 'Backup file is empty'}
            
            # For compressed files, try to decompress
            if backup_path.endswith('.gz'):
                try:
                    with gzip.open(backup_path, 'rb') as f:
                        f.read(1024)  # Read first 1KB
                except Exception as e:
                    return {'success': False, 'error': f'Compressed file corrupted: {e}'}
            
            return {
                'success': True,
                'file_size': file_size,
                'file_size_mb': file_size / (1024 * 1024),
                'readable': True,
                'compressed': backup_path.endswith('.gz')
            }
            
        except Exception as e:
            self.logger.error(f"Verify backup error: {e}")
            return {'success': False, 'error': str(e)}
    
    def cleanup_old_backups(self, retention_days: int = 30) -> Dict[str, Any]:
        """Cleanup old backup files"""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            deleted_count = 0
            deleted_size = 0
            
            for backup_file in self.backup_path.glob('*.sql*'):
                file_time = datetime.fromtimestamp(backup_file.stat().st_ctime)
                
                if file_time < cutoff_date:
                    file_size = backup_file.stat().st_size
                    backup_file.unlink()
                    deleted_count += 1
                    deleted_size += file_size
                    self.logger.info(f"Deleted old backup: {backup_file.name}")
            
            return {
                'success': True,
                'deleted_count': deleted_count,
                'deleted_size_mb': deleted_size / (1024 * 1024),
                'retention_days': retention_days
            }
            
        except Exception as e:
            self.logger.error(f"Cleanup backups error: {e}")
            return {'success': False, 'error': str(e)}


class BackupScheduler:
    """Backup Scheduler for Ocean ERP"""
    
    def __init__(self, config):
        """Initialize backup scheduler"""
        self.config = config
        self.logger = logging.getLogger('OceanERP.BackupScheduler')
        self.backup_manager = BackupManager(config)
        
    def schedule_backup(self, schedule_config: Dict[str, Any]) -> bool:
        """Schedule a backup"""
        try:
            # This would integrate with system cron or Windows Task Scheduler
            # For now, we'll create a simple scheduling mechanism
            
            schedule_file = Path('backup_schedules.json')
            schedules = []
            
            if schedule_file.exists():
                with open(schedule_file, 'r') as f:
                    schedules = json.load(f)
            
            schedules.append(schedule_config)
            
            with open(schedule_file, 'w') as f:
                json.dump(schedules, f, indent=2, default=str)
            
            self.logger.info(f"Backup scheduled: {schedule_config.get('name')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Schedule backup error: {e}")
            return False
    
    def run_scheduled_backups(self):
        """Run scheduled backups"""
        try:
            schedule_file = Path('backup_schedules.json')
            
            if not schedule_file.exists():
                return
            
            with open(schedule_file, 'r') as f:
                schedules = json.load(f)
            
            for schedule in schedules:
                if self._should_run_backup(schedule):
                    self.logger.info(f"Running scheduled backup: {schedule.get('name')}")
                    
                    result = self.backup_manager.create_backup(schedule)
                    
                    if result['success']:
                        self.logger.info(f"Scheduled backup completed: {schedule.get('name')}")
                    else:
                        self.logger.error(f"Scheduled backup failed: {schedule.get('name')} - {result.get('error')}")
            
        except Exception as e:
            self.logger.error(f"Run scheduled backups error: {e}")
    
    def _should_run_backup(self, schedule: Dict[str, Any]) -> bool:
        """Check if backup should run based on schedule"""
        try:
            frequency = schedule.get('frequency', 'daily')
            last_run = schedule.get('last_run')
            
            if not last_run:
                return True
            
            last_run_date = datetime.fromisoformat(last_run)
            now = datetime.now()
            
            if frequency == 'daily':
                return (now - last_run_date).days >= 1
            elif frequency == 'weekly':
                return (now - last_run_date).days >= 7
            elif frequency == 'monthly':
                return (now - last_run_date).days >= 30
            
            return False
            
        except Exception as e:
            self.logger.error(f"Check schedule error: {e}")
            return False