# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyPoints(BaseModel):
    """Loyalty Points Management"""
    
    _name = 'loyalty.points'
    _description = 'Loyalty Points'
    _order = 'date desc, id desc'
    
    name = CharField(string='Reference', required=True, size=64)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', required=True)
    
    # Points Details
    points = IntegerField(string='Points', required=True)
    points_type = SelectionField([
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
        ('expired', 'Expired'),
        ('adjusted', 'Adjusted'),
        ('bonus', 'Bonus'),
    ], string='Points Type', required=True, default='earned')
    
    # Transaction Details
    transaction_id = Many2oneField('sale.order', string='Sale Order')
    transaction_type = SelectionField([
        ('purchase', 'Purchase'),
        ('redemption', 'Redemption'),
        ('bonus', 'Bonus'),
        ('adjustment', 'Adjustment'),
        ('expiry', 'Expiry'),
        ('referral', 'Referral'),
        ('birthday', 'Birthday'),
    ], string='Transaction Type', required=True, default='purchase')
    
    # Expiry Management
    expiry_date = DateField(string='Expiry Date')
    is_expired = BooleanField(string='Expired', default=False)
    expiry_notification_sent = BooleanField(string='Expiry Notification Sent', default=False)
    
    # Kids Clothing Context
    age_group = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
    ], string='Age Group')
    
    gender = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender')
    
    season = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    ], string='Season')
    
    # Additional Information
    description = TextField(string='Description')
    note = TextField(string='Internal Note')
    
    # System Fields
    date = DateTimeField(string='Date', required=True, default=lambda self: self.env['datetime'].now())
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def create(self, vals):
        """Create loyalty points with validation"""
        if 'points' in vals and vals['points'] <= 0:
            raise ValidationError('Points must be greater than zero!')
        
        if 'expiry_date' not in vals and 'program_id' in vals:
            program = self.env['loyalty.program'].browse(vals['program_id'])
            if program.points_expiry_days:
                from datetime import datetime, timedelta
                expiry_date = datetime.now() + timedelta(days=program.points_expiry_days)
                vals['expiry_date'] = expiry_date.date()
        
        return super(LoyaltyPoints, self).create(vals)
    
    def write(self, vals):
        """Update loyalty points with validation"""
        if 'points' in vals and vals['points'] <= 0:
            raise ValidationError('Points must be greater than zero!')
        
        return super(LoyaltyPoints, self).write(vals)
    
    def action_expire_points(self):
        """Mark points as expired"""
        self.write({
            'is_expired': True,
            'points_type': 'expired',
        })
    
    def action_send_expiry_notification(self):
        """Send expiry notification to customer"""
        for record in self:
            if not record.expiry_notification_sent:
                # Send notification logic would go here
                record.write({'expiry_notification_sent': True})
    
    def action_adjust_points(self, adjustment_points, reason):
        """Adjust points with reason"""
        self.create({
            'name': f'ADJ-{self.name}',
            'partner_id': self.partner_id.id,
            'program_id': self.program_id.id,
            'points': abs(adjustment_points),
            'points_type': 'adjusted',
            'transaction_type': 'adjustment',
            'description': reason,
        })


class LoyaltyPointsBalance(BaseModel):
    """Loyalty Points Balance"""
    
    _name = 'loyalty.points.balance'
    _description = 'Loyalty Points Balance'
    _order = 'partner_id, program_id'
    
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', required=True)
    
    # Balance Information
    total_points = IntegerField(string='Total Points', default=0)
    available_points = IntegerField(string='Available Points', default=0)
    expired_points = IntegerField(string='Expired Points', default=0)
    redeemed_points = IntegerField(string='Redeemed Points', default=0)
    
    # Tier Information
    tier_id = Many2oneField('loyalty.tier', string='Current Tier')
    tier_points = IntegerField(string='Tier Points', default=0)
    next_tier_id = Many2oneField('loyalty.tier', string='Next Tier')
    next_tier_points = IntegerField(string='Next Tier Points', default=0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_balance(self):
        """Compute points balance"""
        for record in self:
            # Get all points for this customer and program
            points = self.env['loyalty.points'].search([
                ('partner_id', '=', record.partner_id.id),
                ('program_id', '=', record.program_id.id),
            ])
            
            total_earned = sum(points.filtered(lambda p: p.points_type == 'earned').mapped('points'))
            total_redeemed = sum(points.filtered(lambda p: p.points_type == 'redeemed').mapped('points'))
            total_expired = sum(points.filtered(lambda p: p.points_type == 'expired').mapped('points'))
            
            record.total_points = total_earned
            record.redeemed_points = total_redeemed
            record.expired_points = total_expired
            record.available_points = total_earned - total_redeemed - total_expired
    
    def action_update_balance(self):
        """Update points balance"""
        self._compute_balance()