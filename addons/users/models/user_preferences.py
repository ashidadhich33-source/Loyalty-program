# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json

_logger = logging.getLogger(__name__)


class UserPreferences(models.Model):
    """User preferences model for Kids Clothing ERP"""
    
    _name = 'user.preferences'
    _description = 'User Preferences'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Preference Name',
        required=True,
        help='Name of the preference'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the preference'
    )
    
    key = fields.Char(
        string='Key',
        required=True,
        help='Unique key for the preference'
    )
    
    # Preference details
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        help='User this preference belongs to'
    )
    
    value = fields.Text(
        string='Value',
        help='Value of the preference'
    )
    
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ], string='Value Type', default='string', help='Type of the preference value')
    
    # Preference category
    category = fields.Selection([
        ('ui', 'User Interface'),
        ('notifications', 'Notifications'),
        ('security', 'Security'),
        ('performance', 'Performance'),
        ('accessibility', 'Accessibility'),
        ('localization', 'Localization'),
        ('integration', 'Integration'),
        ('custom', 'Custom'),
    ], string='Category', default='custom', help='Category of the preference')
    
    # Preference scope
    scope = fields.Selection([
        ('user', 'User'),
        ('company', 'Company'),
        ('global', 'Global'),
    ], string='Scope', default='user', help='Scope of the preference')
    
    # Preference status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the preference is active'
    )
    
    is_system_preference = fields.Boolean(
        string='System Preference',
        default=False,
        help='Whether this is a system preference (cannot be deleted)'
    )
    
    # Preference validation
    validation_rule = fields.Text(
        string='Validation Rule',
        help='Python validation rule for the preference value'
    )
    
    default_value = fields.Text(
        string='Default Value',
        help='Default value for the preference'
    )
    
    # Preference options
    options = fields.Text(
        string='Options',
        help='Available options for the preference (JSON format)'
    )
    
    # Preference metadata
    metadata = fields.Text(
        string='Metadata',
        help='Additional metadata for the preference (JSON format)'
    )
    
    # Preference analytics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this preference has been accessed'
    )
    
    last_accessed = fields.Datetime(
        string='Last Accessed',
        help='When this preference was last accessed'
    )
    
    # Preference dependencies
    depends_on = fields.Many2many(
        'user.preferences',
        'preference_dependency_rel',
        'preference_id',
        'dependency_id',
        string='Depends On',
        help='Preferences this preference depends on'
    )
    
    required_by = fields.Many2many(
        'user.preferences',
        'preference_dependency_rel',
        'dependency_id',
        'preference_id',
        string='Required By',
        help='Preferences that depend on this preference'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default value if not provided
        if 'value' not in vals and 'default_value' in vals:
            vals['value'] = vals['default_value']
        
        return super(UserPreferences, self).create(vals)
    
    def write(self, vals):
        """Override write to handle preference updates"""
        result = super(UserPreferences, self).write(vals)
        
        # Update last accessed timestamp
        if vals:
            self.last_accessed = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system preferences"""
        for preference in self:
            if preference.is_system_preference:
                raise ValidationError(_('System preferences cannot be deleted'))
        
        return super(UserPreferences, self).unlink()
    
    def get_value(self):
        """Get preference value with type conversion"""
        if not self.value:
            return self.default_value
        
        try:
            if self.value_type == 'string':
                return self.value
            elif self.value_type == 'integer':
                return int(self.value)
            elif self.value_type == 'float':
                return float(self.value)
            elif self.value_type == 'boolean':
                return self.value.lower() in ('true', '1', 'yes', 'on')
            elif self.value_type == 'json':
                return json.loads(self.value)
            elif self.value_type == 'date':
                return fields.Date.from_string(self.value)
            elif self.value_type == 'datetime':
                return fields.Datetime.from_string(self.value)
            else:
                return self.value
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            _logger.error(f"Error converting preference value: {str(e)}")
            return self.default_value
    
    def set_value(self, value):
        """Set preference value with type conversion"""
        try:
            if self.value_type == 'string':
                self.value = str(value)
            elif self.value_type == 'integer':
                self.value = str(int(value))
            elif self.value_type == 'float':
                self.value = str(float(value))
            elif self.value_type == 'boolean':
                self.value = str(bool(value)).lower()
            elif self.value_type == 'json':
                self.value = json.dumps(value)
            elif self.value_type == 'date':
                self.value = fields.Date.to_string(value)
            elif self.value_type == 'datetime':
                self.value = fields.Datetime.to_string(value)
            else:
                self.value = str(value)
            
            # Update usage statistics
            self.usage_count += 1
            self.last_accessed = fields.Datetime.now()
            
        except (ValueError, TypeError, json.JSONEncodeError) as e:
            _logger.error(f"Error setting preference value: {str(e)}")
            raise ValidationError(_('Invalid value for preference: %s') % str(e))
    
    def validate_value(self, value):
        """Validate preference value"""
        if self.validation_rule:
            try:
                # Evaluate validation rule
                eval_context = {
                    'value': value,
                    'self': self,
                    'preference': self,
                }
                if not eval(self.validation_rule, eval_context):
                    raise ValidationError(_('Preference value validation failed'))
            except Exception as e:
                _logger.error(f"Error validating preference value: {str(e)}")
                raise ValidationError(_('Preference value validation error: %s') % str(e))
        
        return True
    
    def get_options(self):
        """Get preference options"""
        if self.options:
            try:
                return json.loads(self.options)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_metadata(self):
        """Get preference metadata"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_metadata(self, metadata):
        """Set preference metadata"""
        self.metadata = json.dumps(metadata)
    
    def get_preference_summary(self):
        """Get preference summary"""
        return {
            'name': self.name,
            'key': self.key,
            'value': self.get_value(),
            'value_type': self.value_type,
            'category': self.category,
            'scope': self.scope,
            'is_active': self.is_active,
            'usage_count': self.usage_count,
            'last_accessed': self.last_accessed,
        }
    
    @api.model
    def get_user_preferences(self, user_id, category=None):
        """Get preferences for a specific user"""
        domain = [('user_id', '=', user_id), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_preference_by_key(self, user_id, key):
        """Get preference by key for a specific user"""
        return self.search([
            ('user_id', '=', user_id),
            ('key', '=', key),
            ('is_active', '=', True),
        ], limit=1)
    
    @api.model
    def set_user_preference(self, user_id, key, value, value_type='string', category='custom'):
        """Set user preference"""
        preference = self.get_preference_by_key(user_id, key)
        
        if preference:
            preference.set_value(value)
        else:
            self.create({
                'user_id': user_id,
                'key': key,
                'value': str(value),
                'value_type': value_type,
                'category': category,
            })
    
    @api.model
    def get_user_preference(self, user_id, key, default=None):
        """Get user preference value"""
        preference = self.get_preference_by_key(user_id, key)
        
        if preference:
            return preference.get_value()
        else:
            return default
    
    @api.model
    def get_company_preferences(self, company_id, category=None):
        """Get preferences for a specific company"""
        domain = [('scope', '=', 'company'), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_global_preferences(self, category=None):
        """Get global preferences"""
        domain = [('scope', '=', 'global'), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_preferences_by_category(self, category):
        """Get preferences by category"""
        return self.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_system_preferences(self):
        """Get all system preferences"""
        return self.search([
            ('is_system_preference', '=', True),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_custom_preferences(self):
        """Get all custom preferences"""
        return self.search([
            ('is_system_preference', '=', False),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_preference_analytics(self):
        """Get preference analytics"""
        total_preferences = self.search_count([])
        active_preferences = self.search_count([('is_active', '=', True)])
        system_preferences = self.search_count([('is_system_preference', '=', True)])
        custom_preferences = self.search_count([('is_system_preference', '=', False)])
        
        return {
            'total_preferences': total_preferences,
            'active_preferences': active_preferences,
            'system_preferences': system_preferences,
            'custom_preferences': custom_preferences,
            'inactive_preferences': total_preferences - active_preferences,
            'active_percentage': (active_preferences / total_preferences * 100) if total_preferences > 0 else 0,
        }
    
    @api.constrains('key')
    def _check_key(self):
        """Validate preference key"""
        for preference in self:
            if preference.key:
                # Check for duplicate keys for the same user
                existing = self.search([
                    ('key', '=', preference.key),
                    ('user_id', '=', preference.user_id.id),
                    ('id', '!=', preference.id),
                ])
                if existing:
                    raise ValidationError(_('Preference key must be unique for each user'))
    
    @api.constrains('depends_on')
    def _check_dependencies(self):
        """Validate preference dependencies"""
        for preference in self:
            if preference in preference.depends_on:
                raise ValidationError(_('Preference cannot depend on itself'))
            
            # Check for circular dependencies
            for dep in preference.depends_on:
                if preference in dep.required_by:
                    raise ValidationError(_('Circular dependency detected'))
    
    def action_activate(self):
        """Activate preference"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate preference"""
        self.is_active = False
        return True
    
    def action_reset_to_default(self):
        """Reset preference to default value"""
        if self.default_value:
            self.value = self.default_value
        return True
    
    def action_duplicate(self):
        """Duplicate preference"""
        self.ensure_one()
        
        new_preference = self.copy({
            'name': f'{self.name} (Copy)',
            'key': f'{self.key}_copy',
            'is_system_preference': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Preference',
            'res_model': 'user.preferences',
            'res_id': new_preference.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_preference(self):
        """Export preference definition"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'key': self.key,
            'value': self.value,
            'value_type': self.value_type,
            'category': self.category,
            'scope': self.scope,
            'default_value': self.default_value,
            'options': self.options,
            'metadata': self.metadata,
        }
    
    def action_import_preference(self, preference_data):
        """Import preference definition"""
        self.ensure_one()
        
        self.write(preference_data)
        return True