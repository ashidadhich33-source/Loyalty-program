/* POS Return JavaScript for Kids Clothing ERP */

// POS Return Dashboard functionality
class POSReturnDashboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind dashboard refresh button
        $(document).on('click', '.pos-return-refresh-btn', () => {
            this.refreshDashboard();
        });
        
        // Bind new return button
        $(document).on('click', '.pos-new-return-btn', () => {
            this.startNewReturn();
        });
    }
    
    loadDashboardData() {
        // Load dashboard data via AJAX
        $.ajax({
            url: '/pos_return/dashboard_data',
            type: 'GET',
            success: (data) => {
                this.updateDashboard(data);
            },
            error: (error) => {
                console.error('Error loading return dashboard data:', error);
            }
        });
    }
    
    updateDashboard(data) {
        // Update dashboard statistics
        $('.pos-return-today-count').text(data.today_returns);
        $('.pos-return-today-value').text(this.formatCurrency(data.today_value));
        
        // Update return summary
        this.updateReturnSummary(data.return_summary);
    }
    
    updateReturnSummary(summary) {
        const container = $('.pos-return-summary-stats');
        container.empty();
        
        Object.entries(summary).forEach(([reason, count]) => {
            const statCard = $(`
                <div class="pos-return-stat-card">
                    <div class="stat-value">${count}</div>
                    <div class="stat-label">${reason}</div>
                </div>
            `);
            container.append(statCard);
        });
    }
    
    refreshDashboard() {
        this.loadDashboardData();
        this.showNotification('Return dashboard refreshed', 'success');
    }
    
    startNewReturn() {
        // Open new return wizard
        window.open('/pos_return/new_return', '_blank');
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-return-notification pos-return-notification-${type} pos-return-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Return Processing functionality
class POSReturnProcessor {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind return reason selection
        $(document).on('click', '.pos-return-reason', (e) => {
            this.selectReturnReason($(e.currentTarget));
        });
        
        // Bind return type selection
        $(document).on('change', '.pos-return-type', (e) => {
            this.updateReturnType(e.target.value);
        });
        
        // Bind refund method selection
        $(document).on('click', '.pos-refund-method', (e) => {
            this.selectRefundMethod($(e.currentTarget));
        });
        
        // Bind customer age input
        $(document).on('input', '.pos-customer-age', (e) => {
            this.updateCustomerAge(e.target.value);
        });
        
        // Bind calculate refund button
        $(document).on('click', '.pos-calculate-refund-btn', () => {
            this.calculateRefund();
        });
        
        // Bind process return button
        $(document).on('click', '.pos-process-return-btn', () => {
            this.processReturn();
        });
    }
    
    selectReturnReason(element) {
        $('.pos-return-reason').removeClass('selected');
        element.addClass('selected');
        
        const reasonId = element.data('reason-id');
        $('.pos-selected-return-reason').val(reasonId);
        
        this.updateReturnPolicy(reasonId);
    }
    
    updateReturnPolicy(reasonId) {
        // Get return reason details
        $.ajax({
            url: `/pos_return/get_reason_policy/${reasonId}`,
            type: 'GET',
            success: (data) => {
                this.displayReturnPolicy(data);
            },
            error: (error) => {
                console.error('Error loading return policy:', error);
            }
        });
    }
    
    displayReturnPolicy(policy) {
        const container = $('.pos-return-policy-info');
        container.empty();
        
        const policyCard = $(`
            <div class="pos-return-policy ${policy.within_policy ? 'success' : 'warning'}">
                <h4>Return Policy</h4>
                <p><strong>Max Period:</strong> ${policy.max_return_period} days</p>
                <p><strong>Full Refund:</strong> ${policy.allow_full_refund ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Partial Refund:</strong> ${policy.allow_partial_refund ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Store Credit:</strong> ${policy.allow_store_credit ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Exchange:</strong> ${policy.allow_exchange ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Default Refund:</strong> ${policy.default_refund_percentage}%</p>
                ${policy.age_group_restriction !== 'none' ? `<p><strong>Age Restriction:</strong> ${policy.age_group_restriction}</p>` : ''}
            </div>
        `);
        
        container.append(policyCard);
    }
    
    updateReturnType(type) {
        // Update return type specific fields
        if (type === 'full_return') {
            $('.pos-full-return-fields').show();
            $('.pos-partial-return-fields').hide();
        } else if (type === 'partial_return') {
            $('.pos-full-return-fields').hide();
            $('.pos-partial-return-fields').show();
        } else {
            $('.pos-full-return-fields').hide();
            $('.pos-partial-return-fields').hide();
        }
    }
    
    selectRefundMethod(element) {
        $('.pos-refund-method').removeClass('selected');
        element.addClass('selected');
        
        const method = element.data('method');
        $('.pos-selected-refund-method').val(method);
        
        this.updateRefundMethodFields(method);
    }
    
    updateRefundMethodFields(method) {
        if (method === 'store_credit') {
            $('.pos-store-credit-fields').show();
            $('.pos-cash-refund-fields').hide();
            $('.pos-card-refund-fields').hide();
        } else if (method === 'cash') {
            $('.pos-store-credit-fields').hide();
            $('.pos-cash-refund-fields').show();
            $('.pos-card-refund-fields').hide();
        } else if (method === 'card') {
            $('.pos-store-credit-fields').hide();
            $('.pos-cash-refund-fields').hide();
            $('.pos-card-refund-fields').show();
        } else {
            $('.pos-store-credit-fields').hide();
            $('.pos-cash-refund-fields').hide();
            $('.pos-card-refund-fields').hide();
        }
    }
    
    updateCustomerAge(age) {
        // Validate age-based policies
        const reasonId = $('.pos-selected-return-reason').val();
        if (reasonId && age) {
            $.ajax({
                url: `/pos_return/validate_age_policy/${reasonId}/${age}`,
                type: 'GET',
                success: (data) => {
                    if (!data.valid) {
                        this.showNotification(data.message, 'warning');
                    }
                },
                error: (error) => {
                    console.error('Error validating age policy:', error);
                }
            });
        }
    }
    
    calculateRefund() {
        const reasonId = $('.pos-selected-return-reason').val();
        const returnType = $('.pos-return-type').val();
        const originalAmount = parseFloat($('.pos-original-amount').val()) || 0;
        
        if (!reasonId || !returnType || originalAmount <= 0) {
            this.showNotification('Please select reason, type, and enter original amount', 'warning');
            return;
        }
        
        $.ajax({
            url: `/pos_return/calculate_refund/${reasonId}/${returnType}/${originalAmount}`,
            type: 'GET',
            success: (data) => {
                this.updateRefundAmounts(data);
            },
            error: (error) => {
                console.error('Error calculating refund:', error);
            }
        });
    }
    
    updateRefundAmounts(data) {
        $('.pos-refund-percentage').val(data.refund_percentage);
        $('.pos-refund-amount').val(this.formatCurrency(data.refund_amount));
        $('.pos-store-credit-amount').val(this.formatCurrency(data.store_credit_amount));
        
        if (data.store_credit_amount > 0) {
            $('.pos-store-credit-info').show();
            $('.pos-store-credit-expiry').val(data.store_credit_expiry);
        } else {
            $('.pos-store-credit-info').hide();
        }
    }
    
    processReturn() {
        const returnData = this.collectReturnData();
        
        if (!this.validateReturnData(returnData)) {
            return;
        }
        
        $.ajax({
            url: '/pos_return/process_return',
            type: 'POST',
            data: returnData,
            success: (response) => {
                this.showNotification('Return processed successfully', 'success');
                this.resetReturnForm();
                // Redirect to return details
                window.location.href = `/pos_return/view/${response.return_id}`;
            },
            error: (error) => {
                this.showNotification('Error processing return', 'error');
            }
        });
    }
    
    collectReturnData() {
        return {
            customer_id: $('.pos-customer-id').val(),
            original_order_id: $('.pos-original-order-id').val(),
            return_reason_id: $('.pos-selected-return-reason').val(),
            return_type: $('.pos-return-type').val(),
            customer_age: $('.pos-customer-age').val(),
            refund_method: $('.pos-selected-refund-method').val(),
            refund_percentage: $('.pos-refund-percentage').val(),
            store_credit_amount: $('.pos-store-credit-amount').val(),
            store_credit_expiry: $('.pos-store-credit-expiry').val(),
            reason_note: $('.pos-reason-note').val(),
            note: $('.pos-return-note').val(),
            return_lines: this.collectReturnLines()
        };
    }
    
    collectReturnLines() {
        const lines = [];
        $('.pos-return-line').each(function() {
            const line = {
                product_id: $(this).find('.pos-product').val(),
                return_qty: $(this).find('.pos-return-qty').val(),
                original_qty: $(this).find('.pos-original-qty').val(),
                return_reason: $(this).find('.pos-line-return-reason').val(),
                product_condition: $(this).find('.pos-product-condition').val(),
                product_size: $(this).find('.pos-product-size').val(),
                product_color: $(this).find('.pos-product-color').val()
            };
            lines.push(line);
        });
        return lines;
    }
    
    validateReturnData(data) {
        const errors = [];
        
        if (!data.customer_id) {
            errors.push('Customer is required');
        }
        
        if (!data.original_order_id) {
            errors.push('Original order is required');
        }
        
        if (!data.return_reason_id) {
            errors.push('Return reason is required');
        }
        
        if (!data.return_type) {
            errors.push('Return type is required');
        }
        
        if (!data.refund_method) {
            errors.push('Refund method is required');
        }
        
        if (!data.return_lines || data.return_lines.length === 0) {
            errors.push('At least one return line is required');
        }
        
        if (errors.length > 0) {
            this.showNotification(errors.join('\n'), 'error');
            return false;
        }
        
        return true;
    }
    
    resetReturnForm() {
        $('.pos-return-reason').removeClass('selected');
        $('.pos-refund-method').removeClass('selected');
        $('.pos-return-type').val('');
        $('.pos-customer-age').val('');
        $('.pos-refund-percentage').val('');
        $('.pos-refund-amount').val('');
        $('.pos-store-credit-amount').val('');
        $('.pos-store-credit-expiry').val('');
        $('.pos-reason-note').val('');
        $('.pos-return-note').val('');
        $('.pos-return-line').remove();
        $('.pos-return-policy-info').empty();
        $('.pos-store-credit-info').hide();
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-return-notification pos-return-notification-${type} pos-return-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Return Analytics functionality
class POSReturnAnalytics {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadAnalyticsData();
    }
    
    bindEvents() {
        // Bind date range filter
        $(document).on('change', '.pos-return-date-filter', (e) => {
            this.updateDateFilter(e.target.value);
        });
        
        // Bind reason filter
        $(document).on('change', '.pos-return-reason-filter', (e) => {
            this.updateReasonFilter(e.target.value);
        });
    }
    
    loadAnalyticsData() {
        $.ajax({
            url: '/pos_return/analytics_data',
            type: 'GET',
            success: (data) => {
                this.updateAnalytics(data);
            },
            error: (error) => {
                console.error('Error loading return analytics:', error);
            }
        });
    }
    
    updateAnalytics(data) {
        // Update return statistics
        this.updateReturnStats(data.stats);
        
        // Update return trends
        this.updateReturnTrends(data.trends);
        
        // Update reason breakdown
        this.updateReasonBreakdown(data.reasons);
    }
    
    updateReturnStats(stats) {
        $('.pos-return-total-count').text(stats.total_returns);
        $('.pos-return-total-value').text(this.formatCurrency(stats.total_value));
        $('.pos-return-avg-value').text(this.formatCurrency(stats.avg_value));
        $('.pos-return-success-rate').text(`${stats.success_rate}%`);
    }
    
    updateReturnTrends(trends) {
        // This would update charts/graphs
        // Implementation depends on charting library
    }
    
    updateReasonBreakdown(reasons) {
        const container = $('.pos-return-reason-breakdown');
        container.empty();
        
        Object.entries(reasons).forEach(([reason, data]) => {
            const reasonCard = $(`
                <div class="pos-return-reason-card">
                    <div class="reason-name">${reason}</div>
                    <div class="reason-description">${data.description}</div>
                    <div class="reason-policy">Count: ${data.count} | Value: ${this.formatCurrency(data.value)}</div>
                </div>
            `);
            container.append(reasonCard);
        });
    }
    
    updateDateFilter(dateRange) {
        // Reload analytics with new date filter
        this.loadAnalyticsData();
    }
    
    updateReasonFilter(reasonId) {
        // Reload analytics with new reason filter
        this.loadAnalyticsData();
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
}

// Initialize POS Return components when document is ready
$(document).ready(function() {
    // Initialize dashboard if element exists
    if ($('.pos-return-dashboard').length) {
        new POSReturnDashboard();
    }
    
    // Initialize return processor if element exists
    if ($('.pos-return-processor').length) {
        new POSReturnProcessor();
    }
    
    // Initialize analytics if element exists
    if ($('.pos-return-analytics').length) {
        new POSReturnAnalytics();
    }
});