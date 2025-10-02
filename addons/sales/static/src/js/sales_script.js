// Kids Clothing ERP - Sales Addon - JavaScript

// Sales Order Management
class SalesOrderManager {
    constructor() {
        this.initializeEventListeners();
        this.setupAutoSave();
        this.setupValidation();
    }

    initializeEventListeners() {
        // Order line management
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-order-line')) {
                this.addOrderLine();
            }
            if (e.target.classList.contains('remove-order-line')) {
                this.removeOrderLine(e.target);
            }
        });

        // Product selection
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('product-select')) {
                this.onProductChange(e.target);
            }
        });

        // Quantity changes
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('quantity-input')) {
                this.calculateLineTotal(e.target);
            }
        });

        // Price changes
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('price-input')) {
                this.calculateLineTotal(e.target);
            }
        });
    }

    setupAutoSave() {
        // Auto-save form data every 30 seconds
        setInterval(() => {
            this.autoSave();
        }, 30000);
    }

    setupValidation() {
        // Real-time validation
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('required-field')) {
                this.validateField(e.target);
            }
        });
    }

    addOrderLine() {
        const orderLinesContainer = document.querySelector('.order-lines-container');
        if (!orderLinesContainer) return;

        const lineTemplate = document.querySelector('.order-line-template');
        if (!lineTemplate) return;

        const newLine = lineTemplate.cloneNode(true);
        newLine.classList.remove('order-line-template');
        newLine.classList.add('order-line');
        newLine.style.display = 'block';

        // Clear values
        newLine.querySelectorAll('input, select').forEach(field => {
            field.value = '';
        });

        // Add remove button
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-danger btn-sm remove-order-line';
        removeBtn.innerHTML = 'Remove';
        newLine.querySelector('.line-actions').appendChild(removeBtn);

        orderLinesContainer.appendChild(newLine);
        this.updateLineNumbers();
    }

    removeOrderLine(button) {
        const line = button.closest('.order-line');
        if (line) {
            line.remove();
            this.updateLineNumbers();
            this.calculateOrderTotal();
        }
    }

    updateLineNumbers() {
        const lines = document.querySelectorAll('.order-line');
        lines.forEach((line, index) => {
            const lineNumber = line.querySelector('.line-number');
            if (lineNumber) {
                lineNumber.textContent = index + 1;
            }
        });
    }

    onProductChange(selectElement) {
        const line = selectElement.closest('.order-line');
        if (!line) return;

        const productId = selectElement.value;
        if (!productId) return;

        // Fetch product details
        this.fetchProductDetails(productId, line);
    }

    async fetchProductDetails(productId, line) {
        try {
            const response = await fetch(`/api/products/${productId}`);
            const product = await response.json();

            // Update price
            const priceInput = line.querySelector('.price-input');
            if (priceInput) {
                priceInput.value = product.price || 0;
            }

            // Update available sizes
            const sizeSelect = line.querySelector('.size-select');
            if (sizeSelect && product.sizes) {
                sizeSelect.innerHTML = '<option value="">Select Size</option>';
                product.sizes.forEach(size => {
                    const option = document.createElement('option');
                    option.value = size.id;
                    option.textContent = size.name;
                    sizeSelect.appendChild(option);
                });
            }

            // Update available colors
            const colorSelect = line.querySelector('.color-select');
            if (colorSelect && product.colors) {
                colorSelect.innerHTML = '<option value="">Select Color</option>';
                product.colors.forEach(color => {
                    const option = document.createElement('option');
                    option.value = color.id;
                    option.textContent = color.name;
                    colorSelect.appendChild(option);
                });
            }

            this.calculateLineTotal(line);
        } catch (error) {
            console.error('Error fetching product details:', error);
        }
    }

    calculateLineTotal(line) {
        const quantityInput = line.querySelector('.quantity-input');
        const priceInput = line.querySelector('.price-input');
        const totalSpan = line.querySelector('.line-total');

        if (quantityInput && priceInput && totalSpan) {
            const quantity = parseFloat(quantityInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            const total = quantity * price;
            totalSpan.textContent = total.toFixed(2);
        }

        this.calculateOrderTotal();
    }

    calculateOrderTotal() {
        const lines = document.querySelectorAll('.order-line');
        let total = 0;

        lines.forEach(line => {
            const totalSpan = line.querySelector('.line-total');
            if (totalSpan) {
                const lineTotal = parseFloat(totalSpan.textContent) || 0;
                total += lineTotal;
            }
        });

        const orderTotalElement = document.querySelector('.order-total');
        if (orderTotalElement) {
            orderTotalElement.textContent = total.toFixed(2);
        }
    }

    validateField(field) {
        const value = field.value.trim();
        const isValid = value.length > 0;

        field.classList.toggle('is-invalid', !isValid);
        field.classList.toggle('is-valid', isValid);

        return isValid;
    }

    autoSave() {
        const form = document.querySelector('.sale-order-form');
        if (!form) return;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Save to localStorage as backup
        localStorage.setItem('sale_order_draft', JSON.stringify(data));

        // Send to server
        fetch('/api/sales/auto-save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).catch(error => {
            console.error('Auto-save failed:', error);
        });
    }
}

