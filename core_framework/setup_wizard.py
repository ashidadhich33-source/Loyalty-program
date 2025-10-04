#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Database Setup Wizard
================================

Database setup wizard similar to Odoo's database creation wizard.
"""

import os
import sys
import json
import hashlib
import secrets
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseSetupWizard:
    """Database Setup Wizard for Ocean ERP"""
    
    def __init__(self, config_path: str = None):
        """Initialize setup wizard"""
        self.config_path = config_path or 'erp.conf'
        self.setup_data = {}
        self.logger = logging.getLogger('OceanERP.SetupWizard')
        
    def run_setup(self, setup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete database setup"""
        try:
            self.logger.info("Starting Ocean ERP database setup...")
            self.setup_data = setup_data
            
            # Step 1: Validate setup data
            if not self._validate_setup_data():
                return {'success': False, 'error': 'Invalid setup data'}
            
            # Step 2: Create database
            if not self._create_database():
                return {'success': False, 'error': 'Failed to create database'}
            
            # Step 3: Update configuration
            if not self._update_configuration():
                return {'success': False, 'error': 'Failed to update configuration'}
            
            # Step 4: Create database tables
            if not self._create_database_tables():
                return {'success': False, 'error': 'Failed to create database tables'}
            
            # Step 5: Create admin user
            if not self._create_admin_user():
                return {'success': False, 'error': 'Failed to create admin user'}
            
            # Step 6: Create default company
            if not self._create_default_company():
                return {'success': False, 'error': 'Failed to create default company'}
            
            # Step 7: Load master data
            if not self._load_master_data():
                return {'success': False, 'error': 'Failed to load master data'}
            
            # Step 8: Initialize system settings
            if not self._initialize_system_settings():
                return {'success': False, 'error': 'Failed to initialize system settings'}
            
            # Step 9: Create setup completion marker
            self._create_setup_completion_marker()
            
            self.logger.info("Ocean ERP database setup completed successfully!")
            return {
                'success': True,
                'message': 'Database setup completed successfully',
                'admin_user': self.setup_data.get('admin_user'),
                'company_name': self.setup_data.get('company_name'),
                'database_name': self.setup_data.get('database_name')
            }
            
        except Exception as e:
            self.logger.error(f"Setup wizard error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_setup_data(self) -> bool:
        """Validate setup data"""
        required_fields = ['database_name', 'admin_user', 'admin_password', 'company_name']
        
        for field in required_fields:
            if not self.setup_data.get(field):
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate password strength
        password = self.setup_data.get('admin_password', '')
        if len(password) < 8:
            self.logger.error("Password must be at least 8 characters long")
            return False
        
        return True
    
    def _create_database(self) -> bool:
        """Create PostgreSQL database"""
        try:
            db_name = self.setup_data.get('database_name')
            
            # Connect to PostgreSQL server
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='postgres',  # Default PostgreSQL password
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if cursor.fetchone():
                self.logger.warning(f"Database {db_name} already exists")
            else:
                # Create database
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                self.logger.info(f"Created database: {db_name}")
            
            # Create user if specified
            db_user = self.setup_data.get('database_user', 'erp_user')
            db_password = self.setup_data.get('database_password', 'erp_password')
            
            try:
                cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
                self.logger.info(f"Created user: {db_user}")
            except psycopg2.errors.DuplicateObject:
                self.logger.warning(f"User {db_user} already exists")
            
            # Grant privileges
            cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO {db_user}')
            cursor.execute(f'ALTER USER {db_user} CREATEDB')
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Database creation error: {e}")
            return False
    
    def _update_configuration(self) -> bool:
        """Update configuration file with new database settings"""
        try:
            # Load current config
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Update database configuration
            config['database'] = {
                'host': 'localhost',
                'port': 5432,
                'user': self.setup_data.get('database_user', 'erp_user'),
                'password': self.setup_data.get('database_password', 'erp_password'),
                'name': self.setup_data.get('database_name'),
                'pool_size': 20,
                'max_overflow': 30,
                'echo': False
            }
            
            # Update security configuration
            config['security'] = {
                'secret_key': secrets.token_urlsafe(32),
                'session_timeout': 3600,
                'max_login_attempts': 5,
                'lockout_duration': 300
            }
            
            # Save updated config
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.logger.info("Configuration updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration update error: {e}")
            return False
    
    def _create_database_tables(self) -> bool:
        """Create database tables for all models"""
        try:
            from core_framework.database import DatabaseManager
            from core_framework.config import Config
            from core_framework.orm import ORMManager
            
            # Initialize database manager with new config
            config = Config(self.config_path)
            db_manager = DatabaseManager(config)
            
            if not db_manager.initialize():
                return False
            
            # Initialize ORM manager
            orm_manager = ORMManager(config)
            if not orm_manager.initialize():
                return False
            
            # Load addons to register models
            from core_framework.addon_manager import AddonManager
            addon_manager = AddonManager(config)
            addon_manager.load_addons()
            
            # Create tables for all registered models
            orm_manager.create_tables()
            
            self.logger.info("Database tables created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Table creation error: {e}")
            return False
    
    def _create_admin_user(self) -> bool:
        """Create admin user"""
        try:
            from core_framework.database import DatabaseManager
            from core_framework.config import Config
            
            config = Config(self.config_path)
            db_manager = DatabaseManager(config)
            db_manager.initialize()
            
            # Hash password
            password_hash = self._hash_password(self.setup_data.get('admin_password'))
            
            # Create admin user
            admin_data = {
                'name': self.setup_data.get('admin_name', 'Administrator'),
                'login': self.setup_data.get('admin_user'),
                'email': self.setup_data.get('admin_email', 'admin@example.com'),
                'password': password_hash,
                'active': True,
                'is_active_user': True,
                'theme_preference': 'kids',
                'language_preference': 'en_US',
                'timezone_preference': 'Asia/Kolkata',
                'enable_notifications': True,
                'enable_sound': True,
                'enable_animations': True,
                'touchscreen_mode': False,
                'compact_mode': False,
                'login_count': 0,
                'failed_login_count': 0,
                'account_locked': False,
                'create_date': datetime.now(),
                'write_date': datetime.now(),
                'create_uid': 1,
                'write_uid': 1
            }
            
            user_id = db_manager.insert_record('res_users', admin_data)
            
            self.logger.info(f"Created admin user: {self.setup_data.get('admin_user')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Admin user creation error: {e}")
            return False
    
    def _create_default_company(self) -> bool:
        """Create default company"""
        try:
            from core_framework.database import DatabaseManager
            from core_framework.config import Config
            
            config = Config(self.config_path)
            db_manager = DatabaseManager(config)
            db_manager.initialize()
            
            # Create default company
            company_data = {
                'name': self.setup_data.get('company_name'),
                'email': self.setup_data.get('company_email', ''),
                'phone': self.setup_data.get('company_phone', ''),
                'website': self.setup_data.get('company_website', ''),
                'street': self.setup_data.get('company_street', ''),
                'city': self.setup_data.get('company_city', ''),
                'state_id': None,
                'zip': self.setup_data.get('company_zip', ''),
                'country_id': 1,  # Default to India
                'currency_id': 1,  # Default to INR
                'is_default': True,
                'active': True,
                'create_date': datetime.now(),
                'write_date': datetime.now(),
                'create_uid': 1,
                'write_uid': 1
            }
            
            company_id = db_manager.insert_record('res_company', company_data)
            
            self.logger.info(f"Created default company: {self.setup_data.get('company_name')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Company creation error: {e}")
            return False
    
    def _load_master_data(self) -> bool:
        """Load master data (age groups, seasons, etc.)"""
        try:
            from core_framework.database import DatabaseManager
            from core_framework.config import Config
            
            config = Config(self.config_path)
            db_manager = DatabaseManager(config)
            db_manager.initialize()
            
            # Load age groups
            age_groups = [
                {'name': 'Newborn', 'code': 'newborn', 'min_age': 0, 'max_age': 6, 'description': 'Newborn babies (0-6 months)'},
                {'name': 'Infant', 'code': 'infant', 'min_age': 6, 'max_age': 12, 'description': 'Infants (6-12 months)'},
                {'name': 'Toddler', 'code': 'toddler', 'min_age': 12, 'max_age': 36, 'description': 'Toddlers (1-3 years)'},
                {'name': 'Preschool', 'code': 'preschool', 'min_age': 36, 'max_age': 60, 'description': 'Preschool children (3-5 years)'},
                {'name': 'School Age', 'code': 'school', 'min_age': 60, 'max_age': 144, 'description': 'School age children (5-12 years)'},
                {'name': 'Teen', 'code': 'teen', 'min_age': 144, 'max_age': 216, 'description': 'Teenagers (12-18 years)'}
            ]
            
            for age_group in age_groups:
                age_group.update({
                    'active': True,
                    'create_date': datetime.now(),
                    'write_date': datetime.now(),
                    'create_uid': 1,
                    'write_uid': 1
                })
                db_manager.insert_record('age_group', age_group)
            
            # Load seasons
            seasons = [
                {'name': 'Summer', 'code': 'summer', 'description': 'Summer season clothing'},
                {'name': 'Winter', 'code': 'winter', 'description': 'Winter season clothing'},
                {'name': 'Monsoon', 'code': 'monsoon', 'description': 'Monsoon season clothing'},
                {'name': 'All Season', 'code': 'all_season', 'description': 'All season clothing'}
            ]
            
            for season in seasons:
                season.update({
                    'active': True,
                    'create_date': datetime.now(),
                    'write_date': datetime.now(),
                    'create_uid': 1,
                    'write_uid': 1
                })
                db_manager.insert_record('season', season)
            
            # Load genders
            genders = [
                {'name': 'Unisex', 'code': 'unisex', 'description': 'Unisex clothing'},
                {'name': 'Boys', 'code': 'boys', 'description': 'Boys clothing'},
                {'name': 'Girls', 'code': 'girls', 'description': 'Girls clothing'}
            ]
            
            for gender in genders:
                gender.update({
                    'active': True,
                    'create_date': datetime.now(),
                    'write_date': datetime.now(),
                    'create_uid': 1,
                    'write_uid': 1
                })
                db_manager.insert_record('gender', gender)
            
            self.logger.info("Master data loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Master data loading error: {e}")
            return False
    
    def _initialize_system_settings(self) -> bool:
        """Initialize system settings"""
        try:
            from core_framework.database import DatabaseManager
            from core_framework.config import Config
            
            config = Config(self.config_path)
            db_manager = DatabaseManager(config)
            db_manager.initialize()
            
            # System parameters
            system_params = [
                {'key': 'core_base.enable_child_profiles', 'value': 'True'},
                {'key': 'core_base.enable_age_based_discounts', 'value': 'True'},
                {'key': 'core_base.enable_loyalty_program', 'value': 'True'},
                {'key': 'core_base.enable_exchange_system', 'value': 'True'},
                {'key': 'core_base.enable_multi_location', 'value': 'True'},
                {'key': 'core_base.enable_stock_aging', 'value': 'True'},
                {'key': 'core_base.enable_touchscreen_mode', 'value': 'True'},
                {'key': 'core_base.enable_barcode_scanning', 'value': 'True'},
                {'key': 'core_base.enable_gst', 'value': 'True'},
                {'key': 'core_base.enable_e_invoice', 'value': 'True'},
                {'key': 'core_base.enable_e_way_bill', 'value': 'True'},
                {'key': 'core_base.enable_sms_notifications', 'value': 'True'},
                {'key': 'core_base.enable_email_notifications', 'value': 'True'},
                {'key': 'core_base.enable_whatsapp_notifications', 'value': 'True'}
            ]
            
            for param in system_params:
                param.update({
                    'create_date': datetime.now(),
                    'write_date': datetime.now(),
                    'create_uid': 1,
                    'write_uid': 1
                })
                db_manager.insert_record('ocean_config_parameter', param)
            
            self.logger.info("System settings initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"System settings initialization error: {e}")
            return False
    
    def _create_setup_completion_marker(self):
        """Create setup completion marker"""
        try:
            setup_marker = {
                'setup_completed': True,
                'setup_date': datetime.now().isoformat(),
                'admin_user': self.setup_data.get('admin_user'),
                'company_name': self.setup_data.get('company_name'),
                'database_name': self.setup_data.get('database_name'),
                'version': '1.0.0'
            }
            
            with open('.ocean_setup_complete', 'w') as f:
                json.dump(setup_marker, f, indent=2)
            
            self.logger.info("Setup completion marker created")
            
        except Exception as e:
            self.logger.error(f"Setup marker creation error: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using secure method"""
        salt = secrets.token_hex(16)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def is_setup_complete(self) -> bool:
        """Check if setup is complete"""
        return os.path.exists('.ocean_setup_complete')
    
    def get_setup_status(self) -> Dict[str, Any]:
        """Get setup status"""
        if self.is_setup_complete():
            try:
                with open('.ocean_setup_complete', 'r') as f:
                    return json.load(f)
            except:
                return {'setup_completed': True, 'setup_date': 'Unknown'}
        else:
            return {'setup_completed': False}


class LogoManager:
    """Logo management system"""
    
    def __init__(self, config):
        """Initialize logo manager"""
        self.config = config
        self.logo_path = config.get('web.logo_path', 'static/images/logo')
        self.logo_formats = ['png', 'jpg', 'jpeg', 'svg', 'gif']
        self.max_size = 2 * 1024 * 1024  # 2MB
        self.logger = logging.getLogger('OceanERP.LogoManager')
        
    def upload_logo(self, logo_file, logo_type='main') -> Dict[str, Any]:
        """Upload logo file"""
        try:
            # Validate file
            if not self._validate_logo_file(logo_file):
                return {'success': False, 'error': 'Invalid logo file'}
            
            # Create logo directory
            logo_dir = Path(self.logo_path)
            logo_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            file_extension = logo_file.filename.split('.')[-1].lower()
            logo_filename = f"{logo_type}_logo.{file_extension}"
            logo_filepath = logo_dir / logo_filename
            
            # Save file
            logo_file.save(str(logo_filepath))
            
            # Update logo configuration
            self._update_logo_config(logo_type, str(logo_filepath))
            
            self.logger.info(f"Logo uploaded successfully: {logo_filename}")
            return {
                'success': True,
                'message': 'Logo uploaded successfully',
                'logo_path': str(logo_filepath),
                'logo_url': f'/static/images/logo/{logo_filename}'
            }
            
        except Exception as e:
            self.logger.error(f"Logo upload error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_logo_file(self, logo_file) -> bool:
        """Validate logo file"""
        if not logo_file or not logo_file.filename:
            return False
        
        # Check file extension
        file_extension = logo_file.filename.split('.')[-1].lower()
        if file_extension not in self.logo_formats:
            return False
        
        # Check file size
        logo_file.seek(0, 2)  # Seek to end
        file_size = logo_file.tell()
        logo_file.seek(0)  # Reset to beginning
        
        if file_size > self.max_size:
            return False
        
        return True
    
    def _update_logo_config(self, logo_type, logo_path):
        """Update logo configuration"""
        try:
            # Update configuration file
            config_path = self.config.get('config_path', 'erp.conf')
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            if 'web' not in config:
                config['web'] = {}
            
            config['web'][f'{logo_type}_logo'] = logo_path
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Logo config update error: {e}")
    
    def get_logo_url(self, logo_type='main') -> str:
        """Get logo URL"""
        try:
            config_path = self.config.get('config_path', 'erp.conf')
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                logo_path = config.get('web', {}).get(f'{logo_type}_logo', '')
                if logo_path and os.path.exists(logo_path):
                    # Convert absolute path to URL
                    logo_filename = os.path.basename(logo_path)
                    return f'/static/images/logo/{logo_filename}'
            
            # Default logo
            return '/static/images/logo/default_logo.png'
            
        except Exception as e:
            self.logger.error(f"Logo URL error: {e}")
            return '/static/images/logo/default_logo.png'
    
    def delete_logo(self, logo_type='main') -> bool:
        """Delete logo"""
        try:
            config_path = self.config.get('config_path', 'erp.conf')
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                logo_path = config.get('web', {}).get(f'{logo_type}_logo', '')
                if logo_path and os.path.exists(logo_path):
                    os.remove(logo_path)
                
                # Remove from config
                if 'web' in config and f'{logo_type}_logo' in config['web']:
                    del config['web'][f'{logo_type}_logo']
                    
                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Logo deletion error: {e}")
            return False