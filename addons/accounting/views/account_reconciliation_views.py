# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Reconciliation Views
=========================================

Views for account reconciliation management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class AccountReconciliationTreeView(TreeView):
    """Account Reconciliation Tree View"""
    
    _name = 'account.reconciliation.tree'
    _model = 'account.reconciliation'
    _title = 'Account Reconciliations'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Reconciliation Name', 'width': 200},
            {'name': 'date', 'label': 'Date', 'width': 100},
            {'name': 'account_id', 'label': 'Account', 'width': 150},
            {'name': 'reconciliation_type', 'label': 'Type', 'width': 120},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'total_amount', 'label': 'Total Amount', 'width': 120},
            {'name': 'reconciled_amount', 'label': 'Reconciled', 'width': 120},
            {'name': 'unreconciled_amount', 'label': 'Unreconciled', 'width': 120},
            {'name': 'partner_id', 'label': 'Partner', 'width': 150},
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
            'in_progress': {'color': 'blue'},
            'completed': {'color': 'green'},
            'cancelled': {'color': 'red'},
        }


class AccountReconciliationFormView(FormView):
    """Account Reconciliation Form View"""
    
    _name = 'account.reconciliation.form'
    _model = 'account.reconciliation'
    _title = 'Account Reconciliation'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Reconciliation Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'date',
                'label': 'Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'account_id',
                'label': 'Account',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'reconciliation_type',
                'label': 'Reconciliation Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'state',
                'label': 'Status',
                'type': 'selection',
                'readonly': True,
            },
            {
                'name': 'total_amount',
                'label': 'Total Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'reconciled_amount',
                'label': 'Reconciled Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'unreconciled_amount',
                'label': 'Unreconciled Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'partner_id',
                'label': 'Partner',
                'type': 'many2one',
            },
            {
                'name': 'bank_id',
                'label': 'Bank',
                'type': 'many2one',
            },
            {
                'name': 'bank_account_id',
                'label': 'Bank Account',
                'type': 'many2one',
            },
            {
                'name': 'notes',
                'label': 'Notes',
                'type': 'text',
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
            {
                'name': 'currency_id',
                'label': 'Currency',
                'type': 'many2one',
            },
        ]
    
    def get_buttons(self):
        """Get form view buttons"""
        return [
            {
                'name': 'action_start',
                'label': 'Start',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_complete',
                'label': 'Complete',
                'type': 'object',
                'class': 'btn-primary',
                'attrs': {'invisible': [('state', '!=', 'in_progress')]},
            },
            {
                'name': 'action_cancel',
                'label': 'Cancel',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '=', 'completed')]},
            },
            {
                'name': 'action_reopen',
                'label': 'Reopen',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('state', '!=', 'completed')]},
            },
            {
                'name': 'action_view_lines',
                'label': 'View Lines',
                'type': 'object',
                'class': 'btn-info',
            },
        ]


