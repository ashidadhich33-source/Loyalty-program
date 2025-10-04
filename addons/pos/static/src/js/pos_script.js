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
});