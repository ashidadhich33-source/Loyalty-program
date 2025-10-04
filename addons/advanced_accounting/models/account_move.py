# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Journal Entries
========================================================

Journal entries management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    """Journal Entry"""
    
    _name = 'account.move'
    _description = 'Journal Entry'
    _order = 'date desc, name desc'
    _rec_name = 'name'
    
    # Basic Information
    name = fields.Char(
        string='Entry Number',
        required=True,
        help='Journal entry number'
    )
    
    ref = fields.Char(
        string='Reference',
        help='Reference number'
    )
    
    # Journal Information
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        help='Journal for this entry'
    )
    
    # Entry Type
    move_type = fields.Selection([
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
        ('out_refund', 'Customer Refund'),
        ('in_refund', 'Vendor Refund'),
    ], string='Entry Type', required=True, default='entry', help='Type of journal entry')
    
    # Dates
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        help='Entry date'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this entry belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Entry currency'
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner for this entry'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this entry')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this entry')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this entry relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this entry')
    
    # Indian Compliance Fields
    gst_applicable = fields.Boolean(
        string='GST Applicable',
        default=True,
        help='Whether GST is applicable to this entry'
    )
    
    gst_amount = fields.Float(
        string='GST Amount',
        digits=(12, 2),
        default=0.0,
        help='GST amount for this entry'
    )
    
    tds_applicable = fields.Boolean(
        string='TDS Applicable',
        default=False,
        help='Whether TDS is applicable to this entry'
    )
    
    tds_amount = fields.Float(
        string='TDS Amount',
        digits=(12, 2),
        default=0.0,
        help='TDS amount for this entry'
    )
    
    # Amounts
    amount_total = fields.Float(
        string='Total Amount',
        compute='_compute_amounts',
        store=True,
        help='Total amount of this entry'
    )
    
    amount_debit = fields.Float(
        string='Total Debit',
        compute='_compute_amounts',
        store=True,
        help='Total debit amount'
    )
    
    amount_credit = fields.Float(
        string='Total Credit',
        compute='_compute_amounts',
        store=True,
        help='Total credit amount'
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', help='Entry status')
    
    # Entry Lines
    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='Entry Lines',
        help='Journal entry lines'
    )
    
    # Notes
    narration = fields.Text(
        string='Narration',
        help='Entry narration'
    )
    
    # Analytics
    total_lines = fields.Integer(
        string='Total Lines',
        compute='_compute_analytics',
        store=True,
        help='Total number of lines'
    )
    
    @api.depends('line_ids.debit', 'line_ids.credit')
    def _compute_amounts(self):
        """Compute amounts"""
        for move in self:
            move.amount_debit = sum(move.line_ids.mapped('debit'))
            move.amount_credit = sum(move.line_ids.mapped('credit'))
            move.amount_total = move.amount_debit + move.amount_credit
    
    @api.depends('line_ids')
    def _compute_analytics(self):
        """Compute analytics"""
        for move in self:
            move.total_lines = len(move.line_ids)
    
    @api.constrains('line_ids')
    def _check_balanced(self):
        """Check if entry is balanced"""
        for move in self:
            if move.line_ids:
                total_debit = sum(move.line_ids.mapped('debit'))
                total_credit = sum(move.line_ids.mapped('credit'))
                if abs(total_debit - total_credit) > 0.01:
                    raise ValidationError(_('Journal entry must be balanced. Debit: %s, Credit: %s') % (total_debit, total_credit))
    
    @api.constrains('line_ids')
    def _check_lines(self):
        """Check entry lines"""
        for move in self:
            if not move.line_ids:
                raise ValidationError(_('Journal entry must have at least one line.'))
    
    def action_post(self):
        """Post journal entry"""
        for move in self:
            if move.state != 'draft':
                raise UserError(_('Only draft entries can be posted.'))
            
            # Validate entry
            move._check_balanced()
            move._check_lines()
            
            # Post entry
            move.state = 'posted'
            
            # Update account balances
            for line in move.line_ids:
                line._update_account_balance()
    
    def action_cancel(self):
        """Cancel journal entry"""
        for move in self:
            if move.state == 'posted':
                # Reverse account balances
                for line in move.line_ids:
                    line._reverse_account_balance()
            
            move.state = 'cancelled'
    
    def action_draft(self):
        """Set to draft"""
        for move in self:
            if move.state == 'cancelled':
                move.state = 'draft'
    
    def action_reverse(self):
        """Reverse journal entry"""
        for move in self:
            if move.state != 'posted':
                raise UserError(_('Only posted entries can be reversed.'))
            
            # Create reversal entry
            reversal_move = self._create_reversal_entry()
            
            return {
                'type': 'ir.actions.act_window',
                'name': _('Reversal Entry'),
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': reversal_move.id,
            }
    
    def _create_reversal_entry(self):
        """Create reversal entry"""
        self.ensure_one()
        
        reversal_vals = {
            'name': f"REV-{self.name}",
            'ref': f"Reversal of {self.ref or self.name}",
            'journal_id': self.journal_id.id,
            'move_type': 'entry',
            'date': fields.Date.context_today(self),
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'narration': f"Reversal of entry {self.name}",
        }
        
        reversal_move = self.create(reversal_vals)
        
        # Create reversal lines
        for line in self.line_ids:
            reversal_line_vals = {
                'move_id': reversal_move.id,
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'debit': line.credit,
                'credit': line.debit,
                'name': f"Reversal of {line.name}",
                'ref': line.ref,
            }
            self.env['account.move.line'].create(reversal_line_vals)
        
        return reversal_move
    
    def get_entry_analytics(self):
        """Get entry analytics"""
        self.ensure_one()
        return {
            'total_lines': self.total_lines,
            'amount_debit': self.amount_debit,
            'amount_credit': self.amount_credit,
            'amount_total': self.amount_total,
        }


