#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Backup Service
=========================

Background service for scheduled backups and maintenance.
"""

import sys
import time
import signal
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core_framework.backup_manager import BackupManager, BackupScheduler
from core_framework.config import Config

class BackupService:
    """Backup Service for Ocean ERP"""
    
    def __init__(self):
        """Initialize backup service"""
        self.config = Config()
        self.backup_manager = BackupManager(self.config)
        self.scheduler = BackupScheduler(self.config)
        self.running = True
        self.logger = logging.getLogger('OceanERP.BackupService')
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def run(self):
        """Run backup service"""
        self.logger.info("Starting Ocean ERP Backup Service...")
        
        try:
            while self.running:
                try:
                    # Run scheduled backups
                    self.scheduler.run_scheduled_backups()
                    
                    # Cleanup old backups
                    self._cleanup_old_backups()
                    
                    # Sleep for 1 hour
                    self.logger.info("Backup service sleeping for 1 hour...")
                    time.sleep(3600)
                    
                except Exception as e:
                    self.logger.error(f"Backup service error: {e}")
                    time.sleep(300)  # Sleep for 5 minutes on error
                    
        except KeyboardInterrupt:
            self.logger.info("Backup service interrupted by user")
        finally:
            self.logger.info("Backup service stopped")
    
    def _cleanup_old_backups(self):
        """Cleanup old backups"""
        try:
            retention_days = self.config.get('backup', {}).get('retention_days', 30)
            
            if self.config.get('backup', {}).get('auto_cleanup', True):
                result = self.backup_manager.cleanup_old_backups(retention_days)
                
                if result['success'] and result['deleted_count'] > 0:
                    self.logger.info(f"Cleaned up {result['deleted_count']} old backups, "
                                   f"freed {result['deleted_size_mb']:.2f} MB")
                    
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
    
    def create_immediate_backup(self, name: str = None):
        """Create immediate backup"""
        try:
            if not name:
                name = f"service_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_config = {
                'name': name,
                'description': f"Service backup created on {datetime.now()}",
                'backup_type': 'scheduled',
                'compression_enabled': self.config.get('backup', {}).get('compression_enabled', True),
                'include_data': True,
                'include_schema': True,
                'include_indexes': True,
            }
            
            result = self.backup_manager.create_backup(backup_config)
            
            if result['success']:
                self.logger.info(f"Immediate backup created: {name}")
                return True
            else:
                self.logger.error(f"Immediate backup failed: {result['error']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Immediate backup error: {e}")
            return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ocean ERP Backup Service')
    parser.add_argument('--daemon', '-d', action='store_true', help='Run as daemon')
    parser.add_argument('--backup', '-b', help='Create immediate backup with given name')
    parser.add_argument('--log-level', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Log level')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('backup_service.log'),
            logging.StreamHandler()
        ]
    )
    
    service = BackupService()
    
    if args.backup:
        # Create immediate backup
        success = service.create_immediate_backup(args.backup)
        sys.exit(0 if success else 1)
    else:
        # Run service
        service.run()

if __name__ == '__main__':
    main()