/* Kids Clothing ERP - Sales JavaScript */

ocean.define('sales.KidsClothingSales', function (require) {
    'use strict';

    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    var _t = core._t;

    // Sales Utilities
    var SalesUtils = {
        formatCurrency: function(amount) {
            return '₹' + parseFloat(amount).toFixed(2);
        },
        
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
        
        getGenderIcon: function(gender) {
            var icons = {
                'boys': 'fa fa-male',
                'girls': 'fa fa-female',
                'unisex': 'fa fa-users',
                'all': 'fa fa-child'
            };
            return icons[gender] || 'fa fa-tag';
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
        
        calculateDiscount: function(amount, discountType, discountValue) {
            if (discountType === 'percentage') {
                return amount * (discountValue / 100);
            } else if (discountType === 'fixed') {
                return discountValue;
            }
            return 0;
        },
        
        calculateTax: function(amount, taxRate) {
            return amount * (taxRate / 100);
        }
    };

    // Sales Order Controller
    var SalesOrderController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_send_quotation': '_onSendQuotation',
            'click .o_confirm_order': '_onConfirmOrder',
            'click .o_mark_done': '_onMarkDone',
            'click .o_cancel_order': '_onCancelOrder',
            'click .o_reset_draft': '_onResetDraft',
            'change .o_discount_type': '_onDiscountTypeChange',
            'change .o_discount_value': '_onDiscountValueChange',
            'click .o_add_product': '_onAddProduct',
            'click .o_remove_product': '_onRemoveProduct'
        }),

        _onSendQuotation: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Send Quotation'), _t('Are you sure you want to send this quotation to the customer?'), {
                confirm_callback: function() {
                    self.model.call('action_quotation_send').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onConfirmOrder: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Confirm Order'), _t('Are you sure you want to confirm this quotation to a sales order?'), {
                confirm_callback: function() {
                    self.model.call('action_confirm').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onMarkDone: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Mark as Done'), _t('Are you sure you want to mark this order as done?'), {
                confirm_callback: function() {
                    self.model.call('action_done').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onCancelOrder: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Cancel Order'), _t('Are you sure you want to cancel this order?'), {
                confirm_callback: function() {
                    self.model.call('action_cancel').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onResetDraft: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Reset to Draft'), _t('Are you sure you want to reset this order to draft?'), {
                confirm_callback: function() {
                    self.model.call('action_draft').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onDiscountTypeChange: function(ev) {
            var discountType = $(ev.currentTarget).val();
            var $form = this.$el;
            
            // Show/hide relevant discount fields
            if (discountType === 'percentage') {
                $form.find('.o_discount_percentage_field').show();
                $form.find('.o_discount_amount_field').hide();
            } else if (discountType === 'fixed') {
                $form.find('.o_discount_percentage_field').hide();
                $form.find('.o_discount_amount_field').show();
            } else {
                $form.find('.o_discount_percentage_field').hide();
                $form.find('.o_discount_amount_field').hide();
            }
        },

        _onDiscountValueChange: function(ev) {
            var self = this;
            var discountType = this.model.get('discount_type');
            var discountValue = parseFloat($(ev.currentTarget).val()) || 0;
            
            // Calculate and update amounts
            self._updateOrderAmounts(discountType, discountValue);
        },

        _onAddProduct: function(ev) {
            ev.preventDefault();
            var self = this;
            
            // Open product selection dialog
            self.do_action({
                type: 'ocean.actions.act_window',
                res_model: 'product.template',
                view_mode: 'tree,form',
                target: 'new',
                context: {
                    'default_order_id': self.model.get('id')
                }
            });
        },

        _onRemoveProduct: function(ev) {
            ev.preventDefault();
            var self = this;
            var productId = $(ev.currentTarget).data('product-id');
            
            Dialog.confirm(this, _t('Remove Product'), _t('Are you sure you want to remove this product from the order?'), {
                confirm_callback: function() {
                    // Remove product from order
                    self.model.call('remove_product', [productId]).then(function() {
                        self.render();
                    });
                }
            });
        },

        _updateOrderAmounts: function(discountType, discountValue) {
            var self = this;
            var orderLines = this.model.get('order_line_ids');
            var totalAmount = 0;
            
            // Calculate total from order lines
            for (var i = 0; i < orderLines.length; i++) {
                totalAmount += orderLines[i].price_subtotal;
            }
            
            // Apply discount
            var discountAmount = SalesUtils.calculateDiscount(totalAmount, discountType, discountValue);
            var discountedAmount = totalAmount - discountAmount;
            
            // Calculate tax
            var taxAmount = SalesUtils.calculateTax(discountedAmount, 18); // 18% GST
            var totalAmount = discountedAmount + taxAmount;
            
            // Update model
            this.model.set('amount_untaxed', discountedAmount);
            this.model.set('amount_tax', taxAmount);
            this.model.set('amount_total', totalAmount);
        }
    });

    // Sales Delivery Controller
    var SalesDeliveryController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_confirm_delivery': '_onConfirmDelivery',
            'click .o_ship_delivery': '_onShipDelivery',
            'click .o_deliver_delivery': '_onDeliverDelivery',
            'click .o_fail_delivery': '_onFailDelivery',
            'click .o_retry_delivery': '_onRetryDelivery',
            'click .o_cancel_delivery': '_onCancelDelivery',
            'click .o_track_delivery': '_onTrackDelivery',
            'click .o_schedule_delivery': '_onScheduleDelivery'
        }),

        _onConfirmDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Confirm Delivery'), _t('Are you sure you want to confirm this delivery?'), {
                confirm_callback: function() {
                    self.model.call('action_confirm').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onShipDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Ship Delivery'), _t('Are you sure you want to mark this delivery as shipped?'), {
                confirm_callback: function() {
                    self.model.call('action_ship').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onDeliverDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Deliver'), _t('Are you sure you want to mark this delivery as delivered?'), {
                confirm_callback: function() {
                    self.model.call('action_deliver').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onFailDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Mark as Failed'), _t('Are you sure you want to mark this delivery as failed?'), {
                confirm_callback: function() {
                    self.model.call('action_fail').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onRetryDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Retry Delivery'), _t('Are you sure you want to retry this delivery?'), {
                confirm_callback: function() {
                    self.model.call('action_retry').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onCancelDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Cancel Delivery'), _t('Are you sure you want to cancel this delivery?'), {
                confirm_callback: function() {
                    self.model.call('action_cancel').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onTrackDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_track_delivery').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },

        _onScheduleDelivery: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_schedule_delivery').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        }
    });

    // Sales Return Controller
    var SalesReturnController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_confirm_return': '_onConfirmReturn',
            'click .o_receive_return': '_onReceiveReturn',
            'click .o_process_return': '_onProcessReturn',
            'click .o_refund_return': '_onRefundReturn',
            'click .o_exchange_return': '_onExchangeReturn',
            'click .o_reject_return': '_onRejectReturn',
            'click .o_cancel_return': '_onCancelReturn',
            'click .o_create_exchange': '_onCreateExchange'
        }),

        _onConfirmReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Confirm Return'), _t('Are you sure you want to confirm this return?'), {
                confirm_callback: function() {
                    self.model.call('action_confirm').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onReceiveReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Receive Return'), _t('Are you sure you want to mark this return as received?'), {
                confirm_callback: function() {
                    self.model.call('action_receive').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onProcessReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Process Return'), _t('Are you sure you want to process this return?'), {
                confirm_callback: function() {
                    self.model.call('action_process').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onRefundReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Process Refund'), _t('Are you sure you want to process the refund for this return?'), {
                confirm_callback: function() {
                    self.model.call('action_refund').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onExchangeReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Process Exchange'), _t('Are you sure you want to process the exchange for this return?'), {
                confirm_callback: function() {
                    self.model.call('action_exchange').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onRejectReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Reject Return'), _t('Are you sure you want to reject this return?'), {
                confirm_callback: function() {
                    self.model.call('action_reject').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onCancelReturn: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Cancel Return'), _t('Are you sure you want to cancel this return?'), {
                confirm_callback: function() {
                    self.model.call('action_cancel').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onCreateExchange: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_create_exchange_order').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        }
    });

    // Sales Analytics Controller
    var SalesAnalyticsController = AbstractController.extend({
        events: _.extend({}, AbstractController.prototype.events, {
            'click .o_generate_report': '_onGenerateReport',
            'click .o_export_data': '_onExportData'
        }),

        _onGenerateReport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_generate_report').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },

        _onExportData: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_export_data').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        }
    });

    return {
        SalesOrderController: SalesOrderController,
        SalesDeliveryController: SalesDeliveryController,
        SalesReturnController: SalesReturnController,
        SalesAnalyticsController: SalesAnalyticsController,
        SalesUtils: SalesUtils
    };
});