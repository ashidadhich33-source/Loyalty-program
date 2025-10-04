# -*- coding: utf-8 -*-
"""
Ocean ERP - Accounting Dashboard
=================================

Accounting dashboard for kids clothing retail.
"""

from core_framework.ui import View, DashboardView
from core_framework.actions import ActWindow


class AccountingDashboardView(DashboardView):
    """Accounting Dashboard View"""
    
    _name = 'accounting.dashboard'
    _title = 'Accounting Dashboard'
    
    def get_dashboard_widgets(self):
        """Get dashboard widgets"""
        return [
            {
                'name': 'chart_of_accounts_widget',
                'title': 'Chart of Accounts',
                'type': 'chart',
                'data': self._get_chart_of_accounts_data(),
                'width': 6,
            },
            {
                'name': 'journal_entries_widget',
                'title': 'Recent Journal Entries',
                'type': 'list',
                'data': self._get_recent_journal_entries(),
                'width': 6,
            },
            {
                'name': 'account_balances_widget',
                'title': 'Account Balances',
                'type': 'table',
                'data': self._get_account_balances(),
                'width': 12,
            },
            {
                'name': 'kids_clothing_sales_widget',
                'title': 'Kids Clothing Sales by Age Group',
                'type': 'chart',
                'data': self._get_kids_clothing_sales_data(),
                'width': 6,
            },
            {
                'name': 'seasonal_analysis_widget',
                'title': 'Seasonal Analysis',
                'type': 'chart',
                'data': self._get_seasonal_analysis_data(),
                'width': 6,
            },
            {
                'name': 'brand_performance_widget',
                'title': 'Brand Performance',
                'type': 'chart',
                'data': self._get_brand_performance_data(),
                'width': 12,
            },
        ]
    
    def _get_chart_of_accounts_data(self):
        """Get chart of accounts data"""
        return {
            'type': 'pie',
            'data': [
                {'name': 'Assets', 'value': 1000000},
                {'name': 'Liabilities', 'value': 500000},
                {'name': 'Equity', 'value': 300000},
                {'name': 'Income', 'value': 800000},
                {'name': 'Expenses', 'value': 600000},
            ]
        }
    
    def _get_recent_journal_entries(self):
        """Get recent journal entries"""
        return [
            {'name': 'ENTRY001', 'date': '2024-01-15', 'amount': 50000, 'status': 'Posted'},
            {'name': 'ENTRY002', 'date': '2024-01-14', 'amount': 25000, 'status': 'Posted'},
            {'name': 'ENTRY003', 'date': '2024-01-13', 'amount': 75000, 'status': 'Draft'},
            {'name': 'ENTRY004', 'date': '2024-01-12', 'amount': 30000, 'status': 'Posted'},
            {'name': 'ENTRY005', 'date': '2024-01-11', 'amount': 45000, 'status': 'Posted'},
        ]
    
    def _get_account_balances(self):
        """Get account balances"""
        return [
            {'account': '1000 - Cash', 'balance': 150000, 'type': 'Asset'},
            {'account': '1100 - Accounts Receivable', 'balance': 200000, 'type': 'Asset'},
            {'account': '1200 - Inventory', 'balance': 300000, 'type': 'Asset'},
            {'account': '2000 - Accounts Payable', 'balance': 100000, 'type': 'Liability'},
            {'account': '3000 - Capital', 'balance': 500000, 'type': 'Equity'},
            {'account': '4000 - Sales', 'balance': 800000, 'type': 'Income'},
            {'account': '5000 - Cost of Goods Sold', 'balance': 400000, 'type': 'Expense'},
        ]
    
    def _get_kids_clothing_sales_data(self):
        """Get kids clothing sales data"""
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
    
    def _get_seasonal_analysis_data(self):
        """Get seasonal analysis data"""
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


class AccountingDashboardActWindow(ActWindow):
    """Accounting Dashboard Action Window"""
    
    _name = 'action_accounting_dashboard'
    _model = 'accounting.dashboard'
    _view_mode = 'dashboard'
    _title = 'Accounting Dashboard'
    
    def get_context(self):
        """Get action window context"""
        return {}
    
    def get_domain(self):
        """Get action window domain"""
        return []
    
    def get_help(self):
        """Get action window help"""
        return {
            'title': 'Welcome to the Accounting Dashboard!',
            'message': 'Monitor your financial performance and kids clothing business metrics.',
        }