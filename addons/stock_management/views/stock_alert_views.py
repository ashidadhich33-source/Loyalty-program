# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Alert Views
=============================

Views for stock alert management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class StockAlertTreeView(TreeView):
    """Stock Alert Tree View"""
    
    _name = 'stock.alert.tree'
    _model = 'stock.alert'
    _title = 'Stock Alerts'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Alert Name', 'width': 200},
            {'name': 'product_id', 'label': 'Product', 'width': 150},
            {'name': 'alert_type', 'label': 'Alert Type', 'width': 120},
            {'name': 'priority', 'label': 'Priority', 'width': 100},
            {'name': 'status', 'label': 'Status', 'width': 100},
            {'name': 'current_stock', 'label': 'Current Stock', 'width': 100},
            {'name': 'minimum_stock', 'label': 'Min Stock', 'width': 100},
            {'name': 'reorder_point', 'label': 'Reorder Point', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
            {'name': 'assigned_to', 'label': 'Assigned To', 'width': 120},
            {'name': 'due_date', 'label': 'Due Date', 'width': 120},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'urgent': {'color': 'red'},
            'high': {'color': 'orange'},
            'medium': {'color': 'blue'},
            'low': {'color': 'green'},
        }


class StockAlertFormView(FormView):
    """Stock Alert Form View"""
    
    _name = 'stock.alert.form'
    _model = 'stock.alert'
    _title = 'Stock Alert'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Alert Name',
                'type': 'char',
                'required': True,
            },
            {
                'name': 'product_id',
                'label': 'Product',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'product_template_id',
                'label': 'Product Template',
                'type': 'many2one',
            },
            {
                'name': 'alert_type',
                'label': 'Alert Type',
                'type': 'selection',
                'required': True,
            },
            {
                'name': 'priority',
                'label': 'Priority',
                'type': 'selection',
            },
            {
                'name': 'status',
                'label': 'Status',
                'type': 'selection',
            },
            {
                'name': 'current_stock',
                'label': 'Current Stock',
                'type': 'float',
            },
            {
                'name': 'minimum_stock',
                'label': 'Minimum Stock',
                'type': 'float',
            },
            {
                'name': 'maximum_stock',
                'label': 'Maximum Stock',
                'type': 'float',
            },
            {
                'name': 'reorder_point',
                'label': 'Reorder Point',
                'type': 'float',
            },
            {
                'name': 'reorder_quantity',
                'label': 'Reorder Quantity',
                'type': 'float',
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
                'name': 'message',
                'label': 'Message',
                'type': 'text',
            },
            {
                'name': 'action_required',
                'label': 'Action Required',
                'type': 'char',
            },
            {
                'name': 'assigned_to',
                'label': 'Assigned To',
                'type': 'many2one',
            },
            {
                'name': 'due_date',
                'label': 'Due Date',
                'type': 'datetime',
            },
            {
                'name': 'resolved_date',
                'label': 'Resolved Date',
                'type': 'datetime',
                'readonly': True,
            },
            {
                'name': 'resolved_by',
                'label': 'Resolved By',
                'type': 'many2one',
                'readonly': True,
            },
            {
                'name': 'resolution_notes',
                'label': 'Resolution Notes',
                'type': 'text',
            },
            {
                'name': 'location_id',
                'label': 'Location',
                'type': 'many2one',
            },
            {
                'name': 'warehouse_id',
                'label': 'Warehouse',
                'type': 'many2one',
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
                'name': 'action_resolve',
                'label': 'Resolve',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('status', '=', 'resolved')]},
            },
            {
                'name': 'action_cancel',
                'label': 'Cancel',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('status', 'in', ['resolved', 'cancelled'])]},
            },
            {
                'name': 'action_reactivate',
                'label': 'Reactivate',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('status', '!=', 'cancelled')]},
            },
            {
                'name': 'create_reorder_rule',
                'label': 'Create Reorder Rule',
                'type': 'object',
                'class': 'btn-info',
            },
            {
                'name': 'generate_purchase_order',
                'label': 'Generate Purchase Order',
                'type': 'object',
                'class': 'btn-primary',
            },
        ]


class StockAlertSearchView(SearchView):
    """Stock Alert Search View"""
    
    _name = 'stock.alert.search'
    _model = 'stock.alert'
    _title = 'Search Stock Alerts'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Alert Name'},
            {'name': 'product_id', 'label': 'Product'},
            {'name': 'alert_type', 'label': 'Alert Type'},
            {'name': 'priority', 'label': 'Priority'},
            {'name': 'status', 'label': 'Status'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'assigned_to', 'label': 'Assigned To'},
        ]
    
    def get_filters(self):
        """Get search view filters"""
        return [
            {'name': 'active', 'label': 'Active', 'domain': [('status', '=', 'active')]},
            {'name': 'resolved', 'label': 'Resolved', 'domain': [('status', '=', 'resolved')]},
            {'name': 'cancelled', 'label': 'Cancelled', 'domain': [('status', '=', 'cancelled')]},
            {'name': 'urgent', 'label': 'Urgent', 'domain': [('priority', '=', 'urgent')]},
            {'name': 'high', 'label': 'High Priority', 'domain': [('priority', '=', 'high')]},
            {'name': 'medium', 'label': 'Medium Priority', 'domain': [('priority', '=', 'medium')]},
            {'name': 'low', 'label': 'Low Priority', 'domain': [('priority', '=', 'low')]},
            {'name': 'low_stock', 'label': 'Low Stock', 'domain': [('alert_type', '=', 'low_stock')]},
            {'name': 'out_of_stock', 'label': 'Out of Stock', 'domain': [('alert_type', '=', 'out_of_stock')]},
            {'name': 'overstock', 'label': 'Overstock', 'domain': [('alert_type', '=', 'overstock')]},
            {'name': 'expiry', 'label': 'Expiry Alert', 'domain': [('alert_type', '=', 'expiry')]},
            {'name': 'seasonal', 'label': 'Seasonal Alert', 'domain': [('alert_type', '=', 'seasonal')]},
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
            {'name': 'alert_type', 'label': 'Alert Type'},
            {'name': 'priority', 'label': 'Priority'},
            {'name': 'status', 'label': 'Status'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'assigned_to', 'label': 'Assigned To'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class StockAlertKanbanView(KanbanView):
    """Stock Alert Kanban View"""
    
    _name = 'stock.alert.kanban'
    _model = 'stock.alert'
    _title = 'Stock Alerts'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'status', 'label': 'Status'},
            {'name': 'priority', 'label': 'Priority'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'status',
            'priority',
            'name',
            'product_id',
            'alert_type',
            'current_stock',
            'minimum_stock',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
            'assigned_to',
            'due_date',
        ]


class StockAlertActWindow(ActWindow):
    """Stock Alert Action Window"""
    
    _name = 'action_stock_alert'
    _model = 'stock.alert'
    _view_mode = 'tree,form,kanban'
    _title = 'Stock Alerts'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first stock alert!',
            'message': 'Stock alerts help you manage inventory levels and prevent stockouts.',
        }