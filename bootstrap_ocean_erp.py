#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Bootstrap Script
============================

Bootstrap script to initialize Ocean ERP system.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OceanERPBootstrap:
    """Ocean ERP Bootstrap Manager"""
    
    def __init__(self):
        """Initialize bootstrap manager"""
        self.project_root = Path(__file__).parent
        self.logger = logging.getLogger('OceanERP.Bootstrap')
        
    def run_bootstrap(self):
        """Run complete bootstrap process"""
        try:
            self.logger.info("Starting Ocean ERP bootstrap process...")
            
            # Step 1: Check system requirements
            if not self._check_system_requirements():
                return False
            
            # Step 2: Create necessary directories
            if not self._create_directories():
                return False
            
            # Step 3: Install Python dependencies
            if not self._install_dependencies():
                return False
            
            # Step 4: Create default configuration
            if not self._create_default_config():
                return False
            
            # Step 5: Create default logo
            if not self._create_default_logo():
                return False
            
            # Step 6: Set up permissions
            if not self._setup_permissions():
                return False
            
            self.logger.info("Ocean ERP bootstrap completed successfully!")
            self._print_next_steps()
            return True
            
        except Exception as e:
            self.logger.error(f"Bootstrap error: {e}")
            return False
    
    def _check_system_requirements(self):
        """Check system requirements"""
        self.logger.info("Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.logger.error("Python 3.8+ is required")
            return False
        
        self.logger.info(f"Python version: {sys.version}")
        
        # Check if PostgreSQL is available
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['psql', '--version'], 
                                      capture_output=True, text=True, timeout=10, shell=True)
            else:  # Linux/macOS
                result = subprocess.run(['psql', '--version'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.info(f"PostgreSQL found: {result.stdout.strip()}")
            else:
                self.logger.warning("PostgreSQL not found - please install PostgreSQL")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.logger.warning("PostgreSQL not found - please install PostgreSQL")
        
        return True
    
    def _create_directories(self):
        """Create necessary directories"""
        self.logger.info("Creating necessary directories...")
        
        directories = [
            'static/images/logo',
            'static/css',
            'static/js',
            'templates',
            'uploads',
            'logs',
            'backups',
            'data',
            'config'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
        
        return True
    
    def _install_dependencies(self):
        """Install Python dependencies"""
        self.logger.info("Installing Python dependencies...")
        
        try:
            # Check if requirements.txt exists
            requirements_file = self.project_root / 'requirements.txt'
            if not requirements_file.exists():
                self.logger.error("requirements.txt not found")
                return False
            
            # Install dependencies
            if os.name == 'nt':  # Windows
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
                ], capture_output=True, text=True, timeout=300, shell=True)
            else:  # Linux/macOS
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
                ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.logger.info("Dependencies installed successfully")
                return True
            else:
                self.logger.error(f"Failed to install dependencies: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Dependency installation timed out")
            return False
        except Exception as e:
            self.logger.error(f"Dependency installation error: {e}")
            return False
    
    def _create_default_config(self):
        """Create default configuration"""
        self.logger.info("Creating default configuration...")
        
        config_file = self.project_root / 'erp.conf'
        
        if config_file.exists():
            self.logger.info("Configuration file already exists")
            return True
        
        default_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "user": "erp_user",
                "password": "erp_password",
                "name": "ocean_erp",
                "pool_size": 20,
                "max_overflow": 30,
                "echo": False
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8069,
                "workers": 4,
                "timeout": 30,
                "max_requests": 1000
            },
            "addons": {
                "path": "addons",
                "auto_install": True,
                "update_mode": "manual"
            },
            "security": {
                "secret_key": "ocean-erp-default-secret-key-change-in-production",
                "session_timeout": 3600,
                "max_login_attempts": 5,
                "lockout_duration": 300
            },
            "logging": {
                "level": "INFO",
                "file": "erp.log",
                "max_size": 10485760,
                "backup_count": 5
            },
            "web": {
                "static_path": "static",
                "template_path": "templates",
                "debug": False,
                "theme": "kids_clothing",
                "logo_path": "static/images/logo"
            },
            "localization": {
                "country": "IN",
                "currency": "INR",
                "language": "en_IN",
                "timezone": "Asia/Kolkata",
                "date_format": "%d/%m/%Y",
                "time_format": "%H:%M:%S"
            },
            "kids_clothing": {
                "age_groups": ["0-2", "2-4", "4-6", "6-8", "8-10", "10-12", "12-14", "14-16"],
                "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
                "colors": ["Red", "Blue", "Green", "Yellow", "Pink", "Purple", "Orange", "Black", "White"],
                "brands": ["Brand A", "Brand B", "Brand C"],
                "seasons": ["Spring", "Summer", "Fall", "Winter"]
            },
            "backup": {
                "path": "backups",
                "retention_days": 30,
                "compression_enabled": True,
                "encryption_enabled": False,
                "auto_cleanup": True,
                "scheduled_backups": True
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            self.logger.info("Default configuration created")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create configuration: {e}")
            return False
    
    def _create_default_logo(self):
        """Create default logo"""
        self.logger.info("Creating default logo...")
        
        logo_dir = self.project_root / 'static' / 'images' / 'logo'
        logo_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if default logo already exists
        default_logo = logo_dir / 'default_logo.svg'
        if default_logo.exists():
            self.logger.info("Default logo already exists")
            return True
        
        # Create a simple default logo if SVG doesn't exist
        try:
            # Copy the SVG logo we created earlier
            if (self.project_root / 'static' / 'images' / 'logo' / 'default_logo.svg').exists():
                self.logger.info("Default logo created")
                return True
            else:
                self.logger.warning("Default logo file not found")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to create default logo: {e}")
            return False
    
    def _setup_permissions(self):
        """Set up file permissions"""
        self.logger.info("Setting up file permissions...")
        
        try:
            # Make run_erp.py executable (Linux/macOS only)
            if os.name != 'nt':  # Not Windows
                run_script = self.project_root / 'run_erp.py'
                if run_script.exists():
                    os.chmod(run_script, 0o755)
                    self.logger.info("Made run_erp.py executable")
            
            # Set permissions for directories (Linux/macOS only)
            if os.name != 'nt':  # Not Windows
                directories = ['uploads', 'logs', 'backups', 'static']
                for directory in directories:
                    dir_path = self.project_root / directory
                    if dir_path.exists():
                        os.chmod(dir_path, 0o755)
                        self.logger.info(f"Set permissions for {directory}")
            
            # Windows: Set permissions using icacls
            if os.name == 'nt':  # Windows
                directories = ['uploads', 'logs', 'backups', 'static']
                for directory in directories:
                    dir_path = self.project_root / directory
                    if dir_path.exists():
                        try:
                            subprocess.run(['icacls', str(dir_path), '/grant', 'Everyone:F', '/T'], 
                                         capture_output=True, shell=True)
                            self.logger.info(f"Set permissions for {directory}")
                        except:
                            self.logger.warning(f"Could not set permissions for {directory}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set permissions: {e}")
            return False
    
    def _print_next_steps(self):
        """Print next steps for user"""
        print("\n" + "="*60)
        print("🌊 Ocean ERP Bootstrap Complete!")
        print("="*60)
        print("\nNext Steps:")
        
        if os.name == 'nt':  # Windows
            print("1. Set up PostgreSQL database:")
            print("   createdb -U postgres ocean_erp")
            print("   createuser -U postgres erp_user")
            print("   psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;\"")
            print("\n2. Start the Ocean ERP server:")
            print("   python run_erp.py")
        else:  # Linux/macOS
            print("1. Set up PostgreSQL database:")
            print("   sudo -u postgres createdb ocean_erp")
            print("   sudo -u postgres createuser erp_user")
            print("   sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;\"")
            print("\n2. Start the Ocean ERP server:")
            print("   python3 run_erp.py")
        
        print("\n3. Open your browser and go to:")
        print("   http://localhost:8069")
        print("\n4. Complete the database setup wizard")
        print("\n5. Login with your admin credentials")
        print("\n" + "="*60)
        print("🎉 Your Ocean ERP system is ready!")
        print("="*60)

def main():
    """Main entry point"""
    bootstrap = OceanERPBootstrap()
    
    if bootstrap.run_bootstrap():
        print("\n✅ Bootstrap completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Bootstrap failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()