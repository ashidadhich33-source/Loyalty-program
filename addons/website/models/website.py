# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Management
=====================================

Website management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    """Website"""
    
    _name = 'website'
    _description = 'Website'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Website Name',
        required=True,
        help='Website name'
    )
    
    domain = fields.Char(
        string='Domain',
        required=True,
        help='Website domain (e.g., www.kidsclothing.com)'
    )
    
    url = fields.Char(
        string='URL',
        compute='_compute_url',
        store=True,
        help='Full website URL'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this website belongs to'
    )
    
    # Website Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this website is active'
    )
    
    is_default = fields.Boolean(
        string='Default Website',
        default=False,
        help='Whether this is the default website'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering websites'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this website')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this website')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this website focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this website')
    
    # Design Settings
    theme_id = fields.Many2one(
        'website.theme',
        string='Theme',
        help='Website theme'
    )
    
    color_scheme = fields.Selection([
        ('bright', 'Bright & Colorful'),
        ('pastel', 'Pastel & Soft'),
        ('neutral', 'Neutral & Classic'),
        ('vibrant', 'Vibrant & Bold'),
        ('custom', 'Custom'),
    ], string='Color Scheme', default='bright', help='Website color scheme')
    
    primary_color = fields.Char(
        string='Primary Color',
        default='#FF6B6B',
        help='Primary color for the website'
    )
    
    secondary_color = fields.Char(
        string='Secondary Color',
        default='#4ECDC4',
        help='Secondary color for the website'
    )
    
    # SEO Settings
    meta_title = fields.Char(
        string='Meta Title',
        help='Website meta title for SEO'
    )
    
    meta_description = fields.Text(
        string='Meta Description',
        help='Website meta description for SEO'
    )
    
    meta_keywords = fields.Char(
        string='Meta Keywords',
        help='Website meta keywords for SEO'
    )
    
    # Analytics Settings
    google_analytics_id = fields.Char(
        string='Google Analytics ID',
        help='Google Analytics tracking ID'
    )
    
    google_tag_manager_id = fields.Char(
        string='Google Tag Manager ID',
        help='Google Tag Manager ID'
    )
    
    facebook_pixel_id = fields.Char(
        string='Facebook Pixel ID',
        help='Facebook Pixel tracking ID'
    )
    
    # Social Media Settings
    facebook_url = fields.Char(
        string='Facebook URL',
        help='Facebook page URL'
    )
    
    instagram_url = fields.Char(
        string='Instagram URL',
        help='Instagram profile URL'
    )
    
    twitter_url = fields.Char(
        string='Twitter URL',
        help='Twitter profile URL'
    )
    
    youtube_url = fields.Char(
        string='YouTube URL',
        help='YouTube channel URL'
    )
    
    # Contact Information
    contact_email = fields.Char(
        string='Contact Email',
        help='Contact email address'
    )
    
    contact_phone = fields.Char(
        string='Contact Phone',
        help='Contact phone number'
    )
    
    contact_address = fields.Text(
        string='Contact Address',
        help='Contact address'
    )
    
    # Indian Localization
    gst_number = fields.Char(
        string='GST Number',
        help='GST registration number'
    )
    
    pan_number = fields.Char(
        string='PAN Number',
        help='PAN number'
    )
    
    # Website Pages
    page_ids = fields.One2many(
        'website.page',
        'website_id',
        string='Pages',
        help='Website pages'
    )
    
    # Analytics
    total_pages = fields.Integer(
        string='Total Pages',
        compute='_compute_analytics',
        store=True,
        help='Total number of pages'
    )
    
    total_visitors = fields.Integer(
        string='Total Visitors',
        compute='_compute_analytics',
        store=True,
        help='Total number of visitors'
    )
    
    total_page_views = fields.Integer(
        string='Total Page Views',
        compute='_compute_analytics',
        store=True,
        help='Total number of page views'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this website'
    )
    
    @api.depends('domain')
    def _compute_url(self):
        """Compute website URL"""
        for website in self:
            if website.domain:
                website.url = f"https://{website.domain}"
            else:
                website.url = False
    
    @api.depends('page_ids')
    def _compute_analytics(self):
        """Compute analytics"""
        for website in self:
            website.total_pages = len(website.page_ids)
            # This would be computed from analytics data
            website.total_visitors = 0
            website.total_page_views = 0
    
    @api.constrains('domain')
    def _check_domain(self):
        """Validate domain"""
        for website in self:
            if not website.domain:
                raise ValidationError(_('Domain is required.'))
            
            # Check for duplicate domains
            duplicate = self.search([
                ('domain', '=', website.domain),
                ('id', '!=', website.id)
            ])
            if duplicate:
                raise ValidationError(_('Domain must be unique.'))
    
    @api.constrains('is_default')
    def _check_default(self):
        """Validate default website"""
        for website in self:
            if website.is_default:
                # Ensure only one default website per company
                other_default = self.search([
                    ('company_id', '=', website.company_id.id),
                    ('is_default', '=', True),
                    ('id', '!=', website.id)
                ])
                if other_default:
                    other_default.write({'is_default': False})
    
    def action_view_pages(self):
        """View website pages"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Website Pages'),
            'res_model': 'website.page',
            'view_mode': 'tree,form',
            'domain': [('website_id', '=', self.id)],
            'context': {'default_website_id': self.id},
        }
    
    def action_create_page(self):
        """Create new page"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Page'),
            'res_model': 'website.page',
            'view_mode': 'form',
            'context': {'default_website_id': self.id},
        }
    
    def action_view_analytics(self):
        """View website analytics"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Website Analytics'),
            'res_model': 'website.analytics',
            'view_mode': 'tree,form',
            'domain': [('website_id', '=', self.id)],
            'context': {'default_website_id': self.id},
        }
    
    def get_website_analytics(self, date_from=None, date_to=None):
        """Get website analytics for date range"""
        self.ensure_one()
        # This would query analytics data
        # For now, returning basic info
        return {
            'total_pages': self.total_pages,
            'total_visitors': self.total_visitors,
            'total_page_views': self.total_page_views,
        }