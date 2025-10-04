# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Content Management
=============================================

Website content management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class WebsiteContent(models.Model):
    """Website Content"""
    
    _name = 'website.content'
    _description = 'Website Content'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Content Name',
        required=True,
        help='Content name'
    )
    
    title = fields.Char(
        string='Title',
        help='Content title'
    )
    
    # Content Type
    content_type = fields.Selection([
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('gallery', 'Image Gallery'),
        ('slider', 'Image Slider'),
        ('banner', 'Banner'),
        ('testimonial', 'Testimonial'),
        ('product_showcase', 'Product Showcase'),
        ('newsletter', 'Newsletter Signup'),
        ('contact_form', 'Contact Form'),
        ('custom', 'Custom'),
    ], string='Content Type', required=True, help='Type of content')
    
    # Content Data
    text_content = fields.Html(
        string='Text Content',
        help='Text content'
    )
    
    image_url = fields.Char(
        string='Image URL',
        help='Image URL'
    )
    
    video_url = fields.Char(
        string='Video URL',
        help='Video URL'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this content belongs to'
    )
    
    page_id = fields.Many2one(
        'website.page',
        string='Page',
        help='Page this content belongs to'
    )
    
    # Content Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this content is active'
    )
    
    is_published = fields.Boolean(
        string='Published',
        default=False,
        help='Whether this content is published'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering content'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this content')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this content')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this content focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this content')
    
    # Display Settings
    display_position = fields.Selection([
        ('header', 'Header'),
        ('hero', 'Hero Section'),
        ('content', 'Content Area'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('popup', 'Popup'),
        ('custom', 'Custom'),
    ], string='Display Position', help='Where to display this content')
    
    display_style = fields.Selection([
        ('full_width', 'Full Width'),
        ('container', 'Container'),
        ('card', 'Card'),
        ('banner', 'Banner'),
        ('custom', 'Custom'),
    ], string='Display Style', help='How to display this content')
    
    # Responsive Settings
    show_on_desktop = fields.Boolean(
        string='Show on Desktop',
        default=True,
        help='Whether to show this content on desktop'
    )
    
    show_on_tablet = fields.Boolean(
        string='Show on Tablet',
        default=True,
        help='Whether to show this content on tablet'
    )
    
    show_on_mobile = fields.Boolean(
        string='Show on Mobile',
        default=True,
        help='Whether to show this content on mobile'
    )
    
    # Analytics
    total_views = fields.Integer(
        string='Total Views',
        compute='_compute_analytics',
        store=True,
        help='Total number of content views'
    )
    
    engagement_rate = fields.Float(
        string='Engagement Rate (%)',
        compute='_compute_analytics',
        store=True,
        help='Content engagement rate percentage'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this content'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for content in self:
            # This would be computed from analytics data
            content.total_views = 0
            content.engagement_rate = 0.0
    
    def action_publish(self):
        """Publish content"""
        for content in self:
            if not content.is_active:
                raise UserError(_('Only active content can be published.'))
            
            content.is_published = True
    
    def action_unpublish(self):
        """Unpublish content"""
        for content in self:
            content.is_published = False
    
    def action_preview(self):
        """Preview content"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/website/content_preview/{self.id}',
            'target': 'new',
        }
    
    def get_content_analytics(self, date_from=None, date_to=None):
        """Get content analytics for date range"""
        self.ensure_one()
        # This would query analytics data
        # For now, returning basic info
        return {
            'total_views': self.total_views,
            'engagement_rate': self.engagement_rate,
        }


class WebsiteGallery(models.Model):
    """Website Gallery"""
    
    _name = 'website.gallery'
    _description = 'Website Gallery'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Gallery Name',
        required=True,
        help='Gallery name'
    )
    
    description = fields.Text(
        string='Description',
        help='Gallery description'
    )
    
    # Gallery Images
    image_ids = fields.One2many(
        'website.gallery.image',
        'gallery_id',
        string='Images',
        help='Gallery images'
    )
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this gallery belongs to'
    )
    
    # Gallery Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this gallery is active'
    )
    
    is_published = fields.Boolean(
        string='Published',
        default=False,
        help='Whether this gallery is published'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering galleries'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this gallery')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this gallery')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this gallery focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this gallery')
    
    # Display Settings
    gallery_type = fields.Selection([
        ('grid', 'Grid Gallery'),
        ('slider', 'Image Slider'),
        ('masonry', 'Masonry Gallery'),
        ('carousel', 'Carousel'),
        ('lightbox', 'Lightbox Gallery'),
    ], string='Gallery Type', help='Type of gallery display')
    
    # Analytics
    total_views = fields.Integer(
        string='Total Views',
        compute='_compute_analytics',
        store=True,
        help='Total number of gallery views'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this gallery'
    )
    
    @api.depends('image_ids')
    def _compute_analytics(self):
        """Compute analytics"""
        for gallery in self:
            # This would be computed from analytics data
            gallery.total_views = 0
    
    def action_publish(self):
        """Publish gallery"""
        for gallery in self:
            if not gallery.is_active:
                raise UserError(_('Only active galleries can be published.'))
            
            gallery.is_published = True
    
    def action_unpublish(self):
        """Unpublish gallery"""
        for gallery in self:
            gallery.is_published = False


class WebsiteGalleryImage(models.Model):
    """Website Gallery Image"""
    
    _name = 'website.gallery.image'
    _description = 'Website Gallery Image'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Image Name',
        required=True,
        help='Image name'
    )
    
    image_url = fields.Char(
        string='Image URL',
        required=True,
        help='Image URL'
    )
    
    alt_text = fields.Char(
        string='Alt Text',
        help='Image alt text for accessibility'
    )
    
    caption = fields.Text(
        string='Caption',
        help='Image caption'
    )
    
    # Gallery Information
    gallery_id = fields.Many2one(
        'website.gallery',
        string='Gallery',
        required=True,
        ondelete='cascade',
        help='Gallery this image belongs to'
    )
    
    # Image Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this image is active'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering images'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this image')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this image')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this image focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this image')
    
    # Analytics
    total_views = fields.Integer(
        string='Total Views',
        compute='_compute_analytics',
        store=True,
        help='Total number of image views'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this image'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for image in self:
            # This would be computed from analytics data
            image.total_views = 0