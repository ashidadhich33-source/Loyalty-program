# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CompanyLocation(models.Model):
    """Company location model for Kids Clothing ERP"""
    
    _name = 'company.location'
    _description = 'Company Location'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Location Name',
        required=True,
        help='Name of the location'
    )
    
    code = fields.Char(
        string='Location Code',
        required=True,
        help='Unique code for the location'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the location'
    )
    
    # Company and branch relationship
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='Company this location belongs to'
    )
    
    branch_id = fields.Many2one(
        'company.branch',
        string='Branch',
        help='Branch this location belongs to'
    )
    
    # Location hierarchy
    parent_location_id = fields.Many2one(
        'company.location',
        string='Parent Location',
        help='Parent location in hierarchy'
    )
    
    child_location_ids = fields.One2many(
        'company.location',
        'parent_location_id',
        string='Child Locations',
        help='Child locations in hierarchy'
    )
    
    location_level = fields.Integer(
        string='Location Level',
        default=1,
        help='Level in location hierarchy'
    )
    
    # Location information
    location_type = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('showroom', 'Showroom'),
        ('office', 'Office'),
        ('storage', 'Storage'),
        ('retail', 'Retail Store'),
        ('wholesale', 'Wholesale Store'),
        ('franchise', 'Franchise Store'),
        ('distribution', 'Distribution Center'),
        ('manufacturing', 'Manufacturing Unit'),
        ('other', 'Other'),
    ], string='Location Type', default='warehouse', help='Type of location')
    
    # Location address
    street = fields.Char(
        string='Street',
        help='Street address'
    )
    
    street2 = fields.Char(
        string='Street2',
        help='Street address line 2'
    )
    
    city = fields.Char(
        string='City',
        help='City'
    )
    
    state_id = fields.Many2one(
        'res.country.state',
        string='State',
        help='State'
    )
    
    zip = fields.Char(
        string='ZIP',
        help='ZIP code'
    )
    
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        help='Country'
    )
    
    # Contact information
    phone = fields.Char(
        string='Phone',
        help='Location phone number'
    )
    
    mobile = fields.Char(
        string='Mobile',
        help='Location mobile number'
    )
    
    email = fields.Char(
        string='Email',
        help='Location email address'
    )
    
    # Location manager
    manager_id = fields.Many2one(
        'res.users',
        string='Location Manager',
        help='Location manager'
    )
    
    # Location settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the location is active'
    )
    
    is_default = fields.Boolean(
        string='Default Location',
        default=False,
        help='Whether this is the default location'
    )
    
    # Location capacity
    max_capacity = fields.Float(
        string='Max Capacity',
        help='Maximum capacity of the location'
    )
    
    current_capacity = fields.Float(
        string='Current Capacity',
        compute='_compute_current_capacity',
        store=True,
        help='Current capacity usage'
    )
    
    capacity_unit = fields.Selection([
        ('sqft', 'Square Feet'),
        ('sqm', 'Square Meters'),
        ('units', 'Units'),
        ('kg', 'Kilograms'),
        ('tons', 'Tons'),
    ], string='Capacity Unit', default='sqft', help='Unit of capacity measurement')
    
    # Location features
    enable_inventory = fields.Boolean(
        string='Enable Inventory',
        default=True,
        help='Enable inventory for this location'
    )
    
    enable_sales = fields.Boolean(
        string='Enable Sales',
        default=True,
        help='Enable sales for this location'
    )
    
    enable_purchase = fields.Boolean(
        string='Enable Purchase',
        default=True,
        help='Enable purchase for this location'
    )
    
    enable_manufacturing = fields.Boolean(
        string='Enable Manufacturing',
        default=False,
        help='Enable manufacturing for this location'
    )
    
    # Location analytics
    total_products = fields.Integer(
        string='Total Products',
        compute='_compute_total_products',
        store=True,
        help='Total products in this location'
    )
    
    total_value = fields.Float(
        string='Total Value',
        compute='_compute_total_value',
        store=True,
        help='Total value of products in this location'
    )
    
    # Location users
    user_ids = fields.Many2many(
        'res.users',
        'location_user_rel',
        'location_id',
        'user_id',
        string='Users',
        help='Users assigned to this location'
    )
    
    # Location coordinates
    latitude = fields.Float(
        string='Latitude',
        help='Latitude coordinate'
    )
    
    longitude = fields.Float(
        string='Longitude',
        help='Longitude coordinate'
    )
    
    # Location operating hours
    operating_hours = fields.Text(
        string='Operating Hours',
        help='Operating hours of the location'
    )
    
    # Location services
    services_ids = fields.Many2many(
        'location.service',
        'location_service_rel',
        'location_id',
        'service_id',
        string='Services',
        help='Services provided at this location'
    )
    
    @api.depends('user_ids')
    def _compute_current_capacity(self):
        """Compute current capacity usage"""
        for location in self:
            # This would need actual implementation based on inventory data
            location.current_capacity = 0.0
    
    @api.depends('user_ids')
    def _compute_total_products(self):
        """Compute total products in this location"""
        for location in self:
            # This would need actual implementation based on product data
            location.total_products = 0
    
    @api.depends('user_ids')
    def _compute_total_value(self):
        """Compute total value of products in this location"""
        for location in self:
            # This would need actual implementation based on product data
            location.total_value = 0.0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set location level
        if 'parent_location_id' in vals and vals['parent_location_id']:
            parent = self.browse(vals['parent_location_id'])
            vals['location_level'] = parent.location_level + 1
        else:
            vals['location_level'] = 1
        
        return super(CompanyLocation, self).create(vals)
    
    def write(self, vals):
        """Override write to handle location updates"""
        result = super(CompanyLocation, self).write(vals)
        
        # Update child location levels if parent changed
        if 'parent_location_id' in vals:
            for location in self:
                location._update_child_levels()
        
        return result
    
    def _update_child_levels(self):
        """Update child location levels"""
        for child in self.child_location_ids:
            child.location_level = self.location_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of locations with data"""
        for location in self:
            if location.user_ids:
                raise ValidationError(_('Cannot delete location with users. Please reassign users first.'))
            
            if location.child_location_ids:
                raise ValidationError(_('Cannot delete location with child locations. Please delete child locations first.'))
        
        return super(CompanyLocation, self).unlink()
    
    def action_activate(self):
        """Activate location"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate location"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default location"""
        # Remove default from other locations in same company
        self.search([
            ('company_id', '=', self.company_id.id),
            ('is_default', '=', True),
        ]).write({'is_default': False})
        
        # Set this location as default
        self.is_default = True
        return True
    
    def get_location_hierarchy(self):
        """Get location hierarchy"""
        hierarchy = []
        current_location = self
        
        while current_location:
            hierarchy.insert(0, current_location)
            current_location = current_location.parent_location_id
        
        return hierarchy
    
    def get_child_locations(self):
        """Get all child locations"""
        child_locations = []
        
        for child in self.child_location_ids:
            child_locations.append(child)
            child_locations.extend(child.get_child_locations())
        
        return child_locations
    
    def get_location_users(self):
        """Get all users in this location"""
        return self.user_ids
    
    def get_location_analytics(self):
        """Get location analytics"""
        return {
            'total_products': self.total_products,
            'total_value': self.total_value,
            'current_capacity': self.current_capacity,
            'max_capacity': self.max_capacity,
            'location_type': self.location_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
            'enable_manufacturing': self.enable_manufacturing,
        }
    
    @api.model
    def get_locations_by_company(self, company_id):
        """Get locations by company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_locations_by_branch(self, branch_id):
        """Get locations by branch"""
        return self.search([
            ('branch_id', '=', branch_id),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_locations_by_type(self, location_type):
        """Get locations by type"""
        return self.search([
            ('location_type', '=', location_type),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_default_location(self, company_id):
        """Get default location for company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @api.model
    def get_location_analytics_summary(self):
        """Get location analytics summary"""
        total_locations = self.search_count([])
        active_locations = self.search_count([('is_active', '=', True)])
        default_locations = self.search_count([('is_default', '=', True)])
        
        return {
            'total_locations': total_locations,
            'active_locations': active_locations,
            'default_locations': default_locations,
            'inactive_locations': total_locations - active_locations,
            'active_percentage': (active_locations / total_locations * 100) if total_locations > 0 else 0,
        }
    
    @api.constrains('code')
    def _check_code(self):
        """Validate location code"""
        for location in self:
            if location.code:
                # Check for duplicate codes in same company
                existing = self.search([
                    ('code', '=', location.code),
                    ('company_id', '=', location.company_id.id),
                    ('id', '!=', location.id),
                ])
                if existing:
                    raise ValidationError(_('Location code must be unique within company'))
    
    @api.constrains('parent_location_id')
    def _check_parent_location(self):
        """Validate parent location"""
        for location in self:
            if location.parent_location_id and location.parent_location_id == location:
                raise ValidationError(_('Location cannot be its own parent'))
            
            if location.parent_location_id:
                # Check for circular reference
                current = location.parent_location_id
                while current:
                    if current == location:
                        raise ValidationError(_('Circular reference in location hierarchy'))
                    current = current.parent_location_id
                
                # Check if parent location belongs to same company
                if location.parent_location_id.company_id != location.company_id:
                    raise ValidationError(_('Parent location must belong to same company'))
    
    @api.constrains('branch_id')
    def _check_branch(self):
        """Validate branch"""
        for location in self:
            if location.branch_id and location.branch_id.company_id != location.company_id:
                raise ValidationError(_('Branch must belong to same company'))
    
    @api.constrains('is_default')
    def _check_default_location(self):
        """Validate default location"""
        for location in self:
            if location.is_default:
                # Check if there's already a default location in same company
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('company_id', '=', location.company_id.id),
                    ('id', '!=', location.id),
                ])
                if existing_default:
                    raise ValidationError(_('Only one location can be set as default per company'))
    
    @api.constrains('max_capacity', 'current_capacity')
    def _check_capacity(self):
        """Validate capacity"""
        for location in self:
            if location.max_capacity and location.current_capacity > location.max_capacity:
                raise ValidationError(_('Current capacity exceeds maximum capacity'))
    
    def action_duplicate(self):
        """Duplicate location"""
        self.ensure_one()
        
        new_location = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Location',
            'res_model': 'company.location',
            'res_id': new_location.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_location(self):
        """Export location data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'location_type': self.location_type,
            'company_id': self.company_id.id,
            'branch_id': self.branch_id.id if self.branch_id else None,
            'parent_location_id': self.parent_location_id.id if self.parent_location_id else None,
            'street': self.street,
            'city': self.city,
            'state_id': self.state_id.id if self.state_id else None,
            'zip': self.zip,
            'country_id': self.country_id.id if self.country_id else None,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'manager_id': self.manager_id.id if self.manager_id else None,
            'max_capacity': self.max_capacity,
            'capacity_unit': self.capacity_unit,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
            'enable_manufacturing': self.enable_manufacturing,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'operating_hours': self.operating_hours,
        }
    
    def action_import_location(self, location_data):
        """Import location data"""
        self.ensure_one()
        
        self.write(location_data)
        return True