// Sales Team Management
class SalesTeamManager {
    constructor() {
        this.initializeEventListeners();
        this.setupTeamAnalytics();
    }

    initializeEventListeners() {
        // Team member management
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-team-member')) {
                this.addTeamMember();
            }
            if (e.target.classList.contains('remove-team-member')) {
                this.removeTeamMember(e.target);
            }
        });

        // Team performance updates
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('team-target-input')) {
                this.updateTeamTargets();
            }
        });
    }

    setupTeamAnalytics() {
        // Initialize team performance charts
        this.initializePerformanceCharts();
        this.setupRealTimeUpdates();
    }

    addTeamMember() {
        const membersContainer = document.querySelector('.team-members-container');
        if (!membersContainer) return;

        const memberTemplate = document.querySelector('.team-member-template');
        if (!memberTemplate) return;

        const newMember = memberTemplate.cloneNode(true);
        newMember.classList.remove('team-member-template');
        newMember.classList.add('team-member');
        newMember.style.display = 'block';

        // Clear values
        newMember.querySelectorAll('input, select').forEach(field => {
            field.value = '';
        });

        // Add remove button
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-danger btn-sm remove-team-member';
        removeBtn.innerHTML = 'Remove';
        newMember.querySelector('.member-actions').appendChild(removeBtn);

        membersContainer.appendChild(newMember);
    }

    removeTeamMember(button) {
        const member = button.closest('.team-member');
        if (member) {
            member.remove();
            this.updateTeamPerformance();
        }
    }

    updateTeamTargets() {
        const targetInputs = document.querySelectorAll('.team-target-input');
        let totalTarget = 0;

        targetInputs.forEach(input => {
            totalTarget += parseFloat(input.value) || 0;
        });

        const totalTargetElement = document.querySelector('.total-team-target');
        if (totalTargetElement) {
            totalTargetElement.textContent = totalTarget.toFixed(2);
        }

        this.updateTeamPerformance();
    }

    updateTeamPerformance() {
        // Calculate team performance metrics
        const achievedAmount = this.calculateAchievedAmount();
        const targetAmount = this.calculateTargetAmount();
        const performancePercentage = targetAmount > 0 ? (achievedAmount / targetAmount) * 100 : 0;

        const performanceElement = document.querySelector('.team-performance');
        if (performanceElement) {
            performanceElement.textContent = performancePercentage.toFixed(1) + '%';
        }

        this.updatePerformanceChart(achievedAmount, targetAmount);
    }

    calculateAchievedAmount() {
        const achievedInputs = document.querySelectorAll('.member-achieved-input');
        let total = 0;

        achievedInputs.forEach(input => {
            total += parseFloat(input.value) || 0;
        });

        return total;
    }

    calculateTargetAmount() {
        const targetInputs = document.querySelectorAll('.member-target-input');
        let total = 0;

        targetInputs.forEach(input => {
            total += parseFloat(input.value) || 0;
        });

        return total;
    }

    updatePerformanceChart(achieved, target) {
        const chartElement = document.querySelector('.performance-chart');
        if (!chartElement) return;

        const percentage = target > 0 ? (achieved / target) * 100 : 0;
        chartElement.style.width = Math.min(percentage, 100) + '%';
        chartElement.classList.toggle('over-target', percentage > 100);
    }

    initializePerformanceCharts() {
        // Initialize any performance charts
        const charts = document.querySelectorAll('.performance-chart');
        charts.forEach(chart => {
            this.animateChart(chart);
        });
    }

    animateChart(chart) {
        const targetWidth = chart.dataset.percentage || 0;
        chart.style.width = '0%';
        
        setTimeout(() => {
            chart.style.transition = 'width 1s ease-in-out';
            chart.style.width = targetWidth + '%';
        }, 100);
    }

    setupRealTimeUpdates() {
        // Set up real-time updates for team performance
        setInterval(() => {
            this.updateTeamPerformance();
        }, 60000); // Update every minute
    }
}

