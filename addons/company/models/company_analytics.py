# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class CompanyAnalytics(models.Model):
    """Company analytics model for Kids Clothing ERP"""
    
    _name = 'company.analytics'
    _description = 'Company Analytics'
    _order = 'date desc'
    
    # Basic fields
    name = fields.Char(
        string='Analytics Name',
        required=True,
        help='Name of the analytics record'
    )
    
    # Company relationship
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='Company this analytics belongs to'
    )
    
    # Analytics details
    date = fields.Date(
        string='Date',
        required=True,
        help='Date of the analytics'
    )
    
    period_type = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', default='daily', help='Type of analytics period')
    
    # Financial metrics
    total_sales = fields.Float(
        string='Total Sales',
        default=0.0,
        help='Total sales for the period'
    )
    
    total_purchase = fields.Float(
        string='Total Purchase',
        default=0.0,
        help='Total purchase for the period'
    )
    
    total_profit = fields.Float(
        string='Total Profit',
        compute='_compute_total_profit',
        store=True,
        help='Total profit for the period'
    )
    
    profit_margin = fields.Float(
        string='Profit Margin',
        compute='_compute_profit_margin',
        store=True,
        help='Profit margin percentage'
    )
    
    # Operational metrics
    total_orders = fields.Integer(
        string='Total Orders',
        default=0,
        help='Total orders for the period'
    )
    
    total_customers = fields.Integer(
        string='Total Customers',
        default=0,
        help='Total customers for the period'
    )
    
    total_products = fields.Integer(
        string='Total Products',
        default=0,
        help='Total products for the period'
    )
    
    # User metrics
    total_users = fields.Integer(
        string='Total Users',
        default=0,
        help='Total users for the period'
    )
    
    active_users = fields.Integer(
        string='Active Users',
        default=0,
        help='Active users for the period'
    )
    
    # Inventory metrics
    total_inventory_value = fields.Float(
        string='Total Inventory Value',
        default=0.0,
        help='Total inventory value for the period'
    )
    
    inventory_turnover = fields.Float(
        string='Inventory Turnover',
        default=0.0,
        help='Inventory turnover ratio'
    )
    
    # Performance metrics
    average_order_value = fields.Float(
        string='Average Order Value',
        compute='_compute_average_order_value',
        store=True,
        help='Average order value for the period'
    )
    
    customer_retention_rate = fields.Float(
        string='Customer Retention Rate',
        default=0.0,
        help='Customer retention rate percentage'
    )
    
    # Growth metrics
    sales_growth = fields.Float(
        string='Sales Growth',
        default=0.0,
        help='Sales growth percentage'
    )
    
    customer_growth = fields.Float(
        string='Customer Growth',
        default=0.0,
        help='Customer growth percentage'
    )
    
    user_growth = fields.Float(
        string='User Growth',
        default=0.0,
        help='User growth percentage'
    )
    
    # Efficiency metrics
    sales_per_user = fields.Float(
        string='Sales per User',
        compute='_compute_sales_per_user',
        store=True,
        help='Sales per user for the period'
    )
    
    orders_per_user = fields.Float(
        string='Orders per User',
        compute='_compute_orders_per_user',
        store=True,
        help='Orders per user for the period'
    )
    
    # Quality metrics
    order_fulfillment_rate = fields.Float(
        string='Order Fulfillment Rate',
        default=0.0,
        help='Order fulfillment rate percentage'
    )
    
    customer_satisfaction = fields.Float(
        string='Customer Satisfaction',
        default=0.0,
        help='Customer satisfaction score'
    )
    
    # Analytics metadata
    metadata = fields.Text(
        string='Metadata',
        help='Additional analytics metadata (JSON format)'
    )
    
    # Analytics status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the analytics record is active'
    )
    
    is_processed = fields.Boolean(
        string='Processed',
        default=False,
        help='Whether the analytics has been processed'
    )
    
    @api.depends('total_sales', 'total_purchase')
    def _compute_total_profit(self):
        """Compute total profit"""
        for analytics in self:
            analytics.total_profit = analytics.total_sales - analytics.total_purchase
    
    @api.depends('total_sales', 'total_profit')
    def _compute_profit_margin(self):
        """Compute profit margin"""
        for analytics in self:
            if analytics.total_sales > 0:
                analytics.profit_margin = (analytics.total_profit / analytics.total_sales) * 100
            else:
                analytics.profit_margin = 0.0
    
    @api.depends('total_sales', 'total_orders')
    def _compute_average_order_value(self):
        """Compute average order value"""
        for analytics in self:
            if analytics.total_orders > 0:
                analytics.average_order_value = analytics.total_sales / analytics.total_orders
            else:
                analytics.average_order_value = 0.0
    
    @api.depends('total_sales', 'active_users')
    def _compute_sales_per_user(self):
        """Compute sales per user"""
        for analytics in self:
            if analytics.active_users > 0:
                analytics.sales_per_user = analytics.total_sales / analytics.active_users
            else:
                analytics.sales_per_user = 0.0
    
    @api.depends('total_orders', 'active_users')
    def _compute_orders_per_user(self):
        """Compute orders per user"""
        for analytics in self:
            if analytics.active_users > 0:
                analytics.orders_per_user = analytics.total_orders / analytics.active_users
            else:
                analytics.orders_per_user = 0.0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default date if not provided
        if 'date' not in vals:
            vals['date'] = fields.Date.today()
        
        return super(CompanyAnalytics, self).create(vals)
    
    def write(self, vals):
        """Override write to handle analytics updates"""
        result = super(CompanyAnalytics, self).write(vals)
        
        # Mark as processed if key metrics are updated
        if any(field in vals for field in ['total_sales', 'total_purchase', 'total_orders', 'total_customers']):
            self.is_processed = True
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of processed analytics"""
        for analytics in self:
            if analytics.is_processed:
                raise ValidationError(_('Processed analytics cannot be deleted'))
        
        return super(CompanyAnalytics, self).unlink()
    
    def action_process(self):
        """Process analytics"""
        self.ensure_one()
        
        # This would need actual implementation to process analytics
        self.is_processed = True
        return True
    
    def action_reprocess(self):
        """Reprocess analytics"""
        self.ensure_one()
        
        self.is_processed = False
        self.action_process()
        return True
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'name': self.name,
            'date': self.date,
            'period_type': self.period_type,
            'total_sales': self.total_sales,
            'total_purchase': self.total_purchase,
            'total_profit': self.total_profit,
            'profit_margin': self.profit_margin,
            'total_orders': self.total_orders,
            'total_customers': self.total_customers,
            'total_products': self.total_products,
            'total_users': self.total_users,
            'active_users': self.active_users,
            'average_order_value': self.average_order_value,
            'sales_per_user': self.sales_per_user,
            'orders_per_user': self.orders_per_user,
            'is_processed': self.is_processed,
        }
    
    @api.model
    def get_analytics_by_company(self, company_id, date_from=None, date_to=None):
        """Get analytics by company"""
        domain = [('company_id', '=', company_id), ('is_active', '=', True)]
        
        if date_from:
            domain.append(('date', '>=', date_from))
        
        if date_to:
            domain.append(('date', '<=', date_to))
        
        return self.search(domain)
    
    @api.model
    def get_analytics_by_period(self, period_type, date_from=None, date_to=None):
        """Get analytics by period type"""
        domain = [('period_type', '=', period_type), ('is_active', '=', True)]
        
        if date_from:
            domain.append(('date', '>=', date_from))
        
        if date_to:
            domain.append(('date', '<=', date_to))
        
        return self.search(domain)
    
    @api.model
    def get_analytics_summary(self, company_id=None, date_from=None, date_to=None):
        """Get analytics summary"""
        domain = [('is_active', '=', True)]
        
        if company_id:
            domain.append(('company_id', '=', company_id))
        
        if date_from:
            domain.append(('date', '>=', date_from))
        
        if date_to:
            domain.append(('date', '<=', date_to))
        
        analytics = self.search(domain)
        
        if not analytics:
            return {
                'total_sales': 0.0,
                'total_purchase': 0.0,
                'total_profit': 0.0,
                'total_orders': 0,
                'total_customers': 0,
                'total_products': 0,
                'total_users': 0,
                'active_users': 0,
                'average_order_value': 0.0,
                'sales_per_user': 0.0,
                'orders_per_user': 0.0,
            }
        
        return {
            'total_sales': sum(analytics.mapped('total_sales')),
            'total_purchase': sum(analytics.mapped('total_purchase')),
            'total_profit': sum(analytics.mapped('total_profit')),
            'total_orders': sum(analytics.mapped('total_orders')),
            'total_customers': sum(analytics.mapped('total_customers')),
            'total_products': sum(analytics.mapped('total_products')),
            'total_users': sum(analytics.mapped('total_users')),
            'active_users': sum(analytics.mapped('active_users')),
            'average_order_value': sum(analytics.mapped('average_order_value')) / len(analytics) if analytics else 0.0,
            'sales_per_user': sum(analytics.mapped('sales_per_user')) / len(analytics) if analytics else 0.0,
            'orders_per_user': sum(analytics.mapped('orders_per_user')) / len(analytics) if analytics else 0.0,
        }
    
    @api.model
    def generate_analytics(self, company_id, date, period_type='daily'):
        """Generate analytics for a specific period"""
        analytics = self.create({
            'name': f'Analytics {date}',
            'company_id': company_id,
            'date': date,
            'period_type': period_type,
        })
        
        # This would need actual implementation to generate analytics data
        analytics.action_process()
        
        return analytics
    
    @api.model
    def get_analytics_trends(self, company_id, metric, days=30):
        """Get analytics trends for a specific metric"""
        date_from = fields.Date.today() - timedelta(days=days)
        
        analytics = self.search([
            ('company_id', '=', company_id),
            ('date', '>=', date_from),
            ('is_active', '=', True),
        ], order='date')
        
        trends = []
        for analytic in analytics:
            trends.append({
                'date': analytic.date,
                'value': getattr(analytic, metric, 0),
            })
        
        return trends
    
    @api.model
    def get_analytics_comparison(self, company_id, metric, current_period, previous_period):
        """Get analytics comparison between periods"""
        current_analytics = self.search([
            ('company_id', '=', company_id),
            ('date', '>=', current_period['start']),
            ('date', '<=', current_period['end']),
            ('is_active', '=', True),
        ])
        
        previous_analytics = self.search([
            ('company_id', '=', company_id),
            ('date', '>=', previous_period['start']),
            ('date', '<=', previous_period['end']),
            ('is_active', '=', True),
        ])
        
        current_value = sum(getattr(analytic, metric, 0) for analytic in current_analytics)
        previous_value = sum(getattr(analytic, metric, 0) for analytic in previous_analytics)
        
        if previous_value > 0:
            growth_rate = ((current_value - previous_value) / previous_value) * 100
        else:
            growth_rate = 0.0
        
        return {
            'current_value': current_value,
            'previous_value': previous_value,
            'growth_rate': growth_rate,
            'growth_direction': 'up' if growth_rate > 0 else 'down' if growth_rate < 0 else 'stable',
        }
    
    @api.model
    def get_analytics_analytics(self):
        """Get analytics analytics summary"""
        total_analytics = self.search_count([])
        active_analytics = self.search_count([('is_active', '=', True)])
        processed_analytics = self.search_count([('is_processed', '=', True)])
        
        return {
            'total_analytics': total_analytics,
            'active_analytics': active_analytics,
            'processed_analytics': processed_analytics,
            'inactive_analytics': total_analytics - active_analytics,
            'unprocessed_analytics': total_analytics - processed_analytics,
            'active_percentage': (active_analytics / total_analytics * 100) if total_analytics > 0 else 0,
            'processed_percentage': (processed_analytics / total_analytics * 100) if total_analytics > 0 else 0,
        }
    
    @api.constrains('date')
    def _check_date(self):
        """Validate analytics date"""
        for analytics in self:
            if analytics.date > fields.Date.today():
                raise ValidationError(_('Analytics date cannot be in the future'))
    
    @api.constrains('total_sales', 'total_purchase')
    def _check_financial_values(self):
        """Validate financial values"""
        for analytics in self:
            if analytics.total_sales < 0:
                raise ValidationError(_('Total sales cannot be negative'))
            
            if analytics.total_purchase < 0:
                raise ValidationError(_('Total purchase cannot be negative'))
    
    def action_duplicate(self):
        """Duplicate analytics"""
        self.ensure_one()
        
        new_analytics = self.copy({
            'name': f'{self.name} (Copy)',
            'is_processed': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Analytics',
            'res_model': 'company.analytics',
            'res_id': new_analytics.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_analytics(self):
        """Export analytics data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'company_id': self.company_id.id,
            'date': self.date,
            'period_type': self.period_type,
            'total_sales': self.total_sales,
            'total_purchase': self.total_purchase,
            'total_profit': self.total_profit,
            'profit_margin': self.profit_margin,
            'total_orders': self.total_orders,
            'total_customers': self.total_customers,
            'total_products': self.total_products,
            'total_users': self.total_users,
            'active_users': self.active_users,
            'average_order_value': self.average_order_value,
            'sales_per_user': self.sales_per_user,
            'orders_per_user': self.orders_per_user,
            'is_processed': self.is_processed,
        }
    
    def action_import_analytics(self, analytics_data):
        """Import analytics data"""
        self.ensure_one()
        
        self.write(analytics_data)
        return True