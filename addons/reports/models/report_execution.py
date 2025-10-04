#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Report Execution Model
==========================================

Report execution tracking and history.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    DateTimeField, IntegerField, FloatField, BooleanField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class ReportExecution(BaseModel, KidsClothingMixin):
    """Report Execution Model"""
    
    _name = 'report.execution'
    _description = 'Report Execution'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Execution Name', size=200)
    template_id = Many2OneField('report.template', 'Report Template', required=True)
    user_id = Many2OneField('users.user', 'User', required=True)
    
    # Execution Details
    status = SelectionField([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('cancelled', 'Cancelled'),
    ], 'Status', default='draft')
    
    filters = TextField('Filters Applied', help='JSON string of filters')
    parameters = TextField('Parameters', help='Additional parameters')
    
    # Results
    data = TextField('Report Data', help='Generated report data')
    record_count = IntegerField('Record Count', default=0)
    execution_time = FloatField('Execution Time (seconds)', digits=(10, 3))
    
    # Output Files
    output_file = CharField('Output File Path', size=500)
    file_size = IntegerField('File Size (bytes)', default=0)
    output_format = SelectionField([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
        ('json', 'JSON'),
    ], 'Output Format')
    
    # Error Handling
    error_message = TextField('Error Message')
    error_traceback = TextField('Error Traceback')
    
    # Scheduling
    scheduled_execution = BooleanField('Scheduled Execution', default=False)
    schedule_id = Many2OneField('report.schedule', 'Schedule')
    
    # Access and Sharing
    is_shared = BooleanField('Shared', default=False)
    shared_with_ids = One2ManyField('users.user', 'shared_execution_ids', 'Shared With')
    
    def execute_report(self):
        """Execute the report"""
        import time
        start_time = time.time()
        
        try:
            self.write({'status': 'running'})
            
            # Execute the report template
            result = self.template_id.generate_report(
                filters=self.filters,
                user_id=self.user_id
            )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Update execution record
            self.write({
                'status': 'completed',
                'execution_time': execution_time,
                'data': str(result.data) if hasattr(result, 'data') else str(result),
                'record_count': result.record_count if hasattr(result, 'record_count') else 0,
            })
            
            return True
            
        except Exception as e:
            import traceback
            execution_time = time.time() - start_time
            
            self.write({
                'status': 'error',
                'execution_time': execution_time,
                'error_message': str(e),
                'error_traceback': traceback.format_exc(),
            })
            return False
    
    def export_report(self, format='pdf'):
        """Export report to specified format"""
        try:
            if self.status != 'completed':
                raise ValueError("Report must be completed before export")
            
            # Generate export file based on format
            if format == 'pdf':
                return self._export_to_pdf()
            elif format == 'excel':
                return self._export_to_excel()
            elif format == 'csv':
                return self._export_to_csv()
            elif format == 'html':
                return self._export_to_html()
            elif format == 'json':
                return self._export_to_json()
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.write({
                'error_message': f"Export error: {str(e)}",
            })
            raise e
    
    def _export_to_pdf(self):
        """Export report to PDF"""
        # Implementation for PDF export
        return {'file_path': '/tmp/report.pdf', 'format': 'pdf'}
    
    def _export_to_excel(self):
        """Export report to Excel"""
        # Implementation for Excel export
        return {'file_path': '/tmp/report.xlsx', 'format': 'excel'}
    
    def _export_to_csv(self):
        """Export report to CSV"""
        # Implementation for CSV export
        return {'file_path': '/tmp/report.csv', 'format': 'csv'}
    
    def _export_to_html(self):
        """Export report to HTML"""
        # Implementation for HTML export
        return {'file_path': '/tmp/report.html', 'format': 'html'}
    
    def _export_to_json(self):
        """Export report to JSON"""
        # Implementation for JSON export
        return {'file_path': '/tmp/report.json', 'format': 'json'}
    
    def share_report(self, user_ids):
        """Share report with users"""
        self.write({
            'is_shared': True,
            'shared_with_ids': [(6, 0, user_ids)],
        })
    
    def get_execution_summary(self):
        """Get execution summary"""
        return {
            'id': self.id,
            'name': self.name,
            'template': self.template_id.name,
            'status': self.status,
            'execution_time': self.execution_time,
            'record_count': self.record_count,
            'create_date': self.create_date,
            'user': self.user_id.name,
        }