// Sales Analytics Management
class SalesAnalyticsManager {
    constructor() {
        this.initializeCharts();
        this.setupFilters();
        this.setupExport();
    }

    initializeCharts() {
        // Initialize sales performance charts
        this.initializeSalesChart();
        this.initializeAgeGroupChart();
        this.initializeGenderChart();
        this.initializeSeasonChart();
    }

    initializeSalesChart() {
        const chartElement = document.querySelector('.sales-chart');
        if (!chartElement) return;

        // Create sales performance chart
        this.createSalesChart(chartElement);
    }

    initializeAgeGroupChart() {
        const chartElement = document.querySelector('.age-group-chart');
        if (!chartElement) return;

        // Create age group sales chart
        this.createAgeGroupChart(chartElement);
    }

    initializeGenderChart() {
        const chartElement = document.querySelector('.gender-chart');
        if (!chartElement) return;

        // Create gender sales chart
        this.createGenderChart(chartElement);
    }

    initializeSeasonChart() {
        const chartElement = document.querySelector('.season-chart');
        if (!chartElement) return;

        // Create season sales chart
        this.createSeasonChart(chartElement);
    }

    createSalesChart(container) {
        // Create a simple bar chart for sales performance
        const data = this.getSalesData();
        const maxValue = Math.max(...data.map(item => item.value));

        data.forEach((item, index) => {
            const bar = document.createElement('div');
            bar.className = 'chart-bar';
            bar.style.height = (item.value / maxValue) * 100 + '%';
            bar.style.backgroundColor = this.getColor(index);
            bar.title = item.label + ': ' + item.value;
            container.appendChild(bar);
        });
    }

    createAgeGroupChart(container) {
        const data = this.getAgeGroupData();
        this.createPieChart(container, data);
    }

    createGenderChart(container) {
        const data = this.getGenderData();
        this.createPieChart(container, data);
    }

    createSeasonChart(container) {
        const data = this.getSeasonData();
        this.createPieChart(container, data);
    }

    createPieChart(container, data) {
        const total = data.reduce((sum, item) => sum + item.value, 0);
        let currentAngle = 0;

        data.forEach((item, index) => {
            const slice = document.createElement('div');
            slice.className = 'chart-slice';
            slice.style.backgroundColor = this.getColor(index);
            slice.style.transform = `rotate(${currentAngle}deg)`;
            slice.style.width = '50%';
            slice.style.height = '50%';
            slice.style.borderRadius = '50%';
            slice.title = item.label + ': ' + item.value;
            container.appendChild(slice);

            currentAngle += (item.value / total) * 360;
        });
    }

    getSalesData() {
        // Mock data - in real implementation, this would come from the server
        return [
            { label: 'Jan', value: 10000 },
            { label: 'Feb', value: 12000 },
            { label: 'Mar', value: 15000 },
            { label: 'Apr', value: 18000 },
            { label: 'May', value: 20000 },
            { label: 'Jun', value: 22000 }
        ];
    }

    getAgeGroupData() {
        return [
            { label: 'Infant', value: 30 },
            { label: 'Toddler', value: 25 },
            { label: 'Preschool', value: 20 },
            { label: 'Child', value: 15 },
            { label: 'Teen', value: 10 }
        ];
    }

    getGenderData() {
        return [
            { label: 'Boys', value: 60 },
            { label: 'Girls', value: 40 }
        ];
    }

    getSeasonData() {
        return [
            { label: 'Spring', value: 25 },
            { label: 'Summer', value: 30 },
            { label: 'Fall', value: 20 },
            { label: 'Winter', value: 25 }
        ];
    }

    getColor(index) {
        const colors = [
            '#667eea', '#764ba2', '#f093fb', '#f5576c',
            '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
        ];
        return colors[index % colors.length];
    }

    setupFilters() {
        // Set up date range filters
        const dateRangeInput = document.querySelector('.date-range-input');
        if (dateRangeInput) {
            dateRangeInput.addEventListener('change', () => {
                this.updateAnalytics();
            });
        }

        // Set up team filters
        const teamFilter = document.querySelector('.team-filter');
        if (teamFilter) {
            teamFilter.addEventListener('change', () => {
                this.updateAnalytics();
            });
        }

        // Set up territory filters
        const territoryFilter = document.querySelector('.territory-filter');
        if (territoryFilter) {
            territoryFilter.addEventListener('change', () => {
                this.updateAnalytics();
            });
        }
    }

