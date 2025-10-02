#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Configuration Manager
=========================================

Configuration management for the standalone ERP system.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration Manager for ERP System"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config_data = self._load_config()
        
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        return os.path.join(os.path.dirname(__file__), '..', 'erp.conf')
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = self._get_default_config()
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
            except Exception as e:
                logging.warning(f"Failed to load config file: {e}")
        
        return default_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            # Database Configuration
            'database': {
                'host': 'localhost',
                'port': 5432,
                'user': 'erp_user',
                'password': 'erp_password',
                'name': 'kids_clothing_erp',
                'pool_size': 20,
                'max_overflow': 30,
                'echo': False
            },
            
            # Server Configuration
            'server': {
                'host': 'localhost',
                'port': 8069,
                'workers': 4,
                'timeout': 30,
                'max_requests': 1000
            },
            
            # Addons Configuration
            'addons': {
                'path': 'addons',
                'auto_install': True,
                'update_mode': 'manual'
            },
            
            # Security Configuration
            'security': {
                'secret_key': 'your-secret-key-here',
                'session_timeout': 3600,
                'max_login_attempts': 5,
                'lockout_duration': 300
            },
            
            # Logging Configuration
            'logging': {
                'level': 'INFO',
                'file': 'erp.log',
                'max_size': 10485760,  # 10MB
                'backup_count': 5
            },
            
            # Web Interface Configuration
            'web': {
                'static_path': 'static',
                'template_path': 'templates',
                'debug': False,
                'theme': 'kids_clothing'
            },
            
            # Indian Localization
            'localization': {
                'country': 'IN',
                'currency': 'INR',
                'language': 'en_IN',
                'timezone': 'Asia/Kolkata',
                'date_format': '%d/%m/%Y',
                'time_format': '%H:%M:%S'
            },
            
            # Kids Clothing Specific
            'kids_clothing': {
                'age_groups': ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16'],
                'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
                'colors': ['Red', 'Blue', 'Green', 'Yellow', 'Pink', 'Purple', 'Orange', 'Black', 'White'],
                'brands': ['Brand A', 'Brand B', 'Brand C'],
                'seasons': ['Spring', 'Summer', 'Fall', 'Winter']
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
    
    def get_database_url(self) -> str:
        """Get database connection URL"""
        db_config = self.get('database')
        return f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    
    def get_addons_path(self) -> str:
        """Get addons directory path"""
        return os.path.abspath(self.get('addons.path', 'addons'))
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get('web.debug', False)
    
    def get_secret_key(self) -> str:
        """Get secret key for sessions"""
        return self.get('security.secret_key', 'default-secret-key')