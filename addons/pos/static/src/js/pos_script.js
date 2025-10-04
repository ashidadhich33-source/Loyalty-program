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

// POS Product Grid functionality
class POSProductGrid {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadProducts();
    }
    
    bindEvents() {
        // Bind product search
        $(document).on('input', '.pos-product-search', (e) => {
            this.searchProducts(e.target.value);
        });
        
        // Bind category filter
        $(document).on('change', '.pos-category-filter', (e) => {
            this.filterByCategory(e.target.value);
        });
        
        // Bind product click
        $(document).on('click', '.pos-product-card', (e) => {
            const productId = $(e.currentTarget).data('product-id');
            this.addToCart(productId);
        });
    }
    
    loadProducts() {
        $.ajax({
            url: '/pos/products',
            type: 'GET',
            success: (data) => {
                this.renderProducts(data);
            },
            error: (error) => {
                console.error('Error loading products:', error);
            }
        });
    }
    
    renderProducts(products) {
        const container = $('.pos-product-grid');
        container.empty();
        
        products.forEach(product => {
            const productCard = $(`
                <div class="pos-product-card" data-product-id="${product.id}">
                    <div class="product-image">
                        ${product.image ? `<img src="${product.image}" alt="${product.name}">` : 'No Image'}
                    </div>
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">${this.formatCurrency(product.price)}</div>
                    <div class="product-code">${product.code}</div>
                </div>
            `);
            
            container.append(productCard);
        });
    }
    
    searchProducts(query) {
        $('.pos-product-card').each(function() {
            const productName = $(this).find('.product-name').text().toLowerCase();
            const productCode = $(this).find('.product-code').text().toLowerCase();
            const searchQuery = query.toLowerCase();
            
            if (productName.includes(searchQuery) || productCode.includes(searchQuery)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
    
    filterByCategory(categoryId) {
        if (categoryId === '') {
            $('.pos-product-card').show();
        } else {
            $('.pos-product-card').each(function() {
                const productCategory = $(this).data('category-id');
                if (productCategory == categoryId) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }
    }
    
    addToCart(productId) {
        $.ajax({
            url: '/pos/add_to_cart',
            type: 'POST',
            data: { product_id: productId },
            success: (response) => {
                this.showNotification('Product added to cart', 'success');
                this.updateCartDisplay();
            },
            error: (error) => {
                this.showNotification('Error adding product to cart', 'error');
            }
        });
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
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
    
    updateCartDisplay() {
        // This would update the cart display
        // Implementation depends on cart structure
    }
}

// POS Cart functionality
class POSCart {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadCart();
    }
    
    bindEvents() {
        // Bind quantity change
        $(document).on('click', '.quantity-btn', (e) => {
            const action = $(e.currentTarget).data('action');
            const productId = $(e.currentTarget).data('product-id');
            this.updateQuantity(productId, action);
        });
        
        // Bind quantity input change
        $(document).on('change', '.quantity-input', (e) => {
            const productId = $(e.currentTarget).data('product-id');
            const quantity = parseInt(e.target.value);
            this.setQuantity(productId, quantity);
        });
        
        // Bind remove item
        $(document).on('click', '.pos-remove-item', (e) => {
            const productId = $(e.currentTarget).data('product-id');
            this.removeItem(productId);
        });
        
        // Bind checkout
        $(document).on('click', '.pos-checkout-btn', () => {
            this.checkout();
        });
    }
    
    loadCart() {
        $.ajax({
            url: '/pos/cart',
            type: 'GET',
            success: (data) => {
                this.renderCart(data);
            },
            error: (error) => {
                console.error('Error loading cart:', error);
            }
        });
    }
    
    renderCart(cart) {
        const container = $('.pos-cart-items');
        container.empty();
        
        cart.items.forEach(item => {
            const cartItem = $(`
                <div class="pos-cart-item" data-product-id="${item.product_id}">
                    <div class="item-info">
                        <div class="item-name">${item.product_name}</div>
                        <div class="item-price">${this.formatCurrency(item.price_unit)}</div>
                    </div>
                    <div class="item-controls">
                        <div class="quantity-control">
                            <button class="quantity-btn" data-action="decrease" data-product-id="${item.product_id}">-</button>
                            <input type="number" class="quantity-input" value="${item.qty}" data-product-id="${item.product_id}" min="1">
                            <button class="quantity-btn" data-action="increase" data-product-id="${item.product_id}">+</button>
                        </div>
                        <div class="item-total">${this.formatCurrency(item.price_total)}</div>
                        <button class="pos-remove-item" data-product-id="${item.product_id}">×</button>
                    </div>
                </div>
            `);
            
            container.append(cartItem);
        });
        
        this.updateCartTotal(cart);
    }
    
    updateQuantity(productId, action) {
        $.ajax({
            url: '/pos/update_quantity',
            type: 'POST',
            data: { 
                product_id: productId, 
                action: action 
            },
            success: (response) => {
                this.loadCart();
            },
            error: (error) => {
                this.showNotification('Error updating quantity', 'error');
            }
        });
    }
    
    setQuantity(productId, quantity) {
        if (quantity < 1) {
            this.removeItem(productId);
            return;
        }
        
        $.ajax({
            url: '/pos/set_quantity',
            type: 'POST',
            data: { 
                product_id: productId, 
                quantity: quantity 
            },
            success: (response) => {
                this.loadCart();
            },
            error: (error) => {
                this.showNotification('Error updating quantity', 'error');
            }
        });
    }
    
    removeItem(productId) {
        if (confirm('Remove this item from cart?')) {
            $.ajax({
                url: '/pos/remove_item',
                type: 'POST',
                data: { product_id: productId },
                success: (response) => {
                    this.loadCart();
                    this.showNotification('Item removed from cart', 'success');
                },
                error: (error) => {
                    this.showNotification('Error removing item', 'error');
                }
            });
        }
    }
    
    checkout() {
        if ($('.pos-cart-item').length === 0) {
            this.showNotification('Cart is empty', 'warning');
            return;
        }
        
        if (confirm('Proceed to checkout?')) {
            $.ajax({
                url: '/pos/checkout',
                type: 'POST',
                success: (response) => {
                    this.showNotification('Order created successfully', 'success');
                    this.loadCart(); // Clear cart
                },
                error: (error) => {
                    this.showNotification('Error during checkout', 'error');
                }
            });
        }
    }
    
    updateCartTotal(cart) {
        $('.pos-cart-subtotal').text(this.formatCurrency(cart.amount_untaxed));
        $('.pos-cart-tax').text(this.formatCurrency(cart.amount_tax));
        $('.pos-cart-discount').text(this.formatCurrency(cart.amount_discount));
        $('.pos-cart-total').text(this.formatCurrency(cart.amount_total));
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
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
    
    // Initialize cart if element exists
    if ($('.pos-cart-items').length) {
        new POSCart();
    }
});

// POS Payment functionality
class POSPayment {
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
        
        // Bind payment amount input
        $(document).on('input', '.pos-payment-amount', (e) => {
            this.updatePaymentAmount();
        });
        
        // Bind process payment
        $(document).on('click', '.pos-process-payment', () => {
            this.processPayment();
        });
    }
    
    selectPaymentMethod(element) {
        $('.pos-payment-method').removeClass('selected');
        element.addClass('selected');
        
        const methodId = element.data('method-id');
        $('.pos-selected-payment-method').val(methodId);
        
        this.updatePaymentForm();
    }
    
    updatePaymentForm() {
        const selectedMethod = $('.pos-payment-method.selected');
        const isCash = selectedMethod.data('is-cash');
        const isDigital = selectedMethod.data('is-digital');
        
        if (isCash) {
            $('.pos-cash-amount-group').show();
            $('.pos-digital-payment-group').hide();
        } else if (isDigital) {
            $('.pos-cash-amount-group').hide();
            $('.pos-digital-payment-group').show();
        } else {
            $('.pos-cash-amount-group').hide();
            $('.pos-digital-payment-group').hide();
        }
    }
    
    updatePaymentAmount() {
        const amount = parseFloat($('.pos-payment-amount').val()) || 0;
        const total = parseFloat($('.pos-cart-total').text().replace(/[^\d.-]/g, '')) || 0;
        
        if (amount > total) {
            const change = amount - total;
            $('.pos-change-amount').text(this.formatCurrency(change));
            $('.pos-change-group').show();
        } else {
            $('.pos-change-group').hide();
        }
    }
    
    processPayment() {
        const paymentMethodId = $('.pos-selected-payment-method').val();
        const amount = parseFloat($('.pos-payment-amount').val()) || 0;
        
        if (!paymentMethodId) {
            this.showNotification('Please select a payment method', 'warning');
            return;
        }
        
        if (amount <= 0) {
            this.showNotification('Please enter payment amount', 'warning');
            return;
        }
        
        $.ajax({
            url: '/pos/process_payment',
            type: 'POST',
            data: {
                payment_method_id: paymentMethodId,
                amount: amount
            },
            success: (response) => {
                this.showNotification('Payment processed successfully', 'success');
                this.resetPaymentForm();
            },
            error: (error) => {
                this.showNotification('Error processing payment', 'error');
            }
        });
    }
    
    resetPaymentForm() {
        $('.pos-payment-method').removeClass('selected');
        $('.pos-payment-amount').val('');
        $('.pos-cash-amount-group').hide();
        $('.pos-digital-payment-group').hide();
        $('.pos-change-group').hide();
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
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

// Initialize payment functionality
$(document).ready(function() {
    if ($('.pos-payment-method').length) {
        new POSPayment();
    }
});