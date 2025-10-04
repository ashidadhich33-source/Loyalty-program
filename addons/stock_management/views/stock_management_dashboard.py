# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Management Dashboard
======================================

Stock management dashboard for kids clothing retail.
"""

from core_framework.ui import View, DashboardView
from core_framework.actions import ActWindow


class StockManagementDashboardView(DashboardView):
    """Stock Management Dashboard View"""
    
    _name = 'stock.management.dashboard'
    _title = 'Stock Management Dashboard'
    
    def get_dashboard_widgets(self):
        """Get dashboard widgets"""
        return [
            {
                'name': 'stock_alerts_widget',
                'title': 'Stock Alerts',
                'type': 'chart',
                'data': self._get_stock_alerts_data(),
                'width': 6,
            },
            {
                'name': 'reorder_rules_widget',
                'title': 'Reorder Rules Status',
                'type': 'chart',
                'data': self._get_reorder_rules_data(),
                'width': 6,
            },
            {
                'name': 'stock_levels_widget',
                'title': 'Stock Levels by Age Group',
                'type': 'chart',
                'data': self._get_stock_levels_data(),
                'width': 12,
            },
            {
                'name': 'seasonal_stock_widget',
                'title': 'Seasonal Stock Analysis',
                'type': 'chart',
                'data': self._get_seasonal_stock_data(),
                'width': 6,
            },
            {
                'name': 'brand_performance_widget',
                'title': 'Brand Performance',
                'type': 'chart',
                'data': self._get_brand_performance_data(),
                'width': 6,
            },
            {
                'name': 'size_distribution_widget',
                'title': 'Size Distribution',
                'type': 'chart',
                'data': self._get_size_distribution_data(),
                'width': 12,
            },
            {
                'name': 'color_trends_widget',
                'title': 'Color Trends',
                'type': 'chart',
                'data': self._get_color_trends_data(),
                'width': 6,
            },
            {
                'name': 'recent_adjustments_widget',
                'title': 'Recent Stock Adjustments',
                'type': 'list',
                'data': self._get_recent_adjustments(),
                'width': 6,
            },
        ]
    
    def _get_stock_alerts_data(self):
        """Get stock alerts data"""
        return {
            'type': 'pie',
            'data': [
                {'name': 'Low Stock', 'value': 15},
                {'name': 'Out of Stock', 'value': 5},
                {'name': 'Overstock', 'value': 8},
                {'name': 'Expiry Alert', 'value': 3},
                {'name': 'Seasonal Alert', 'value': 12},
            ]
        }
    
    def _get_reorder_rules_data(self):
        """Get reorder rules data"""
        return {
            'type': 'bar',
            'data': [
                {'name': 'Active', 'value': 45},
                {'name': 'Suspended', 'value': 8},
                {'name': 'Draft', 'value': 12},
                {'name': 'Cancelled', 'value': 3},
            ]
        }
    
    def _get_stock_levels_data(self):
        """Get stock levels by age group data"""
        return {
            'type': 'bar',
            'data': [
                {'name': 'Baby (0-2)', 'value': 150000},
                {'name': 'Toddler (2-4)', 'value': 200000},
                {'name': 'Pre-school (4-6)', 'value': 180000},
                {'name': 'Early School (6-8)', 'value': 160000},
                {'name': 'Middle School (8-10)', 'value': 140000},
                {'name': 'Late School (10-12)', 'value': 120000},
                {'name': 'Teen (12-14)', 'value': 100000},
                {'name': 'Young Adult (14-16)', 'value': 80000},
            ]
        }
    
    def _get_seasonal_stock_data(self):
        """Get seasonal stock data"""
        return {
            'type': 'line',
            'data': [
                {'name': 'Summer', 'value': 250000},
                {'name': 'Winter', 'value': 300000},
                {'name': 'Monsoon', 'value': 200000},
                {'name': 'All Season', 'value': 150000},
            ]
        }
    
    def _get_brand_performance_data(self):
        """Get brand performance data"""
        return {
            'type': 'bar',
            'data': [
                {'name': 'Kids Brand A', 'value': 200000},
                {'name': 'Kids Brand B', 'value': 180000},
                {'name': 'Kids Brand C', 'value': 160000},
                {'name': 'Kids Brand D', 'value': 140000},
                {'name': 'Kids Brand E', 'value': 120000},
            ]
        }
    
    def _get_size_distribution_data(self):
        """Get size distribution data"""
        return {
            'type': 'bar',
            'data': [
                {'name': 'XS', 'value': 50000},
                {'name': 'S', 'value': 80000},
                {'name': 'M', 'value': 120000},
                {'name': 'L', 'value': 100000},
                {'name': 'XL', 'value': 80000},
                {'name': 'XXL', 'value': 60000},
                {'name': 'XXXL', 'value': 40000},
            ]
        }
    
    def _get_color_trends_data(self):
        """Get color trends data"""
        return {
            'type': 'pie',
            'data': [
                {'name': 'Blue', 'value': 25},
                {'name': 'Red', 'value': 20},
                {'name': 'Green', 'value': 15},
                {'name': 'Yellow', 'value': 12},
                {'name': 'Pink', 'value': 10},
                {'name': 'Purple', 'value': 8},
                {'name': 'Black', 'value': 5},
                {'name': 'White', 'value': 5},
            ]
        }
    
    def _get_recent_adjustments(self):
        """Get recent stock adjustments"""
        return [
            {'name': 'ADJ001', 'date': '2024-01-15', 'type': 'Physical Count', 'amount': 50000, 'status': 'Done'},
            {'name': 'ADJ002', 'date': '2024-01-14', 'type': 'Damage', 'amount': -25000, 'status': 'Done'},
            {'name': 'ADJ003', 'date': '2024-01-13', 'type': 'Seasonal', 'amount': 75000, 'status': 'Approved'},
            {'name': 'ADJ004', 'date': '2024-01-12', 'type': 'Expiry', 'amount': -30000, 'status': 'Done'},
            {'name': 'ADJ005', 'date': '2024-01-11', 'type': 'Size Adjustment', 'amount': 45000, 'status': 'Done'},
        ]


class StockManagementDashboardActWindow(ActWindow):
    """Stock Management Dashboard Action Window"""
    
    _name = 'action_stock_management_dashboard'
    _model = 'stock.management.dashboard'
    _view_mode = 'dashboard'
    _title = 'Stock Management Dashboard'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Welcome to the Stock Management Dashboard!',
            'message': 'Monitor your inventory levels and kids clothing stock performance.',
        }