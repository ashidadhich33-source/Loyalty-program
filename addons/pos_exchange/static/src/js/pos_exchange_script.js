/* POS Exchange JavaScript for Kids Clothing ERP */

// POS Exchange Dashboard functionality
class POSExchangeDashboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind dashboard refresh button
        $(document).on('click', '.pos-exchange-refresh-btn', () => {
            this.refreshDashboard();
        });
        
        // Bind new exchange button
        $(document).on('click', '.pos-new-exchange-btn', () => {
            this.startNewExchange();
        });
    }
    
    loadDashboardData() {
        // Load dashboard data via AJAX
        $.ajax({
            url: '/pos_exchange/dashboard_data',
            type: 'GET',
            success: (data) => {
                this.updateDashboard(data);
            },
            error: (error) => {
                console.error('Error loading exchange dashboard data:', error);
            }
        });
    }
    
    updateDashboard(data) {
        // Update dashboard statistics
        $('.pos-exchange-today-count').text(data.today_exchanges);
        $('.pos-exchange-today-value').text(this.formatCurrency(data.today_value));
        
        // Update exchange summary
        this.updateExchangeSummary(data.exchange_summary);
    }
    
    updateExchangeSummary(summary) {
        const container = $('.pos-exchange-summary-stats');
        container.empty();
        
        Object.entries(summary).forEach(([reason, count]) => {
            const statCard = $(`
                <div class="pos-exchange-stat-card">
                    <div class="stat-value">${count}</div>
                    <div class="stat-label">${reason}</div>
                </div>
            `);
            container.append(statCard);
        });
    }
    
    refreshDashboard() {
        this.loadDashboardData();
        this.showNotification('Exchange dashboard refreshed', 'success');
    }
    
    startNewExchange() {
        // Open new exchange wizard
        window.open('/pos_exchange/new_exchange', '_blank');
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-exchange-notification pos-exchange-notification-${type} pos-exchange-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Exchange Processing functionality
class POSExchangeProcessor {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind exchange reason selection
        $(document).on('click', '.pos-exchange-reason', (e) => {
            this.selectExchangeReason($(e.currentTarget));
        });
        
        // Bind exchange type selection
        $(document).on('change', '.pos-exchange-type', (e) => {
            this.updateExchangeType(e.target.value);
        });
        
        // Bind customer age input
        $(document).on('input', '.pos-customer-age', (e) => {
            this.updateCustomerAge(e.target.value);
        });
        
        // Bind process exchange button
        $(document).on('click', '.pos-process-exchange-btn', () => {
            this.processExchange();
        });
    }
    
    selectExchangeReason(element) {
        $('.pos-exchange-reason').removeClass('selected');
        element.addClass('selected');
        
        const reasonId = element.data('reason-id');
        $('.pos-selected-exchange-reason').val(reasonId);
        
        this.updateExchangePolicy(reasonId);
    }
    
    updateExchangePolicy(reasonId) {
        // Get exchange reason details
        $.ajax({
            url: `/pos_exchange/get_reason_policy/${reasonId}`,
            type: 'GET',
            success: (data) => {
                this.displayExchangePolicy(data);
            },
            error: (error) => {
                console.error('Error loading exchange policy:', error);
            }
        });
    }
    
    displayExchangePolicy(policy) {
        const container = $('.pos-exchange-policy-info');
        container.empty();
        
        const policyCard = $(`
            <div class="pos-exchange-policy ${policy.within_policy ? 'success' : 'warning'}">
                <h4>Exchange Policy</h4>
                <p><strong>Max Period:</strong> ${policy.max_exchange_period} days</p>
                <p><strong>Size Changes:</strong> ${policy.allow_size_change ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Color Changes:</strong> ${policy.allow_color_change ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Style Changes:</strong> ${policy.allow_style_change ? 'Allowed' : 'Not Allowed'}</p>
                <p><strong>Refunds:</strong> ${policy.allow_refund ? 'Allowed' : 'Not Allowed'}</p>
                ${policy.age_group_restriction !== 'none' ? `<p><strong>Age Restriction:</strong> ${policy.age_group_restriction}</p>` : ''}
            </div>
        `);
        
        container.append(policyCard);
    }
    
    updateExchangeType(type) {
        // Update exchange type specific fields
        if (type === 'size_change') {
            $('.pos-size-change-fields').show();
            $('.pos-color-change-fields').hide();
            $('.pos-style-change-fields').hide();
        } else if (type === 'color_change') {
            $('.pos-size-change-fields').hide();
            $('.pos-color-change-fields').show();
            $('.pos-style-change-fields').hide();
        } else if (type === 'style_change') {
            $('.pos-size-change-fields').hide();
            $('.pos-color-change-fields').hide();
            $('.pos-style-change-fields').show();
        } else {
            $('.pos-size-change-fields').hide();
            $('.pos-color-change-fields').hide();
            $('.pos-style-change-fields').hide();
        }
    }
    
    updateCustomerAge(age) {
        // Validate age-based policies
        const reasonId = $('.pos-selected-exchange-reason').val();
        if (reasonId && age) {
            $.ajax({
                url: `/pos_exchange/validate_age_policy/${reasonId}/${age}`,
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
    
    processExchange() {
        const exchangeData = this.collectExchangeData();
        
        if (!this.validateExchangeData(exchangeData)) {
            return;
        }
        
        $.ajax({
            url: '/pos_exchange/process_exchange',
            type: 'POST',
            data: exchangeData,
            success: (response) => {
                this.showNotification('Exchange processed successfully', 'success');
                this.resetExchangeForm();
                // Redirect to exchange details
                window.location.href = `/pos_exchange/view/${response.exchange_id}`;
            },
            error: (error) => {
                this.showNotification('Error processing exchange', 'error');
            }
        });
    }
    
    collectExchangeData() {
        return {
            customer_id: $('.pos-customer-id').val(),
            original_order_id: $('.pos-original-order-id').val(),
            exchange_reason_id: $('.pos-selected-exchange-reason').val(),
            exchange_type: $('.pos-exchange-type').val(),
            customer_age: $('.pos-customer-age').val(),
            reason_note: $('.pos-reason-note').val(),
            note: $('.pos-exchange-note').val(),
            exchange_lines: this.collectExchangeLines()
        };
    }
    
    collectExchangeLines() {
        const lines = [];
        $('.pos-exchange-line').each(function() {
            const line = {
                original_product_id: $(this).find('.pos-original-product').val(),
                new_product_id: $(this).find('.pos-new-product').val(),
                return_qty: $(this).find('.pos-return-qty').val(),
                exchange_qty: $(this).find('.pos-exchange-qty').val(),
                exchange_reason: $(this).find('.pos-line-exchange-reason').val(),
                original_size: $(this).find('.pos-original-size').val(),
                new_size: $(this).find('.pos-new-size').val(),
                original_color: $(this).find('.pos-original-color').val(),
                new_color: $(this).find('.pos-new-color').val()
            };
            lines.push(line);
        });
        return lines;
    }
    
    validateExchangeData(data) {
        const errors = [];
        
        if (!data.customer_id) {
            errors.push('Customer is required');
        }
        
        if (!data.original_order_id) {
            errors.push('Original order is required');
        }
        
        if (!data.exchange_reason_id) {
            errors.push('Exchange reason is required');
        }
        
        if (!data.exchange_type) {
            errors.push('Exchange type is required');
        }
        
        if (!data.exchange_lines || data.exchange_lines.length === 0) {
            errors.push('At least one exchange line is required');
        }
        
        if (errors.length > 0) {
            this.showNotification(errors.join('\n'), 'error');
            return false;
        }
        
        return true;
    }
    
    resetExchangeForm() {
        $('.pos-exchange-reason').removeClass('selected');
        $('.pos-exchange-type').val('');
        $('.pos-customer-age').val('');
        $('.pos-reason-note').val('');
        $('.pos-exchange-note').val('');
        $('.pos-exchange-line').remove();
        $('.pos-exchange-policy-info').empty();
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-exchange-notification pos-exchange-notification-${type} pos-exchange-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Exchange Analytics functionality
class POSExchangeAnalytics {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadAnalyticsData();
    }
    
    bindEvents() {
        // Bind date range filter
        $(document).on('change', '.pos-exchange-date-filter', (e) => {
            this.updateDateFilter(e.target.value);
        });
        
        // Bind reason filter
        $(document).on('change', '.pos-exchange-reason-filter', (e) => {
            this.updateReasonFilter(e.target.value);
        });
    }
    
    loadAnalyticsData() {
        $.ajax({
            url: '/pos_exchange/analytics_data',
            type: 'GET',
            success: (data) => {
                this.updateAnalytics(data);
            },
            error: (error) => {
                console.error('Error loading exchange analytics:', error);
            }
        });
    }
    
    updateAnalytics(data) {
        // Update exchange statistics
        this.updateExchangeStats(data.stats);
        
        // Update exchange trends
        this.updateExchangeTrends(data.trends);
        
        // Update reason breakdown
        this.updateReasonBreakdown(data.reasons);
    }
    
    updateExchangeStats(stats) {
        $('.pos-exchange-total-count').text(stats.total_exchanges);
        $('.pos-exchange-total-value').text(this.formatCurrency(stats.total_value));
        $('.pos-exchange-avg-value').text(this.formatCurrency(stats.avg_value));
        $('.pos-exchange-success-rate').text(`${stats.success_rate}%`);
    }
    
    updateExchangeTrends(trends) {
        // This would update charts/graphs
        // Implementation depends on charting library
    }
    
    updateReasonBreakdown(reasons) {
        const container = $('.pos-exchange-reason-breakdown');
        container.empty();
        
        Object.entries(reasons).forEach(([reason, data]) => {
            const reasonCard = $(`
                <div class="pos-exchange-reason-card">
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

// Initialize POS Exchange components when document is ready
$(document).ready(function() {
    // Initialize dashboard if element exists
    if ($('.pos-exchange-dashboard').length) {
        new POSExchangeDashboard();
    }
    
    // Initialize exchange processor if element exists
    if ($('.pos-exchange-processor').length) {
        new POSExchangeProcessor();
    }
    
    // Initialize analytics if element exists
    if ($('.pos-exchange-analytics').length) {
        new POSExchangeAnalytics();
    }
});