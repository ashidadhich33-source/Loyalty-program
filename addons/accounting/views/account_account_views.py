# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Account Views
=================================

Views for account account management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class AccountAccountTreeView(TreeView):
    """Account Account Tree View"""
    
    _name = 'account.account.tree'
    _model = 'account.account'
    _title = 'Chart of Accounts'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'code', 'label': 'Code', 'width': 100},
            {'name': 'name', 'label': 'Account Name', 'width': 200},
            {'name': 'account_type', 'label': 'Type', 'width': 100},
            {'name': 'account_subtype', 'label': 'Subtype', 'width': 120},
            {'name': 'parent_id', 'label': 'Parent', 'width': 150},
            {'name': 'level', 'label': 'Level', 'width': 80},
            {'name': 'full_code', 'label': 'Full Code', 'width': 120},
            {'name': 'balance', 'label': 'Balance', 'width': 100},
            {'name': 'debit', 'label': 'Debit', 'width': 100},
            {'name': 'credit', 'label': 'Credit', 'width': 100},
            {'name': 'reconcile', 'label': 'Reconcile', 'width': 80},
            {'name': 'active', 'label': 'Active', 'width': 80},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'asset': {'color': 'blue'},
            'liability': {'color': 'red'},
            'equity': {'color': 'green'},
            'income': {'color': 'orange'},
            'expense': {'color': 'gray'},
        }


class AccountAccountFormView(FormView):
    """Account Account Form View"""
    
    _name = 'account.account.form'
    _model = 'account.account'
    _title = 'Account'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Account Name',
                'type': 'char',
                'required': True,
                'readonly': True,
            },
            {
                'name': 'code',
                'label': 'Account Code',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'account_type',
                'label': 'Account Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'account_subtype',
                'label': 'Account Subtype',
                'type': 'selection',
            },
            {
                'name': 'parent_id',
                'label': 'Parent Account',
                'type': 'many2one',
            },
            {
                'name': 'level',
                'label': 'Level',
                'type': 'integer',
                'readonly': True,
            },
            {
                'name': 'full_code',
                'label': 'Full Code',
                'type': 'char',
                'readonly': True,
            },
            {
                'name': 'balance',
                'label': 'Balance',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'debit',
                'label': 'Debit',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'credit',
                'label': 'Credit',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'reconcile',
                'label': 'Allow Reconciliation',
                'type': 'boolean',
            },
            {
                'name': 'deprecated',
                'label': 'Deprecated',
                'type': 'boolean',
            },
            {
                'name': 'active',
                'label': 'Active',
                'type': 'boolean',
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
                'name': 'user_type_id',
                'label': 'Account Type',
                'type': 'many2one',
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
                'name': 'action_view_move_lines',
                'label': 'View Move Lines',
                'type': 'object',
                'class': 'btn-primary',
            },
            {
                'name': 'action_reconcile',
                'label': 'Reconcile',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('reconcile', '=', False)]},
            },
            {
                'name': 'action_generate_report',
                'label': 'Generate Report',
                'type': 'object',
                'class': 'btn-info',
            },
        ]


class AccountAccountSearchView(SearchView):
    """Account Account Search View"""
    
    _name = 'account.account.search'
    _model = 'account.account'
    _title = 'Search Accounts'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Name'},
            {'name': 'code', 'label': 'Code'},
            {'name': 'account_type', 'label': 'Account Type'},
            {'name': 'account_subtype', 'label': 'Account Subtype'},
            {'name': 'parent_id', 'label': 'Parent Account'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
        ]
    
    def get_filters(self):
        """Get search view filters"""
        return [
            {'name': 'active', 'label': 'Active', 'domain': [('active', '=', True)]},
            {'name': 'inactive', 'label': 'Inactive', 'domain': [('active', '=', False)]},
            {'name': 'reconcilable', 'label': 'Reconcilable', 'domain': [('reconcile', '=', True)]},
            {'name': 'deprecated', 'label': 'Deprecated', 'domain': [('deprecated', '=', True)]},
            {'name': 'asset', 'label': 'Asset', 'domain': [('account_type', '=', 'asset')]},
            {'name': 'liability', 'label': 'Liability', 'domain': [('account_type', '=', 'liability')]},
            {'name': 'equity', 'label': 'Equity', 'domain': [('account_type', '=', 'equity')]},
            {'name': 'income', 'label': 'Income', 'domain': [('account_type', '=', 'income')]},
            {'name': 'expense', 'label': 'Expense', 'domain': [('account_type', '=', 'expense')]},
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
            {'name': 'account_type', 'label': 'Account Type'},
            {'name': 'account_subtype', 'label': 'Account Subtype'},
            {'name': 'parent_id', 'label': 'Parent Account'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class AccountAccountKanbanView(KanbanView):
    """Account Account Kanban View"""
    
    _name = 'account.account.kanban'
    _model = 'account.account'
    _title = 'Chart of Accounts'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'account_type', 'label': 'Account Type'},
            {'name': 'account_subtype', 'label': 'Account Subtype'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'account_type',
            'account_subtype',
            'code',
            'name',
            'balance',
            'debit',
            'credit',
            'reconcile',
            'active',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class AccountAccountActWindow(ActWindow):
    """Account Account Action Window"""
    
    _name = 'action_account_account'
    _model = 'account.account'
    _view_mode = 'tree,form'
    _title = 'Chart of Accounts'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first account!',
            'message': 'The chart of accounts is the foundation of your accounting system.',
        }


class AccountAccountTypeTreeView(TreeView):
    """Account Account Type Tree View"""
    
    _name = 'account.account.type.tree'
    _model = 'account.account.type'
    _title = 'Account Types'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Name', 'width': 200},
            {'name': 'type', 'label': 'Type', 'width': 100},
            {'name': 'sequence', 'label': 'Sequence', 'width': 100},
            {'name': 'include_initial_balance', 'label': 'Include Initial Balance', 'width': 150},
            {'name': 'reconcile', 'label': 'Allow Reconciliation', 'width': 150},
            {'name': 'active', 'label': 'Active', 'width': 80},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'asset': {'color': 'blue'},
            'liability': {'color': 'red'},
            'equity': {'color': 'green'},
            'income': {'color': 'orange'},
            'expense': {'color': 'gray'},
        }


class AccountAccountTypeFormView(FormView):
    """Account Account Type Form View"""
    
    _name = 'account.account.type.form'
    _model = 'account.account.type'
    _title = 'Account Type'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Name',
                'type': 'char',
                'required': True,
                'readonly': True,
            },
            {
                'name': 'type',
                'label': 'Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
            },
            {
                'name': 'include_initial_balance',
                'label': 'Include Initial Balance',
                'type': 'boolean',
            },
            {
                'name': 'reconcile',
                'label': 'Allow Reconciliation',
                'type': 'boolean',
            },
            {
                'name': 'active',
                'label': 'Active',
                'type': 'boolean',
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


class AccountAccountTypeActWindow(ActWindow):
    """Account Account Type Action Window"""
    
    _name = 'action_account_account_type'
    _model = 'account.account.type'
    _view_mode = 'tree,form'
    _title = 'Account Types'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first account type!',
            'message': 'Account types define the categories for your chart of accounts.',
        }