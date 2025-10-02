#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Addon Manager
================================

Addon management system for the standalone ERP system.
"""

import os
import sys
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

class AddonManager:
    """Addon Manager for ERP System"""
    
    def __init__(self, config):
        """Initialize addon manager"""
        self.config = config
        self.addons_path = config.get_addons_path()
        self.addons = {}
        self.loaded_addons = []
        self.logger = logging.getLogger('ERP.AddonManager')
        
    def load_addons(self):
        """Load all available addons"""
        try:
            self.logger.info("Loading addons...")
            
            # Scan addons directory
            addon_dirs = self._scan_addon_directories()
            
            # Load each addon
            for addon_name in addon_dirs:
                self._load_addon(addon_name)
            
            # Install addons if auto_install is enabled
            if self.config.get('addons.auto_install', True):
                self._auto_install_addons()
            
            self.logger.info(f"Loaded {len(self.loaded_addons)} addons")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load addons: {e}")
            return False
    
    def _scan_addon_directories(self) -> List[str]:
        """Scan addons directory for available addons"""
        addon_dirs = []
        
        if not os.path.exists(self.addons_path):
            self.logger.warning(f"Addons directory not found: {self.addons_path}")
            return addon_dirs
        
        for item in os.listdir(self.addons_path):
            item_path = os.path.join(self.addons_path, item)
            if os.path.isdir(item_path):
                manifest_path = os.path.join(item_path, '__manifest__.py')
                if os.path.exists(manifest_path):
                    addon_dirs.append(item)
        
        return sorted(addon_dirs)
    
    def _load_addon(self, addon_name: str):
        """Load a specific addon"""
        try:
            addon_path = os.path.join(self.addons_path, addon_name)
            manifest_path = os.path.join(addon_path, '__manifest__.py')
            
            # Load manifest
            manifest = self._load_manifest(manifest_path)
            if not manifest:
                return False
            
            # Add to addons registry
            self.addons[addon_name] = {
                'name': addon_name,
                'path': addon_path,
                'manifest': manifest,
                'installed': False,
                'models': [],
                'views': [],
                'data': []
            }
            
            self.logger.info(f"Loaded addon: {addon_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load addon {addon_name}: {e}")
            return False
    
    def _load_manifest(self, manifest_path: str) -> Optional[Dict]:
        """Load addon manifest"""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_content = f.read()
            
            # Execute manifest to get dictionary
            manifest_globals = {}
            exec(manifest_content, manifest_globals)
            
            # Find the manifest dictionary
            for key, value in manifest_globals.items():
                if isinstance(value, dict) and 'name' in value:
                    return value
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to load manifest {manifest_path}: {e}")
            return None
    
    def _auto_install_addons(self):
        """Auto-install addons if configured"""
        for addon_name, addon_info in self.addons.items():
            if addon_info['manifest'].get('auto_install', False):
                self.install_addon(addon_name)
    
    def install_addon(self, addon_name: str) -> bool:
        """Install a specific addon"""
        try:
            if addon_name not in self.addons:
                self.logger.error(f"Addon {addon_name} not found")
                return False
            
            addon_info = self.addons[addon_name]
            manifest = addon_info['manifest']
            
            # Check dependencies
            if not self._check_dependencies(manifest.get('depends', [])):
                self.logger.error(f"Dependencies not met for {addon_name}")
                return False
            
            # Load models
            self._load_addon_models(addon_name)
            
            # Load views
            self._load_addon_views(addon_name)
            
            # Load data
            self._load_addon_data(addon_name)
            
            # Mark as installed
            addon_info['installed'] = True
            self.loaded_addons.append(addon_name)
            
            self.logger.info(f"Installed addon: {addon_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install addon {addon_name}: {e}")
            return False
    
    def _check_dependencies(self, depends: List[str]) -> bool:
        """Check if addon dependencies are met"""
        for dep in depends:
            if dep not in self.loaded_addons:
                self.logger.warning(f"Dependency {dep} not installed")
                return False
        return True
    
    def _load_addon_models(self, addon_name: str):
        """Load addon models"""
        try:
            addon_path = self.addons[addon_name]['path']
            models_path = os.path.join(addon_path, 'models')
            
            if not os.path.exists(models_path):
                return
            
            # Add models directory to Python path
            if models_path not in sys.path:
                sys.path.insert(0, models_path)
            
            # Import models
            for file_name in os.listdir(models_path):
                if file_name.endswith('.py') and file_name != '__init__.py':
                    module_name = file_name[:-3]
                    try:
                        module = importlib.import_module(module_name)
                        self.logger.info(f"Loaded model {module_name} from {addon_name}")
                    except Exception as e:
                        self.logger.error(f"Failed to load model {module_name}: {e}")
            
        except Exception as e:
            self.logger.error(f"Failed to load models for {addon_name}: {e}")
    
    def _load_addon_views(self, addon_name: str):
        """Load addon views"""
        try:
            addon_path = self.addons[addon_name]['path']
            views_path = os.path.join(addon_path, 'views')
            
            if not os.path.exists(views_path):
                return
            
            # Load view files
            for file_name in os.listdir(views_path):
                if file_name.endswith('.xml'):
                    view_path = os.path.join(views_path, file_name)
                    self.logger.info(f"Loaded view {file_name} from {addon_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load views for {addon_name}: {e}")
    
    def _load_addon_data(self, addon_name: str):
        """Load addon data"""
        try:
            addon_path = self.addons[addon_name]['path']
            data_path = os.path.join(addon_path, 'data')
            
            if not os.path.exists(data_path):
                return
            
            # Load data files
            for file_name in os.listdir(data_path):
                if file_name.endswith('.xml'):
                    data_file_path = os.path.join(data_path, file_name)
                    self.logger.info(f"Loaded data {file_name} from {addon_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load data for {addon_name}: {e}")
    
    def uninstall_addon(self, addon_name: str) -> bool:
        """Uninstall a specific addon"""
        try:
            if addon_name not in self.addons:
                self.logger.error(f"Addon {addon_name} not found")
                return False
            
            addon_info = self.addons[addon_name]
            
            # Check if other addons depend on this one
            if self._check_reverse_dependencies(addon_name):
                self.logger.error(f"Cannot uninstall {addon_name}: other addons depend on it")
                return False
            
            # Mark as uninstalled
            addon_info['installed'] = False
            if addon_name in self.loaded_addons:
                self.loaded_addons.remove(addon_name)
            
            self.logger.info(f"Uninstalled addon: {addon_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to uninstall addon {addon_name}: {e}")
            return False
    
    def _check_reverse_dependencies(self, addon_name: str) -> bool:
        """Check if other addons depend on this addon"""
        for other_addon_name, other_addon_info in self.addons.items():
            if other_addon_info['installed']:
                depends = other_addon_info['manifest'].get('depends', [])
                if addon_name in depends:
                    return True
        return False
    
    def update_addons(self):
        """Update all installed addons"""
        try:
            self.logger.info("Updating addons...")
            
            for addon_name in self.loaded_addons:
                self._update_addon(addon_name)
            
            self.logger.info("Addons updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update addons: {e}")
            return False
    
    def _update_addon(self, addon_name: str):
        """Update a specific addon"""
        try:
            # Reload addon
            self._load_addon(addon_name)
            
            # Reinstall if needed
            if self.addons[addon_name]['installed']:
                self.install_addon(addon_name)
            
            self.logger.info(f"Updated addon: {addon_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to update addon {addon_name}: {e}")
    
    def get_addon_info(self, addon_name: str) -> Optional[Dict]:
        """Get addon information"""
        return self.addons.get(addon_name)
    
    def list_addons(self) -> List[Dict]:
        """List all addons"""
        return list(self.addons.values())
    
    def list_installed_addons(self) -> List[str]:
        """List installed addons"""
        return self.loaded_addons.copy()