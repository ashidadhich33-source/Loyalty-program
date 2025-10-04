# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Period Views
=================================

Views for account period management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class AccountPeriodTreeView(TreeView):
    """Account Period Tree View"""
    
    _name = 'account.period.tree'
    _model = 'account.period'
    _title = 'Accounting Periods'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Period Name', 'width': 200},
            {'name': 'code', 'label': 'Code', 'width': 100},
            {'name': 'date_start', 'label': 'Start Date', 'width': 100},
            {'name': 'date_stop', 'label': 'End Date', 'width': 100},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'fiscalyear_id', 'label': 'Fiscal Year', 'width': 120},
            {'name': 'special', 'label': 'Special', 'width': 80},
            {'name': 'period_type', 'label': 'Period Type', 'width': 120},
            {'name': 'move_count', 'label': 'Move Count', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'draft': {'color': 'gray'},
            'open': {'color': 'green'},
            'closed': {'color': 'red'},
        }


class AccountPeriodFormView(FormView):
    """Account Period Form View"""
    
    _name = 'account.period.form'
    _model = 'account.period'
    _title = 'Accounting Period'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Period Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'code',
                'label': 'Period Code',
                'type': 'char',
            },
            {
                'name': 'date_start',
                'label': 'Start Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'date_stop',
                'label': 'End Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'state',
                'label': 'Status',
                'type': 'selection',
                'readonly': True,
            },
            {
                'name': 'fiscalyear_id',
                'label': 'Fiscal Year',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'special',
                'label': 'Special Period',
                'type': 'boolean',
            },
            {
                'name': 'period_type',
                'label': 'Period Type',
                'type': 'selection',
            },
            {
                'name': 'move_count',
                'label': 'Move Count',
                'type': 'integer',
                'readonly': True,
            },
            {
                'name': 'age_group',
                'label': 'Age Group',
                'type': 'selection',
            },
            {
                'name': 'size',
                'label': 'Size',
                'type': 'selection',
            },
            {
                'name': 'season',
                'label': 'Season',
                'type': 'selection',
            },
            {
                'name': 'brand',
                'label': 'Brand',
                'type': 'char',
            },
            {
                'name': 'color',
                'label': 'Color',
                'type': 'char',
            },
            {
                'name': 'company_id',
                'label': 'Company',
                'type': 'many2one',
            },
        ]
    
    def get_buttons(self):
        """Get form view buttons"""
        return [
            {
                'name': 'action_open',
                'label': 'Open',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_close',
                'label': 'Close',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '!=', 'open')]},
            },
            {
                'name': 'action_reopen',
                'label': 'Reopen',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('state', '!=', 'closed')]},
            },
            {
                'name': 'action_view_moves',
                'label': 'View Moves',
                'type': 'object',
                'class': 'btn-info',
            },
        ]


