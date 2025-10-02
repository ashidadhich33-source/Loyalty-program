# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Company Settings
============================================

Standalone version of the company settings model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CompanySettings(BaseModel):
    """Company settings model for Kids Clothing ERP"""
    
    _name = 'company.settings'
    _description = 'Company Settings'
    _table = 'company_settings'
    
    # Basic fields
    name = CharField(
        string='Setting Name',
        size=100,
        required=True,
        help='Name of the setting'
    )
    
    key = CharField(
        string='Setting Key',
        size=100,
        required=True,
        help='Unique key for the setting'
    )
    
    value = TextField(
        string='Setting Value',
        help='Value of the setting'
    )
    
    description = TextField(
        string='Description',
        help='Description of the setting'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        required=True,
        help='Company this setting belongs to'
    )
    
    # Setting information
    setting_type = SelectionField(
        string='Setting Type',
        selection=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('float', 'Float'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
            ('list', 'List'),
            ('dict', 'Dictionary'),
        ],
        default='string',
        help='Type of the setting value'
    )
    
    # Setting category
    category = SelectionField(
        string='Category',
        selection=[
            ('general', 'General'),
            ('financial', 'Financial'),
            ('inventory', 'Inventory'),
            ('sales', 'Sales'),
            ('purchase', 'Purchase'),
            ('hr', 'Human Resources'),
            ('security', 'Security'),
            ('integration', 'Integration'),
            ('custom', 'Custom'),
        ],
        default='general',
        help='Category of the setting'
    )
    
    # Setting status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the setting is active'
    )
    
    is_system_setting = BooleanField(
        string='System Setting',
        default=False,
        help='Whether this is a system setting'
    )
    
    # Setting validation
    validation_rules = TextField(
        string='Validation Rules',
        help='JSON validation rules for this setting'
    )
    
    # Setting metadata
    created_by = IntegerField(
        string='Created By',
        help='User who created this setting'
    )
    
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when setting was created'
    )
    
    updated_by = IntegerField(
        string='Updated By',
        help='User who last updated this setting'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date when setting was last updated'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set created date
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        # Set updated date
        vals['updated_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle setting updates"""
        # Set updated date
        vals['updated_date'] = datetime.now()
        
        result = super().write(vals)
        
        # Log setting updates
        for setting in self:
            if vals:
                logger.info(f"Setting {setting.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system settings"""
        for setting in self:
            if setting.is_system_setting:
                raise ValueError('System settings cannot be deleted')
        
        return super().unlink()
    
    def get_setting_value(self):
        """Get setting value with proper type conversion"""
        if not self.value:
            return None
        
        try:
            if self.setting_type == 'string':
                return str(self.value)
            elif self.setting_type == 'integer':
                return int(self.value)
            elif self.setting_type == 'float':
                return float(self.value)
            elif self.setting_type == 'boolean':
                return self.value.lower() in ['true', '1', 'yes', 'on']
            elif self.setting_type in ['json', 'list', 'dict']:
                import json
                return json.loads(self.value)
            else:
                return self.value
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logger.error(f"Error converting setting value: {e}")
            return self.value
    
    def set_setting_value(self, value):
        """Set setting value with proper type conversion"""
        if self.setting_type == 'string':
            self.value = str(value)
        elif self.setting_type == 'integer':
            self.value = str(int(value))
        elif self.setting_type == 'float':
            self.value = str(float(value))
        elif self.setting_type == 'boolean':
            self.value = str(bool(value)).lower()
        elif self.setting_type in ['json', 'list', 'dict']:
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)
    
    def validate_setting_value(self):
        """Validate setting value"""
        if not self.validation_rules:
            return True
        
        try:
            import json
            rules = json.loads(self.validation_rules)
            value = self.get_setting_value()
            
            # Check required
            if rules.get('required', False) and value is None:
                raise ValueError(f'Setting {self.name} is required')
            
            # Check min/max for numeric values
            if self.setting_type in ['integer', 'float']:
                if 'min' in rules and value < rules['min']:
                    raise ValueError(f'Setting {self.name} must be >= {rules["min"]}')
                if 'max' in rules and value > rules['max']:
                    raise ValueError(f'Setting {self.name} must be <= {rules["max"]}')
            
            # Check length for string values
            if self.setting_type == 'string':
                if 'min_length' in rules and len(value) < rules['min_length']:
                    raise ValueError(f'Setting {self.name} must be at least {rules["min_length"]} characters')
                if 'max_length' in rules and len(value) > rules['max_length']:
                    raise ValueError(f'Setting {self.name} must be at most {rules["max_length"]} characters')
            
            # Check allowed values
            if 'allowed_values' in rules and value not in rules['allowed_values']:
                raise ValueError(f'Setting {self.name} must be one of: {rules["allowed_values"]}')
            
            return True
            
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logger.error(f"Setting validation error: {e}")
            return False
    
    def get_setting_info(self):
        """Get setting information"""
        return {
            'name': self.name,
            'key': self.key,
            'value': self.get_setting_value(),
            'setting_type': self.setting_type,
            'category': self.category,
            'is_active': self.is_active,
            'is_system_setting': self.is_system_setting,
            'description': self.description,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
        }
    
    @classmethod
    def get_company_settings(cls, company_id: int, category: str = None):
        """Get company settings"""
        domain = [('company_id', '=', company_id), ('is_active', '=', True)]
        if category:
            domain.append(('category', '=', category))
        
        return cls.search(domain)
    
    @classmethod
    def get_company_setting(cls, company_id: int, setting_key: str):
        """Get specific company setting"""
        setting = cls.search([
            ('company_id', '=', company_id),
            ('key', '=', setting_key),
            ('is_active', '=', True),
        ], limit=1)
        
        return setting.get_setting_value() if setting else None
    
    @classmethod
    def set_company_setting(cls, company_id: int, setting_key: str, value, setting_type: str = 'string', category: str = 'general'):
        """Set company setting"""
        setting = cls.search([
            ('company_id', '=', company_id),
            ('key', '=', setting_key),
        ], limit=1)
        
        if setting:
            setting.set_setting_value(value)
            setting.setting_type = setting_type
            setting.category = category
            setting.updated_date = datetime.now()
        else:
            setting = cls.create({
                'company_id': company_id,
                'key': setting_key,
                'setting_type': setting_type,
                'category': category,
            })
            setting.set_setting_value(value)
        
        return setting
    
    @classmethod
    def get_settings_by_category(cls, category: str):
        """Get settings by category"""
        return cls.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_settings(cls):
        """Get system settings"""
        return cls.search([
            ('is_system_setting', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_settings(cls):
        """Get custom settings"""
        return cls.search([
            ('is_system_setting', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_setting_analytics(cls):
        """Get setting analytics"""
        # In standalone version, we'll return mock data
        return {
            'total_settings': 0,
            'active_settings': 0,
            'system_settings': 0,
            'custom_settings': 0,
            'inactive_settings': 0,
            'settings_by_category': {},
        }
    
    def _check_setting_key(self):
        """Validate setting key"""
        if not self.key:
            raise ValueError('Setting key is required')
        
        # Check for duplicate keys for the same company
        existing = self.search([
            ('company_id', '=', self.company_id),
            ('key', '=', self.key),
            ('id', '!=', self.id),
        ])
        if existing:
            raise ValueError('Setting key must be unique for each company')
    
    def _check_setting_type(self):
        """Validate setting type"""
        valid_types = ['string', 'integer', 'float', 'boolean', 'json', 'list', 'dict']
        if self.setting_type not in valid_types:
            raise ValueError(f'Invalid setting type: {self.setting_type}')
    
    def _check_category(self):
        """Validate category"""
        valid_categories = ['general', 'financial', 'inventory', 'sales', 'purchase', 'hr', 'security', 'integration', 'custom']
        if self.category not in valid_categories:
            raise ValueError(f'Invalid category: {self.category}')
    
    def action_duplicate(self):
        """Duplicate setting"""
        self.ensure_one()
        
        new_setting = self.copy({
            'name': f'{self.name} (Copy)',
            'key': f'{self.key}_copy',
            'is_system_setting': False,
        })
        
        return new_setting
    
    def action_export_setting(self):
        """Export setting data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'key': self.key,
            'value': self.get_setting_value(),
            'setting_type': self.setting_type,
            'category': self.category,
            'is_active': self.is_active,
            'description': self.description,
        }
    
    def action_import_setting(self, setting_data: Dict[str, Any]):
        """Import setting data"""
        self.ensure_one()
        
        self.write(setting_data)
        return True