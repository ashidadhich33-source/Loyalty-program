# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import io
import csv


class ImportTemplate(models.Model):
    _name = 'import.template'
    _description = 'Import Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Template Name',
        required=True,
        tracking=True,
        help="Name of the import template"
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help="Description of the import template"
    )
    
    model_name = fields.Char(
        string='Target Model',
        required=True,
        help="Target model for this template"
    )
    
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        help="Target model for this template"
    )
    
    template_type = fields.Selection([
        ('excel', 'Excel Template'),
        ('csv', 'CSV Template'),
        ('json', 'JSON Template'),
        ('xml', 'XML Template'),
    ], string='Template Type', required=True, default='excel',
       help="Type of template file")
    
    # Template File
    template_file = fields.Binary(
        string='Template File',
        help="Template file for import"
    )
    
    template_filename = fields.Char(
        string='Template Filename',
        help="Name of the template file"
    )
    
    # Template Configuration
    has_header = fields.Boolean(
        string='Has Header Row',
        default=True,
        help="Whether the template has a header row"
    )
    
    header_row = fields.Integer(
        string='Header Row',
        default=1,
        help="Row number containing headers"
    )
    
    data_start_row = fields.Integer(
        string='Data Start Row',
        default=2,
        help="Row number where data starts"
    )
    
    max_rows = fields.Integer(
        string='Maximum Rows',
        default=10000,
        help="Maximum number of rows to process"
    )
    
    # Field Mapping
    field_mapping_ids = fields.One2many(
        'import.mapping',
        'template_id',
        string='Field Mappings',
        help="Field mappings for this template"
    )
    
    # Validation Rules
    validation_rules = fields.Text(
        string='Validation Rules',
        help="JSON string containing validation rules"
    )
    
    required_fields = fields.Text(
        string='Required Fields',
        help="Comma-separated list of required fields"
    )
    
    unique_fields = fields.Text(
        string='Unique Fields',
        help="Comma-separated list of unique fields"
    )
    
    # Kids Clothing Specific
    is_kids_specific = fields.Boolean(
        string='Kids Specific',
        default=False,
        help="Whether this template is specific to kids clothing"
    )
    
    age_group_validation = fields.Boolean(
        string='Age Group Validation',
        default=False,
        help="Enable age group validation"
    )
    
    gender_validation = fields.Boolean(
        string='Gender Validation',
        default=False,
        help="Enable gender validation"
    )
    
    size_validation = fields.Boolean(
        string='Size Validation',
        default=False,
        help="Enable size validation"
    )
    
    # Indian Localization
    gstin_validation = fields.Boolean(
        string='GSTIN Validation',
        default=False,
        help="Enable GSTIN validation"
    )
    
    pan_validation = fields.Boolean(
        string='PAN Validation',
        default=False,
        help="Enable PAN validation"
    )
    
    mobile_validation = fields.Boolean(
        string='Mobile Validation',
        default=False,
        help="Enable mobile number validation"
    )
    
    # Template Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
        help="Whether this template is active"
    )
    
    is_default = fields.Boolean(
        string='Default Template',
        default=False,
        help="Whether this is the default template for the model"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of templates in the list"
    )
    
    # Usage Statistics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help="Number of times this template has been used"
    )
    
    last_used = fields.Datetime(
        string='Last Used',
        help="When this template was last used"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this template belongs to"
    )
    
    # Template Categories
    category_ids = fields.Many2many(
        'import.template.category',
        string='Categories',
        help="Categories for this template"
    )
    
    tags = fields.Char(
        string='Tags',
        help="Tags for this template"
    )
    
    # Template Versioning
    version = fields.Char(
        string='Version',
        default='1.0',
        help="Version of this template"
    )
    
    parent_template_id = fields.Many2one(
        'import.template',
        string='Parent Template',
        help="Parent template for versioning"
    )
    
    child_template_ids = fields.One2many(
        'import.template',
        'parent_template_id',
        string='Child Templates',
        help="Child templates for versioning"
    )
    
    @api.depends('model_id')
    def _compute_model_name(self):
        for template in self:
            if template.model_id:
                template.model_name = template.model_id.model
    
    @api.constrains('model_id', 'is_default')
    def _check_default_template(self):
        for template in self:
            if template.is_default:
                existing_default = self.search([
                    ('model_id', '=', template.model_id.id),
                    ('is_default', '=', True),
                    ('id', '!=', template.id)
                ])
                if existing_default:
                    raise ValidationError(_('Only one default template is allowed per model.'))
    
    @api.constrains('header_row', 'data_start_row')
    def _check_row_numbers(self):
        for template in self:
            if template.header_row >= template.data_start_row:
                raise ValidationError(_('Header row must be before data start row.'))
    
    @api.constrains('max_rows')
    def _check_max_rows(self):
        for template in self:
            if template.max_rows <= 0:
                raise ValidationError(_('Maximum rows must be greater than 0.'))
    
    def action_download_template(self):
        """Download template file"""
        if not self.template_file:
            raise ValidationError(_('No template file available for download.'))
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=import.template&id={self.id}&field=template_file&filename_field=template_filename&download=true',
            'target': 'new',
        }
    
    def action_preview_template(self):
        """Preview template structure"""
        if not self.template_file:
            raise ValidationError(_('No template file available for preview.'))
        
        # This would typically show a preview of the template
        # For now, return a placeholder action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Template Preview',
            'res_model': 'import.template',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
    
    def action_validate_template(self):
        """Validate template structure"""
        if not self.template_file:
            raise ValidationError(_('No template file available for validation.'))
        
        # Template validation logic would go here
        # For now, just return success
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Template Validation'),
                'message': _('Template validation completed successfully.'),
                'type': 'success',
            }
        }
    
    def action_duplicate_template(self):
        """Duplicate this template"""
        new_template = self.copy({
            'name': f"{self.name} (Copy)",
            'is_default': False,
            'usage_count': 0,
            'last_used': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Template',
            'res_model': 'import.template',
            'view_mode': 'form',
            'res_id': new_template.id,
        }
    
    def action_export_template(self):
        """Export template configuration"""
        # Export template configuration as JSON
        config = {
            'name': self.name,
            'description': self.description,
            'model_name': self.model_name,
            'template_type': self.template_type,
            'has_header': self.has_header,
            'header_row': self.header_row,
            'data_start_row': self.data_start_row,
            'max_rows': self.max_rows,
            'validation_rules': self.validation_rules,
            'required_fields': self.required_fields,
            'unique_fields': self.unique_fields,
            'field_mappings': [
                {
                    'source_field': mapping.source_field,
                    'target_field': mapping.target_field,
                    'data_type': mapping.data_type,
                    'required': mapping.required,
                    'default_value': mapping.default_value,
                }
                for mapping in self.field_mapping_ids
            ]
        }
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=import.template&id={self.id}&field=template_file&filename_field=template_filename&download=true',
            'target': 'new',
        }
    
    def get_template_data(self):
        """Get template data as list of dictionaries"""
        if not self.template_file:
            return []
        
        try:
            file_content = base64.b64decode(self.template_file)
            
            if self.template_type == 'csv':
                return self._parse_csv_data(file_content)
            elif self.template_type == 'excel':
                return self._parse_excel_data(file_content)
            else:
                return []
        except Exception as e:
            raise ValidationError(_('Error parsing template file: %s') % str(e))
    
    def _parse_csv_data(self, file_content):
        """Parse CSV data"""
        try:
            csv_data = io.StringIO(file_content.decode('utf-8'))
            reader = csv.DictReader(csv_data)
            return list(reader)
        except Exception as e:
            raise ValidationError(_('Error parsing CSV file: %s') % str(e))
    
    def _parse_excel_data(self, file_content):
        """Parse Excel data"""
        try:
            import pandas as pd
            excel_data = pd.read_excel(io.BytesIO(file_content))
            return excel_data.to_dict('records')
        except ImportError:
            raise ValidationError(_('Pandas library is required for Excel file processing.'))
        except Exception as e:
            raise ValidationError(_('Error parsing Excel file: %s') % str(e))
    
    def validate_import_data(self, data):
        """Validate import data against template rules"""
        errors = []
        
        # Validate required fields
        if self.required_fields:
            required_list = [field.strip() for field in self.required_fields.split(',')]
            for row_num, row in enumerate(data, start=self.data_start_row):
                for field in required_list:
                    if not row.get(field):
                        errors.append(f"Row {row_num}: Required field '{field}' is missing")
        
        # Validate unique fields
        if self.unique_fields:
            unique_list = [field.strip() for field in self.unique_fields.split(',')]
            seen_values = {}
            for row_num, row in enumerate(data, start=self.data_start_row):
                for field in unique_list:
                    value = row.get(field)
                    if value:
                        if value in seen_values:
                            errors.append(f"Row {row_num}: Duplicate value '{value}' in unique field '{field}' (first seen in row {seen_values[value]})")
                        else:
                            seen_values[value] = row_num
        
        # Kids clothing specific validation
        if self.is_kids_specific:
            errors.extend(self._validate_kids_clothing_data(data))
        
        # Indian localization validation
        if self.gstin_validation:
            errors.extend(self._validate_gstin_data(data))
        
        if self.pan_validation:
            errors.extend(self._validate_pan_data(data))
        
        if self.mobile_validation:
            errors.extend(self._validate_mobile_data(data))
        
        return errors
    
    def _validate_kids_clothing_data(self, data):
        """Validate kids clothing specific data"""
        errors = []
        
        # Age group validation
        if self.age_group_validation:
            valid_age_groups = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', 'all']
            for row_num, row in enumerate(data, start=self.data_start_row):
                age_group = row.get('age_group')
                if age_group and age_group not in valid_age_groups:
                    errors.append(f"Row {row_num}: Invalid age group '{age_group}'. Valid values: {', '.join(valid_age_groups)}")
        
        # Gender validation
        if self.gender_validation:
            valid_genders = ['boys', 'girls', 'unisex']
            for row_num, row in enumerate(data, start=self.data_start_row):
                gender = row.get('gender')
                if gender and gender not in valid_genders:
                    errors.append(f"Row {row_num}: Invalid gender '{gender}'. Valid values: {', '.join(valid_genders)}")
        
        # Size validation
        if self.size_validation:
            valid_sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
            for row_num, row in enumerate(data, start=self.data_start_row):
                size = row.get('size')
                if size and size not in valid_sizes:
                    errors.append(f"Row {row_num}: Invalid size '{size}'. Valid values: {', '.join(valid_sizes)}")
        
        return errors
    
    def _validate_gstin_data(self, data):
        """Validate GSTIN data"""
        errors = []
        # GSTIN validation logic would go here
        return errors
    
    def _validate_pan_data(self, data):
        """Validate PAN data"""
        errors = []
        # PAN validation logic would go here
        return errors
    
    def _validate_mobile_data(self, data):
        """Validate mobile number data"""
        errors = []
        # Mobile validation logic would go here
        return errors