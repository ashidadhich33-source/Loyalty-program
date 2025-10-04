/* POS Payment JavaScript for Kids Clothing ERP */

// POS Payment Dashboard functionality
class POSPaymentDashboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind dashboard refresh button
        $(document).on('click', '.pos-payment-refresh-btn', () => {
            this.refreshDashboard();
        });
        
        // Bind new payment button
        $(document).on('click', '.pos-new-payment-btn', () => {
            this.startNewPayment();
        });
    }
    
    loadDashboardData() {
        // Load dashboard data via AJAX
        $.ajax({
            url: '/pos_payment/dashboard_data',
            type: 'GET',
            success: (data) => {
                this.updateDashboard(data);
            },
            error: (error) => {
                console.error('Error loading payment dashboard data:', error);
            }
        });
    }
    
    updateDashboard(data) {
        // Update dashboard statistics
        $('.pos-payment-today-count').text(data.today_transactions);
        $('.pos-payment-today-value').text(this.formatCurrency(data.today_value));
        
        // Update payment summary
        this.updatePaymentSummary(data.payment_summary);
    }
    
    updatePaymentSummary(summary) {
        const container = $('.pos-payment-summary-stats');
        container.empty();
        
        Object.entries(summary).forEach(([method, data]) => {
            const statCard = $(`
                <div class="pos-payment-stat-card">
                    <div class="stat-value">${data.count}</div>
                    <div class="stat-label">${method}</div>
                    <div class="stat-change">${this.formatCurrency(data.value)}</div>
                </div>
            `);
            container.append(statCard);
        });
    }
    
    refreshDashboard() {
        this.loadDashboardData();
        this.showNotification('Payment dashboard refreshed', 'success');
    }
    
    startNewPayment() {
        // Open new payment wizard
        window.open('/pos_payment/new_payment', '_blank');
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-payment-notification pos-payment-notification-${type} pos-payment-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Payment Processing functionality
class POSPaymentProcessor {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind payment method selection
        $(document).on('click', '.pos-payment-method', (e) => {
            this.selectPaymentMethod($(e.currentTarget));
        });
        
        // Bind terminal selection
        $(document).on('click', '.pos-payment-terminal', (e) => {
            this.selectTerminal($(e.currentTarget));
        });
        
        // Bind amount input
        $(document).on('input', '.pos-payment-amount', (e) => {
            this.updateAmount(e.target.value);
        });
        
        // Bind customer age input
        $(document).on('input', '.pos-customer-age', (e) => {
            this.updateCustomerAge(e.target.value);
        });
        
        // Bind calculate fee button
        $(document).on('click', '.pos-calculate-fee-btn', () => {
            this.calculateFee();
        });
        
        // Bind PIN verification
        $(document).on('click', '.pos-verify-pin-btn', () => {
            this.verifyPIN();
        });
        
        // Bind signature verification
        $(document).on('click', '.pos-verify-signature-btn', () => {
            this.verifySignature();
        });
        
        // Bind process payment button
        $(document).on('click', '.pos-process-payment-btn', () => {
            this.processPayment();
        });
    }
    
    selectPaymentMethod(element) {
        $('.pos-payment-method').removeClass('selected');
        element.addClass('selected');
        
        const methodId = element.data('method-id');
        $('.pos-selected-payment-method').val(methodId);
        
        this.updatePaymentMethodFields(methodId);
    }
    
    updatePaymentMethodFields(methodId) {
        // Get payment method details
        $.ajax({
            url: `/pos_payment/get_method_details/${methodId}`,
            type: 'GET',
            success: (data) => {
                this.displayPaymentMethodInfo(data);
            },
            error: (error) => {
                console.error('Error loading payment method details:', error);
            }
        });
    }
    
    displayPaymentMethodInfo(method) {
        const container = $('.pos-payment-method-info');
        container.empty();
        
        const methodCard = $(`
            <div class="pos-payment-method">
                <div class="method-header">
                    <div class="method-name">${method.name}</div>
                    <div class="method-icon">${method.icon}</div>
                </div>
                <div class="method-details">${method.description}</div>
                <div class="method-fee">Fee: ${method.fee_type === 'percentage' ? method.fee_percentage + '%' : this.formatCurrency(method.fee_amount)}</div>
                <div class="method-limits">Min: ${this.formatCurrency(method.min_amount)} | Max: ${this.formatCurrency(method.max_amount)}</div>
            </div>
        `);
        
        container.append(methodCard);
        
        // Update security requirements
        this.updateSecurityRequirements(method);
    }
    
    updateSecurityRequirements(method) {
        const container = $('.pos-payment-security');
        container.empty();
        
        const securityCard = $(`
            <div class="pos-payment-security ${method.requires_pin || method.requires_signature ? 'warning' : 'success'}">
                <div class="security-title">Security Requirements</div>
                <div class="security-item">
                    <div class="security-icon">${method.requires_pin ? '🔒' : '✅'}</div>
                    <div class="security-text">PIN Verification</div>
                    <div class="security-status ${method.requires_pin ? 'required' : 'verified'}">${method.requires_pin ? 'Required' : 'Not Required'}</div>
                </div>
                <div class="security-item">
                    <div class="security-icon">${method.requires_signature ? '✍️' : '✅'}</div>
                    <div class="security-text">Signature Verification</div>
                    <div class="security-status ${method.requires_signature ? 'required' : 'verified'}">${method.requires_signature ? 'Required' : 'Not Required'}</div>
                </div>
                <div class="security-item">
                    <div class="security-icon">${method.requires_adult_supervision ? '👨‍👩‍👧‍👦' : '✅'}</div>
                    <div class="security-text">Adult Supervision</div>
                    <div class="security-status ${method.requires_adult_supervision ? 'required' : 'verified'}">${method.requires_adult_supervision ? 'Required' : 'Not Required'}</div>
                </div>
            </div>
        `);
        
        container.append(securityCard);
    }
    
    selectTerminal(element) {
        $('.pos-payment-terminal').removeClass('selected');
        element.addClass('selected');
        
        const terminalId = element.data('terminal-id');
        $('.pos-selected-terminal').val(terminalId);
        
        this.updateTerminalFields(terminalId);
    }
    
    updateTerminalFields(terminalId) {
        // Get terminal details
        $.ajax({
            url: `/pos_payment/get_terminal_details/${terminalId}`,
            type: 'GET',
            success: (data) => {
                this.displayTerminalInfo(data);
            },
            error: (error) => {
                console.error('Error loading terminal details:', error);
            }
        });
    }
    
    displayTerminalInfo(terminal) {
        const container = $('.pos-payment-terminal-info');
        container.empty();
        
        const terminalCard = $(`
            <div class="pos-payment-terminal">
                <div class="terminal-header">
                    <div class="terminal-name">${terminal.name}</div>
                    <div class="terminal-status ${terminal.status}">${terminal.status}</div>
                </div>
                <div class="terminal-info">${terminal.description}</div>
                <div class="terminal-stats">
                    <div class="terminal-stat">
                        <div class="stat-value">${terminal.total_transactions}</div>
                        <div class="stat-label">Transactions</div>
                    </div>
                    <div class="terminal-stat">
                        <div class="stat-value">${terminal.success_rate}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                    <div class="terminal-stat">
                        <div class="stat-value">${terminal.average_transaction_time}s</div>
                        <div class="stat-label">Avg Time</div>
                    </div>
                </div>
            </div>
        `);
        
        container.append(terminalCard);
    }
    
    updateAmount(amount) {
        const amountValue = parseFloat(amount) || 0;
        $('.pos-payment-amount-value').text(this.formatCurrency(amountValue));
        
        // Validate amount against payment method limits
        this.validateAmount(amountValue);
    }
    
    validateAmount(amount) {
        const methodId = $('.pos-selected-payment-method').val();
        if (!methodId || amount <= 0) {
            return;
        }
        
        $.ajax({
            url: `/pos_payment/validate_amount/${methodId}/${amount}`,
            type: 'GET',
            success: (data) => {
                if (!data.valid) {
                    this.showNotification(data.message, 'warning');
                }
            },
            error: (error) => {
                console.error('Error validating amount:', error);
            }
        });
    }
    
    updateCustomerAge(age) {
        const methodId = $('.pos-selected-payment-method').val();
        if (methodId && age) {
            $.ajax({
                url: `/pos_payment/validate_age_policy/${methodId}/${age}`,
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
    
    calculateFee() {
        const methodId = $('.pos-selected-payment-method').val();
        const amount = parseFloat($('.pos-payment-amount').val()) || 0;
        
        if (!methodId || amount <= 0) {
            this.showNotification('Please select payment method and enter amount', 'warning');
            return;
        }
        
        $.ajax({
            url: `/pos_payment/calculate_fee/${methodId}/${amount}`,
            type: 'GET',
            success: (data) => {
                this.updateFeeAmounts(data);
            },
            error: (error) => {
                console.error('Error calculating fee:', error);
            }
        });
    }
    
    updateFeeAmounts(data) {
        $('.pos-payment-fee').val(this.formatCurrency(data.fee));
        $('.pos-payment-net-amount').val(this.formatCurrency(data.net_amount));
        
        // Update fee display
        $('.pos-payment-amount-fee').text(`Fee: ${this.formatCurrency(data.fee)}`);
        $('.pos-payment-amount-net').text(`Net: ${this.formatCurrency(data.net_amount)}`);
    }
    
    verifyPIN() {
        // This would integrate with PIN verification system
        $('.pos-pin-verified').val('true');
        $('.pos-verify-pin-btn').text('PIN Verified').addClass('btn-success').removeClass('btn-primary');
        this.showNotification('PIN verified successfully', 'success');
    }
    
    verifySignature() {
        // This would integrate with signature verification system
        $('.pos-signature-verified').val('true');
        $('.pos-verify-signature-btn').text('Signature Verified').addClass('btn-success').removeClass('btn-primary');
        this.showNotification('Signature verified successfully', 'success');
    }
    
    processPayment() {
        const paymentData = this.collectPaymentData();
        
        if (!this.validatePaymentData(paymentData)) {
            return;
        }
        
        $.ajax({
            url: '/pos_payment/process_payment',
            type: 'POST',
            data: paymentData,
            success: (response) => {
                this.showNotification('Payment processed successfully', 'success');
                this.resetPaymentForm();
                // Redirect to transaction details
                window.location.href = `/pos_payment/view_transaction/${response.transaction_id}`;
            },
            error: (error) => {
                this.showNotification('Error processing payment', 'error');
            }
        });
    }
    
    collectPaymentData() {
        return {
            session_id: $('.pos-session-id').val(),
            order_id: $('.pos-order-id').val(),
            payment_method_id: $('.pos-selected-payment-method').val(),
            terminal_id: $('.pos-selected-terminal').val(),
            amount: $('.pos-payment-amount').val(),
            customer_age: $('.pos-customer-age').val(),
            payment_reference: $('.pos-payment-reference').val(),
            card_number: $('.pos-card-number').val(),
            card_type: $('.pos-card-type').val(),
            card_holder_name: $('.pos-card-holder-name').val(),
            upi_id: $('.pos-upi-id').val(),
            wallet_provider: $('.pos-wallet-provider').val(),
            wallet_transaction_id: $('.pos-wallet-transaction-id').val(),
            pin_verified: $('.pos-pin-verified').val(),
            signature_verified: $('.pos-signature-verified').val(),
            note: $('.pos-payment-note').val()
        };
    }
    
    validatePaymentData(data) {
        const errors = [];
        
        if (!data.payment_method_id) {
            errors.push('Payment method is required');
        }
        
        if (!data.amount || data.amount <= 0) {
            errors.push('Payment amount must be greater than 0');
        }
        
        if (!data.session_id) {
            errors.push('Session is required');
        }
        
        if (!data.order_id) {
            errors.push('Order is required');
        }
        
        if (errors.length > 0) {
            this.showNotification(errors.join('\n'), 'error');
            return false;
        }
        
        return true;
    }
    
    resetPaymentForm() {
        $('.pos-payment-method').removeClass('selected');
        $('.pos-payment-terminal').removeClass('selected');
        $('.pos-selected-payment-method').val('');
        $('.pos-selected-terminal').val('');
        $('.pos-payment-amount').val('');
        $('.pos-customer-age').val('');
        $('.pos-payment-reference').val('');
        $('.pos-card-number').val('');
        $('.pos-card-type').val('');
        $('.pos-card-holder-name').val('');
        $('.pos-upi-id').val('');
        $('.pos-wallet-provider').val('');
        $('.pos-wallet-transaction-id').val('');
        $('.pos-pin-verified').val('');
        $('.pos-signature-verified').val('');
        $('.pos-payment-note').val('');
        $('.pos-payment-method-info').empty();
        $('.pos-payment-terminal-info').empty();
        $('.pos-payment-security').empty();
        $('.pos-payment-fee').val('');
        $('.pos-payment-net-amount').val('');
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-payment-notification pos-payment-notification-${type} pos-payment-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Payment Analytics functionality
class POSPaymentAnalytics {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadAnalyticsData();
    }
    
    bindEvents() {
        // Bind date range filter
        $(document).on('change', '.pos-payment-date-filter', (e) => {
            this.updateDateFilter(e.target.value);
        });
        
        // Bind payment method filter
        $(document).on('change', '.pos-payment-method-filter', (e) => {
            this.updatePaymentMethodFilter(e.target.value);
        });
        
        // Bind terminal filter
        $(document).on('change', '.pos-payment-terminal-filter', (e) => {
            this.updateTerminalFilter(e.target.value);
        });
    }
    
    loadAnalyticsData() {
        $.ajax({
            url: '/pos_payment/analytics_data',
            type: 'GET',
            success: (data) => {
                this.updateAnalytics(data);
            },
            error: (error) => {
                console.error('Error loading payment analytics:', error);
            }
        });
    }
    
    updateAnalytics(data) {
        // Update payment statistics
        this.updatePaymentStats(data.stats);
        
        // Update payment trends
        this.updatePaymentTrends(data.trends);
        
        // Update method breakdown
        this.updateMethodBreakdown(data.methods);
        
        // Update terminal performance
        this.updateTerminalPerformance(data.terminals);
    }
    
    updatePaymentStats(stats) {
        $('.pos-payment-total-count').text(stats.total_transactions);
        $('.pos-payment-total-value').text(this.formatCurrency(stats.total_value));
        $('.pos-payment-avg-value').text(this.formatCurrency(stats.avg_value));
        $('.pos-payment-success-rate').text(`${stats.success_rate}%`);
        $('.pos-payment-fee-total').text(this.formatCurrency(stats.total_fees));
    }
    
    updatePaymentTrends(trends) {
        // This would update charts/graphs
        // Implementation depends on charting library
    }
    
    updateMethodBreakdown(methods) {
        const container = $('.pos-payment-method-breakdown');
        container.empty();
        
        Object.entries(methods).forEach(([method, data]) => {
            const methodCard = $(`
                <div class="pos-payment-method-card">
                    <div class="method-name">${method}</div>
                    <div class="method-description">${data.description}</div>
                    <div class="method-policy">Count: ${data.count} | Value: ${this.formatCurrency(data.value)} | Fee: ${this.formatCurrency(data.fee)}</div>
                </div>
            `);
            container.append(methodCard);
        });
    }
    
    updateTerminalPerformance(terminals) {
        const container = $('.pos-payment-terminal-performance');
        container.empty();
        
        Object.entries(terminals).forEach(([terminal, data]) => {
            const terminalCard = $(`
                <div class="pos-payment-terminal-card">
                    <div class="terminal-name">${terminal}</div>
                    <div class="terminal-info">${data.description}</div>
                    <div class="terminal-stats">
                        <div class="terminal-stat">
                            <div class="stat-value">${data.transactions}</div>
                            <div class="stat-label">Transactions</div>
                        </div>
                        <div class="terminal-stat">
                            <div class="stat-value">${data.success_rate}%</div>
                            <div class="stat-label">Success Rate</div>
                        </div>
                        <div class="terminal-stat">
                            <div class="stat-value">${data.avg_time}s</div>
                            <div class="stat-label">Avg Time</div>
                        </div>
                    </div>
                </div>
            `);
            container.append(terminalCard);
        });
    }
    
    updateDateFilter(dateRange) {
        // Reload analytics with new date filter
        this.loadAnalyticsData();
    }
    
    updatePaymentMethodFilter(methodId) {
        // Reload analytics with new payment method filter
        this.loadAnalyticsData();
    }
    
    updateTerminalFilter(terminalId) {
        // Reload analytics with new terminal filter
        this.loadAnalyticsData();
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
}

// Initialize POS Payment components when document is ready
$(document).ready(function() {
    // Initialize dashboard if element exists
    if ($('.pos-payment-dashboard').length) {
        new POSPaymentDashboard();
    }
    
    // Initialize payment processor if element exists
    if ($('.pos-payment-processor').length) {
        new POSPaymentProcessor();
    }
    
    // Initialize analytics if element exists
    if ($('.pos-payment-analytics').length) {
        new POSPaymentAnalytics();
    }
});