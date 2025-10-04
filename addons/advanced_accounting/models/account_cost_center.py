# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Cost Center Management
==============================================================

Cost center management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountCostCenter(models.Model):
    """Cost Center"""
    
    _name = 'account.cost.center'
    _description = 'Cost Center'
    _order = 'code'
    
    # Basic Information
    name = fields.Char(
        string='Cost Center Name',
        required=True,
        help='Cost center name'
    )
    
    code = fields.Char(
        string='Cost Center Code',
        required=True,
        help='Cost center code'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this cost center belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Cost center currency'
    )
    
    # Hierarchy
    parent_id = fields.Many2one(
        'account.cost.center',
        string='Parent Cost Center',
        help='Parent cost center in the hierarchy'
    )
    
    child_ids = fields.One2many(
        'account.cost.center',
        'parent_id',
        string='Child Cost Centers',
        help='Child cost centers'
    )
    
    # Manager Information
    manager_id = fields.Many2one(
        'hr.employee',
        string='Manager',
        help='Cost center manager'
    )
    
    # Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this cost center is active'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this cost center')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this cost center')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this cost center relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this cost center')
    
    # Analytics
    total_expenses = fields.Float(
        string='Total Expenses',
        compute='_compute_analytics',
        store=True,
        help='Total expenses for this cost center'
    )
    
    total_revenue = fields.Float(
        string='Total Revenue',
        compute='_compute_analytics',
        store=True,
        help='Total revenue for this cost center'
    )
    
    profit_loss = fields.Float(
        string='Profit/Loss',
        compute='_compute_analytics',
        store=True,
        help='Profit or loss for this cost center'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this cost center'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for cost_center in self:
            # This would be computed from journal entries
            # For now, setting to 0
            cost_center.total_expenses = 0.0
            cost_center.total_revenue = 0.0
            cost_center.profit_loss = 0.0
    
    @api.constrains('code')
    def _check_code(self):
        """Validate cost center code"""
        for cost_center in self:
            if not cost_center.code:
                raise ValidationError(_('Cost center code is required.'))
            
            # Check for duplicate codes
            duplicate = self.search([
                ('code', '=', cost_center.code),
                ('company_id', '=', cost_center.company_id.id),
                ('id', '!=', cost_center.id)
            ])
            if duplicate:
                raise ValidationError(_('Cost center code must be unique within the company.'))
    
    @api.constrains('parent_id')
    def _check_parent(self):
        """Validate parent cost center"""
        for cost_center in self:
            if cost_center.parent_id:
                if cost_center.parent_id == cost_center:
                    raise ValidationError(_('Cost center cannot be its own parent.'))
                
                if cost_center.parent_id.parent_id == cost_center:
                    raise ValidationError(_('Cost center cannot be parent of its parent.'))
    
    def name_get(self):
        """Return display name"""
        result = []
        for cost_center in self:
            result.append((cost_center.id, f"{cost_center.code} - {cost_center.name}"))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search by name or code"""
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        cost_centers = self.search(domain + args, limit=limit)
        return cost_centers.name_get()
    
    def action_view_expenses(self):
        """View expenses for this cost center"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('cost_center_id', '=', self.id)],
            'context': {'default_cost_center_id': self.id},
        }
    
    def action_view_revenue(self):
        """View revenue for this cost center"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Revenue'),
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('cost_center_id', '=', self.id)],
            'context': {'default_cost_center_id': self.id},
        }
    
    def get_cost_center_analytics(self, date_from=None, date_to=None):
        """Get cost center analytics for date range"""
        self.ensure_one()
        # This would query journal entries
        # For now, returning basic info
        return {
            'total_expenses': self.total_expenses,
            'total_revenue': self.total_revenue,
            'profit_loss': self.profit_loss,
        }