// Discounts Management JavaScript
ocean.define('discounts.DiscountsController', function (require) {
    'use strict';
    
    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    
    // Discount Program Controller
    var DiscountProgramController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .discount-program-generate': '_onGenerateCoupons',
            'click .discount-program-analytics': '_onShowAnalytics',
        }),
        
        _onGenerateCoupons: function () {
            var self = this;
            var programId = this.model.get('id');
            
            if (!programId) {
                this.do_warn('Please save the program first');
                return;
            }
            
            rpc.query({
                model: 'discount.program',
                method: 'generate_coupons',
                args: [programId],
            }).then(function (result) {
                self.do_notify('Success', 'Coupons generated successfully');
            });
        },
        
        _onShowAnalytics: function () {
            var self = this;
            var programId = this.model.get('id');
            
            if (!programId) {
                this.do_warn('Please save the program first');
                return;
            }
            
            rpc.query({
                model: 'discount.program',
                method: 'get_analytics',
                args: [programId],
            }).then(function (result) {
                self._showAnalyticsDialog(result);
            });
        },
        
        _showAnalyticsDialog: function (data) {
            var dialog = new Dialog(this, {
                title: 'Discount Program Analytics',
                size: 'large',
                $content: $('<div>').html(this._renderAnalytics(data)),
                buttons: [
                    {text: 'Close', close: true}
                ]
            });
            dialog.open();
        },
        
        _renderAnalytics: function (data) {
            var html = '<div class="discount-analytics">';
            html += '<div class="row">';
            html += '<div class="col-md-6">';
            html += '<h4>Usage Statistics</h4>';
            html += '<p>Total Usage: ' + data.total_usage + '</p>';
            html += '<p>Total Customers: ' + data.total_customers + '</p>';
            html += '<p>Total Orders: ' + data.total_orders + '</p>';
            html += '</div>';
            html += '<div class="col-md-6">';
            html += '<h4>Financial Impact</h4>';
            html += '<p>Total Discount Amount: $' + data.total_discount_amount + '</p>';
            html += '<p>Program ROI: ' + data.program_roi + '%</p>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            return html;
        }
    });
    
    // Discount Rule Controller
    var DiscountRuleController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'change .discount-rule-type': '_onRuleTypeChange',
        }),
        
        _onRuleTypeChange: function (event) {
            var ruleType = $(event.target).val();
            this._updateRuleFields(ruleType);
        },
        
        _updateRuleFields: function (ruleType) {
            var self = this;
            
            // Hide all rule-specific fields
            $('.rule-field').hide();
            
            // Show relevant fields based on rule type
            switch (ruleType) {
                case 'minimum_amount':
                    $('.rule-field.minimum-amount').show();
                    break;
                case 'maximum_amount':
                    $('.rule-field.maximum-amount').show();
                    break;
                case 'customer_segment':
                    $('.rule-field.customer-segment').show();
                    break;
                case 'product_category':
                    $('.rule-field.product-category').show();
                    break;
                case 'age_group':
                    $('.rule-field.age-group').show();
                    break;
                case 'seasonal':
                    $('.rule-field.seasonal').show();
                    break;
            }
        }
    });
    
    // Discount Coupon Controller
    var DiscountCouponController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .discount-coupon-generate': '_onGenerateCoupons',
            'click .discount-coupon-validate': '_onValidateCoupon',
        }),
        
        _onGenerateCoupons: function () {
            var self = this;
            var dialog = new Dialog(this, {
                title: 'Generate Discount Coupons',
                size: 'medium',
                $content: $('<div>').html(this._renderCouponGenerationForm()),
                buttons: [
                    {text: 'Generate', click: function () { self._generateCoupons(); }},
                    {text: 'Cancel', close: true}
                ]
            });
            dialog.open();
        },
        
        _renderCouponGenerationForm: function () {
            var html = '<div class="coupon-generation-form">';
            html += '<div class="form-group">';
            html += '<label>Coupon Type:</label>';
            html += '<select class="form-control coupon-type">';
            html += '<option value="percentage">Percentage</option>';
            html += '<option value="fixed">Fixed Amount</option>';
            html += '<option value="free_shipping">Free Shipping</option>';
            html += '</select>';
            html += '</div>';
            html += '<div class="form-group">';
            html += '<label>Discount Value:</label>';
            html += '<input type="number" class="form-control discount-value" step="0.01">';
            html += '</div>';
            html += '<div class="form-group">';
            html += '<label>Number of Coupons:</label>';
            html += '<input type="number" class="form-control coupon-count" value="100">';
            html += '</div>';
            html += '</div>';
            return html;
        },
        
        _generateCoupons: function () {
            var self = this;
            var couponType = $('.coupon-type').val();
            var discountValue = $('.discount-value').val();
            var couponCount = $('.coupon-count').val();
            
            if (!discountValue || !couponCount) {
                this.do_warn('Please fill in all fields');
                return;
            }
            
            rpc.query({
                model: 'discount.coupon',
                method: 'generate_coupons',
                args: [{
                    type: couponType,
                    discount_value: parseFloat(discountValue),
                    count: parseInt(couponCount)
                }],
            }).then(function (result) {
                self.do_notify('Success', 'Coupons generated successfully');
                self.reload();
            });
        },
        
        _onValidateCoupon: function () {
            var self = this;
            var dialog = new Dialog(this, {
                title: 'Validate Discount Coupon',
                size: 'small',
                $content: $('<div>').html(this._renderCouponValidationForm()),
                buttons: [
                    {text: 'Validate', click: function () { self._validateCoupon(); }},
                    {text: 'Cancel', close: true}
                ]
            });
            dialog.open();
        },
        
        _renderCouponValidationForm: function () {
            var html = '<div class="coupon-validation-form">';
            html += '<div class="form-group">';
            html += '<label>Coupon Code:</label>';
            html += '<input type="text" class="form-control coupon-code" placeholder="Enter coupon code">';
            html += '</div>';
            html += '</div>';
            return html;
        },
        
        _validateCoupon: function () {
            var self = this;
            var couponCode = $('.coupon-code').val();
            
            if (!couponCode) {
                this.do_warn('Please enter a coupon code');
                return;
            }
            
            rpc.query({
                model: 'discount.coupon',
                method: 'validate_coupon',
                args: [couponCode],
            }).then(function (result) {
                if (result.valid) {
                    self.do_notify('Success', 'Coupon is valid');
                } else {
                    self.do_warn('Invalid Coupon', result.message);
                }
            });
        }
    });
    
    // Discount Approval Controller
    var DiscountApprovalController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .discount-approval-approve': '_onApprove',
            'click .discount-approval-reject': '_onReject',
        }),
        
        _onApprove: function (event) {
            var self = this;
            var approvalId = $(event.target).data('approval-id');
            
            rpc.query({
                model: 'discount.approval',
                method: 'approve',
                args: [approvalId],
            }).then(function (result) {
                self.do_notify('Success', 'Discount approved successfully');
                self.reload();
            });
        },
        
        _onReject: function (event) {
            var self = this;
            var approvalId = $(event.target).data('approval-id');
            
            rpc.query({
                model: 'discount.approval',
                method: 'reject',
                args: [approvalId],
            }).then(function (result) {
                self.do_notify('Success', 'Discount rejected');
                self.reload();
            });
        }
    });
    
    // Discount Campaign Controller
    var DiscountCampaignController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .discount-campaign-launch': '_onLaunchCampaign',
            'click .discount-campaign-pause': '_onPauseCampaign',
            'click .discount-campaign-analytics': '_onShowCampaignAnalytics',
        }),
        
        _onLaunchCampaign: function () {
            var self = this;
            var campaignId = this.model.get('id');
            
            if (!campaignId) {
                this.do_warn('Please save the campaign first');
                return;
            }
            
            rpc.query({
                model: 'discount.campaign',
                method: 'launch',
                args: [campaignId],
            }).then(function (result) {
                self.do_notify('Success', 'Campaign launched successfully');
                self.reload();
            });
        },
        
        _onPauseCampaign: function () {
            var self = this;
            var campaignId = this.model.get('id');
            
            if (!campaignId) {
                this.do_warn('Please save the campaign first');
                return;
            }
            
            rpc.query({
                model: 'discount.campaign',
                method: 'pause',
                args: [campaignId],
            }).then(function (result) {
                self.do_notify('Success', 'Campaign paused successfully');
                self.reload();
            });
        },
        
        _onShowCampaignAnalytics: function () {
            var self = this;
            var campaignId = this.model.get('id');
            
            if (!campaignId) {
                this.do_warn('Please save the campaign first');
                return;
            }
            
            rpc.query({
                model: 'discount.campaign',
                method: 'get_analytics',
                args: [campaignId],
            }).then(function (result) {
                self._showCampaignAnalyticsDialog(result);
            });
        },
        
        _showCampaignAnalyticsDialog: function (data) {
            var dialog = new Dialog(this, {
                title: 'Campaign Analytics',
                size: 'large',
                $content: $('<div>').html(this._renderCampaignAnalytics(data)),
                buttons: [
                    {text: 'Close', close: true}
                ]
            });
            dialog.open();
        },
        
        _renderCampaignAnalytics: function (data) {
            var html = '<div class="campaign-analytics">';
            html += '<div class="row">';
            html += '<div class="col-md-6">';
            html += '<h4>Campaign Performance</h4>';
            html += '<p>Total Usage: ' + data.total_usage + '</p>';
            html += '<p>Total Customers: ' + data.total_customers + '</p>';
            html += '<p>Total Orders: ' + data.total_orders + '</p>';
            html += '</div>';
            html += '<div class="col-md-6">';
            html += '<h4>Financial Impact</h4>';
            html += '<p>Total Campaign Value: $' + data.total_campaign_value + '</p>';
            html += '<p>Average Campaign Value: $' + data.average_campaign_value + '</p>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            return html;
        }
    });
    
    // Discount Analytics Controller
    var DiscountAnalyticsController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .discount-analytics-generate': '_onGenerateAnalytics',
            'click .discount-analytics-export': '_onExportAnalytics',
        }),
        
        _onGenerateAnalytics: function () {
            var self = this;
            
            rpc.query({
                model: 'discount.analytics',
                method: 'generate_analytics',
                args: [],
            }).then(function (result) {
                self.do_notify('Success', 'Analytics generated successfully');
                self.reload();
            });
        },
        
        _onExportAnalytics: function () {
            var self = this;
            
            rpc.query({
                model: 'discount.analytics',
                method: 'export_analytics',
                args: [],
            }).then(function (result) {
                self.do_notify('Success', 'Analytics exported successfully');
            });
        }
    });
    
    return {
        DiscountProgramController: DiscountProgramController,
        DiscountRuleController: DiscountRuleController,
        DiscountCouponController: DiscountCouponController,
        DiscountApprovalController: DiscountApprovalController,
        DiscountCampaignController: DiscountCampaignController,
        DiscountAnalyticsController: DiscountAnalyticsController,
    };
});