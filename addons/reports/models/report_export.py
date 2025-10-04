#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Report Export Model
======================================

Report export functionality for various formats.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    DateTimeField, IntegerField, BooleanField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class ReportExport(BaseModel, KidsClothingMixin):
    """Report Export Model"""
    
    _name = 'report.export'
    _description = 'Report Export'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Export Name', required=True, size=200)
    execution_id = Many2OneField('report.execution', 'Report Execution', required=True)
    user_id = Many2OneField('users.user', 'Exported By', required=True)
    
    # Export Configuration
    export_format = SelectionField([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
        ('json', 'JSON'),
        ('xml', 'XML'),
    ], 'Export Format', required=True)
    
    # File Information
    file_path = CharField('File Path', size=500)
    file_name = CharField('File Name', size=200)
    file_size = IntegerField('File Size (bytes)', default=0)
    mime_type = CharField('MIME Type', size=100)
    
    # Export Settings
    include_header = BooleanField('Include Header', default=True)
    include_footer = BooleanField('Include Footer', default=True)
    page_size = SelectionField([
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
    ], 'Page Size', default='A4')
    
    orientation = SelectionField([
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ], 'Orientation', default='portrait')
    
    # Export Status
    status = SelectionField([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ], 'Status', default='pending')
    
    progress = FloatField('Progress (%)', digits=(5, 2), default=0.0)
    error_message = TextField('Error Message')
    
    # Timing
    start_time = DateTimeField('Start Time')
    end_time = DateTimeField('End Time')
    duration = FloatField('Duration (seconds)', digits=(10, 3))
    
    # Download Tracking
    download_count = IntegerField('Download Count', default=0)
    last_download = DateTimeField('Last Download')
    expires_at = DateTimeField('Expires At')
    
    def export_report(self):
        """Export report to specified format"""
        import time
        start_time = time.time()
        
        try:
            self.write({
                'status': 'processing',
                'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'progress': 0.0,
            })
            
            # Get report data
            report_data = self.execution_id.data
            if not report_data:
                raise ValueError("No report data available for export")
            
            # Export based on format
            if self.export_format == 'pdf':
                result = self._export_to_pdf(report_data)
            elif self.export_format == 'excel':
                result = self._export_to_excel(report_data)
            elif self.export_format == 'csv':
                result = self._export_to_csv(report_data)
            elif self.export_format == 'html':
                result = self._export_to_html(report_data)
            elif self.export_format == 'json':
                result = self._export_to_json(report_data)
            elif self.export_format == 'xml':
                result = self._export_to_xml(report_data)
            else:
                raise ValueError(f"Unsupported export format: {self.export_format}")
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Update export record
            self.write({
                'status': 'completed',
                'progress': 100.0,
                'end_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration,
                'file_path': result.get('file_path', ''),
                'file_name': result.get('file_name', ''),
                'file_size': result.get('file_size', 0),
                'mime_type': result.get('mime_type', ''),
            })
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            
            self.write({
                'status': 'error',
                'end_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration,
                'error_message': str(e),
            })
            raise e
    
    def _export_to_pdf(self, data):
        """Export to PDF format"""
        # Implementation for PDF export
        # This would use a PDF library like ReportLab or WeasyPrint
        return {
            'file_path': '/tmp/report.pdf',
            'file_name': f"{self.name}.pdf",
            'file_size': 1024,
            'mime_type': 'application/pdf',
        }
    
    def _export_to_excel(self, data):
        """Export to Excel format"""
        # Implementation for Excel export
        # This would use openpyxl or xlsxwriter
        return {
            'file_path': '/tmp/report.xlsx',
            'file_name': f"{self.name}.xlsx",
            'file_size': 2048,
            'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }
    
    def _export_to_csv(self, data):
        """Export to CSV format"""
        # Implementation for CSV export
        import csv
        import json
        
        file_path = f"/tmp/{self.name}.csv"
        
        # Convert data to CSV format
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                data = [{'data': data}]
        
        if isinstance(data, list) and data:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys() if data else []
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if self.include_header:
                    writer.writeheader()
                
                for row in data:
                    writer.writerow(row)
        
        return {
            'file_path': file_path,
            'file_name': f"{self.name}.csv",
            'file_size': 512,
            'mime_type': 'text/csv',
        }
    
    def _export_to_html(self, data):
        """Export to HTML format"""
        # Implementation for HTML export
        return {
            'file_path': '/tmp/report.html',
            'file_name': f"{self.name}.html",
            'file_size': 1536,
            'mime_type': 'text/html',
        }
    
    def _export_to_json(self, data):
        """Export to JSON format"""
        # Implementation for JSON export
        import json
        
        file_path = f"/tmp/{self.name}.json"
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, default=str)
        
        return {
            'file_path': file_path,
            'file_name': f"{self.name}.json",
            'file_size': 768,
            'mime_type': 'application/json',
        }
    
    def _export_to_xml(self, data):
        """Export to XML format"""
        # Implementation for XML export
        return {
            'file_path': '/tmp/report.xml',
            'file_name': f"{self.name}.xml",
            'file_size': 1024,
            'mime_type': 'application/xml',
        }
    
    def get_download_url(self):
        """Get download URL for the exported file"""
        if self.status != 'completed':
            return None
        
        # Generate secure download URL
        return f"/reports/download/{self.id}"
    
    def record_download(self):
        """Record download event"""
        from datetime import datetime
        
        self.write({
            'download_count': self.download_count + 1,
            'last_download': datetime.now(),
        })
    
    def is_expired(self):
        """Check if export has expired"""
        if not self.expires_at:
            return False
        
        from datetime import datetime
        return datetime.now() > self.expires_at
    
    def cleanup_file(self):
        """Clean up exported file"""
        import os
        
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                self.write({'file_path': ''})
            except Exception as e:
                # Log error but don't raise
                pass
    
    def get_export_summary(self):
        """Get export summary"""
        return {
            'id': self.id,
            'name': self.name,
            'format': self.export_format,
            'status': self.status,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'progress': self.progress,
            'download_count': self.download_count,
            'create_date': self.create_date,
            'expires_at': self.expires_at,
            'is_expired': self.is_expired(),
        }