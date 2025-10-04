# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class AccountMoveWizard(models.TransientModel):
    _name = 'account.move.wizard'
    _description = 'Journal Entry Wizard'

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        help='Journal for this entry'
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        help='Date of the journal entry'
    )
    
    ref = fields.Char(
        string='Reference',
        help='Reference for this entry'
    )
    
    narration = fields.Text(
        string='Narration',
        help='Narration for this entry'
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
    ], string='Age Group', help='Age group for this entry')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this entry')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this entry')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this entry'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this entry'
    )
    
    # Entry Lines
    line_ids = fields.One2many(
        'account.move.line.wizard',
        'wizard_id',
        string='Entry Lines',
        help='Lines of the journal entry'
    )
    
    # Financial Information
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
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_totals',
        help='Balance of the entry'
    )
    
    is_balanced = fields.Boolean(
        string='Is Balanced',
        compute='_compute_totals',
        help='Whether the entry is balanced'
    )
    
    @api.depends('line_ids')
    def _compute_totals(self):
        for record in self:
            lines = record.line_ids
            record.total_debit = sum(lines.mapped('debit'))
            record.total_credit = sum(lines.mapped('credit'))
            record.balance = record.total_debit - record.total_credit
            record.is_balanced = abs(record.balance) < 0.01
    
    def action_create_entry(self):
        """Create the journal entry"""
        self.ensure_one()
        
        if not self.is_balanced:
            raise UserError(_('Journal entry must be balanced before creating.'))
        
        if not self.line_ids:
            raise UserError(_('Journal entry must have at least one line.'))
        
        # Create journal entry
        move_vals = {
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': self.ref,
            'narration': self.narration,
            'age_group': self.age_group,
            'size': self.size,
            'season': self.season,
            'brand': self.brand,
            'color': self.color,
            'line_ids': [(0, 0, {
                'account_id': line.account_id.id,
                'name': line.name,
                'debit': line.debit,
                'credit': line.credit,
                'age_group': line.age_group,
                'size': line.size,
                'season': line.season,
                'brand': line.brand,
                'color': line.color,
                'partner_id': line.partner_id.id if line.partner_id else False,
                'product_id': line.product_id.id if line.product_id else False,
            }) for line in self.line_ids]
        }
        
        move = self.env['account.move'].create(move_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entry'),
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_add_line(self):
        """Add a new line to the entry"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add Line'),
            'res_model': 'account.move.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_wizard_id': self.id},
        }


class AccountMoveLineWizard(models.TransientModel):
    _name = 'account.move.line.wizard'
    _description = 'Journal Entry Line Wizard'

    wizard_id = fields.Many2one(
        'account.move.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
        help='Wizard this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account for this line'
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
    
    @api.onchange('account_id')
    def _onchange_account_id(self):
        if self.account_id:
            self.age_group = self.account_id.age_group
            self.size = self.account_id.size
            self.season = self.account_id.season
            self.brand = self.account_id.brand
            self.color = self.account_id.color
    
    def action_add_line(self):
        """Add this line to the wizard"""
        self.ensure_one()
        
        if not self.account_id:
            raise UserError(_('Please select an account.'))
        
        if not self.debit and not self.credit:
            raise UserError(_('Please enter either debit or credit amount.'))
        
        return {
            'type': 'ir.actions.act_window_close',
        }