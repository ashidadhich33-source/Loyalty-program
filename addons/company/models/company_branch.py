# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class CompanyBranch(models.Model):
    """Company branch model for Kids Clothing ERP"""
    
    _name = 'company.branch'
    _description = 'Company Branch'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Branch Name',
        required=True,
        help='Name of the branch'
    )
    
    code = fields.Char(
        string='Branch Code',
        required=True,
        help='Unique code for the branch'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the branch'
    )
    
    # Company relationship
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='Company this branch belongs to'
    )
    
    # Branch hierarchy
    parent_branch_id = fields.Many2one(
        'company.branch',
        string='Parent Branch',
        help='Parent branch in hierarchy'
    )
    
    child_branch_ids = fields.One2many(
        'company.branch',
        'parent_branch_id',
        string='Child Branches',
        help='Child branches in hierarchy'
    )
    
    branch_level = fields.Integer(
        string='Branch Level',
        default=1,
        help='Level in branch hierarchy'
    )
    
    # Branch information
    branch_type = fields.Selection([
        ('head_office', 'Head Office'),
        ('regional_office', 'Regional Office'),
        ('branch_office', 'Branch Office'),
        ('warehouse', 'Warehouse'),
        ('showroom', 'Showroom'),
        ('franchise', 'Franchise'),
        ('distributor', 'Distributor'),
    ], string='Branch Type', default='branch_office', help='Type of branch')
    
    # Branch address
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
        help='Branch phone number'
    )
    
    mobile = fields.Char(
        string='Mobile',
        help='Branch mobile number'
    )
    
    email = fields.Char(
        string='Email',
        help='Branch email address'
    )
    
    website = fields.Char(
        string='Website',
        help='Branch website'
    )
    
    # Branch manager
    manager_id = fields.Many2one(
        'res.users',
        string='Branch Manager',
        help='Branch manager'
    )
    
    # Branch settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the branch is active'
    )
    
    is_default = fields.Boolean(
        string='Default Branch',
        default=False,
        help='Whether this is the default branch'
    )
    
    # Branch capacity
    max_users = fields.Integer(
        string='Max Users',
        default=50,
        help='Maximum number of users for this branch'
    )
    
    current_users = fields.Integer(
        string='Current Users',
        compute='_compute_current_users',
        store=True,
        help='Current number of users in this branch'
    )
    
    # Branch features
    enable_pos = fields.Boolean(
        string='Enable POS',
        default=True,
        help='Enable POS for this branch'
    )
    
    enable_inventory = fields.Boolean(
        string='Enable Inventory',
        default=True,
        help='Enable inventory for this branch'
    )
    
    enable_sales = fields.Boolean(
        string='Enable Sales',
        default=True,
        help='Enable sales for this branch'
    )
    
    enable_purchase = fields.Boolean(
        string='Enable Purchase',
        default=True,
        help='Enable purchase for this branch'
    )
    
    # Branch analytics
    total_sales = fields.Float(
        string='Total Sales',
        compute='_compute_total_sales',
        store=True,
        help='Total sales for this branch'
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        compute='_compute_total_orders',
        store=True,
        help='Total orders for this branch'
    )
    
    # Branch users
    user_ids = fields.Many2many(
        'res.users',
        'branch_user_rel',
        'branch_id',
        'user_id',
        string='Users',
        help='Users assigned to this branch'
    )
    
    # Branch locations
    location_ids = fields.One2many(
        'company.location',
        'branch_id',
        string='Locations',
        help='Locations in this branch'
    )
    
    @api.depends('user_ids')
    def _compute_current_users(self):
        """Compute current users for this branch"""
        for branch in self:
            branch.current_users = len(branch.user_ids)
    
    @api.depends('user_ids')
    def _compute_total_sales(self):
        """Compute total sales for this branch"""
        for branch in self:
            # This would need actual implementation based on sales data
            branch.total_sales = 0.0
    
    @api.depends('user_ids')
    def _compute_total_orders(self):
        """Compute total orders for this branch"""
        for branch in self:
            # This would need actual implementation based on order data
            branch.total_orders = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set branch level
        if 'parent_branch_id' in vals and vals['parent_branch_id']:
            parent = self.browse(vals['parent_branch_id'])
            vals['branch_level'] = parent.branch_level + 1
        else:
            vals['branch_level'] = 1
        
        return super(CompanyBranch, self).create(vals)
    
    def write(self, vals):
        """Override write to handle branch updates"""
        result = super(CompanyBranch, self).write(vals)
        
        # Update child branch levels if parent changed
        if 'parent_branch_id' in vals:
            for branch in self:
                branch._update_child_levels()
        
        return result
    
    def _update_child_levels(self):
        """Update child branch levels"""
        for child in self.child_branch_ids:
            child.branch_level = self.branch_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of branches with data"""
        for branch in self:
            if branch.user_ids:
                raise ValidationError(_('Cannot delete branch with users. Please reassign users first.'))
            
            if branch.location_ids:
                raise ValidationError(_('Cannot delete branch with locations. Please delete locations first.'))
        
        return super(CompanyBranch, self).unlink()
    
    def action_activate(self):
        """Activate branch"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate branch"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default branch"""
        # Remove default from other branches in same company
        self.search([
            ('company_id', '=', self.company_id.id),
            ('is_default', '=', True),
        ]).write({'is_default': False})
        
        # Set this branch as default
        self.is_default = True
        return True
    
    def get_branch_hierarchy(self):
        """Get branch hierarchy"""
        hierarchy = []
        current_branch = self
        
        while current_branch:
            hierarchy.insert(0, current_branch)
            current_branch = current_branch.parent_branch_id
        
        return hierarchy
    
    def get_child_branches(self):
        """Get all child branches"""
        child_branches = []
        
        for child in self.child_branch_ids:
            child_branches.append(child)
            child_branches.extend(child.get_child_branches())
        
        return child_branches
    
    def get_branch_users(self):
        """Get all users in this branch"""
        return self.user_ids
    
    def get_branch_locations(self):
        """Get all locations in this branch"""
        return self.location_ids
    
    def get_branch_analytics(self):
        """Get branch analytics"""
        return {
            'total_users': self.current_users,
            'max_users': self.max_users,
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'branch_type': self.branch_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'enable_pos': self.enable_pos,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
        }
    
    @api.model
    def get_branches_by_company(self, company_id):
        """Get branches by company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_branches_by_type(self, branch_type):
        """Get branches by type"""
        return self.search([
            ('branch_type', '=', branch_type),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_default_branch(self, company_id):
        """Get default branch for company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @api.model
    def get_branch_analytics_summary(self):
        """Get branch analytics summary"""
        total_branches = self.search_count([])
        active_branches = self.search_count([('is_active', '=', True)])
        default_branches = self.search_count([('is_default', '=', True)])
        
        return {
            'total_branches': total_branches,
            'active_branches': active_branches,
            'default_branches': default_branches,
            'inactive_branches': total_branches - active_branches,
            'active_percentage': (active_branches / total_branches * 100) if total_branches > 0 else 0,
        }
    
    @api.constrains('code')
    def _check_code(self):
        """Validate branch code"""
        for branch in self:
            if branch.code:
                # Check for duplicate codes in same company
                existing = self.search([
                    ('code', '=', branch.code),
                    ('company_id', '=', branch.company_id.id),
                    ('id', '!=', branch.id),
                ])
                if existing:
                    raise ValidationError(_('Branch code must be unique within company'))
    
    @api.constrains('parent_branch_id')
    def _check_parent_branch(self):
        """Validate parent branch"""
        for branch in self:
            if branch.parent_branch_id and branch.parent_branch_id == branch:
                raise ValidationError(_('Branch cannot be its own parent'))
            
            if branch.parent_branch_id:
                # Check for circular reference
                current = branch.parent_branch_id
                while current:
                    if current == branch:
                        raise ValidationError(_('Circular reference in branch hierarchy'))
                    current = current.parent_branch_id
                
                # Check if parent branch belongs to same company
                if branch.parent_branch_id.company_id != branch.company_id:
                    raise ValidationError(_('Parent branch must belong to same company'))
    
    @api.constrains('is_default')
    def _check_default_branch(self):
        """Validate default branch"""
        for branch in self:
            if branch.is_default:
                # Check if there's already a default branch in same company
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('company_id', '=', branch.company_id.id),
                    ('id', '!=', branch.id),
                ])
                if existing_default:
                    raise ValidationError(_('Only one branch can be set as default per company'))
    
    @api.constrains('max_users', 'current_users')
    def _check_user_capacity(self):
        """Validate user capacity"""
        for branch in self:
            if branch.current_users > branch.max_users:
                raise ValidationError(_('Current users exceed maximum capacity'))
    
    def action_duplicate(self):
        """Duplicate branch"""
        self.ensure_one()
        
        new_branch = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Branch',
            'res_model': 'company.branch',
            'res_id': new_branch.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_branch(self):
        """Export branch data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'branch_type': self.branch_type,
            'company_id': self.company_id.id,
            'parent_branch_id': self.parent_branch_id.id if self.parent_branch_id else None,
            'street': self.street,
            'city': self.city,
            'state_id': self.state_id.id if self.state_id else None,
            'zip': self.zip,
            'country_id': self.country_id.id if self.country_id else None,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'website': self.website,
            'manager_id': self.manager_id.id if self.manager_id else None,
            'max_users': self.max_users,
            'enable_pos': self.enable_pos,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
        }
    
    def action_import_branch(self, branch_data):
        """Import branch data"""
        self.ensure_one()
        
        self.write(branch_data)
        return True