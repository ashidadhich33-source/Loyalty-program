# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountApprovalWorkflow(BaseModel):
    """Discount Approval Workflow"""
    
    _name = 'discount.approval.workflow'
    _description = 'Discount Approval Workflow'
    _order = 'name'
    
    name = CharField(string='Workflow Name', required=True, size=100)
    code = CharField(string='Workflow Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Workflow Configuration
    is_active = BooleanField(string='Active', default=True)
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    
    # Approval Steps
    step_ids = One2manyField('discount.approval.step', 'workflow_id', string='Approval Steps')
    step_count = IntegerField(string='Step Count', compute='_compute_step_count', store=True)
    
    # Workflow Settings
    auto_approve = BooleanField(string='Auto Approve', default=False)
    require_all_approvers = BooleanField(string='Require All Approvers', default=True)
    allow_self_approval = BooleanField(string='Allow Self Approval', default=False)
    escalation_days = IntegerField(string='Escalation Days', default=3)
    
    # Kids Clothing Specific
    age_group_target = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Target', default='all')
    
    gender_target = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Target', default='all')
    
    season_target = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all', 'All Seasons'),
    ], string='Season Target', default='all')
    
    # Analytics
    total_requests = IntegerField(string='Total Requests', default=0)
    approved_requests = IntegerField(string='Approved Requests', default=0)
    rejected_requests = IntegerField(string='Rejected Requests', default=0)
    pending_requests = IntegerField(string='Pending Requests', default=0)
    approval_rate = FloatField(string='Approval Rate', digits=(16, 2), default=0.0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_step_count(self):
        """Compute step count"""
        for record in self:
            record.step_count = len(record.step_ids)
    
    def create(self, vals):
        """Create approval workflow with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Approval workflow code must be unique!')
        
        return super(DiscountApprovalWorkflow, self).create(vals)
    
    def write(self, vals):
        """Update approval workflow with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Approval workflow code must be unique!')
        
        return super(DiscountApprovalWorkflow, self).write(vals)
    
    def action_activate(self):
        """Activate approval workflow"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate approval workflow"""
        self.write({'is_active': False})
    
    def action_view_requests(self):
        """View approval requests"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Approval Requests',
            'res_model': 'discount.approval.request',
            'view_mode': 'tree,form',
            'domain': [('workflow_id', '=', self.id)],
        }


class DiscountApprovalStep(BaseModel):
    """Discount Approval Step"""
    
    _name = 'discount.approval.step'
    _description = 'Discount Approval Step'
    _order = 'sequence, name'
    
    name = CharField(string='Step Name', required=True, size=100)
    workflow_id = Many2oneField('discount.approval.workflow', string='Workflow', required=True)
    sequence = IntegerField(string='Sequence', required=True, default=10)
    is_active = BooleanField(string='Active', default=True)
    
    # Step Configuration
    step_type = SelectionField([
        ('approval', 'Approval'),
        ('notification', 'Notification'),
        ('escalation', 'Escalation'),
        ('condition', 'Condition'),
    ], string='Step Type', required=True, default='approval')
    
    # Approvers
    approver_ids = One2manyField('discount.approval.approver', 'step_id', string='Approvers')
    approver_count = IntegerField(string='Approver Count', compute='_compute_approver_count', store=True)
    
    # Approval Settings
    approval_type = SelectionField([
        ('any', 'Any Approver'),
        ('all', 'All Approvers'),
        ('majority', 'Majority'),
        ('first', 'First Response'),
    ], string='Approval Type', default='any')
    
    # Conditions
    condition_field = CharField(string='Condition Field', size=100)
    condition_operator = SelectionField([
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
    ], string='Condition Operator', default='equals')
    condition_value = TextField(string='Condition Value')
    
    # Timeout Settings
    timeout_days = IntegerField(string='Timeout (Days)', default=0)  # 0 = no timeout
    escalation_user_id = Many2oneField('res.users', string='Escalation User')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_approver_count(self):
        """Compute approver count"""
        for record in self:
            record.approver_count = len(record.approver_ids)


class DiscountApprovalApprover(BaseModel):
    """Discount Approval Approver"""
    
    _name = 'discount.approval.approver'
    _description = 'Discount Approval Approver'
    _order = 'sequence, user_id'
    
    step_id = Many2oneField('discount.approval.step', string='Step', required=True)
    user_id = Many2oneField('res.users', string='Approver', required=True)
    sequence = IntegerField(string='Sequence', default=10)
    is_active = BooleanField(string='Active', default=True)
    
    # Approval Settings
    approval_type = SelectionField([
        ('required', 'Required'),
        ('optional', 'Optional'),
        ('escalation', 'Escalation'),
    ], string='Approval Type', default='required')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)


class DiscountApprovalRequest(BaseModel):
    """Discount Approval Request"""
    
    _name = 'discount.approval.request'
    _description = 'Discount Approval Request'
    _order = 'create_date desc, name'
    
    name = CharField(string='Request Reference', required=True, size=64)
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    workflow_id = Many2oneField('discount.approval.workflow', string='Approval Workflow', required=True)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    order_id = Many2oneField('sale.order', string='Sale Order')
    
    # Request Details
    request_type = SelectionField([
        ('discount', 'Discount Request'),
        ('coupon', 'Coupon Request'),
        ('bulk', 'Bulk Discount Request'),
        ('special', 'Special Discount Request'),
    ], string='Request Type', required=True, default='discount')
    
    discount_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
        ('free_shipping', 'Free Shipping'),
        ('loyalty_points', 'Loyalty Points'),
    ], string='Discount Type', required=True, default='percentage')
    
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2), default=0.0)
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Request Status
    state = SelectionField([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    
    # Approval Details
    current_step_id = Many2oneField('discount.approval.step', string='Current Step')
    approved_by = Many2oneField('res.users', string='Approved By')
    approved_date = DateTimeField(string='Approved Date')
    rejected_by = Many2oneField('res.users', string='Rejected By')
    rejected_date = DateTimeField(string='Rejected Date')
    rejection_reason = TextField(string='Rejection Reason')
    
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
    justification = TextField(string='Justification')
    note = TextField(string='Internal Note')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def action_submit(self):
        """Submit approval request"""
        self.write({'state': 'submitted'})
    
    def action_approve(self):
        """Approve request"""
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approved_date': self.env['datetime'].now(),
        })
    
    def action_reject(self, reason):
        """Reject request"""
        self.write({
            'state': 'rejected',
            'rejected_by': self.env.user.id,
            'rejected_date': self.env['datetime'].now(),
            'rejection_reason': reason,
        })
    
    def action_cancel(self):
        """Cancel request"""
        self.write({'state': 'cancelled'})