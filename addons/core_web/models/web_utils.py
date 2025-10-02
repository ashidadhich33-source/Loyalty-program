# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json
import base64
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class WebUtils(models.AbstractModel):
    """Web utilities for Kids Clothing ERP"""
    
    _name = 'web.utils'
    _description = 'Web Utilities'
    
    @api.model
    def get_user_preferences(self):
        """Get user preferences for web interface"""
        user = self.env.user
        
        preferences = {
            'theme': 'kids_clothing',
            'language': user.lang or 'en_US',
            'timezone': user.tz or 'Asia/Kolkata',
            'date_format': '%d/%m/%Y',
            'time_format': '%H:%M:%S',
            'currency': 'INR',
            'notifications_enabled': True,
            'sound_enabled': True,
            'animations_enabled': True,
            'touchscreen_mode': False,
            'compact_mode': False,
        }
        
        return preferences
    
    @api.model
    def set_user_preferences(self, preferences):
        """Set user preferences for web interface"""
        user = self.env.user
        
        # Update user preferences
        if 'language' in preferences:
            user.lang = preferences['language']
        if 'timezone' in preferences:
            user.tz = preferences['timezone']
        
        # Store additional preferences in user context
        user_context = user.context or {}
        user_context.update(preferences)
        user.context = user_context
        
        return True
    
    @api.model
    def get_theme_config(self):
        """Get theme configuration for kids clothing theme"""
        return {
            'name': 'Kids Clothing Theme',
            'version': '1.0.0',
            'colors': {
                'primary': '#ff6b6b',
                'secondary': '#4ecdc4',
                'accent': '#45b7d1',
                'success': '#96ceb4',
                'warning': '#feca57',
                'danger': '#ff9ff3',
                'light': '#f8f9fa',
                'dark': '#2c3e50',
            },
            'fonts': {
                'primary': 'Roboto, sans-serif',
                'secondary': 'Open Sans, sans-serif',
                'monospace': 'Monaco, monospace',
            },
            'sizes': {
                'small': '12px',
                'medium': '14px',
                'large': '16px',
                'xlarge': '18px',
            },
            'spacing': {
                'xs': '4px',
                'sm': '8px',
                'md': '16px',
                'lg': '24px',
                'xl': '32px',
            },
            'border_radius': {
                'small': '4px',
                'medium': '8px',
                'large': '12px',
                'round': '50%',
            },
            'shadows': {
                'light': '0 2px 4px rgba(0,0,0,0.1)',
                'medium': '0 4px 8px rgba(0,0,0,0.15)',
                'heavy': '0 8px 16px rgba(0,0,0,0.2)',
            },
        }
    
    @api.model
    def get_responsive_breakpoints(self):
        """Get responsive breakpoints for different screen sizes"""
        return {
            'xs': '0px',
            'sm': '576px',
            'md': '768px',
            'lg': '992px',
            'xl': '1200px',
            'xxl': '1400px',
        }
    
    @api.model
    def get_icon_mapping(self):
        """Get icon mapping for different modules and actions"""
        return {
            'core': 'fa-cog',
            'contacts': 'fa-users',
            'products': 'fa-shopping-bag',
            'sales': 'fa-shopping-cart',
            'pos': 'fa-cash-register',
            'inventory': 'fa-warehouse',
            'accounting': 'fa-calculator',
            'hr': 'fa-user-tie',
            'reports': 'fa-chart-bar',
            'settings': 'fa-cogs',
            'help': 'fa-question-circle',
            'logout': 'fa-sign-out-alt',
            'profile': 'fa-user',
            'notifications': 'fa-bell',
            'search': 'fa-search',
            'filter': 'fa-filter',
            'sort': 'fa-sort',
            'add': 'fa-plus',
            'edit': 'fa-edit',
            'delete': 'fa-trash',
            'save': 'fa-save',
            'cancel': 'fa-times',
            'print': 'fa-print',
            'export': 'fa-download',
            'import': 'fa-upload',
            'refresh': 'fa-refresh',
            'back': 'fa-arrow-left',
            'forward': 'fa-arrow-right',
            'up': 'fa-arrow-up',
            'down': 'fa-arrow-down',
            'left': 'fa-chevron-left',
            'right': 'fa-chevron-right',
            'expand': 'fa-expand',
            'collapse': 'fa-compress',
            'fullscreen': 'fa-expand-arrows-alt',
            'minimize': 'fa-window-minimize',
            'maximize': 'fa-window-maximize',
            'close': 'fa-times',
            'check': 'fa-check',
            'warning': 'fa-exclamation-triangle',
            'error': 'fa-exclamation-circle',
            'info': 'fa-info-circle',
            'success': 'fa-check-circle',
        }
    
    @api.model
    def get_menu_structure(self):
        """Get menu structure for the application"""
        return {
            'main': {
                'name': 'Kids Clothing ERP',
                'icon': 'fa-shopping-bag',
                'children': [
                    {
                        'name': 'Dashboard',
                        'icon': 'fa-tachometer-alt',
                        'action': 'action_dashboard',
                        'sequence': 10,
                    },
                    {
                        'name': 'Sales',
                        'icon': 'fa-shopping-cart',
                        'children': [
                            {
                                'name': 'Quotations',
                                'action': 'action_quotations',
                                'sequence': 10,
                            },
                            {
                                'name': 'Sales Orders',
                                'action': 'action_sales_orders',
                                'sequence': 20,
                            },
                            {
                                'name': 'Customers',
                                'action': 'action_customers',
                                'sequence': 30,
                            },
                        ],
                        'sequence': 20,
                    },
                    {
                        'name': 'Point of Sale',
                        'icon': 'fa-cash-register',
                        'action': 'action_pos',
                        'sequence': 30,
                    },
                    {
                        'name': 'Inventory',
                        'icon': 'fa-warehouse',
                        'children': [
                            {
                                'name': 'Products',
                                'action': 'action_products',
                                'sequence': 10,
                            },
                            {
                                'name': 'Stock',
                                'action': 'action_stock',
                                'sequence': 20,
                            },
                            {
                                'name': 'Warehouses',
                                'action': 'action_warehouses',
                                'sequence': 30,
                            },
                        ],
                        'sequence': 40,
                    },
                    {
                        'name': 'Accounting',
                        'icon': 'fa-calculator',
                        'children': [
                            {
                                'name': 'Invoices',
                                'action': 'action_invoices',
                                'sequence': 10,
                            },
                            {
                                'name': 'Payments',
                                'action': 'action_payments',
                                'sequence': 20,
                            },
                            {
                                'name': 'Reports',
                                'action': 'action_accounting_reports',
                                'sequence': 30,
                            },
                        ],
                        'sequence': 50,
                    },
                    {
                        'name': 'Reports',
                        'icon': 'fa-chart-bar',
                        'action': 'action_reports',
                        'sequence': 60,
                    },
                    {
                        'name': 'Settings',
                        'icon': 'fa-cogs',
                        'action': 'action_settings',
                        'sequence': 70,
                    },
                ],
            },
        }
    
    @api.model
    def get_breadcrumb(self, model, record_id=None):
        """Get breadcrumb navigation for current page"""
        breadcrumb = []
        
        # Add home
        breadcrumb.append({
            'name': 'Home',
            'url': '/web',
            'icon': 'fa-home',
        })
        
        # Add model-specific breadcrumb
        if model:
            model_info = self.get_model_info(model)
            breadcrumb.append({
                'name': model_info['name'],
                'url': f'/web#model={model}',
                'icon': model_info['icon'],
            })
        
        # Add record-specific breadcrumb
        if record_id:
            record = self.env[model].browse(record_id)
            if record.exists():
                breadcrumb.append({
                    'name': record.display_name,
                    'url': f'/web#id={record_id}&model={model}',
                    'icon': 'fa-file',
                })
        
        return breadcrumb
    
    @api.model
    def get_model_info(self, model_name):
        """Get model information for display"""
        model_info = {
            'name': model_name.replace('.', ' ').title(),
            'icon': 'fa-file',
            'description': '',
        }
        
        # Model-specific information
        model_mapping = {
            'res.partner': {'name': 'Contacts', 'icon': 'fa-users'},
            'product.template': {'name': 'Products', 'icon': 'fa-shopping-bag'},
            'sale.order': {'name': 'Sales Orders', 'icon': 'fa-shopping-cart'},
            'pos.order': {'name': 'POS Orders', 'icon': 'fa-cash-register'},
            'stock.quant': {'name': 'Stock', 'icon': 'fa-warehouse'},
            'account.move': {'name': 'Invoices', 'icon': 'fa-file-invoice'},
            'res.users': {'name': 'Users', 'icon': 'fa-users'},
            'res.company': {'name': 'Companies', 'icon': 'fa-building'},
        }
        
        if model_name in model_mapping:
            model_info.update(model_mapping[model_name])
        
        return model_info
    
    @api.model
    def get_page_title(self, model=None, record_id=None):
        """Get page title for current page"""
        if model and record_id:
            record = self.env[model].browse(record_id)
            if record.exists():
                return f"{record.display_name} - Kids Clothing ERP"
        elif model:
            model_info = self.get_model_info(model)
            return f"{model_info['name']} - Kids Clothing ERP"
        else:
            return "Kids Clothing ERP"
    
    @api.model
    def get_favicon(self):
        """Get favicon for the application"""
        return '/core_web/static/src/img/favicon.ico'
    
    @api.model
    def get_logo(self):
        """Get logo for the application"""
        return '/core_web/static/src/img/logo.png'
    
    @api.model
    def get_loading_spinner(self):
        """Get loading spinner HTML"""
        return '''
        <div class="loading-spinner-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading...</div>
        </div>
        '''
    
    @api.model
    def get_error_page(self, error_code, error_message):
        """Get error page HTML"""
        return f'''
        <div class="error-page">
            <div class="error-code">{error_code}</div>
            <div class="error-message">{error_message}</div>
            <div class="error-actions">
                <a href="/web" class="btn btn-primary">Go Home</a>
                <a href="javascript:history.back()" class="btn btn-secondary">Go Back</a>
            </div>
        </div>
        '''
    
    @api.model
    def get_success_page(self, title, message, redirect_url=None):
        """Get success page HTML"""
        return f'''
        <div class="success-page">
            <div class="success-icon">✓</div>
            <div class="success-title">{title}</div>
            <div class="success-message">{message}</div>
            <div class="success-actions">
                {f'<a href="{redirect_url}" class="btn btn-primary">Continue</a>' if redirect_url else ''}
                <a href="/web" class="btn btn-secondary">Go Home</a>
            </div>
        </div>
        '''
    
    @api.model
    def get_confirm_dialog(self, title, message, confirm_text="Confirm", cancel_text="Cancel"):
        """Get confirmation dialog HTML"""
        return f'''
        <div class="confirm-dialog">
            <div class="confirm-title">{title}</div>
            <div class="confirm-message">{message}</div>
            <div class="confirm-actions">
                <button class="btn btn-primary confirm-btn">{confirm_text}</button>
                <button class="btn btn-secondary cancel-btn">{cancel_text}</button>
            </div>
        </div>
        '''
    
    @api.model
    def get_tooltip(self, text, position="top"):
        """Get tooltip HTML"""
        return f'''
        <div class="tooltip tooltip-{position}" data-tooltip="{text}">
            <i class="fa fa-question-circle"></i>
        </div>
        '''
    
    @api.model
    def get_badge(self, text, type="default"):
        """Get badge HTML"""
        return f'<span class="badge badge-{type}">{text}</span>'
    
    @api.model
    def get_alert(self, message, type="info"):
        """Get alert HTML"""
        return f'''
        <div class="alert alert-{type}">
            <i class="fa fa-info-circle"></i>
            <span class="alert-message">{message}</span>
            <button class="alert-close">&times;</button>
        </div>
        '''
    
    @api.model
    def get_progress_bar(self, value, max_value=100, show_percentage=True):
        """Get progress bar HTML"""
        percentage = (value / max_value) * 100 if max_value > 0 else 0
        return f'''
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%"></div>
            {f'<span class="progress-text">{percentage:.1f}%</span>' if show_percentage else ''}
        </div>
        '''
    
    @api.model
    def get_rating_stars(self, rating, max_rating=5, interactive=False):
        """Get rating stars HTML"""
        stars = ''
        for i in range(1, max_rating + 1):
            if i <= rating:
                stars += '<i class="fa fa-star star-filled"></i>'
            elif i - 0.5 <= rating:
                stars += '<i class="fa fa-star-half-o star-half"></i>'
            else:
                stars += '<i class="fa fa-star-o star-empty"></i>'
        
        return f'''
        <div class="rating-stars {"interactive" if interactive else ""}">
            {stars}
        </div>
        '''
    
    @api.model
    def get_pagination(self, current_page, total_pages, base_url):
        """Get pagination HTML"""
        pagination = '<div class="pagination">'
        
        # Previous button
        if current_page > 1:
            pagination += f'<a href="{base_url}?page={current_page-1}" class="page-btn prev">Previous</a>'
        
        # Page numbers
        start_page = max(1, current_page - 2)
        end_page = min(total_pages, current_page + 2)
        
        for page in range(start_page, end_page + 1):
            if page == current_page:
                pagination += f'<span class="page-btn current">{page}</span>'
            else:
                pagination += f'<a href="{base_url}?page={page}" class="page-btn">{page}</a>'
        
        # Next button
        if current_page < total_pages:
            pagination += f'<a href="{base_url}?page={current_page+1}" class="page-btn next">Next</a>'
        
        pagination += '</div>'
        return pagination