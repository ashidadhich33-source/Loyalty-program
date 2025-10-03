// Loyalty Script for Ocean ERP
ocean.define('loyalty.LoyaltyController', function (require) {
    'use strict';
    
    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    
    // Loyalty Program Controller
    var LoyaltyProgramController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_program_activate': '_onActivate',
            'click .o_loyalty_program_deactivate': '_onDeactivate',
            'click .o_loyalty_program_view_customers': '_onViewCustomers',
            'click .o_loyalty_program_view_analytics': '_onViewAnalytics',
        }),
        
        _onActivate: function (event) {
            event.preventDefault();
            var self = this;
            var programId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to activate this loyalty program?', {
                title: 'Activate Program',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.program',
                        method: 'action_activate',
                        args: [programId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onDeactivate: function (event) {
            event.preventDefault();
            var self = this;
            var programId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to deactivate this loyalty program?', {
                title: 'Deactivate Program',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.program',
                        method: 'action_deactivate',
                        args: [programId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onViewCustomers: function (event) {
            event.preventDefault();
            var self = this;
            var programId = this.getSelectedIds()[0];
            
            rpc.query({
                model: 'loyalty.program',
                method: 'action_view_customers',
                args: [programId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
        
        _onViewAnalytics: function (event) {
            event.preventDefault();
            var self = this;
            var programId = this.getSelectedIds()[0];
            
            rpc.query({
                model: 'loyalty.program',
                method: 'action_view_analytics',
                args: [programId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
    });
    
    // Loyalty Points Controller
    var LoyaltyPointsController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_points_expire': '_onExpirePoints',
            'click .o_loyalty_points_send_notification': '_onSendNotification',
            'click .o_loyalty_points_adjust': '_onAdjustPoints',
        }),
        
        _onExpirePoints: function (event) {
            event.preventDefault();
            var self = this;
            var pointsId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to expire these points?', {
                title: 'Expire Points',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.points',
                        method: 'action_expire_points',
                        args: [pointsId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onSendNotification: function (event) {
            event.preventDefault();
            var self = this;
            var pointsId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to send expiry notification for these points?', {
                title: 'Send Expiry Notification',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.points',
                        method: 'action_send_expiry_notification',
                        args: [pointsId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onAdjustPoints: function (event) {
            event.preventDefault();
            var self = this;
            var pointsId = this.getSelectedIds()[0];
            
            Dialog.prompt(this, 'Enter adjustment points and reason:', {
                title: 'Adjust Points',
                input: 'text',
                confirm_callback: function (value) {
                    var parts = value.split(',');
                    var adjustmentPoints = parseInt(parts[0]);
                    var reason = parts[1] || 'Manual adjustment';
                    
                    rpc.query({
                        model: 'loyalty.points',
                        method: 'action_adjust_points',
                        args: [pointsId, adjustmentPoints, reason],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // Loyalty Reward Controller
    var LoyaltyRewardController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_reward_redeem': '_onRedeem',
        }),
        
        _onRedeem: function (event) {
            event.preventDefault();
            var self = this;
            var rewardId = this.getSelectedIds()[0];
            
            Dialog.prompt(this, 'Enter customer ID and quantity:', {
                title: 'Redeem Reward',
                input: 'text',
                confirm_callback: function (value) {
                    var parts = value.split(',');
                    var partnerId = parseInt(parts[0]);
                    var quantity = parseInt(parts[1]) || 1;
                    
                    rpc.query({
                        model: 'loyalty.reward',
                        method: 'action_redeem',
                        args: [rewardId, partnerId, quantity],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // Loyalty Voucher Controller
    var LoyaltyVoucherController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_voucher_activate': '_onActivate',
            'click .o_loyalty_voucher_use': '_onUse',
            'click .o_loyalty_voucher_cancel': '_onCancel',
            'click .o_loyalty_voucher_expire': '_onExpire',
        }),
        
        _onActivate: function (event) {
            event.preventDefault();
            var self = this;
            var voucherId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to activate this voucher?', {
                title: 'Activate Voucher',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.voucher',
                        method: 'action_activate',
                        args: [voucherId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onUse: function (event) {
            event.preventDefault();
            var self = this;
            var voucherId = this.getSelectedIds()[0];
            
            Dialog.prompt(this, 'Enter customer ID:', {
                title: 'Use Voucher',
                input: 'text',
                confirm_callback: function (value) {
                    var partnerId = parseInt(value);
                    
                    rpc.query({
                        model: 'loyalty.voucher',
                        method: 'action_use',
                        args: [voucherId, partnerId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onCancel: function (event) {
            event.preventDefault();
            var self = this;
            var voucherId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to cancel this voucher?', {
                title: 'Cancel Voucher',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.voucher',
                        method: 'action_cancel',
                        args: [voucherId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onExpire: function (event) {
            event.preventDefault();
            var self = this;
            var voucherId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to expire this voucher?', {
                title: 'Expire Voucher',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.voucher',
                        method: 'action_expire',
                        args: [voucherId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // Loyalty Offer Controller
    var LoyaltyOfferController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_offer_activate': '_onActivate',
            'click .o_loyalty_offer_deactivate': '_onDeactivate',
            'click .o_loyalty_offer_send_notification': '_onSendNotification',
            'click .o_loyalty_offer_view_usage': '_onViewUsage',
        }),
        
        _onActivate: function (event) {
            event.preventDefault();
            var self = this;
            var offerId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to activate this offer?', {
                title: 'Activate Offer',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.offer',
                        method: 'action_activate',
                        args: [offerId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onDeactivate: function (event) {
            event.preventDefault();
            var self = this;
            var offerId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to deactivate this offer?', {
                title: 'Deactivate Offer',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.offer',
                        method: 'action_deactivate',
                        args: [offerId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onSendNotification: function (event) {
            event.preventDefault();
            var self = this;
            var offerId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to send notification for this offer?', {
                title: 'Send Notification',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.offer',
                        method: 'action_send_notification',
                        args: [offerId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onViewUsage: function (event) {
            event.preventDefault();
            var self = this;
            var offerId = this.getSelectedIds()[0];
            
            rpc.query({
                model: 'loyalty.offer',
                method: 'action_view_usage',
                args: [offerId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
    });
    
    // Loyalty Tier Controller
    var LoyaltyTierController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_tier_view_customers': '_onViewCustomers',
            'click .o_loyalty_tier_view_analytics': '_onViewAnalytics',
        }),
        
        _onViewCustomers: function (event) {
            event.preventDefault();
            var self = this;
            var tierId = this.getSelectedIds()[0];
            
            rpc.query({
                model: 'loyalty.tier',
                method: 'action_view_customers',
                args: [tierId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
        
        _onViewAnalytics: function (event) {
            event.preventDefault();
            var self = this;
            var tierId = this.getSelectedIds()[0];
            
            rpc.query({
                model: 'loyalty.tier',
                method: 'action_view_analytics',
                args: [tierId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
    });
    
    // Loyalty Analytics Controller
    var LoyaltyAnalyticsController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_loyalty_analytics_generate': '_onGenerateAnalytics',
            'click .o_loyalty_analytics_export': '_onExportAnalytics',
        }),
        
        _onGenerateAnalytics: function (event) {
            event.preventDefault();
            var self = this;
            var analyticsId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to generate analytics for this period?', {
                title: 'Generate Analytics',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.analytics',
                        method: 'action_generate_analytics',
                        args: [analyticsId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onExportAnalytics: function (event) {
            event.preventDefault();
            var self = this;
            var analyticsId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to export analytics data?', {
                title: 'Export Analytics',
                confirm_callback: function () {
                    rpc.query({
                        model: 'loyalty.analytics',
                        method: 'action_export_analytics',
                        args: [analyticsId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    return {
        LoyaltyProgramController: LoyaltyProgramController,
        LoyaltyPointsController: LoyaltyPointsController,
        LoyaltyRewardController: LoyaltyRewardController,
        LoyaltyVoucherController: LoyaltyVoucherController,
        LoyaltyOfferController: LoyaltyOfferController,
        LoyaltyTierController: LoyaltyTierController,
        LoyaltyAnalyticsController: LoyaltyAnalyticsController,
    };
});