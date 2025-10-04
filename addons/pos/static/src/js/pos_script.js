/* POS JavaScript for Kids Clothing ERP */

// POS Dashboard functionality
class POSDashboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind dashboard refresh button
        $(document).on('click', '.pos-refresh-btn', () => {
            this.refreshDashboard();
        });
        
        // Bind session start button
        $(document).on('click', '.pos-start-session-btn', () => {
            this.startSession();
        });
        
        // Bind session close button
        $(document).on('click', '.pos-close-session-btn', () => {
            this.closeSession();
        });
    }
    
    loadDashboardData() {
        // Load dashboard data via AJAX
        $.ajax({
            url: '/pos/dashboard_data',
            type: 'GET',
            success: (data) => {
                this.updateDashboard(data);
            },
            error: (error) => {
                console.error('Error loading dashboard data:', error);
            }
        });
    }
    
    updateDashboard(data) {
        // Update dashboard statistics
        $('.pos-today-sales').text(data.today_sales);
        $('.pos-today-revenue').text(this.formatCurrency(data.today_revenue));
        
        // Update session info
        if (data.session_info.has_active_session) {
            $('.pos-session-status').html(`
                <div class="pos-session-card active">
                    <div class="session-info">
                        <div>
                            <strong>Active Session:</strong> ${data.session_info.session_user}
                        </div>
                        <div class="session-status opened">OPENED</div>
                    </div>
                    <div class="session-details">
                        Started: ${this.formatDateTime(data.session_info.session_start)}
                    </div>
                </div>
            `);
        } else {
            $('.pos-session-status').html(`
                <div class="pos-session-card">
                    <div class="session-info">
                        <div><strong>No Active Session</strong></div>
                        <div class="session-status closed">CLOSED</div>
                    </div>
                </div>
            `);
        }
    }
    
    refreshDashboard() {
        this.loadDashboardData();
        this.showNotification('Dashboard refreshed', 'success');
    }
    
    startSession() {
        if (confirm('Start a new POS session?')) {
            $.ajax({
                url: '/pos/start_session',
                type: 'POST',
                success: (response) => {
                    this.showNotification('Session started successfully', 'success');
                    this.loadDashboardData();
                },
                error: (error) => {
                    this.showNotification('Error starting session', 'error');
                }
            });
        }
    }
    
    closeSession() {
        if (confirm('Close the current session?')) {
            $.ajax({
                url: '/pos/close_session',
                type: 'POST',
                success: (response) => {
                    this.showNotification('Session closed successfully', 'success');
                    this.loadDashboardData();
                },
                error: (error) => {
                    this.showNotification('Error closing session', 'error');
                }
            });
        }
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    formatDateTime(dateString) {
        return new Date(dateString).toLocaleString('en-IN');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = $(`
            <div class="pos-notification pos-notification-${type} pos-fade-in">
                ${message}
            </div>
        `);
        
        // Add to page
        $('body').append(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Customer Management functionality
class POSCustomerManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind customer search
        $(document).on('input', '.pos-customer-search', (e) => {
            this.searchCustomers(e.target.value);
        });
        
        // Bind create customer button
        $(document).on('click', '.pos-create-customer-btn', () => {
            this.openCustomerWizard();
        });
        
        // Bind customer selection
        $(document).on('click', '.pos-customer-item', (e) => {
            const customerId = $(e.currentTarget).data('customer-id');
            this.selectCustomer(customerId);
        });
    }
    
    searchCustomers(query) {
        if (query.length < 2) {
            $('.pos-customer-results').hide();
            return;
        }
        
        $.ajax({
            url: '/pos/search_customers',
            type: 'GET',
            data: { q: query },
            success: (customers) => {
                this.displayCustomerResults(customers);
            },
            error: (error) => {
                console.error('Error searching customers:', error);
            }
        });
    }
    
    displayCustomerResults(customers) {
        const container = $('.pos-customer-results');
        container.empty();
        
        if (customers.length === 0) {
            container.html(`
                <div class="pos-no-customers">
                    <p>No customers found</p>
                    <button class="pos-create-customer-btn btn btn-primary">Create New Customer</button>
                </div>
            `);
        } else {
            customers.forEach(customer => {
                const customerItem = $(`
                    <div class="pos-customer-item" data-customer-id="${customer.id}">
                        <div class="customer-name">${customer.name}</div>
                        <div class="customer-details">
                            ${customer.email ? `<div class="customer-email">${customer.email}</div>` : ''}
                            ${customer.phone ? `<div class="customer-phone">${customer.phone}</div>` : ''}
                        </div>
                    </div>
                `);
                container.append(customerItem);
            });
        }
        
        container.show();
    }
    
    selectCustomer(customerId) {
        // Set customer in POS order
        $('.pos-customer-field').val(customerId);
        $('.pos-customer-results').hide();
        
        // Load customer details
        this.loadCustomerDetails(customerId);
    }
    
    loadCustomerDetails(customerId) {
        $.ajax({
            url: '/pos/customer_details',
            type: 'GET',
            data: { customer_id: customerId },
            success: (customer) => {
                this.displayCustomerInfo(customer);
            },
            error: (error) => {
                console.error('Error loading customer details:', error);
            }
        });
    }
    
    displayCustomerInfo(customer) {
        $('.pos-customer-info').html(`
            <div class="customer-card">
                <div class="customer-header">
                    <h4>${customer.name}</h4>
                    <span class="customer-type">${customer.customer_type}</span>
                </div>
                <div class="customer-details">
                    ${customer.email ? `<div><strong>Email:</strong> ${customer.email}</div>` : ''}
                    ${customer.phone ? `<div><strong>Phone:</strong> ${customer.phone}</div>` : ''}
                    ${customer.loyalty_points ? `<div><strong>Loyalty Points:</strong> ${customer.loyalty_points}</div>` : ''}
                    ${customer.loyalty_level ? `<div><strong>Loyalty Level:</strong> ${customer.loyalty_level}</div>` : ''}
                </div>
            </div>
        `);
    }
    
    openCustomerWizard() {
        // Open customer creation wizard
        window.open('/pos/customer_wizard', '_blank', 'width=800,height=600');
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-notification pos-notification-${type} pos-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// POS Loyalty Points Management functionality
class POSLoyaltyManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind loyalty points redemption button
        $(document).on('click', '.pos-redeem-loyalty-btn', () => {
            this.openLoyaltyWizard();
        });
        
        // Bind loyalty points display
        $(document).on('change', '.pos-customer-field', (e) => {
            this.loadCustomerLoyaltyInfo(e.target.value);
        });
        
        // Bind quick redemption buttons
        $(document).on('click', '.pos-quick-redeem-btn', (e) => {
            const points = $(e.currentTarget).data('points');
            this.quickRedeemPoints(points);
        });
    }
    
    loadCustomerLoyaltyInfo(customerId) {
        if (!customerId) {
            $('.pos-loyalty-info').hide();
            return;
        }
        
        $.ajax({
            url: '/pos/customer_loyalty_info',
            type: 'GET',
            data: { customer_id: customerId },
            success: (loyaltyInfo) => {
                this.displayLoyaltyInfo(loyaltyInfo);
            },
            error: (error) => {
                console.error('Error loading loyalty info:', error);
            }
        });
    }
    
    displayLoyaltyInfo(loyaltyInfo) {
        if (loyaltyInfo.available_points > 0) {
            $('.pos-loyalty-info').html(`
                <div class="loyalty-card">
                    <div class="loyalty-header">
                        <h4>Loyalty Points</h4>
                        <span class="loyalty-level ${loyaltyInfo.loyalty_level}">${loyaltyInfo.loyalty_level.toUpperCase()}</span>
                    </div>
                    <div class="loyalty-details">
                        <div class="loyalty-points">
                            <strong>Available Points:</strong> ${loyaltyInfo.available_points}
                        </div>
                        <div class="loyalty-discount">
                            <strong>Max Discount:</strong> ₹${loyaltyInfo.max_discount.toFixed(2)}
                        </div>
                        <div class="loyalty-rate">
                            <strong>Rate:</strong> ${loyaltyInfo.points_rate} points = ₹1
                        </div>
                    </div>
                    <div class="loyalty-actions">
                        <button class="pos-redeem-loyalty-btn btn btn-primary">Redeem Points</button>
                        <div class="quick-redeem">
                            <button class="pos-quick-redeem-btn btn btn-sm btn-outline-primary" data-points="100">100 pts</button>
                            <button class="pos-quick-redeem-btn btn btn-sm btn-outline-primary" data-points="500">500 pts</button>
                            <button class="pos-quick-redeem-btn btn btn-sm btn-outline-primary" data-points="1000">1000 pts</button>
                            <button class="pos-quick-redeem-btn btn btn-sm btn-outline-primary" data-points="${loyaltyInfo.available_points}">Max</button>
                        </div>
                    </div>
                </div>
            `).show();
        } else {
            $('.pos-loyalty-info').html(`
                <div class="loyalty-card no-points">
                    <div class="loyalty-header">
                        <h4>Loyalty Points</h4>
                    </div>
                    <div class="loyalty-details">
                        <p>No loyalty points available</p>
                        <p>Start earning points with your purchases!</p>
                    </div>
                </div>
            `).show();
        }
    }
    
    openLoyaltyWizard() {
        // Open loyalty points redemption wizard
        const orderId = $('.pos-order-id').val();
        if (!orderId) {
            this.showNotification('Please save the order first', 'warning');
            return;
        }
        
        window.open(`/pos/loyalty_wizard?order_id=${orderId}`, '_blank', 'width=600,height=500');
    }
    
    quickRedeemPoints(points) {
        const orderId = $('.pos-order-id').val();
        if (!orderId) {
            this.showNotification('Please save the order first', 'warning');
            return;
        }
        
        if (confirm(`Redeem ${points} loyalty points?`)) {
            $.ajax({
                url: '/pos/redeem_loyalty_points',
                type: 'POST',
                data: { 
                    order_id: orderId,
                    points: points
                },
                success: (response) => {
                    this.showNotification('Loyalty points redeemed successfully', 'success');
                    this.updateOrderTotal(response.discount_amount);
                    this.loadCustomerLoyaltyInfo($('.pos-customer-field').val());
                },
                error: (error) => {
                    this.showNotification('Error redeeming loyalty points', 'error');
                }
            });
        }
    }
    
    updateOrderTotal(discountAmount) {
        const currentTotal = parseFloat($('.pos-order-total').text());
        const newTotal = currentTotal - discountAmount;
        $('.pos-order-total').text(newTotal.toFixed(2));
        
        // Update discount display
        $('.pos-loyalty-discount').text(`₹${discountAmount.toFixed(2)}`);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="pos-notification pos-notification-${type} pos-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize POS components when document is ready
$(document).ready(function() {
    // Initialize dashboard if element exists
    if ($('.pos-dashboard').length) {
        new POSDashboard();
    }
    
    // Initialize product grid if element exists
    if ($('.pos-product-grid').length) {
        new POSProductGrid();
    }
    
    // Initialize customer manager if element exists
    if ($('.pos-customer-section').length) {
        new POSCustomerManager();
    }
    
    // Initialize loyalty manager if element exists
    if ($('.pos-loyalty-section').length) {
        new POSLoyaltyManager();
    }
});