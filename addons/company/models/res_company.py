# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    """Extended company model for Kids Clothing ERP"""
    
    _inherit = 'res.company'
    
    # Company Information
    company_type = fields.Selection([
        ('retail', 'Retail Store'),
        ('wholesale', 'Wholesale'),
        ('franchise', 'Franchise'),
        ('corporate', 'Corporate'),
        ('distributor', 'Distributor'),
        ('manufacturer', 'Manufacturer'),
    ], string='Company Type', default='retail', help='Type of company')
    
    business_nature = fields.Selection([
        ('kids_clothing', 'Kids Clothing'),
        ('fashion_retail', 'Fashion Retail'),
        ('general_retail', 'General Retail'),
        ('ecommerce', 'E-commerce'),
        ('wholesale_trade', 'Wholesale Trade'),
        ('manufacturing', 'Manufacturing'),
    ], string='Business Nature', default='kids_clothing', help='Nature of business')
    
    # Company Hierarchy
    parent_company_id = fields.Many2one(
        'res.company',
        string='Parent Company',
        help='Parent company in hierarchy'
    )
    
    child_company_ids = fields.One2many(
        'res.company',
        'parent_company_id',
        string='Child Companies',
        help='Child companies in hierarchy'
    )
    
    company_level = fields.Integer(
        string='Company Level',
        default=1,
        help='Level in company hierarchy'
    )
    
    # GST Information
    gstin = fields.Char(
        string='GSTIN',
        help='GST Identification Number'
    )
    
    gst_registration_date = fields.Date(
        string='GST Registration Date',
        help='Date of GST registration'
    )
    
    gst_status = fields.Selection([
        ('registered', 'Registered'),
        ('unregistered', 'Unregistered'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ], string='GST Status', default='registered', help='GST registration status')
    
    # Company Address
    registered_address = fields.Text(
        string='Registered Address',
        help='Registered office address'
    )
    
    business_address = fields.Text(
        string='Business Address',
        help='Business office address'
    )
    
    warehouse_address = fields.Text(
        string='Warehouse Address',
        help='Warehouse address'
    )
    
    # Contact Information
    contact_person = fields.Char(
        string='Contact Person',
        help='Primary contact person'
    )
    
    contact_phone = fields.Char(
        string='Contact Phone',
        help='Primary contact phone'
    )
    
    contact_email = fields.Char(
        string='Contact Email',
        help='Primary contact email'
    )
    
    # Financial Information
    financial_year_start = fields.Date(
        string='Financial Year Start',
        help='Start date of financial year'
    )
    
    financial_year_end = fields.Date(
        string='Financial Year End',
        help='End date of financial year'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.INR'),
        help='Company currency'
    )
    
    # Company Settings
    enable_multi_company = fields.Boolean(
        string='Enable Multi-Company',
        default=True,
        help='Enable multi-company operations'
    )
    
    enable_gst = fields.Boolean(
        string='Enable GST',
        default=True,
        help='Enable GST compliance'
    )
    
    enable_e_invoice = fields.Boolean(
        string='Enable E-invoice',
        default=True,
        help='Enable E-invoice generation'
    )
    
    enable_e_way_bill = fields.Boolean(
        string='Enable E-way Bill',
        default=True,
        help='Enable E-way bill generation'
    )
    
    # Company Branches
    branch_ids = fields.One2many(
        'company.branch',
        'company_id',
        string='Branches',
        help='Company branches'
    )
    
    # Company Locations
    location_ids = fields.One2many(
        'company.location',
        'company_id',
        string='Locations',
        help='Company locations'
    )
    
    # Company Users
    user_ids = fields.Many2many(
        'res.users',
        'company_user_rel',
        'company_id',
        'user_id',
        string='Users',
        help='Users assigned to this company'
    )
    
    # Company Analytics
    total_users = fields.Integer(
        string='Total Users',
        compute='_compute_total_users',
        store=True,
        help='Total number of users in this company'
    )
    
    active_users = fields.Integer(
        string='Active Users',
        compute='_compute_active_users',
        store=True,
        help='Number of active users in this company'
    )
    
    # Company Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the company is active'
    )
    
    is_default = fields.Boolean(
        string='Default Company',
        default=False,
        help='Whether this is the default company'
    )
    
    # Company Documents
    logo = fields.Binary(
        string='Company Logo',
        help='Company logo'
    )
    
    document_ids = fields.One2many(
        'company.document',
        'company_id',
        string='Documents',
        help='Company documents'
    )
    
    # Company Communication
    website = fields.Char(
        string='Website',
        help='Company website'
    )
    
    social_media_ids = fields.One2many(
        'company.social.media',
        'company_id',
        string='Social Media',
        help='Company social media accounts'
    )
    
    # Company Analytics
    analytics_ids = fields.One2many(
        'company.analytics',
        'company_id',
        string='Analytics',
        help='Company analytics data'
    )
    
    @api.depends('user_ids')
    def _compute_total_users(self):
        """Compute total users for this company"""
        for company in self:
            company.total_users = len(company.user_ids)
    
    @api.depends('user_ids', 'user_ids.active')
    def _compute_active_users(self):
        """Compute active users for this company"""
        for company in self:
            company.active_users = len(company.user_ids.filtered('active'))
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default financial year if not provided
        if 'financial_year_start' not in vals:
            current_year = datetime.now().year
            vals['financial_year_start'] = f'{current_year}-04-01'
            vals['financial_year_end'] = f'{current_year + 1}-03-31'
        
        # Set company level
        if 'parent_company_id' in vals and vals['parent_company_id']:
            parent = self.browse(vals['parent_company_id'])
            vals['company_level'] = parent.company_level + 1
        else:
            vals['company_level'] = 1
        
        return super(ResCompany, self).create(vals)
    
    def write(self, vals):
        """Override write to handle company updates"""
        result = super(ResCompany, self).write(vals)
        
        # Update child company levels if parent changed
        if 'parent_company_id' in vals:
            for company in self:
                company._update_child_levels()
        
        return result
    
    def _update_child_levels(self):
        """Update child company levels"""
        for child in self.child_company_ids:
            child.company_level = self.company_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of companies with data"""
        for company in self:
            if company.user_ids:
                raise UserError(_('Cannot delete company with users. Please reassign users first.'))
            
            if company.branch_ids:
                raise UserError(_('Cannot delete company with branches. Please delete branches first.'))
            
            if company.location_ids:
                raise UserError(_('Cannot delete company with locations. Please delete locations first.'))
        
        return super(ResCompany, self).unlink()
    
    def action_activate(self):
        """Activate company"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate company"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default company"""
        # Remove default from other companies
        self.search([('is_default', '=', True)]).write({'is_default': False})
        
        # Set this company as default
        self.is_default = True
        return True
    
    def action_validate_gstin(self):
        """Validate GSTIN"""
        self.ensure_one()
        
        if not self.gstin:
            raise ValidationError(_('GSTIN is required for validation'))
        
        # Use system utils to validate GSTIN
        if not self.env['system.utils'].validate_gst_number(self.gstin):
            raise ValidationError(_('Invalid GSTIN format'))
        
        return True
    
    def action_generate_gstin(self):
        """Generate GSTIN based on company details"""
        self.ensure_one()
        
        if not self.state_id:
            raise ValidationError(_('State is required to generate GSTIN'))
        
        if not self.partner_id:
            raise ValidationError(_('Partner is required to generate GSTIN'))
        
        # Generate GSTIN (this would need actual implementation)
        state_code = self.state_id.code
        pan_number = self.partner_id.vat or 'ABCDE1234F'
        entity_number = '1'
        z_character = 'Z'
        checksum = '1'
        
        gstin = state_code + pan_number + entity_number + z_character + checksum
        
        self.gstin = gstin
        return True
    
    def get_company_hierarchy(self):
        """Get company hierarchy"""
        hierarchy = []
        current_company = self
        
        while current_company:
            hierarchy.insert(0, current_company)
            current_company = current_company.parent_company_id
        
        return hierarchy
    
    def get_child_companies(self):
        """Get all child companies"""
        child_companies = []
        
        for child in self.child_company_ids:
            child_companies.append(child)
            child_companies.extend(child.get_child_companies())
        
        return child_companies
    
    def get_company_users(self):
        """Get all users in this company"""
        return self.user_ids
    
    def get_company_branches(self):
        """Get all branches in this company"""
        return self.branch_ids
    
    def get_company_locations(self):
        """Get all locations in this company"""
        return self.location_ids
    
    def get_company_analytics(self):
        """Get company analytics"""
        return {
            'total_users': self.total_users,
            'active_users': self.active_users,
            'total_branches': len(self.branch_ids),
            'total_locations': len(self.location_ids),
            'company_type': self.company_type,
            'business_nature': self.business_nature,
            'gst_status': self.gst_status,
            'is_active': self.is_active,
            'is_default': self.is_default,
        }
    
    @api.model
    def get_companies_by_type(self, company_type):
        """Get companies by type"""
        return self.search([
            ('company_type', '=', company_type),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_companies_by_business_nature(self, business_nature):
        """Get companies by business nature"""
        return self.search([
            ('business_nature', '=', business_nature),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_companies_with_gst(self):
        """Get companies with GST registration"""
        return self.search([
            ('gstin', '!=', False),
            ('gst_status', '=', 'registered'),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_default_company(self):
        """Get default company"""
        return self.search([('is_default', '=', True)], limit=1)
    
    @api.model
    def get_company_analytics_summary(self):
        """Get company analytics summary"""
        total_companies = self.search_count([])
        active_companies = self.search_count([('is_active', '=', True)])
        companies_with_gst = self.search_count([('gstin', '!=', False)])
        default_companies = self.search_count([('is_default', '=', True)])
        
        return {
            'total_companies': total_companies,
            'active_companies': active_companies,
            'companies_with_gst': companies_with_gst,
            'default_companies': default_companies,
            'inactive_companies': total_companies - active_companies,
            'active_percentage': (active_companies / total_companies * 100) if total_companies > 0 else 0,
        }
    
    @api.constrains('gstin')
    def _check_gstin(self):
        """Validate GSTIN format"""
        for company in self:
            if company.gstin and not self.env['system.utils'].validate_gst_number(company.gstin):
                raise ValidationError(_('Invalid GSTIN format'))
    
    @api.constrains('parent_company_id')
    def _check_parent_company(self):
        """Validate parent company"""
        for company in self:
            if company.parent_company_id and company.parent_company_id == company:
                raise ValidationError(_('Company cannot be its own parent'))
            
            if company.parent_company_id:
                # Check for circular reference
                current = company.parent_company_id
                while current:
                    if current == company:
                        raise ValidationError(_('Circular reference in company hierarchy'))
                    current = current.parent_company_id
    
    @api.constrains('financial_year_start', 'financial_year_end')
    def _check_financial_year(self):
        """Validate financial year"""
        for company in self:
            if company.financial_year_start and company.financial_year_end:
                if company.financial_year_start >= company.financial_year_end:
                    raise ValidationError(_('Financial year start must be before end date'))
                
                # Check if financial year is 12 months
                start_date = fields.Date.from_string(company.financial_year_start)
                end_date = fields.Date.from_string(company.financial_year_end)
                diff_days = (end_date - start_date).days
                
                if diff_days < 365 or diff_days > 366:
                    raise ValidationError(_('Financial year must be 12 months'))
    
    @api.constrains('is_default')
    def _check_default_company(self):
        """Validate default company"""
        for company in self:
            if company.is_default:
                # Check if there's already a default company
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('id', '!=', company.id),
                ])
                if existing_default:
                    raise ValidationError(_('Only one company can be set as default'))
    
    def action_duplicate(self):
        """Duplicate company"""
        self.ensure_one()
        
        new_company = self.copy({
            'name': f'{self.name} (Copy)',
            'is_default': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Company',
            'res_model': 'res.company',
            'res_id': new_company.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_company(self):
        """Export company data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'company_type': self.company_type,
            'business_nature': self.business_nature,
            'gstin': self.gstin,
            'gst_status': self.gst_status,
            'currency_id': self.currency_id.id,
            'financial_year_start': self.financial_year_start,
            'financial_year_end': self.financial_year_end,
            'enable_multi_company': self.enable_multi_company,
            'enable_gst': self.enable_gst,
            'enable_e_invoice': self.enable_e_invoice,
            'enable_e_way_bill': self.enable_e_way_bill,
        }
    
    def action_import_company(self, company_data):
        """Import company data"""
        self.ensure_one()
        
        self.write(company_data)
        return True