# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Child Profile Management
====================================================

Standalone version of the child profile management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, DateField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class ChildProfile(BaseModel):
    """Child profile model for Kids Clothing ERP"""
    
    _name = 'child.profile'
    _description = 'Child Profile'
    _table = 'child_profile'
    
    # Basic child information
    name = CharField(
        string='Child Name',
        size=255,
        required=True,
        help='Name of the child'
    )
    
    parent_id = IntegerField(
        string='Parent ID',
        required=True,
        help='Parent contact'
    )
    
    date_of_birth = DateField(
        string='Date of Birth',
        help='Date of birth of the child'
    )
    
    age = IntegerField(
        string='Age',
        default=0,
        help='Age of the child in years'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('boy', 'Boy'),
            ('girl', 'Girl'),
            ('other', 'Other'),
        ],
        required=True,
        help='Gender of the child'
    )
    
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-3 months)'),
            ('infant', 'Infant (3-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school_age', 'School Age (6-12 years)'),
            ('teen', 'Teen (13-18 years)'),
        ],
        help='Age group of the child'
    )
    
    # Physical measurements
    current_height = FloatField(
        string='Current Height (cm)',
        default=0.0,
        help='Current height in cm'
    )
    
    current_weight = FloatField(
        string='Current Weight (kg)',
        default=0.0,
        help='Current weight in kg'
    )
    
    clothing_size = CharField(
        string='Clothing Size',
        size=20,
        help='Current clothing size'
    )
    
    shoe_size = CharField(
        string='Shoe Size',
        size=20,
        help='Current shoe size'
    )
    
    # Preferences
    favorite_colors = CharField(
        string='Favorite Colors',
        size=255,
        help='Favorite colors'
    )
    
    favorite_brands = Many2ManyField(
        string='Favorite Brands',
        comodel_name='product.brand',
        help='Favorite product brands'
    )
    
    preferred_styles = CharField(
        string='Preferred Styles',
        size=255,
        help='Preferred clothing styles'
    )
    
    # Health and special needs
    allergies = TextField(
        string='Allergies/Sensitivities',
        help='Allergies or sensitivities'
    )
    
    special_notes = TextField(
        string='Special Notes',
        help='Special notes about the child'
    )
    
    # Photo
    photo = CharField(
        string='Photo',
        size=255,
        help='Path to child photo'
    )
    
    # Company and status
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this child profile belongs to'
    )
    
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        default='active',
        help='Status of the child profile'
    )
    
    # Analytics
    total_purchases = IntegerField(
        string='Total Purchases',
        default=0,
        help='Total number of purchases for this child'
    )
    
    total_spent = FloatField(
        string='Total Spent',
        default=0.0,
        help='Total amount spent on this child'
    )
    
    last_purchase_date = DateTimeField(
        string='Last Purchase Date',
        help='Date of last purchase for this child'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        result = super().create(vals)
        
        # Compute age and age group
        for child in result:
            child._compute_age()
            child._compute_age_group()
        
        return result
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle child profile updates"""
        result = super().write(vals)
        
        # Update age and age group if date of birth changed
        if 'date_of_birth' in vals:
            for child in self:
                child._compute_age()
                child._compute_age_group()
        
        # Log child profile updates
        for child in self:
            if vals:
                logger.info(f"Child profile {child.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def _compute_age(self):
        """Compute age from date of birth"""
        for child in self:
            if child.date_of_birth:
                today = date.today()
                dob = datetime.strptime(child.date_of_birth, '%Y-%m-%d').date()
                child.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                child.age = 0
    
    def _compute_age_group(self):
        """Compute age group from age"""
        for child in self:
            age = child.age
            if age < 0.25:  # 0-3 months
                child.age_group = 'newborn'
            elif age < 1:  # 3-12 months
                child.age_group = 'infant'
            elif age < 3:  # 1-3 years
                child.age_group = 'toddler'
            elif age < 5:  # 3-5 years
                child.age_group = 'preschool'
            elif age < 13:  # 6-12 years
                child.age_group = 'school_age'
            else:  # 13+ years
                child.age_group = 'teen'
    
    def get_child_analytics(self):
        """Get child analytics"""
        return {
            'age': self.age,
            'age_group': self.age_group,
            'total_purchases': self.total_purchases,
            'total_spent': self.total_spent,
            'last_purchase_date': self.last_purchase_date,
            'favorite_colors': self.favorite_colors,
            'preferred_styles': self.preferred_styles,
            'status': self.status,
        }
    
    @classmethod
    def get_children_by_age_group(cls, age_group: str):
        """Get children by age group"""
        return cls.search([
            ('age_group', '=', age_group),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_children_by_gender(cls, gender: str):
        """Get children by gender"""
        return cls.search([
            ('gender', '=', gender),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_children_by_parent(cls, parent_id: int):
        """Get children by parent"""
        return cls.search([
            ('parent_id', '=', parent_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_children_by_company(cls, company_id: int):
        """Get children by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_child_analytics_summary(cls):
        """Get child analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_children': 0,
            'active_children': 0,
            'newborn_children': 0,
            'infant_children': 0,
            'toddler_children': 0,
            'preschool_children': 0,
            'school_age_children': 0,
            'teen_children': 0,
            'inactive_children': 0,
            'active_percentage': 0,
        }
    
    def action_activate(self):
        """Activate child profile"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate child profile"""
        self.status = 'inactive'
        return True
    
    def get_size_recommendations(self):
        """Get size recommendations based on age and measurements"""
        recommendations = []
        
        if self.age_group == 'newborn':
            recommendations = ['0-3M', '3M']
        elif self.age_group == 'infant':
            recommendations = ['3M', '6M', '9M', '12M']
        elif self.age_group == 'toddler':
            recommendations = ['12M', '18M', '2T', '3T']
        elif self.age_group == 'preschool':
            recommendations = ['3T', '4T', '5T']
        elif self.age_group == 'school_age':
            recommendations = ['XS', 'S', 'M', 'L']
        elif self.age_group == 'teen':
            recommendations = ['S', 'M', 'L', 'XL']
        
        return recommendations
    
    def get_style_recommendations(self):
        """Get style recommendations based on age and gender"""
        recommendations = []
        
        if self.gender == 'boy':
            if self.age_group in ['toddler', 'preschool']:
                recommendations = ['Casual', 'Play', 'Formal']
            elif self.age_group in ['school_age', 'teen']:
                recommendations = ['Casual', 'Sports', 'Formal', 'Trendy']
        elif self.gender == 'girl':
            if self.age_group in ['toddler', 'preschool']:
                recommendations = ['Casual', 'Play', 'Party', 'Formal']
            elif self.age_group in ['school_age', 'teen']:
                recommendations = ['Casual', 'Party', 'Formal', 'Trendy', 'Ethnic']
        else:
            recommendations = ['Casual', 'Unisex']
        
        return recommendations
    
    def action_duplicate(self):
        """Duplicate child profile"""
        self.ensure_one()
        
        new_child = self.copy({
            'name': f'{self.name} (Copy)',
        })
        
        return new_child
    
    def action_export_child(self):
        """Export child profile data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'age': self.age,
            'gender': self.gender,
            'age_group': self.age_group,
            'current_height': self.current_height,
            'current_weight': self.current_weight,
            'clothing_size': self.clothing_size,
            'shoe_size': self.shoe_size,
            'favorite_colors': self.favorite_colors,
            'preferred_styles': self.preferred_styles,
            'allergies': self.allergies,
            'special_notes': self.special_notes,
        }
    
    def action_import_child(self, child_data: Dict[str, Any]):
        """Import child profile data"""
        self.ensure_one()
        
        self.write(child_data)
        return True