class AccountReconciliationSearchView(SearchView):
    """Account Reconciliation Search View"""
    
    _name = 'account.reconciliation.search'
    _model = 'account.reconciliation'
    _title = 'Search Account Reconciliations'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Reconciliation Name'},
            {'name': 'account_id', 'label': 'Account'},
            {'name': 'reconciliation_type', 'label': 'Type'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'partner_id', 'label': 'Partner'},
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
            {'name': 'in_progress', 'label': 'In Progress', 'domain': [('state', '=', 'in_progress')]},
            {'name': 'completed', 'label': 'Completed', 'domain': [('state', '=', 'completed')]},
            {'name': 'cancelled', 'label': 'Cancelled', 'domain': [('state', '=', 'cancelled')]},
            {'name': 'bank', 'label': 'Bank Reconciliation', 'domain': [('reconciliation_type', '=', 'bank')]},
            {'name': 'customer', 'label': 'Customer Reconciliation', 'domain': [('reconciliation_type', '=', 'customer')]},
            {'name': 'supplier', 'label': 'Supplier Reconciliation', 'domain': [('reconciliation_type', '=', 'supplier')]},
            {'name': 'inventory', 'label': 'Inventory Reconciliation', 'domain': [('reconciliation_type', '=', 'inventory')]},
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
            {'name': 'reconciliation_type', 'label': 'Reconciliation Type'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'account_id', 'label': 'Account'},
            {'name': 'partner_id', 'label': 'Partner'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class AccountReconciliationKanbanView(KanbanView):
    """Account Reconciliation Kanban View"""
    
    _name = 'account.reconciliation.kanban'
    _model = 'account.reconciliation'
    _title = 'Account Reconciliations'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'state', 'label': 'Status'},
            {'name': 'reconciliation_type', 'label': 'Reconciliation Type'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'state',
            'reconciliation_type',
            'name',
            'date',
            'account_id',
            'total_amount',
            'reconciled_amount',
            'unreconciled_amount',
            'partner_id',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class AccountReconciliationActWindow(ActWindow):
    """Account Reconciliation Action Window"""
    
    _name = 'action_account_reconciliation'
    _model = 'account.reconciliation'
    _view_mode = 'tree,form,kanban'
    _title = 'Account Reconciliations'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first account reconciliation!',
            'message': 'Account reconciliations help you match transactions.',
        }


class AccountReconciliationLineTreeView(TreeView):
    """Account Reconciliation Line Tree View"""
    
    _name = 'account.reconciliation.line.tree'
    _model = 'account.reconciliation.line'
    _title = 'Reconciliation Lines'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'reconciliation_id', 'label': 'Reconciliation', 'width': 150},
            {'name': 'move_line_id', 'label': 'Move Line', 'width': 150},
            {'name': 'name', 'label': 'Description', 'width': 200},
            {'name': 'date', 'label': 'Date', 'width': 100},
            {'name': 'amount', 'label': 'Amount', 'width': 100},
            {'name': 'reconciled', 'label': 'Reconciled', 'width': 100},
            {'name': 'partner_id', 'label': 'Partner', 'width': 150},
            {'name': 'ref', 'label': 'Reference', 'width': 120},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'reconciled': {'color': 'green'},
            'unreconciled': {'color': 'red'},
        }


class AccountReconciliationLineFormView(FormView):
    """Account Reconciliation Line Form View"""
    
    _name = 'account.reconciliation.line.form'
    _model = 'account.reconciliation.line'
    _title = 'Reconciliation Line'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'reconciliation_id',
                'label': 'Reconciliation',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
            },
            {
                'name': 'move_line_id',
                'label': 'Move Line',
                'type': 'many2one',
            },
            {
                'name': 'name',
                'label': 'Description',
                'type': 'char',
            },
            {
                'name': 'date',
                'label': 'Date',
                'type': 'datetime',
            },
            {
                'name': 'amount',
                'label': 'Amount',
                'type': 'float',
            },
            {
                'name': 'reconciled',
                'label': 'Reconciled',
                'type': 'boolean',
            },
            {
                'name': 'partner_id',
                'label': 'Partner',
                'type': 'many2one',
            },
            {
                'name': 'ref',
                'label': 'Reference',
                'type': 'char',
            },
            {
                'name': 'currency_id',
                'label': 'Currency',
                'type': 'many2one',
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
                'name': 'action_reconcile',
                'label': 'Reconcile',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('reconciled', '=', True)]},
            },
            {
                'name': 'action_unreconcile',
                'label': 'Unreconcile',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('reconciled', '=', False)]},
            },
        ]


class AccountReconciliationLineActWindow(ActWindow):
    """Account Reconciliation Line Action Window"""
    
    _name = 'action_account_reconciliation_line'
    _model = 'account.reconciliation.line'
    _view_mode = 'tree,form'
    _title = 'Reconciliation Lines'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'View reconciliation lines!',
            'message': 'Reconciliation lines show the details of each transaction.',
        }