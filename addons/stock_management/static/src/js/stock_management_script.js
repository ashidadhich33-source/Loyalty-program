/* Stock Management JavaScript */

odoo.define('stock_management.stock_management', function (require) {
    'use strict';

    var core = require('web.core');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var KanbanView = require('web.KanbanView');
    var AbstractAction = require('web.AbstractAction');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');

    var _t = core._t;

    // Stock Alert Management
    var StockAlertManager = AbstractAction.extend({
        template: 'stock_management.StockAlertManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadStockAlerts();
        },
        
        loadStockAlerts: function () {
            var self = this;
            rpc.query({
                model: 'stock.alert',
                method: 'search_read',
                args: [[], ['name', 'product_id', 'warehouse_id', 'alert_type', 'priority', 'status', 'current_stock', 'minimum_stock']],
            }).then(function (alerts) {
                self.renderStockAlerts(alerts);
            });
        },
        
        renderStockAlerts: function (alerts) {
            var self = this;
            var $alertsContainer = this.$('.o_stock_alerts_container');
            
            alerts.forEach(function (alert) {
                var $alert = self.createAlertElement(alert);
                $alertsContainer.append($alert);
            });
        },
        
        createAlertElement: function (alert) {
            var priorityClass = 'o_stock_alert_priority_' + alert.priority;
            var statusClass = 'o_stock_alert_status_' + alert.status;
            
            var $alert = $('<div>')
                .addClass('o_stock_alert_card')
                .addClass(priorityClass)
                .addClass(statusClass)
                .html(
                    '<div class="o_alert_header">' +
                        '<h4>' + alert.name + '</h4>' +
                        '<span class="o_alert_priority">' + alert.priority + '</span>' +
                    '</div>' +
                    '<div class="o_alert_body">' +
                        '<p><strong>Product:</strong> ' + alert.product_id[1] + '</p>' +
                        '<p><strong>Warehouse:</strong> ' + alert.warehouse_id[1] + '</p>' +
                        '<p><strong>Type:</strong> ' + alert.alert_type + '</p>' +
                        '<p><strong>Stock:</strong> ' + alert.current_stock + ' / ' + alert.minimum_stock + '</p>' +
                    '</div>' +
                    '<div class="o_alert_actions">' +
                        '<button class="o_stock_btn_primary o_acknowledge_btn">Acknowledge</button>' +
                        '<button class="o_stock_btn_success o_resolve_btn">Resolve</button>' +
                    '</div>'
                );
            
            // Add click handlers
            $alert.find('.o_acknowledge_btn').on('click', function () {
                self.acknowledgeAlert(alert.id);
            });
            
            $alert.find('.o_resolve_btn').on('click', function () {
                self.resolveAlert(alert.id);
            });
            
            return $alert;
        },
        
        acknowledgeAlert: function (alertId) {
            var self = this;
            rpc.query({
                model: 'stock.alert',
                method: 'action_acknowledge',
                args: [alertId],
            }).then(function () {
                self.loadStockAlerts();
            });
        },
        
        resolveAlert: function (alertId) {
            var self = this;
            rpc.query({
                model: 'stock.alert',
                method: 'action_resolve',
                args: [alertId],
            }).then(function () {
                self.loadStockAlerts();
            });
        }
    });

    // Reorder Rule Management
    var ReorderRuleManager = AbstractAction.extend({
        template: 'stock_management.ReorderRuleManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadReorderRules();
        },
        
        loadReorderRules: function () {
            var self = this;
            rpc.query({
                model: 'stock.reorder.rule',
                method: 'search_read',
                args: [[], ['name', 'product_id', 'warehouse_id', 'minimum_stock', 'maximum_stock', 'reorder_qty', 'current_stock', 'stock_status']],
            }).then(function (rules) {
                self.renderReorderRules(rules);
            });
        },
        
        renderReorderRules: function (rules) {
            var self = this;
            var $rulesContainer = this.$('.o_reorder_rules_container');
            
            rules.forEach(function (rule) {
                var $rule = self.createRuleElement(rule);
                $rulesContainer.append($rule);
            });
        },
        
        createRuleElement: function (rule) {
            var statusClass = 'o_stock_status_' + rule.stock_status;
            
            var $rule = $('<div>')
                .addClass('o_reorder_rule_card')
                .addClass(statusClass)
                .html(
                    '<div class="o_rule_header">' +
                        '<h4>' + rule.name + '</h4>' +
                        '<span class="o_rule_status">' + rule.stock_status + '</span>' +
                    '</div>' +
                    '<div class="o_rule_body">' +
                        '<p><strong>Product:</strong> ' + rule.product_id[1] + '</p>' +
                        '<p><strong>Warehouse:</strong> ' + rule.warehouse_id[1] + '</p>' +
                        '<p><strong>Min Stock:</strong> ' + rule.minimum_stock + '</p>' +
                        '<p><strong>Max Stock:</strong> ' + rule.maximum_stock + '</p>' +
                        '<p><strong>Reorder Qty:</strong> ' + rule.reorder_qty + '</p>' +
                        '<p><strong>Current Stock:</strong> ' + rule.current_stock + '</p>' +
                    '</div>' +
                    '<div class="o_rule_actions">' +
                        '<button class="o_stock_btn_primary o_create_po_btn">Create PO</button>' +
                        '<button class="o_stock_btn_warning o_optimize_btn">Optimize</button>' +
                    '</div>'
                );
            
            // Add click handlers
            $rule.find('.o_create_po_btn').on('click', function () {
                self.createPurchaseOrder(rule.id);
            });
            
            $rule.find('.o_optimize_btn').on('click', function () {
                self.optimizeRule(rule.id);
            });
            
            return $rule;
        },
        
        createPurchaseOrder: function (ruleId) {
            var self = this;
            rpc.query({
                model: 'stock.reorder.rule',
                method: 'action_create_purchase_order',
                args: [ruleId],
            }).then(function (result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },
        
        optimizeRule: function (ruleId) {
            var self = this;
            rpc.query({
                model: 'stock.reorder.rule',
                method: 'action_optimize_rule',
                args: [ruleId],
            }).then(function () {
                self.loadReorderRules();
            });
        }
    });

    // Stock Adjustment Management
    var StockAdjustmentManager = AbstractAction.extend({
        template: 'stock_management.StockAdjustmentManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadStockAdjustments();
        },
        
        loadStockAdjustments: function () {
            var self = this;
            rpc.query({
                model: 'stock.adjustment',
                method: 'search_read',
                args: [[], ['name', 'date', 'warehouse_id', 'adjustment_type', 'state', 'total_quantity_adjusted', 'total_value_adjusted']],
            }).then(function (adjustments) {
                self.renderStockAdjustments(adjustments);
            });
        },
        
        renderStockAdjustments: function (adjustments) {
            var self = this;
            var $adjustmentsContainer = this.$('.o_stock_adjustments_container');
            
            adjustments.forEach(function (adjustment) {
                var $adjustment = self.createAdjustmentElement(adjustment);
                $adjustmentsContainer.append($adjustment);
            });
        },
        
        createAdjustmentElement: function (adjustment) {
            var stateClass = 'o_adjustment_state_' + adjustment.state;
            
            var $adjustment = $('<div>')
                .addClass('o_stock_adjustment_card')
                .addClass(stateClass)
                .html(
                    '<div class="o_adjustment_header">' +
                        '<h4>' + adjustment.name + '</h4>' +
                        '<span class="o_adjustment_state">' + adjustment.state + '</span>' +
                    '</div>' +
                    '<div class="o_adjustment_body">' +
                        '<p><strong>Date:</strong> ' + adjustment.date + '</p>' +
                        '<p><strong>Warehouse:</strong> ' + adjustment.warehouse_id[1] + '</p>' +
                        '<p><strong>Type:</strong> ' + adjustment.adjustment_type + '</p>' +
                        '<p><strong>Qty Adjusted:</strong> ' + adjustment.total_quantity_adjusted + '</p>' +
                        '<p><strong>Value Adjusted:</strong> ' + adjustment.total_value_adjusted + '</p>' +
                    '</div>' +
                    '<div class="o_adjustment_actions">' +
                        '<button class="o_stock_btn_primary o_confirm_btn">Confirm</button>' +
                        '<button class="o_stock_btn_success o_approve_btn">Approve</button>' +
                        '<button class="o_stock_btn_warning o_done_btn">Done</button>' +
                    '</div>'
                );
            
            // Add click handlers
            $adjustment.find('.o_confirm_btn').on('click', function () {
                self.confirmAdjustment(adjustment.id);
            });
            
            $adjustment.find('.o_approve_btn').on('click', function () {
                self.approveAdjustment(adjustment.id);
            });
            
            $adjustment.find('.o_done_btn').on('click', function () {
                self.doneAdjustment(adjustment.id);
            });
            
            return $adjustment;
        },
        
        confirmAdjustment: function (adjustmentId) {
            var self = this;
            rpc.query({
                model: 'stock.adjustment',
                method: 'action_confirm',
                args: [adjustmentId],
            }).then(function () {
                self.loadStockAdjustments();
            });
        },
        
        approveAdjustment: function (adjustmentId) {
            var self = this;
            rpc.query({
                model: 'stock.adjustment',
                method: 'action_approve',
                args: [adjustmentId],
            }).then(function () {
                self.loadStockAdjustments();
            });
        },
        
        doneAdjustment: function (adjustmentId) {
            var self = this;
            rpc.query({
                model: 'stock.adjustment',
                method: 'action_done',
                args: [adjustmentId],
            }).then(function () {
                self.loadStockAdjustments();
            });
        }
    });

    // Stock Analysis Management
    var StockAnalysisManager = AbstractAction.extend({
        template: 'stock_management.StockAnalysisManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadStockAnalysis();
        },
        
        loadStockAnalysis: function () {
            var self = this;
            rpc.query({
                model: 'stock.analysis',
                method: 'search_read',
                args: [[], ['name', 'date', 'analysis_type', 'state', 'total_products', 'total_stock_value', 'total_stock_quantity']],
            }).then(function (analyses) {
                self.renderStockAnalysis(analyses);
            });
        },
        
        renderStockAnalysis: function (analyses) {
            var self = this;
            var $analysesContainer = this.$('.o_stock_analyses_container');
            
            analyses.forEach(function (analysis) {
                var $analysis = self.createAnalysisElement(analysis);
                $analysesContainer.append($analysis);
            });
        },
        
        createAnalysisElement: function (analysis) {
            var stateClass = 'o_analysis_state_' + analysis.state;
            
            var $analysis = $('<div>')
                .addClass('o_stock_analysis_card')
                .addClass(stateClass)
                .html(
                    '<div class="o_analysis_header">' +
                        '<h4>' + analysis.name + '</h4>' +
                        '<span class="o_analysis_state">' + analysis.state + '</span>' +
                    '</div>' +
                    '<div class="o_analysis_body">' +
                        '<p><strong>Date:</strong> ' + analysis.date + '</p>' +
                        '<p><strong>Type:</strong> ' + analysis.analysis_type + '</p>' +
                        '<p><strong>Products:</strong> ' + analysis.total_products + '</p>' +
                        '<p><strong>Stock Value:</strong> ' + analysis.total_stock_value + '</p>' +
                        '<p><strong>Stock Quantity:</strong> ' + analysis.total_stock_quantity + '</p>' +
                    '</div>' +
                    '<div class="o_analysis_actions">' +
                        '<button class="o_stock_btn_primary o_run_analysis_btn">Run Analysis</button>' +
                        '<button class="o_stock_btn_success o_view_results_btn">View Results</button>' +
                    </div>'
                );
            
            // Add click handlers
            $analysis.find('.o_run_analysis_btn').on('click', function () {
                self.runAnalysis(analysis.id);
            });
            
            $analysis.find('.o_view_results_btn').on('click', function () {
                self.viewResults(analysis.id);
            });
            
            return $analysis;
        },
        
        runAnalysis: function (analysisId) {
            var self = this;
            rpc.query({
                model: 'stock.analysis',
                method: 'action_run_analysis',
                args: [analysisId],
            }).then(function () {
                self.loadStockAnalysis();
            });
        },
        
        viewResults: function (analysisId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Analysis Results',
                res_model: 'stock.analysis',
                res_id: analysisId,
                view_mode: 'form',
                target: 'current',
            });
        }
    });

    // Dashboard Widget
    var StockDashboardWidget = AbstractAction.extend({
        template: 'stock_management.StockDashboard',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadDashboardData();
        },
        
        loadDashboardData: function () {
            var self = this;
            
            // Load stock alerts
            rpc.query({
                model: 'stock.alert',
                method: 'search_count',
                args: [[('status', '=', 'active')]],
            }).then(function (activeAlerts) {
                self.$('.o_active_alerts_count').text(activeAlerts);
            });
            
            // Load critical alerts
            rpc.query({
                model: 'stock.alert',
                method: 'search_count',
                args: [[('priority', '=', 'critical')]],
            }).then(function (criticalAlerts) {
                self.$('.o_critical_alerts_count').text(criticalAlerts);
            });
            
            // Load reorder rules
            rpc.query({
                model: 'stock.reorder.rule',
                method: 'search_count',
                args: [[('active', '=', True)]],
            }).then(function (activeRules) {
                self.$('.o_active_rules_count').text(activeRules);
            });
            
            // Load pending adjustments
            rpc.query({
                model: 'stock.adjustment',
                method: 'search_count',
                args: [[('state', '=', 'confirmed'), ('require_approval', '=', True)]],
            }).then(function (pendingAdjustments) {
                self.$('.o_pending_adjustments_count').text(pendingAdjustments);
            });
        }
    });

    // Utility Functions
    var StockManagementUtils = {
        formatCurrency: function (amount) {
            return new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR'
            }).format(amount);
        },
        
        formatNumber: function (number) {
            return new Intl.NumberFormat('en-IN').format(number);
        },
        
        formatDate: function (date) {
            return new Date(date).toLocaleDateString('en-IN');
        },
        
        formatDateTime: function (datetime) {
            return new Date(datetime).toLocaleString('en-IN');
        },
        
        showNotification: function (title, message, type) {
            var notification = new Dialog(this, {
                title: title,
                size: 'medium',
                buttons: [
                    {
                        text: 'OK',
                        click: function () {
                            notification.close();
                        }
                    }
                ]
            });
            
            notification.appendTo($('<div>').html(message));
            notification.open();
        },
        
        showLoading: function (element) {
            var $loading = $('<div>').addClass('o_stock_loading');
            $(element).append($loading);
        },
        
        hideLoading: function (element) {
            $(element).find('.o_stock_loading').remove();
        }
    };

    // Register actions
    core.action_registry.add('stock_alert_manager', StockAlertManager);
    core.action_registry.add('reorder_rule_manager', ReorderRuleManager);
    core.action_registry.add('stock_adjustment_manager', StockAdjustmentManager);
    core.action_registry.add('stock_analysis_manager', StockAnalysisManager);
    core.action_registry.add('stock_dashboard_widget', StockDashboardWidget);

    return {
        StockAlertManager: StockAlertManager,
        ReorderRuleManager: ReorderRuleManager,
        StockAdjustmentManager: StockAdjustmentManager,
        StockAnalysisManager: StockAnalysisManager,
        StockDashboardWidget: StockDashboardWidget,
        StockManagementUtils: StockManagementUtils
    };
});