class AccountPeriodSearchView(SearchView):
    """Account Period Search View"""
    
    _name = 'account.period.search'
    _model = 'account.period'
    _title = 'Search Accounting Periods'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Period Name'},
            {'name': 'code', 'label': 'Code'},
            {'name': 'fiscalyear_id', 'label': 'Fiscal Year'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
        ]
    
    def get_filters(self):
        """Get search view filters"""
        return [
            {'name': 'draft', 'label': 'Draft', 'domain': [('state', '=', 'draft')]},
            {'name': 'open', 'label': 'Open', 'domain': [('state', '=', 'open')]},
            {'name': 'closed', 'label': 'Closed', 'domain': [('state', '=', 'closed')]},
            {'name': 'special', 'label': 'Special Periods', 'domain': [('special', '=', True)]},
            {'name': 'monthly', 'label': 'Monthly', 'domain': [('period_type', '=', 'monthly')]},
            {'name': 'quarterly', 'label': 'Quarterly', 'domain': [('period_type', '=', 'quarterly')]},
            {'name': 'yearly', 'label': 'Yearly', 'domain': [('period_type', '=', 'yearly')]},
            {'name': 'age_0_2', 'label': 'Baby (0-2 years)', 'domain': [('age_group', '=', '0-2')]},
            {'name': 'age_2_4', 'label': 'Toddler (2-4 years)', 'domain': [('age_group', '=', '2-4')]},
            {'name': 'age_4_6', 'label': 'Pre-school (4-6 years)', 'domain': [('age_group', '=', '4-6')]},
            {'name': 'summer', 'label': 'Summer', 'domain': [('season', '=', 'summer')]},
            {'name': 'winter', 'label': 'Winter', 'domain': [('season', '=', 'winter')]},
            {'name': 'monsoon', 'label': 'Monsoon', 'domain': [('season', '=', 'monsoon')]},
        ]
    
    def get_groups(self):
        """Get search view groups"""
        return [
            {'name': 'fiscalyear_id', 'label': 'Fiscal Year'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'period_type', 'label': 'Period Type'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class AccountPeriodKanbanView(KanbanView):
    """Account Period Kanban View"""
    
    _name = 'account.period.kanban'
    _model = 'account.period'
    _title = 'Accounting Periods'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'state', 'label': 'Status'},
            {'name': 'fiscalyear_id', 'label': 'Fiscal Year'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'state',
            'fiscalyear_id',
            'name',
            'code',
            'date_start',
            'date_stop',
            'special',
            'period_type',
            'move_count',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class AccountPeriodActWindow(ActWindow):
    """Account Period Action Window"""
    
    _name = 'action_account_period'
    _model = 'account.period'
    _view_mode = 'tree,form,kanban'
    _title = 'Accounting Periods'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first accounting period!',
            'message': 'Accounting periods help you organize your financial data.',
        }


class AccountFiscalYearTreeView(TreeView):
    """Account Fiscal Year Tree View"""
    
    _name = 'account.fiscal.year.tree'
    _model = 'account.fiscal.year'
    _title = 'Fiscal Years'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Fiscal Year Name', 'width': 200},
            {'name': 'code', 'label': 'Code', 'width': 100},
            {'name': 'date_start', 'label': 'Start Date', 'width': 100},
            {'name': 'date_stop', 'label': 'End Date', 'width': 100},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'period_count', 'label': 'Period Count', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'draft': {'color': 'gray'},
            'open': {'color': 'green'},
            'closed': {'color': 'red'},
        }


class AccountFiscalYearFormView(FormView):
    """Account Fiscal Year Form View"""
    
    _name = 'account.fiscal.year.form'
    _model = 'account.fiscal.year'
    _title = 'Fiscal Year'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Fiscal Year Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'code',
                'label': 'Fiscal Year Code',
                'type': 'char',
            },
            {
                'name': 'date_start',
                'label': 'Start Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'date_stop',
                'label': 'End Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'state',
                'label': 'Status',
                'type': 'selection',
                'readonly': True,
            },
            {
                'name': 'period_count',
                'label': 'Period Count',
                'type': 'integer',
                'readonly': True,
            },
            {
                'name': 'age_group',
                'label': 'Age Group',
                'type': 'selection',
            },
            {
                'name': 'season',
                'label': 'Season',
                'type': 'selection',
            },
            {
                'name': 'brand',
                'label': 'Brand',
                'type': 'char',
            },
            {
                'name': 'color',
                'label': 'Color',
                'type': 'char',
            },
            {
                'name': 'company_id',
                'label': 'Company',
                'type': 'many2one',
            },
        ]
    
    def get_buttons(self):
        """Get form view buttons"""
        return [
            {
                'name': 'action_open',
                'label': 'Open',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_close',
                'label': 'Close',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '!=', 'open')]},
            },
            {
                'name': 'action_reopen',
                'label': 'Reopen',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('state', '!=', 'closed')]},
            },
            {
                'name': 'generate_periods',
                'label': 'Generate Periods',
                'type': 'object',
                'class': 'btn-info',
                'attrs': {'invisible': [('period_count', '>', 0)]},
            },
            {
                'name': 'action_view_periods',
                'label': 'View Periods',
                'type': 'object',
                'class': 'btn-primary',
            },
        ]


class AccountFiscalYearActWindow(ActWindow):
    """Account Fiscal Year Action Window"""
    
    _name = 'action_account_fiscal_year'
    _model = 'account.fiscal.year'
    _view_mode = 'tree,form'
    _title = 'Fiscal Years'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first fiscal year!',
            'message': 'Fiscal years help you organize your accounting periods.',
        }