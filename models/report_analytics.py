# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from collections import defaultdict


class ReportAnalytics(models.Model):
    _name = 'report.analytics'
    _description = 'Kids Clothing ERP Analytics'
    _auto = False

    # Date fields
    date = fields.Date(string='Date', readonly=True)
    month = fields.Char(string='Month', readonly=True)
    quarter = fields.Char(string='Quarter', readonly=True)
    year = fields.Integer(string='Year', readonly=True)
    
    # Sales metrics
    total_sales = fields.Float(string='Total Sales', readonly=True)
    total_orders = fields.Integer(string='Total Orders', readonly=True)
    avg_order_value = fields.Float(string='Average Order Value', readonly=True)
    
    # Age group sales
    newborn_sales = fields.Float(string='Newborn Sales', readonly=True)
    infant_sales = fields.Float(string='Infant Sales', readonly=True)
    toddler_sales = fields.Float(string='Toddler Sales', readonly=True)
    preschool_sales = fields.Float(string='Preschool Sales', readonly=True)
    child_sales = fields.Float(string='Child Sales', readonly=True)
    teen_sales = fields.Float(string='Teen Sales', readonly=True)
    
    # Gender sales
    boys_sales = fields.Float(string='Boys Sales', readonly=True)
    girls_sales = fields.Float(string='Girls Sales', readonly=True)
    unisex_sales = fields.Float(string='Unisex Sales', readonly=True)
    
    # Seasonal sales
    spring_sales = fields.Float(string='Spring Sales', readonly=True)
    summer_sales = fields.Float(string='Summer Sales', readonly=True)
    fall_sales = fields.Float(string='Fall Sales', readonly=True)
    winter_sales = fields.Float(string='Winter Sales', readonly=True)
    
    # Customer metrics
    new_customers = fields.Integer(string='New Customers', readonly=True)
    returning_customers = fields.Integer(string='Returning Customers', readonly=True)
    loyalty_points_earned = fields.Integer(string='Loyalty Points Earned', readonly=True)
    loyalty_points_used = fields.Integer(string='Loyalty Points Used', readonly=True)
    
    # Product metrics
    total_products_sold = fields.Integer(string='Total Products Sold', readonly=True)
    unique_products_sold = fields.Integer(string='Unique Products Sold', readonly=True)
    gift_wraps_sold = fields.Integer(string='Gift Wraps Sold', readonly=True)
    
    # Exchange/Return metrics
    exchanges_processed = fields.Integer(string='Exchanges Processed', readonly=True)
    returns_processed = fields.Integer(string='Returns Processed', readonly=True)
    exchange_return_rate = fields.Float(string='Exchange/Return Rate', readonly=True)
    
    def init(self):
        """Initialize the analytics view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    row_number() OVER () AS id,
                    so.date_order::date AS date,
                    to_char(so.date_order, 'YYYY-MM') AS month,
                    'Q' || EXTRACT(QUARTER FROM so.date_order) AS quarter,
                    EXTRACT(YEAR FROM so.date_order) AS year,
                    SUM(so.amount_total) AS total_sales,
                    COUNT(so.id) AS total_orders,
                    AVG(so.amount_total) AS avg_order_value,
                    SUM(CASE WHEN pt.age_group = 'newborn' THEN sol.price_subtotal ELSE 0 END) AS newborn_sales,
                    SUM(CASE WHEN pt.age_group = 'infant' THEN sol.price_subtotal ELSE 0 END) AS infant_sales,
                    SUM(CASE WHEN pt.age_group = 'toddler' THEN sol.price_subtotal ELSE 0 END) AS toddler_sales,
                    SUM(CASE WHEN pt.age_group = 'preschool' THEN sol.price_subtotal ELSE 0 END) AS preschool_sales,
                    SUM(CASE WHEN pt.age_group = 'child' THEN sol.price_subtotal ELSE 0 END) AS child_sales,
                    SUM(CASE WHEN pt.age_group = 'teen' THEN sol.price_subtotal ELSE 0 END) AS teen_sales,
                    SUM(CASE WHEN pt.gender = 'boys' THEN sol.price_subtotal ELSE 0 END) AS boys_sales,
                    SUM(CASE WHEN pt.gender = 'girls' THEN sol.price_subtotal ELSE 0 END) AS girls_sales,
                    SUM(CASE WHEN pt.gender = 'unisex' THEN sol.price_subtotal ELSE 0 END) AS unisex_sales,
                    SUM(CASE WHEN pt.season = 'spring' THEN sol.price_subtotal ELSE 0 END) AS spring_sales,
                    SUM(CASE WHEN pt.season = 'summer' THEN sol.price_subtotal ELSE 0 END) AS summer_sales,
                    SUM(CASE WHEN pt.season = 'fall' THEN sol.price_subtotal ELSE 0 END) AS fall_sales,
                    SUM(CASE WHEN pt.season = 'winter' THEN sol.price_subtotal ELSE 0 END) AS winter_sales,
                    COUNT(DISTINCT CASE WHEN rp.create_date::date = so.date_order::date THEN rp.id END) AS new_customers,
                    COUNT(DISTINCT CASE WHEN rp.create_date::date < so.date_order::date THEN rp.id END) AS returning_customers,
                    SUM(so.loyalty_points_earned) AS loyalty_points_earned,
                    SUM(so.loyalty_points_used) AS loyalty_points_used,
                    SUM(sol.product_uom_qty) AS total_products_sold,
                    COUNT(DISTINCT sol.product_id) AS unique_products_sold,
                    COUNT(CASE WHEN so.gift_wrap = true THEN 1 END) AS gift_wraps_sold,
                    COUNT(CASE WHEN so.is_exchange = true THEN 1 END) AS exchanges_processed,
                    COUNT(CASE WHEN so.is_return = true THEN 1 END) AS returns_processed,
                    CASE 
                        WHEN COUNT(so.id) > 0 THEN 
                            (COUNT(CASE WHEN so.is_exchange = true THEN 1 END) + 
                             COUNT(CASE WHEN so.is_return = true THEN 1 END))::float / COUNT(so.id) * 100
                        ELSE 0 
                    END AS exchange_return_rate
                FROM sale_order so
                LEFT JOIN sale_order_line sol ON sol.order_id = so.id
                LEFT JOIN product_product pp ON pp.id = sol.product_id
                LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
                LEFT JOIN res_partner rp ON rp.id = so.partner_id
                WHERE so.state IN ('sale', 'done')
                GROUP BY so.date_order::date, to_char(so.date_order, 'YYYY-MM'), 
                         EXTRACT(QUARTER FROM so.date_order), EXTRACT(YEAR FROM so.date_order)
                ORDER BY so.date_order::date DESC
            )
        """ % self._table)

    @api.model
    def get_sales_trends(self, days=30):
        """Get sales trends for the last N days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        return self.search([
            ('date', '>=', start_date),
            ('date', '<=', end_date),
        ], order='date ASC')
    
    @api.model
    def get_age_group_analysis(self, days=30):
        """Get age group sales analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'newborn': sum(trends.mapped('newborn_sales')),
            'infant': sum(trends.mapped('infant_sales')),
            'toddler': sum(trends.mapped('toddler_sales')),
            'preschool': sum(trends.mapped('preschool_sales')),
            'child': sum(trends.mapped('child_sales')),
            'teen': sum(trends.mapped('teen_sales')),
        }
    
    @api.model
    def get_gender_analysis(self, days=30):
        """Get gender sales analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'boys': sum(trends.mapped('boys_sales')),
            'girls': sum(trends.mapped('girls_sales')),
            'unisex': sum(trends.mapped('unisex_sales')),
        }
    
    @api.model
    def get_seasonal_analysis(self, days=30):
        """Get seasonal sales analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'spring': sum(trends.mapped('spring_sales')),
            'summer': sum(trends.mapped('summer_sales')),
            'fall': sum(trends.mapped('fall_sales')),
            'winter': sum(trends.mapped('winter_sales')),
        }
    
    @api.model
    def get_customer_analysis(self, days=30):
        """Get customer analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'new_customers': sum(trends.mapped('new_customers')),
            'returning_customers': sum(trends.mapped('returning_customers')),
            'loyalty_points_earned': sum(trends.mapped('loyalty_points_earned')),
            'loyalty_points_used': sum(trends.mapped('loyalty_points_used')),
        }
    
    @api.model
    def get_product_analysis(self, days=30):
        """Get product analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'total_products_sold': sum(trends.mapped('total_products_sold')),
            'unique_products_sold': max(trends.mapped('unique_products_sold')),
            'gift_wraps_sold': sum(trends.mapped('gift_wraps_sold')),
        }
    
    @api.model
    def get_exchange_return_analysis(self, days=30):
        """Get exchange/return analysis"""
        trends = self.get_sales_trends(days)
        
        return {
            'exchanges_processed': sum(trends.mapped('exchanges_processed')),
            'returns_processed': sum(trends.mapped('returns_processed')),
            'exchange_return_rate': sum(trends.mapped('exchange_return_rate')) / len(trends) if trends else 0,
        }
    
    @api.model
    def get_comprehensive_analytics(self, days=30):
        """Get comprehensive analytics for the specified period"""
        return {
            'sales_trends': self.get_sales_trends(days),
            'age_group_analysis': self.get_age_group_analysis(days),
            'gender_analysis': self.get_gender_analysis(days),
            'seasonal_analysis': self.get_seasonal_analysis(days),
            'customer_analysis': self.get_customer_analysis(days),
            'product_analysis': self.get_product_analysis(days),
            'exchange_return_analysis': self.get_exchange_return_analysis(days),
        }