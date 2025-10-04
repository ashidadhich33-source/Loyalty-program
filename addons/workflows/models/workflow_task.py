#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Task Model
======================================

Workflow task management for task execution and tracking.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowTask(BaseModel, KidsClothingMixin):
    """Workflow Task Model for Task Execution and Tracking"""
    
    _name = 'workflow.task'
    _description = 'Workflow Task'
    _order = 'sequence, create_date'
    
    # Basic Information
    name = CharField('Task Name', required=True, size=200)
    description = TextField('Description')
    instance_id = Many2OneField('workflow.instance', 'Instance', required=True)
    action_id = Many2OneField('workflow.action', 'Action')
    
    # Task Configuration
    task_type = SelectionField([
        ('manual', 'Manual Task'),
        ('automatic', 'Automatic Task'),
        ('approval', 'Approval Task'),
        ('notification', 'Notification Task'),
        ('script', 'Script Task'),
        ('webhook', 'Webhook Task'),
        ('email', 'Email Task'),
        ('custom', 'Custom Task'),
    ], 'Task Type', required=True)
    
    # Task Status
    status = SelectionField([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
        ('skipped', 'Skipped'),
    ], 'Status', default='pending')
    
    # Task Assignment
    assigned_user_id = Many2OneField('users.user', 'Assigned To')
    assigned_group_id = Many2OneField('users.group', 'Assigned Group')
    user_id = Many2OneField('users.user', 'Created By', required=True)
    
    # Task Execution
    start_date = DateTimeField('Start Date')
    end_date = DateTimeField('End Date')
    duration = FloatField('Duration (minutes)', digits=(10, 2), default=0.0)
    execution_time = FloatField('Execution Time (seconds)', digits=(10, 2), default=0.0)
    
    # Task Priority
    priority = SelectionField([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], 'Priority', default='normal')
    
    # Task Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_required = BooleanField('Required', default=True)
    auto_execute = BooleanField('Auto Execute', default=False)
    
    # Task Dependencies
    depends_on_ids = One2ManyField('workflow.task.dependency', 'task_id', 'Dependencies')
    required_tasks = TextField('Required Tasks', 
                              help='Comma-separated list of required task IDs')
    
    # Task Results
    result_data = TextField('Result Data', 
                           help='JSON result data')
    error_message = TextField('Error Message')
    retry_count = IntegerField('Retry Count', default=0)
    max_retries = IntegerField('Max Retries', default=3)
    
    # Task Notifications
    notify_on_start = BooleanField('Notify on Start', default=False)
    notify_on_complete = BooleanField('Notify on Complete', default=False)
    notify_on_failure = BooleanField('Notify on Failure', default=True)
    
    def start_task(self):
        """Start task execution"""
        try:
            # Check dependencies
            if not self._check_dependencies():
                raise Exception("Task dependencies not met")
            
            # Update status
            self.write({
                'status': 'in_progress',
                'start_date': self.env.cr.now(),
            })
            
            # Send start notification
            if self.notify_on_start:
                self._send_notification('task_started')
            
            # Execute task based on type
            if self.task_type == 'automatic':
                self._execute_automatic_task()
            elif self.task_type == 'script':
                self._execute_script_task()
            elif self.task_type == 'webhook':
                self._execute_webhook_task()
            elif self.task_type == 'email':
                self._execute_email_task()
            elif self.task_type == 'notification':
                self._execute_notification_task()
            elif self.task_type == 'manual':
                # Manual tasks require user intervention
                pass
            elif self.task_type == 'approval':
                # Approval tasks require user approval
                pass
            
            return True
            
        except Exception as e:
            self.write({
                'status': 'failed',
                'error_message': str(e),
                'retry_count': self.retry_count + 1,
            })
            
            # Send failure notification
            if self.notify_on_failure:
                self._send_notification('task_failed')
            
            raise e
    
    def _check_dependencies(self):
        """Check task dependencies"""
        for dependency in self.depends_on_ids:
            if dependency.depends_on_task.status != 'completed':
                return False
        return True
    
    def _execute_automatic_task(self):
        """Execute automatic task"""
        if self.action_id:
            self.action_id.execute_action(self.instance_id)
        self.complete_task()
    
    def _execute_script_task(self):
        """Execute script task"""
        if self.action_id and self.action_id.script_content:
            # Execute script content
            # Implementation would execute the script safely
            pass
        self.complete_task()
    
    def _execute_webhook_task(self):
        """Execute webhook task"""
        if self.action_id and self.action_id.webhook_url:
            # Execute webhook call
            # Implementation would make webhook request
            pass
        self.complete_task()
    
    def _execute_email_task(self):
        """Execute email task"""
        if self.action_id and self.action_id.email_template:
            # Send email
            # Implementation would send email
            pass
        self.complete_task()
    
    def _execute_notification_task(self):
        """Execute notification task"""
        if self.action_id:
            # Send notification
            # Implementation would send notification
            pass
        self.complete_task()
    
    def complete_task(self, result_data=None):
        """Complete task execution"""
        try:
            self.write({
                'status': 'completed',
                'end_date': self.env.cr.now(),
                'result_data': str(result_data) if result_data else '',
            })
            
            # Calculate duration
            if self.start_date and self.end_date:
                duration = (self.end_date - self.start_date).total_seconds() / 60
                self.write({'duration': duration})
            
            # Send completion notification
            if self.notify_on_complete:
                self._send_notification('task_completed')
            
            # Trigger dependent tasks
            self._trigger_dependent_tasks()
            
            return True
            
        except Exception as e:
            raise e
    
    def _trigger_dependent_tasks(self):
        """Trigger dependent tasks"""
        dependent_tasks = self.env['workflow.task'].search([
            ('depends_on_ids.depends_on_task', '=', self.id),
            ('status', '=', 'pending')
        ])
        
        for task in dependent_tasks:
            if task._check_dependencies():
                task.start_task()
    
    def fail_task(self, error_message):
        """Fail task execution"""
        try:
            self.write({
                'status': 'failed',
                'error_message': error_message,
                'retry_count': self.retry_count + 1,
            })
            
            # Send failure notification
            if self.notify_on_failure:
                self._send_notification('task_failed')
            
            # Retry if possible
            if self.retry_count < self.max_retries:
                self.retry_task()
            
            return True
            
        except Exception as e:
            raise e
    
    def retry_task(self):
        """Retry failed task"""
        try:
            self.write({
                'status': 'pending',
                'error_message': '',
            })
            
            # Auto-start if configured
            if self.auto_execute:
                self.start_task()
            
            return True
            
        except Exception as e:
            raise e
    
    def cancel_task(self, reason=None):
        """Cancel task execution"""
        try:
            self.write({
                'status': 'cancelled',
                'end_date': self.env.cr.now(),
                'error_message': reason or 'Task cancelled',
            })
            
            return True
            
        except Exception as e:
            raise e
    
    def skip_task(self, reason=None):
        """Skip task execution"""
        try:
            self.write({
                'status': 'skipped',
                'end_date': self.env.cr.now(),
                'error_message': reason or 'Task skipped',
            })
            
            # Trigger dependent tasks
            self._trigger_dependent_tasks()
            
            return True
            
        except Exception as e:
            raise e
    
    def _send_notification(self, notification_type):
        """Send task notification"""
        # Implementation would send notification
        pass
    
    def get_task_summary(self):
        """Get task summary"""
        return {
            'id': self.id,
            'name': self.name,
            'task_type': self.task_type,
            'status': self.status,
            'priority': self.priority,
            'assigned_user': self.assigned_user_id.name if self.assigned_user_id else None,
            'duration': self.duration,
            'retry_count': self.retry_count,
        }


class WorkflowTaskDependency(BaseModel, KidsClothingMixin):
    """Workflow Task Dependency"""
    
    _name = 'workflow.task.dependency'
    _description = 'Workflow Task Dependency'
    
    task_id = Many2OneField('workflow.task', 'Task', required=True)
    depends_on_task = Many2OneField('workflow.task', 'Depends On Task', required=True)
    dependency_type = SelectionField([
        ('required', 'Required'),
        ('optional', 'Optional'),
        ('conflict', 'Conflict'),
    ], 'Dependency Type', default='required')
    description = TextField('Description')