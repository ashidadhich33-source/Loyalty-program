# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Customer Creation Wizard
===============================================

Customer creation wizard for POS transactions.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PosCustomerWizard(models.TransientModel):
    """POS Customer Creation Wizard"""
    
    _name = 'pos.customer.wizard'
    _description = 'POS Customer Creation Wizard'
    
    # Basic Information
    name = fields.Char(
        string='Customer Name',
        required=True,
        help='Name of the customer'
    )
    
    # Contact Information
    email = fields.Char(
        string='Email',
        help='Email address of the customer'
    )
    
    phone = fields.Char(
        string='Phone',
        help='Phone number of the customer'
    )
    
    mobile = fields.Char(
        string='Mobile',
        help='Mobile number of the customer'
    )
    
    # Address Information
    street = fields.Char(
        string='Street',
        help='Street address'
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
        string='ZIP Code',
        help='ZIP code'
    )
    
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        help='Country'
    )
    
    # Kids Clothing Specific Fields
    child_count = fields.Integer(
        string='Number of Children',
        default=0,
        help='Number of children in the family'
    )
    
    child_ages = fields.Text(
        string='Child Ages',
        help='Ages of the children (comma separated)'
    )
    
    age_group_interest = fields.Selection([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-12 months)'),
        ('toddler', 'Toddler (1-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Ages')
    ], string='Age Group Interest', help='Primary age group interest')
    
    gender_preference = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders')
    ], string='Gender Preference', help='Gender preference for clothing')
    
    seasonal_interest = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
        ('festive', 'Festive'),
        ('party', 'Party Wear')
    ], string='Seasonal Interest', help='Seasonal preference for clothing')
    
    # Customer Type
    customer_type = fields.Selection([
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
    ], string='Customer Type', default='individual', required=True)
    
    # Loyalty Program
    loyalty_program_id = fields.Many2one(
        'loyalty.program',
        string='Loyalty Program',
        help='Loyalty program for this customer'
    )
    
    # Additional Information
    notes = fields.Text(
        string='Notes',
        help='Additional notes about the customer'
    )
    
    # Return Information
    created_customer_id = fields.Many2one(
        'contact.customer',
        string='Created Customer',
        readonly=True
    )
    
    @api.model
    def default_get(self, fields_list):
        """Set default values"""
        defaults = super().default_get(fields_list)
        
        # Set default country to India
        india = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        if india:
            defaults['country_id'] = india.id
        
        # Set default loyalty program
        default_program = self.env['loyalty.program'].search([
            ('is_active', '=', True)
        ], limit=1)
        if default_program:
            defaults['loyalty_program_id'] = default_program.id
        
        return defaults
    
    def action_create_customer(self):
        """Create customer from wizard"""
        self.ensure_one()
        
        # Validate required fields
        if not self.name:
            raise ValidationError(_('Customer name is required.'))
        
        # Check for duplicate email
        if self.email:
            existing_customer = self.env['contact.customer'].search([
                ('email', '=', self.email)
            ])
            if existing_customer:
                raise ValidationError(_('Customer with this email already exists.'))
        
        # Create customer
        customer_vals = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'street': self.street,
            'city': self.city,
            'state_id': self.state_id.id if self.state_id else False,
            'zip': self.zip,
            'country_id': self.country_id.id if self.country_id else False,
            'customer_type': self.customer_type,
            'child_count': self.child_count,
            'child_ages': self.child_ages,
            'age_group_interest': self.age_group_interest,
            'gender_preference': self.gender_preference,
            'seasonal_interest': self.seasonal_interest,
            'notes': self.notes,
        }
        
        customer = self.env['contact.customer'].create(customer_vals)
        
        # Assign to loyalty program if selected
        if self.loyalty_program_id:
            customer.write({'loyalty_program_id': self.loyalty_program_id.id})
        
        # Store created customer
        self.created_customer_id = customer.id
        
        # Return action to show created customer
        return {
            'type': 'ir.actions.act_window',
            'name': _('Customer Created'),
            'res_model': 'contact.customer',
            'res_id': customer.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {'from_pos': True}
        }
    
    def action_create_and_continue(self):
        """Create customer and return to POS"""
        self.ensure_one()
        
        # Create customer
        self.action_create_customer()
        
        # Return to POS with customer selected
        return {
            'type': 'ir.actions.act_window_close',
            'context': {
                'pos_customer_created': True,
                'pos_customer_id': self.created_customer_id.id,
                'pos_customer_name': self.created_customer_id.name
            }
        }