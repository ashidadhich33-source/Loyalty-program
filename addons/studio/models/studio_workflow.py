#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Workflow
==================================

Studio workflow management for custom workflow creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioWorkflow(BaseModel, KidsClothingMixin):
    """Studio Workflow for Custom Workflow Creation"""
    
    _name = 'studio.workflow'
    _description = 'Studio Workflow'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Workflow Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    model_id = Many2OneField('studio.model', 'Model', required=True)
    
    # Workflow Configuration
    workflow_type = SelectionField([
        ('approval', 'Approval Workflow'),
        ('sequential', 'Sequential Workflow'),
        ('parallel', 'Parallel Workflow'),
        ('conditional', 'Conditional Workflow'),
        ('custom', 'Custom Workflow'),
    ], 'Workflow Type', default='approval')
    
    # Workflow Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_default = BooleanField('Default Workflow', default=False)
    
    # Workflow States
    initial_state = CharField('Initial State', required=True, size=100, default='draft')
    final_states = TextField('Final States', 
                           help='Comma-separated list of final states')
    
    # Workflow Components
    state_ids = One2ManyField('studio.workflow.state', 'workflow_id', 'States')
    transition_ids = One2ManyField('studio.workflow.transition', 'workflow_id', 'Transitions')
    condition_ids = One2ManyField('studio.workflow.condition', 'workflow_id', 'Conditions')
    action_ids = One2ManyField('studio.workflow.action', 'workflow_id', 'Actions')
    
    # Workflow Execution
    auto_execute = BooleanField('Auto Execute', default=False)
    execution_timeout = IntegerField('Execution Timeout (minutes)', default=60)
    retry_count = IntegerField('Retry Count', default=3)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'workflow_group_ids', 'Access Groups')
    
    def generate_workflow_code(self):
        """Generate Python workflow code"""
        code_lines = []
        
        # Add imports
        code_lines.append("from core_framework.orm import BaseModel, CharField, SelectionField")
        code_lines.append("from addons.core_base.models.base_mixins import KidsClothingMixin")
        code_lines.append("")
        
        # Add workflow class
        code_lines.append(f"class {self._get_class_name()}(BaseModel, KidsClothingMixin):")
        code_lines.append(f'    """{self.description or self.name}"""')
        code_lines.append("")
        code_lines.append(f"    _name = '{self.technical_name}'")
        code_lines.append(f"    _description = '{self.description or self.name}'")
        code_lines.append("")
        
        # Add state field
        states = [(state.code, state.name) for state in self.state_ids]
        code_lines.append(f"    state = SelectionField([{states}], 'State', default='{self.initial_state}')")
        code_lines.append("")
        
        # Add workflow methods
        code_lines.append("    def execute_workflow(self, action_name):")
        code_lines.append("        \"\"\"Execute workflow action\"\"\"")
        code_lines.append("        # Workflow execution logic")
        code_lines.append("        pass")
        code_lines.append("")
        
        code_lines.append("    def get_available_actions(self):")
        code_lines.append("        \"\"\"Get available workflow actions\"\"\"")
        code_lines.append("        # Return available actions based on current state")
        code_lines.append("        return []")
        
        return "\n".join(code_lines)
    
    def _get_class_name(self):
        """Get Python class name from technical name"""
        parts = self.technical_name.split('.')
        return ''.join(word.capitalize() for word in parts)
    
    def deploy_workflow(self):
        """Deploy workflow to system"""
        try:
            # Generate workflow code
            workflow_code = self.generate_workflow_code()
            
            # Create workflow file
            workflow_file_path = f"addons/{self.model_id.project_id.code}/models/{self.technical_name.replace('.', '_')}.py"
            
            # Write workflow file
            with open(workflow_file_path, 'w') as f:
                f.write(workflow_code)
            
            return True
            
        except Exception as e:
            raise e
    
    def get_workflow_summary(self):
        """Get workflow summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'workflow_type': self.workflow_type,
            'model_name': self.model_id.technical_name,
            'state_count': len(self.state_ids),
            'transition_count': len(self.transition_ids),
            'is_default': self.is_default,
        }


class StudioWorkflowState(BaseModel, KidsClothingMixin):
    """Studio Workflow State"""
    
    _name = 'studio.workflow.state'
    _description = 'Studio Workflow State'
    
    workflow_id = Many2OneField('studio.workflow', 'Workflow', required=True)
    name = CharField('State Name', required=True, size=200)
    code = CharField('State Code', required=True, size=100)
    description = TextField('Description')
    sequence = IntegerField('Sequence', default=10)
    is_final = BooleanField('Final State', default=False)
    color = CharField('Color', size=20, default='#000000')


class StudioWorkflowTransition(BaseModel, KidsClothingMixin):
    """Studio Workflow Transition"""
    
    _name = 'studio.workflow.transition'
    _description = 'Studio Workflow Transition'
    
    workflow_id = Many2OneField('studio.workflow', 'Workflow', required=True)
    name = CharField('Transition Name', required=True, size=200)
    code = CharField('Transition Code', required=True, size=100)
    from_state_id = Many2OneField('studio.workflow.state', 'From State', required=True)
    to_state_id = Many2OneField('studio.workflow.state', 'To State', required=True)
    description = TextField('Description')
    sequence = IntegerField('Sequence', default=10)
    required_permission = CharField('Required Permission', size=100)
    condition_ids = One2ManyField('studio.workflow.condition', 'transition_id', 'Conditions')


class StudioWorkflowCondition(BaseModel, KidsClothingMixin):
    """Studio Workflow Condition"""
    
    _name = 'studio.workflow.condition'
    _description = 'Studio Workflow Condition'
    
    workflow_id = Many2OneField('studio.workflow', 'Workflow', required=True)
    transition_id = Many2OneField('studio.workflow.transition', 'Transition')
    name = CharField('Condition Name', required=True, size=200)
    field_name = CharField('Field Name', required=True, size=100)
    operator = SelectionField([
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
    ], 'Operator', required=True)
    value = TextField('Value')
    sequence = IntegerField('Sequence', default=10)


class StudioWorkflowAction(BaseModel, KidsClothingMixin):
    """Studio Workflow Action"""
    
    _name = 'studio.workflow.action'
    _description = 'Studio Workflow Action'
    
    workflow_id = Many2OneField('studio.workflow', 'Workflow', required=True)
    name = CharField('Action Name', required=True, size=200)
    code = CharField('Action Code', required=True, size=100)
    action_type = SelectionField([
        ('method', 'Method Call'),
        ('email', 'Send Email'),
        ('notification', 'Send Notification'),
        ('webhook', 'Webhook Call'),
        ('script', 'Python Script'),
        ('workflow', 'Sub Workflow'),
    ], 'Action Type', required=True)
    method_name = CharField('Method Name', size=100)
    script_content = TextField('Script Content')
    email_template = CharField('Email Template', size=100)
    webhook_url = CharField('Webhook URL', size=500)
    sequence = IntegerField('Sequence', default=10)
    execute_on = SelectionField([
        ('before_transition', 'Before Transition'),
        ('after_transition', 'After Transition'),
        ('on_state_entry', 'On State Entry'),
        ('on_state_exit', 'On State Exit'),
    ], 'Execute On', default='after_transition')