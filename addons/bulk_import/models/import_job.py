# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import json
from datetime import datetime


class ImportJob(models.Model):
    _name = 'import.job'
    _description = 'Import Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Job Name',
        required=True,
        tracking=True,
        help="Name of the import job"
    )
    
    description = fields.Text(
        string='Description',
        help="Description of the import job"
    )
    
    # Job Configuration
    template_id = fields.Many2one(
        'import.template',
        string='Template',
        required=True,
        ondelete='cascade',
        help="Template used for this import job"
    )
    
    model_name = fields.Char(
        string='Target Model',
        related='template_id.model_name',
        store=True,
        help="Target model for this import job"
    )
    
    # Import File
    import_file = fields.Binary(
        string='Import File',
        required=True,
        help="File to import"
    )
    
    import_filename = fields.Char(
        string='Import Filename',
        help="Name of the import file"
    )
    
    file_size = fields.Float(
        string='File Size (KB)',
        compute='_compute_file_size',
        help="Size of the import file in KB"
    )
    
    # Job Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validating', 'Validating'),
        ('validated', 'Validated'),
        ('importing', 'Importing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True,
       help="Current status of the import job")
    
    # Progress Tracking
    total_rows = fields.Integer(
        string='Total Rows',
        help="Total number of rows to process"
    )
    
    processed_rows = fields.Integer(
        string='Processed Rows',
        default=0,
        help="Number of rows processed"
    )
    
    success_rows = fields.Integer(
        string='Success Rows',
        default=0,
        help="Number of rows successfully processed"
    )
    
    error_rows = fields.Integer(
        string='Error Rows',
        default=0,
        help="Number of rows with errors"
    )
    
    progress_percentage = fields.Float(
        string='Progress (%)',
        compute='_compute_progress_percentage',
        help="Progress percentage of the import job"
    )
    
    # Import Results
    import_results = fields.Text(
        string='Import Results',
        help="JSON string containing import results"
    )
    
    error_log = fields.Text(
        string='Error Log',
        help="Detailed error log for failed imports"
    )
    
    warning_log = fields.Text(
        string='Warning Log',
        help="Warning log for imports with warnings"
    )
    
    # Job Statistics
    start_time = fields.Datetime(
        string='Start Time',
        help="When the import job started"
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help="When the import job ended"
    )
    
    duration = fields.Float(
        string='Duration (seconds)',
        compute='_compute_duration',
        help="Duration of the import job in seconds"
    )
    
    # User and Company
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        help="User who created this import job"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this import job belongs to"
    )
    
    # Import Options
    import_options = fields.Text(
        string='Import Options',
        help="JSON string containing import options"
    )
    
    skip_validation = fields.Boolean(
        string='Skip Validation',
        default=False,
        help="Skip data validation during import"
    )
    
    update_existing = fields.Boolean(
        string='Update Existing',
        default=False,
        help="Update existing records instead of creating new ones"
    )
    
    create_missing = fields.Boolean(
        string='Create Missing',
        default=True,
        help="Create missing related records"
    )
    
    # Batch Processing
    batch_size = fields.Integer(
        string='Batch Size',
        default=100,
        help="Number of records to process in each batch"
    )
    
    batch_count = fields.Integer(
        string='Batch Count',
        compute='_compute_batch_count',
        help="Total number of batches"
    )
    
    current_batch = fields.Integer(
        string='Current Batch',
        default=0,
        help="Current batch being processed"
    )
    
    # Error Handling
    max_errors = fields.Integer(
        string='Max Errors',
        default=100,
        help="Maximum number of errors before stopping import"
    )
    
    stop_on_error = fields.Boolean(
        string='Stop on Error',
        default=False,
        help="Stop import on first error"
    )
    
    # Scheduling
    scheduled_date = fields.Datetime(
        string='Scheduled Date',
        help="When to start the import job"
    )
    
    is_scheduled = fields.Boolean(
        string='Scheduled',
        default=False,
        help="Whether this job is scheduled"
    )
    
    # Related Records
    created_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Created Records',
        domain=[('action', '=', 'create')],
        help="Records created by this import job"
    )
    
    updated_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Updated Records',
        domain=[('action', '=', 'update')],
        help="Records updated by this import job"
    )
    
    error_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Error Records',
        domain=[('state', '=', 'error')],
        help="Records with errors in this import job"
    )
    
    @api.depends('import_file')
    def _compute_file_size(self):
        for job in self:
            if job.import_file:
                file_content = base64.b64decode(job.import_file)
                job.file_size = len(file_content) / 1024  # Convert to KB
            else:
                job.file_size = 0.0
    
    @api.depends('total_rows', 'processed_rows')
    def _compute_progress_percentage(self):
        for job in self:
            if job.total_rows > 0:
                job.progress_percentage = (job.processed_rows / job.total_rows) * 100
            else:
                job.progress_percentage = 0.0
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for job in self:
            if job.start_time and job.end_time:
                delta = job.end_time - job.start_time
                job.duration = delta.total_seconds()
            else:
                job.duration = 0.0
    
    @api.depends('total_rows', 'batch_size')
    def _compute_batch_count(self):
        for job in self:
            if job.total_rows > 0 and job.batch_size > 0:
                job.batch_count = (job.total_rows + job.batch_size - 1) // job.batch_size
            else:
                job.batch_count = 0
    
    @api.constrains('batch_size')
    def _check_batch_size(self):
        for job in self:
            if job.batch_size <= 0:
                raise ValidationError(_('Batch size must be greater than 0.'))
    
    @api.constrains('max_errors')
    def _check_max_errors(self):
        for job in self:
            if job.max_errors < 0:
                raise ValidationError(_('Max errors cannot be negative.'))
    
    def action_start_import(self):
        """Start the import job"""
        if self.state != 'draft':
            raise ValidationError(_('Import job can only be started from draft state.'))
        
        self.write({
            'state': 'validating',
            'start_time': fields.Datetime.now(),
        })
        
        # Start validation in background
        self._validate_import_data()
        
        return True
    
    def action_cancel_import(self):
        """Cancel the import job"""
        if self.state in ['completed', 'failed', 'cancelled']:
            raise ValidationError(_('Cannot cancel import job in current state.'))
        
        self.write({
            'state': 'cancelled',
            'end_time': fields.Datetime.now(),
        })
        
        return True
    
    def action_retry_import(self):
        """Retry the import job"""
        if self.state not in ['failed', 'cancelled']:
            raise ValidationError(_('Can only retry failed or cancelled import jobs.'))
        
        self.write({
            'state': 'draft',
            'processed_rows': 0,
            'success_rows': 0,
            'error_rows': 0,
            'current_batch': 0,
            'start_time': False,
            'end_time': False,
            'import_results': False,
            'error_log': False,
            'warning_log': False,
        })
        
        return True
    
    def action_view_results(self):
        """View import results"""
        action = self.env.ref('bulk_import.action_import_record').read()[0]
        action['domain'] = [('import_job_id', '=', self.id)]
        action['context'] = {'default_import_job_id': self.id}
        return action
    
    def action_view_errors(self):
        """View import errors"""
        action = self.env.ref('bulk_import.action_import_record').read()[0]
        action['domain'] = [('import_job_id', '=', self.id), ('state', '=', 'error')]
        action['context'] = {'default_import_job_id': self.id}
        return action
    
    def _validate_import_data(self):
        """Validate import data"""
        try:
            # Parse import data
            data = self._parse_import_data()
            self.total_rows = len(data)
            
            # Validate data using template
            errors = self.template_id.validate_import_data(data)
            
            if errors:
                self.write({
                    'state': 'failed',
                    'error_log': '\n'.join(errors),
                    'end_time': fields.Datetime.now(),
                })
            else:
                self.write({
                    'state': 'validated',
                })
                # Start import process
                self._start_import_process(data)
                
        except Exception as e:
            self.write({
                'state': 'failed',
                'error_log': str(e),
                'end_time': fields.Datetime.now(),
            })
    
    def _parse_import_data(self):
        """Parse import data from file"""
        if not self.import_file:
            raise ValidationError(_('No import file available.'))
        
        file_content = base64.b64decode(self.import_file)
        
        if self.template_id.template_type == 'csv':
            return self._parse_csv_data(file_content)
        elif self.template_id.template_type == 'excel':
            return self._parse_excel_data(file_content)
        else:
            raise ValidationError(_('Unsupported file type.'))
    
    def _parse_csv_data(self, file_content):
        """Parse CSV data"""
        import csv
        import io
        
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
    
    def _start_import_process(self, data):
        """Start the import process"""
        self.write({
            'state': 'importing',
        })
        
        # Process data in batches
        batch_size = self.batch_size
        total_batches = self.batch_count
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(data))
            batch_data = data[start_idx:end_idx]
            
            self._process_batch(batch_data, batch_num + 1)
            
            # Update progress
            self.write({
                'processed_rows': end_idx,
                'current_batch': batch_num + 1,
            })
            
            # Check for errors
            if self.error_rows >= self.max_errors and self.stop_on_error:
                self.write({
                    'state': 'failed',
                    'end_time': fields.Datetime.now(),
                })
                return
        
        # Import completed
        self.write({
            'state': 'completed',
            'end_time': fields.Datetime.now(),
        })
    
    def _process_batch(self, batch_data, batch_num):
        """Process a batch of data"""
        for row_data in batch_data:
            try:
                # Create or update record
                record = self._create_or_update_record(row_data)
                
                # Create import record
                self.env['import.record'].create({
                    'import_job_id': self.id,
                    'record_id': record.id,
                    'model_name': self.model_name,
                    'action': 'create' if not self.update_existing else 'update',
                    'state': 'success',
                    'data': json.dumps(row_data),
                })
                
                self.success_rows += 1
                
            except Exception as e:
                # Create error record
                self.env['import.record'].create({
                    'import_job_id': self.id,
                    'model_name': self.model_name,
                    'action': 'create' if not self.update_existing else 'update',
                    'state': 'error',
                    'data': json.dumps(row_data),
                    'error_message': str(e),
                })
                
                self.error_rows += 1
    
    def _create_or_update_record(self, row_data):
        """Create or update a record"""
        # Map data using template field mappings
        mapped_data = self._map_data(row_data)
        
        if self.update_existing:
            # Find existing record
            domain = self._build_search_domain(mapped_data)
            existing_record = self.env[self.model_name].search(domain, limit=1)
            
            if existing_record:
                existing_record.write(mapped_data)
                return existing_record
        
        # Create new record
        return self.env[self.model_name].create(mapped_data)
    
    def _map_data(self, row_data):
        """Map row data to model fields"""
        mapped_data = {}
        
        for mapping in self.template_id.field_mapping_ids:
            source_value = row_data.get(mapping.source_field)
            
            if source_value:
                # Transform data if needed
                if mapping.data_type == 'integer':
                    source_value = int(source_value)
                elif mapping.data_type == 'float':
                    source_value = float(source_value)
                elif mapping.data_type == 'boolean':
                    source_value = source_value.lower() in ['true', '1', 'yes', 'on']
                
                mapped_data[mapping.target_field] = source_value
            elif mapping.required:
                if mapping.default_value:
                    mapped_data[mapping.target_field] = mapping.default_value
                else:
                    raise ValidationError(_('Required field %s is missing') % mapping.target_field)
        
        return mapped_data
    
    def _build_search_domain(self, mapped_data):
        """Build search domain for finding existing records"""
        domain = []
        
        # Use unique fields for search
        if self.template_id.unique_fields:
            unique_list = [field.strip() for field in self.template_id.unique_fields.split(',')]
            for field in unique_list:
                if field in mapped_data:
                    domain.append((field, '=', mapped_data[field]))
        
        return domain