# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = 'Sales Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Commission Name',
        required=True,
        help="Name of the commission"
    )
    
    code = fields.Char(
        string='Commission Code',
        required=True,
        help="Code for the commission"
    )
    
    # Commission Information
    description = fields.Text(
        string='Description',
        help="Description of the commission"
    )
    
    # Commission Type
    commission_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('tiered', 'Tiered'),
    ], string='Commission Type', default='percentage',
       help="Type of commission calculation"
    )
    
    # Commission Rate
    commission_rate = fields.Float(
        string='Commission Rate (%)',
        digits='Commission Rate',
        help="Commission rate as percentage"
    )
    
    fixed_amount = fields.Monetary(
        string='Fixed Amount',
        help="Fixed commission amount"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for this commission"
    )
    
    # Commission Rules
    rule_ids = fields.One2many(
        'sale.commission.rule',
        'commission_id',
        string='Commission Rules',
        help="Rules for this commission"
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group Focus', default='all',
       help="Primary age group focus for this commission")
    
    gender_focus = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Focus', default='all',
       help="Primary gender focus for this commission")
    
    season_focus = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Seasons'),
    ], string='Season Focus', default='all_season',
       help="Primary season focus for this commission")
    
    # Commission Conditions
    minimum_amount = fields.Monetary(
        string='Minimum Amount',
        help="Minimum amount for commission"
    )
    
    maximum_amount = fields.Monetary(
        string='Maximum Amount',
        help="Maximum amount for commission"
    )
    
    # Commission Period
    period_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('per_order', 'Per Order'),
    ], string='Period Type', default='per_order',
       help="Period for commission calculation"
    )
    
    # Commission Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft',
       help="Current status of the commission")
    
    # Commission Analytics
    total_commission = fields.Monetary(
        string='Total Commission',
        compute='_compute_total_commission',
        help="Total commission paid"
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        compute='_compute_total_orders',
        help="Total number of orders with this commission"
    )
    
    # Kids Clothing Specific Analytics
    kids_commission = fields.Monetary(
        string='Kids Commission',
        compute='_compute_kids_commission',
        help="Total commission from kids items"
    )
    
    age_group_commission = fields.Text(
        string='Age Group Commission',
        compute='_compute_age_group_commission',
        help="Commission by age group"
    )
    
    gender_commission = fields.Text(
        string='Gender Commission',
        compute='_compute_gender_commission',
        help="Commission by gender"
    )
    
    season_commission = fields.Text(
        string='Season Commission',
        compute='_compute_season_commission',
        help="Commission by season"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this commission belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this commission is active"
    )
    
    @api.depends('rule_ids', 'rule_ids.commission_amount')
    def _compute_total_commission(self):
        for commission in self:
            commission.total_commission = sum(rule.commission_amount for rule in commission.rule_ids)
    
    @api.depends('rule_ids', 'rule_ids.order_count')
    def _compute_total_orders(self):
        for commission in self:
            commission.total_orders = sum(rule.order_count for rule in commission.rule_ids)
    
    @api.depends('rule_ids', 'rule_ids.kids_commission')
    def _compute_kids_commission(self):
        for commission in self:
            commission.kids_commission = sum(rule.kids_commission for rule in commission.rule_ids)
    
    @api.depends('rule_ids', 'rule_ids.age_group_commission')
    def _compute_age_group_commission(self):
        for commission in self:
            age_group_commission = {}
            for rule in commission.rule_ids:
                if rule.age_group_commission:
                    try:
                        rule_commission = eval(rule.age_group_commission)
                        for age_group, amount in rule_commission.items():
                            if age_group not in age_group_commission:
                                age_group_commission[age_group] = 0
                            age_group_commission[age_group] += amount
                    except:
                        pass
            commission.age_group_commission = str(age_group_commission)
    
    @api.depends('rule_ids', 'rule_ids.gender_commission')
    def _compute_gender_commission(self):
        for commission in self:
            gender_commission = {}
            for rule in commission.rule_ids:
                if rule.gender_commission:
                    try:
                        rule_commission = eval(rule.gender_commission)
                        for gender, amount in rule_commission.items():
                            if gender not in gender_commission:
                                gender_commission[gender] = 0
                            gender_commission[gender] += amount
                    except:
                        pass
            commission.gender_commission = str(gender_commission)
    
    @api.depends('rule_ids', 'rule_ids.season_commission')
    def _compute_season_commission(self):
        for commission in self:
            season_commission = {}
            for rule in commission.rule_ids:
                if rule.season_commission:
                    try:
                        rule_commission = eval(rule.season_commission)
                        for season, amount in rule_commission.items():
                            if season not in season_commission:
                                season_commission[season] = 0
                            season_commission[season] += amount
                    except:
                        pass
            commission.season_commission = str(season_commission)
    
    def action_activate(self):
        """Activate commission"""
        self.write({'state': 'active'})
        return True
    
    def action_deactivate(self):
        """Deactivate commission"""
        self.write({'state': 'inactive'})
        return True
    
    def action_view_rules(self):
        """View commission rules"""
        action = self.env.ref('sales.action_sale_commission_rule').read()[0]
        action['domain'] = [('commission_id', '=', self.id)]
        return action
    
    def action_view_analytics(self):
        """View commission analytics"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('commission_id', '=', self.id)]
        return action


class SaleCommissionRule(models.Model):
    _name = 'sale.commission.rule'
    _description = 'Sales Commission Rule'
    _order = 'commission_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this commission rule"
    )
    
    # Commission Reference
    commission_id = fields.Many2one(
        'sale.commission',
        string='Commission',
        required=True,
        ondelete='cascade',
        help="Commission this rule belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of rules in the commission"
    )
    
    # Rule Information
    name = fields.Char(
        string='Rule Name',
        required=True,
        help="Name of this commission rule"
    )
    
    description = fields.Text(
        string='Description',
        help="Description of this commission rule"
    )
    
    # Rule Conditions
    condition_type = fields.Selection([
        ('amount', 'Amount Based'),
        ('quantity', 'Quantity Based'),
        ('product', 'Product Based'),
        ('customer', 'Customer Based'),
        ('territory', 'Territory Based'),
        ('team', 'Team Based'),
    ], string='Condition Type', default='amount',
       help="Type of condition for this rule"
    )
    
    # Amount Conditions
    minimum_amount = fields.Monetary(
        string='Minimum Amount',
        help="Minimum amount for this rule"
    )
    
    maximum_amount = fields.Monetary(
        string='Maximum Amount',
        help="Maximum amount for this rule"
    )
    
    # Quantity Conditions
    minimum_quantity = fields.Float(
        string='Minimum Quantity',
        help="Minimum quantity for this rule"
    )
    
    maximum_quantity = fields.Float(
        string='Maximum Quantity',
        help="Maximum quantity for this rule"
    )
    
    # Product Conditions
    product_ids = fields.Many2many(
        'product.product',
        string='Products',
        help="Products for this rule"
    )
    
    category_ids = fields.Many2many(
        'product.category',
        string='Categories',
        help="Categories for this rule"
    )
    
    # Customer Conditions
    customer_ids = fields.Many2many(
        'res.partner',
        string='Customers',
        help="Customers for this rule"
    )
    
    customer_segment_ids = fields.Many2many(
        'res.partner.segment',
        string='Customer Segments',
        help="Customer segments for this rule"
    )
    
    # Territory Conditions
    territory_ids = fields.Many2many(
        'sale.territory',
        string='Territories',
        help="Territories for this rule"
    )
    
    # Team Conditions
    team_ids = fields.Many2many(
        'sale.team',
        string='Teams',
        help="Teams for this rule"
    )
    
    # Kids Clothing Specific Conditions
    age_group_ids = fields.Many2many(
        'product.age.group',
        string='Age Groups',
        help="Age groups for this rule"
    )
    
    gender_ids = fields.Many2many(
        'product.gender',
        string='Genders',
        help="Genders for this rule"
    )
    
    season_ids = fields.Many2many(
        'product.season',
        string='Seasons',
        help="Seasons for this rule"
    )
    
    # Commission Calculation
    commission_rate = fields.Float(
        string='Commission Rate (%)',
        digits='Commission Rate',
        help="Commission rate for this rule"
    )
    
    fixed_amount = fields.Monetary(
        string='Fixed Amount',
        help="Fixed commission amount for this rule"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='commission_id.currency_id',
        store=True,
        help="Currency for this rule"
    )
    
    # Commission Analytics
    commission_amount = fields.Monetary(
        string='Commission Amount',
        compute='_compute_commission_amount',
        help="Total commission amount for this rule"
    )
    
    order_count = fields.Integer(
        string='Order Count',
        compute='_compute_order_count',
        help="Total number of orders for this rule"
    )
    
    # Kids Clothing Specific Analytics
    kids_commission = fields.Monetary(
        string='Kids Commission',
        compute='_compute_kids_commission',
        help="Total commission from kids items for this rule"
    )
    
    age_group_commission = fields.Text(
        string='Age Group Commission',
        compute='_compute_age_group_commission',
        help="Commission by age group for this rule"
    )
    
    gender_commission = fields.Text(
        string='Gender Commission',
        compute='_compute_gender_commission',
        help="Commission by gender for this rule"
    )
    
    season_commission = fields.Text(
        string='Season Commission',
        compute='_compute_season_commission',
        help="Commission by season for this rule"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='commission_id.company_id',
        store=True,
        help="Company this rule belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this rule is active"
    )
    
    @api.depends('name', 'commission_id', 'commission_id.name')
    def _compute_display_name(self):
        for rule in self:
            if rule.commission_id:
                rule.display_name = f"{rule.name} - {rule.commission_id.name}"
            else:
                rule.display_name = rule.name
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_commission_amount(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to 0
            rule.commission_amount = 0.0
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_order_count(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to 0
            rule.order_count = 0
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_kids_commission(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to 0
            rule.kids_commission = 0.0
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_age_group_commission(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to empty
            rule.age_group_commission = str({})
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_gender_commission(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to empty
            rule.gender_commission = str({})
    
    @api.depends('commission_id', 'commission_id.rule_ids')
    def _compute_season_commission(self):
        for rule in self:
            # This would be calculated based on actual orders
            # For now, we'll set it to empty
            rule.season_commission = str({})