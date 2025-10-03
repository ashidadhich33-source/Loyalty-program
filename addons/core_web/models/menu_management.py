# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MenuManagement(BaseModel):
    """Menu management for Kids Clothing ERP"""
    
    _name = 'menu.management'
    _description = 'Menu Management'
    _order = 'sequence, name'
    
    # Basic fields
    name = CharField(
        string='Menu Name',
        size=255,
        required=True,
        help='Display name of the menu item'
    
    )
    
    technical_name = CharField(
        string='Technical Name',
        size=255,
        required=True,
        help='Technical name for the menu item'
    
    )
    
    description = TextField(
        string='Description',
        help='Description of the menu item'
    )
    
    # Menu structure
    parent_id = Many2OneField(
        'menu.management',
        string='Parent Menu',
        help='Parent menu item'
    )
    
    child_ids = One2ManyField('menu.management', inverse_name='parent_id', string='Child Menus', help='Child menu items'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Menu sequence order'
    )
    
    # Menu properties
    icon = CharField(
        string='Icon',
        help='Icon class for the menu item'
    )
    
    action_id = Many2OneField(
        'ocean.actions.act_window',
        string='Action',
        help='Action to execute when menu is clicked'
    )
    
    url = CharField(
        string='URL',
        help='URL to navigate to when menu is clicked'
    )
    
    # Access control
    group_ids = Many2ManyField('ocean.groups', string='Groups', help='User groups that can access this menu'
    )
    
    user_ids = Many2ManyField('res.users', string='Users', help='Specific users who can access this menu'
    )
    
    # Menu state
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the menu is active'
    )
    
    is_visible = BooleanField(
        string='Visible',
        default=True,
        help='Whether the menu is visible'
    )
    
    is_clickable = BooleanField(
        string='Clickable',
        default=True,
        help='Whether the menu is clickable'
    )
    
    # Menu styling
    css_class = CharField(
        string='CSS Class',
        help='CSS class for menu styling'
    )
    
    badge_text = CharField(
        string='Badge Text',
        help='Badge text to display on menu'
    )
    
    badge_color = CharField(
        string='Badge Color',
        help='Badge color (CSS color value)'
    )
    
    # Menu behavior
    open_in_new_tab = BooleanField(
        string='Open in New Tab',
        default=False,
        help='Open menu in new tab'
    )
    
    confirm_before_action = BooleanField(
        string='Confirm Before Action',
        default=False,
        help='Show confirmation dialog before action'
    )
    
    confirmation_message = TextField(
        string='Confirmation Message',
        help='Message to show in confirmation dialog'
    )
    
    # Menu permissions
    require_permission = BooleanField(
        string='Require Permission',
        default=False,
        help='Require specific permission to access'
    )
    
    permission_name = CharField(
        string='Permission Name',
        help='Name of the required permission'
    )
    
    # Menu analytics
    click_count = IntegerField(
        string='Click Count',
        default=0,
        help='Number of times menu was clicked'
    )
    
    last_clicked = DateFieldtime(
        string='Last Clicked',
        help='When menu was last clicked'
    )
    
    # Menu customization
    is_customizable = BooleanField(
        string='Customizable',
        default=True,
        help='Whether menu can be customized by users'
    )
    
    is_system_menu = BooleanField(
        string='System Menu',
        default=False,
        help='Whether this is a system menu (cannot be deleted)'
    )
    
    # Menu dependencies
    depends_on = CharField(
        string='Depends On',
        help='Comma-separated list of menu technical names this menu depends on'
    )
    
    # Menu conditions
    condition = TextField(
        string='Condition',
        help='Python condition to evaluate for menu visibility'
    )
    
    @api.model
    def get_user_menus(self, user_id=None):
        """Get menus accessible to a user"""
        if not user_id:
            user_id = self.env.user.id
        
        user = self.env['res.users'].browse(user_id)
        
        # Get all active menus
        menus = self.search([
            ('is_active', '=', True),
            ('is_visible', '=', True),
        ])
        
        # Filter by user access
        accessible_menus = []
        for menu in menus:
            if self._can_access_menu(menu, user):
                accessible_menus.append(menu)
        
        return accessible_menus
    
    def _can_access_menu(self, menu, user):
        """Check if user can access a menu"""
        # Check if menu has specific users
        if menu.user_ids and user not in menu.user_ids:
            return False
        
        # Check if menu has specific groups
        if menu.group_ids and not any(group in user.groups_id for group in menu.group_ids):
            return False
        
        # Check if menu requires permission
        if menu.require_permission:
            if not self._has_permission(menu.permission_name, user):
                return False
        
        # Check if menu has condition
        if menu.condition:
            if not self._evaluate_condition(menu.condition, user):
                return False
        
        return True
    
    def _has_permission(self, permission_name, user):
        """Check if user has specific permission"""
        # This would implement permission checking logic
        return True
    
    def _evaluate_condition(self, condition, user):
        """Evaluate menu condition"""
        try:
            # This would implement condition evaluation logic
            return True
        except Exception as e:
            _logger.error(f"Error evaluating menu condition: {str(e)}")
            return False
    
    def click_menu(self):
        """Handle menu click"""
        self.click_count += 1
        self.last_clicked = DateFieldtime.now()
        
        # Execute menu action
        if self.action_id:
            return self.action_id.read()[0]
        elif self.url:
            return {'type': 'ocean.actions.act_url', 'url': self.url}
        
        return {}
    
    def get_menu_tree(self, user_id=None):
        """Get menu tree for a user"""
        if not user_id:
            user_id = self.env.user.id
        
        user_menus = self.get_user_menus(user_id)
        
        # Build tree structure
        menu_tree = []
        for menu in user_menus:
            if not menu.parent_id:
                menu_tree.append(self._build_menu_node(menu, user_menus))
        
        return menu_tree
    
    def _build_menu_node(self, menu, all_menus):
        """Build menu node with children"""
        node = {
            'id': menu.id,
            'name': menu.name,
            'technical_name': menu.technical_name,
            'icon': menu.icon,
            'url': menu.url,
            'action_id': menu.action_id.id if menu.action_id else None,
            'badge_text': menu.badge_text,
            'badge_color': menu.badge_color,
            'css_class': menu.css_class,
            'open_in_new_tab': menu.open_in_new_tab,
            'confirm_before_action': menu.confirm_before_action,
            'confirmation_message': menu.confirmation_message,
            'children': []
        }
        
        # Add children
        for child in all_menus:
            if child.parent_id == menu:
                node['children'].append(self._build_menu_node(child, all_menus))
        
        return node
    
    @api.model
    def create_menu(self, name, technical_name, parent_id=None, **kwargs):
        """Create a new menu item"""
        menu_vals = {
            'name': name,
            'technical_name': technical_name,
            'parent_id': parent_id,
            **kwargs
        }
        
        return self.create(menu_vals)
    
    @api.model
    def update_menu(self, technical_name, **kwargs):
        """Update menu by technical name"""
        menu = self.search([('technical_name', '=', technical_name)], limit=1)
        if menu:
            menu.write(kwargs)
        return menu
    
    @api.model
    def delete_menu(self, technical_name):
        """Delete menu by technical name"""
        menu = self.search([('technical_name', '=', technical_name)], limit=1)
        if menu and not menu.is_system_menu:
            menu.unlink()
        return menu
    
    @api.model
    def get_menu_by_technical_name(self, technical_name):
        """Get menu by technical name"""
        return self.search([('technical_name', '=', technical_name)], limit=1)
    
    @api.model
    def get_menu_breadcrumb(self, technical_name):
        """Get breadcrumb for a menu"""
        menu = self.get_menu_by_technical_name(technical_name)
        if not menu:
            return []
        
        breadcrumb = []
        current_menu = menu
        
        while current_menu:
            breadcrumb.insert(0, {
                'name': current_menu.name,
                'technical_name': current_menu.technical_name,
                'url': current_menu.url,
                'action_id': current_menu.action_id.id if current_menu.action_id else None,
            })
            current_menu = current_menu.parent_id
        
        return breadcrumb
    
    @api.model
    def get_menu_analytics(self, date_from=None, date_to=None):
        """Get menu analytics"""
        domain = []
        
        if date_from:
            domain.append(('last_clicked', '>=', date_from))
        if date_to:
            domain.append(('last_clicked', '<=', date_to))
        
        menus = self.search(domain)
        
        analytics = {
            'total_menus': len(menus),
            'active_menus': len(menus.filtered('is_active')),
            'total_clicks': sum(menus.mapped('click_count')),
            'most_clicked': menus.sorted('click_count', reverse=True)[:10],
            'recent_clicks': menus.sorted('last_clicked', reverse=True)[:10],
        }
        
        return analytics
    
    @api.model
    def reset_menu_analytics(self):
        """Reset menu analytics"""
        menus = self.search([])
        menus.write({
            'click_count': 0,
            'last_clicked': False,
        })
        
        _logger.info("Menu analytics reset")
        return len(menus)
    
    @api.model
    def export_menu_structure(self):
        """Export menu structure"""
        menus = self.search([])
        
        structure = []
        for menu in menus:
            structure.append({
                'technical_name': menu.technical_name,
                'name': menu.name,
                'parent_technical_name': menu.parent_id.technical_name if menu.parent_id else None,
                'sequence': menu.sequence,
                'icon': menu.icon,
                'action_id': menu.action_id.id if menu.action_id else None,
                'url': menu.url,
                'group_ids': menu.group_ids.ids,
                'user_ids': menu.user_ids.ids,
                'is_active': menu.is_active,
                'is_visible': menu.is_visible,
                'is_clickable': menu.is_clickable,
                'css_class': menu.css_class,
                'badge_text': menu.badge_text,
                'badge_color': menu.badge_color,
                'open_in_new_tab': menu.open_in_new_tab,
                'confirm_before_action': menu.confirm_before_action,
                'confirmation_message': menu.confirmation_message,
                'require_permission': menu.require_permission,
                'permission_name': menu.permission_name,
                'is_customizable': menu.is_customizable,
                'is_system_menu': menu.is_system_menu,
                'depends_on': menu.depends_on,
                'condition': menu.condition,
            })
        
        return structure
    
    @api.model
    def import_menu_structure(self, structure):
        """Import menu structure"""
        imported_count = 0
        
        for menu_data in structure:
            # Find parent menu
            parent_id = None
            if menu_data.get('parent_technical_name'):
                parent = self.search([('technical_name', '=', menu_data['parent_technical_name'])], limit=1)
                if parent:
                    parent_id = parent.id
            
            # Create or update menu
            menu = self.search([('technical_name', '=', menu_data['technical_name'])], limit=1)
            if menu:
                menu.write({
                    'name': menu_data['name'],
                    'parent_id': parent_id,
                    'sequence': menu_data['sequence'],
                    'icon': menu_data['icon'],
                    'action_id': menu_data['action_id'],
                    'url': menu_data['url'],
                    'group_ids': [(6, 0, menu_data['group_ids'])],
                    'user_ids': [(6, 0, menu_data['user_ids'])],
                    'is_active': menu_data['is_active'],
                    'is_visible': menu_data['is_visible'],
                    'is_clickable': menu_data['is_clickable'],
                    'css_class': menu_data['css_class'],
                    'badge_text': menu_data['badge_text'],
                    'badge_color': menu_data['badge_color'],
                    'open_in_new_tab': menu_data['open_in_new_tab'],
                    'confirm_before_action': menu_data['confirm_before_action'],
                    'confirmation_message': menu_data['confirmation_message'],
                    'require_permission': menu_data['require_permission'],
                    'permission_name': menu_data['permission_name'],
                    'is_customizable': menu_data['is_customizable'],
                    'is_system_menu': menu_data['is_system_menu'],
                    'depends_on': menu_data['depends_on'],
                    'condition': menu_data['condition'],
                })
            else:
                self.create({
                    'technical_name': menu_data['technical_name'],
                    'name': menu_data['name'],
                    'parent_id': parent_id,
                    'sequence': menu_data['sequence'],
                    'icon': menu_data['icon'],
                    'action_id': menu_data['action_id'],
                    'url': menu_data['url'],
                    'group_ids': [(6, 0, menu_data['group_ids'])],
                    'user_ids': [(6, 0, menu_data['user_ids'])],
                    'is_active': menu_data['is_active'],
                    'is_visible': menu_data['is_visible'],
                    'is_clickable': menu_data['is_clickable'],
                    'css_class': menu_data['css_class'],
                    'badge_text': menu_data['badge_text'],
                    'badge_color': menu_data['badge_color'],
                    'open_in_new_tab': menu_data['open_in_new_tab'],
                    'confirm_before_action': menu_data['confirm_before_action'],
                    'confirmation_message': menu_data['confirmation_message'],
                    'require_permission': menu_data['require_permission'],
                    'permission_name': menu_data['permission_name'],
                    'is_customizable': menu_data['is_customizable'],
                    'is_system_menu': menu_data['is_system_menu'],
                    'depends_on': menu_data['depends_on'],
                    'condition': menu_data['condition'],
                })
                imported_count += 1
        
        _logger.info(f"Imported {imported_count} menu items")
        return imported_count