# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImportMapping(models.Model):
    _name = 'import.mapping'
    _description = 'Import Field Mapping'
    _order = 'sequence, source_field'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this mapping"
    )
    
    template_id = fields.Many2one(
        'import.template',
        string='Template',
        required=True,
        ondelete='cascade',
        help="Template this mapping belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of mappings in the template"
    )
    
    # Source Field
    source_field = fields.Char(
        string='Source Field',
        required=True,
        help="Field name in the import file"
    )
    
    source_field_label = fields.Char(
        string='Source Field Label',
        help="Human-readable label for source field"
    )
    
    # Target Field
    target_field = fields.Char(
        string='Target Field',
        required=True,
        help="Field name in the target model"
    )
    
    target_field_label = fields.Char(
        string='Target Field Label',
        help="Human-readable label for target field"
    )
    
    # Data Type and Transformation
    data_type = fields.Selection([
        ('char', 'Text'),
        ('text', 'Long Text'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('selection', 'Selection'),
        ('many2one', 'Many2one'),
        ('many2many', 'Many2many'),
        ('one2many', 'One2many'),
    ], string='Data Type', required=True, default='char',
       help="Data type of the target field")
    
    # Field Properties
    required = fields.Boolean(
        string='Required',
        default=False,
        help="Whether this field is required"
    )
    
    default_value = fields.Char(
        string='Default Value',
        help="Default value if source field is empty"
    )
    
    # Data Transformation
    transformation_rule = fields.Selection([
        ('none', 'No Transformation'),
        ('uppercase', 'Uppercase'),
        ('lowercase', 'Lowercase'),
        ('title', 'Title Case'),
        ('trim', 'Trim Whitespace'),
        ('replace', 'Replace Text'),
        ('split', 'Split Text'),
        ('join', 'Join Text'),
        ('format', 'Format Text'),
        ('validate', 'Validate Format'),
    ], string='Transformation Rule', default='none',
       help="Data transformation rule to apply")
    
    transformation_value = fields.Char(
        string='Transformation Value',
        help="Value for transformation (e.g., replacement text, format pattern)"
    )
    
    # Validation Rules
    validation_rule = fields.Selection([
        ('none', 'No Validation'),
        ('email', 'Email Format'),
        ('phone', 'Phone Number'),
        ('url', 'URL Format'),
        ('numeric', 'Numeric Only'),
        ('alpha', 'Alphabetic Only'),
        ('alphanumeric', 'Alphanumeric Only'),
        ('length', 'Length Check'),
        ('range', 'Range Check'),
        ('pattern', 'Pattern Match'),
        ('custom', 'Custom Validation'),
    ], string='Validation Rule', default='none',
       help="Validation rule to apply")
    
    validation_value = fields.Char(
        string='Validation Value',
        help="Value for validation (e.g., min length, pattern)"
    )
    
    validation_message = fields.Char(
        string='Validation Message',
        help="Custom error message for validation failure"
    )
    
    # Kids Clothing Specific
    is_kids_specific = fields.Boolean(
        string='Kids Specific',
        default=False,
        help="Whether this mapping is specific to kids clothing"
    )
    
    age_group_validation = fields.Boolean(
        string='Age Group Validation',
        default=False,
        help="Enable age group validation for this field"
    )
    
    gender_validation = fields.Boolean(
        string='Gender Validation',
        default=False,
        help="Enable gender validation for this field"
    )
    
    size_validation = fields.Boolean(
        string='Size Validation',
        default=False,
        help="Enable size validation for this field"
    )
    
    # Indian Localization
    gstin_validation = fields.Boolean(
        string='GSTIN Validation',
        default=False,
        help="Enable GSTIN validation for this field"
    )
    
    pan_validation = fields.Boolean(
        string='PAN Validation',
        default=False,
        help="Enable PAN validation for this field"
    )
    
    mobile_validation = fields.Boolean(
        string='Mobile Validation',
        default=False,
        help="Enable mobile number validation for this field"
    )
    
    # Related Field Mapping
    related_field = fields.Char(
        string='Related Field',
        help="Related field for many2one, many2many, one2many fields"
    )
    
    related_model = fields.Char(
        string='Related Model',
        help="Related model for many2one, many2many, one2many fields"
    )
    
    search_field = fields.Char(
        string='Search Field',
        help="Field to search for related records"
    )
    
    create_if_not_found = fields.Boolean(
        string='Create if Not Found',
        default=False,
        help="Create related record if not found"
    )
    
    # Field Mapping Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this mapping is active"
    )
    
    is_mapped = fields.Boolean(
        string='Mapped',
        default=False,
        help="Whether this field is mapped"
    )
    
    # Usage Statistics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help="Number of times this mapping has been used"
    )
    
    success_count = fields.Integer(
        string='Success Count',
        default=0,
        help="Number of successful mappings"
    )
    
    error_count = fields.Integer(
        string='Error Count',
        default=0,
        help="Number of failed mappings"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this mapping belongs to"
    )
    
    @api.depends('source_field', 'target_field')
    def _compute_display_name(self):
        for mapping in self:
            mapping.display_name = f"{mapping.source_field} → {mapping.target_field}"
    
    @api.constrains('source_field', 'target_field')
    def _check_field_mapping(self):
        for mapping in self:
            if mapping.source_field == mapping.target_field:
                raise ValidationError(_('Source field and target field cannot be the same.'))
    
    @api.constrains('validation_rule', 'validation_value')
    def _check_validation_rule(self):
        for mapping in self:
            if mapping.validation_rule in ['length', 'range', 'pattern'] and not mapping.validation_value:
                raise ValidationError(_('Validation value is required for the selected validation rule.'))
    
    def action_test_mapping(self):
        """Test this field mapping"""
        # Test mapping logic would go here
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Mapping Test'),
                'message': _('Field mapping test completed successfully.'),
                'type': 'success',
            }
        }
    
    def action_validate_mapping(self):
        """Validate this field mapping"""
        errors = []
        
        # Check if target field exists in the model
        if self.template_id.model_id:
            model_fields = self.env[self.template_id.model_name]._fields
            if self.target_field not in model_fields:
                errors.append(f"Target field '{self.target_field}' does not exist in model '{self.template_id.model_name}'")
        
        # Check data type compatibility
        if self.template_id.model_id and self.target_field in model_fields:
            field = model_fields[self.target_field]
            if not self._is_data_type_compatible(field.type, self.data_type):
                errors.append(f"Data type '{self.data_type}' is not compatible with field type '{field.type}'")
        
        if errors:
            raise ValidationError(_('Mapping validation failed:\n%s') % '\n'.join(errors))
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Mapping Validation'),
                'message': _('Field mapping validation completed successfully.'),
                'type': 'success',
            }
        }
    
    def _is_data_type_compatible(self, field_type, data_type):
        """Check if data type is compatible with field type"""
        compatibility_map = {
            'char': ['char', 'text'],
            'text': ['char', 'text'],
            'integer': ['integer'],
            'float': ['float', 'integer'],
            'boolean': ['boolean'],
            'date': ['date'],
            'datetime': ['datetime', 'date'],
            'selection': ['selection', 'char'],
            'many2one': ['many2one'],
            'many2many': ['many2many'],
            'one2many': ['one2many'],
        }
        
        return data_type in compatibility_map.get(field_type, [])
    
    def transform_value(self, value):
        """Transform value according to transformation rule"""
        if not value or self.transformation_rule == 'none':
            return value
        
        if self.transformation_rule == 'uppercase':
            return str(value).upper()
        elif self.transformation_rule == 'lowercase':
            return str(value).lower()
        elif self.transformation_rule == 'title':
            return str(value).title()
        elif self.transformation_rule == 'trim':
            return str(value).strip()
        elif self.transformation_rule == 'replace':
            if self.transformation_value:
                return str(value).replace(self.transformation_value, '')
        elif self.transformation_rule == 'split':
            if self.transformation_value:
                return str(value).split(self.transformation_value)
        elif self.transformation_rule == 'join':
            if self.transformation_value and isinstance(value, list):
                return self.transformation_value.join(value)
        elif self.transformation_rule == 'format':
            if self.transformation_value:
                return self.transformation_value.format(value)
        
        return value
    
    def validate_value(self, value):
        """Validate value according to validation rule"""
        if not value or self.validation_rule == 'none':
            return True, None
        
        error_message = self.validation_message or f"Validation failed for field {self.source_field}"
        
        if self.validation_rule == 'email':
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, str(value)):
                return False, error_message
        
        elif self.validation_rule == 'phone':
            import re
            pattern = r'^[\+]?[1-9][\d]{0,15}$'
            if not re.match(pattern, str(value).replace(' ', '').replace('-', '')):
                return False, error_message
        
        elif self.validation_rule == 'url':
            import re
            pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
            if not re.match(pattern, str(value)):
                return False, error_message
        
        elif self.validation_rule == 'numeric':
            if not str(value).replace('.', '').replace('-', '').isdigit():
                return False, error_message
        
        elif self.validation_rule == 'alpha':
            if not str(value).isalpha():
                return False, error_message
        
        elif self.validation_rule == 'alphanumeric':
            if not str(value).isalnum():
                return False, error_message
        
        elif self.validation_rule == 'length':
            if self.validation_value:
                try:
                    min_length, max_length = map(int, self.validation_value.split('-'))
                    if not (min_length <= len(str(value)) <= max_length):
                        return False, error_message
                except ValueError:
                    pass
        
        elif self.validation_rule == 'range':
            if self.validation_value:
                try:
                    min_val, max_val = map(float, self.validation_value.split('-'))
                    if not (min_val <= float(value) <= max_val):
                        return False, error_message
                except (ValueError, TypeError):
                    pass
        
        elif self.validation_rule == 'pattern':
            if self.validation_value:
                import re
                if not re.match(self.validation_value, str(value)):
                    return False, error_message
        
        # Kids clothing specific validation
        if self.is_kids_specific:
            if self.age_group_validation:
                valid_age_groups = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', 'all']
                if str(value) not in valid_age_groups:
                    return False, f"Invalid age group '{value}'. Valid values: {', '.join(valid_age_groups)}"
            
            if self.gender_validation:
                valid_genders = ['boys', 'girls', 'unisex']
                if str(value) not in valid_genders:
                    return False, f"Invalid gender '{value}'. Valid values: {', '.join(valid_genders)}"
            
            if self.size_validation:
                valid_sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
                if str(value) not in valid_sizes:
                    return False, f"Invalid size '{value}'. Valid values: {', '.join(valid_sizes)}"
        
        # Indian localization validation
        if self.gstin_validation:
            if not self._validate_gstin(str(value)):
                return False, f"Invalid GSTIN format: {value}"
        
        if self.pan_validation:
            if not self._validate_pan(str(value)):
                return False, f"Invalid PAN format: {value}"
        
        if self.mobile_validation:
            if not self._validate_mobile(str(value)):
                return False, f"Invalid mobile number format: {value}"
        
        return True, None
    
    def _validate_gstin(self, gstin):
        """Validate GSTIN format"""
        import re
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        return bool(re.match(pattern, gstin))
    
    def _validate_pan(self, pan):
        """Validate PAN format"""
        import re
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan))
    
    def _validate_mobile(self, mobile):
        """Validate mobile number format"""
        import re
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, mobile))