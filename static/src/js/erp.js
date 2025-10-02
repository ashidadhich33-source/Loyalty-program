/* Kids Clothing ERP JavaScript */

odoo.define('kids_clothing_erp.erp', function (require) {
    'use strict';

    var core = require('web.core');
    var FormView = require('web.FormView');
    var ListView = require('web.ListView');
    var KanbanView = require('web.KanbanView');
    var AbstractAction = require('web.AbstractAction');

    // Custom Dashboard Widget
    var KidsClothingDashboard = AbstractAction.extend({
        template: 'kids_clothing_erp.dashboard',
        
        start: function () {
            this._super.apply(this, arguments);
            this.load_dashboard_data();
        },
        
        load_dashboard_data: function () {
            var self = this;
            this._rpc({
                model: 'sale.order',
                method: 'get_dashboard_data',
            }).then(function (data) {
                self.$('.dashboard-stats').html(data.stats_html);
                self.$('.recent-orders').html(data.orders_html);
            });
        }
    });

    // Custom Form View for Kids Clothing
    var KidsClothingFormView = FormView.extend({
        events: _.extend({}, FormView.prototype.events, {
            'change .kids-clothing-checkbox': 'on_kids_clothing_change',
            'change .child-age-input': 'on_child_age_change',
        }),
        
        on_kids_clothing_change: function (event) {
            var $checkbox = $(event.currentTarget);
            var is_checked = $checkbox.is(':checked');
            this.$('.kids-clothing-fields').toggle(is_checked);
            
            if (is_checked) {
                this.$('.kids-clothing-fields').addClass('fade-in-up');
            }
        },
        
        on_child_age_change: function (event) {
            var age = parseInt($(event.currentTarget).val());
            var $size_field = this.$('.child-size-field');
            
            if (age >= 2 && age <= 4) {
                $size_field.find('option[value="xs"]').prop('selected', true);
            } else if (age >= 4 && age <= 6) {
                $size_field.find('option[value="s"]').prop('selected', true);
            } else if (age >= 6 && age <= 8) {
                $size_field.find('option[value="m"]').prop('selected', true);
            } else if (age >= 8 && age <= 10) {
                $size_field.find('option[value="l"]').prop('selected', true);
            } else if (age >= 10 && age <= 12) {
                $size_field.find('option[value="xl"]').prop('selected', true);
            }
        }
    });

    // Custom List View for Kids Clothing
    var KidsClothingListView = ListView.extend({
        events: _.extend({}, ListView.prototype.events, {
            'click .loyalty-points-btn': 'on_loyalty_points_click',
            'click .age-range-filter': 'on_age_range_filter',
        }),
        
        on_loyalty_points_click: function (event) {
            event.preventDefault();
            var $btn = $(event.currentTarget);
            var partner_id = $btn.data('partner-id');
            
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'Loyalty Points History',
                res_model: 'loyalty.points.history',
                view_mode: 'tree,form',
                domain: [('partner_id', '=', partner_id)],
                context: {'default_partner_id': partner_id},
            });
        },
        
        on_age_range_filter: function (event) {
            event.preventDefault();
            var $btn = $(event.currentTarget);
            var age_range = $btn.data('age-range');
            
            this.trigger_up('search', {
                domain: [('child_age', '>=', age_range.split('-')[0]), 
                        ('child_age', '<=', age_range.split('-')[1])],
            });
        }
    });

    // Custom Kanban View for Products
    var KidsClothingKanbanView = KanbanView.extend({
        events: _.extend({}, KanbanView.prototype.events, {
            'click .product-image': 'on_product_image_click',
            'click .size-variant': 'on_size_variant_click',
            'click .color-variant': 'on_color_variant_click',
        }),
        
        on_product_image_click: function (event) {
            event.preventDefault();
            var $card = $(event.currentTarget).closest('.oe_kanban_card');
            var product_id = $card.data('id');
            
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'Product Details',
                res_model: 'product.template',
                res_id: product_id,
                view_mode: 'form',
                views: [[false, 'form']],
            });
        },
        
        on_size_variant_click: function (event) {
            event.preventDefault();
            var $btn = $(event.currentTarget);
            var size = $btn.data('size');
            var $card = $btn.closest('.oe_kanban_card');
            
            // Update size selection
            $card.find('.size-variant').removeClass('selected');
            $btn.addClass('selected');
            
            // Update product variant
            this._rpc({
                model: 'product.template',
                method: 'get_variant_by_size',
                args: [$card.data('id'), size],
            }).then(function (variant_id) {
                if (variant_id) {
                    $card.find('.product-variant-id').val(variant_id);
                }
            });
        },
        
        on_color_variant_click: function (event) {
            event.preventDefault();
            var $btn = $(event.currentTarget);
            var color = $btn.data('color');
            var $card = $btn.closest('.oe_kanban_card');
            
            // Update color selection
            $card.find('.color-variant').removeClass('selected');
            $btn.addClass('selected');
            
            // Update product image
            var image_url = $btn.data('image-url');
            if (image_url) {
                $card.find('.product-image').attr('src', image_url);
            }
        }
    });

    // Custom POS Widget
    var KidsClothingPOS = AbstractAction.extend({
        template: 'kids_clothing_erp.pos',
        
        start: function () {
            this._super.apply(this, arguments);
            this.init_pos_interface();
        },
        
        init_pos_interface: function () {
            var self = this;
            
            // Initialize product grid
            this.load_products();
            
            // Initialize customer search
            this.init_customer_search();
            
            // Initialize loyalty points
            this.init_loyalty_points();
        },
        
        load_products: function () {
            var self = this;
            this._rpc({
                model: 'product.template',
                method: 'search_read',
                args: [[('is_kids_clothing', '=', true)]],
                kwargs: {
                    fields: ['name', 'list_price', 'image_128', 'age_range', 'gender', 'size_variants'],
                }
            }).then(function (products) {
                self.render_products(products);
            });
        },
        
        render_products: function (products) {
            var $container = this.$('.products-grid');
            $container.empty();
            
            _.each(products, function (product) {
                var $product = $('<div class="product-card">');
                $product.html(
                    '<div class="product-image">' +
                        '<img src="' + (product.image_128 || '/web/static/src/img/placeholder.png') + '" alt="' + product.name + '">' +
                    '</div>' +
                    '<div class="product-info">' +
                        '<h4>' + product.name + '</h4>' +
                        '<p class="price">$' + product.list_price + '</p>' +
                        '<div class="age-range">' + product.age_range + '</div>' +
                        '<div class="gender">' + product.gender + '</div>' +
                    '</div>'
                );
                $container.append($product);
            });
        },
        
        init_customer_search: function () {
            var self = this;
            this.$('.customer-search').on('input', function () {
                var query = $(this).val();
                if (query.length >= 2) {
                    self.search_customers(query);
                }
            });
        },
        
        search_customers: function (query) {
            var self = this;
            this._rpc({
                model: 'res.partner',
                method: 'name_search',
                args: [query],
                kwargs: {
                    args: [('is_kids_clothing_customer', '=', true)],
                    limit: 10,
                }
            }).then(function (customers) {
                self.render_customer_suggestions(customers);
            });
        },
        
        render_customer_suggestions: function (customers) {
            var $suggestions = this.$('.customer-suggestions');
            $suggestions.empty();
            
            _.each(customers, function (customer) {
                var $suggestion = $('<div class="customer-suggestion">');
                $suggestion.html(
                    '<div class="customer-name">' + customer[1] + '</div>' +
                    '<div class="customer-info">' + customer[0] + '</div>'
                );
                $suggestions.append($suggestion);
            });
        },
        
        init_loyalty_points: function () {
            var self = this;
            this.$('.loyalty-points-input').on('change', function () {
                var points = parseInt($(this).val()) || 0;
                var discount = Math.floor(points / 100); // 1 dollar discount per 100 points
                self.$('.loyalty-discount').text('-$' + discount);
            });
        }
    });

    // Register views
    core.view_registry.add('kids_clothing_form', KidsClothingFormView);
    core.view_registry.add('kids_clothing_list', KidsClothingListView);
    core.view_registry.add('kids_clothing_kanban', KidsClothingKanbanView);
    core.action_registry.add('kids_clothing_dashboard', KidsClothingDashboard);
    core.action_registry.add('kids_clothing_pos', KidsClothingPOS);

    return {
        KidsClothingDashboard: KidsClothingDashboard,
        KidsClothingFormView: KidsClothingFormView,
        KidsClothingListView: KidsClothingListView,
        KidsClothingKanbanView: KidsClothingKanbanView,
        KidsClothingPOS: KidsClothingPOS,
    };
});