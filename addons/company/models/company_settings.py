# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CompanySettings(models.Model):
    """Company settings model for Kids Clothing ERP"""
    
    _name = 'company.settings'
    _description = 'Company Settings'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Setting Name',
        required=True,
        help='Name of the setting'
    )
    
    key = fields.Char(
        string='Setting Key',
        required=True,
        help='Unique key for the setting'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the setting'
    )
    
    # Company relationship
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='Company this setting belongs to'
    )
    
    # Setting details
    value = fields.Text(
        string='Value',
        help='Value of the setting'
    )
    
    value_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
    ], string='Value Type', default='string', help='Type of the setting value')
    
    # Setting category
    category = fields.Selection([
        ('general', 'General'),
        ('financial', 'Financial'),
        ('inventory', 'Inventory'),
        ('sales', 'Sales'),
        ('purchase', 'Purchase'),
        ('hr', 'Human Resources'),
        ('pos', 'Point of Sale'),
        ('ecommerce', 'E-commerce'),
        ('integration', 'Integration'),
        ('security', 'Security'),
        ('custom', 'Custom'),
    ], string='Category', default='general', help='Category of the setting')
    
    # Setting scope
    scope = fields.Selection([
        ('company', 'Company'),
        ('branch', 'Branch'),
        ('location', 'Location'),
        ('user', 'User'),
    ], string='Scope', default='company', help='Scope of the setting')
    
    # Setting status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the setting is active'
    )
    
    is_system_setting = fields.Boolean(
        string='System Setting',
        default=False,
        help='Whether this is a system setting (cannot be deleted)'
    )
    
    # Setting validation
    validation_rule = fields.Text(
        string='Validation Rule',
        help='Python validation rule for the setting value'
    )
    
    default_value = fields.Text(
        string='Default Value',
        help='Default value for the setting'
    )
    
    # Setting options
    options = fields.Text(
        string='Options',
        help='Available options for the setting (JSON format)'
    )
    
    # Setting metadata
    metadata = fields.Text(
        string='Metadata',
        help='Additional metadata for the setting (JSON format)'
    )
    
    # Setting analytics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this setting has been accessed'
    )
    
    last_accessed = fields.Datetime(
        string='Last Accessed',
        help='When this setting was last accessed'
    )
    
    # Setting dependencies
    depends_on = fields.Many2many(
        'company.settings',
        'company_setting_dependency_rel',
        'setting_id',
        'dependency_id',
        string='Depends On',
        help='Settings this setting depends on'
    )
    
    required_by = fields.Many2many(
        'company.settings',
        'company_setting_dependency_rel',
        'dependency_id',
        'setting_id',
        string='Required By',
        help='Settings that depend on this setting'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default value if not provided
        if 'value' not in vals and 'default_value' in vals:
            vals['value'] = vals['default_value']
        
        return super(CompanySettings, self).create(vals)
    
    def write(self, vals):
        """Override write to handle setting updates"""
        result = super(CompanySettings, self).write(vals)
        
        # Update last accessed timestamp
        if vals:
            self.last_accessed = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system settings"""
        for setting in self:
            if setting.is_system_setting:
                raise ValidationError(_('System settings cannot be deleted'))
        
        return super(CompanySettings, self).unlink()
    
    def get_value(self):
        """Get setting value with type conversion"""
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
                import json
                return json.loads(self.value)
            elif self.value_type == 'date':
                return fields.Date.from_string(self.value)
            elif self.value_type == 'datetime':
                return fields.Datetime.from_string(self.value)
            else:
                return self.value
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            _logger.error(f"Error converting setting value: {str(e)}")
            return self.default_value
    
    def set_value(self, value):
        """Set setting value with type conversion"""
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
                import json
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
            _logger.error(f"Error setting setting value: {str(e)}")
            raise ValidationError(_('Invalid value for setting: %s') % str(e))
    
    def validate_value(self, value):
        """Validate setting value"""
        if self.validation_rule:
            try:
                # Evaluate validation rule
                eval_context = {
                    'value': value,
                    'self': self,
                    'setting': self,
                }
                if not eval(self.validation_rule, eval_context):
                    raise ValidationError(_('Setting value validation failed'))
            except Exception as e:
                _logger.error(f"Error validating setting value: {str(e)}")
                raise ValidationError(_('Setting value validation error: %s') % str(e))
        
        return True
    
    def get_options(self):
        """Get setting options"""
        if self.options:
            try:
                import json
                return json.loads(self.options)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_metadata(self):
        """Get setting metadata"""
        if self.metadata:
            try:
                import json
                return json.loads(self.metadata)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_metadata(self, metadata):
        """Set setting metadata"""
        import json
        self.metadata = json.dumps(metadata)
    
    def get_setting_summary(self):
        """Get setting summary"""
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
    def get_company_settings(self, company_id, category=None):
        """Get settings for a specific company"""
        domain = [('company_id', '=', company_id), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_setting_by_key(self, company_id, key):
        """Get setting by key for a specific company"""
        return self.search([
            ('company_id', '=', company_id),
            ('key', '=', key),
            ('is_active', '=', True),
        ], limit=1)
    
    @api.model
    def set_company_setting(self, company_id, key, value, value_type='string', category='general'):
        """Set company setting"""
        setting = self.get_setting_by_key(company_id, key)
        
        if setting:
            setting.set_value(value)
        else:
            self.create({
                'company_id': company_id,
                'key': key,
                'value': str(value),
                'value_type': value_type,
                'category': category,
            })
    
    @api.model
    def get_company_setting(self, company_id, key, default=None):
        """Get company setting value"""
        setting = self.get_setting_by_key(company_id, key)
        
        if setting:
            return setting.get_value()
        else:
            return default
    
    @api.model
    def get_branch_settings(self, branch_id, category=None):
        """Get settings for a specific branch"""
        domain = [('scope', '=', 'branch'), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_location_settings(self, location_id, category=None):
        """Get settings for a specific location"""
        domain = [('scope', '=', 'location'), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_user_settings(self, user_id, category=None):
        """Get settings for a specific user"""
        domain = [('scope', '=', 'user'), ('is_active', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        return self.search(domain)
    
    @api.model
    def get_settings_by_category(self, category):
        """Get settings by category"""
        return self.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_system_settings(self):
        """Get all system settings"""
        return self.search([
            ('is_system_setting', '=', True),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_custom_settings(self):
        """Get all custom settings"""
        return self.search([
            ('is_system_setting', '=', False),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_setting_analytics(self):
        """Get setting analytics"""
        total_settings = self.search_count([])
        active_settings = self.search_count([('is_active', '=', True)])
        system_settings = self.search_count([('is_system_setting', '=', True)])
        custom_settings = self.search_count([('is_system_setting', '=', False)])
        
        return {
            'total_settings': total_settings,
            'active_settings': active_settings,
            'system_settings': system_settings,
            'custom_settings': custom_settings,
            'inactive_settings': total_settings - active_settings,
            'active_percentage': (active_settings / total_settings * 100) if total_settings > 0 else 0,
        }
    
    @api.constrains('key')
    def _check_key(self):
        """Validate setting key"""
        for setting in self:
            if setting.key:
                # Check for duplicate keys for the same company
                existing = self.search([
                    ('key', '=', setting.key),
                    ('company_id', '=', setting.company_id.id),
                    ('id', '!=', setting.id),
                ])
                if existing:
                    raise ValidationError(_('Setting key must be unique for each company'))
    
    @api.constrains('depends_on')
    def _check_dependencies(self):
        """Validate setting dependencies"""
        for setting in self:
            if setting in setting.depends_on:
                raise ValidationError(_('Setting cannot depend on itself'))
            
            # Check for circular dependencies
            for dep in setting.depends_on:
                if setting in dep.required_by:
                    raise ValidationError(_('Circular dependency detected'))
    
    def action_activate(self):
        """Activate setting"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate setting"""
        self.is_active = False
        return True
    
    def action_reset_to_default(self):
        """Reset setting to default value"""
        if self.default_value:
            self.value = self.default_value
        return True
    
    def action_duplicate(self):
        """Duplicate setting"""
        self.ensure_one()
        
        new_setting = self.copy({
            'name': f'{self.name} (Copy)',
            'key': f'{self.key}_copy',
            'is_system_setting': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Setting',
            'res_model': 'company.settings',
            'res_id': new_setting.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_setting(self):
        """Export setting definition"""
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
    
    def action_import_setting(self, setting_data):
        """Import setting definition"""
        self.ensure_one()
        
        self.write(setting_data)
        return True