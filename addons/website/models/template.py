# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Template Management
==============================================

Website template management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class WebsiteTemplate(models.Model):
    """Website Template"""
    
    _name = 'website.template'
    _description = 'Website Template'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Template Name',
        required=True,
        help='Template name'
    )
    
    code = fields.Char(
        string='Template Code',
        required=True,
        help='Template code (e.g., kids_clothing_home)'
    )
    
    description = fields.Text(
        string='Description',
        help='Template description'
    )
    
    # Template Type
    template_type = fields.Selection([
        ('home', 'Home Page'),
        ('product', 'Product Page'),
        ('category', 'Category Page'),
        ('about', 'About Us'),
        ('contact', 'Contact'),
        ('blog', 'Blog'),
        ('news', 'News'),
        ('custom', 'Custom'),
    ], string='Template Type', required=True, help='Type of template')
    
    # Template Content
    html_content = fields.Html(
        string='HTML Content',
        help='Template HTML content'
    )
    
    css_content = fields.Text(
        string='CSS Content',
        help='Template CSS content'
    )
    
    js_content = fields.Text(
        string='JavaScript Content',
        help='Template JavaScript content'
    )
    
    # Template Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this template is active'
    )
    
    is_default = fields.Boolean(
        string='Default Template',
        default=False,
        help='Whether this is the default template for its type'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering templates'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this template')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this template')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this template focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this template')
    
    # Design Settings
    color_scheme = fields.Selection([
        ('bright', 'Bright & Colorful'),
        ('pastel', 'Pastel & Soft'),
        ('neutral', 'Neutral & Classic'),
        ('vibrant', 'Vibrant & Bold'),
        ('custom', 'Custom'),
    ], string='Color Scheme', help='Template color scheme')
    
    layout_type = fields.Selection([
        ('single_column', 'Single Column'),
        ('two_column', 'Two Column'),
        ('three_column', 'Three Column'),
        ('grid', 'Grid Layout'),
        ('masonry', 'Masonry Layout'),
        ('custom', 'Custom Layout'),
    ], string='Layout Type', help='Template layout type')
    
    # Responsive Settings
    is_responsive = fields.Boolean(
        string='Responsive',
        default=True,
        help='Whether this template is responsive'
    )
    
    mobile_optimized = fields.Boolean(
        string='Mobile Optimized',
        default=True,
        help='Whether this template is mobile optimized'
    )
    
    tablet_optimized = fields.Boolean(
        string='Tablet Optimized',
        default=True,
        help='Whether this template is tablet optimized'
    )
    
    # SEO Settings
    seo_friendly = fields.Boolean(
        string='SEO Friendly',
        default=True,
        help='Whether this template is SEO friendly'
    )
    
    meta_tags_included = fields.Boolean(
        string='Meta Tags Included',
        default=True,
        help='Whether meta tags are included in template'
    )
    
    # Analytics
    total_usage = fields.Integer(
        string='Total Usage',
        compute='_compute_analytics',
        store=True,
        help='Total number of times this template is used'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this template'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for template in self:
            # This would be computed from usage data
            template.total_usage = 0
    
    @api.constrains('code')
    def _check_code(self):
        """Validate template code"""
        for template in self:
            if not template.code:
                raise ValidationError(_('Template code is required.'))
            
            # Check for duplicate codes
            duplicate = self.search([
                ('code', '=', template.code),
                ('id', '!=', template.id)
            ])
            if duplicate:
                raise ValidationError(_('Template code must be unique.'))
    
    @api.constrains('is_default', 'template_type')
    def _check_default(self):
        """Validate default template"""
        for template in self:
            if template.is_default:
                # Ensure only one default template per type
                other_default = self.search([
                    ('template_type', '=', template.template_type),
                    ('is_default', '=', True),
                    ('id', '!=', template.id)
                ])
                if other_default:
                    other_default.write({'is_default': False})
    
    def action_preview(self):
        """Preview template"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/website/template_preview/{self.id}',
            'target': 'new',
        }
    
    def action_duplicate(self):
        """Duplicate template"""
        self.ensure_one()
        new_template = self.copy({
            'name': f"{self.name} (Copy)",
            'code': f"{self.code}_copy",
            'is_default': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Duplicated Template'),
            'res_model': 'website.template',
            'view_mode': 'form',
            'res_id': new_template.id,
        }
    
    def get_template_analytics(self):
        """Get template analytics"""
        self.ensure_one()
        # This would query usage data
        # For now, returning basic info
        return {
            'total_usage': self.total_usage,
        }


class WebsiteTheme(models.Model):
    """Website Theme"""
    
    _name = 'website.theme'
    _description = 'Website Theme'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Theme Name',
        required=True,
        help='Theme name'
    )
    
    code = fields.Char(
        string='Theme Code',
        required=True,
        help='Theme code (e.g., kids_clothing_bright)'
    )
    
    description = fields.Text(
        string='Description',
        help='Theme description'
    )
    
    # Theme Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this theme is active'
    )
    
    is_default = fields.Boolean(
        string='Default Theme',
        default=False,
        help='Whether this is the default theme'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering themes'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this theme')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this theme')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this theme focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this theme')
    
    # Design Settings
    color_scheme = fields.Selection([
        ('bright', 'Bright & Colorful'),
        ('pastel', 'Pastel & Soft'),
        ('neutral', 'Neutral & Classic'),
        ('vibrant', 'Vibrant & Bold'),
        ('custom', 'Custom'),
    ], string='Color Scheme', help='Theme color scheme')
    
    primary_color = fields.Char(
        string='Primary Color',
        help='Primary color for the theme'
    )
    
    secondary_color = fields.Char(
        string='Secondary Color',
        help='Secondary color for the theme'
    )
    
    accent_color = fields.Char(
        string='Accent Color',
        help='Accent color for the theme'
    )
    
    # Typography
    font_family = fields.Char(
        string='Font Family',
        help='Font family for the theme'
    )
    
    font_size = fields.Char(
        string='Font Size',
        help='Font size for the theme'
    )
    
    # Layout
    layout_width = fields.Selection([
        ('fixed', 'Fixed Width'),
        ('fluid', 'Fluid Width'),
        ('responsive', 'Responsive'),
    ], string='Layout Width', help='Theme layout width')
    
    sidebar_position = fields.Selection([
        ('left', 'Left Sidebar'),
        ('right', 'Right Sidebar'),
        ('none', 'No Sidebar'),
    ], string='Sidebar Position', help='Sidebar position')
    
    # Analytics
    total_usage = fields.Integer(
        string='Total Usage',
        compute='_compute_analytics',
        store=True,
        help='Total number of times this theme is used'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this theme'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for theme in self:
            # This would be computed from usage data
            theme.total_usage = 0
    
    @api.constrains('code')
    def _check_code(self):
        """Validate theme code"""
        for theme in self:
            if not theme.code:
                raise ValidationError(_('Theme code is required.'))
            
            # Check for duplicate codes
            duplicate = self.search([
                ('code', '=', theme.code),
                ('id', '!=', theme.id)
            ])
            if duplicate:
                raise ValidationError(_('Theme code must be unique.'))
    
    @api.constrains('is_default')
    def _check_default(self):
        """Validate default theme"""
        for theme in self:
            if theme.is_default:
                # Ensure only one default theme
                other_default = self.search([
                    ('is_default', '=', True),
                    ('id', '!=', theme.id)
                ])
                if other_default:
                    other_default.write({'is_default': False})
    
    def action_preview(self):
        """Preview theme"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/website/theme_preview/{self.id}',
            'target': 'new',
        }
    
    def get_theme_analytics(self):
        """Get theme analytics"""
        self.ensure_one()
        # This would query usage data
        # For now, returning basic info
        return {
            'total_usage': self.total_usage,
        }