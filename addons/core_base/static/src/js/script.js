/* Kids Clothing ERP - Core Base JavaScript */

ocean.define('core_base.KidsClothingCore', function (require) {
    'use strict';

    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    var _t = core._t;

    // Age Group Utilities
    var AgeGroupUtils = {
        getAgeGroupFromMonths: function(months) {
            if (months <= 6) return 'newborn';
            if (months <= 12) return 'infant';
            if (months <= 36) return 'toddler';
            if (months <= 60) return 'preschool';
            if (months <= 144) return 'school';
            return 'teen';
        },
        
        getAgeGroupFromBirthDate: function(birthDate) {
            if (!birthDate) return 'newborn';
            
            var today = new Date();
            var birth = new Date(birthDate);
            var ageMonths = (today.getFullYear() - birth.getFullYear()) * 12 + 
                           (today.getMonth() - birth.getMonth());
            
            return this.getAgeGroupFromMonths(ageMonths);
        },
        
        getAgeGroupBadge: function(ageGroup) {
            var badges = {
                'newborn': '<span class="age-group-badge age-group-newborn">Newborn</span>',
                'infant': '<span class="age-group-badge age-group-infant">Infant</span>',
                'toddler': '<span class="age-group-badge age-group-toddler">Toddler</span>',
                'preschool': '<span class="age-group-badge age-group-preschool">Preschool</span>',
                'school': '<span class="age-group-badge age-group-school">School</span>',
                'teen': '<span class="age-group-badge age-group-teen">Teen</span>'
            };
            return badges[ageGroup] || '';
        }
    };

    // Gender Utilities
    var GenderUtils = {
        getGenderBadge: function(gender) {
            var badges = {
                'unisex': '<span class="gender-badge gender-unisex">Unisex</span>',
                'boys': '<span class="gender-badge gender-boys">Boys</span>',
                'girls': '<span class="gender-badge gender-girls">Girls</span>'
            };
            return badges[gender] || '';
        }
    };

    // Season Utilities
    var SeasonUtils = {
        getSeasonFromDate: function(date) {
            if (!date) date = new Date();
            var month = date.getMonth() + 1;
            
            if (month >= 3 && month <= 5) return 'summer';
            if (month >= 6 && month <= 9) return 'monsoon';
            return 'winter';
        },
        
        getSeasonBadge: function(season) {
            var badges = {
                'summer': '<span class="season-badge season-summer">Summer</span>',
                'winter': '<span class="season-badge season-winter">Winter</span>',
                'monsoon': '<span class="season-badge season-monsoon">Monsoon</span>',
                'all_season': '<span class="season-badge season-all-season">All Season</span>'
            };
            return badges[season] || '';
        }
    };

    // Price Utilities
    var PriceUtils = {
        formatCurrency: function(amount, currency = 'INR') {
            var symbols = {
                'INR': '₹',
                'USD': '$',
                'EUR': '€',
                'GBP': '£',
                'JPY': '¥'
            };
            var symbol = symbols[currency] || currency;
            return symbol + ' ' + amount.toLocaleString('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        
        calculateDiscount: function(listPrice, discountPercent) {
            var discountAmount = (listPrice * discountPercent) / 100;
            var finalPrice = listPrice - discountAmount;
            
            return {
                originalPrice: listPrice,
                discountPercent: discountPercent,
                discountAmount: discountAmount,
                finalPrice: finalPrice
            };
        },
        
        calculateMargin: function(listPrice, costPrice) {
            if (!listPrice || !costPrice) return 0;
            return ((listPrice - costPrice) / listPrice) * 100;
        }
    };

    // Stock Utilities
    var StockUtils = {
        getStockStatus: function(quantity, minQuantity = 0) {
            if (quantity <= 0) return 'out_of_stock';
            if (quantity <= minQuantity) return 'low_stock';
            return 'in_stock';
        },
        
        getStockBadge: function(status) {
            var badges = {
                'in_stock': '<span class="stock-status stock-in-stock">In Stock</span>',
                'low_stock': '<span class="stock-status stock-low-stock">Low Stock</span>',
                'out_of_stock': '<span class="stock-status stock-out-of-stock">Out of Stock</span>'
            };
            return badges[status] || '';
        }
    };

    // Validation Utilities
    var ValidationUtils = {
        validateGST: function(gstNumber) {
            if (!gstNumber || gstNumber.length !== 15) return false;
            if (!/^\d+$/.test(gstNumber)) return false;
            
            var stateCode = gstNumber.substring(0, 2);
            var panNumber = gstNumber.substring(2, 12);
            var entityNumber = gstNumber.substring(12, 13);
            var zCharacter = gstNumber.substring(13, 14);
            var checksum = gstNumber.substring(14, 15);
            
            // Validate state code (01-37)
            if (parseInt(stateCode) < 1 || parseInt(stateCode) > 37) return false;
            
            // Validate PAN format
            if (!/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(panNumber)) return false;
            
            return true;
        },
        
        validatePAN: function(panNumber) {
            if (!panNumber || panNumber.length !== 10) return false;
            return /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(panNumber);
        },
        
        validateMobile: function(mobileNumber) {
            if (!mobileNumber) return false;
            var clean = mobileNumber.replace(/\D/g, '');
            return clean.length === 10 && /^[6789]/.test(clean);
        },
        
        formatMobile: function(mobileNumber) {
            if (!mobileNumber) return '';
            var clean = mobileNumber.replace(/\D/g, '');
            if (clean.length === 10) return '+91' + clean;
            if (clean.length === 12 && clean.startsWith('91')) return '+' + clean;
            return mobileNumber;
        }
    };

    // Form Enhancements
    var FormEnhancements = {
        enhanceAgeGroupField: function(field) {
            if (!field) return;
            
            field.on('change', function() {
                var ageGroup = field.get_value();
                var badge = AgeGroupUtils.getAgeGroupBadge(ageGroup);
                field.$el.find('.age-group-display').html(badge);
            });
        },
        
        enhanceGenderField: function(field) {
            if (!field) return;
            
            field.on('change', function() {
                var gender = field.get_value();
                var badge = GenderUtils.getGenderBadge(gender);
                field.$el.find('.gender-display').html(badge);
            });
        },
        
        enhanceSeasonField: function(field) {
            if (!field) return;
            
            field.on('change', function() {
                var season = field.get_value();
                var badge = SeasonUtils.getSeasonBadge(season);
                field.$el.find('.season-display').html(badge);
            });
        },
        
        enhancePriceField: function(listPriceField, costPriceField, marginField) {
            if (!listPriceField || !costPriceField || !marginField) return;
            
            var updateMargin = function() {
                var listPrice = parseFloat(listPriceField.get_value()) || 0;
                var costPrice = parseFloat(costPriceField.get_value()) || 0;
                var margin = PriceUtils.calculateMargin(listPrice, costPrice);
                marginField.set_value(margin.toFixed(2) + '%');
            };
            
            listPriceField.on('change', updateMargin);
            costPriceField.on('change', updateMargin);
        }
    };

    // System Information Dialog
    var SystemInfoDialog = Dialog.extend({
        template: 'core_base.SystemInfoDialog',
        
        init: function(parent, options) {
            this.options = options || {};
            this._super(parent, {
                title: _t('System Information'),
                size: 'large',
                buttons: [
                    {text: _t('Close'), close: true}
                ]
            });
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.loadSystemInfo();
            });
        },
        
        loadSystemInfo: function() {
            var self = this;
            rpc.query({
                model: 'res.config.settings',
                method: 'get_system_info',
                args: []
            }).then(function(info) {
                self.$('.system-info-version').text(info.version);
                self.$('.system-info-modules').text(info.modules_installed);
                self.$('.system-info-users').text(info.users_count);
                self.$('.system-info-companies').text(info.companies_count);
            });
        }
    });

    // Configuration Form Controller
    var ConfigFormController = FormController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceConfigurationForm();
            });
        },
        
        enhanceConfigurationForm: function() {
            var self = this;
            
            // Add fade-in animation
            this.$el.addClass('fade-in');
            
            // Enhance form fields
            this._super();
        }
    });

    // List Controller Enhancements
    var ListControllerEnhancements = ListController.extend({
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.enhanceListView();
            });
        },
        
        enhanceListView: function() {
            var self = this;
            
            // Add age group badges to list view
            this.$('.o_list_view tbody tr').each(function() {
                var $row = $(this);
                var ageGroup = $row.find('td[data-field="age_group"]').text();
                if (ageGroup) {
                    var badge = AgeGroupUtils.getAgeGroupBadge(ageGroup);
                    $row.find('td[data-field="age_group"]').html(badge);
                }
            });
        }
    });

    // Export utilities for use in other modules
    return {
        AgeGroupUtils: AgeGroupUtils,
        GenderUtils: GenderUtils,
        SeasonUtils: SeasonUtils,
        PriceUtils: PriceUtils,
        StockUtils: StockUtils,
        ValidationUtils: ValidationUtils,
        FormEnhancements: FormEnhancements,
        SystemInfoDialog: SystemInfoDialog,
        ConfigFormController: ConfigFormController,
        ListControllerEnhancements: ListControllerEnhancements
    };
});

// System Information Dialog Template
ocean.define('core_base.SystemInfoDialog', function (require) {
    'use strict';
    
    return {
        template: 'core_base.SystemInfoDialog'
    };
});

// System Information Dialog Template
ocean.define('core_base.SystemInfoDialog', function (require) {
    'use strict';
    
    return {
        template: 'core_base.SystemInfoDialog'
    };
});