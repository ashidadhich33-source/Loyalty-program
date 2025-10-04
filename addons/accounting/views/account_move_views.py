# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Move Views
==============================

Views for account move management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class AccountMoveTreeView(TreeView):
    """Account Move Tree View"""
    
    _name = 'account.move.tree'
    _model = 'account.move'
    _title = 'Journal Entries'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Entry Number', 'width': 120},
            {'name': 'date', 'label': 'Date', 'width': 100},
            {'name': 'ref', 'label': 'Reference', 'width': 120},
            {'name': 'journal_id', 'label': 'Journal', 'width': 120},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'partner_id', 'label': 'Partner', 'width': 150},
            {'name': 'amount_total', 'label': 'Total Amount', 'width': 120},
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
            'posted': {'color': 'green'},
            'cancel': {'color': 'red'},
        }


class AccountMoveFormView(FormView):
    """Account Move Form View"""
    
    _name = 'account.move.form'
    _model = 'account.move'
    _title = 'Journal Entry'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Entry Number',
                'type': 'char',
                'readonly': True,
            },
            {
                'name': 'date',
                'label': 'Date',
                'type': 'datetime',
                'required': True,
            },
            {
                'name': 'ref',
                'label': 'Reference',
                'type': 'char',
            },
            {
                'name': 'journal_id',
                'label': 'Journal',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'state',
                'label': 'Status',
                'type': 'selection',
                'readonly': True,
            },
            {
                'name': 'partner_id',
                'label': 'Partner',
                'type': 'many2one',
            },
            {
                'name': 'amount_total',
                'label': 'Total Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'amount_untaxed',
                'label': 'Untaxed Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'amount_tax',
                'label': 'Tax Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'narration',
                'label': 'Narration',
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
                'name': 'action_post',
                'label': 'Post',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_cancel',
                'label': 'Cancel',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '=', 'posted')]},
            },
            {
                'name': 'action_draft',
                'label': 'Set to Draft',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('state', '!=', 'cancel')]},
            },
            {
                'name': 'action_reverse',
                'label': 'Reverse',
                'type': 'object',
                'class': 'btn-info',
                'attrs': {'invisible': [('state', '!=', 'posted')]},
            },
        ]


class AccountMoveSearchView(SearchView):
    """Account Move Search View"""
    
    _name = 'account.move.search'
    _model = 'account.move'
    _title = 'Search Journal Entries'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Entry Number'},
            {'name': 'ref', 'label': 'Reference'},
            {'name': 'journal_id', 'label': 'Journal'},
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
            {'name': 'posted', 'label': 'Posted', 'domain': [('state', '=', 'posted')]},
            {'name': 'cancelled', 'label': 'Cancelled', 'domain': [('state', '=', 'cancel')]},
            {'name': 'today', 'label': 'Today', 'domain': [('date', '>=', 'today'), ('date', '<=', 'today')]},
            {'name': 'this_week', 'label': 'This Week', 'domain': [('date', '>=', 'this_week'), ('date', '<=', 'this_week')]},
            {'name': 'this_month', 'label': 'This Month', 'domain': [('date', '>=', 'this_month'), ('date', '<=', 'this_month')]},
            {'name': 'this_year', 'label': 'This Year', 'domain': [('date', '>=', 'this_year'), ('date', '<=', 'this_year')]},
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
            {'name': 'journal_id', 'label': 'Journal'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'partner_id', 'label': 'Partner'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class AccountMoveKanbanView(KanbanView):
    """Account Move Kanban View"""
    
    _name = 'account.move.kanban'
    _model = 'account.move'
    _title = 'Journal Entries'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'state', 'label': 'Status'},
            {'name': 'journal_id', 'label': 'Journal'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'state',
            'journal_id',
            'name',
            'date',
            'ref',
            'partner_id',
            'amount_total',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class AccountMoveActWindow(ActWindow):
    """Account Move Action Window"""
    
    _name = 'action_account_move'
    _model = 'account.move'
    _view_mode = 'tree,form,kanban'
    _title = 'Journal Entries'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first journal entry!',
            'message': 'Journal entries record financial transactions.',
        }


class AccountMoveLineTreeView(TreeView):
    """Account Move Line Tree View"""
    
    _name = 'account.move.line.tree'
    _model = 'account.move.line'
    _title = 'Journal Entry Lines'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'move_id', 'label': 'Journal Entry', 'width': 120},
            {'name': 'account_id', 'label': 'Account', 'width': 150},
            {'name': 'name', 'label': 'Label', 'width': 200},
            {'name': 'debit', 'label': 'Debit', 'width': 100},
            {'name': 'credit', 'label': 'Credit', 'width': 100},
            {'name': 'partner_id', 'label': 'Partner', 'width': 150},
            {'name': 'product_id', 'label': 'Product', 'width': 150},
            {'name': 'quantity', 'label': 'Quantity', 'width': 100},
            {'name': 'price_unit', 'label': 'Unit Price', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'debit': {'color': 'red'},
            'credit': {'color': 'green'},
        }


class AccountMoveLineFormView(FormView):
    """Account Move Line Form View"""
    
    _name = 'account.move.line.form'
    _model = 'account.move.line'
    _title = 'Journal Entry Line'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'move_id',
                'label': 'Journal Entry',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
            },
            {
                'name': 'account_id',
                'label': 'Account',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'name',
                'label': 'Label',
                'type': 'char',
            },
            {
                'name': 'debit',
                'label': 'Debit',
                'type': 'float',
            },
            {
                'name': 'credit',
                'label': 'Credit',
                'type': 'float',
            },
            {
                'name': 'partner_id',
                'label': 'Partner',
                'type': 'many2one',
            },
            {
                'name': 'product_id',
                'label': 'Product',
                'type': 'many2one',
            },
            {
                'name': 'quantity',
                'label': 'Quantity',
                'type': 'float',
            },
            {
                'name': 'price_unit',
                'label': 'Unit Price',
                'type': 'float',
            },
            {
                'name': 'amount_currency',
                'label': 'Amount Currency',
                'type': 'float',
            },
            {
                'name': 'currency_id',
                'label': 'Currency',
                'type': 'many2one',
            },
            {
                'name': 'date',
                'label': 'Date',
                'type': 'datetime',
            },
            {
                'name': 'ref',
                'label': 'Reference',
                'type': 'char',
            },
            {
                'name': 'tax_ids',
                'label': 'Taxes',
                'type': 'many2many',
            },
            {
                'name': 'analytic_account_id',
                'label': 'Analytic Account',
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


class AccountMoveLineActWindow(ActWindow):
    """Account Move Line Action Window"""
    
    _name = 'action_account_move_line'
    _model = 'account.move.line'
    _view_mode = 'tree,form'
    _title = 'Journal Entry Lines'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'View journal entry lines!',
            'message': 'Journal entry lines show the details of each transaction.',
        }