    setupExport() {
        // Set up export functionality
        const exportBtn = document.querySelector('.export-analytics-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportAnalytics();
            });
        }
    }

    updateAnalytics() {
        // Update analytics based on current filters
        this.initializeCharts();
    }

    exportAnalytics() {
        // Export analytics data
        const data = this.getAnalyticsData();
        const csv = this.convertToCSV(data);
        this.downloadCSV(csv, 'sales_analytics.csv');
    }

    getAnalyticsData() {
        // Get current analytics data
        return {
            sales: this.getSalesData(),
            ageGroups: this.getAgeGroupData(),
            genders: this.getGenderData(),
            seasons: this.getSeasonData()
        };
    }

    convertToCSV(data) {
        let csv = 'Category,Label,Value\n';
        
        data.sales.forEach(item => {
            csv += `Sales,${item.label},${item.value}\n`;
        });
        
        data.ageGroups.forEach(item => {
            csv += `Age Group,${item.label},${item.value}\n`;
        });
        
        data.genders.forEach(item => {
            csv += `Gender,${item.label},${item.value}\n`;
        });
        
        data.seasons.forEach(item => {
            csv += `Season,${item.label},${item.value}\n`;
        });
        
        return csv;
    }

    downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}

// Sales Commission Management
class SalesCommissionManager {
    constructor() {
        this.initializeEventListeners();
        this.setupCommissionCalculation();
    }

    initializeEventListeners() {
        // Commission calculation
        document.addEventListener('input', (e) => {
            if (e.target.classList.contains('commission-input')) {
                this.calculateCommission(e.target);
            }
        });

        // Commission approval
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('approve-commission')) {
                this.approveCommission(e.target);
            }
            if (e.target.classList.contains('pay-commission')) {
                this.payCommission(e.target);
            }
        });
    }

    setupCommissionCalculation() {
        // Set up automatic commission calculation
        this.calculateAllCommissions();
    }

    calculateCommission(input) {
        const row = input.closest('.commission-row');
        if (!row) return;

        const baseAmount = parseFloat(row.querySelector('.base-amount-input').value) || 0;
        const rate = parseFloat(row.querySelector('.commission-rate-input').value) || 0;
        const calculatedAmount = (baseAmount * rate) / 100;

        const calculatedInput = row.querySelector('.calculated-amount-input');
        if (calculatedInput) {
            calculatedInput.value = calculatedAmount.toFixed(2);
        }

        this.updateTotalCommission();
    }

    calculateAllCommissions() {
        const commissionRows = document.querySelectorAll('.commission-row');
        commissionRows.forEach(row => {
            this.calculateCommission(row.querySelector('.commission-input'));
        });
    }

    updateTotalCommission() {
        const calculatedInputs = document.querySelectorAll('.calculated-amount-input');
        let total = 0;

        calculatedInputs.forEach(input => {
            total += parseFloat(input.value) || 0;
        });

        const totalElement = document.querySelector('.total-commission');
        if (totalElement) {
            totalElement.textContent = total.toFixed(2);
        }
    }

    approveCommission(button) {
        const row = button.closest('.commission-row');
        if (!row) return;

        // Update status
        const statusElement = row.querySelector('.commission-status');
        if (statusElement) {
            statusElement.textContent = 'Approved';
            statusElement.className = 'commission-status status-approved';
        }

        // Disable button
        button.disabled = true;
        button.textContent = 'Approved';
    }

    payCommission(button) {
        const row = button.closest('.commission-row');
        if (!row) return;

        // Update status
        const statusElement = row.querySelector('.commission-status');
        if (statusElement) {
            statusElement.textContent = 'Paid';
            statusElement.className = 'commission-status status-paid';
        }

        // Disable button
        button.disabled = true;
        button.textContent = 'Paid';
    }
}

// Initialize all managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize sales order manager
    if (document.querySelector('.sale-order-form')) {
        new SalesOrderManager();
    }

    // Initialize sales team manager
    if (document.querySelector('.sales-team-form')) {
        new SalesTeamManager();
    }

    // Initialize sales analytics manager
    if (document.querySelector('.sales-analytics')) {
        new SalesAnalyticsManager();
    }

    // Initialize sales commission manager
    if (document.querySelector('.sales-commission-form')) {
        new SalesCommissionManager();
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Export for use in other modules
window.SalesOrderManager = SalesOrderManager;
window.SalesTeamManager = SalesTeamManager;
window.SalesAnalyticsManager = SalesAnalyticsManager;
window.SalesCommissionManager = SalesCommissionManager;