class AccountMoveLine(models.Model):
    """Journal Entry Line"""
    
    _name = 'account.move.line'
    _description = 'Journal Entry Line'
    _order = 'move_id, sequence'
    
    # Basic Information
    name = fields.Char(
        string='Description',
        required=True,
        help='Line description'
    )
    
    ref = fields.Char(
        string='Reference',
        help='Line reference'
    )
    
    # Entry Information
    move_id = fields.Many2one(
        'account.move',
        string='Journal Entry',
        required=True,
        ondelete='cascade',
        help='Journal entry this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Line sequence'
    )
    
    # Account Information
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account for this line'
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner for this line'
    )
    
    # Amounts
    debit = fields.Float(
        string='Debit',
        digits=(12, 2),
        default=0.0,
        help='Debit amount'
    )
    
    credit = fields.Float(
        string='Credit',
        digits=(12, 2),
        default=0.0,
        help='Credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        store=True,
        help='Line balance'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='move_id.currency_id',
        help='Line currency'
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='move_id.company_id',
        help='Company this line belongs to'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this line')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this line')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this line relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this line')
    
    # Indian Compliance Fields
    gst_applicable = fields.Boolean(
        string='GST Applicable',
        default=True,
        help='Whether GST is applicable to this line'
    )
    
    gst_amount = fields.Float(
        string='GST Amount',
        digits=(12, 2),
        default=0.0,
        help='GST amount for this line'
    )
    
    tds_applicable = fields.Boolean(
        string='TDS Applicable',
        default=False,
        help='Whether TDS is applicable to this line'
    )
    
    tds_amount = fields.Float(
        string='TDS Amount',
        digits=(12, 2),
        default=0.0,
        help='TDS amount for this line'
    )
    
    @api.depends('debit', 'credit')
    def _compute_balance(self):
        """Compute line balance"""
        for line in self:
            line.balance = line.debit - line.credit
    
    @api.constrains('debit', 'credit')
    def _check_amounts(self):
        """Check line amounts"""
        for line in self:
            if line.debit < 0 or line.credit < 0:
                raise ValidationError(_('Debit and credit amounts cannot be negative.'))
            
            if line.debit > 0 and line.credit > 0:
                raise ValidationError(_('Line cannot have both debit and credit amounts.'))
    
    def _update_account_balance(self):
        """Update account balance"""
        self.ensure_one()
        # This would update the account balance
        # For now, just logging
        _logger.info(f"Updating account balance for {self.account_id.name}")
    
    def _reverse_account_balance(self):
        """Reverse account balance"""
        self.ensure_one()
        # This would reverse the account balance
        # For now, just logging
        _logger.info(f"Reversing account balance for {self.account_id.name}")