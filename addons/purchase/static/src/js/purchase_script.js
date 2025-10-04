/**
 * Purchase Module JavaScript
 * =========================
 * 
 * JavaScript functionality for the Purchase module
 */

class PurchaseDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboardData();
        this.setupCharts();
    }

    setupEventListeners() {
        // Purchase order creation
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-create-purchase-order')) {
                this.createPurchaseOrder();
            }
        });

        // Vendor bill creation
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-create-vendor-bill')) {
                this.createVendorBill();
            }
        });

        // Analytics refresh
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-refresh-analytics')) {
                this.refreshAnalytics();
            }
        });

        // Purchase order approval
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-approve-order')) {
                this.approvePurchaseOrder(e.target.dataset.orderId);
            }
        });

        // Vendor bill payment
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-pay-bill')) {
                this.payVendorBill(e.target.dataset.billId);
            }
        });
    }

    loadDashboardData() {
        // Load purchase statistics
        this.loadPurchaseStats();
        
        // Load recent orders
        this.loadRecentOrders();
        
        // Load supplier performance
        this.loadSupplierPerformance();
        
        // Load kids clothing analytics
        this.loadKidsClothingAnalytics();
    }

    loadPurchaseStats() {
        // Simulate API call
        const stats = {
            totalOrders: 45,
            totalAmount: 125000,
            averageOrderValue: 2777.78,
            totalSuppliers: 12,
            fulfillmentRate: 95.5,
            costSavings: 6250
        };

        this.updateStatsDisplay(stats);
    }

    updateStatsDisplay(stats) {
        const elements = {
            'total-orders': stats.totalOrders,
            'total-amount': this.formatCurrency(stats.totalAmount),
            'average-order-value': this.formatCurrency(stats.averageOrderValue),
            'total-suppliers': stats.totalSuppliers,
            'fulfillment-rate': stats.fulfillmentRate + '%',
            'cost-savings': this.formatCurrency(stats.costSavings)
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    loadRecentOrders() {
        // Simulate recent orders data
        const orders = [
            {
                id: 1,
                name: 'PO2024001',
                supplier: 'Kids Fashion Supplier',
                date: '2024-01-15',
                amount: 5000,
                status: 'approved',
                ageGroup: 'child',
                season: 'summer'
            },
            {
                id: 2,
                name: 'PO2024002',
                supplier: 'Toddler Wear Co.',
                date: '2024-01-16',
                amount: 7500,
                status: 'done',
                ageGroup: 'toddler',
                season: 'winter'
            }
        ];

        this.displayRecentOrders(orders);
    }

    displayRecentOrders(orders) {
        const container = document.getElementById('recent-orders');
        if (!container) return;

        const html = orders.map(order => `
            <div class="purchase-line-item">
                <div class="row">
                    <div class="col-md-3">
                        <strong>${order.name}</strong>
                    </div>
                    <div class="col-md-3">
                        ${order.supplier}
                    </div>
                    <div class="col-md-2">
                        ${order.date}
                    </div>
                    <div class="col-md-2">
                        ${this.formatCurrency(order.amount)}
                    </div>
                    <div class="col-md-2">
                        <span class="purchase-status ${order.status}">${order.status}</span>
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-12">
                        <small class="text-muted">
                            Age Group: ${order.ageGroup} | Season: ${order.season}
                        </small>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    loadSupplierPerformance() {
        // Simulate supplier performance data
        const suppliers = [
            { name: 'Kids Fashion Supplier', performance: 95, orders: 15, amount: 45000 },
            { name: 'Toddler Wear Co.', performance: 92, orders: 12, amount: 38000 },
            { name: 'Teen Clothing Ltd.', performance: 88, orders: 8, amount: 25000 }
        ];

        this.displaySupplierPerformance(suppliers);
    }

    displaySupplierPerformance(suppliers) {
        const container = document.getElementById('supplier-performance');
        if (!container) return;

        const html = suppliers.map(supplier => `
            <div class="purchase-supplier-card">
                <h4>${supplier.name}</h4>
                <div class="supplier-info">
                    <div>Performance Score: ${supplier.performance}%</div>
                    <div>Total Orders: ${supplier.orders}</div>
                    <div>Total Amount: ${this.formatCurrency(supplier.amount)}</div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    loadKidsClothingAnalytics() {
        // Simulate kids clothing analytics
        const analytics = {
            ageGroups: {
                'infant': 15,
                'toddler': 25,
                'child': 35,
                'teen': 25
            },
            seasons: {
                'summer': 40,
                'winter': 30,
                'monsoon': 20,
                'all_season': 10
            },
            genders: {
                'boys': 45,
                'girls': 40,
                'unisex': 15
            },
            occasions: {
                'daily_wear': 50,
                'school': 25,
                'party_wear': 15,
                'sports': 10
            }
        };

        this.displayKidsClothingAnalytics(analytics);
    }

    displayKidsClothingAnalytics(analytics) {
        const container = document.getElementById('kids-clothing-analytics');
        if (!container) return;

        const html = `
            <div class="purchase-kids-clothing">
                <h4>Kids Clothing Analytics</h4>
                <div class="row">
                    <div class="col-md-6">
                        <h5>Age Groups</h5>
                        ${Object.entries(analytics.ageGroups).map(([group, count]) => `
                            <span class="age-group">${group}: ${count}%</span>
                        `).join('')}
                    </div>
                    <div class="col-md-6">
                        <h5>Seasons</h5>
                        ${Object.entries(analytics.seasons).map(([season, count]) => `
                            <span class="season">${season}: ${count}%</span>
                        `).join('')}
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-6">
                        <h5>Genders</h5>
                        ${Object.entries(analytics.genders).map(([gender, count]) => `
                            <span class="age-group">${gender}: ${count}%</span>
                        `).join('')}
                    </div>
                    <div class="col-md-6">
                        <h5>Occasions</h5>
                        ${Object.entries(analytics.occasions).map(([occasion, count]) => `
                            <span class="season">${occasion}: ${count}%</span>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    setupCharts() {
        // Setup purchase analytics charts
        this.setupPurchaseTrendChart();
        this.setupSupplierPerformanceChart();
        this.setupSeasonalTrendChart();
    }

    setupPurchaseTrendChart() {
        // Simulate chart setup
        const ctx = document.getElementById('purchase-trend-chart');
        if (!ctx) return;

        // Chart.js implementation would go here
        console.log('Setting up purchase trend chart');
    }

    setupSupplierPerformanceChart() {
        // Simulate chart setup
        const ctx = document.getElementById('supplier-performance-chart');
        if (!ctx) return;

        // Chart.js implementation would go here
        console.log('Setting up supplier performance chart');
    }

    setupSeasonalTrendChart() {
        // Simulate chart setup
        const ctx = document.getElementById('seasonal-trend-chart');
        if (!ctx) return;

        // Chart.js implementation would go here
        console.log('Setting up seasonal trend chart');
    }

    createPurchaseOrder() {
        // Open purchase order creation wizard
        this.showNotification('Opening Purchase Order Creation Wizard...', 'info');
        
        // Simulate wizard opening
        setTimeout(() => {
            this.showNotification('Purchase Order Creation Wizard opened', 'success');
        }, 1000);
    }

    createVendorBill() {
        // Open vendor bill creation wizard
        this.showNotification('Opening Vendor Bill Creation Wizard...', 'info');
        
        // Simulate wizard opening
        setTimeout(() => {
            this.showNotification('Vendor Bill Creation Wizard opened', 'success');
        }, 1000);
    }

    refreshAnalytics() {
        this.showNotification('Refreshing analytics data...', 'info');
        
        // Simulate data refresh
        setTimeout(() => {
            this.loadDashboardData();
            this.showNotification('Analytics data refreshed successfully', 'success');
        }, 2000);
    }

    approvePurchaseOrder(orderId) {
        this.showNotification(`Approving Purchase Order ${orderId}...`, 'info');
        
        // Simulate approval process
        setTimeout(() => {
            this.showNotification(`Purchase Order ${orderId} approved successfully`, 'success');
            this.loadRecentOrders(); // Refresh the list
        }, 1500);
    }

    payVendorBill(billId) {
        this.showNotification(`Processing payment for Bill ${billId}...`, 'info');
        
        // Simulate payment process
        setTimeout(() => {
            this.showNotification(`Payment for Bill ${billId} processed successfully`, 'success');
        }, 2000);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PurchaseDashboard();
});

// Export for use in other modules
window.PurchaseDashboard = PurchaseDashboard;