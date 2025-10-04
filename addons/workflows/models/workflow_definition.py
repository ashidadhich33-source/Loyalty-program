#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Definition Model
============================================

Workflow definition management for business process automation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowDefinition(BaseModel, KidsClothingMixin):
    """Workflow Definition Model for Business Process Automation"""
    
    _name = 'workflow.definition'
    _description = 'Workflow Definition'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Workflow Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    
    # Workflow Configuration
    workflow_type = SelectionField([
        ('approval', 'Approval Workflow'),
        ('sequential', 'Sequential Workflow'),
        ('parallel', 'Parallel Workflow'),
        ('conditional', 'Conditional Workflow'),
        ('state_machine', 'State Machine'),
        ('custom', 'Custom Workflow'),
    ], 'Workflow Type', required=True)
    
    # Model Configuration
    model_name = CharField('Model Name', required=True, size=100,
                          help='Model this workflow applies to')
    trigger_field = CharField('Trigger Field', size=100,
                             help='Field that triggers the workflow')
    trigger_condition = TextField('Trigger Condition', 
                                 help='Condition for workflow trigger')
    
    # Workflow Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_system = BooleanField('System Workflow', default=False)
    
    # Workflow States
    initial_state = CharField('Initial State', required=True, size=100, default='draft')
    final_states = TextField('Final States', 
                           help='Comma-separated list of final states')
    
    # Workflow Components
    state_ids = One2ManyField('workflow.state', 'workflow_id', 'States')
    transition_ids = One2ManyField('workflow.transition', 'workflow_id', 'Transitions')
    condition_ids = One2ManyField('workflow.condition', 'workflow_id', 'Conditions')
    action_ids = One2ManyField('workflow.action', 'workflow_id', 'Actions')
    
    # Workflow Execution
    auto_execute = BooleanField('Auto Execute', default=True)
    execution_timeout = IntegerField('Execution Timeout (minutes)', default=60)
    retry_count = IntegerField('Retry Count', default=3)
    retry_interval = IntegerField('Retry Interval (minutes)', default=5)
    
    # Workflow Statistics
    instance_count = IntegerField('Instance Count', default=0)
    success_count = IntegerField('Success Count', default=0)
    failure_count = IntegerField('Failure Count', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    average_duration = FloatField('Average Duration (minutes)', digits=(10, 2), default=0.0)
    
    # Workflow Templates
    template_id = Many2OneField('workflow.template', 'Template')
    is_template = BooleanField('Is Template', default=False)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'workflow_group_ids', 'Access Groups')
    
    def create_instance(self, record_id, context=None):
        """Create workflow instance"""
        try:
            instance_data = {
                'workflow_id': self.id,
                'record_id': record_id,
                'model_name': self.model_name,
                'current_state': self.initial_state,
                'status': 'running',
                'user_id': self.env.uid,
            }
            
            if context:
                instance_data['context'] = str(context)
            
            instance = self.env['workflow.instance'].create(instance_data)
            
            # Update statistics
            self.write({'instance_count': self.instance_count + 1})
            
            # Execute initial actions
            self._execute_initial_actions(instance)
            
            return instance
            
        except Exception as e:
            raise e
    
    def _execute_initial_actions(self, instance):
        """Execute initial workflow actions"""
        initial_actions = self.action_ids.filtered(lambda a: a.execute_on == 'on_workflow_start')
        
        for action in initial_actions:
            try:
                action.execute_action(instance)
            except Exception as e:
                # Log error but continue
                pass
    
    def get_available_transitions(self, current_state, context=None):
        """Get available transitions from current state"""
        transitions = self.transition_ids.filtered(
            lambda t: t.from_state == current_state and t.active
        )
        
        available_transitions = []
        for transition in transitions:
            if self._evaluate_transition_conditions(transition, context):
                available_transitions.append(transition)
        
        return available_transitions
    
    def _evaluate_transition_conditions(self, transition, context):
        """Evaluate transition conditions"""
        conditions = transition.condition_ids
        
        for condition in conditions:
            if not self._evaluate_condition(condition, context):
                return False
        
        return True
    
    def _evaluate_condition(self, condition, context):
        """Evaluate workflow condition"""
        try:
            if condition.condition_type == 'field_value':
                return self._evaluate_field_condition(condition, context)
            elif condition.condition_type == 'user_permission':
                return self._evaluate_permission_condition(condition, context)
            elif condition.condition_type == 'script':
                return self._evaluate_script_condition(condition, context)
            elif condition.condition_type == 'domain':
                return self._evaluate_domain_condition(condition, context)
            else:
                return True
        except Exception as e:
            return False
    
    def _evaluate_field_condition(self, condition, context):
        """Evaluate field-based condition"""
        # Implementation would evaluate field conditions
        return True
    
    def _evaluate_permission_condition(self, condition, context):
        """Evaluate permission-based condition"""
        # Implementation would evaluate permission conditions
        return True
    
    def _evaluate_script_condition(self, condition, context):
        """Evaluate script-based condition"""
        # Implementation would execute condition script
        return True
    
    def _evaluate_domain_condition(self, condition, context):
        """Evaluate domain-based condition"""
        # Implementation would evaluate domain conditions
        return True
    
    def execute_transition(self, instance, transition_code, context=None):
        """Execute workflow transition"""
        try:
            transition = self.transition_ids.filtered(
                lambda t: t.code == transition_code
            )
            
            if not transition:
                raise Exception(f"Transition {transition_code} not found")
            
            transition = transition[0]
            
            # Check if transition is available
            if not self._evaluate_transition_conditions(transition, context):
                raise Exception(f"Transition {transition_code} conditions not met")
            
            # Update instance state
            instance.write({
                'current_state': transition.to_state,
                'last_transition': transition_code,
                'last_transition_date': self.env.cr.now(),
            })
            
            # Execute transition actions
            transition_actions = self.action_ids.filtered(
                lambda a: a.transition_id.id == transition.id
            )
            
            for action in transition_actions:
                action.execute_action(instance)
            
            # Check if workflow is complete
            if transition.to_state in self._get_final_states():
                instance.write({'status': 'completed'})
                self._execute_completion_actions(instance)
            
            return True
            
        except Exception as e:
            # Update failure statistics
            self.write({'failure_count': self.failure_count + 1})
            raise e
    
    def _get_final_states(self):
        """Get final states list"""
        if self.final_states:
            return [state.strip() for state in self.final_states.split(',')]
        return []
    
    def _execute_completion_actions(self, instance):
        """Execute workflow completion actions"""
        completion_actions = self.action_ids.filtered(
            lambda a: a.execute_on == 'on_workflow_complete'
        )
        
        for action in completion_actions:
            try:
                action.execute_action(instance)
            except Exception as e:
                # Log error but continue
                pass
    
    def get_workflow_summary(self):
        """Get workflow summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'workflow_type': self.workflow_type,
            'model_name': self.model_name,
            'state_count': len(self.state_ids),
            'transition_count': len(self.transition_ids),
            'instance_count': self.instance_count,
            'success_rate': self.success_rate,
            'average_duration': self.average_duration,
        }


class WorkflowTemplate(BaseModel, KidsClothingMixin):
    """Workflow Template for Reusable Workflows"""
    
    _name = 'workflow.template'
    _description = 'Workflow Template'
    
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    category = CharField('Category', size=100)
    
    # Template Configuration
    template_config = TextField('Template Configuration', 
                               help='JSON template configuration')
    workflow_data = TextField('Workflow Data', 
                             help='JSON workflow data')
    
    # Template Usage
    usage_count = IntegerField('Usage Count', default=0)
    is_public = BooleanField('Public Template', default=False)
    
    def create_workflow_from_template(self, workflow_name, model_name):
        """Create workflow from template"""
        try:
            # Parse template configuration
            template_config = self._parse_template_config()
            
            # Create workflow
            workflow_data = {
                'name': workflow_name,
                'technical_name': workflow_name.lower().replace(' ', '_'),
                'description': template_config.get('description', ''),
                'workflow_type': template_config.get('workflow_type', 'custom'),
                'model_name': model_name,
                'initial_state': template_config.get('initial_state', 'draft'),
                'final_states': template_config.get('final_states', ''),
                'user_id': self.env.uid,
            }
            
            workflow = self.env['workflow.definition'].create(workflow_data)
            
            # Create workflow components from template
            self._create_workflow_components(workflow.id, template_config)
            
            # Update usage count
            self.write({'usage_count': self.usage_count + 1})
            
            return workflow
            
        except Exception as e:
            raise e
    
    def _parse_template_config(self):
        """Parse template configuration"""
        import json
        try:
            return json.loads(self.template_config) if self.template_config else {}
        except:
            return {}
    
    def _create_workflow_components(self, workflow_id, template_config):
        """Create workflow components from template"""
        # Implementation would create states, transitions, conditions, and actions
        pass