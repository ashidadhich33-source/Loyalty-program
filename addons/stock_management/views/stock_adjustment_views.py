# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Adjustment Views
==================================

Views for stock adjustment management.
"""

from core_framework.ui import View, TreeView, FormView, SearchView, KanbanView
from core_framework.actions import ActWindow


class StockAdjustmentTreeView(TreeView):
    """Stock Adjustment Tree View"""
    
    _name = 'stock.adjustment.tree'
    _model = 'stock.adjustment'
    _title = 'Stock Adjustments'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'name', 'label': 'Adjustment Number', 'width': 150},
            {'name': 'date', 'label': 'Date', 'width': 100},
            {'name': 'adjustment_type', 'label': 'Type', 'width': 120},
            {'name': 'state', 'label': 'Status', 'width': 100},
            {'name': 'location_id', 'label': 'Location', 'width': 120},
            {'name': 'warehouse_id', 'label': 'Warehouse', 'width': 120},
            {'name': 'total_quantity', 'label': 'Total Qty', 'width': 100},
            {'name': 'total_amount', 'label': 'Total Amount', 'width': 120},
            {'name': 'require_approval', 'label': 'Require Approval', 'width': 120},
            {'name': 'approved_by', 'label': 'Approved By', 'width': 120},
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
            'pending_approval': {'color': 'orange'},
            'approved': {'color': 'blue'},
            'done': {'color': 'green'},
            'cancelled': {'color': 'red'},
        }


class StockAdjustmentFormView(FormView):
    """Stock Adjustment Form View"""
    
    _name = 'stock.adjustment.form'
    _model = 'stock.adjustment'
    _title = 'Stock Adjustment'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'name',
                'label': 'Adjustment Number',
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
                'name': 'adjustment_type',
                'label': 'Adjustment Type',
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
                'name': 'location_id',
                'label': 'Location',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'warehouse_id',
                'label': 'Warehouse',
                'type': 'many2one',
            },
            {
                'name': 'require_approval',
                'label': 'Require Approval',
                'type': 'boolean',
            },
            {
                'name': 'approved_by',
                'label': 'Approved By',
                'type': 'many2one',
                'readonly': True,
            },
            {
                'name': 'approved_date',
                'label': 'Approved Date',
                'type': 'datetime',
                'readonly': True,
            },
            {
                'name': 'total_quantity',
                'label': 'Total Quantity',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'total_amount',
                'label': 'Total Amount',
                'type': 'float',
                'readonly': True,
            },
            {
                'name': 'reason',
                'label': 'Reason',
                'type': 'char',
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
        ]
    
    def get_buttons(self):
        """Get form view buttons"""
        return [
            {
                'name': 'action_submit_for_approval',
                'label': 'Submit for Approval',
                'type': 'object',
                'class': 'btn-primary',
                'attrs': {'invisible': [('state', '!=', 'draft')]},
            },
            {
                'name': 'action_approve',
                'label': 'Approve',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'pending_approval')]},
            },
            {
                'name': 'action_done',
                'label': 'Mark as Done',
                'type': 'object',
                'class': 'btn-success',
                'attrs': {'invisible': [('state', '!=', 'approved')]},
            },
            {
                'name': 'action_cancel',
                'label': 'Cancel',
                'type': 'object',
                'class': 'btn-danger',
                'attrs': {'invisible': [('state', '=', 'done')]},
            },
            {
                'name': 'action_view_lines',
                'label': 'View Lines',
                'type': 'object',
                'class': 'btn-info',
            },
        ]


class StockAdjustmentSearchView(SearchView):
    """Stock Adjustment Search View"""
    
    _name = 'stock.adjustment.search'
    _model = 'stock.adjustment'
    _title = 'Search Stock Adjustments'
    
    def get_fields(self):
        """Get search view fields"""
        return [
            {'name': 'name', 'label': 'Adjustment Number'},
            {'name': 'adjustment_type', 'label': 'Type'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'location_id', 'label': 'Location'},
            {'name': 'warehouse_id', 'label': 'Warehouse'},
            {'name': 'approved_by', 'label': 'Approved By'},
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
            {'name': 'pending_approval', 'label': 'Pending Approval', 'domain': [('state', '=', 'pending_approval')]},
            {'name': 'approved', 'label': 'Approved', 'domain': [('state', '=', 'approved')]},
            {'name': 'done', 'label': 'Done', 'domain': [('state', '=', 'done')]},
            {'name': 'cancelled', 'label': 'Cancelled', 'domain': [('state', '=', 'cancelled')]},
            {'name': 'physical_count', 'label': 'Physical Count', 'domain': [('adjustment_type', '=', 'physical_count')]},
            {'name': 'damage', 'label': 'Damage', 'domain': [('adjustment_type', '=', 'damage')]},
            {'name': 'theft', 'label': 'Theft', 'domain': [('adjustment_type', '=', 'theft')]},
            {'name': 'expiry', 'label': 'Expiry', 'domain': [('adjustment_type', '=', 'expiry')]},
            {'name': 'seasonal', 'label': 'Seasonal', 'domain': [('adjustment_type', '=', 'seasonal')]},
            {'name': 'size', 'label': 'Size Adjustment', 'domain': [('adjustment_type', '=', 'size')]},
            {'name': 'brand', 'label': 'Brand Adjustment', 'domain': [('adjustment_type', '=', 'brand')]},
            {'name': 'color', 'label': 'Color Adjustment', 'domain': [('adjustment_type', '=', 'color')]},
            {'name': 'quality_issue', 'label': 'Quality Issue', 'domain': [('adjustment_type', '=', 'quality_issue')]},
            {'name': 'return', 'label': 'Return', 'domain': [('adjustment_type', '=', 'return')]},
            {'name': 'donation', 'label': 'Donation', 'domain': [('adjustment_type', '=', 'donation')]},
            {'name': 'disposal', 'label': 'Disposal', 'domain': [('adjustment_type', '=', 'disposal')]},
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
            {'name': 'adjustment_type', 'label': 'Adjustment Type'},
            {'name': 'state', 'label': 'Status'},
            {'name': 'location_id', 'label': 'Location'},
            {'name': 'warehouse_id', 'label': 'Warehouse'},
            {'name': 'approved_by', 'label': 'Approved By'},
            {'name': 'age_group', 'label': 'Age Group'},
            {'name': 'size', 'label': 'Size'},
            {'name': 'season', 'label': 'Season'},
            {'name': 'brand', 'label': 'Brand'},
            {'name': 'color', 'label': 'Color'},
            {'name': 'company_id', 'label': 'Company'},
        ]


class StockAdjustmentKanbanView(KanbanView):
    """Stock Adjustment Kanban View"""
    
    _name = 'stock.adjustment.kanban'
    _model = 'stock.adjustment'
    _title = 'Stock Adjustments'
    
    def get_kanban_columns(self):
        """Get kanban view columns"""
        return [
            {'name': 'state', 'label': 'Status'},
            {'name': 'adjustment_type', 'label': 'Adjustment Type'},
        ]
    
    def get_kanban_fields(self):
        """Get kanban view fields"""
        return [
            'state',
            'adjustment_type',
            'name',
            'date',
            'location_id',
            'warehouse_id',
            'total_quantity',
            'total_amount',
            'require_approval',
            'approved_by',
            'age_group',
            'size',
            'season',
            'brand',
            'color',
        ]


class StockAdjustmentActWindow(ActWindow):
    """Stock Adjustment Action Window"""
    
    _name = 'action_stock_adjustment'
    _model = 'stock.adjustment'
    _view_mode = 'tree,form,kanban'
    _title = 'Stock Adjustments'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Create your first stock adjustment!',
            'message': 'Stock adjustments help you correct inventory discrepancies.',
        }


class StockAdjustmentLineTreeView(TreeView):
    """Stock Adjustment Line Tree View"""
    
    _name = 'stock.adjustment.line.tree'
    _model = 'stock.adjustment.line'
    _title = 'Adjustment Lines'
    
    def get_columns(self):
        """Get tree view columns"""
        return [
            {'name': 'adjustment_id', 'label': 'Adjustment', 'width': 150},
            {'name': 'product_id', 'label': 'Product', 'width': 150},
            {'name': 'quantity', 'label': 'Quantity', 'width': 100},
            {'name': 'theoretical_quantity', 'label': 'Theoretical Qty', 'width': 120},
            {'name': 'actual_quantity', 'label': 'Actual Qty', 'width': 100},
            {'name': 'unit_cost', 'label': 'Unit Cost', 'width': 100},
            {'name': 'amount', 'label': 'Amount', 'width': 100},
            {'name': 'age_group', 'label': 'Age Group', 'width': 100},
            {'name': 'size', 'label': 'Size', 'width': 80},
            {'name': 'season', 'label': 'Season', 'width': 100},
            {'name': 'brand', 'label': 'Brand', 'width': 100},
            {'name': 'color', 'label': 'Color', 'width': 100},
        ]
    
    def get_decorations(self):
        """Get tree view decorations"""
        return {
            'positive': {'color': 'green'},
            'negative': {'color': 'red'},
        }


class StockAdjustmentLineFormView(FormView):
    """Stock Adjustment Line Form View"""
    
    _name = 'stock.adjustment.line.form'
    _model = 'stock.adjustment.line'
    _title = 'Adjustment Line'
    
    def get_fields(self):
        """Get form view fields"""
        return [
            {
                'name': 'adjustment_id',
                'label': 'Adjustment',
                'type': 'many2one',
                'required': True,
            },
            {
                'name': 'sequence',
                'label': 'Sequence',
                'type': 'integer',
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
                'name': 'quantity',
                'label': 'Quantity',
                'type': 'float',
                'required': True,
            },
            {
                'name': 'theoretical_quantity',
                'label': 'Theoretical Quantity',
                'type': 'float',
            },
            {
                'name': 'actual_quantity',
                'label': 'Actual Quantity',
                'type': 'float',
            },
            {
                'name': 'product_uom_id',
                'label': 'Unit of Measure',
                'type': 'many2one',
            },
            {
                'name': 'unit_cost',
                'label': 'Unit Cost',
                'type': 'float',
            },
            {
                'name': 'amount',
                'label': 'Amount',
                'type': 'float',
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


class StockAdjustmentLineActWindow(ActWindow):
    """Stock Adjustment Line Action Window"""
    
    _name = 'action_stock_adjustment_line'
    _model = 'stock.adjustment.line'
    _view_mode = 'tree,form'
    _title = 'Adjustment Lines'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'View adjustment lines!',
            'message': 'Adjustment lines show the details of each product adjustment.',
        }