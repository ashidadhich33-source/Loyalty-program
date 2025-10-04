#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Condition Model
============================================

Workflow condition management for conditional logic.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowCondition(BaseModel, KidsClothingMixin):
    """Workflow Condition Model for Conditional Logic"""
    
    _name = 'workflow.condition'
    _description = 'Workflow Condition'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Condition Name', required=True, size=200)
    description = TextField('Description')
    workflow_id = Many2OneField('workflow.definition', 'Workflow')
    transition_id = Many2OneField('workflow.transition', 'Transition')
    
    # Condition Configuration
    condition_type = SelectionField([
        ('field_value', 'Field Value'),
        ('user_permission', 'User Permission'),
        ('group_membership', 'Group Membership'),
        ('role_assignment', 'Role Assignment'),
        ('time_based', 'Time Based'),
        ('date_based', 'Date Based'),
        ('script', 'Script'),
        ('domain', 'Domain'),
        ('custom', 'Custom'),
    ], 'Condition Type', required=True)
    
    # Condition Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_required = BooleanField('Required', default=True)
    
    # Field-based Conditions
    field_name = CharField('Field Name', size=100)
    field_operator = SelectionField([
        ('=', 'Equals'),
        ('!=', 'Not Equals'),
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('>=', 'Greater Than or Equal'),
        ('<=', 'Less Than or Equal'),
        ('in', 'In'),
        ('not in', 'Not In'),
        ('like', 'Like'),
        ('ilike', 'Ilike'),
        ('is_null', 'Is Null'),
        ('is_not_null', 'Is Not Null'),
    ], 'Field Operator', default='=')
    field_value = TextField('Field Value')
    
    # Permission-based Conditions
    required_permission = CharField('Required Permission', size=100)
    required_group = CharField('Required Group', size=100)
    required_role = CharField('Required Role', size=100)
    
    # Time-based Conditions
    time_condition = SelectionField([
        ('business_hours', 'Business Hours'),
        ('weekend', 'Weekend'),
        ('specific_time', 'Specific Time'),
        ('time_range', 'Time Range'),
    ], 'Time Condition')
    start_time = CharField('Start Time', size=10)
    end_time = CharField('End Time', size=10)
    timezone = CharField('Timezone', size=50, default='UTC')
    
    # Date-based Conditions
    date_condition = SelectionField([
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('this_year', 'This Year'),
        ('specific_date', 'Specific Date'),
        ('date_range', 'Date Range'),
    ], 'Date Condition')
    start_date = CharField('Start Date', size=20)
    end_date = CharField('End Date', size=20)
    
    # Script-based Conditions
    condition_script = TextField('Condition Script', 
                                help='Python script for condition evaluation')
    
    # Domain-based Conditions
    condition_domain = TextField('Condition Domain', 
                                help='Domain for condition evaluation')
    
    # Custom Conditions
    custom_condition = TextField('Custom Condition', 
                                help='Custom condition definition')
    
    # Condition Logic
    logical_operator = SelectionField([
        ('and', 'AND'),
        ('or', 'OR'),
        ('not', 'NOT'),
    ], 'Logical Operator', default='and')
    
    # Condition Statistics
    evaluation_count = IntegerField('Evaluation Count', default=0)
    true_count = IntegerField('True Count', default=0)
    false_count = IntegerField('False Count', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'condition_group_ids', 'Access Groups')
    
    def evaluate_condition(self, instance, context=None):
        """Evaluate workflow condition"""
        try:
            result = False
            
            if self.condition_type == 'field_value':
                result = self._evaluate_field_condition(instance, context)
            elif self.condition_type == 'user_permission':
                result = self._evaluate_permission_condition(instance, context)
            elif self.condition_type == 'group_membership':
                result = self._evaluate_group_condition(instance, context)
            elif self.condition_type == 'role_assignment':
                result = self._evaluate_role_condition(instance, context)
            elif self.condition_type == 'time_based':
                result = self._evaluate_time_condition(instance, context)
            elif self.condition_type == 'date_based':
                result = self._evaluate_date_condition(instance, context)
            elif self.condition_type == 'script':
                result = self._evaluate_script_condition(instance, context)
            elif self.condition_type == 'domain':
                result = self._evaluate_domain_condition(instance, context)
            elif self.condition_type == 'custom':
                result = self._evaluate_custom_condition(instance, context)
            
            # Update statistics
            self.write({
                'evaluation_count': self.evaluation_count + 1,
                'true_count': self.true_count + (1 if result else 0),
                'false_count': self.false_count + (0 if result else 1),
                'success_rate': self._calculate_success_rate(),
            })
            
            return result
            
        except Exception as e:
            # Update failure statistics
            self.write({
                'evaluation_count': self.evaluation_count + 1,
                'false_count': self.false_count + 1,
                'success_rate': self._calculate_success_rate(),
            })
            return False
    
    def _evaluate_field_condition(self, instance, context):
        """Evaluate field-based condition"""
        try:
            if not self.field_name:
                return False
            
            # Get field value from instance record
            record = self.env[instance.model_name].browse(instance.record_id)
            field_value = getattr(record, self.field_name, None)
            
            # Compare field value with condition value
            condition_value = self._parse_condition_value(self.field_value)
            
            return self._compare_values(field_value, self.field_operator, condition_value)
            
        except Exception as e:
            return False
    
    def _evaluate_permission_condition(self, instance, context):
        """Evaluate permission-based condition"""
        try:
            user_id = context.get('user_id') if context else self.env.uid
            
            if self.required_permission:
                # Check user permission
                # Implementation would check user permission
                pass
            
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_group_condition(self, instance, context):
        """Evaluate group membership condition"""
        try:
            user_id = context.get('user_id') if context else self.env.uid
            
            if self.required_group:
                user_groups = self._get_user_groups(user_id)
                return self.required_group in [g.name for g in user_groups]
            
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_role_condition(self, instance, context):
        """Evaluate role assignment condition"""
        try:
            user_id = context.get('user_id') if context else self.env.uid
            
            if self.required_role:
                user_roles = self._get_user_roles(user_id)
                return self.required_role in [r.name for r in user_roles]
            
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_time_condition(self, instance, context):
        """Evaluate time-based condition"""
        try:
            from datetime import datetime, time
            
            current_time = datetime.now().time()
            
            if self.time_condition == 'business_hours':
                # Check if current time is within business hours
                business_start = time(9, 0)  # 9:00 AM
                business_end = time(17, 0)   # 5:00 PM
                return business_start <= current_time <= business_end
            
            elif self.time_condition == 'weekend':
                # Check if current day is weekend
                current_day = datetime.now().weekday()
                return current_day >= 5  # Saturday = 5, Sunday = 6
            
            elif self.time_condition == 'specific_time':
                if self.start_time and self.end_time:
                    start_time = datetime.strptime(self.start_time, '%H:%M').time()
                    end_time = datetime.strptime(self.end_time, '%H:%M').time()
                    return start_time <= current_time <= end_time
            
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_date_condition(self, instance, context):
        """Evaluate date-based condition"""
        try:
            from datetime import datetime, date
            
            current_date = date.today()
            
            if self.date_condition == 'today':
                return True  # Always true for today
            
            elif self.date_condition == 'yesterday':
                yesterday = current_date - timedelta(days=1)
                return current_date == yesterday
            
            elif self.date_condition == 'this_week':
                # Check if current date is within this week
                # Implementation would check week boundaries
                return True
            
            elif self.date_condition == 'specific_date':
                if self.start_date:
                    target_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
                    return current_date == target_date
            
            elif self.date_condition == 'date_range':
                if self.start_date and self.end_date:
                    start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
                    end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
                    return start_date <= current_date <= end_date
            
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_script_condition(self, instance, context):
        """Evaluate script-based condition"""
        try:
            if not self.condition_script:
                return True
            
            # Execute condition script safely
            # Implementation would execute script with proper security measures
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_domain_condition(self, instance, context):
        """Evaluate domain-based condition"""
        try:
            if not self.condition_domain:
                return True
            
            # Parse and evaluate domain
            # Implementation would evaluate domain against instance record
            return True
            
        except Exception as e:
            return False
    
    def _evaluate_custom_condition(self, instance, context):
        """Evaluate custom condition"""
        try:
            if not self.custom_condition:
                return True
            
            # Evaluate custom condition
            # Implementation would evaluate custom condition
            return True
            
        except Exception as e:
            return False
    
    def _parse_condition_value(self, value_str):
        """Parse condition value string"""
        try:
            # Try to parse as JSON
            import json
            return json.loads(value_str)
        except:
            # Return as string
            return value_str
    
    def _compare_values(self, field_value, operator, condition_value):
        """Compare field value with condition value"""
        try:
            if operator == '=':
                return field_value == condition_value
            elif operator == '!=':
                return field_value != condition_value
            elif operator == '>':
                return field_value > condition_value
            elif operator == '<':
                return field_value < condition_value
            elif operator == '>=':
                return field_value >= condition_value
            elif operator == '<=':
                return field_value <= condition_value
            elif operator == 'in':
                return field_value in condition_value
            elif operator == 'not in':
                return field_value not in condition_value
            elif operator == 'like':
                return str(field_value).find(str(condition_value)) != -1
            elif operator == 'ilike':
                return str(field_value).lower().find(str(condition_value).lower()) != -1
            elif operator == 'is_null':
                return field_value is None
            elif operator == 'is_not_null':
                return field_value is not None
            else:
                return False
        except Exception as e:
            return False
    
    def _get_user_groups(self, user_id):
        """Get user groups"""
        user = self.env['users.user'].browse(user_id)
        return user.group_ids if user else []
    
    def _get_user_roles(self, user_id):
        """Get user roles"""
        user = self.env['users.user'].browse(user_id)
        return user.role_ids if user else []
    
    def _calculate_success_rate(self):
        """Calculate success rate"""
        total_evaluations = self.true_count + self.false_count
        if total_evaluations == 0:
            return 0.0
        
        success_rate = (self.true_count / total_evaluations) * 100
        return round(success_rate, 2)
    
    def get_condition_summary(self):
        """Get condition summary"""
        return {
            'id': self.id,
            'name': self.name,
            'condition_type': self.condition_type,
            'field_name': self.field_name,
            'field_operator': self.field_operator,
            'evaluation_count': self.evaluation_count,
            'success_rate': self.success_rate,
            'is_required': self.is_required,
        }