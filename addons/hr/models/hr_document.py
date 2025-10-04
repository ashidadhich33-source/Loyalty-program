# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrDocument(models.Model):
    _name = 'hr.document'
    _description = 'Employee Document'
    _order = 'name'

    # Basic Information
    name = fields.Char(
        string='Document Name',
        required=True
    )
    document_type = fields.Selection([
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('education_certificate', 'Education Certificate'),
        ('experience_certificate', 'Experience Certificate'),
        ('salary_certificate', 'Salary Certificate'),
        ('offer_letter', 'Offer Letter'),
        ('appointment_letter', 'Appointment Letter'),
        ('contract', 'Employment Contract'),
        ('nda', 'Non-Disclosure Agreement'),
        ('policy_acknowledgment', 'Policy Acknowledgment'),
        ('training_certificate', 'Training Certificate'),
        ('other', 'Other'),
    ], string='Document Type', required=True, default='other')
    
    # Employee Information
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        index=True
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='employee_id.company_id',
        store=True
    )
    
    # Document Details
    document_number = fields.Char(
        string='Document Number',
        help='Document reference number'
    )
    issue_date = fields.Date(
        string='Issue Date'
    )
    expiry_date = fields.Date(
        string='Expiry Date'
    )
    issuing_authority = fields.Char(
        string='Issuing Authority',
        help='Authority that issued this document'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Age group focus for this document')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this document')
    
    # Document Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ], string='Status', default='draft', tracking=True)
    
    # Additional Fields
    description = fields.Text(
        string='Description',
        help='Description of this document'
    )
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this document'
    )
    
    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for document in self:
            if document.expiry_date and document.issue_date and document.expiry_date < document.issue_date:
                raise ValidationError(_('Expiry date cannot be before issue date.'))
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.age_group_focus = self.employee_id.age_group_specialization
            self.season_specialization = self.employee_id.season_preference
    
    def action_submit(self):
        """Submit document for verification"""
        for document in self:
            if document.state != 'draft':
                raise UserError(_('Only draft documents can be submitted.'))
            document.state = 'submitted'
        return True
    
    def action_verify(self):
        """Verify document"""
        for document in self:
            if document.state != 'submitted':
                raise UserError(_('Only submitted documents can be verified.'))
            document.state = 'verified'
        return True
    
    def action_reject(self):
        """Reject document"""
        for document in self:
            if document.state != 'submitted':
                raise UserError(_('Only submitted documents can be rejected.'))
            document.state = 'rejected'
        return True
    
    def action_expire(self):
        """Mark document as expired"""
        for document in self:
            if document.state not in ['verified']:
                raise UserError(_('Only verified documents can be marked as expired.'))
            document.state = 'expired'
        return True
    
    def action_draft(self):
        """Set document to draft"""
        for document in self:
            document.state = 'draft'
        return True