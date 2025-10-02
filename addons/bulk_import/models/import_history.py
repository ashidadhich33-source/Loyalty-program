# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImportHistory(models.Model):
    _name = 'import.history'
    _description = 'Import History'
    _order = 'import_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this history record"
    )
    
    # Import Job Reference
    import_job_id = fields.Many2one(
        'import.job',
        string='Import Job',
        required=True,
        ondelete='cascade',
        help="Import job this history record belongs to"
    )
    
    template_id = fields.Many2one(
        'import.template',
        string='Template',
        related='import_job_id.template_id',
        store=True,
        help="Template used for this import"
    )
    
    model_name = fields.Char(
        string='Target Model',
        related='import_job_id.model_name',
        store=True,
        help="Target model for this import"
    )
    
    # Import Details
    import_date = fields.Datetime(
        string='Import Date',
        required=True,
        default=fields.Datetime.now,
        help="Date and time of the import"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='User',
        related='import_job_id.user_id',
        store=True,
        help="User who performed the import"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='import_job_id.company_id',
        store=True,
        help="Company this import belongs to"
    )
    
    # Import Results
    total_records = fields.Integer(
        string='Total Records',
        help="Total number of records processed"
    )
    
    success_records = fields.Integer(
        string='Success Records',
        help="Number of records successfully processed"
    )
    
    error_records = fields.Integer(
        string='Error Records',
        help="Number of records with errors"
    )
    
    warning_records = fields.Integer(
        string='Warning Records',
        help="Number of records with warnings"
    )
    
    # Performance Metrics
    duration = fields.Float(
        string='Duration (seconds)',
        help="Duration of the import in seconds"
    )
    
    records_per_second = fields.Float(
        string='Records per Second',
        compute='_compute_records_per_second',
        help="Number of records processed per second"
    )
    
    # File Information
    file_name = fields.Char(
        string='File Name',
        related='import_job_id.import_filename',
        store=True,
        help="Name of the imported file"
    )
    
    file_size = fields.Float(
        string='File Size (KB)',
        related='import_job_id.file_size',
        store=True,
        help="Size of the imported file in KB"
    )
    
    # Import Status
    status = fields.Selection([
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('partial', 'Partial Success'),
    ], string='Status', required=True, default='completed',
       help="Status of the import")
    
    # Error Information
    error_summary = fields.Text(
        string='Error Summary',
        help="Summary of errors encountered during import"
    )
    
    error_details = fields.Text(
        string='Error Details',
        help="Detailed error information"
    )
    
    # Success Information
    success_summary = fields.Text(
        string='Success Summary',
        help="Summary of successful imports"
    )
    
    # Import Options
    import_options = fields.Text(
        string='Import Options',
        help="Options used for this import"
    )
    
    # Data Quality Metrics
    data_quality_score = fields.Float(
        string='Data Quality Score (%)',
        compute='_compute_data_quality_score',
        help="Data quality score for this import"
    )
    
    completeness_score = fields.Float(
        string='Completeness Score (%)',
        help="Completeness score for this import"
    )
    
    accuracy_score = fields.Float(
        string='Accuracy Score (%)',
        help="Accuracy score for this import"
    )
    
    consistency_score = fields.Float(
        string='Consistency Score (%)',
        help="Consistency score for this import"
    )
    
    # Business Impact
    business_impact = fields.Selection([
        ('low', 'Low Impact'),
        ('medium', 'Medium Impact'),
        ('high', 'High Impact'),
        ('critical', 'Critical Impact'),
    ], string='Business Impact', default='medium',
       help="Business impact of this import")
    
    cost_savings = fields.Float(
        string='Cost Savings',
        digits='Product Price',
        help="Cost savings from this import"
    )
    
    time_savings = fields.Float(
        string='Time Savings (hours)',
        help="Time savings from this import in hours"
    )
    
    # Related Records
    created_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Created Records',
        domain=[('action', '=', 'create')],
        help="Records created by this import"
    )
    
    updated_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Updated Records',
        domain=[('action', '=', 'update')],
        help="Records updated by this import"
    )
    
    error_record_ids = fields.One2many(
        'import.record',
        'import_job_id',
        string='Error Records',
        domain=[('state', '=', 'error')],
        help="Records with errors in this import"
    )
    
    @api.depends('import_job_id.name', 'import_date')
    def _compute_display_name(self):
        for history in self:
            history.display_name = f"{history.import_job_id.name} - {history.import_date.strftime('%Y-%m-%d %H:%M')}"
    
    @api.depends('total_records', 'duration')
    def _compute_records_per_second(self):
        for history in self:
            if history.duration > 0:
                history.records_per_second = history.total_records / history.duration
            else:
                history.records_per_second = 0.0
    
    @api.depends('success_records', 'total_records')
    def _compute_data_quality_score(self):
        for history in self:
            if history.total_records > 0:
                history.data_quality_score = (history.success_records / history.total_records) * 100
            else:
                history.data_quality_score = 0.0
    
    def action_view_import_job(self):
        """View the import job"""
        action = self.env.ref('bulk_import.action_import_job').read()[0]
        action['res_id'] = self.import_job_id.id
        action['view_mode'] = 'form'
        return action
    
    def action_view_records(self):
        """View import records"""
        action = self.env.ref('bulk_import.action_import_record').read()[0]
        action['domain'] = [('import_job_id', '=', self.import_job_id.id)]
        return action
    
    def action_view_errors(self):
        """View import errors"""
        action = self.env.ref('bulk_import.action_import_record').read()[0]
        action['domain'] = [('import_job_id', '=', self.import_job_id.id), ('state', '=', 'error')]
        return action
    
    def action_export_results(self):
        """Export import results"""
        # Export results logic would go here
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=import.history&id={self.id}&field=import_results&download=true',
            'target': 'new',
        }
    
    def action_retry_import(self):
        """Retry the import"""
        if self.status in ['completed', 'cancelled']:
            raise ValidationError(_('Cannot retry completed or cancelled imports.'))
        
        # Create new import job based on this history
        new_job = self.env['import.job'].create({
            'name': f"{self.import_job_id.name} (Retry)",
            'template_id': self.template_id.id,
            'import_file': self.import_job_id.import_file,
            'import_filename': self.import_job_id.import_filename,
            'user_id': self.env.user.id,
            'company_id': self.env.company.id,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Retry Import',
            'res_model': 'import.job',
            'view_mode': 'form',
            'res_id': new_job.id,
        }
    
    def action_analyze_errors(self):
        """Analyze import errors"""
        if not self.error_records:
            raise ValidationError(_('No errors to analyze.'))
        
        # Error analysis logic would go here
        return {
            'type': 'ir.actions.act_window',
            'name': 'Error Analysis',
            'res_model': 'import.record',
            'view_mode': 'tree,form',
            'domain': [('import_job_id', '=', self.import_job_id.id), ('state', '=', 'error')],
            'context': {'group_by': 'error_type'},
        }
    
    def action_generate_report(self):
        """Generate import report"""
        # Report generation logic would go here
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Report',
            'res_model': 'import.statistics',
            'view_mode': 'form',
            'context': {'default_import_history_id': self.id},
        }


class ImportRecord(models.Model):
    _name = 'import.record'
    _description = 'Import Record'
    _order = 'create_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this record"
    )
    
    # Import Job Reference
    import_job_id = fields.Many2one(
        'import.job',
        string='Import Job',
        required=True,
        ondelete='cascade',
        help="Import job this record belongs to"
    )
    
    # Record Information
    record_id = fields.Integer(
        string='Record ID',
        help="ID of the created/updated record"
    )
    
    model_name = fields.Char(
        string='Model Name',
        required=True,
        help="Name of the model"
    )
    
    action = fields.Selection([
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ], string='Action', required=True, default='create',
       help="Action performed on the record")
    
    # Record Status
    state = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('skipped', 'Skipped'),
    ], string='Status', required=True, default='success',
       help="Status of the record processing")
    
    # Record Data
    data = fields.Text(
        string='Data',
        help="JSON string containing the record data"
    )
    
    original_data = fields.Text(
        string='Original Data',
        help="Original data from the import file"
    )
    
    # Error Information
    error_message = fields.Text(
        string='Error Message',
        help="Error message if processing failed"
    )
    
    error_type = fields.Char(
        string='Error Type',
        help="Type of error encountered"
    )
    
    error_code = fields.Char(
        string='Error Code',
        help="Error code for categorization"
    )
    
    # Processing Information
    processing_time = fields.Float(
        string='Processing Time (seconds)',
        help="Time taken to process this record"
    )
    
    validation_errors = fields.Text(
        string='Validation Errors',
        help="Validation errors for this record"
    )
    
    # Record Details
    record_name = fields.Char(
        string='Record Name',
        help="Name of the record (if available)"
    )
    
    record_code = fields.Char(
        string='Record Code',
        help="Code of the record (if available)"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='import_job_id.company_id',
        store=True,
        help="Company this record belongs to"
    )
    
    @api.depends('model_name', 'action', 'record_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.model_name} - {record.action} - {record.record_id or 'New'}"
    
    def action_view_record(self):
        """View the actual record"""
        if not self.record_id:
            raise ValidationError(_('No record to view.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Record',
            'res_model': self.model_name,
            'view_mode': 'form',
            'res_id': self.record_id,
        }
    
    def action_retry_record(self):
        """Retry processing this record"""
        if self.state != 'error':
            raise ValidationError(_('Can only retry records with errors.'))
        
        # Retry logic would go here
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Record Retry'),
                'message': _('Record retry initiated.'),
                'type': 'info',
            }
        }
    
    def action_view_error_details(self):
        """View error details"""
        if self.state != 'error':
            raise ValidationError(_('No errors to view.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Error Details',
            'res_model': 'import.record',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }