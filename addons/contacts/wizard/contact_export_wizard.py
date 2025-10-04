# -*- coding: utf-8 -*-
"""
Contact Export Wizard
=====================

Wizard for exporting contacts to external formats.
"""

from ocean import fields, models


class ContactExportWizard(models.TransientModel):
    """Wizard for exporting contacts."""
    
    _name = 'contact.export.wizard'
    _description = 'Contact Export Wizard'
    
    name = fields.Char(string='Export Name', required=True)
    export_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File'),
        ('json', 'JSON File'),
    ], string='Export Type', required=True, default='csv')
    
    contact_ids = fields.Many2many(
        'res.partner',
        string='Contacts to Export',
        required=True
    )
    
    include_fields = fields.Selection([
        ('basic', 'Basic Fields Only'),
        ('detailed', 'Detailed Fields'),
        ('all', 'All Fields'),
    ], string='Include Fields', required=True, default='basic')
    
    def action_export(self):
        """Export contacts to file."""
        # Implementation would go here
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }