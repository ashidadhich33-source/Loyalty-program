# -*- coding: utf-8 -*-
"""
Contact Import Wizard
=====================

Wizard for importing contacts from external sources.
"""

from ocean import fields, models


class ContactImportWizard(models.TransientModel):
    """Wizard for importing contacts."""
    
    _name = 'contact.import.wizard'
    _description = 'Contact Import Wizard'
    
    name = fields.Char(string='Import Name', required=True)
    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File'),
        ('json', 'JSON File'),
    ], string='Import Type', required=True, default='csv')
    
    file_data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name')
    
    import_mode = fields.Selection([
        ('create', 'Create New'),
        ('update', 'Update Existing'),
        ('create_update', 'Create or Update'),
    ], string='Import Mode', required=True, default='create')
    
    def action_import(self):
        """Import contacts from file."""
        # Implementation would go here
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }