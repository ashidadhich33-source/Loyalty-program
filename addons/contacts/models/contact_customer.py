# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Customer Management
===============================================

Standalone version of the customer management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactCustomer(BaseModel):
    """Customer contact model for Kids Clothing ERP"""
    
    _name = 'contact.customer'
    _description = 'Customer Contact'
    _table = 'contact_customer'
    
    # Basic customer information
    name = CharField(
        string='Name',
        size=255,
        required=True,
        help='Name of the customer'
    )
    
    partner_id = IntegerField(
        string='Partner ID',
        required=True,
        help='Related partner'
    )
    
    customer_code = CharField(
        string='Customer Code',
        size=50,
        help='Unique customer code'
    )
    
    customer_type = SelectionField(
        string='Customer Type',
        selection=[
            ('individual', 'Individual'),
            ('corporate', 'Corporate'),
            ('wholesale', 'Wholesale'),
            ('retail', 'Retail'),
        ],
        default='individual',
        help='Type of customer'
    )
    
    # Loyalty program
    loyalty_points = IntegerField(
        string='Loyalty Points',
        default=0,
        help='Loyalty points earned'
    )
    
    loyalty_level = SelectionField(
        string='Loyalty Level',
        selection=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        default='bronze',
        help='Loyalty level based on points'
    )
    
    # Credit management
    credit_limit = FloatField(
        string='Credit Limit',
        default=0.0,
        help='Credit limit for this customer'
    )
    
    credit_balance = FloatField(
        string='Credit Balance',
        default=0.0,
        help='Current credit balance'
    )
    
    payment_terms = IntegerField(
        string='Payment Terms ID',
        help='Payment terms for this customer'
    )
    
    # Company and status
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this customer belongs to'
    )
    
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('blacklisted', 'Blacklisted'),
        ],
        default='active',
        help='Customer status'
    )
    
    # Customer preferences
    preferred_payment_method = SelectionField(
        string='Preferred Payment Method',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('upi', 'UPI'),
            ('net_banking', 'Net Banking'),
            ('cheque', 'Cheque'),
            ('credit', 'Credit'),
        ],
        help='Preferred payment method'
    )
    
    preferred_delivery_method = SelectionField(
        string='Preferred Delivery Method',
        selection=[
            ('home_delivery', 'Home Delivery'),
            ('pickup', 'Store Pickup'),
            ('express', 'Express Delivery'),
        ],
        help='Preferred delivery method'
    )
    
    # Customer analytics
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total number of orders'
    )
    
    total_spent = FloatField(
        string='Total Spent',
        default=0.0,
        help='Total amount spent'
    )
    
    last_order_date = DateTimeField(
        string='Last Order Date',
        help='Date of last order'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    # Customer notes
    notes = TextField(
        string='Notes',
        help='Additional notes about the customer'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Generate customer code if not provided
        if not vals.get('customer_code'):
            vals['customer_code'] = f"CUST{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle customer updates"""
        result = super().write(vals)
        
        # Update loyalty level based on points
        if 'loyalty_points' in vals:
            self._compute_loyalty_level()
        
        # Log customer updates
        for customer in self:
            if vals:
                logger.info(f"Customer {customer.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def _compute_loyalty_level(self):
        """Compute loyalty level based on points"""
        for customer in self:
            if customer.loyalty_points >= 10000:
                customer.loyalty_level = 'platinum'
            elif customer.loyalty_points >= 5000:
                customer.loyalty_level = 'gold'
            elif customer.loyalty_points >= 2000:
                customer.loyalty_level = 'silver'
            else:
                customer.loyalty_level = 'bronze'
    
    def get_customer_analytics(self):
        """Get customer analytics"""
        return {
            'total_orders': self.total_orders,
            'total_spent': self.total_spent,
            'last_order_date': self.last_order_date,
            'average_order_value': self.average_order_value,
            'loyalty_points': self.loyalty_points,
            'loyalty_level': self.loyalty_level,
            'credit_limit': self.credit_limit,
            'credit_balance': self.credit_balance,
            'status': self.status,
        }
    
    @classmethod
    def get_customers_by_type(cls, customer_type: str):
        """Get customers by type"""
        return cls.search([
            ('customer_type', '=', customer_type),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_customers_by_loyalty_level(cls, loyalty_level: str):
        """Get customers by loyalty level"""
        return cls.search([
            ('loyalty_level', '=', loyalty_level),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_customers_by_company(cls, company_id: int):
        """Get customers by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_customer_analytics_summary(cls):
        """Get customer analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_customers': 0,
            'active_customers': 0,
            'bronze_customers': 0,
            'silver_customers': 0,
            'gold_customers': 0,
            'platinum_customers': 0,
            'inactive_customers': 0,
            'active_percentage': 0,
        }
    
    def action_activate(self):
        """Activate customer"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate customer"""
        self.status = 'inactive'
        return True
    
    def action_blacklist(self):
        """Blacklist customer"""
        self.status = 'blacklisted'
        return True
    
    def action_unblacklist(self):
        """Remove from blacklist"""
        self.status = 'active'
        return True
    
    def add_loyalty_points(self, points: int):
        """Add loyalty points"""
        self.loyalty_points += points
        self._compute_loyalty_level()
        return True
    
    def redeem_loyalty_points(self, points: int):
        """Redeem loyalty points"""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            self._compute_loyalty_level()
            return True
        else:
            raise ValueError('Insufficient loyalty points')
    
    def get_available_credit(self):
        """Get available credit"""
        return self.credit_limit - self.credit_balance
    
    def action_duplicate(self):
        """Duplicate customer"""
        self.ensure_one()
        
        new_customer = self.copy({
            'name': f'{self.name} (Copy)',
            'customer_code': f"CUST{datetime.now().strftime('%Y%m%d%H%M%S')}",
        })
        
        return new_customer
    
    def action_export_customer(self):
        """Export customer data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'customer_code': self.customer_code,
            'customer_type': self.customer_type,
            'loyalty_points': self.loyalty_points,
            'loyalty_level': self.loyalty_level,
            'credit_limit': self.credit_limit,
            'credit_balance': self.credit_balance,
            'status': self.status,
            'preferred_payment_method': self.preferred_payment_method,
            'preferred_delivery_method': self.preferred_delivery_method,
        }
    
    def action_import_customer(self, customer_data: Dict[str, Any]):
        """Import customer data"""
        self.ensure_one()
        
        self.write(customer_data)
        return True