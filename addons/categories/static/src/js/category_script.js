/* Kids Clothing ERP - Categories JavaScript */

ocean.define('categories.KidsClothingCategories', function (require) {
    'use strict';

    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    var _t = core._t;

    // Category Management Utilities
    var CategoryUtils = {
        getAgeGroupColor: function(ageGroup) {
            var colors = {
                'newborn': '#FFB6C1',  // Light Pink
                'infant': '#87CEEB',   // Sky Blue
                'toddler': '#98FB98',  // Pale Green
                'preschool': '#F0E68C', // Khaki
                'school': '#DDA0DD',   // Plum
                'teen': '#FFA07A'      // Light Salmon
            };
            return colors[ageGroup] || '#E0E0E0';
        },
        
        getSeasonColor: function(season) {
            var colors = {
                'summer': '#FFD700',   // Gold
                'winter': '#B0C4DE',   // Light Steel Blue
                'monsoon': '#32CD32',  // Lime Green
                'all_season': '#D3D3D3', // Light Gray
                'festive': '#FF6347',  // Tomato
                'party': '#DA70D6'     // Orchid
            };
            return colors[season] || '#E0E0E0';
        },
        
        getGenderIcon: function(gender) {
            var icons = {
                'boys': 'fa fa-male',
                'girls': 'fa fa-female',
                'unisex': 'fa fa-users',
                'all': 'fa fa-child'
            };
            return icons[gender] || 'fa fa-tag';
        },
        
        formatCategoryHierarchy: function(category) {
            var hierarchy = [];
            var current = category;
            
            while (current && current.parent_id) {
                hierarchy.unshift(current.parent_id.name);
                current = current.parent_id;
            }
            
            if (hierarchy.length > 0) {
                return hierarchy.join(' > ') + ' > ' + category.name;
            }
            return category.name;
        }
    };

    // Category Form Controller
    var CategoryFormController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_category_analyze': '_onAnalyzeCategory',
            'click .o_category_products': '_onViewProducts',
            'change .o_category_type': '_onCategoryTypeChange'
        }),

        _onAnalyzeCategory: function(ev) {
            ev.preventDefault();
            var self = this;
            var categoryId = this.model.get(this.handle).id;
            
            rpc.query({
                model: 'category.analytics',
                method: 'create',
                args: [{
                    name: 'Category Analysis',
                    category_id: categoryId,
                    date: new Date()
                }]
            }).then(function(result) {
                self.do_action({
                    type: 'ocean.actions.act_window',
                    res_model: 'category.analytics',
                    res_id: result,
                    view_mode: 'form',
                    target: 'current'
                });
            });
        },

        _onViewProducts: function(ev) {
            ev.preventDefault();
            var categoryId = this.model.get(this.handle).id;
            
            this.do_action({
                type: 'ocean.actions.act_window',
                res_model: 'product.template',
                view_mode: 'tree,form',
                domain: [['categ_id', '=', categoryId]],
                context: {'default_categ_id': categoryId}
            });
        },

        _onCategoryTypeChange: function(ev) {
            var categoryType = $(ev.currentTarget).val();
            var $form = this.$el;
            
            // Show/hide relevant fields based on category type
            if (categoryType === 'age_based') {
                $form.find('.o_age_group_field').show();
                $form.find('.o_gender_field').hide();
                $form.find('.o_season_field').hide();
            } else if (categoryType === 'gender') {
                $form.find('.o_age_group_field').hide();
                $form.find('.o_gender_field').show();
                $form.find('.o_season_field').hide();
            } else if (categoryType === 'seasonal') {
                $form.find('.o_age_group_field').hide();
                $form.find('.o_gender_field').hide();
                $form.find('.o_season_field').show();
            } else {
                $form.find('.o_age_group_field').hide();
                $form.find('.o_gender_field').hide();
                $form.find('.o_season_field').hide();
            }
        }
    });

    // Category List Controller
    var CategoryListController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .o_category_analyze': '_onAnalyzeCategory',
            'click .o_category_products': '_onViewProducts'
        }),

        _onAnalyzeCategory: function(ev) {
            ev.preventDefault();
            var self = this;
            var categoryId = $(ev.currentTarget).data('category-id');
            
            rpc.query({
                model: 'category.analytics',
                method: 'create',
                args: [{
                    name: 'Category Analysis',
                    category_id: categoryId,
                    date: new Date()
                }]
            }).then(function(result) {
                self.do_action({
                    type: 'ocean.actions.act_window',
                    res_model: 'category.analytics',
                    res_id: result,
                    view_mode: 'form',
                    target: 'current'
                });
            });
        },

        _onViewProducts: function(ev) {
            ev.preventDefault();
            var categoryId = $(ev.currentTarget).data('category-id');
            
            this.do_action({
                type: 'ocean.actions.act_window',
                res_model: 'product.template',
                view_mode: 'tree,form',
                domain: [['categ_id', '=', categoryId]],
                context: {'default_categ_id': categoryId}
            });
        }
    });

    // Category Analytics Controller
    var CategoryAnalyticsController = AbstractController.extend({
        events: _.extend({}, AbstractController.prototype.events, {
            'click .o_generate_report': '_onGenerateReport'
        }),

        _onGenerateReport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Generate Report'), _t('Do you want to generate a detailed analytics report?'), {
                confirm_callback: function() {
                    self._generateAnalyticsReport();
                }
            });
        },

        _generateAnalyticsReport: function() {
            var self = this;
            var analyticsId = this.model.get(this.handle).id;
            
            rpc.query({
                model: 'category.analytics',
                method: 'action_generate_report',
                args: [analyticsId]
            }).then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        }
    });

    return {
        CategoryFormController: CategoryFormController,
        CategoryListController: CategoryListController,
        CategoryAnalyticsController: CategoryAnalyticsController,
        CategoryUtils: CategoryUtils
    };
});