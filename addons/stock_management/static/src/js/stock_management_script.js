/* Ocean ERP - Stock Management JavaScript */

/**
 * Ocean ERP Stock Management Module
 * =================================
 * 
 * JavaScript functionality for the stock management addon in Ocean ERP.
 */

class OceanStockManagement {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind form events
        this.bindFormEvents();
        
        // Bind button events
        this.bindButtonEvents();
        
        // Bind table events
        this.bindTableEvents();
    }
    
    bindFormEvents() {
        // Alert form events
        document.addEventListener('change', (e) => {
            if (e.target.matches('.ocean_alert_form input[name="alert_type"]')) {
                this.onAlertTypeChange(e.target.value);
            }
        });
        
        // Product change
        document.addEventListener('change', (e) => {
            if (e.target.matches('.ocean_alert_form select[name="product_id"]')) {
                this.onProductChange(e.target.value);
            }
        });
        
        // Priority change
        document.addEventListener('change', (e) => {
            if (e.target.matches('.ocean_alert_form select[name="priority"]')) {
                this.onPriorityChange(e.target.value);
            }
        });
    }
    
    bindButtonEvents() {
        // Resolve alert button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_resolve')) {
                this.resolveAlert(e.target.dataset.alertId);
            }
        });
        
        // Cancel alert button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_cancel')) {
                this.cancelAlert(e.target.dataset.alertId);
            }
        });
        
        // Reactivate alert button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_reactivate')) {
                this.reactivateAlert(e.target.dataset.alertId);
            }
        });
        
        // Create reorder rule button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_create_reorder_rule')) {
                this.createReorderRule(e.target.dataset.alertId);
            }
        });
        
        // Generate purchase order button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_generate_purchase_order')) {
                this.generatePurchaseOrder(e.target.dataset.alertId);
            }
        });
    }
    
    bindTableEvents() {
        // Table row click events
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_alert_table tbody tr')) {
                this.selectAlertRow(e.target);
            }
        });
        
        // Sort events
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_alert_table th[data-sort]')) {
                this.sortTable(e.target.dataset.sort);
            }
        });
    }
    
    onAlertTypeChange(alertType) {
        // Update alert message based on type
        const messageField = document.querySelector('.ocean_alert_form textarea[name="message"]');
        if (messageField) {
            this.updateAlertMessage(messageField, alertType);
        }
        
        // Update action required based on type
        const actionField = document.querySelector('.ocean_alert_form input[name="action_required"]');
        if (actionField) {
            this.updateActionRequired(actionField, alertType);
        }
    }
    
    updateAlertMessage(field, alertType) {
        const messages = {
            'low_stock': 'Product stock is below minimum level. Please reorder soon.',
            'out_of_stock': 'Product is out of stock. Immediate reorder required.',
            'overstock': 'Product stock is above maximum level. Consider reducing inventory.',
            'expiry': 'Product is approaching expiry date. Consider discounting or disposal.',
            'seasonal': 'Product is out of season. Consider moving to clearance.',
            'size': 'Specific size is running low. Consider reordering this size.',
            'brand': 'Brand stock is low. Consider reordering from this brand.',
            'color': 'Specific color is running low. Consider reordering this color.',
        };
        
        field.value = messages[alertType] || '';
    }
    
    updateActionRequired(field, alertType) {
        const actions = {
            'low_stock': 'Reorder product',
            'out_of_stock': 'Urgent reorder required',
            'overstock': 'Reduce inventory',
            'expiry': 'Discount or dispose',
            'seasonal': 'Move to clearance',
            'size': 'Reorder specific size',
            'brand': 'Reorder from brand',
            'color': 'Reorder specific color',
        };
        
        field.value = actions[alertType] || '';
    }
    
    onProductChange(productId) {
        if (productId) {
            // Load product details
            this.loadProductDetails(productId);
        }
    }
    
    async loadProductDetails(productId) {
        try {
            const response = await fetch(`/api/stock/product/${productId}`);
            const data = await response.json();
            
            // Update form fields with product data
            this.populateProductFields(data);
        } catch (error) {
            console.error('Error loading product details:', error);
        }
    }
    
    populateProductFields(data) {
        // Update age group
        const ageGroupField = document.querySelector('.ocean_alert_form select[name="age_group"]');
        if (ageGroupField && data.age_group) {
            ageGroupField.value = data.age_group;
        }
        
        // Update size
        const sizeField = document.querySelector('.ocean_alert_form select[name="size"]');
        if (sizeField && data.size) {
            sizeField.value = data.size;
        }
        
        // Update season
        const seasonField = document.querySelector('.ocean_alert_form select[name="season"]');
        if (seasonField && data.season) {
            seasonField.value = data.season;
        }
        
        // Update brand
        const brandField = document.querySelector('.ocean_alert_form input[name="brand"]');
        if (brandField && data.brand) {
            brandField.value = data.brand;
        }
        
        // Update color
        const colorField = document.querySelector('.ocean_alert_form input[name="color"]');
        if (colorField && data.color) {
            colorField.value = data.color;
        }
        
        // Update current stock
        const currentStockField = document.querySelector('.ocean_alert_form input[name="current_stock"]');
        if (currentStockField && data.current_stock !== undefined) {
            currentStockField.value = data.current_stock;
        }
        
        // Update minimum stock
        const minStockField = document.querySelector('.ocean_alert_form input[name="minimum_stock"]');
        if (minStockField && data.minimum_stock !== undefined) {
            minStockField.value = data.minimum_stock;
        }
        
        // Update maximum stock
        const maxStockField = document.querySelector('.ocean_alert_form input[name="maximum_stock"]');
        if (maxStockField && data.maximum_stock !== undefined) {
            maxStockField.value = data.maximum_stock;
        }
        
        // Update reorder point
        const reorderPointField = document.querySelector('.ocean_alert_form input[name="reorder_point"]');
        if (reorderPointField && data.reorder_point !== undefined) {
            reorderPointField.value = data.reorder_point;
        }
    }
    
    onPriorityChange(priority) {
        // Update due date based on priority
        const dueDateField = document.querySelector('.ocean_alert_form input[name="due_date"]');
        if (dueDateField) {
            this.updateDueDate(dueDateField, priority);
        }
    }
    
    updateDueDate(field, priority) {
        const now = new Date();
        let daysToAdd = 7; // Default
        
        switch (priority) {
            case 'urgent':
                daysToAdd = 1;
                break;
            case 'high':
                daysToAdd = 3;
                break;
            case 'medium':
                daysToAdd = 7;
                break;
            case 'low':
                daysToAdd = 14;
                break;
        }
        
        const dueDate = new Date(now.getTime() + (daysToAdd * 24 * 60 * 60 * 1000));
        field.value = dueDate.toISOString().slice(0, 16);
    }
    
    resolveAlert(alertId) {
        // Resolve the alert
        fetch(`/api/stock/alerts/${alertId}/resolve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.showNotification('Alert resolved successfully', 'success');
            this.refreshAlertList();
        })
        .catch(error => {
            console.error('Error resolving alert:', error);
            this.showNotification('Error resolving alert', 'danger');
        });
    }
    
    cancelAlert(alertId) {
        // Cancel the alert
        fetch(`/api/stock/alerts/${alertId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.showNotification('Alert cancelled successfully', 'success');
            this.refreshAlertList();
        })
        .catch(error => {
            console.error('Error cancelling alert:', error);
            this.showNotification('Error cancelling alert', 'danger');
        });
    }
    
    reactivateAlert(alertId) {
        // Reactivate the alert
        fetch(`/api/stock/alerts/${alertId}/reactivate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.showNotification('Alert reactivated successfully', 'success');
            this.refreshAlertList();
        })
        .catch(error => {
            console.error('Error reactivating alert:', error);
            this.showNotification('Error reactivating alert', 'danger');
        });
    }
    
    createReorderRule(alertId) {
        // Create reorder rule from alert
        fetch(`/api/stock/alerts/${alertId}/create_reorder_rule`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.showNotification('Reorder rule created successfully', 'success');
        })
        .catch(error => {
            console.error('Error creating reorder rule:', error);
            this.showNotification('Error creating reorder rule', 'danger');
        });
    }
    
    generatePurchaseOrder(alertId) {
        // Generate purchase order from alert
        fetch(`/api/stock/alerts/${alertId}/generate_purchase_order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            this.showNotification('Purchase order generated successfully', 'success');
        })
        .catch(error => {
            console.error('Error generating purchase order:', error);
            this.showNotification('Error generating purchase order', 'danger');
        });
    }
    
    selectAlertRow(row) {
        // Remove previous selection
        document.querySelectorAll('.ocean_alert_table tbody tr').forEach(r => {
            r.classList.remove('selected');
        });
        
        // Add selection to current row
        row.classList.add('selected');
        
        // Update form with selected alert data
        this.loadAlertData(row.dataset.alertId);
    }
    
    loadAlertData(alertId) {
        // Load alert data into form
        fetch(`/api/stock/alerts/${alertId}`)
            .then(response => response.json())
            .then(data => {
                this.populateForm(data);
            })
            .catch(error => {
                console.error('Error loading alert data:', error);
            });
    }
    
    populateForm(data) {
        // Populate form fields with alert data
        Object.keys(data).forEach(key => {
            const field = document.querySelector(`.ocean_alert_form [name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
    
    sortTable(column) {
        // Sort table by column
        const table = document.querySelector('.ocean_alert_table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        const sortedRows = rows.sort((a, b) => {
            const aValue = a.querySelector(`[data-column="${column}"]`).textContent;
            const bValue = b.querySelector(`[data-column="${column}"]`).textContent;
            
            return aValue.localeCompare(bValue);
        });
        
        // Reorder rows
        sortedRows.forEach(row => tbody.appendChild(row));
    }
    
    loadDashboardData() {
        // Load dashboard statistics
        this.loadAlertStatistics();
        this.loadStockStatistics();
        this.loadReorderStatistics();
    }
    
    async loadAlertStatistics() {
        try {
            const response = await fetch('/api/stock/statistics/alerts');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_total_alerts').textContent = data.total;
            document.querySelector('.ocean_active_alerts').textContent = data.active;
            document.querySelector('.ocean_resolved_alerts').textContent = data.resolved;
            document.querySelector('.ocean_urgent_alerts').textContent = data.urgent;
        } catch (error) {
            console.error('Error loading alert statistics:', error);
        }
    }
    
    async loadStockStatistics() {
        try {
            const response = await fetch('/api/stock/statistics/stock');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_low_stock_items').textContent = data.low_stock;
            document.querySelector('.ocean_out_of_stock_items').textContent = data.out_of_stock;
            document.querySelector('.ocean_overstock_items').textContent = data.overstock;
        } catch (error) {
            console.error('Error loading stock statistics:', error);
        }
    }
    
    async loadReorderStatistics() {
        try {
            const response = await fetch('/api/stock/statistics/reorder');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_pending_reorders').textContent = data.pending;
            document.querySelector('.ocean_completed_reorders').textContent = data.completed;
        } catch (error) {
            console.error('Error loading reorder statistics:', error);
        }
    }
    
    refreshAlertList() {
        // Refresh the alert list
        location.reload();
    }
    
    // Utility methods
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    formatNumber(number) {
        return new Intl.NumberFormat('en-IN').format(number);
    }
    
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-IN');
    }
    
    showNotification(message, type = 'info') {
        // Show notification to user
        const notification = document.createElement('div');
        notification.className = `ocean_notification ocean_notification_${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    showLoading(element) {
        const loading = document.createElement('div');
        loading.className = 'ocean_stock_loading';
        element.appendChild(loading);
    }
    
    hideLoading(element) {
        const loading = element.querySelector('.ocean_stock_loading');
        if (loading) {
            loading.remove();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OceanStockManagement();
});

// Export for use in other modules
window.OceanStockManagement = OceanStockManagement;