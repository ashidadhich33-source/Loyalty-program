#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Import History Model
========================================

Import history tracking for bulk import operations.
"""

import logging
from datetime import datetime
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ImportHistory(BaseModel):
    """Import history for tracking import operations"""
    
    _name = 'import.history'
    _description = 'Import History'
    _table = 'import_history'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='History Name',
        size=100,
        required=True,
        help='Name of the import history record'
    )
    
    job_id = Many2OneField(
        'import.job',
        string='Import Job',
        required=True,
        help='Related import job'
    )
    
    # Import Details
    model_name = CharField(
        string='Target Model',
        size=100,
        help='Model that was imported to'
    )
    
    record_id = IntegerField(
        string='Record ID',
        help='ID of the created/updated record'
    )
    
    record_name = CharField(
        string='Record Name',
        size=100,
        help='Name of the created/updated record'
    )
    
    # Operation Details
    operation_type = SelectionField(
        string='Operation',
        selection=[
            ('create', 'Create'),
            ('update', 'Update'),
            ('skip', 'Skip'),
            ('error', 'Error')
        ],
        help='Type of operation performed'
    )
    
    # Data Details
    original_data = TextField(
        string='Original Data',
        help='Original data from import file'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Data after processing and validation'
    )
    
    # Error Information
    error_message = TextField(
        string='Error Message',
        help='Error message if operation failed'
    )
    
    error_details = TextField(
        string='Error Details',
        help='Detailed error information'
    )
    
    # Validation Results
    validation_passed = BooleanField(
        string='Validation Passed',
        default=True,
        help='Whether validation passed for this record'
    )
    
    validation_errors = TextField(
        string='Validation Errors',
        help='Validation errors for this record'
    )
    
    # Status
    is_successful = BooleanField(
        string='Successful',
        default=False,
        help='Whether the operation was successful'
    )
    
    # Timestamps
    process_time = DateTimeField(
        string='Process Time',
        default=datetime.now,
        help='When this record was processed'
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
        if 'name' not in vals:
            vals['name'] = f"Import History - {vals.get('record_name', 'Unknown')}"
        
        return super().create(vals)
    
    def action_view_record(self):
        """View the imported record"""
        if not self.record_id or not self.model_name:
            return {}
        
        return {
            'type': 'ocean.actions.act_window',
            'name': f'View {self.record_name}',
            'res_model': self.model_name,
            'res_id': self.record_id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def action_retry_import(self):
        """Retry importing this record"""
        if not self.job_id or self.job_id.state != 'draft':
            raise ValidationError("Cannot retry import. Job must be in draft state.")
        
        # Add record back to job for retry
        import_data = self.original_data
        if import_data:
            # Parse and add to job data
            self.job_id.import_data += '\n' + import_data
    
    def action_rollback(self):
        """Rollback this import record"""
        if not self.is_successful or not self.record_id:
            raise ValidationError("Cannot rollback unsuccessful or non-existent records")
        
        try:
            # Delete the created record
            model = self.env[self.model_name]
            record = model.browse(self.record_id)
            if record.exists():
                record.unlink()
                
                # Update history
                self.operation_type = 'rollback'
                self.is_successful = False
                self.error_message = 'Record rolled back'
                
        except Exception as e:
            raise ValidationError(f"Failed to rollback record: {str(e)}")
    
    def get_import_statistics(self):
        """Get statistics for this import history"""
        job = self.job_id
        
        stats = {
            'total_records': job.total_records,
            'successful_records': job.successful_records,
            'failed_records': job.failed_records,
            'success_rate': (job.successful_records / job.total_records * 100) if job.total_records > 0 else 0,
            'duration': (job.end_time - job.start_time) if job.end_time and job.start_time else None,
            'average_time_per_record': None
        }
        
        if stats['duration'] and job.total_records > 0:
            stats['average_time_per_record'] = stats['duration'].total_seconds() / job.total_records
        
        return stats
    
    def action_export_errors(self):
        """Export error records to CSV"""
        if not self.error_message:
            raise ValidationError("No errors to export")
        
        # Create CSV with error details
        csv_content = f"Record,Error Message,Error Details\n"
        csv_content += f"{self.record_name},{self.error_message},{self.error_details}\n"
        
        return {
            'type': 'ocean.actions.act_url',
            'url': f'/bulk_import/export_errors/{self.id}',
            'target': 'new'
        }