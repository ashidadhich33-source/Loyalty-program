#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Report Schedule Model
========================================

Report scheduling for automated report generation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    DateTimeField, BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class ReportSchedule(BaseModel, KidsClothingMixin):
    """Report Schedule Model"""
    
    _name = 'report.schedule'
    _description = 'Report Schedule'
    _order = 'next_run_date'
    
    # Basic Information
    name = CharField('Schedule Name', required=True, size=200)
    description = TextField('Description')
    template_id = Many2OneField('report.template', 'Report Template', required=True)
    user_id = Many2OneField('users.user', 'Created By', required=True)
    
    # Schedule Configuration
    frequency = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ], 'Frequency', required=True, default='daily')
    
    interval = IntegerField('Interval', default=1, 
                           help='Run every X days/weeks/months')
    
    # Time Configuration
    run_time = CharField('Run Time', size=10, default='09:00',
                        help='Time to run (HH:MM format)')
    timezone = CharField('Timezone', size=50, default='UTC')
    
    # Day Configuration (for weekly/monthly)
    weekdays = SelectionField([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], 'Weekdays', multiple=True)
    
    month_days = SelectionField([
        ('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th'),
        ('5', '5th'), ('6', '6th'), ('7', '7th'), ('8', '8th'),
        ('9', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th'),
        ('13', '13th'), ('14', '14th'), ('15', '15th'), ('16', '16th'),
        ('17', '17th'), ('18', '18th'), ('19', '19th'), ('20', '20th'),
        ('21', '21st'), ('22', '22nd'), ('23', '23rd'), ('24', '24th'),
        ('25', '25th'), ('26', '26th'), ('27', '27th'), ('28', '28th'),
        ('29', '29th'), ('30', '30th'), ('31', '31st'),
    ], 'Month Days', multiple=True)
    
    # Status and Control
    active = BooleanField('Active', default=True)
    status = SelectionField([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('error', 'Error'),
    ], 'Status', default='draft')
    
    # Execution Tracking
    last_run_date = DateTimeField('Last Run Date')
    next_run_date = DateTimeField('Next Run Date')
    execution_count = IntegerField('Execution Count', default=0)
    success_count = IntegerField('Success Count', default=0)
    error_count = IntegerField('Error Count', default=0)
    
    # Report Configuration
    filters = TextField('Default Filters', help='Default filters for scheduled report')
    output_format = SelectionField([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
        ('json', 'JSON'),
    ], 'Output Format', default='pdf')
    
    # Notification Configuration
    notify_on_success = BooleanField('Notify on Success', default=False)
    notify_on_error = BooleanField('Notify on Error', default=True)
    notify_users = One2ManyField('users.user', 'schedule_notification_ids', 'Notify Users')
    email_notifications = BooleanField('Email Notifications', default=True)
    
    # Execution History
    execution_ids = One2ManyField('report.execution', 'schedule_id', 'Executions')
    
    def calculate_next_run(self):
        """Calculate next run date based on schedule"""
        from datetime import datetime, timedelta
        import calendar
        
        if not self.active:
            return None
        
        now = datetime.now()
        
        if self.frequency == 'daily':
            next_run = now + timedelta(days=self.interval)
        elif self.frequency == 'weekly':
            days_ahead = self.interval * 7
            next_run = now + timedelta(days=days_ahead)
        elif self.frequency == 'monthly':
            # Add months
            month = now.month + self.interval
            year = now.year
            while month > 12:
                month -= 12
                year += 1
            try:
                next_run = now.replace(year=year, month=month)
            except ValueError:
                # Handle month with fewer days
                next_run = now.replace(year=year, month=month, day=1)
                next_run = next_run.replace(day=calendar.monthrange(year, month)[1])
        elif self.frequency == 'quarterly':
            # Add quarters (3 months)
            month = now.month + (self.interval * 3)
            year = now.year
            while month > 12:
                month -= 12
                year += 1
            try:
                next_run = now.replace(year=year, month=month)
            except ValueError:
                next_run = now.replace(year=year, month=month, day=1)
                next_run = next_run.replace(day=calendar.monthrange(year, month)[1])
        elif self.frequency == 'yearly':
            next_run = now.replace(year=now.year + self.interval)
        else:
            # Custom frequency - would need custom logic
            next_run = now + timedelta(days=self.interval)
        
        # Set the time
        hour, minute = map(int, self.run_time.split(':'))
        next_run = next_run.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return next_run
    
    def execute_scheduled_report(self):
        """Execute scheduled report"""
        try:
            # Create execution record
            execution = self.env['report.execution'].create({
                'name': f"Scheduled: {self.name}",
                'template_id': self.template_id.id,
                'user_id': self.user_id.id,
                'filters': self.filters,
                'scheduled_execution': True,
                'schedule_id': self.id,
                'status': 'running',
            })
            
            # Execute the report
            success = execution.execute_report()
            
            # Update schedule statistics
            self.write({
                'last_run_date': execution.create_date,
                'execution_count': self.execution_count + 1,
            })
            
            if success:
                self.write({'success_count': self.success_count + 1})
                if self.notify_on_success:
                    self._send_success_notification(execution)
            else:
                self.write({'error_count': self.error_count + 1})
                if self.notify_on_error:
                    self._send_error_notification(execution)
            
            # Calculate next run
            next_run = self.calculate_next_run()
            if next_run:
                self.write({'next_run_date': next_run})
            
            return execution
            
        except Exception as e:
            self.write({
                'error_count': self.error_count + 1,
                'status': 'error',
            })
            if self.notify_on_error:
                self._send_error_notification(None, str(e))
            raise e
    
    def _send_success_notification(self, execution):
        """Send success notification"""
        # Implementation for success notification
        pass
    
    def _send_error_notification(self, execution, error_message=None):
        """Send error notification"""
        # Implementation for error notification
        pass
    
    def pause_schedule(self):
        """Pause the schedule"""
        self.write({
            'active': False,
            'status': 'paused',
        })
    
    def resume_schedule(self):
        """Resume the schedule"""
        next_run = self.calculate_next_run()
        self.write({
            'active': True,
            'status': 'running',
            'next_run_date': next_run,
        })
    
    def get_schedule_summary(self):
        """Get schedule summary"""
        return {
            'id': self.id,
            'name': self.name,
            'template': self.template_id.name,
            'frequency': self.frequency,
            'status': self.status,
            'active': self.active,
            'last_run': self.last_run_date,
            'next_run': self.next_run_date,
            'execution_count': self.execution_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
        }