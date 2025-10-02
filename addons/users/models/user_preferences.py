# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - User Preferences
===========================================

Standalone version of the user preferences model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class UserPreferences(BaseModel):
    """User preferences model for Kids Clothing ERP"""
    
    _name = 'user.preferences'
    _description = 'User Preferences'
    _table = 'user_preferences'
    
    # Basic preference information
    user_id = IntegerField(
        string='User ID',
        required=True,
        help='User this preference belongs to'
    )
    
    preference_key = CharField(
        string='Preference Key',
        size=100,
        required=True,
        help='Preference key/name'
    )
    
    preference_value = TextField(
        string='Preference Value',
        help='Preference value (JSON encoded)'
    )
    
    preference_type = SelectionField(
        string='Preference Type',
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
        help='Type of preference value'
    )
    
    # Preference category
    category = SelectionField(
        string='Category',
        selection=[
            ('ui', 'User Interface'),
            ('notifications', 'Notifications'),
            ('security', 'Security'),
            ('data', 'Data Display'),
            ('workflow', 'Workflow'),
            ('integration', 'Integration'),
            ('custom', 'Custom'),
        ],
        default='custom',
        help='Preference category'
    )
    
    # Preference settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the preference is active'
    )
    
    is_system_preference = BooleanField(
        string='System Preference',
        default=False,
        help='Whether this is a system preference'
    )
    
    # Preference metadata
    description = TextField(
        string='Description',
        help='Preference description'
    )
    
    default_value = TextField(
        string='Default Value',
        help='Default value for this preference'
    )
    
    # Preference validation
    validation_rules = TextField(
        string='Validation Rules',
        help='JSON validation rules for this preference'
    )
    
    # Preference timing
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when preference was created'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date when preference was last updated'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='Date when preference was last used'
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
        """Override write to handle preference updates"""
        # Set updated date
        vals['updated_date'] = datetime.now()
        vals['last_used'] = datetime.now()
        
        result = super().write(vals)
        
        # Log preference updates
        for preference in self:
            if vals:
                logger.info(f"Preference {preference.preference_key} updated for user {preference.user_id}")
        
        return result
    
    def get_preference_value(self):
        """Get preference value with proper type conversion"""
        if not self.preference_value:
            return None
        
        try:
            if self.preference_type == 'string':
                return str(self.preference_value)
            elif self.preference_type == 'integer':
                return int(self.preference_value)
            elif self.preference_type == 'float':
                return float(self.preference_value)
            elif self.preference_type == 'boolean':
                return self.preference_value.lower() in ['true', '1', 'yes', 'on']
            elif self.preference_type in ['json', 'list', 'dict']:
                return json.loads(self.preference_value)
            else:
                return self.preference_value
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logger.error(f"Error converting preference value: {e}")
            return self.preference_value
    
    def set_preference_value(self, value):
        """Set preference value with proper type conversion"""
        if self.preference_type == 'string':
            self.preference_value = str(value)
        elif self.preference_type == 'integer':
            self.preference_value = str(int(value))
        elif self.preference_type == 'float':
            self.preference_value = str(float(value))
        elif self.preference_type == 'boolean':
            self.preference_value = str(bool(value)).lower()
        elif self.preference_type in ['json', 'list', 'dict']:
            self.preference_value = json.dumps(value)
        else:
            self.preference_value = str(value)
    
    def validate_preference_value(self):
        """Validate preference value"""
        if not self.validation_rules:
            return True
        
        try:
            rules = json.loads(self.validation_rules)
            value = self.get_preference_value()
            
            # Check required
            if rules.get('required', False) and value is None:
                raise ValueError(f'Preference {self.preference_key} is required')
            
            # Check min/max for numeric values
            if self.preference_type in ['integer', 'float']:
                if 'min' in rules and value < rules['min']:
                    raise ValueError(f'Preference {self.preference_key} must be >= {rules["min"]}')
                if 'max' in rules and value > rules['max']:
                    raise ValueError(f'Preference {self.preference_key} must be <= {rules["max"]}')
            
            # Check length for string values
            if self.preference_type == 'string':
                if 'min_length' in rules and len(value) < rules['min_length']:
                    raise ValueError(f'Preference {self.preference_key} must be at least {rules["min_length"]} characters')
                if 'max_length' in rules and len(value) > rules['max_length']:
                    raise ValueError(f'Preference {self.preference_key} must be at most {rules["max_length"]} characters')
            
            # Check allowed values
            if 'allowed_values' in rules and value not in rules['allowed_values']:
                raise ValueError(f'Preference {self.preference_key} must be one of: {rules["allowed_values"]}')
            
            return True
            
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            logger.error(f"Preference validation error: {e}")
            return False
    
    def get_preference_info(self):
        """Get preference information"""
        return {
            'user_id': self.user_id,
            'preference_key': self.preference_key,
            'preference_value': self.get_preference_value(),
            'preference_type': self.preference_type,
            'category': self.category,
            'is_active': self.is_active,
            'description': self.description,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'last_used': self.last_used,
        }
    
    @classmethod
    def get_user_preferences(cls, user_id: int, category: str = None):
        """Get user preferences"""
        domain = [('user_id', '=', user_id), ('is_active', '=', True)]
        if category:
            domain.append(('category', '=', category))
        
        return cls.search(domain)
    
    @classmethod
    def get_user_preference(cls, user_id: int, preference_key: str):
        """Get specific user preference"""
        preference = cls.search([
            ('user_id', '=', user_id),
            ('preference_key', '=', preference_key),
            ('is_active', '=', True),
        ], limit=1)
        
        return preference.get_preference_value() if preference else None
    
    @classmethod
    def set_user_preference(cls, user_id: int, preference_key: str, value, preference_type: str = 'string', category: str = 'custom'):
        """Set user preference"""
        preference = cls.search([
            ('user_id', '=', user_id),
            ('preference_key', '=', preference_key),
        ], limit=1)
        
        if preference:
            preference.set_preference_value(value)
            preference.preference_type = preference_type
            preference.category = category
            preference.updated_date = datetime.now()
            preference.last_used = datetime.now()
        else:
            preference = cls.create({
                'user_id': user_id,
                'preference_key': preference_key,
                'preference_type': preference_type,
                'category': category,
            })
            preference.set_preference_value(value)
        
        return preference
    
    @classmethod
    def get_preferences_by_category(cls, category: str):
        """Get preferences by category"""
        return cls.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_preferences(cls):
        """Get system preferences"""
        return cls.search([
            ('is_system_preference', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_preferences(cls):
        """Get custom preferences"""
        return cls.search([
            ('is_system_preference', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_preference_analytics(cls):
        """Get preference analytics"""
        total_preferences = cls.search_count([])
        active_preferences = cls.search_count([('is_active', '=', True)])
        system_preferences = cls.search_count([('is_system_preference', '=', True)])
        custom_preferences = cls.search_count([('is_system_preference', '=', False)])
        
        # Get preferences by category
        preferences_by_category = {}
        for category in ['ui', 'notifications', 'security', 'data', 'workflow', 'integration', 'custom']:
            count = cls.search_count([
                ('category', '=', category),
                ('is_active', '=', True),
            ])
            preferences_by_category[category] = count
        
        return {
            'total_preferences': total_preferences,
            'active_preferences': active_preferences,
            'system_preferences': system_preferences,
            'custom_preferences': custom_preferences,
            'inactive_preferences': total_preferences - active_preferences,
            'preferences_by_category': preferences_by_category,
        }
    
    def _check_preference_key(self):
        """Validate preference key"""
        if not self.preference_key:
            raise ValueError('Preference key is required')
        
        # Check for duplicate keys for the same user
        existing = self.search([
            ('user_id', '=', self.user_id),
            ('preference_key', '=', self.preference_key),
            ('id', '!=', self.id),
        ])
        if existing:
            raise ValueError('Preference key must be unique for each user')
    
    def _check_preference_type(self):
        """Validate preference type"""
        valid_types = ['string', 'integer', 'float', 'boolean', 'json', 'list', 'dict']
        if self.preference_type not in valid_types:
            raise ValueError(f'Invalid preference type: {self.preference_type}')
    
    def _check_category(self):
        """Validate category"""
        valid_categories = ['ui', 'notifications', 'security', 'data', 'workflow', 'integration', 'custom']
        if self.category not in valid_categories:
            raise ValueError(f'Invalid category: {self.category}')