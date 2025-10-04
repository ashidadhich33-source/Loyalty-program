#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Transition Model
============================================

Workflow transition management for state transitions.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowTransition(BaseModel, KidsClothingMixin):
    """Workflow Transition Model for State Transitions"""
    
    _name = 'workflow.transition'
    _description = 'Workflow Transition'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Transition Name', required=True, size=200)
    code = CharField('Transition Code', required=True, size=100)
    description = TextField('Description')
    workflow_id = Many2OneField('workflow.definition', 'Workflow', required=True)
    
    # Transition Configuration
    from_state = CharField('From State', required=True, size=100)
    to_state = CharField('To State', required=True, size=100)
    
    # Transition Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_default = BooleanField('Default Transition', default=False)
    
    # Transition Conditions
    condition_ids = One2ManyField('workflow.condition', 'transition_id', 'Conditions')
    required_permission = CharField('Required Permission', size=100)
    required_group = CharField('Required Group', size=100)
    required_role = CharField('Required Role', size=100)
    
    # Transition Actions
    action_ids = One2ManyField('workflow.action', 'transition_id', 'Actions')
    
    # Transition Properties
    transition_type = SelectionField([
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('conditional', 'Conditional'),
        ('approval', 'Approval'),
        ('custom', 'Custom'),
    ], 'Transition Type', default='manual')
    
    # Transition Validation
    validation_script = TextField('Validation Script', 
                                 help='Python script for transition validation')
    validation_domain = TextField('Validation Domain', 
                                 help='Domain for transition validation')
    
    # Transition Statistics
    execution_count = IntegerField('Execution Count', default=0)
    success_count = IntegerField('Success Count', default=0)
    failure_count = IntegerField('Failure Count', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    average_execution_time = FloatField('Average Execution Time (seconds)', digits=(10, 2), default=0.0)
    
    # Transition UI
    button_text = CharField('Button Text', size=200)
    button_icon = CharField('Button Icon', size=100)
    button_color = CharField('Button Color', size=20, default='#000000')
    confirmation_message = TextField('Confirmation Message')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'transition_group_ids', 'Access Groups')
    
    def execute_transition(self, instance, context=None):
        """Execute workflow transition"""
        try:
            # Validate transition
            if not self._validate_transition(instance, context):
                raise Exception(f"Transition {self.code} validation failed")
            
            # Check conditions
            if not self._check_conditions(instance, context):
                raise Exception(f"Transition {self.code} conditions not met")
            
            # Check permissions
            if not self._check_permissions(instance, context):
                raise Exception(f"Transition {self.code} permission denied")
            
            # Update instance state
            instance.write({
                'previous_state': instance.current_state,
                'current_state': self.to_state,
                'last_transition': self.code,
                'last_transition_date': self.env.cr.now(),
                'transition_count': instance.transition_count + 1,
            })
            
            # Execute transition actions
            for action in self.action_ids:
                try:
                    action.execute_action(instance)
                except Exception as e:
                    # Log error but continue
                    pass
            
            # Update statistics
            self.write({
                'execution_count': self.execution_count + 1,
                'success_count': self.success_count + 1,
                'success_rate': self._calculate_success_rate(),
            })
            
            return True
            
        except Exception as e:
            # Update failure statistics
            self.write({
                'execution_count': self.execution_count + 1,
                'failure_count': self.failure_count + 1,
                'success_rate': self._calculate_success_rate(),
            })
            raise e
    
    def _validate_transition(self, instance, context):
        """Validate transition execution"""
        try:
            # Check if transition is active
            if not self.active:
                return False
            
            # Check if instance is in correct state
            if instance.current_state != self.from_state:
                return False
            
            # Execute validation script if provided
            if self.validation_script:
                # Implementation would execute validation script safely
                pass
            
            # Evaluate validation domain if provided
            if self.validation_domain:
                # Implementation would evaluate validation domain
                pass
            
            return True
            
        except Exception as e:
            return False
    
    def _check_conditions(self, instance, context):
        """Check transition conditions"""
        for condition in self.condition_ids:
            if not condition.evaluate_condition(instance, context):
                return False
        return True
    
    def _check_permissions(self, instance, context):
        """Check transition permissions"""
        user_id = context.get('user_id') if context else self.env.uid
        
        # Check required permission
        if self.required_permission:
            # Implementation would check user permission
            pass
        
        # Check required group
        if self.required_group:
            user_groups = self._get_user_groups(user_id)
            if self.required_group not in [g.name for g in user_groups]:
                return False
        
        # Check required role
        if self.required_role:
            user_roles = self._get_user_roles(user_id)
            if self.required_role not in [r.name for r in user_roles]:
                return False
        
        return True
    
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
        total_attempts = self.success_count + self.failure_count
        if total_attempts == 0:
            return 0.0
        
        success_rate = (self.success_count / total_attempts) * 100
        return round(success_rate, 2)
    
    def get_available_for_state(self, state):
        """Get transitions available for a state"""
        return self.search([
            ('workflow_id', '=', self.workflow_id.id),
            ('from_state', '=', state),
            ('active', '=', True)
        ])
    
    def get_transition_summary(self):
        """Get transition summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'from_state': self.from_state,
            'to_state': self.to_state,
            'transition_type': self.transition_type,
            'execution_count': self.execution_count,
            'success_rate': self.success_rate,
            'is_default': self.is_default,
        }


class WorkflowTransitionTemplate(BaseModel, KidsClothingMixin):
    """Workflow Transition Template for Reusable Transitions"""
    
    _name = 'workflow.transition.template'
    _description = 'Workflow Transition Template'
    
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    category = CharField('Category', size=100)
    
    # Template Configuration
    template_config = TextField('Template Configuration', 
                               help='JSON template configuration')
    transition_data = TextField('Transition Data', 
                               help='JSON transition data')
    
    # Template Usage
    usage_count = IntegerField('Usage Count', default=0)
    is_public = BooleanField('Public Template', default=False)
    
    def create_transition_from_template(self, workflow_id, transition_name, from_state, to_state):
        """Create transition from template"""
        try:
            # Parse template configuration
            template_config = self._parse_template_config()
            
            # Create transition
            transition_data = {
                'name': transition_name,
                'code': transition_name.lower().replace(' ', '_'),
                'description': template_config.get('description', ''),
                'workflow_id': workflow_id,
                'from_state': from_state,
                'to_state': to_state,
                'transition_type': template_config.get('transition_type', 'manual'),
                'button_text': template_config.get('button_text', transition_name),
                'button_icon': template_config.get('button_icon', ''),
                'button_color': template_config.get('button_color', '#000000'),
                'confirmation_message': template_config.get('confirmation_message', ''),
                'user_id': self.env.uid,
            }
            
            transition = self.env['workflow.transition'].create(transition_data)
            
            # Create transition components from template
            self._create_transition_components(transition.id, template_config)
            
            # Update usage count
            self.write({'usage_count': self.usage_count + 1})
            
            return transition
            
        except Exception as e:
            raise e
    
    def _parse_template_config(self):
        """Parse template configuration"""
        import json
        try:
            return json.loads(self.template_config) if self.template_config else {}
        except:
            return {}
    
    def _create_transition_components(self, transition_id, template_config):
        """Create transition components from template"""
        # Implementation would create conditions and actions from template
        pass