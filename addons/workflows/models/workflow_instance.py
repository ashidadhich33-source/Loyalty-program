#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Instance Model
=========================================

Workflow instance management for workflow execution tracking.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowInstance(BaseModel, KidsClothingMixin):
    """Workflow Instance Model for Workflow Execution Tracking"""
    
    _name = 'workflow.instance'
    _description = 'Workflow Instance'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Instance Name', required=True, size=200)
    workflow_id = Many2OneField('workflow.definition', 'Workflow', required=True)
    record_id = IntegerField('Record ID', required=True,
                            help='ID of the record this workflow applies to')
    model_name = CharField('Model Name', required=True, size=100)
    
    # Instance Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ], 'Status', default='draft')
    
    # Current State
    current_state = CharField('Current State', required=True, size=100)
    previous_state = CharField('Previous State', size=100)
    
    # Execution Tracking
    start_date = DateTimeField('Start Date')
    end_date = DateTimeField('End Date')
    duration = FloatField('Duration (minutes)', digits=(10, 2), default=0.0)
    
    # Transition Tracking
    last_transition = CharField('Last Transition', size=100)
    last_transition_date = DateTimeField('Last Transition Date')
    transition_count = IntegerField('Transition Count', default=0)
    
    # Task Management
    task_ids = One2ManyField('workflow.task', 'instance_id', 'Tasks')
    active_task_count = IntegerField('Active Task Count', default=0)
    completed_task_count = IntegerField('Completed Task Count', default=0)
    
    # Execution Context
    context = TextField('Context', help='Execution context data')
    user_id = Many2OneField('users.user', 'Started By', required=True)
    assigned_user_id = Many2OneField('users.user', 'Assigned To')
    
    # Error Handling
    error_message = TextField('Error Message')
    error_count = IntegerField('Error Count', default=0)
    retry_count = IntegerField('Retry Count', default=0)
    
    # Performance Metrics
    execution_time = FloatField('Execution Time (seconds)', digits=(10, 2), default=0.0)
    memory_usage = FloatField('Memory Usage (MB)', digits=(10, 2), default=0.0)
    
    def start_workflow(self):
        """Start workflow execution"""
        try:
            self.write({
                'status': 'running',
                'start_date': self.env.cr.now(),
            })
            
            # Create initial tasks
            self._create_initial_tasks()
            
            return True
            
        except Exception as e:
            self.write({
                'status': 'failed',
                'error_message': str(e),
                'error_count': self.error_count + 1,
            })
            raise e
    
    def _create_initial_tasks(self):
        """Create initial workflow tasks"""
        initial_actions = self.workflow_id.action_ids.filtered(
            lambda a: a.execute_on == 'on_workflow_start'
        )
        
        for action in initial_actions:
            task_data = {
                'instance_id': self.id,
                'action_id': action.id,
                'name': f"Initial: {action.name}",
                'status': 'pending',
                'user_id': self.user_id.id,
            }
            
            self.env['workflow.task'].create(task_data)
    
    def execute_transition(self, transition_code, context=None):
        """Execute workflow transition"""
        try:
            # Update previous state
            self.write({'previous_state': self.current_state})
            
            # Execute transition
            result = self.workflow_id.execute_transition(self, transition_code, context)
            
            if result:
                # Update transition tracking
                self.write({
                    'transition_count': self.transition_count + 1,
                    'last_transition': transition_code,
                    'last_transition_date': self.env.cr.now(),
                })
                
                # Create tasks for new state
                self._create_state_tasks()
                
                # Update duration
                if self.start_date:
                    duration = (self.env.cr.now() - self.start_date).total_seconds() / 60
                    self.write({'duration': duration})
            
            return result
            
        except Exception as e:
            self.write({
                'status': 'failed',
                'error_message': str(e),
                'error_count': self.error_count + 1,
            })
            raise e
    
    def _create_state_tasks(self):
        """Create tasks for current state"""
        state_actions = self.workflow_id.action_ids.filtered(
            lambda a: a.execute_on == 'on_state_entry' and a.state == self.current_state
        )
        
        for action in state_actions:
            task_data = {
                'instance_id': self.id,
                'action_id': action.id,
                'name': f"State: {action.name}",
                'status': 'pending',
                'user_id': self.user_id.id,
            }
            
            self.env['workflow.task'].create(task_data)
    
    def complete_workflow(self):
        """Complete workflow execution"""
        try:
            self.write({
                'status': 'completed',
                'end_date': self.env.cr.now(),
            })
            
            # Calculate final duration
            if self.start_date and self.end_date:
                duration = (self.end_date - self.start_date).total_seconds() / 60
                self.write({'duration': duration})
            
            # Complete all pending tasks
            pending_tasks = self.task_ids.filtered(lambda t: t.status == 'pending')
            for task in pending_tasks:
                task.write({'status': 'completed'})
            
            return True
            
        except Exception as e:
            self.write({
                'status': 'failed',
                'error_message': str(e),
                'error_count': self.error_count + 1,
            })
            raise e
    
    def cancel_workflow(self, reason=None):
        """Cancel workflow execution"""
        try:
            self.write({
                'status': 'cancelled',
                'end_date': self.env.cr.now(),
                'error_message': reason or 'Workflow cancelled by user',
            })
            
            # Cancel all pending tasks
            pending_tasks = self.task_ids.filtered(lambda t: t.status == 'pending')
            for task in pending_tasks:
                task.write({'status': 'cancelled'})
            
            return True
            
        except Exception as e:
            raise e
    
    def suspend_workflow(self, reason=None):
        """Suspend workflow execution"""
        try:
            self.write({
                'status': 'suspended',
                'error_message': reason or 'Workflow suspended',
            })
            
            # Suspend all pending tasks
            pending_tasks = self.task_ids.filtered(lambda t: t.status == 'pending')
            for task in pending_tasks:
                task.write({'status': 'suspended'})
            
            return True
            
        except Exception as e:
            raise e
    
    def resume_workflow(self):
        """Resume suspended workflow"""
        try:
            self.write({'status': 'running'})
            
            # Resume suspended tasks
            suspended_tasks = self.task_ids.filtered(lambda t: t.status == 'suspended')
            for task in suspended_tasks:
                task.write({'status': 'pending'})
            
            return True
            
        except Exception as e:
            raise e
    
    def retry_workflow(self):
        """Retry failed workflow"""
        try:
            self.write({
                'status': 'running',
                'retry_count': self.retry_count + 1,
                'error_message': '',
            })
            
            # Retry failed tasks
            failed_tasks = self.task_ids.filtered(lambda t: t.status == 'failed')
            for task in failed_tasks:
                task.write({'status': 'pending'})
            
            return True
            
        except Exception as e:
            raise e
    
    def get_available_transitions(self):
        """Get available transitions for current state"""
        return self.workflow_id.get_available_transitions(self.current_state, self.context)
    
    def get_execution_log(self):
        """Get workflow execution log"""
        log_entries = []
        
        # Add workflow start
        if self.start_date:
            log_entries.append({
                'timestamp': self.start_date,
                'event': 'workflow_started',
                'message': f"Workflow {self.workflow_id.name} started",
                'user': self.user_id.name,
            })
        
        # Add transitions
        transitions = self.env['workflow.transition.log'].search([
            ('instance_id', '=', self.id)
        ], order='create_date')
        
        for transition in transitions:
            log_entries.append({
                'timestamp': transition.create_date,
                'event': 'transition_executed',
                'message': f"Transition {transition.transition_code} executed",
                'user': transition.user_id.name,
            })
        
        # Add workflow completion
        if self.end_date:
            log_entries.append({
                'timestamp': self.end_date,
                'event': 'workflow_completed',
                'message': f"Workflow {self.workflow_id.name} completed",
                'user': self.user_id.name,
            })
        
        return sorted(log_entries, key=lambda x: x['timestamp'])
    
    def get_instance_summary(self):
        """Get instance summary"""
        return {
            'id': self.id,
            'name': self.name,
            'workflow_name': self.workflow_id.name,
            'model_name': self.model_name,
            'record_id': self.record_id,
            'status': self.status,
            'current_state': self.current_state,
            'duration': self.duration,
            'transition_count': self.transition_count,
            'task_count': len(self.task_ids),
            'active_task_count': self.active_task_count,
            'completed_task_count': self.completed_task_count,
        }


class WorkflowTransitionLog(BaseModel, KidsClothingMixin):
    """Workflow Transition Log for Audit Trail"""
    
    _name = 'workflow.transition.log'
    _description = 'Workflow Transition Log'
    
    instance_id = Many2OneField('workflow.instance', 'Instance', required=True)
    transition_code = CharField('Transition Code', required=True, size=100)
    from_state = CharField('From State', required=True, size=100)
    to_state = CharField('To State', required=True, size=100)
    user_id = Many2OneField('users.user', 'Executed By', required=True)
    context = TextField('Context')
    execution_time = FloatField('Execution Time (seconds)', digits=(10, 2))