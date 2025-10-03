#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Import Template Model
=========================================

Template management for bulk import operations.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ImportTemplate(BaseModel):
    """Import templates for different data types"""
    
    _name = 'import.template'
    _description = 'Import Template'
    _table = 'import_template'
    _order = 'name'
    
    # Basic Information
    name = CharField(
        string='Template Name',
        size=100,
        required=True,
        help='Name of the import template'
    )
    
    description = TextField(
        string='Description',
        help='Description of the template'
    )
    
    # Template Configuration
    model_name = CharField(
        string='Target Model',
        size=100,
        required=True,
        help='Model to import data into'
    )
    
    template_type = SelectionField(
        string='Template Type',
        selection=[
            ('excel', 'Excel (.xlsx)'),
            ('csv', 'CSV (.csv)'),
            ('json', 'JSON (.json)'),
            ('xml', 'XML (.xml)')
        ],
        default='excel',
        help='Type of template file'
    )
    
    # Template File
    template_file = CharField(
        string='Template File',
        size=255,
        help='Path to template file'
    )
    
    template_content = TextField(
        string='Template Content',
        help='Template file content'
    )
    
    # Field Mapping
    field_mapping = TextField(
        string='Field Mapping',
        help='JSON mapping of columns to model fields'
    )
    
    # Validation Rules
    validation_rules = TextField(
        string='Validation Rules',
        help='JSON validation rules for imported data'
    )
    
    # Template Properties
    has_header = BooleanField(
        string='Has Header',
        default=True,
        help='Whether template has header row'
    )
    
    skip_empty_rows = BooleanField(
        string='Skip Empty Rows',
        default=True,
        help='Whether to skip empty rows'
    )
    
    max_rows = IntegerField(
        string='Max Rows',
        default=1000,
        help='Maximum number of rows to process'
    )
    
    batch_size = IntegerField(
        string='Batch Size',
        default=100,
        help='Number of records to process in each batch'
    )
    
    # Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this template is active'
    )
    
    is_default = BooleanField(
        string='Default Template',
        default=False,
        help='Whether this is the default template for the model'
    )
    
    # Usage Statistics
    usage_count = IntegerField(
        string='Usage Count',
        default=0,
        help='Number of times this template has been used'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='When this template was last used'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'field_mapping' not in vals:
            vals['field_mapping'] = '{}'
        if 'validation_rules' not in vals:
            vals['validation_rules'] = '{}'
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update usage statistics"""
        result = super().write(vals)
        
        # Update usage count if template is used
        if 'usage_count' in vals:
            self.last_used = self.env['datetime'].now()
        
        return result
    
    def generate_template_file(self):
        """Generate template file for download"""
        import json
        
        # Get model fields
        model_fields = self._get_model_fields()
        
        # Create template data
        template_data = {
            'model': self.model_name,
            'fields': model_fields,
            'validation_rules': json.loads(self.validation_rules or '{}'),
            'field_mapping': json.loads(self.field_mapping or '{}')
        }
        
        # Generate file content based on type
        if self.template_type == 'excel':
            return self._generate_excel_template(template_data)
        elif self.template_type == 'csv':
            return self._generate_csv_template(template_data)
        elif self.template_type == 'json':
            return self._generate_json_template(template_data)
        elif self.template_type == 'xml':
            return self._generate_xml_template(template_data)
        
        return None
    
    def _get_model_fields(self):
        """Get fields for the target model"""
        # This would integrate with the ORM to get model fields
        # For now, return common fields
        return [
            {'name': 'name', 'type': 'char', 'required': True},
            {'name': 'code', 'type': 'char', 'required': False},
            {'name': 'description', 'type': 'text', 'required': False},
            {'name': 'is_active', 'type': 'boolean', 'required': False}
        ]
    
    def _generate_excel_template(self, template_data):
        """Generate Excel template"""
        # This would use openpyxl or xlsxwriter to create Excel file
        # For now, return placeholder
        return "Excel template content"
    
    def _generate_csv_template(self, template_data):
        """Generate CSV template"""
        # Create CSV header
        headers = [field['name'] for field in template_data['fields']]
        return ','.join(headers)
    
    def _generate_json_template(self, template_data):
        """Generate JSON template"""
        import json
        return json.dumps(template_data, indent=2)
    
    def _generate_xml_template(self, template_data):
        """Generate XML template"""
        # Create XML template
        xml_content = f"<{self.model_name}>\n"
        for field in template_data['fields']:
            xml_content += f"  <{field['name']}></{field['name']}>\n"
        xml_content += f"</{self.model_name}>"
        return xml_content
    
    def validate_import_data(self, data):
        """Validate imported data against template rules"""
        import json
        
        validation_rules = json.loads(self.validation_rules or '{}')
        errors = []
        
        for row_num, row_data in enumerate(data, 1):
            row_errors = self._validate_row(row_data, validation_rules, row_num)
            errors.extend(row_errors)
        
        return errors
    
    def _validate_row(self, row_data, validation_rules, row_num):
        """Validate a single row of data"""
        errors = []
        
        # Check required fields
        for field_name, field_config in validation_rules.get('required_fields', {}).items():
            if field_config.get('required', False) and not row_data.get(field_name):
                errors.append(f"Row {row_num}: {field_name} is required")
        
        # Check field types
        for field_name, field_config in validation_rules.get('field_types', {}).items():
            if field_name in row_data:
                value = row_data[field_name]
                expected_type = field_config.get('type')
                
                if expected_type == 'integer' and not str(value).isdigit():
                    errors.append(f"Row {row_num}: {field_name} must be an integer")
                elif expected_type == 'float' and not str(value).replace('.', '').isdigit():
                    errors.append(f"Row {row_num}: {field_name} must be a number")
                elif expected_type == 'boolean' and value not in ['True', 'False', 'true', 'false', '1', '0']:
                    errors.append(f"Row {row_num}: {field_name} must be True/False")
        
        return errors
    
    def action_download_template(self):
        """Action to download template file"""
        template_content = self.generate_template_file()
        
        return {
            'type': 'ocean.actions.act_url',
            'url': f'/bulk_import/download_template/{self.id}',
            'target': 'new'
        }
    
    def action_import_data(self):
        """Action to start import process"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Import Data - {self.name}',
            'res_model': 'import.job',
            'view_mode': 'form',
            'context': {'default_template_id': self.id}
        }