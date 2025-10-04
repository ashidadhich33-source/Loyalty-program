# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Analytics Management
===============================================

Website analytics management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)


class WebsiteAnalytics(models.Model):
    """Website Analytics"""
    
    _name = 'website.analytics'
    _description = 'Website Analytics'
    _order = 'date desc'
    
    # Basic Information
    name = fields.Char(
        string='Analytics Name',
        compute='_compute_name',
        store=True,
        help='Analytics name'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this analytics belongs to'
    )
    
    page_id = fields.Many2one(
        'website.page',
        string='Page',
        help='Page this analytics belongs to'
    )
    
    # Date Information
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        help='Analytics date'
    )
    
    # Traffic Metrics
    total_visitors = fields.Integer(
        string='Total Visitors',
        default=0,
        help='Total number of visitors'
    )
    
    unique_visitors = fields.Integer(
        string='Unique Visitors',
        default=0,
        help='Number of unique visitors'
    )
    
    total_page_views = fields.Integer(
        string='Total Page Views',
        default=0,
        help='Total number of page views'
    )
    
    avg_session_duration = fields.Float(
        string='Avg Session Duration (minutes)',
        default=0.0,
        help='Average session duration in minutes'
    )
    
    bounce_rate = fields.Float(
        string='Bounce Rate (%)',
        default=0.0,
        help='Bounce rate percentage'
    )
    
    # Geographic Data
    country = fields.Char(
        string='Country',
        help='Visitor country'
    )
    
    state = fields.Char(
        string='State',
        help='Visitor state'
    )
    
    city = fields.Char(
        string='City',
        help='Visitor city'
    )
    
    # Device Information
    device_type = fields.Selection([
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
    ], string='Device Type', help='Visitor device type')
    
    browser = fields.Char(
        string='Browser',
        help='Visitor browser'
    )
    
    operating_system = fields.Char(
        string='Operating System',
        help='Visitor operating system'
    )
    
    # Traffic Sources
    traffic_source = fields.Selection([
        ('direct', 'Direct'),
        ('search', 'Search Engine'),
        ('social', 'Social Media'),
        ('referral', 'Referral'),
        ('email', 'Email'),
        ('paid', 'Paid Advertising'),
        ('other', 'Other'),
    ], string='Traffic Source', help='Traffic source')
    
    referrer_url = fields.Char(
        string='Referrer URL',
        help='Referrer URL'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this analytics')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this analytics')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this analytics focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this analytics')
    
    # Conversion Metrics
    total_conversions = fields.Integer(
        string='Total Conversions',
        default=0,
        help='Total number of conversions'
    )
    
    conversion_rate = fields.Float(
        string='Conversion Rate (%)',
        default=0.0,
        help='Conversion rate percentage'
    )
    
    # Revenue Metrics
    total_revenue = fields.Float(
        string='Total Revenue',
        default=0.0,
        help='Total revenue generated'
    )
    
    avg_order_value = fields.Float(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this analytics'
    )
    
    @api.depends('website_id', 'page_id', 'date')
    def _compute_name(self):
        """Compute analytics name"""
        for analytics in self:
            if analytics.page_id:
                analytics.name = f"{analytics.website_id.name} - {analytics.page_id.name} - {analytics.date}"
            else:
                analytics.name = f"{analytics.website_id.name} - {analytics.date}"
    
    @api.constrains('date')
    def _check_date(self):
        """Validate date"""
        for analytics in self:
            if analytics.date > fields.Date.context_today(self):
                raise ValidationError(_('Analytics date cannot be in the future.'))
    
    def get_analytics_summary(self, date_from=None, date_to=None):
        """Get analytics summary for date range"""
        self.ensure_one()
        # This would query analytics data
        # For now, returning basic info
        return {
            'total_visitors': self.total_visitors,
            'unique_visitors': self.unique_visitors,
            'total_page_views': self.total_page_views,
            'avg_session_duration': self.avg_session_duration,
            'bounce_rate': self.bounce_rate,
            'conversion_rate': self.conversion_rate,
            'total_revenue': self.total_revenue,
        }


