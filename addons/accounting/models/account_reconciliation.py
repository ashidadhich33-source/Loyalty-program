# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountReconciliation(models.Model):
    _name = 'account.reconciliation'
    _description = 'Account Reconciliation'
    _order = 'date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Reconciliation Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help='Reference of the reconciliation'
    )
    
    date = fields.Date(
        string='Reconciliation Date',
        required=True,
        default=fields.Date.today,
        help='Date of the reconciliation'
    )
    
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account to reconcile'
    )
    
    reconciliation_type = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('bank', 'Bank Reconciliation'),
        ('customer', 'Customer Reconciliation'),
        ('supplier', 'Supplier Reconciliation'),
        ('inventory', 'Inventory Reconciliation'),
    ], string='Reconciliation Type', required=True, help='Type of reconciliation')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True, help='State of the reconciliation')
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-14', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this reconciliation')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this reconciliation')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this reconciliation')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this reconciliation'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this reconciliation'
    )
    
    # Reconciliation Lines
    reconciliation_line_ids = fields.One2many(
        'account.reconciliation.line',
        'reconciliation_id',
        string='Reconciliation Lines',
        help='Lines of the reconciliation'
    )
    
    # Reconciliation Summary
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_totals',
        help='Total amount reconciled'
    )
    
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_totals',
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_totals',
        help='Total credit amount'
    )
    
    is_balanced = fields.Boolean(
        string='Is Balanced',
        compute='_compute_totals',
        help='Whether the reconciliation is balanced'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this reconciliation belongs to'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this reconciliation'
    )
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the reconciliation was created'
    )
    
    confirm_date = fields.Datetime(
        string='Confirmed On',
        readonly=True,
        help='Date when the reconciliation was confirmed'
    )
    
    done_date = fields.Datetime(
        string='Done On',
        readonly=True,
        help='Date when the reconciliation was completed'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the reconciliation'
    )
    
    confirmed_by = fields.Many2one(
        'res.users',
        string='Confirmed By',
        readonly=True,
        help='User who confirmed the reconciliation'
    )
    
    done_by = fields.Many2one(
        'res.users',
        string='Done By',
        readonly=True,
        help='User who completed the reconciliation'
    )
    
    @api.depends('reconciliation_line_ids')
    def _compute_totals(self):
        for record in self:
            lines = record.reconciliation_line_ids
            record.total_debit = sum(lines.mapped('debit'))
            record.total_credit = sum(lines.mapped('credit'))
            record.total_amount = record.total_debit + record.total_credit
            record.is_balanced = abs(record.total_debit - record.total_credit) < 0.01
    
    @api.model
    def create(self, vals):
        """Override create to generate sequence"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('account.reconciliation') or _('New')
        return super(AccountReconciliation, self).create(vals)
    
    def action_confirm(self):
        """Confirm the reconciliation"""
        for record in self:
            if record.state == 'draft':
                if not record.is_balanced:
                    raise UserError(_('Reconciliation must be balanced before confirming.'))
                
                record.write({
                    'state': 'confirmed',
                    'confirm_date': fields.Datetime.now(),
                    'confirmed_by': self.env.user.id,
                })
    
    def action_done(self):
        """Complete the reconciliation"""
        for record in self:
            if record.state == 'confirmed':
                # Mark lines as reconciled
                for line in record.reconciliation_line_ids:
                    if line.move_line_id:
                        line.move_line_id.write({
                            'reconciled': True,
                            'reconciled_date': record.date,
                        })
                
                record.write({
                    'state': 'done',
                    'done_date': fields.Datetime.now(),
                    'done_by': self.env.user.id,
                })
    
    def action_cancel(self):
        """Cancel the reconciliation"""
        for record in self:
            if record.state in ['draft', 'confirmed']:
                record.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        """Reset to draft state"""
        for record in self:
            if record.state == 'cancelled':
                record.write({'state': 'draft'})
    
    @api.constrains('reconciliation_line_ids')
    def _check_lines(self):
        for record in self:
            if not record.reconciliation_line_ids:
                raise ValidationError(_('Reconciliation must have at least one line.'))
    
    def action_add_line(self):
        """Add a new line to the reconciliation"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add Line'),
            'res_model': 'account.reconciliation.line',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_reconciliation_id': self.id},
        }
    
    @api.model
    def get_kids_clothing_reconciliations(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get reconciliations filtered by kids clothing criteria"""
        domain = [('state', '=', 'done')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)
    
    @api.model
    def create_kids_clothing_reconciliation(self, account_id, age_group=None, size=None, season=None, brand=None, color=None):
        """Create a reconciliation for kids clothing transaction"""
        # This method would create reconciliations tailored for kids clothing transactions
        pass


class AccountReconciliationLine(models.Model):
    _name = 'account.reconciliation.line'
    _description = 'Reconciliation Line'
    _order = 'sequence, id'

    reconciliation_id = fields.Many2one(
        'account.reconciliation',
        string='Reconciliation',
        required=True,
        ondelete='cascade',
        help='Reconciliation this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    move_line_id = fields.Many2one(
        'account.move.line',
        string='Journal Entry Line',
        help='Journal entry line to reconcile'
    )
    
    name = fields.Char(
        string='Description',
        help='Description of this line'
    )
    
    debit = fields.Float(
        string='Debit',
        digits='Account',
        help='Debit amount'
    )
    
    credit = fields.Float(
        string='Credit',
        digits='Account',
        help='Credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        help='Balance of this line'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this line')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this line')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this line')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this line'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this line'
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner for this line'
    )
    
    # Product Information
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        help='Product for this line'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this line belongs to'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this line'
    )
    
    @api.depends('debit', 'credit')
    def _compute_balance(self):
        for record in self:
            record.balance = record.debit - record.credit
    
    @api.constrains('debit', 'credit')
    def _check_amounts(self):
        for record in self:
            if record.debit and record.credit:
                raise ValidationError(_('A line cannot have both debit and credit amounts.'))
            
            if not record.debit and not record.credit:
                raise ValidationError(_('A line must have either debit or credit amount.'))
    
    @api.onchange('move_line_id')
    def _onchange_move_line_id(self):
        if self.move_line_id:
            self.name = self.move_line_id.name
            self.debit = self.move_line_id.debit
            self.credit = self.move_line_id.credit
            self.age_group = self.move_line_id.age_group
            self.size = self.move_line_id.size
            self.season = self.move_line_id.season
            self.brand = self.move_line_id.brand
            self.color = self.move_line_id.color
            self.partner_id = self.move_line_id.partner_id
            self.product_id = self.move_line_id.product_id
    
    @api.model
    def get_kids_clothing_reconciliation_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get reconciliation lines filtered by kids clothing criteria"""
        domain = [('reconciliation_id.state', '=', 'done')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)