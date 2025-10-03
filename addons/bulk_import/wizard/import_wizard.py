#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Import Wizard
=================================

Wizard for bulk import operations.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ImportWizard(BaseModel):
    """Wizard for bulk import operations"""
    
    _name = 'import.wizard'
    _description = 'Import Wizard'
    _table = 'import_wizard'
    
    # Basic Information
    name = CharField(
        string='Wizard Name',
        size=100,
        default='Bulk Import Wizard',
        help='Name of the import wizard'
    )
    
    # Template Selection
    template_id = Many2OneField(
        'import.template',
        string='Import Template',
        required=True,
        help='Select import template'
    )
    
    # File Upload
    import_file = CharField(
        string='Import File',
        size=255,
        help='Path to import file'
    )
    
    import_data = TextField(
        string='Import Data',
        help='Raw import data'
    )
    
    # Import Settings
    batch_size = IntegerField(
        string='Batch Size',
        default=100,
        help='Number of records to process in each batch'
    )
    
    skip_errors = BooleanField(
        string='Skip Errors',
        default=True,
        help='Skip records with errors and continue'
    )
    
    update_existing = BooleanField(
        string='Update Existing',
        default=False,
        help='Update existing records instead of creating new ones'
    )
    
    validate_data = BooleanField(
        string='Validate Data',
        default=True,
        help='Validate data before importing'
    )
    
    # Preview Data
    preview_data = TextField(
        string='Preview Data',
        help='Preview of data to be imported'
    )
    
    show_preview = BooleanField(
        string='Show Preview',
        default=False,
        help='Show data preview before importing'
    )
    
    # Status
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('preview', 'Preview'),
            ('ready', 'Ready to Import'),
            ('importing', 'Importing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='draft',
        help='Current state of the wizard'
    )
    
    # Results
    import_job_id = Many2OneField(
        'import.job',
        string='Import Job',
        help='Created import job'
    )
    
    def action_load_template(self):
        """Load template and prepare for import"""
        for wizard in self:
            if not wizard.template_id:
                raise ValidationError("Please select a template")
            
            # Load template configuration
            template = wizard.template_id
            wizard.batch_size = template.batch_size
            wizard.validate_data = True
            
            # Generate preview if data is available
            if wizard.import_data:
                wizard.action_preview_data()
            
            wizard.state = 'ready'
    
    def action_preview_data(self):
        """Preview import data"""
        for wizard in self:
            if not wizard.import_data:
                raise ValidationError("No data to preview")
            
            # Parse and preview data
            preview = self._parse_preview_data(wizard.import_data, wizard.template_id)
            wizard.preview_data = preview
            wizard.show_preview = True
            wizard.state = 'preview'
    
    def action_start_import(self):
        """Start the import process"""
        for wizard in self:
            if not wizard.template_id or not wizard.import_data:
                raise ValidationError("Template and data are required")
            
            # Create import job
            job_vals = {
                'name': f"Import Job - {wizard.template_id.name}",
                'description': f"Bulk import using {wizard.template_id.name}",
                'template_id': wizard.template_id.id,
                'import_data': wizard.import_data,
                'batch_size': wizard.batch_size,
                'skip_errors': wizard.skip_errors,
                'update_existing': wizard.update_existing
            }
            
            job = self.env['import.job'].create(job_vals)
            wizard.import_job_id = job.id
            
            # Start import
            job.action_start_import()
            
            wizard.state = 'importing'
    
    def action_view_job(self):
        """View the created import job"""
        for wizard in self:
            if not wizard.import_job_id:
                raise ValidationError("No import job created")
            
            return {
                'type': 'ocean.actions.act_window',
                'name': f'Import Job - {wizard.import_job_id.name}',
                'res_model': 'import.job',
                'res_id': wizard.import_job_id.id,
                'view_mode': 'form',
                'target': 'current'
            }
    
    def action_view_results(self):
        """View import results"""
        for wizard in self:
            if not wizard.import_job_id:
                raise ValidationError("No import job created")
            
            return wizard.import_job_id.action_view_results()
    
    def _parse_preview_data(self, data, template):
        """Parse and format preview data"""
        import json
        
        # Parse data based on template type
        if template.template_type == 'csv':
            parsed_data = self._parse_csv_preview(data)
        elif template.template_type == 'json':
            parsed_data = self._parse_json_preview(data)
        else:
            parsed_data = [{'error': 'Preview not supported for this format'}]
        
        # Format for display
        preview_lines = []
        for i, record in enumerate(parsed_data[:10]):  # Show first 10 records
            preview_lines.append(f"Record {i+1}: {json.dumps(record, indent=2)}")
        
        if len(parsed_data) > 10:
            preview_lines.append(f"... and {len(parsed_data) - 10} more records")
        
        return '\n'.join(preview_lines)
    
    def _parse_csv_preview(self, data):
        """Parse CSV data for preview"""
        import csv
        from io import StringIO
        
        csv_data = []
        reader = csv.DictReader(StringIO(data))
        for row in reader:
            csv_data.append(dict(row))
        
        return csv_data
    
    def _parse_json_preview(self, data):
        """Parse JSON data for preview"""
        import json
        return json.loads(data)
    
    def action_reset(self):
        """Reset wizard to draft state"""
        for wizard in self:
            wizard.state = 'draft'
            wizard.import_data = ''
            wizard.preview_data = ''
            wizard.show_preview = False
            wizard.import_job_id = False