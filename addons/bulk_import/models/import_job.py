#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Import Job Model
====================================

Import job management for bulk import operations.
"""

import logging
from datetime import datetime
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ImportJob(BaseModel):
    """Import job for bulk data import"""
    
    _name = 'import.job'
    _description = 'Import Job'
    _table = 'import_job'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Job Name',
        size=100,
        required=True,
        help='Name of the import job'
    )
    
    description = TextField(
        string='Description',
        help='Description of the import job'
    )
    
    # Job Configuration
    template_id = Many2OneField(
        'import.template',
        string='Template',
        required=True,
        help='Import template to use'
    )
    
    import_file = CharField(
        string='Import File',
        size=255,
        help='Path to the import file'
    )
    
    import_data = TextField(
        string='Import Data',
        help='Raw import data'
    )
    
    # Job Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Current status of the import job'
    )
    
    # Progress Tracking
    total_records = IntegerField(
        string='Total Records',
        default=0,
        help='Total number of records to process'
    )
    
    processed_records = IntegerField(
        string='Processed Records',
        default=0,
        help='Number of records processed'
    )
    
    successful_records = IntegerField(
        string='Successful Records',
        default=0,
        help='Number of successfully imported records'
    )
    
    failed_records = IntegerField(
        string='Failed Records',
        default=0,
        help='Number of failed records'
    )
    
    progress_percentage = FloatField(
        string='Progress %',
        digits=(5, 2),
        default=0.0,
        help='Import progress percentage'
    )
    
    # Error Handling
    error_log = TextField(
        string='Error Log',
        help='Detailed error log for failed imports'
    )
    
    validation_errors = TextField(
        string='Validation Errors',
        help='Data validation errors'
    )
    
    # Job Settings
    batch_size = IntegerField(
        string='Batch Size',
        default=100,
        help='Number of records to process in each batch'
    )
    
    skip_errors = BooleanField(
        string='Skip Errors',
        default=True,
        help='Whether to skip records with errors'
    )
    
    update_existing = BooleanField(
        string='Update Existing',
        default=False,
        help='Whether to update existing records'
    )
    
    # Results
    import_summary = TextField(
        string='Import Summary',
        help='Summary of import results'
    )
    
    # Timestamps
    start_time = DateTimeField(
        string='Start Time',
        help='When the import job started'
    )
    
    end_time = DateTimeField(
        string='End Time',
        help='When the import job completed'
    )
    
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
        if 'name' not in vals and 'template_id' in vals:
            template = self.env['import.template'].browse(vals['template_id'])
            vals['name'] = f"Import Job - {template.name}"
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update progress"""
        result = super().write(vals)
        
        # Update progress percentage
        if 'processed_records' in vals or 'total_records' in vals:
            self._update_progress()
        
        return result
    
    def _update_progress(self):
        """Update progress percentage"""
        for record in self:
            if record.total_records > 0:
                record.progress_percentage = (record.processed_records / record.total_records) * 100
            else:
                record.progress_percentage = 0.0
    
    def action_start_import(self):
        """Start the import process"""
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft jobs can be started")
            
            record.state = 'running'
            record.start_time = datetime.now()
            
            # Start import process in background
            self._process_import(record)
    
    def action_cancel_import(self):
        """Cancel the import process"""
        for record in self:
            if record.state == 'running':
                record.state = 'cancelled'
                record.end_time = datetime.now()
    
    def action_retry_import(self):
        """Retry failed import"""
        for record in self:
            if record.state == 'failed':
                record.state = 'draft'
                record.failed_records = 0
                record.error_log = ''
                record.validation_errors = ''
    
    def _process_import(self, job):
        """Process the import job"""
        try:
            # Parse import data
            data = self._parse_import_data(job.import_data, job.template_id)
            job.total_records = len(data)
            
            # Validate data
            validation_errors = job.template_id.validate_import_data(data)
            if validation_errors:
                job.validation_errors = '\n'.join(validation_errors)
                if not job.skip_errors:
                    job.state = 'failed'
                    job.end_time = datetime.now()
                    return
            
            # Process data in batches
            batch_size = job.batch_size
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                self._process_batch(job, batch)
                
                # Update progress
                job.processed_records = min(i + batch_size, len(data))
                job._update_progress()
            
            # Complete job
            job.state = 'completed'
            job.end_time = datetime.now()
            job._generate_summary()
            
        except Exception as e:
            job.state = 'failed'
            job.end_time = datetime.now()
            job.error_log = str(e)
            logger.error(f"Import job {job.id} failed: {e}")
    
    def _parse_import_data(self, import_data, template):
        """Parse import data based on template type"""
        if template.template_type == 'csv':
            return self._parse_csv_data(import_data)
        elif template.template_type == 'excel':
            return self._parse_excel_data(import_data)
        elif template.template_type == 'json':
            return self._parse_json_data(import_data)
        elif template.template_type == 'xml':
            return self._parse_xml_data(import_data)
        
        return []
    
    def _parse_csv_data(self, data):
        """Parse CSV data"""
        import csv
        from io import StringIO
        
        csv_data = []
        reader = csv.DictReader(StringIO(data))
        for row in reader:
            csv_data.append(dict(row))
        
        return csv_data
    
    def _parse_excel_data(self, data):
        """Parse Excel data"""
        # This would use openpyxl to parse Excel files
        # For now, return empty list
        return []
    
    def _parse_json_data(self, data):
        """Parse JSON data"""
        import json
        return json.loads(data)
    
    def _parse_xml_data(self, data):
        """Parse XML data"""
        # This would use xml.etree.ElementTree to parse XML
        # For now, return empty list
        return []
    
    def _process_batch(self, job, batch):
        """Process a batch of records"""
        model_name = job.template_id.model_name
        model = self.env[model_name]
        
        for record_data in batch:
            try:
                # Create or update record
                if job.update_existing:
                    # Update existing record
                    existing = model.search([('name', '=', record_data.get('name'))])
                    if existing:
                        existing.write(record_data)
                    else:
                        model.create(record_data)
                else:
                    # Create new record
                    model.create(record_data)
                
                job.successful_records += 1
                
            except Exception as e:
                job.failed_records += 1
                error_msg = f"Record {record_data}: {str(e)}"
                if job.error_log:
                    job.error_log += '\n' + error_msg
                else:
                    job.error_log = error_msg
                
                if not job.skip_errors:
                    raise e
    
    def _generate_summary(self):
        """Generate import summary"""
        for job in self:
            summary = f"""
Import Summary:
- Total Records: {job.total_records}
- Successful: {job.successful_records}
- Failed: {job.failed_records}
- Success Rate: {(job.successful_records / job.total_records * 100):.2f}%
- Duration: {job.end_time - job.start_time if job.end_time and job.start_time else 'N/A'}
            """.strip()
            
            job.import_summary = summary
    
    def action_view_results(self):
        """View import results"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Import Results - {self.name}',
            'res_model': 'import.history',
            'view_mode': 'tree,form',
            'domain': [('job_id', '=', self.id)],
            'context': {'default_job_id': self.id}
        }