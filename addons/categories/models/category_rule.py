# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CategoryRule(models.Model):
    _name = 'category.rule'
    _description = 'Category Rule'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Rule Name',
        required=True,
        help="Name of the business rule for this category"
    )
    
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        required=True,
        ondelete='cascade',
        help="Category this rule applies to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of rules in the category"
    )
    
    rule_type = fields.Selection([
        ('pricing', 'Pricing Rule'),
        ('discount', 'Discount Rule'),
        ('inventory', 'Inventory Rule'),
        ('marketing', 'Marketing Rule'),
        ('validation', 'Validation Rule'),
        ('workflow', 'Workflow Rule'),
    ], string='Rule Type', required=True, default='pricing',
       help="Type of business rule")
    
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this rule is active"
    )
    
    priority = fields.Selection([
        ('1', 'Very High'),
        ('2', 'High'),
        ('3', 'Medium'),
        ('4', 'Low'),
        ('5', 'Very Low'),
    ], string='Priority', default='3',
       help="Priority of this rule")
    
    # Rule Conditions
    condition_type = fields.Selection([
        ('always', 'Always'),
        ('date_range', 'Date Range'),
        ('customer_type', 'Customer Type'),
        ('quantity', 'Quantity'),
        ('amount', 'Amount'),
        ('season', 'Season'),
        ('age_group', 'Age Group'),
        ('gender', 'Gender'),
        ('brand', 'Brand'),
        ('custom', 'Custom Condition'),
    ], string='Condition Type', required=True, default='always',
       help="Type of condition for this rule")
    
    # Date Range Conditions
    date_from = fields.Date(
        string='Date From',
        help="Start date for date range condition"
    )
    
    date_to = fields.Date(
        string='Date To',
        help="End date for date range condition"
    )
    
    # Customer Type Conditions
    customer_type = fields.Selection([
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
        ('all', 'All Types'),
    ], string='Customer Type', default='all',
       help="Customer type for this rule")
    
    # Quantity Conditions
    min_quantity = fields.Float(
        string='Minimum Quantity',
        digits='Product Unit of Measure',
        help="Minimum quantity for quantity condition"
    )
    
    max_quantity = fields.Float(
        string='Maximum Quantity',
        digits='Product Unit of Measure',
        help="Maximum quantity for quantity condition"
    )
    
    # Amount Conditions
    min_amount = fields.Float(
        string='Minimum Amount',
        digits='Product Price',
        help="Minimum amount for amount condition"
    )
    
    max_amount = fields.Float(
        string='Maximum Amount',
        digits='Product Price',
        help="Maximum amount for amount condition"
    )
    
    # Season Conditions
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', default='all_season',
       help="Season for this rule")
    
    # Age Group Conditions
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', default='all',
       help="Age group for this rule")
    
    # Gender Conditions
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender', default='all',
       help="Gender for this rule")
    
    # Brand Conditions
    brand_ids = fields.Many2many(
        'product.brand',
        string='Brands',
        help="Brands for this rule"
    )
    
    # Custom Condition
    custom_condition = fields.Text(
        string='Custom Condition',
        help="Custom condition expression for this rule"
    )
    
    # Rule Actions
    action_type = fields.Selection([
        ('set_price', 'Set Price'),
        ('apply_discount', 'Apply Discount'),
        ('set_margin', 'Set Margin'),
        ('set_stock', 'Set Stock'),
        ('send_notification', 'Send Notification'),
        ('create_task', 'Create Task'),
        ('run_script', 'Run Script'),
        ('custom', 'Custom Action'),
    ], string='Action Type', required=True, default='set_price',
       help="Type of action for this rule")
    
    # Pricing Actions
    price_type = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('percentage', 'Percentage'),
        ('formula', 'Formula'),
    ], string='Price Type', default='fixed',
       help="Type of price calculation")
    
    price_value = fields.Float(
        string='Price Value',
        digits='Product Price',
        help="Price value for pricing action"
    )
    
    price_formula = fields.Text(
        string='Price Formula',
        help="Formula for price calculation"
    )
    
    # Discount Actions
    discount_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', default='percentage',
       help="Type of discount")
    
    discount_value = fields.Float(
        string='Discount Value',
        digits='Product Price',
        help="Discount value"
    )
    
    # Margin Actions
    margin_percentage = fields.Float(
        string='Margin Percentage (%)',
        digits=(5, 2),
        help="Margin percentage for margin action"
    )
    
    # Stock Actions
    stock_action = fields.Selection([
        ('set_min', 'Set Minimum Stock'),
        ('set_max', 'Set Maximum Stock'),
        ('set_reorder', 'Set Reorder Point'),
        ('set_safety', 'Set Safety Stock'),
    ], string='Stock Action', default='set_min',
       help="Type of stock action")
    
    stock_value = fields.Float(
        string='Stock Value',
        digits='Product Unit of Measure',
        help="Stock value for stock action"
    )
    
    # Notification Actions
    notification_type = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('in_app', 'In-App'),
        ('all', 'All Channels'),
    ], string='Notification Type', default='email',
       help="Type of notification")
    
    notification_template = fields.Text(
        string='Notification Template',
        help="Template for notification"
    )
    
    # Task Actions
    task_name = fields.Char(
        string='Task Name',
        help="Name of the task to create"
    )
    
    task_description = fields.Text(
        string='Task Description',
        help="Description of the task to create"
    )
    
    # Script Actions
    script_name = fields.Char(
        string='Script Name',
        help="Name of the script to run"
    )
    
    script_code = fields.Text(
        string='Script Code',
        help="Code of the script to run"
    )
    
    # Custom Action
    custom_action = fields.Text(
        string='Custom Action',
        help="Custom action code for this rule"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this rule belongs to"
    )
    
    # Rule Execution
    last_executed = fields.Datetime(
        string='Last Executed',
        help="When this rule was last executed"
    )
    
    execution_count = fields.Integer(
        string='Execution Count',
        default=0,
        help="Number of times this rule has been executed"
    )
    
    success_count = fields.Integer(
        string='Success Count',
        default=0,
        help="Number of successful executions"
    )
    
    failure_count = fields.Integer(
        string='Failure Count',
        default=0,
        help="Number of failed executions"
    )
    
    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        for rule in self:
            if rule.date_from and rule.date_to:
                if rule.date_from > rule.date_to:
                    raise ValidationError(_('Date from cannot be greater than date to.'))
    
    @api.constrains('min_quantity', 'max_quantity')
    def _check_quantity_range(self):
        for rule in self:
            if rule.min_quantity and rule.max_quantity:
                if rule.min_quantity > rule.max_quantity:
                    raise ValidationError(_('Minimum quantity cannot be greater than maximum quantity.'))
    
    @api.constrains('min_amount', 'max_amount')
    def _check_amount_range(self):
        for rule in self:
            if rule.min_amount and rule.max_amount:
                if rule.min_amount > rule.max_amount:
                    raise ValidationError(_('Minimum amount cannot be greater than maximum amount.'))
    
    def check_condition(self, context=None):
        """Check if this rule's condition is met"""
        context = context or {}
        
        if not self.is_active:
            return False
        
        if self.condition_type == 'always':
            return True
        
        elif self.condition_type == 'date_range':
            today = fields.Date.today()
            if self.date_from and today < self.date_from:
                return False
            if self.date_to and today > self.date_to:
                return False
            return True
        
        elif self.condition_type == 'customer_type':
            customer_type = context.get('customer_type', 'all')
            return customer_type == self.customer_type or self.customer_type == 'all'
        
        elif self.condition_type == 'quantity':
            quantity = context.get('quantity', 0)
            if self.min_quantity and quantity < self.min_quantity:
                return False
            if self.max_quantity and quantity > self.max_quantity:
                return False
            return True
        
        elif self.condition_type == 'amount':
            amount = context.get('amount', 0)
            if self.min_amount and amount < self.min_amount:
                return False
            if self.max_amount and amount > self.max_amount:
                return False
            return True
        
        elif self.condition_type == 'season':
            season = context.get('season', 'all_season')
            return season == self.season or self.season == 'all_season'
        
        elif self.condition_type == 'age_group':
            age_group = context.get('age_group', 'all')
            return age_group == self.age_group or self.age_group == 'all'
        
        elif self.condition_type == 'gender':
            gender = context.get('gender', 'all')
            return gender == self.gender or self.gender == 'all'
        
        elif self.condition_type == 'brand':
            brand_id = context.get('brand_id')
            if not brand_id:
                return False
            return brand_id in self.brand_ids.ids
        
        elif self.condition_type == 'custom':
            # Custom condition evaluation would go here
            # This is a placeholder for custom logic
            return True
        
        return False
    
    def execute_action(self, context=None):
        """Execute this rule's action"""
        context = context or {}
        
        try:
            if self.action_type == 'set_price':
                return self._execute_set_price(context)
            elif self.action_type == 'apply_discount':
                return self._execute_apply_discount(context)
            elif self.action_type == 'set_margin':
                return self._execute_set_margin(context)
            elif self.action_type == 'set_stock':
                return self._execute_set_stock(context)
            elif self.action_type == 'send_notification':
                return self._execute_send_notification(context)
            elif self.action_type == 'create_task':
                return self._execute_create_task(context)
            elif self.action_type == 'run_script':
                return self._execute_run_script(context)
            elif self.action_type == 'custom':
                return self._execute_custom_action(context)
            
            # Update execution statistics
            self.last_executed = fields.Datetime.now()
            self.execution_count += 1
            self.success_count += 1
            
            return True
            
        except Exception as e:
            self.last_executed = fields.Datetime.now()
            self.execution_count += 1
            self.failure_count += 1
            raise ValidationError(_('Rule execution failed: %s') % str(e))
    
    def _execute_set_price(self, context):
        """Execute set price action"""
        # Implementation would go here
        pass
    
    def _execute_apply_discount(self, context):
        """Execute apply discount action"""
        # Implementation would go here
        pass
    
    def _execute_set_margin(self, context):
        """Execute set margin action"""
        # Implementation would go here
        pass
    
    def _execute_set_stock(self, context):
        """Execute set stock action"""
        # Implementation would go here
        pass
    
    def _execute_send_notification(self, context):
        """Execute send notification action"""
        # Implementation would go here
        pass
    
    def _execute_create_task(self, context):
        """Execute create task action"""
        # Implementation would go here
        pass
    
    def _execute_run_script(self, context):
        """Execute run script action"""
        # Implementation would go here
        pass
    
    def _execute_custom_action(self, context):
        """Execute custom action"""
        # Implementation would go here
        pass