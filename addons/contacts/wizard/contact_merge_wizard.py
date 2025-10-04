# -*- coding: utf-8 -*-
"""
Contact Merge Wizard
====================

Wizard for merging duplicate contacts.
"""

from ocean import fields, models


class ContactMergeWizard(models.TransientModel):
    """Wizard for merging contacts."""
    
    _name = 'contact.merge.wizard'
    _description = 'Contact Merge Wizard'
    
    name = fields.Char(string='Merge Name', required=True)
    
    master_contact_id = fields.Many2one(
        'res.partner',
        string='Master Contact',
        required=True
    )
    
    duplicate_contact_ids = fields.Many2many(
        'res.partner',
        string='Duplicate Contacts',
        required=True
    )
    
    merge_fields = fields.Selection([
        ('name', 'Name'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('address', 'Address'),
        ('notes', 'Notes'),
    ], string='Fields to Merge', required=True, default='name')
    
    def action_merge(self):
        """Merge duplicate contacts."""
        # Implementation would go here
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }