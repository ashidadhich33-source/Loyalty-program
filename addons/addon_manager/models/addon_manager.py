# -*- coding: utf-8 -*-
"""
Ocean ERP - Addon Manager Models
===============================

Addon management models for Ocean ERP.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, SelectionField, FloatField
from typing import Dict, Any, Optional, List
import logging
import os
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AddonManager(BaseModel):
    """Addon Manager model for Ocean ERP"""
    
    _name = 'addon.manager'
    _description = 'Addon Manager'
    _table = 'addon_manager'
    
    # Basic fields
    name = CharField(
        string='Addon Name',
        size=255,
        required=True,
        help='Name of the addon'
    )
    
    technical_name = CharField(
        string='Technical Name',
        size=255,
        required=True,
        help='Technical name of the addon'
    )
    
    version = CharField(
        string='Version',
        size=50,
        default='1.0.0',
        help='Addon version'
    )
    
    summary = CharField(
        string='Summary',
        size=255,
        help='Short description of the addon'
    )
    
    description = TextField(
        string='Description',
        help='Detailed description of the addon'
    )
    
    # Addon details
    category = CharField(
        string='Category',
        size=100,
        help='Addon category'
    )
    
    author = CharField(
        string='Author',
        size=255,
        help='Addon author'
    )
    
    website = CharField(
        string='Website',
        size=255,
        help='Addon website'
    )
    
    license = CharField(
        string='License',
        size=100,
        default='LGPL-3',
        help='Addon license'
    )
    
    # Installation status
    status = SelectionField(
        string='Status',
        selection=[
            ('available', 'Available'),
            ('installed', 'Installed'),
            ('upgradeable', 'Upgradeable'),
            ('uninstalled', 'Uninstalled'),
            ('broken', 'Broken'),
        ],
        default='available',
        help='Addon installation status'
    )
    
    is_installed = BooleanField(
        string='Installed',
        default=False,
        help='Whether addon is installed'
    )
    
    is_application = BooleanField(
        string='Application',
        default=False,
        help='Whether addon is an application'
    )
    
    auto_install = BooleanField(
        string='Auto Install',
        default=False,
        help='Whether addon auto-installs'
    )
    
    # Dependencies
    depends = TextField(
        string='Dependencies',
        help='Addon dependencies (JSON format)'
    )
    
    external_dependencies = TextField(
        string='External Dependencies',
        help='External Python dependencies (JSON format)'
    )
    
    # Installation info
    install_date = DateTimeField(
        string='Install Date',
        help='Date when addon was installed'
    )
    
    update_date = DateTimeField(
        string='Update Date',
        help='Date when addon was last updated'
    )
    
    install_path = CharField(
        string='Install Path',
        size=255,
        help='Path where addon is installed'
    )
    
    # Addon metrics
    download_count = IntegerField(
        string='Download Count',
        default=0,
        help='Number of downloads'
    )
    
    rating = FloatField(
        string='Rating',
        default=0.0,
        help='Addon rating (0-5)'
    )
    
    review_count = IntegerField(
        string='Review Count',
        default=0,
        help='Number of reviews'
    )
    
    # Marketplace info
    is_marketplace = BooleanField(
        string='Marketplace',
        default=False,
        help='Whether addon is from marketplace'
    )
    
    marketplace_url = CharField(
        string='Marketplace URL',
        size=255,
        help='URL to marketplace listing'
    )
    
    price = FloatField(
        string='Price',
        default=0.0,
        help='Addon price'
    )
    
    currency = CharField(
        string='Currency',
        size=10,
        default='USD',
        help='Price currency'
    )
    
    # Development info
    is_development = BooleanField(
        string='Development',
        default=False,
        help='Whether addon is in development'
    )
    
    development_status = SelectionField(
        string='Development Status',
        selection=[
            ('planning', 'Planning'),
            ('development', 'Development'),
            ('testing', 'Testing'),
            ('stable', 'Stable'),
            ('deprecated', 'Deprecated'),
        ],
        help='Development status'
    )
    
    # Metadata
    manifest_data = TextField(
        string='Manifest Data',
        help='Full manifest data (JSON format)'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Error message if addon failed to load'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        if 'technical_name' not in vals and 'name' in vals:
            vals['technical_name'] = vals['name'].lower().replace(' ', '_')
        
        if 'install_date' not in vals and vals.get('is_installed'):
            vals['install_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle status updates"""
        result = super().write(vals)
        
        # Update install date when status changes to installed
        if 'is_installed' in vals and vals['is_installed']:
            for addon in self:
                if not addon.install_date:
                    addon.install_date = datetime.now()
        
        # Update update date when addon is updated
        if 'version' in vals or 'manifest_data' in vals:
            for addon in self:
                addon.update_date = datetime.now()
        
        return result
    
    def action_install(self):
        """Install addon"""
        self.ensure_one()
        
        try:
            # Import addon manager
            from core_framework.addon_manager import AddonManager
            from core_framework.config import Config
            
            config = Config()
            addon_manager = AddonManager(config)
            
            # Install addon
            success = addon_manager.install_addon(self.technical_name)
            
            if success:
                self.write({
                    'is_installed': True,
                    'status': 'installed',
                    'install_date': datetime.now(),
                    'error_message': None
                })
                return True
            else:
                self.write({
                    'status': 'broken',
                    'error_message': 'Installation failed'
                })
                return False
                
        except Exception as e:
            self.write({
                'status': 'broken',
                'error_message': str(e)
            })
            return False
    
    def action_uninstall(self):
        """Uninstall addon"""
        self.ensure_one()
        
        try:
            # Import addon manager
            from core_framework.addon_manager import AddonManager
            from core_framework.config import Config
            
            config = Config()
            addon_manager = AddonManager(config)
            
            # Uninstall addon
            success = addon_manager.uninstall_addon(self.technical_name)
            
            if success:
                self.write({
                    'is_installed': False,
                    'status': 'uninstalled',
                    'install_date': None,
                    'error_message': None
                })
                return True
            else:
                self.write({
                    'status': 'broken',
                    'error_message': 'Uninstallation failed'
                })
                return False
                
        except Exception as e:
            self.write({
                'status': 'broken',
                'error_message': str(e)
            })
            return False
    
    def action_update(self):
        """Update addon"""
        self.ensure_one()
        
        try:
            # Import addon manager
            from core_framework.addon_manager import AddonManager
            from core_framework.config import Config
            
            config = Config()
            addon_manager = AddonManager(config)
            
            # Update addon
            addon_manager._update_addon(self.technical_name)
            
            # Reload manifest data
            self._reload_manifest()
            
            self.write({
                'update_date': datetime.now(),
                'status': 'installed' if self.is_installed else 'available'
            })
            
            return True
            
        except Exception as e:
            self.write({
                'status': 'broken',
                'error_message': str(e)
            })
            return False
    
    def action_reload(self):
        """Reload addon manifest"""
        self.ensure_one()
        
        try:
            self._reload_manifest()
            return True
        except Exception as e:
            self.write({
                'error_message': str(e)
            })
            return False
    
    def _reload_manifest(self):
        """Reload addon manifest from file"""
        try:
            addon_path = Path(self.install_path or f"addons/{self.technical_name}")
            manifest_path = addon_path / '__manifest__.py'
            
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_content = f.read()
                
                # Execute manifest to get dictionary
                manifest_globals = {}
                exec(manifest_content, manifest_globals)
                
                # Find the manifest dictionary
                manifest_data = None
                for key, value in manifest_globals.items():
                    if isinstance(value, dict) and 'name' in value:
                        manifest_data = value
                        break
                
                if manifest_data:
                    # Update fields from manifest
                    self.write({
                        'name': manifest_data.get('name', self.name),
                        'version': manifest_data.get('version', self.version),
                        'summary': manifest_data.get('summary', self.summary),
                        'description': manifest_data.get('description', self.description),
                        'author': manifest_data.get('author', self.author),
                        'website': manifest_data.get('website', self.website),
                        'license': manifest_data.get('license', self.license),
                        'depends': json.dumps(manifest_data.get('depends', [])),
                        'external_dependencies': json.dumps(manifest_data.get('external_dependencies', [])),
                        'manifest_data': json.dumps(manifest_data),
                        'error_message': None
                    })
                    
        except Exception as e:
            self.write({
                'error_message': f'Failed to reload manifest: {str(e)}'
            })
    
    def get_dependencies(self) -> List[str]:
        """Get addon dependencies"""
        try:
            if self.depends:
                return json.loads(self.depends)
            return []
        except:
            return []
    
    def get_external_dependencies(self) -> List[str]:
        """Get external dependencies"""
        try:
            if self.external_dependencies:
                return json.loads(self.external_dependencies)
            return []
        except:
            return []
    
    def get_manifest_data(self) -> Dict[str, Any]:
        """Get full manifest data"""
        try:
            if self.manifest_data:
                return json.loads(self.manifest_data)
            return {}
        except:
            return {}
    
    @classmethod
    def scan_addons(cls):
        """Scan and register all available addons"""
        try:
            from core_framework.addon_manager import AddonManager
            from core_framework.config import Config
            
            config = Config()
            addon_manager = AddonManager(config)
            
            # Load addons
            addon_manager.load_addons()
            
            # Register addons in database
            for addon_name, addon_info in addon_manager.addons.items():
                manifest = addon_info['manifest']
                
                # Check if addon already exists
                existing = cls.search([('technical_name', '=', addon_name)])
                
                if existing:
                    # Update existing addon
                    existing.write({
                        'name': manifest.get('name', addon_name),
                        'version': manifest.get('version', '1.0.0'),
                        'summary': manifest.get('summary', ''),
                        'description': manifest.get('description', ''),
                        'author': manifest.get('author', ''),
                        'website': manifest.get('website', ''),
                        'license': manifest.get('license', 'LGPL-3'),
                        'depends': json.dumps(manifest.get('depends', [])),
                        'external_dependencies': json.dumps(manifest.get('external_dependencies', [])),
                        'manifest_data': json.dumps(manifest),
                        'install_path': addon_info['path'],
                        'is_installed': addon_info['installed'],
                        'status': 'installed' if addon_info['installed'] else 'available',
                        'error_message': None
                    })
                else:
                    # Create new addon record
                    cls.create({
                        'name': manifest.get('name', addon_name),
                        'technical_name': addon_name,
                        'version': manifest.get('version', '1.0.0'),
                        'summary': manifest.get('summary', ''),
                        'description': manifest.get('description', ''),
                        'author': manifest.get('author', ''),
                        'website': manifest.get('website', ''),
                        'license': manifest.get('license', 'LGPL-3'),
                        'depends': json.dumps(manifest.get('depends', [])),
                        'external_dependencies': json.dumps(manifest.get('external_dependencies', [])),
                        'manifest_data': json.dumps(manifest),
                        'install_path': addon_info['path'],
                        'is_installed': addon_info['installed'],
                        'status': 'installed' if addon_info['installed'] else 'available',
                        'is_application': manifest.get('application', False),
                        'auto_install': manifest.get('auto_install', False),
                    })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to scan addons: {e}")
            return False
    
    @classmethod
    def get_installed_addons(cls):
        """Get all installed addons"""
        return cls.search([('is_installed', '=', True)])
    
    @classmethod
    def get_available_addons(cls):
        """Get all available addons"""
        return cls.search([('is_installed', '=', False)])
    
    @classmethod
    def get_applications(cls):
        """Get all application addons"""
        return cls.search([('is_application', '=', True)])
    
    @classmethod
    def get_broken_addons(cls):
        """Get all broken addons"""
        return cls.search([('status', '=', 'broken')])