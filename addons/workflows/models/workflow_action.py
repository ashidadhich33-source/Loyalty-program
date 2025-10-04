#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflow Action Model
=========================================

Workflow action management for automated actions.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WorkflowAction(BaseModel, KidsClothingMixin):
    """Workflow Action Model for Automated Actions"""
    
    _name = 'workflow.action'
    _description = 'Workflow Action'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Action Name', required=True, size=200)
    code = CharField('Action Code', required=True, size=100)
    description = TextField('Description')
    workflow_id = Many2OneField('workflow.definition', 'Workflow')
    transition_id = Many2OneField('workflow.transition', 'Transition')
    
    # Action Configuration
    action_type = SelectionField([
        ('method', 'Method Call'),
        ('email', 'Send Email'),
        ('notification', 'Send Notification'),
        ('webhook', 'Webhook Call'),
        ('script', 'Python Script'),
        ('workflow', 'Sub Workflow'),
        ('field_update', 'Field Update'),
        ('record_create', 'Create Record'),
        ('record_delete', 'Delete Record'),
        ('custom', 'Custom Action'),
    ], 'Action Type', required=True)
    
    # Action Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_required = BooleanField('Required', default=True)
    
    # Execution Settings
    execute_on = SelectionField([
        ('on_workflow_start', 'On Workflow Start'),
        ('on_workflow_complete', 'On Workflow Complete'),
        ('on_state_entry', 'On State Entry'),
        ('on_state_exit', 'On State Exit'),
        ('before_transition', 'Before Transition'),
        ('after_transition', 'After Transition'),
        ('on_task_complete', 'On Task Complete'),
        ('on_task_fail', 'On Task Fail'),
    ], 'Execute On', default='after_transition')
    
    # Method-based Actions
    method_name = CharField('Method Name', size=100)
    method_args = TextField('Method Arguments', 
                           help='JSON arguments for method call')
    
    # Email Actions
    email_template = CharField('Email Template', size=100)
    email_recipients = TextField('Email Recipients', 
                                 help='Comma-separated list of recipients')
    email_subject = CharField('Email Subject', size=200)
    email_body = TextField('Email Body')
    
    # Notification Actions
    notification_type = SelectionField([
        ('in_app', 'In-App Notification'),
        ('push', 'Push Notification'),
        ('sms', 'SMS Notification'),
        ('whatsapp', 'WhatsApp Notification'),
    ], 'Notification Type', default='in_app')
    notification_message = TextField('Notification Message')
    notification_recipients = TextField('Notification Recipients', 
                                       help='Comma-separated list of recipients')
    
    # Webhook Actions
    webhook_url = CharField('Webhook URL', size=500)
    webhook_method = SelectionField([
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ], 'Webhook Method', default='POST')
    webhook_headers = TextField('Webhook Headers', 
                                help='JSON headers for webhook')
    webhook_data = TextField('Webhook Data', 
                             help='JSON data for webhook')
    
    # Script Actions
    script_content = TextField('Script Content', 
                              help='Python script to execute')
    script_timeout = IntegerField('Script Timeout (seconds)', default=30)
    
    # Sub Workflow Actions
    sub_workflow_id = Many2OneField('workflow.definition', 'Sub Workflow')
    sub_workflow_context = TextField('Sub Workflow Context', 
                                     help='JSON context for sub workflow')
    
    # Field Update Actions
    field_name = CharField('Field Name', size=100)
    field_value = TextField('Field Value')
    field_value_type = SelectionField([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('json', 'JSON'),
    ], 'Field Value Type', default='string')
    
    # Record Actions
    target_model = CharField('Target Model', size=100)
    record_domain = TextField('Record Domain', 
                             help='Domain to select records')
    record_data = TextField('Record Data', 
                           help='JSON data for record creation')
    
    # Action Conditions
    condition_ids = One2ManyField('workflow.condition', 'action_id', 'Conditions')
    execution_condition = TextField('Execution Condition', 
                                    help='Condition for action execution')
    
    # Action Statistics
    execution_count = IntegerField('Execution Count', default=0)
    success_count = IntegerField('Success Count', default=0)
    failure_count = IntegerField('Failure Count', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    average_execution_time = FloatField('Average Execution Time (seconds)', digits=(10, 2), default=0.0)
    
    # Error Handling
    error_handling = SelectionField([
        ('ignore', 'Ignore Errors'),
        ('retry', 'Retry on Error'),
        ('fail', 'Fail on Error'),
        ('notify', 'Notify on Error'),
    ], 'Error Handling', default='ignore')
    max_retries = IntegerField('Max Retries', default=3)
    retry_interval = IntegerField('Retry Interval (seconds)', default=5)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'action_group_ids', 'Access Groups')
    
    def execute_action(self, instance, context=None):
        """Execute workflow action"""
        try:
            # Check execution conditions
            if not self._check_execution_conditions(instance, context):
                return True
            
            # Execute action based on type
            if self.action_type == 'method':
                result = self._execute_method_action(instance, context)
            elif self.action_type == 'email':
                result = self._execute_email_action(instance, context)
            elif self.action_type == 'notification':
                result = self._execute_notification_action(instance, context)
            elif self.action_type == 'webhook':
                result = self._execute_webhook_action(instance, context)
            elif self.action_type == 'script':
                result = self._execute_script_action(instance, context)
            elif self.action_type == 'workflow':
                result = self._execute_workflow_action(instance, context)
            elif self.action_type == 'field_update':
                result = self._execute_field_update_action(instance, context)
            elif self.action_type == 'record_create':
                result = self._execute_record_create_action(instance, context)
            elif self.action_type == 'record_delete':
                result = self._execute_record_delete_action(instance, context)
            elif self.action_type == 'custom':
                result = self._execute_custom_action(instance, context)
            else:
                result = True
            
            # Update statistics
            self.write({
                'execution_count': self.execution_count + 1,
                'success_count': self.success_count + 1,
                'success_rate': self._calculate_success_rate(),
            })
            
            return result
            
        except Exception as e:
            # Update failure statistics
            self.write({
                'execution_count': self.execution_count + 1,
                'failure_count': self.failure_count + 1,
                'success_rate': self._calculate_success_rate(),
            })
            
            # Handle error based on error handling setting
            if self.error_handling == 'fail':
                raise e
            elif self.error_handling == 'retry':
                self._retry_action(instance, context)
            elif self.error_handling == 'notify':
                self._notify_error(e)
            
            return False
    
    def _check_execution_conditions(self, instance, context):
        """Check action execution conditions"""
        for condition in self.condition_ids:
            if not condition.evaluate_condition(instance, context):
                return False
        
        # Check execution condition
        if self.execution_condition:
            # Implementation would evaluate execution condition
            pass
        
        return True
    
    def _execute_method_action(self, instance, context):
        """Execute method-based action"""
        try:
            if not self.method_name:
                return True
            
            # Get record
            record = self.env[instance.model_name].browse(instance.record_id)
            
            # Parse method arguments
            method_args = self._parse_json(self.method_args) if self.method_args else {}
            
            # Call method
            method = getattr(record, self.method_name, None)
            if method and callable(method):
                method(**method_args)
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_email_action(self, instance, context):
        """Execute email action"""
        try:
            if not self.email_template and not self.email_subject:
                return True
            
            # Get email recipients
            recipients = self._parse_email_recipients(self.email_recipients)
            
            # Send email
            # Implementation would send email using email template or direct content
            pass
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_notification_action(self, instance, context):
        """Execute notification action"""
        try:
            if not self.notification_message:
                return True
            
            # Get notification recipients
            recipients = self._parse_notification_recipients(self.notification_recipients)
            
            # Send notification
            # Implementation would send notification based on type
            pass
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_webhook_action(self, instance, context):
        """Execute webhook action"""
        try:
            if not self.webhook_url:
                return True
            
            import requests
            import json
            
            # Prepare webhook data
            webhook_data = self._prepare_webhook_data(instance, context)
            
            # Prepare headers
            headers = self._parse_json(self.webhook_headers) if self.webhook_headers else {}
            headers['Content-Type'] = 'application/json'
            
            # Make webhook request
            response = requests.request(
                method=self.webhook_method,
                url=self.webhook_url,
                data=json.dumps(webhook_data),
                headers=headers,
                timeout=30
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Webhook failed with status {response.status_code}")
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_script_action(self, instance, context):
        """Execute script action"""
        try:
            if not self.script_content:
                return True
            
            # Execute script safely
            # Implementation would execute script with proper security measures
            pass
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_workflow_action(self, instance, context):
        """Execute sub-workflow action"""
        try:
            if not self.sub_workflow_id:
                return True
            
            # Create sub-workflow instance
            sub_context = self._parse_json(self.sub_workflow_context) if self.sub_workflow_context else {}
            sub_context.update(context or {})
            
            sub_instance = self.sub_workflow_id.create_instance(instance.record_id, sub_context)
            sub_instance.start_workflow()
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_field_update_action(self, instance, context):
        """Execute field update action"""
        try:
            if not self.field_name:
                return True
            
            # Get record
            record = self.env[instance.model_name].browse(instance.record_id)
            
            # Parse field value
            field_value = self._parse_field_value(self.field_value, self.field_value_type)
            
            # Update field
            record.write({self.field_name: field_value})
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_record_create_action(self, instance, context):
        """Execute record creation action"""
        try:
            if not self.target_model:
                return True
            
            # Parse record data
            record_data = self._parse_json(self.record_data) if self.record_data else {}
            
            # Create record
            self.env[self.target_model].create(record_data)
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_record_delete_action(self, instance, context):
        """Execute record deletion action"""
        try:
            if not self.target_model:
                return True
            
            # Parse domain
            domain = self._parse_json(self.record_domain) if self.record_domain else []
            
            # Find and delete records
            records = self.env[self.target_model].search(domain)
            records.unlink()
            
            return True
            
        except Exception as e:
            raise e
    
    def _execute_custom_action(self, instance, context):
        """Execute custom action"""
        try:
            # Implementation would execute custom action
            pass
            
            return True
            
        except Exception as e:
            raise e
    
    def _parse_json(self, json_str):
        """Parse JSON string"""
        import json
        try:
            return json.loads(json_str) if json_str else {}
        except:
            return {}
    
    def _parse_email_recipients(self, recipients_str):
        """Parse email recipients"""
        if not recipients_str:
            return []
        
        return [email.strip() for email in recipients_str.split(',') if email.strip()]
    
    def _parse_notification_recipients(self, recipients_str):
        """Parse notification recipients"""
        if not recipients_str:
            return []
        
        return [recipient.strip() for recipient in recipients_str.split(',') if recipient.strip()]
    
    def _prepare_webhook_data(self, instance, context):
        """Prepare webhook data"""
        webhook_data = self._parse_json(self.webhook_data) if self.webhook_data else {}
        
        # Add instance data
        webhook_data.update({
            'instance_id': instance.id,
            'workflow_name': instance.workflow_id.name,
            'model_name': instance.model_name,
            'record_id': instance.record_id,
            'current_state': instance.current_state,
            'context': context or {},
        })
        
        return webhook_data
    
    def _parse_field_value(self, value_str, value_type):
        """Parse field value based on type"""
        try:
            if value_type == 'string':
                return str(value_str)
            elif value_type == 'integer':
                return int(value_str)
            elif value_type == 'float':
                return float(value_str)
            elif value_type == 'boolean':
                return value_str.lower() in ['true', '1', 'yes', 'on']
            elif value_type == 'date':
                from datetime import datetime
                return datetime.strptime(value_str, '%Y-%m-%d').date()
            elif value_type == 'datetime':
                from datetime import datetime
                return datetime.strptime(value_str, '%Y-%m-%d %H:%M:%S')
            elif value_type == 'json':
                return self._parse_json(value_str)
            else:
                return value_str
        except Exception as e:
            return value_str
    
    def _retry_action(self, instance, context):
        """Retry action execution"""
        # Implementation would retry action with delay
        pass
    
    def _notify_error(self, error):
        """Notify about action error"""
        # Implementation would send error notification
        pass
    
    def _calculate_success_rate(self):
        """Calculate success rate"""
        total_executions = self.success_count + self.failure_count
        if total_executions == 0:
            return 0.0
        
        success_rate = (self.success_count / total_executions) * 100
        return round(success_rate, 2)
    
    def get_action_summary(self):
        """Get action summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'action_type': self.action_type,
            'execute_on': self.execute_on,
            'execution_count': self.execution_count,
            'success_rate': self.success_rate,
            'is_required': self.is_required,
        }