class WebsiteVisitor(models.Model):
    """Website Visitor"""
    
    _name = 'website.visitor'
    _description = 'Website Visitor'
    _order = 'last_visit desc'
    
    # Basic Information
    name = fields.Char(
        string='Visitor Name',
        compute='_compute_name',
        store=True,
        help='Visitor name'
    )
    
    visitor_id = fields.Char(
        string='Visitor ID',
        required=True,
        help='Unique visitor identifier'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this visitor belongs to'
    )
    
    # Visit Information
    first_visit = fields.Datetime(
        string='First Visit',
        help='First visit date and time'
    )
    
    last_visit = fields.Datetime(
        string='Last Visit',
        help='Last visit date and time'
    )
    
    total_visits = fields.Integer(
        string='Total Visits',
        default=0,
        help='Total number of visits'
    )
    
    total_page_views = fields.Integer(
        string='Total Page Views',
        default=0,
        help='Total number of page views'
    )
    
    # Geographic Information
    country = fields.Char(
        string='Country',
        help='Visitor country'
    )
    
    state = fields.Char(
        string='State',
        help='Visitor state'
    )
    
    city = fields.Char(
        string='City',
        help='Visitor city'
    )
    
    # Device Information
    device_type = fields.Selection([
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
    ], string='Device Type', help='Visitor device type')
    
    browser = fields.Char(
        string='Browser',
        help='Visitor browser'
    )
    
    operating_system = fields.Char(
        string='Operating System',
        help='Visitor operating system'
    )
    
    # Contact Information
    contact_id = fields.Many2one(
        'res.partner',
        string='Contact',
        help='Associated contact'
    )
    
    email = fields.Char(
        string='Email',
        help='Visitor email'
    )
    
    phone = fields.Char(
        string='Phone',
        help='Visitor phone'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this visitor')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this visitor')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this visitor is interested in'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this visitor')
    
    # Behavior
    is_returning = fields.Boolean(
        string='Returning Visitor',
        default=False,
        help='Whether this is a returning visitor'
    )
    
    is_converted = fields.Boolean(
        string='Converted',
        default=False,
        help='Whether this visitor has converted'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this visitor'
    )
    
    @api.depends('visitor_id', 'email', 'contact_id')
    def _compute_name(self):
        """Compute visitor name"""
        for visitor in self:
            if visitor.contact_id:
                visitor.name = visitor.contact_id.name
            elif visitor.email:
                visitor.name = visitor.email
            else:
                visitor.name = visitor.visitor_id
    
    @api.constrains('visitor_id', 'website_id')
    def _check_visitor_id(self):
        """Validate visitor ID"""
        for visitor in self:
            if not visitor.visitor_id:
                raise ValidationError(_('Visitor ID is required.'))
            
            # Check for duplicate visitor IDs within the same website
            duplicate = self.search([
                ('visitor_id', '=', visitor.visitor_id),
                ('website_id', '=', visitor.website_id.id),
                ('id', '!=', visitor.id)
            ])
            if duplicate:
                raise ValidationError(_('Visitor ID must be unique within the website.'))
    
    def action_create_contact(self):
        """Create contact from visitor"""
        self.ensure_one()
        if self.contact_id:
            raise UserError(_('Visitor already has an associated contact.'))
        
        contact_vals = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'is_company': False,
        }
        
        contact = self.env['res.partner'].create(contact_vals)
        self.contact_id = contact.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Created Contact'),
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': contact.id,
        }
    
    def get_visitor_analytics(self):
        """Get visitor analytics"""
        self.ensure_one()
        # This would query visitor data
        # For now, returning basic info
        return {
            'total_visits': self.total_visits,
            'total_page_views': self.total_page_views,
            'is_returning': self.is_returning,
            'is_converted': self.is_converted,
        }