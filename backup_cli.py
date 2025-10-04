#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Backup CLI Tool
===========================

Command-line tool for backup and restore operations.
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core_framework.backup_manager import BackupManager, BackupScheduler
from core_framework.config import Config

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Ocean ERP Backup CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--name', '-n', required=True, help='Backup name')
    backup_parser.add_argument('--description', '-d', help='Backup description')
    backup_parser.add_argument('--type', '-t', choices=['full', 'incremental', 'differential', 'manual'], 
                              default='full', help='Backup type')
    backup_parser.add_argument('--database', help='Database name (default: from config)')
    backup_parser.add_argument('--no-compression', action='store_true', help='Disable compression')
    backup_parser.add_argument('--no-data', action='store_true', help='Exclude data')
    backup_parser.add_argument('--no-schema', action='store_true', help='Exclude schema')
    backup_parser.add_argument('--no-indexes', action='store_true', help='Exclude indexes')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument('--backup', '-b', required=True, help='Backup file path')
    restore_parser.add_argument('--database', '-d', help='Target database name')
    restore_parser.add_argument('--clean', action='store_true', help='Clean database before restore')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available backups')
    list_parser.add_argument('--format', '-f', choices=['table', 'json'], default='table', 
                            help='Output format')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify backup file')
    verify_parser.add_argument('--backup', '-b', required=True, help='Backup file path')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete backup file')
    delete_parser.add_argument('--backup', '-b', required=True, help='Backup file path')
    delete_parser.add_argument('--force', '-f', action='store_true', help='Force deletion')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup old backups')
    cleanup_parser.add_argument('--days', '-d', type=int, default=30, help='Retention days')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule backup')
    schedule_parser.add_argument('--name', '-n', required=True, help='Schedule name')
    schedule_parser.add_argument('--frequency', '-f', choices=['daily', 'weekly', 'monthly'], 
                                required=True, help='Backup frequency')
    schedule_parser.add_argument('--time', '-t', help='Backup time (HH:MM format)')
    schedule_parser.add_argument('--database', help='Database name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Load configuration
        config = Config()
        backup_manager = BackupManager(config)
        
        if args.command == 'backup':
            return handle_backup(backup_manager, args)
        elif args.command == 'restore':
            return handle_restore(backup_manager, args)
        elif args.command == 'list':
            return handle_list(backup_manager, args)
        elif args.command == 'verify':
            return handle_verify(backup_manager, args)
        elif args.command == 'delete':
            return handle_delete(backup_manager, args)
        elif args.command == 'cleanup':
            return handle_cleanup(backup_manager, args)
        elif args.command == 'schedule':
            return handle_schedule(config, args)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_backup(backup_manager, args):
    """Handle backup command"""
    print(f"Creating backup: {args.name}")
    
    backup_config = {
        'name': args.name,
        'description': args.description or f"CLI backup created on {datetime.now()}",
        'backup_type': args.type,
        'database_name': args.database,
        'compression_enabled': not args.no_compression,
        'include_data': not args.no_data,
        'include_schema': not args.no_schema,
        'include_indexes': not args.no_indexes,
    }
    
    result = backup_manager.create_backup(backup_config)
    
    if result['success']:
        config = result['backup_config']
        print(f"✓ Backup created successfully!")
        print(f"  File: {config['backup_file']}")
        print(f"  Path: {config['backup_path']}")
        print(f"  Size: {config['backup_size']:.2f} MB")
        print(f"  Duration: {config['duration']:.2f} minutes")
        return 0
    else:
        print(f"✗ Backup failed: {result['error']}")
        return 1

def handle_restore(backup_manager, args):
    """Handle restore command"""
    print(f"Restoring from backup: {args.backup}")
    
    restore_config = {
        'backup_path': args.backup,
        'target_database': args.database,
        'restore_options': {
            'clean': args.clean,
        }
    }
    
    result = backup_manager.restore_backup(restore_config)
    
    if result['success']:
        log = result['restore_log']
        print(f"✓ Restore completed successfully!")
        print(f"  Duration: {log['duration']:.2f} minutes")
        return 0
    else:
        print(f"✗ Restore failed: {result['error']}")
        return 1

def handle_list(backup_manager, args):
    """Handle list command"""
    backups = backup_manager.list_backups()
    
    if args.format == 'json':
        print(json.dumps(backups, indent=2, default=str))
    else:
        if not backups:
            print("No backups found.")
            return 0
        
        print(f"{'Name':<40} {'Size (MB)':<12} {'Created':<20} {'Modified':<20}")
        print("-" * 100)
        
        for backup in backups:
            print(f"{backup['name']:<40} {backup['size']:<12.2f} "
                  f"{backup['created'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
                  f"{backup['modified'].strftime('%Y-%m-%d %H:%M:%S'):<20}")
    
    return 0

def handle_verify(backup_manager, args):
    """Handle verify command"""
    print(f"Verifying backup: {args.backup}")
    
    result = backup_manager.verify_backup(args.backup)
    
    if result['success']:
        print(f"✓ Backup verification successful!")
        print(f"  Size: {result['file_size_mb']:.2f} MB")
        print(f"  Compressed: {result['compressed']}")
        return 0
    else:
        print(f"✗ Backup verification failed: {result['error']}")
        return 1

def handle_delete(backup_manager, args):
    """Handle delete command"""
    if not args.force:
        confirm = input(f"Are you sure you want to delete {args.backup}? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return 0
    
    print(f"Deleting backup: {args.backup}")
    
    if backup_manager.delete_backup(args.backup):
        print(f"✓ Backup deleted successfully!")
        return 0
    else:
        print(f"✗ Failed to delete backup.")
        return 1

def handle_cleanup(backup_manager, args):
    """Handle cleanup command"""
    print(f"Cleaning up backups older than {args.days} days...")
    
    if args.dry_run:
        print("DRY RUN - No files will be deleted")
        # TODO: Implement dry run functionality
        return 0
    
    result = backup_manager.cleanup_old_backups(args.days)
    
    if result['success']:
        print(f"✓ Cleanup completed!")
        print(f"  Deleted: {result['deleted_count']} files")
        print(f"  Freed: {result['deleted_size_mb']:.2f} MB")
        return 0
    else:
        print(f"✗ Cleanup failed: {result['error']}")
        return 1

def handle_schedule(config, args):
    """Handle schedule command"""
    print(f"Scheduling backup: {args.name}")
    
    scheduler = BackupScheduler(config)
    
    schedule_config = {
        'name': args.name,
        'frequency': args.frequency,
        'time': args.time or '02:00',
        'database': args.database,
        'created': datetime.now().isoformat(),
    }
    
    if scheduler.schedule_backup(schedule_config):
        print(f"✓ Backup scheduled successfully!")
        print(f"  Frequency: {args.frequency}")
        print(f"  Time: {args.time or '02:00'}")
        return 0
    else:
        print(f"✗ Failed to schedule backup.")
        return 1

if __name__ == '__main__':
    sys.exit(main())