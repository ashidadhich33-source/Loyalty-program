# -*- coding: utf-8 -*-
"""
Ocean ERP - Reorder Rule Views
==============================

Views for reorder rule management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class StockReorderRuleTreeView(TreeView):
    """Stock Reorder Rule Tree View"""
    
    _name = 'stock.reorder.rule.tree'
    _model = 'stock.reorder.rule'
    _title = 'Reorder Rules'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Rule Name', 'width': 200},
            {'name': 'product_id', 'label': 'Product', 'width': 150},
            {'name': 'minimum_stock', 'label': 'Min Stock', 'width': 100},
            {'name': 'maximum_stock', 'label': 'Max Stock', 'width': 100},
            {'name': 'reorder_point', 'label': 'Reorder Point', 'width': 100},
            {'name': 'reorder_quantity', 'label': 'Reorder Qty', 'width': 100},
            {'name': 'lead_time', 'label': 'Lead Time', 'width': 100},
            {'name': 'priority', 'label': 'Priority', 'width': 100},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'auto_reorder', 'label': 'Auto Reorder', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'urgent': {'color': 'red'},
            'high': {'color': 'orange'},
            'medium': {'color': 'blue'},
            'low': {'color': 'green'},
        }


class StockReorderRuleFormView(FormView):
    """Stock Reorder Rule Form View"""
    
    _name = 'stock.reorder.rule.form'
    _model = 'stock.reorder.rule'
    _title = 'Reorder Rule'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Rule Name',
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
                'name': 'minimum_stock',
                'label': 'Minimum Stock',
                'type': 'float',
                'required': True,
            },
            {
                'name': 'maximum_stock',
                'label': 'Maximum Stock',
                'type': 'float',
            },
            {
                'name': 'reorder_quantity',
                'label': 'Reorder Quantity',
                'type': 'float',
                'required': True,
            },
            {
                'name': 'reorder_point',
                'label': 'Reorder Point',
                'type': 'float',
                'required': True,
            },
            {
                'name': 'lead_time',
                'label': 'Lead Time (Days)',
                'type': 'integer',
            },
            {
                'name': 'safety_stock',
                'label': 'Safety Stock',
                'type': 'float',
            },
            {
                'name': 'priority',
                'label': 'Priority',
                'type': 'selection',
            },
            {
                'name': 'state',
                'label': 'Status',
                'type': 'selection',
                'readonly': True,
            },
            {
                'name': 'use_eoq',
                'label': 'Use EOQ',
                'type': 'boolean',
            },
            {
                'name': 'annual_demand',
                'label': 'Annual Demand',
                'type': 'float',
            },
            {
                'name': 'ordering_cost',
                'label': 'Ordering Cost',
                'type': 'float',
            },
            {
                'name': 'holding_cost',
                'label': 'Holding Cost',
                'type': 'float',
            },
            {
                'name': 'eoq_quantity',
                'label': 'EOQ Quantity',
                'type': 'float',
                'readonly': True,
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
                'name': 'supplier_id',
                'label': 'Supplier',
                'type': 'many2one',
            },
            {
                'name': 'auto_reorder',
                'label': 'Auto Reorder',
                'type': 'boolean',
            },
            {
                'name': 'last_reorder_date',
                'label': 'Last Reorder Date',
                'type': 'datetime',
                'readonly': True,
            },
            {
                'name': 'next_reorder_date',
                'label': 'Next Reorder Date',
                'type': 'datetime',
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
                'name': 'action_activate',
                'label': 'Activate',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_suspend',
                'label': 'Suspend',
                'type': 'object',
                'class': 'btn-warning',
                'attrs': {'invisible': [('state', '!=', 'active')]},
            },
            {
                'name': 'action_cancel',
                'label': 'Cancel',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '=', 'active')]},
            },
            {
                'name': 'action_reactivate',
                'label': 'Reactivate',
                'type': 'object',
                'class': 'btn-info',
                'attrs': {'invisible': [('state', '!=', 'suspended')]},
            },
            {
                'name': 'calculate_eoq',
                'label': 'Calculate EOQ',
                'type': 'object',
                'class': 'btn-primary',
            },
            {
                'name': 'action_view_alerts',
                'label': 'View Alerts',
                'type': 'object',
                'class': 'btn-info',
            },
            {
                'name': 'action_view_purchase_orders',
                'label': 'View Purchase Orders',
                'type': 'object',
                'class': 'btn-primary',
            },
        ]


class StockReorderRuleSearchView(SearchView):
    """Stock Reorder Rule Search View"""
    
    _name = 'stock.reorder.rule.search'
    _model = 'stock.reorder.rule'
    _title = 'Search Reorder Rules'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Rule Name'},
            {'name': 'product_id', 'label': 'Product'},
            {'name': 'priority', 'label': 'Priority'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'supplier_id', 'label': 'Supplier'},
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
            {'name': 'active', 'label': 'Active', 'domain': [('state', '=', 'active')]},
            {'name': 'suspended', 'label': 'Suspended', 'domain': [('state', '=', 'suspended')]},
            {'name': 'cancelled', 'label': 'Cancelled', 'domain': [('state', '=', 'cancelled')]},
            {'name': 'urgent', 'label': 'Urgent', 'domain': [('priority', '=', 'urgent')]},
            {'name': 'high', 'label': 'High Priority', 'domain': [('priority', '=', 'high')]},
            {'name': 'medium', 'label': 'Medium Priority', 'domain': [('priority', '=', 'medium')]},
            {'name': 'low', 'label': 'Low Priority', 'domain': [('priority', '=', 'low')]},
            {'name': 'auto_reorder', 'label': 'Auto Reorder', 'domain': [('auto_reorder', '=', True)]},
            {'name': 'use_eoq', 'label': 'Use EOQ', 'domain': [('use_eoq', '=', True)]},
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
            {'name': 'state', 'label': 'Status'},
            {'name': 'priority', 'label': 'Priority'},
            {'name': 'product_id', 'label': 'Product'},
            {'name': 'supplier_id', 'label': 'Supplier'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class StockReorderRuleKanbanView(KanbanView):
    """Stock Reorder Rule Kanban View"""
    
    _name = 'stock.reorder.rule.kanban'
    _model = 'stock.reorder.rule'
    _title = 'Reorder Rules'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'state', 'label': 'Status'},
            {'name': 'priority', 'label': 'Priority'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'state',
            'priority',
            'name',
            'product_id',
            'minimum_stock',
            'maximum_stock',
            'reorder_point',
            'reorder_quantity',
            'lead_time',
            'auto_reorder',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class StockReorderRuleActWindow(ActWindow):
    """Stock Reorder Rule Action Window"""
    
    _name = 'action_stock_reorder_rule'
    _model = 'stock.reorder.rule'
    _view_mode = 'tree,form,kanban'
    _title = 'Reorder Rules'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first reorder rule!',
            'message': 'Reorder rules help you maintain optimal inventory levels.',
        }