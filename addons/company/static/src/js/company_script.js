/* Kids Clothing ERP - Company Script */

ocean.define('company.KidsClothingCompany', function (require) {
    'use strict';

    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    var _t = core._t;

    // Company Management Utilities
    var CompanyUtils = {
        // Company Status Management
        getCompanyStatus: function(company) {
            if (!company.is_active) return 'inactive';
            if (company.is_default) return 'default';
            if (company.gst_status === 'registered') return 'gst_registered';
            if (company.gst_status === 'unregistered') return 'gst_unregistered';
            if (company.gst_status === 'cancelled') return 'gst_cancelled';
            if (company.gst_status === 'suspended') return 'gst_suspended';
            return 'active';
        },
        
        getCompanyStatusBadge: function(status) {
            var badges = {
                'active': '<span class="company-status company-status-active">Active</span>',
                'inactive': '<span class="company-status company-status-inactive">Inactive</span>',
                'default': '<span class="company-status company-status-default">Default</span>',
                'gst_registered': '<span class="company-status company-status-gst-registered">GST Registered</span>',
                'gst_unregistered': '<span class="company-status company-status-gst-unregistered">GST Unregistered</span>',
                'gst_cancelled': '<span class="company-status company-status-gst-cancelled">GST Cancelled</span>',
                'gst_suspended': '<span class="company-status company-status-gst-suspended">GST Suspended</span>'
            };
            return badges[status] || '';
        },
        
        // Branch Management
        getBranchIcon: function(branchType) {
            var icons = {
                'head_office': 'fa-building',
                'regional_office': 'fa-city',
                'branch_office': 'fa-store',
                'warehouse': 'fa-warehouse',
                'showroom': 'fa-shopping-bag',
                'franchise': 'fa-handshake',
                'distributor': 'fa-truck'
            };
            return icons[branchType] || 'fa-building';
        },
        
        getBranchTypeClass: function(branchType) {
            var classes = {
                'head_office': 'branch-type',
                'regional_office': 'branch-type',
                'branch_office': 'branch-type',
                'warehouse': 'branch-type',
                'showroom': 'branch-type',
                'franchise': 'branch-type',
                'distributor': 'branch-type'
            };
            return classes[branchType] || 'branch-type';
        },
        
        // Location Management
        getLocationIcon: function(locationType) {
            var icons = {
                'warehouse': 'fa-warehouse',
                'showroom': 'fa-store',
                'office': 'fa-building',
                'storage': 'fa-archive',
                'retail': 'fa-shopping-cart',
                'wholesale': 'fa-truck',
                'franchise': 'fa-handshake',
                'distribution': 'fa-shipping-fast',
                'manufacturing': 'fa-industry',
                'other': 'fa-map-marker-alt'
            };
            return icons[locationType] || 'fa-map-marker-alt';
        },
        
        getLocationTypeClass: function(locationType) {
            var classes = {
                'warehouse': 'location-type',
                'showroom': 'location-type',
                'office': 'location-type',
                'storage': 'location-type',
                'retail': 'location-type',
                'wholesale': 'location-type',
                'franchise': 'location-type',
                'distribution': 'location-type',
                'manufacturing': 'location-type',
                'other': 'location-type'
            };
            return classes[locationType] || 'location-type';
        },
        
        // Financial Year Management
        getFinancialYearIcon: function(state) {
            var icons = {
                'draft': 'fa-edit',
                'active': 'fa-play',
                'closed': 'fa-check',
                'cancelled': 'fa-times'
            };
            return icons[state] || 'fa-calendar';
        },
        
        getFinancialYearStateClass: function(state) {
            var classes = {
                'draft': 'financial-year-state-draft',
                'active': 'financial-year-state-active',
                'closed': 'financial-year-state-closed',
                'cancelled': 'financial-year-state-cancelled'
            };
            return classes[state] || 'financial-year-state-draft';
        },
        
        formatFinancialYearDates: function(dateStart, dateEnd) {
            if (!dateStart || !dateEnd) return '';
            
            var start = new Date(dateStart);
            var end = new Date(dateEnd);
            
            return start.getFullYear() + '-' + end.getFullYear();
        },
        
        // Company Settings Management
        getSettingIcon: function(category) {
            var icons = {
                'general': 'fa-cog',
                'financial': 'fa-calculator',
                'inventory': 'fa-boxes',
                'sales': 'fa-shopping-cart',
                'purchase': 'fa-shopping-bag',
                'hr': 'fa-users',
                'pos': 'fa-cash-register',
                'ecommerce': 'fa-shopping-cart',
                'integration': 'fa-plug',
                'security': 'fa-shield-alt',
                'custom': 'fa-wrench'
            };
            return icons[category] || 'fa-cog';
        },
        
        getSettingIconClass: function(category) {
            var classes = {
                'general': 'company-setting-icon-general',
                'financial': 'company-setting-icon-financial',
                'inventory': 'company-setting-icon-inventory',
                'sales': 'company-setting-icon-sales',
                'purchase': 'company-setting-icon-purchase',
                'hr': 'company-setting-icon-hr',
                'pos': 'company-setting-icon-pos',
                'ecommerce': 'company-setting-icon-ecommerce',
                'integration': 'company-setting-icon-integration',
                'security': 'company-setting-icon-security',
                'custom': 'company-setting-icon-custom'
            };
            return classes[category] || 'company-setting-icon-custom';
        },
        
        getSettingValueClass: function(valueType) {
            var classes = {
                'string': 'company-setting-value',
                'integer': 'company-setting-value',
                'float': 'company-setting-value',
                'boolean': 'company-setting-value',
                'json': 'company-setting-value',
                'date': 'company-setting-value',
                'datetime': 'company-setting-value'
            };
            return classes[valueType] || 'company-setting-value';
        },
        
        getSettingTypeClass: function(valueType) {
            var classes = {
                'string': 'company-setting-type',
                'integer': 'company-setting-type',
                'float': 'company-setting-type',
                'boolean': 'company-setting-type',
                'json': 'company-setting-type',
                'date': 'company-setting-type',
                'datetime': 'company-setting-type'
            };
            return classes[valueType] || 'company-setting-type';
        },
        
        getSettingCategoryClass: function(category) {
            var classes = {
                'general': 'company-setting-category',
                'financial': 'company-setting-category',
                'inventory': 'company-setting-category',
                'sales': 'company-setting-category',
                'purchase': 'company-setting-category',
                'hr': 'company-setting-category',
                'pos': 'company-setting-category',
                'ecommerce': 'company-setting-category',
                'integration': 'company-setting-category',
                'security': 'company-setting-category',
                'custom': 'company-setting-category'
            };
            return classes[category] || 'company-setting-category';
        },
        
        getSettingScopeClass: function(scope) {
            var classes = {
                'company': 'company-setting-scope',
                'branch': 'company-setting-scope',
                'location': 'company-setting-scope',
                'user': 'company-setting-scope'
            };
            return classes[scope] || 'company-setting-scope';
        }
    };

    // Company Form Controller
    var CompanyFormController = FormController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceCompanyForm();
            });
        },
        
        enhanceCompanyForm: function() {
            var self = this;
            
            // Add fade-in animation
            this.$el.addClass('fade-in-up');
            
            // Enhance company status display
            this._super();
        },
        
        _onButtonClicked: function(event) {
            var self = this;
            var $target = $(event.currentTarget);
            var action = $target.data('action');
            
            if (action === 'activate') {
                self._handleCompanyActivation();
            } else if (action === 'deactivate') {
                self._handleCompanyDeactivation();
            } else if (action === 'set_default') {
                self._handleSetDefault();
            } else if (action === 'validate_gstin') {
                self._handleGSTINValidation();
            } else if (action === 'generate_gstin') {
                self._handleGSTINGeneration();
            } else {
                this._super(event);
            }
        },
        
        _handleCompanyActivation: function() {
            var self = this;
            var company = this.model.get(this.handle);
            
            rpc.query({
                model: 'res.company',
                method: 'action_activate',
                args: [company.id],
            }).then(function(result) {
                if (result) {
                    self._showNotification('Company activated successfully', 'success');
                    self.reload();
                }
            });
        },
        
        _handleCompanyDeactivation: function() {
            var self = this;
            var company = this.model.get(this.handle);
            
            Dialog.confirm(this, _t('Are you sure you want to deactivate this company?'), {
                title: _t('Deactivate Company'),
                confirm_callback: function() {
                    rpc.query({
                        model: 'res.company',
                        method: 'action_deactivate',
                        args: [company.id],
                    }).then(function(result) {
                        if (result) {
                            self._showNotification('Company deactivated successfully', 'success');
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _handleSetDefault: function() {
            var self = this;
            var company = this.model.get(this.handle);
            
            Dialog.confirm(this, _t('Are you sure you want to set this company as default?'), {
                title: _t('Set Default Company'),
                confirm_callback: function() {
                    rpc.query({
                        model: 'res.company',
                        method: 'action_set_default',
                        args: [company.id],
                    }).then(function(result) {
                        if (result) {
                            self._showNotification('Company set as default successfully', 'success');
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _handleGSTINValidation: function() {
            var self = this;
            var company = this.model.get(this.handle);
            
            rpc.query({
                model: 'res.company',
                method: 'action_validate_gstin',
                args: [company.id],
            }).then(function(result) {
                if (result) {
                    self._showNotification('GSTIN validated successfully', 'success');
                }
            }).catch(function(error) {
                self._showNotification('GSTIN validation failed: ' + error.message, 'error');
            });
        },
        
        _handleGSTINGeneration: function() {
            var self = this;
            var company = this.model.get(this.handle);
            
            rpc.query({
                model: 'res.company',
                method: 'action_generate_gstin',
                args: [company.id],
            }).then(function(result) {
                if (result) {
                    self._showNotification('GSTIN generated successfully', 'success');
                    self.reload();
                }
            }).catch(function(error) {
                self._showNotification('GSTIN generation failed: ' + error.message, 'error');
            });
        },
        
        _showNotification: function(message, type) {
            // This would integrate with the notification system
            console.log(type + ': ' + message);
        }
    });

    // Company List Controller
    var CompanyListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceCompanyList();
            });
        },
        
        enhanceCompanyList: function() {
            var self = this;
            
            // Add company status badges
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var companyData = $row.data('record');
                
                if (companyData) {
                    var status = CompanyUtils.getCompanyStatus(companyData);
                    var badge = CompanyUtils.getCompanyStatusBadge(status);
                    
                    // Add status badge to the row
                    $row.find('td:first').append(badge);
                }
            });
        }
    });

    // Branch List Controller
    var BranchListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceBranchList();
            });
        },
        
        enhanceBranchList: function() {
            var self = this;
            
            // Add branch icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var branchData = $row.data('record');
                
                if (branchData) {
                    var icon = CompanyUtils.getBranchIcon(branchData.branch_type);
                    var typeClass = CompanyUtils.getBranchTypeClass(branchData.branch_type);
                    
                    // Add branch icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' branch-icon"></i>');
                    
                    // Add branch type badge
                    var $typeCell = $row.find('td[data-field="branch_type"]');
                    if ($typeCell.length) {
                        $typeCell.html('<span class="' + typeClass + '">' + branchData.branch_type + '</span>');
                    }
                }
            });
        }
    });

    // Location List Controller
    var LocationListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceLocationList();
            });
        },
        
        enhanceLocationList: function() {
            var self = this;
            
            // Add location icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var locationData = $row.data('record');
                
                if (locationData) {
                    var icon = CompanyUtils.getLocationIcon(locationData.location_type);
                    var typeClass = CompanyUtils.getLocationTypeClass(locationData.location_type);
                    
                    // Add location icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' location-icon"></i>');
                    
                    // Add location type badge
                    var $typeCell = $row.find('td[data-field="location_type"]');
                    if ($typeCell.length) {
                        $typeCell.html('<span class="' + typeClass + '">' + locationData.location_type + '</span>');
                    }
                }
            });
        }
    });

    // Financial Year List Controller
    var FinancialYearListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceFinancialYearList();
            });
        },
        
        enhanceFinancialYearList: function() {
            var self = this;
            
            // Add financial year icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var fyData = $row.data('record');
                
                if (fyData) {
                    var icon = CompanyUtils.getFinancialYearIcon(fyData.state);
                    var stateClass = CompanyUtils.getFinancialYearStateClass(fyData.state);
                    
                    // Add financial year icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' financial-year-icon"></i>');
                    
                    // Add state badge
                    var $stateCell = $row.find('td[data-field="state"]');
                    if ($stateCell.length) {
                        $stateCell.html('<span class="' + stateClass + '">' + fyData.state + '</span>');
                    }
                    
                    // Format dates
                    var $datesCell = $row.find('td[data-field="date_start"]');
                    if ($datesCell.length) {
                        var formattedDates = CompanyUtils.formatFinancialYearDates(fyData.date_start, fyData.date_end);
                        $datesCell.text(formattedDates);
                    }
                }
            });
        }
    });

    // Company Settings List Controller
    var CompanySettingsListController = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceCompanySettingsList();
            });
        },
        
        enhanceCompanySettingsList: function() {
            var self = this;
            
            // Add company settings icons and formatting
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var settingData = $row.data('record');
                
                if (settingData) {
                    var icon = CompanyUtils.getSettingIcon(settingData.category);
                    var iconClass = CompanyUtils.getSettingIconClass(settingData.category);
                    var valueClass = CompanyUtils.getSettingValueClass(settingData.value_type);
                    var typeClass = CompanyUtils.getSettingTypeClass(settingData.value_type);
                    var categoryClass = CompanyUtils.getSettingCategoryClass(settingData.category);
                    var scopeClass = CompanyUtils.getSettingScopeClass(settingData.scope);
                    
                    // Add setting icon
                    var $iconCell = $row.find('td:first');
                    $iconCell.html('<i class="fa ' + icon + ' ' + iconClass + '"></i>');
                    
                    // Add value badge
                    var $valueCell = $row.find('td[data-field="value"]');
                    if ($valueCell.length) {
                        $valueCell.html('<span class="' + valueClass + '">' + settingData.value + '</span>');
                    }
                    
                    // Add type badge
                    var $typeCell = $row.find('td[data-field="value_type"]');
                    if ($typeCell.length) {
                        $typeCell.html('<span class="' + typeClass + '">' + settingData.value_type + '</span>');
                    }
                    
                    // Add category badge
                    var $categoryCell = $row.find('td[data-field="category"]');
                    if ($categoryCell.length) {
                        $categoryCell.html('<span class="' + categoryClass + '">' + settingData.category + '</span>');
                    }
                    
                    // Add scope badge
                    var $scopeCell = $row.find('td[data-field="scope"]');
                    if ($scopeCell.length) {
                        $scopeCell.html('<span class="' + scopeClass + '">' + settingData.scope + '</span>');
                    }
                }
            });
        }
    });

    // Company Analytics Dialog
    var CompanyAnalyticsDialog = Dialog.extend({
        template: 'company.CompanyAnalyticsDialog',
        
        init: function(parent, options) {
            this.options = options || {};
            this._super(parent, {
                title: _t('Company Analytics'),
                size: 'large',
                buttons: [
                    {text: _t('Close'), close: true}
                ]
            });
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.loadCompanyAnalytics();
            });
        },
        
        loadCompanyAnalytics: function() {
            var self = this;
            
            rpc.query({
                model: 'res.company',
                method: 'get_company_analytics',
                args: []
            }).then(function(analytics) {
                self.$('.analytics-total-users').text(analytics.total_users);
                self.$('.analytics-active-users').text(analytics.active_users);
                self.$('.analytics-total-branches').text(analytics.total_branches);
                self.$('.analytics-total-locations').text(analytics.total_locations);
                self.$('.analytics-company-type').text(analytics.company_type);
                self.$('.analytics-business-nature').text(analytics.business_nature);
                self.$('.analytics-gst-status').text(analytics.gst_status);
                self.$('.analytics-is-active').text(analytics.is_active ? 'Yes' : 'No');
                self.$('.analytics-is-default').text(analytics.is_default ? 'Yes' : 'No');
            });
        }
    });

    // GST Configuration Dialog
    var GSTConfigurationDialog = Dialog.extend({
        template: 'company.GSTConfigurationDialog',
        
        init: function(parent, options) {
            this.options = options || {};
            this._super(parent, {
                title: _t('GST Configuration'),
                size: 'medium',
                buttons: [
                    {text: _t('Save'), click: this._onSave.bind(this)},
                    {text: _t('Cancel'), close: true}
                ]
            });
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.loadGSTConfiguration();
            });
        },
        
        loadGSTConfiguration: function() {
            // Load current GST configuration
            this.$('.gst-configuration-form').show();
        },
        
        _onSave: function() {
            var self = this;
            var gstData = {
                gstin: this.$('.gst-configuration-form input[name="gstin"]').val(),
                gst_status: this.$('.gst-configuration-form select[name="gst_status"]').val(),
                enable_gst: this.$('.gst-configuration-form input[name="enable_gst"]').is(':checked'),
                enable_e_invoice: this.$('.gst-configuration-form input[name="enable_e_invoice"]').is(':checked'),
                enable_e_way_bill: this.$('.gst-configuration-form input[name="enable_e_way_bill"]').is(':checked'),
            };
            
            rpc.query({
                model: 'res.company',
                method: 'write',
                args: [this.options.company_id, gstData],
            }).then(function(result) {
                if (result) {
                    self._showNotification('GST configuration saved successfully', 'success');
                    self.close();
                }
            }).catch(function(error) {
                self._showNotification('GST configuration save failed: ' + error.message, 'error');
            });
        },
        
        _showNotification: function(message, type) {
            // This would integrate with the notification system
            console.log(type + ': ' + message);
        }
    });

    // Multi-Company Dialog
    var MultiCompanyDialog = Dialog.extend({
        template: 'company.MultiCompanyDialog',
        
        init: function(parent, options) {
            this.options = options || {};
            this._super(parent, {
                title: _t('Multi-Company Management'),
                size: 'large',
                buttons: [
                    {text: _t('Close'), close: true}
                ]
            });
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.loadMultiCompanyData();
            });
        },
        
        loadMultiCompanyData: function() {
            var self = this;
            
            rpc.query({
                model: 'res.company',
                method: 'search_read',
                args: [[('is_active', '=', True)]],
                kwargs: {
                    fields: ['name', 'company_type', 'business_nature', 'gst_status', 'total_users', 'active_users']
                }
            }).then(function(companies) {
                self.renderCompanies(companies);
            });
        },
        
        renderCompanies: function(companies) {
            var self = this;
            var $container = this.$('.multi-company-grid');
            
            companies.forEach(function(company) {
                var $card = $('<div class="multi-company-card">');
                $card.html(`
                    <div class="multi-company-card-header">
                        <div class="multi-company-card-logo"></div>
                        <div class="multi-company-card-info">
                            <h3>${company.name}</h3>
                            <p>${company.company_type} - ${company.business_nature}</p>
                        </div>
                    </div>
                    <div class="multi-company-card-stats">
                        <div class="multi-company-card-stat">
                            <div class="multi-company-card-stat-value">${company.total_users}</div>
                            <div class="multi-company-card-stat-label">Total Users</div>
                        </div>
                        <div class="multi-company-card-stat">
                            <div class="multi-company-card-stat-value">${company.active_users}</div>
                            <div class="multi-company-card-stat-label">Active Users</div>
                        </div>
                    </div>
                `);
                $container.append($card);
            });
        }
    });

    // Export utilities for use in other modules
    return {
        CompanyUtils: CompanyUtils,
        CompanyFormController: CompanyFormController,
        CompanyListController: CompanyListController,
        BranchListController: BranchListController,
        LocationListController: LocationListController,
        FinancialYearListController: FinancialYearListController,
        CompanySettingsListController: CompanySettingsListController,
        CompanyAnalyticsDialog: CompanyAnalyticsDialog,
        GSTConfigurationDialog: GSTConfigurationDialog,
        MultiCompanyDialog: MultiCompanyDialog
    };
});