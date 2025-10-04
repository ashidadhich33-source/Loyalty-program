# -*- coding: utf-8 -*-
"""
Ocean ERP - Addon Marketplace Models
===================================

Addon marketplace models for Ocean ERP.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, SelectionField, FloatField
from typing import Dict, Any, Optional, List
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AddonMarketplace(BaseModel):
    """Addon Marketplace model for Ocean ERP"""
    
    _name = 'addon.marketplace'
    _description = 'Addon Marketplace'
    _table = 'addon_marketplace'
    
    # Basic fields
    name = CharField(
        string='Addon Name',
        size=255,
        required=True,
        help='Name of the addon'
    )
    
    technical_name = CharField(
        string='Technical Name',
        size=255,
        required=True,
        help='Technical name of the addon'
    )
    
    version = CharField(
        string='Version',
        size=50,
        default='1.0.0',
        help='Addon version'
    )
    
    summary = CharField(
        string='Summary',
        size=255,
        help='Short description of the addon'
    )
    
    description = TextField(
        string='Description',
        help='Detailed description of the addon'
    )
    
    # Marketplace details
    author = CharField(
        string='Author',
        size=255,
        help='Addon author'
    )
    
    author_email = CharField(
        string='Author Email',
        size=255,
        help='Author email'
    )
    
    website = CharField(
        string='Website',
        size=255,
        help='Addon website'
    )
    
    license = CharField(
        string='License',
        size=100,
        default='LGPL-3',
        help='Addon license'
    )
    
    # Pricing
    price = FloatField(
        string='Price',
        default=0.0,
        help='Addon price'
    )
    
    currency = CharField(
        string='Currency',
        size=10,
        default='USD',
        help='Price currency'
    )
    
    is_free = BooleanField(
        string='Free',
        default=True,
        help='Whether addon is free'
    )
    
    # Marketplace status
    status = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('published', 'Published'),
            ('unpublished', 'Unpublished'),
        ],
        default='draft',
        help='Marketplace status'
    )
    
    is_featured = BooleanField(
        string='Featured',
        default=False,
        help='Whether addon is featured'
    )
    
    is_popular = BooleanField(
        string='Popular',
        default=False,
        help='Whether addon is popular'
    )
    
    # Metrics
    download_count = IntegerField(
        string='Download Count',
        default=0,
        help='Number of downloads'
    )
    
    rating = FloatField(
        string='Rating',
        default=0.0,
        help='Addon rating (0-5)'
    )
    
    review_count = IntegerField(
        string='Review Count',
        default=0,
        help='Number of reviews'
    )
    
    # Categories and tags
    category = CharField(
        string='Category',
        size=100,
        help='Addon category'
    )
    
    tags = TextField(
        string='Tags',
        help='Addon tags (JSON format)'
    )
    
    # Compatibility
    min_version = CharField(
        string='Minimum Version',
        size=50,
        help='Minimum Ocean ERP version required'
    )
    
    max_version = CharField(
        string='Maximum Version',
        size=50,
        help='Maximum Ocean ERP version supported'
    )
    
    # Files and downloads
    download_url = CharField(
        string='Download URL',
        size=255,
        help='URL to download addon'
    )
    
    file_size = IntegerField(
        string='File Size (KB)',
        default=0,
        help='Addon file size in KB'
    )
    
    # Reviews and ratings
    reviews = TextField(
        string='Reviews',
        help='Addon reviews (JSON format)'
    )
    
    # Metadata
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when addon was created'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date when addon was last updated'
    )
    
    published_date = DateTimeField(
        string='Published Date',
        help='Date when addon was published'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        if 'technical_name' not in vals and 'name' in vals:
            vals['technical_name'] = vals['name'].lower().replace(' ', '_')
        
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle updates"""
        result = super().write(vals)
        
        # Update updated_date when any field changes
        if vals:
            for addon in self:
                addon.updated_date = datetime.now()
        
        # Set published_date when status changes to published
        if 'status' in vals and vals['status'] == 'published':
            for addon in self:
                if not addon.published_date:
                    addon.published_date = datetime.now()
        
        return result
    
    def action_publish(self):
        """Publish addon to marketplace"""
        self.ensure_one()
        
        self.write({
            'status': 'published',
            'published_date': datetime.now()
        })
        return True
    
    def action_unpublish(self):
        """Unpublish addon from marketplace"""
        self.ensure_one()
        
        self.write({
            'status': 'unpublished'
        })
        return True
    
    def action_feature(self):
        """Feature addon"""
        self.ensure_one()
        
        self.write({
            'is_featured': True
        })
        return True
    
    def action_unfeature(self):
        """Unfeature addon"""
        self.ensure_one()
        
        self.write({
            'is_featured': False
        })
        return True
    
    def add_review(self, review_data: Dict[str, Any]):
        """Add review to addon"""
        self.ensure_one()
        
        try:
            reviews = []
            if self.reviews:
                reviews = json.loads(self.reviews)
            
            # Add new review
            review_data['date'] = datetime.now().isoformat()
            reviews.append(review_data)
            
            # Update rating
            total_rating = sum(r.get('rating', 0) for r in reviews)
            avg_rating = total_rating / len(reviews) if reviews else 0
            
            self.write({
                'reviews': json.dumps(reviews),
                'review_count': len(reviews),
                'rating': avg_rating
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add review: {e}")
            return False
    
    def increment_download(self):
        """Increment download count"""
        self.ensure_one()
        
        self.write({
            'download_count': self.download_count + 1
        })
        return True
    
    def get_tags(self) -> List[str]:
        """Get addon tags"""
        try:
            if self.tags:
                return json.loads(self.tags)
            return []
        except:
            return []
    
    def set_tags(self, tags: List[str]):
        """Set addon tags"""
        self.ensure_one()
        
        self.write({
            'tags': json.dumps(tags)
        })
        return True
    
    def get_reviews(self) -> List[Dict[str, Any]]:
        """Get addon reviews"""
        try:
            if self.reviews:
                return json.loads(self.reviews)
            return []
        except:
            return []
    
    @classmethod
    def get_featured_addons(cls):
        """Get featured addons"""
        return cls.search([('is_featured', '=', True), ('status', '=', 'published')])
    
    @classmethod
    def get_popular_addons(cls):
        """Get popular addons"""
        return cls.search([('is_popular', '=', True), ('status', '=', 'published')])
    
    @classmethod
    def get_free_addons(cls):
        """Get free addons"""
        return cls.search([('is_free', '=', True), ('status', '=', 'published')])
    
    @classmethod
    def get_paid_addons(cls):
        """Get paid addons"""
        return cls.search([('is_free', '=', False), ('status', '=', 'published')])
    
    @classmethod
    def search_addons(cls, search_term: str = None, category: str = None, tags: List[str] = None):
        """Search addons"""
        domain = [('status', '=', 'published')]
        
        if search_term:
            domain.append(('name', 'ilike', search_term))
        
        if category:
            domain.append(('category', '=', category))
        
        if tags:
            # This would need more sophisticated tag searching
            pass
        
        return cls.search(domain)