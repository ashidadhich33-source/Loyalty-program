# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Journal Views
==================================

Views for account journal management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class AccountJournalTreeView(TreeView):
    """Account Journal Tree View"""
    
    _name = 'account.journal.tree'
    _model = 'account.journal'
    _title = 'Journals'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Journal Name', 'width': 200},
            {'name': 'code', 'label': 'Code', 'width': 100},
            {'name': 'type', 'label': 'Type', 'width': 100},
            {'name': 'sequence', 'label': 'Sequence', 'width': 100},
            {'name': 'currency_id', 'label': 'Currency', 'width': 100},
            {'name': 'show_on_dashboard', 'label': 'Show on Dashboard', 'width': 120},
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
            'sale': {'color': 'green'},
            'purchase': {'color': 'blue'},
            'cash': {'color': 'orange'},
            'bank': {'color': 'purple'},
            'general': {'color': 'gray'},
        }


class AccountJournalFormView(FormView):
    """Account Journal Form View"""
    
    _name = 'account.journal.form'
    _model = 'account.journal'
    _title = 'Journal'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Journal Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'code',
                'label': 'Journal Code',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'type',
                'label': 'Journal Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
            },
            {
                'name': 'currency_id',
                'label': 'Currency',
                'type': 'many2one',
            },
            {
                'name': 'show_on_dashboard',
                'label': 'Show on Dashboard',
                'type': 'boolean',
            },
            {
                'name': 'restrict_mode_hash_table',
                'label': 'Restrict Mode Hash Table',
                'type': 'boolean',
            },
            {
                'name': 'sequence_id',
                'label': 'Entry Sequence',
                'type': 'many2one',
            },
            {
                'name': 'refund_sequence_id',
                'label': 'Refund Entry Sequence',
                'type': 'many2one',
            },
            {
                'name': 'default_account_id',
                'label': 'Default Account',
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
                'name': 'payment_debit_account_id',
                'label': 'Payment Debit Account',
                'type': 'many2one',
            },
            {
                'name': 'payment_credit_account_id',
                'label': 'Payment Credit Account',
                'type': 'many2one',
            },
            {
                'name': 'invoice_reference_type',
                'label': 'Invoice Reference Type',
                'type': 'selection',
            },
            {
                'name': 'alias_id',
                'label': 'Alias',
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
                'name': 'action_create_journal_entry',
                'label': 'Create Journal Entry',
                'type': 'object',
                'class': 'btn-primary',
            },
            {
                'name': 'action_view_journal_entries',
                'label': 'View Journal Entries',
                'type': 'object',
                'class': 'btn-info',
            },
        ]


class AccountJournalSearchView(SearchView):
    """Account Journal Search View"""
    
    _name = 'account.journal.search'
    _model = 'account.journal'
    _title = 'Search Journals'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Journal Name'},
            {'name': 'code', 'label': 'Code'},
            {'name': 'type', 'label': 'Type'},
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
            {'name': 'sale', 'label': 'Sales', 'domain': [('type', '=', 'sale')]},
            {'name': 'purchase', 'label': 'Purchase', 'domain': [('type', '=', 'purchase')]},
            {'name': 'cash', 'label': 'Cash', 'domain': [('type', '=', 'cash')]},
            {'name': 'bank', 'label': 'Bank', 'domain': [('type', '=', 'bank')]},
            {'name': 'general', 'label': 'General', 'domain': [('type', '=', 'general')]},
            {'name': 'dashboard', 'label': 'Show on Dashboard', 'domain': [('show_on_dashboard', '=', True)]},
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
            {'name': 'type', 'label': 'Journal Type'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class AccountJournalKanbanView(KanbanView):
    """Account Journal Kanban View"""
    
    _name = 'account.journal.kanban'
    _model = 'account.journal'
    _title = 'Journals'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'type', 'label': 'Journal Type'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'type',
            'name',
            'code',
            'sequence',
            'currency_id',
            'show_on_dashboard',
            'active',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class AccountJournalActWindow(ActWindow):
    """Account Journal Action Window"""
    
    _name = 'action_account_journal'
    _model = 'account.journal'
    _view_mode = 'tree,form,kanban'
    _title = 'Journals'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first journal!',
            'message': 'Journals are used to record financial transactions.',
        }


class AccountJournalTemplateTreeView(TreeView):
    """Account Journal Template Tree View"""
    
    _name = 'account.journal.template.tree'
    _model = 'account.journal.template'
    _title = 'Journal Templates'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Template Name', 'width': 200},
            {'name': 'type', 'label': 'Type', 'width': 100},
            {'name': 'sequence', 'label': 'Sequence', 'width': 100},
            {'name': 'active', 'label': 'Active', 'width': 80},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'sale': {'color': 'green'},
            'purchase': {'color': 'blue'},
            'cash': {'color': 'orange'},
            'bank': {'color': 'purple'},
            'general': {'color': 'gray'},
        }


class AccountJournalTemplateFormView(FormView):
    """Account Journal Template Form View"""
    
    _name = 'account.journal.template.form'
    _model = 'account.journal.template'
    _title = 'Journal Template'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Template Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'type',
                'label': 'Journal Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
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
                'name': 'create_journal_from_template',
                'label': 'Create Journal from Template',
                'type': 'object',
                'class': 'btn-primary',
            },
        ]


class AccountJournalTemplateActWindow(ActWindow):
    """Account Journal Template Action Window"""
    
    _name = 'action_account_journal_template'
    _model = 'account.journal.template'
    _view_mode = 'tree,form'
    _title = 'Journal Templates'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first journal template!',
            'message': 'Journal templates help you create journals quickly.',
        }