# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Page Management
==========================================

Website page management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class WebsitePage(models.Model):
    """Website Page"""
    
    _name = 'website.page'
    _description = 'Website Page'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Page Name',
        required=True,
        help='Page name'
    )
    
    url = fields.Char(
        string='URL',
        required=True,
        help='Page URL (e.g., /about-us)'
    )
    
    title = fields.Char(
        string='Page Title',
        required=True,
        help='Page title displayed in browser'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this page belongs to'
    )
    
    # Page Type
    page_type = fields.Selection([
        ('home', 'Home Page'),
        ('product', 'Product Page'),
        ('category', 'Category Page'),
        ('about', 'About Us'),
        ('contact', 'Contact'),
        ('blog', 'Blog'),
        ('news', 'News'),
        ('custom', 'Custom Page'),
    ], string='Page Type', required=True, help='Type of page')
    
    # Template
    template_id = fields.Many2one(
        'website.template',
        string='Template',
        help='Page template'
    )
    
    # Content
    content = fields.Html(
        string='Content',
        help='Page content'
    )
    
    # Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this page is active'
    )
    
    is_published = fields.Boolean(
        string='Published',
        default=False,
        help='Whether this page is published'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering pages'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this page')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this page')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this page focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this page')
    
    # SEO Settings
    meta_title = fields.Char(
        string='Meta Title',
        help='Page meta title for SEO'
    )
    
    meta_description = fields.Text(
        string='Meta Description',
        help='Page meta description for SEO'
    )
    
    meta_keywords = fields.Char(
        string='Meta Keywords',
        help='Page meta keywords for SEO'
    )
    
    # Navigation
    show_in_menu = fields.Boolean(
        string='Show in Menu',
        default=True,
        help='Whether to show this page in navigation menu'
    )
    
    menu_parent_id = fields.Many2one(
        'website.menu',
        string='Parent Menu',
        help='Parent menu item'
    )
    
    # Analytics
    total_views = fields.Integer(
        string='Total Views',
        compute='_compute_analytics',
        store=True,
        help='Total number of page views'
    )
    
    unique_visitors = fields.Integer(
        string='Unique Visitors',
        compute='_compute_analytics',
        store=True,
        help='Number of unique visitors'
    )
    
    bounce_rate = fields.Float(
        string='Bounce Rate (%)',
        compute='_compute_analytics',
        store=True,
        help='Page bounce rate percentage'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this page'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for page in self:
            # This would be computed from analytics data
            page.total_views = 0
            page.unique_visitors = 0
            page.bounce_rate = 0.0
    
    @api.constrains('url')
    def _check_url(self):
        """Validate page URL"""
        for page in self:
            if not page.url:
                raise ValidationError(_('Page URL is required.'))
            
            if not page.url.startswith('/'):
                raise ValidationError(_('Page URL must start with /'))
            
            # Check for duplicate URLs within the same website
            duplicate = self.search([
                ('url', '=', page.url),
                ('website_id', '=', page.website_id.id),
                ('id', '!=', page.id)
            ])
            if duplicate:
                raise ValidationError(_('Page URL must be unique within the website.'))
    
    @api.constrains('page_type')
    def _check_page_type(self):
        """Validate page type"""
        for page in self:
            if page.page_type == 'home' and page.url != '/':
                raise ValidationError(_('Home page must have URL "/"'))
    
    def action_publish(self):
        """Publish page"""
        for page in self:
            if not page.is_active:
                raise UserError(_('Only active pages can be published.'))
            
            page.is_published = True
    
    def action_unpublish(self):
        """Unpublish page"""
        for page in self:
            page.is_published = False
    
    def action_preview(self):
        """Preview page"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f"{self.website_id.url}{self.url}",
            'target': 'new',
        }
    
    def action_view_analytics(self):
        """View page analytics"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Page Analytics'),
            'res_model': 'website.analytics',
            'view_mode': 'tree,form',
            'domain': [('page_id', '=', self.id)],
            'context': {'default_page_id': self.id},
        }
    
    def get_page_analytics(self, date_from=None, date_to=None):
        """Get page analytics for date range"""
        self.ensure_one()
        # This would query analytics data
        # For now, returning basic info
        return {
            'total_views': self.total_views,
            'unique_visitors': self.unique_visitors,
            'bounce_rate': self.bounce_rate,
        }


class WebsiteMenu(models.Model):
    """Website Menu"""
    
    _name = 'website.menu'
    _description = 'Website Menu'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Menu Name',
        required=True,
        help='Menu item name'
    )
    
    url = fields.Char(
        string='URL',
        help='Menu item URL'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this menu belongs to'
    )
    
    # Hierarchy
    parent_id = fields.Many2one(
        'website.menu',
        string='Parent Menu',
        help='Parent menu item'
    )
    
    child_ids = fields.One2many(
        'website.menu',
        'parent_id',
        string='Child Menus',
        help='Child menu items'
    )
    
    # Page
    page_id = fields.Many2one(
        'website.page',
        string='Page',
        help='Page this menu item links to'
    )
    
    # Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this menu item is active'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering menu items'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this menu item')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this menu item')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this menu item focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this menu item')
    
    @api.constrains('parent_id')
    def _check_parent(self):
        """Validate parent menu"""
        for menu in self:
            if menu.parent_id:
                if menu.parent_id == menu:
                    raise ValidationError(_('Menu cannot be its own parent.'))
                
                if menu.parent_id.parent_id == menu:
                    raise ValidationError(_('Menu cannot be parent of its parent.'))
    
    def name_get(self):
        """Return display name"""
        result = []
        for menu in self:
            result.append((menu.id, menu.name))
        return result