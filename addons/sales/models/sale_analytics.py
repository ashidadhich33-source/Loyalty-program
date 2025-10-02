# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleAnalytics(models.Model):
    _name = 'sale.analytics'
    _description = 'Sales Analytics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_analytics desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Analytics Name',
        required=True,
        help="Name of the analytics"
    )
    
    # Analytics Information
    date_analytics = fields.Datetime(
        string='Analytics Date',
        required=True,
        default=fields.Datetime.now,
        help="Date of the analytics"
    )
    
    period_start = fields.Datetime(
        string='Period Start',
        required=True,
        help="Start date of the analytics period"
    )
    
    period_end = fields.Datetime(
        string='Period End',
        required=True,
        help="End date of the analytics period"
    )
    
    # Related Records
    order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        help="Sales order for this analytics"
    )
    
    quotation_id = fields.Many2one(
        'sale.quotation',
        string='Sales Quotation',
        help="Sales quotation for this analytics"
    )
    
    delivery_id = fields.Many2one(
        'sale.delivery',
        string='Sales Delivery',
        help="Sales delivery for this analytics"
    )
    
    return_id = fields.Many2one(
        'sale.return',
        string='Sales Return',
        help="Sales return for this analytics"
    )
    
    team_id = fields.Many2one(
        'sale.team',
        string='Sales Team',
        help="Sales team for this analytics"
    )
    
    territory_id = fields.Many2one(
        'sale.territory',
        string='Sales Territory',
        help="Sales territory for this analytics"
    )
    
    commission_id = fields.Many2one(
        'sale.commission',
        string='Sales Commission',
        help="Sales commission for this analytics"
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = fields.Many2one(
        'child.profile',
        string='Child Profile',
        help="Child profile for this analytics"
    )
    
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', help="Age group for this analytics")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help="Gender for this analytics")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help="Season for this analytics")
    
    # Sales Analytics
    total_sales = fields.Monetary(
        string='Total Sales',
        help="Total sales amount"
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        help="Total number of orders"
    )
    
    total_quotations = fields.Integer(
        string='Total Quotations',
        help="Total number of quotations"
    )
    
    total_deliveries = fields.Integer(
        string='Total Deliveries',
        help="Total number of deliveries"
    )
    
    total_returns = fields.Integer(
        string='Total Returns',
        help="Total number of returns"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for this analytics"
    )
    
    # Kids Clothing Specific Analytics
    kids_sales = fields.Monetary(
        string='Kids Sales',
        help="Total sales of kids items"
    )
    
    kids_orders = fields.Integer(
        string='Kids Orders',
        help="Total number of kids orders"
    )
    
    kids_quotations = fields.Integer(
        string='Kids Quotations',
        help="Total number of kids quotations"
    )
    
    kids_deliveries = fields.Integer(
        string='Kids Deliveries',
        help="Total number of kids deliveries"
    )
    
    kids_returns = fields.Integer(
        string='Kids Returns',
        help="Total number of kids returns"
    )
    
    # Age Group Analytics
    age_group_sales = fields.Text(
        string='Age Group Sales',
        help="Sales by age group"
    )
    
    age_group_orders = fields.Text(
        string='Age Group Orders',
        help="Orders by age group"
    )
    
    age_group_quotations = fields.Text(
        string='Age Group Quotations',
        help="Quotations by age group"
    )
    
    age_group_deliveries = fields.Text(
        string='Age Group Deliveries',
        help="Deliveries by age group"
    )
    
    age_group_returns = fields.Text(
        string='Age Group Returns',
        help="Returns by age group"
    )
    
    # Gender Analytics
    gender_sales = fields.Text(
        string='Gender Sales',
        help="Sales by gender"
    )
    
    gender_orders = fields.Text(
        string='Gender Orders',
        help="Orders by gender"
    )
    
    gender_quotations = fields.Text(
        string='Gender Quotations',
        help="Quotations by gender"
    )
    
    gender_deliveries = fields.Text(
        string='Gender Deliveries',
        help="Deliveries by gender"
    )
    
    gender_returns = fields.Text(
        string='Gender Returns',
        help="Returns by gender"
    )
    
    # Season Analytics
    season_sales = fields.Text(
        string='Season Sales',
        help="Sales by season"
    )
    
    season_orders = fields.Text(
        string='Season Orders',
        help="Orders by season"
    )
    
    season_quotations = fields.Text(
        string='Season Quotations',
        help="Quotations by season"
    )
    
    season_deliveries = fields.Text(
        string='Season Deliveries',
        help="Deliveries by season"
    )
    
    season_returns = fields.Text(
        string='Season Returns',
        help="Returns by season"
    )
    
    # Performance Analytics
    conversion_rate = fields.Float(
        string='Conversion Rate (%)',
        help="Quotation to order conversion rate"
    )
    
    delivery_rate = fields.Float(
        string='Delivery Rate (%)',
        help="Order to delivery rate"
    )
    
    return_rate = fields.Float(
        string='Return Rate (%)',
        help="Order to return rate"
    )
    
    # Customer Analytics
    total_customers = fields.Integer(
        string='Total Customers',
        help="Total number of customers"
    )
    
    new_customers = fields.Integer(
        string='New Customers',
        help="Number of new customers"
    )
    
    returning_customers = fields.Integer(
        string='Returning Customers',
        help="Number of returning customers"
    )
    
    # Product Analytics
    total_products = fields.Integer(
        string='Total Products',
        help="Total number of products"
    )
    
    top_products = fields.Text(
        string='Top Products',
        help="Top selling products"
    )
    
    top_categories = fields.Text(
        string='Top Categories',
        help="Top selling categories"
    )
    
    # Team Analytics
    team_performance = fields.Text(
        string='Team Performance',
        help="Performance by team"
    )
    
    territory_performance = fields.Text(
        string='Territory Performance',
        help="Performance by territory"
    )
    
    # Commission Analytics
    total_commission = fields.Monetary(
        string='Total Commission',
        help="Total commission paid"
    )
    
    commission_rate = fields.Float(
        string='Commission Rate (%)',
        help="Average commission rate"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this analytics belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this analytics is active"
    )
    
    def action_view_orders(self):
        """View orders for this analytics"""
        action = self.env.ref('sales.action_sale_order').read()[0]
        if self.order_id:
            action['domain'] = [('id', '=', self.order_id.id)]
        else:
            action['domain'] = [('id', '=', False)]
        return action
    
    def action_view_quotations(self):
        """View quotations for this analytics"""
        action = self.env.ref('sales.action_sale_quotation').read()[0]
        if self.quotation_id:
            action['domain'] = [('id', '=', self.quotation_id.id)]
        else:
            action['domain'] = [('id', '=', False)]
        return action
    
    def action_view_deliveries(self):
        """View deliveries for this analytics"""
        action = self.env.ref('sales.action_sale_delivery').read()[0]
        if self.delivery_id:
            action['domain'] = [('id', '=', self.delivery_id.id)]
        else:
            action['domain'] = [('id', '=', False)]
        return action
    
    def action_view_returns(self):
        """View returns for this analytics"""
        action = self.env.ref('sales.action_sale_return').read()[0]
        if self.return_id:
            action['domain'] = [('id', '=', self.return_id.id)]
        else:
            action['domain'] = [('id', '=', False)]
        return action
    
    def action_view_team(self):
        """View team for this analytics"""
        if not self.team_id:
            raise ValidationError(_('No team found.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Team',
            'res_model': 'sale.team',
            'view_mode': 'form',
            'res_id': self.team_id.id,
        }
    
    def action_view_territory(self):
        """View territory for this analytics"""
        if not self.territory_id:
            raise ValidationError(_('No territory found.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Territory',
            'res_model': 'sale.territory',
            'view_mode': 'form',
            'res_id': self.territory_id.id,
        }
    
    def action_view_commission(self):
        """View commission for this analytics"""
        if not self.commission_id:
            raise ValidationError(_('No commission found.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Commission',
            'res_model': 'sale.commission',
            'view_mode': 'form',
            'res_id': self.commission_id.id,
        }