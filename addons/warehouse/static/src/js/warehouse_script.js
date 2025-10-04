/**
 * Warehouse Management JavaScript
 * =============================
 * 
 * JavaScript functionality for warehouse management interface
 */

class WarehouseDashboard {
    constructor() {
        this.initializeDashboard();
        this.bindEvents();
    }
    
    initializeDashboard() {
        console.log('Initializing Warehouse Dashboard...');
        
        // Load warehouse data
        this.loadWarehouseData();
        
        // Initialize charts if available
        this.initializeCharts();
        
        // Set up auto-refresh
        this.setupAutoRefresh();
    }
    
    bindEvents() {
        // Warehouse card click events
        document.addEventListener('click', (e) => {
            if (e.target.closest('.warehouse-card')) {
                this.handleWarehouseCardClick(e.target.closest('.warehouse-card'));
            }
            
            if (e.target.closest('.location-item')) {
                this.handleLocationClick(e.target.closest('.location-item'));
            }
            
            if (e.target.closest('.operation-item')) {
                this.handleOperationClick(e.target.closest('.operation-item'));
            }
        });
        
        // Search functionality
        const searchInput = document.querySelector('.warehouse-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }
        
        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleFilter(e.target.dataset.filter);
            });
        });
    }
    
    async loadWarehouseData() {
        try {
            const response = await fetch('/api/warehouse/dashboard');
            const data = await response.json();
            
            this.updateDashboard(data);
        } catch (error) {
            console.error('Error loading warehouse data:', error);
            this.showError('Failed to load warehouse data');
        }
    }
    
    updateDashboard(data) {
        // Update warehouse cards
        this.updateWarehouseCards(data.warehouses);
        
        // Update locations
        this.updateLocations(data.locations);
        
        // Update aging data
        this.updateAgingData(data.aging);
        
        // Update expiry data
        this.updateExpiryData(data.expiry);
        
        // Update operations
        this.updateOperations(data.operations);
    }
    
    updateWarehouseCards(warehouses) {
        const container = document.querySelector('.warehouse-cards');
        if (!container) return;
        
        container.innerHTML = warehouses.map(warehouse => `
            <div class="warehouse-card" data-warehouse-id="${warehouse.id}">
                <div class="card-header">
                    <h3 class="card-title">${warehouse.name}</h3>
                    <span class="card-type">${warehouse.type}</span>
                </div>
                <div class="card-stats">
                    <div class="stat-item">
                        <div class="stat-value">${warehouse.total_products}</div>
                        <div class="stat-label">Products</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${warehouse.total_quantity}</div>
                        <div class="stat-label">Quantity</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${warehouse.total_value}</div>
                        <div class="stat-label">Value</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${warehouse.turnover_rate}%</div>
                        <div class="stat-label">Turnover</div>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="btn btn-primary" onclick="warehouseDashboard.viewWarehouse(${warehouse.id})">
                        View Details
                    </button>
                    <button class="btn btn-secondary" onclick="warehouseDashboard.viewLocations(${warehouse.id})">
                        View Locations
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    updateLocations(locations) {
        const container = document.querySelector('.warehouse-locations .locations-list');
        if (!container) return;
        
        container.innerHTML = locations.map(location => `
            <div class="location-item" data-location-id="${location.id}">
                <div class="location-info">
                    <h4 class="location-name">${location.name}</h4>
                    <p class="location-details">${location.type} • ${location.warehouse}</p>
                </div>
                <div class="location-stats">
                    <div class="location-stat">
                        <div class="location-stat-value">${location.product_count}</div>
                        <div class="location-stat-label">Products</div>
                    </div>
                    <div class="location-stat">
                        <div class="location-stat-value">${location.total_quantity}</div>
                        <div class="location-stat-label">Quantity</div>
                    </div>
                    <div class="location-stat">
                        <div class="location-stat-value">${location.capacity_usage}%</div>
                        <div class="location-stat-label">Capacity</div>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    updateAgingData(agingData) {
        const container = document.querySelector('.stock-aging .aging-categories');
        if (!container) return;
        
        container.innerHTML = `
            <div class="aging-category fresh">
                <div class="aging-category-value">${agingData.age_0_30_days}</div>
                <div class="aging-category-label">Fresh (0-30 days)</div>
            </div>
            <div class="aging-category current">
                <div class="aging-category-value">${agingData.age_31_90_days}</div>
                <div class="aging-category-label">Current (31-90 days)</div>
            </div>
            <div class="aging-category aging">
                <div class="aging-category-value">${agingData.age_91_180_days}</div>
                <div class="aging-category-label">Aging (91-180 days)</div>
            </div>
            <div class="aging-category stale">
                <div class="aging-category-value">${agingData.age_181_365_days}</div>
                <div class="aging-category-label">Stale (181-365 days)</div>
            </div>
            <div class="aging-category obsolete">
                <div class="aging-category-value">${agingData.age_over_365_days}</div>
                <div class="aging-category-label">Obsolete (365+ days)</div>
            </div>
        `;
    }
    
    updateExpiryData(expiryData) {
        const container = document.querySelector('.stock-expiry .expiry-categories');
        if (!container) return;
        
        container.innerHTML = `
            <div class="expiry-category expired">
                <div class="expiry-category-value">${expiryData.expired_quantity}</div>
                <div class="expiry-category-label">Expired</div>
            </div>
            <div class="expiry-category urgent">
                <div class="expiry-category-value">${expiryData.expiring_7_days}</div>
                <div class="expiry-category-label">Expiring in 7 days</div>
            </div>
            <div class="expiry-category warning">
                <div class="expiry-category-value">${expiryData.expiring_15_days}</div>
                <div class="expiry-category-label">Expiring in 15 days</div>
            </div>
            <div class="expiry-category caution">
                <div class="expiry-category-value">${expiryData.expiring_30_days}</div>
                <div class="expiry-category-label">Expiring in 30 days</div>
            </div>
            <div class="expiry-category normal">
                <div class="expiry-category-value">${expiryData.expiring_60_days}</div>
                <div class="expiry-category-label">Expiring in 60+ days</div>
            </div>
        `;
    }
    
    updateOperations(operations) {
        const container = document.querySelector('.warehouse-operations .operations-list');
        if (!container) return;
        
        container.innerHTML = operations.map(operation => `
            <div class="operation-item" data-operation-id="${operation.id}">
                <div class="operation-info">
                    <h4 class="operation-name">${operation.name}</h4>
                    <p class="operation-details">${operation.type} • ${operation.warehouse} • ${operation.operator}</p>
                </div>
                <span class="operation-status ${operation.state}">${operation.state}</span>
            </div>
        `).join('');
    }
    
    handleWarehouseCardClick(card) {
        const warehouseId = card.dataset.warehouseId;
        this.viewWarehouse(warehouseId);
    }
    
    handleLocationClick(locationItem) {
        const locationId = locationItem.dataset.locationId;
        this.viewLocation(locationId);
    }
    
    handleOperationClick(operationItem) {
        const operationId = operationItem.dataset.operationId;
        this.viewOperation(operationId);
    }
    
    handleSearch(query) {
        // Filter warehouse cards based on search query
        const cards = document.querySelectorAll('.warehouse-card');
        cards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            const type = card.querySelector('.card-type').textContent.toLowerCase();
            
            if (title.includes(query.toLowerCase()) || type.includes(query.toLowerCase())) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    handleFilter(filter) {
        // Apply filter to warehouse cards
        const cards = document.querySelectorAll('.warehouse-card');
        cards.forEach(card => {
            const type = card.querySelector('.card-type').textContent.toLowerCase();
            
            if (filter === 'all' || type === filter) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    viewWarehouse(warehouseId) {
        // Navigate to warehouse detail page
        window.location.href = `/warehouse/${warehouseId}`;
    }
    
    viewLocations(warehouseId) {
        // Navigate to warehouse locations page
        window.location.href = `/warehouse/${warehouseId}/locations`;
    }
    
    viewLocation(locationId) {
        // Navigate to location detail page
        window.location.href = `/warehouse/location/${locationId}`;
    }
    
    viewOperation(operationId) {
        // Navigate to operation detail page
        window.location.href = `/warehouse/operation/${operationId}`;
    }
    
    initializeCharts() {
        // Initialize charts if Chart.js is available
        if (typeof Chart !== 'undefined') {
            this.createAgingChart();
            this.createExpiryChart();
        }
    }
    
    createAgingChart() {
        const ctx = document.getElementById('agingChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Fresh', 'Current', 'Aging', 'Stale', 'Obsolete'],
                datasets: [{
                    data: [0, 0, 0, 0, 0], // Will be updated with real data
                    backgroundColor: [
                        '#27ae60',
                        '#3498db',
                        '#f39c12',
                        '#e74c3c',
                        '#8e44ad'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    createExpiryChart() {
        const ctx = document.getElementById('expiryChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Expired', '7 days', '15 days', '30 days', '60+ days'],
                datasets: [{
                    label: 'Quantity',
                    data: [0, 0, 0, 0, 0], // Will be updated with real data
                    backgroundColor: [
                        '#e74c3c',
                        '#e67e22',
                        '#f39c12',
                        '#3498db',
                        '#27ae60'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    setupAutoRefresh() {
        // Auto-refresh data every 5 minutes
        setInterval(() => {
            this.loadWarehouseData();
        }, 300000);
    }
    
    showError(message) {
        // Show error message to user
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-error';
        errorDiv.textContent = message;
        
        const dashboard = document.querySelector('.warehouse-dashboard');
        if (dashboard) {
            dashboard.insertBefore(errorDiv, dashboard.firstChild);
            
            // Remove error after 5 seconds
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    }
    
    showSuccess(message) {
        // Show success message to user
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success';
        successDiv.textContent = message;
        
        const dashboard = document.querySelector('.warehouse-dashboard');
        if (dashboard) {
            dashboard.insertBefore(successDiv, dashboard.firstChild);
            
            // Remove success message after 3 seconds
            setTimeout(() => {
                successDiv.remove();
            }, 3000);
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.warehouseDashboard = new WarehouseDashboard();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WarehouseDashboard;
}