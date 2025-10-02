/* Kids Clothing ERP - User Script */

odoo.define('users.KidsClothingUsers', function (require) {
    'use strict';

    var core = require('web.core');
    var FormController = require('web.FormController');
    var ListController = require('web.ListController');
    var AbstractController = require('web.AbstractController');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var _t = core._t;

    // User Management Utilities
    var UserUtils = {
        // User Status Management
        getUserStatus: function(user) {
            if (!user.active) return 'inactive';
            if (user.account_locked) return 'locked';
            if (user.last_login_date) {
                var lastLogin = new Date(user.last_login_date);
                var now = new Date();
                var diffHours = (now - lastLogin) / (1000 * 60 * 60);
                if (diffHours < 1) return 'online';
            }
            return 'offline';
        },
        
        getUserStatusBadge: function(status) {
            var badges = {
                'active': '<span class="user-status user-status-active">Active</span>',
                'inactive': '<span class="user-status user-status-inactive">Inactive</span>',
                'locked': '<span class="user-status user-status-locked">Locked</span>',
                'online': '<span class="user-status user-status-online">Online</span>',
                'offline': '<span class="user-status user-status-offline">Offline</span>'
            };
            return badges[status] || '';
        },
        
        // User Activity Management
        getActivityIcon: function(activityType) {
            var icons = {
                'login': 'fa-sign-in-alt',
                'logout': 'fa-sign-out-alt',
                'create': 'fa-plus',
                'update': 'fa-edit',
                'delete': 'fa-trash',
                'read': 'fa-eye',
                'search': 'fa-search',
                'export': 'fa-download',
                'import': 'fa-upload',
                'print': 'fa-print',
                'email': 'fa-envelope',
                'sms': 'fa-sms',
                'notification': 'fa-bell',
                'security': 'fa-shield-alt',
                'group_assignment': 'fa-user-plus',
                'group_removal': 'fa-user-minus',
                'permission_grant': 'fa-key',
                'permission_revoke': 'fa-key',
                'access_grant': 'fa-unlock',
                'access_revoke': 'fa-lock',
                'password_change': 'fa-lock',
                'password_reset': 'fa-lock',
                'account_lock': 'fa-lock',
                'account_unlock': 'fa-unlock',
                'profile_update': 'fa-user-edit',
                'preference_change': 'fa-cog',
                'system_access': 'fa-desktop',
                'data_access': 'fa-database',
                'report_generation': 'fa-chart-bar',
                'backup': 'fa-save',
                'restore': 'fa-undo',
                'other': 'fa-info-circle'
            };
            return icons[activityType] || 'fa-info-circle';
        },
        
        getActivityIconClass: function(activityType) {
            var classes = {
                'login': 'activity-icon-login',
                'logout': 'activity-icon-logout',
                'create': 'activity-icon-create',
                'update': 'activity-icon-update',
                'delete': 'activity-icon-delete',
                'security': 'activity-icon-security'
            };
            return classes[activityType] || 'activity-icon-login';
        },
        
        formatActivityTime: function(dateString) {
            if (!dateString) return '';
            
            var date = new Date(dateString);
            var now = new Date();
            var diff = now - date;
            
            if (diff < 60000) return 'Just now';
            if (diff < 3600000) return Math.floor(diff / 60000) + ' minutes ago';
            if (diff < 86400000) return Math.floor(diff / 3600000) + ' hours ago';
            if (diff < 604800000) return Math.floor(diff / 86400000) + ' days ago';
            
            return date.toLocaleDateString();
        },
        
        // Permission Management
        getPermissionIcon: function(accessLevel) {
            var icons = {
                'read': 'fa-eye',
                'write': 'fa-edit',
                'create': 'fa-plus',
                'delete': 'fa-trash',
                'admin': 'fa-crown'
            };
            return icons[accessLevel] || 'fa-eye';
        },
        
        getPermissionIconClass: function(accessLevel) {
            var classes = {
                'read': 'permission-icon-read',
                'write': 'permission-icon-write',
                'create': 'permission-icon-create',
                'delete': 'permission-icon-delete',
                'admin': 'permission-icon-admin'
            };
            return classes[accessLevel] || 'permission-icon-read';
        },
        
        getPermissionLevelClass: function(accessLevel) {
            var classes = {
                'read': 'permission-level-read',
                'write': 'permission-level-write',
                'create': 'permission-level-create',
                'delete': 'permission-level-delete',
                'admin': 'permission-level-admin'
            };
            return classes[accessLevel] || 'permission-level-read';
        },
        
        // Group Management
        getGroupIcon: function(category) {
            var icons = {
                'core': 'fa-cog',
                'sales': 'fa-shopping-cart',
                'inventory': 'fa-warehouse',
                'accounting': 'fa-calculator',
                'hr': 'fa-users',
                'pos': 'fa-cash-register',
                'reports': 'fa-chart-bar',
                'settings': 'fa-cogs',
                'custom': 'fa-user-tag'
            };
            return icons[category] || 'fa-user-tag';
        },
        
        getGroupCategoryClass: function(category) {
            var classes = {
                'core': 'group-category',
                'sales': 'group-category',
                'inventory': 'group-category',
                'accounting': 'group-category',
                'hr': 'group-category',
                'pos': 'group-category',
                'reports': 'group-category',
                'settings': 'group-category',
                'custom': 'group-category'
            };
            return classes[category] || 'group-category';
        },
        
        // Preference Management
        getPreferenceIcon: function(category) {
            var icons = {
                'ui': 'fa-desktop',
                'notifications': 'fa-bell',
                'security': 'fa-shield-alt',
                'performance': 'fa-tachometer-alt',
                'accessibility': 'fa-universal-access',
                'localization': 'fa-globe',
                'integration': 'fa-plug',
                'custom': 'fa-cog'
            };
            return icons[category] || 'fa-cog';
        },
        
        getPreferenceIconClass: function(category) {
            var classes = {
                'ui': 'preference-icon-ui',
                'notifications': 'preference-icon-notifications',
                'security': 'preference-icon-security',
                'performance': 'preference-icon-performance',
                'accessibility': 'preference-icon-accessibility',
                'localization': 'preference-icon-localization',
                'integration': 'preference-icon-integration',
                'custom': 'preference-icon-custom'
            };
            return classes[category] || 'preference-icon-custom';
        },
        
        getPreferenceValueClass: function(valueType) {
            var classes = {
                'string': 'preference-value',
                'integer': 'preference-value',
                'float': 'preference-value',
                'boolean': 'preference-value',
                'json': 'preference-value',
                'date': 'preference-value',
                'datetime': 'preference-value'
            };
            return classes[valueType] || 'preference-value';
        },
        
        getPreferenceTypeClass: function(valueType) {
            var classes = {
                'string': 'preference-type',
                'integer': 'preference-type',
                'float': 'preference-type',
                'boolean': 'preference-type',
                'json': 'preference-type',
                'date': 'preference-type',
                'datetime': 'preference-type'
            };
            return classes[valueType] || 'preference-type';
        }
    };

    // User Form Controller
    var UserFormController = FormController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceUserForm();
            });
        },
        
        enhanceUserForm: function() {
            var self = this;
            
            // Add fade-in animation
            this.$el.addClass('fade-in-up');
            
            // Enhance user status display
            this._super();
        },
        
        _onButtonClicked: function(event) {
            var self = this;
            var $target = $(event.currentTarget);
            var action = $target.data('action');
            
            if (action === 'login') {
                self._handleUserLogin();
            } else if (action === 'unlock') {
                self._handleAccountUnlock();
            } else if (action === 'reset_password') {
                self._handlePasswordReset();
            } else {
                this._super(event);
            }
        },
        
        _handleUserLogin: function() {
            var self = this;
            var user = this.model.get(this.handle);
            
            rpc.query({
                model: 'res.users',
                method: 'action_login',
                args: [user.id],
                context: {
                    ip_address: this._getClientIP(),
                    user_agent: navigator.userAgent
                }
            }).then(function(result) {
                if (result) {
                    self._showNotification('User logged in successfully', 'success');
                    self.reload();
                }
            });
        },
        
        _handleAccountUnlock: function() {
            var self = this;
            var user = this.model.get(this.handle);
            
            Dialog.confirm(this, _t('Are you sure you want to unlock this account?'), {
                title: _t('Unlock Account'),
                confirm_callback: function() {
                    rpc.query({
                        model: 'res.users',
                        method: 'action_unlock_account',
                        args: [user.id],
                        context: {
                            ip_address: self._getClientIP(),
                            user_agent: navigator.userAgent
                        }
                    }).then(function(result) {
                        if (result) {
                            self._showNotification('Account unlocked successfully', 'success');
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _handlePasswordReset: function() {
            var self = this;
            var user = this.model.get(this.handle);
            
            Dialog.confirm(this, _t('Are you sure you want to reset the password for this user?'), {
                title: _t('Reset Password'),
                confirm_callback: function() {
                    rpc.query({
                        model: 'res.users',
                        method: 'action_reset_password',
                        args: [user.id],
                        context: {
                            ip_address: self._getClientIP(),
                            user_agent: navigator.userAgent
                        }
                    }).then(function(result) {
                        if (result) {
                            self._showNotification('Password reset successfully. New password: ' + result, 'success');
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _getClientIP: function() {
            // This would need to be implemented to get the actual client IP
            return '127.0.0.1';
        },
        
        _showNotification: function(message, type) {
            // This would integrate with the notification system
            console.log(type + ': ' + message);
        }
    });

    // User List Controller
    var UserListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceUserList();
            });
        },
        
        enhanceUserList: function() {
            var self = this;
            
            // Add user status badges
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var userData = $row.data('record');
                
                if (userData) {
                    var status = UserUtils.getUserStatus(userData);
                    var badge = UserUtils.getUserStatusBadge(status);
                    
                    // Add status badge to the row
                    $row.find('td:first').append(badge);
                }
            });
        }
    });

    // Activity List Controller
    var ActivityListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceActivityList();
            });
        },
        
        enhanceActivityList: function() {
            var self = this;
            
            // Add activity icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var activityData = $row.data('record');
                
                if (activityData) {
                    var icon = UserUtils.getActivityIcon(activityData.activity_type);
                    var iconClass = UserUtils.getActivityIconClass(activityData.activity_type);
                    var time = UserUtils.formatActivityTime(activityData.create_date);
                    
                    // Add activity icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' ' + iconClass + '"></i>');
                    
                    // Format time
                    var $timeCell = $row.find('td[data-field="create_date"]');
                    if ($timeCell.length) {
                        $timeCell.text(time);
                    }
                }
            });
        }
    });

    // Permission List Controller
    var PermissionListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhancePermissionList();
            });
        },
        
        enhancePermissionList: function() {
            var self = this;
            
            // Add permission icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var permissionData = $row.data('record');
                
                if (permissionData) {
                    var icon = UserUtils.getPermissionIcon(permissionData.access_level);
                    var iconClass = UserUtils.getPermissionIconClass(permissionData.access_level);
                    var levelClass = UserUtils.getPermissionLevelClass(permissionData.access_level);
                    
                    // Add permission icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' ' + iconClass + '"></i>');
                    
                    // Add access level badge
                    var $levelCell = $row.find('td[data-field="access_level"]');
                    if ($levelCell.length) {
                        $levelCell.html('<span class="' + levelClass + '">' + permissionData.access_level + '</span>');
                    }
                }
            });
        }
    });

    // Group List Controller
    var GroupListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceGroupList();
            });
        },
        
        enhanceGroupList: function() {
            var self = this;
            
            // Add group icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var groupData = $row.data('record');
                
                if (groupData) {
                    var icon = UserUtils.getGroupIcon(groupData.category);
                    var categoryClass = UserUtils.getGroupCategoryClass(groupData.category);
                    
                    // Add group icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' group-icon"></i>');
                    
                    // Add category badge
                    var $categoryCell = $row.find('td[data-field="category"]');
                    if ($categoryCell.length) {
                        $categoryCell.html('<span class="' + categoryClass + '">' + groupData.category + '</span>');
                    }
                }
            });
        }
    });

    // Preference List Controller
    var PreferenceListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhancePreferenceList();
            });
        },
        
        enhancePreferenceList: function() {
            var self = this;
            
            // Add preference icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var preferenceData = $row.data('record');
                
                if (preferenceData) {
                    var icon = UserUtils.getPreferenceIcon(preferenceData.category);
                    var iconClass = UserUtils.getPreferenceIconClass(preferenceData.category);
                    var valueClass = UserUtils.getPreferenceValueClass(preferenceData.value_type);
                    var typeClass = UserUtils.getPreferenceTypeClass(preferenceData.value_type);
                    
                    // Add preference icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' ' + iconClass + '"></i>');
                    
                    // Add value badge
                    var $valueCell = $row.find('td[data-field="value"]');
                    if ($valueCell.length) {
                        $valueCell.html('<span class="' + valueClass + '">' + preferenceData.value + '</span>');
                    }
                    
                    // Add type badge
                    var $typeCell = $row.find('td[data-field="value_type"]');
                    if ($typeCell.length) {
                        $typeCell.html('<span class="' + typeClass + '">' + preferenceData.value_type + '</span>');
                    }
                }
            });
        }
    });

    // User Analytics Dialog
    var UserAnalyticsDialog = Dialog.extend({
        template: 'users.UserAnalyticsDialog',
        
        init: function(parent, options) {
            this.options = options || {};
            this._super(parent, {
                title: _t('User Analytics'),
                size: 'large',
                buttons: [
                    {text: _t('Close'), close: true}
                ]
            });
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.loadUserAnalytics();
            });
        },
        
        loadUserAnalytics: function() {
            var self = this;
            
            rpc.query({
                model: 'res.users',
                method: 'get_user_analytics',
                args: []
            }).then(function(analytics) {
                self.$('.analytics-total-users').text(analytics.total_users);
                self.$('.analytics-active-users').text(analytics.active_users);
                self.$('.analytics-locked-users').text(analytics.locked_users);
                self.$('.analytics-inactive-users').text(analytics.inactive_users);
                self.$('.analytics-active-percentage').text(analytics.active_percentage.toFixed(1) + '%');
            });
        }
    });

    // Export utilities for use in other modules
    return {
        UserUtils: UserUtils,
        UserFormController: UserFormController,
        UserListController: UserListController,
        ActivityListController: ActivityListController,
        PermissionListController: PermissionListController,
        GroupListController: GroupListController,
        PreferenceListController: PreferenceListController,
        UserAnalyticsDialog: UserAnalyticsDialog
    };
});