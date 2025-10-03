# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductCategoryRule(models.Model):
    _name = 'product.category.rule'
    _description = 'Product Category Rule'
    _order = 'sequence, name'

    name = fields.Char(
        string='Rule Name',
        required=True,
        help="Name of the category rule"
    )
    description = fields.Text(
        string='Description',
        help="Description of this rule"
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this rule is active"
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of rule execution"
    )
    
    # Rule Conditions
    condition_type = fields.Selection([
        ('age_group', 'Age Group'),
        ('gender', 'Gender'),
        ('season', 'Season'),
        ('brand_type', 'Brand Type'),
        ('style_type', 'Style Type'),
        ('color_family', 'Color Family'),
        ('size_range', 'Size Range'),
        ('price_range', 'Price Range'),
        ('margin_range', 'Margin Range'),
        ('custom', 'Custom Condition'),
    ], string='Condition Type', required=True, help="Type of condition for this rule")
    
    condition_operator = fields.Selection([
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('in', 'In'),
        ('not_in', 'Not In'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('between', 'Between'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
    ], string='Operator', required=True, help="Operator for the condition")
    
    condition_value = fields.Char(
        string='Condition Value',
        help="Value for the condition"
    )
    condition_value_2 = fields.Char(
        string='Condition Value 2',
        help="Second value for between conditions"
    )
    
    # Rule Actions
    action_type = fields.Selection([
        ('assign_category', 'Assign Category'),
        ('assign_template', 'Assign Template'),
        ('set_margin', 'Set Margin'),
        ('set_price', 'Set Price'),
        ('set_tag', 'Set Tag'),
        ('send_notification', 'Send Notification'),
        ('create_task', 'Create Task'),
        ('custom', 'Custom Action'),
    ], string='Action Type', required=True, help="Type of action to perform")
    
    target_category_id = fields.Many2one(
        'product.category',
        string='Target Category',
        help="Category to assign to matching products"
    )
    target_template_id = fields.Many2one(
        'product.category.template',
        string='Target Template',
        help="Template to apply to matching products"
    )
    margin_value = fields.Float(
        string='Margin Value (%)',
        digits=(5, 2),
        help="Margin percentage to set"
    )
    price_value = fields.Float(
        string='Price Value',
        digits=(12, 2),
        help="Price to set"
    )
    tag_ids = fields.Many2many(
        'product.category.tag',
        'category_rule_tag_rel',
        'rule_id',
        'tag_id',
        string='Tags',
        help="Tags to assign to matching products"
    )
    notification_message = fields.Text(
        string='Notification Message',
        help="Message to send in notification"
    )
    task_description = fields.Text(
        string='Task Description',
        help="Description for the task to create"
    )
    
    # Rule Scope
    apply_to = fields.Selection([
        ('new_products', 'New Products Only'),
        ('existing_products', 'Existing Products Only'),
        ('all_products', 'All Products'),
    ], string='Apply To', default='new_products', help="Scope of products to apply this rule to")
    
    # Rule Execution
    last_execution = fields.Datetime(
        string='Last Execution',
        readonly=True,
        help="When this rule was last executed"
    )
    execution_count = fields.Integer(
        string='Execution Count',
        readonly=True,
        default=0,
        help="Number of times this rule has been executed"
    )
    success_count = fields.Integer(
        string='Success Count',
        readonly=True,
        default=0,
        help="Number of successful executions"
    )
    error_count = fields.Integer(
        string='Error Count',
        readonly=True,
        default=0,
        help="Number of failed executions"
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this rule belongs to"
    )
    
    # Methods
    def execute_rule(self, products=None):
        """Execute this rule on the given products"""
        if not products:
            products = self._get_target_products()
        
        success_count = 0
        error_count = 0
        
        for product in products:
            try:
                if self._check_condition(product):
                    self._execute_action(product)
                    success_count += 1
            except Exception as e:
                _logger.error(f"Error executing rule {self.name} on product {product.id}: {str(e)}")
                error_count += 1
        
        # Update execution statistics
        self.write({
            'last_execution': fields.Datetime.now(),
            'execution_count': self.execution_count + 1,
            'success_count': self.success_count + success_count,
            'error_count': self.error_count + error_count,
        })
        
        return {
            'success_count': success_count,
            'error_count': error_count,
            'total_processed': len(products)
        }
    
    def _get_target_products(self):
        """Get products to apply this rule to"""
        domain = []
        
        if self.apply_to == 'new_products':
            domain.append(('create_date', '>=', fields.Date.today()))
        elif self.apply_to == 'existing_products':
            domain.append(('create_date', '<', fields.Date.today()))
        
        return self.env['product.template'].search(domain)
    
    def _check_condition(self, product):
        """Check if the product matches the rule condition"""
        if not self.condition_type or not self.condition_operator:
            return False
        
        # Get the value to check based on condition type
        if self.condition_type == 'age_group':
            value = product.categ_id.age_group if product.categ_id else False
        elif self.condition_type == 'gender':
            value = product.categ_id.gender if product.categ_id else False
        elif self.condition_type == 'season':
            value = product.categ_id.season if product.categ_id else False
        elif self.condition_type == 'brand_type':
            value = product.categ_id.brand_type if product.categ_id else False
        elif self.condition_type == 'style_type':
            value = product.categ_id.style_type if product.categ_id else False
        elif self.condition_type == 'color_family':
            value = product.categ_id.color_family if product.categ_id else False
        elif self.condition_type == 'size_range':
            value = product.categ_id.size_range if product.categ_id else False
        elif self.condition_type == 'price_range':
            value = product.list_price
        elif self.condition_type == 'margin_range':
            value = product.margin_percentage if hasattr(product, 'margin_percentage') else 0
        else:
            return False
        
        # Check the condition
        if self.condition_operator == 'equals':
            return str(value) == str(self.condition_value)
        elif self.condition_operator == 'not_equals':
            return str(value) != str(self.condition_value)
        elif self.condition_operator == 'in':
            return str(value) in str(self.condition_value).split(',')
        elif self.condition_operator == 'not_in':
            return str(value) not in str(self.condition_value).split(',')
        elif self.condition_operator == 'greater_than':
            return float(value or 0) > float(self.condition_value or 0)
        elif self.condition_operator == 'less_than':
            return float(value or 0) < float(self.condition_value or 0)
        elif self.condition_operator == 'between':
            min_val = float(self.condition_value or 0)
            max_val = float(self.condition_value_2 or 0)
            return min_val <= float(value or 0) <= max_val
        elif self.condition_operator == 'contains':
            return str(self.condition_value).lower() in str(value or '').lower()
        elif self.condition_operator == 'not_contains':
            return str(self.condition_value).lower() not in str(value or '').lower()
        
        return False
    
    def _execute_action(self, product):
        """Execute the rule action on the product"""
        if self.action_type == 'assign_category':
            if self.target_category_id:
                product.categ_id = self.target_category_id
        elif self.action_type == 'assign_template':
            if self.target_template_id:
                self.target_template_id.apply_to_category(product.categ_id)
        elif self.action_type == 'set_margin':
            if self.margin_value:
                # This would set the margin on the product
                pass
        elif self.action_type == 'set_price':
            if self.price_value:
                product.list_price = self.price_value
        elif self.action_type == 'set_tag':
            if self.tag_ids:
                product.categ_id.tag_ids = [(6, 0, self.tag_ids.ids)]
        elif self.action_type == 'send_notification':
            if self.notification_message:
                # Send notification
                pass
        elif self.action_type == 'create_task':
            if self.task_description:
                # Create task
                pass
    
    def test_rule(self, products=None):
        """Test this rule without executing actions"""
        if not products:
            products = self._get_target_products()
        
        matching_products = []
        for product in products:
            if self._check_condition(product):
                matching_products.append(product)
        
        return {
            'total_products': len(products),
            'matching_products': len(matching_products),
            'match_percentage': (len(matching_products) / len(products) * 100) if products else 0
        }
    
    def reset_statistics(self):
        """Reset execution statistics"""
        self.write({
            'last_execution': False,
            'execution_count': 0,
            'success_count': 0,
            'error_count': 0,
        })
    
    def duplicate_rule(self):
        """Duplicate this rule"""
        copy_vals = {
            'name': f"{self.name} (Copy)",
            'description': self.description,
            'condition_type': self.condition_type,
            'condition_operator': self.condition_operator,
            'condition_value': self.condition_value,
            'condition_value_2': self.condition_value_2,
            'action_type': self.action_type,
            'target_category_id': self.target_category_id.id,
            'target_template_id': self.target_template_id.id,
            'margin_value': self.margin_value,
            'price_value': self.price_value,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'notification_message': self.notification_message,
            'task_description': self.task_description,
            'apply_to': self.apply_to,
        }
        return self.create(copy_vals)