/* Ocean ERP - Accounting JavaScript */

/**
 * Ocean ERP Accounting Module
 * ===========================
 * 
 * JavaScript functionality for the accounting addon in Ocean ERP.
 */

class OceanAccounting {
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
        // Account form events
        document.addEventListener('change', (e) => {
            if (e.target.matches('.ocean_account_form input[name="account_type"]')) {
                this.onAccountTypeChange(e.target.value);
            }
        });
        
        // Parent account change
        document.addEventListener('change', (e) => {
            if (e.target.matches('.ocean_account_form select[name="parent_id"]')) {
                this.onParentAccountChange(e.target.value);
            }
        });
    }
    
    bindButtonEvents() {
        // View move lines button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_view_move_lines')) {
                this.viewMoveLines(e.target.dataset.accountId);
            }
        });
        
        // Reconcile button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_reconcile')) {
                this.reconcileAccount(e.target.dataset.accountId);
            }
        });
        
        // Generate report button
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_btn_generate_report')) {
                this.generateReport(e.target.dataset.accountId);
            }
        });
    }
    
    bindTableEvents() {
        // Table row click events
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_account_table tbody tr')) {
                this.selectAccountRow(e.target);
            }
        });
        
        // Sort events
        document.addEventListener('click', (e) => {
            if (e.target.matches('.ocean_account_table th[data-sort]')) {
                this.sortTable(e.target.dataset.sort);
            }
        });
    }
    
    onAccountTypeChange(accountType) {
        // Update account subtype options based on account type
        const subtypeSelect = document.querySelector('.ocean_account_form select[name="account_subtype"]');
        if (subtypeSelect) {
            this.updateAccountSubtypeOptions(subtypeSelect, accountType);
        }
        
        // Update account code prefix
        const codeInput = document.querySelector('.ocean_account_form input[name="code"]');
        if (codeInput && !codeInput.value) {
            this.generateAccountCode(codeInput, accountType);
        }
    }
    
    updateAccountSubtypeOptions(select, accountType) {
        const options = this.getAccountSubtypeOptions(accountType);
        
        // Clear existing options
        select.innerHTML = '<option value="">Select Subtype</option>';
        
        // Add new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.label;
            select.appendChild(optionElement);
        });
    }
    
    getAccountSubtypeOptions(accountType) {
        const subtypes = {
            'asset': [
                { value: 'current_asset', label: 'Current Asset' },
                { value: 'fixed_asset', label: 'Fixed Asset' },
                { value: 'intangible_asset', label: 'Intangible Asset' },
                { value: 'other_asset', label: 'Other Asset' }
            ],
            'liability': [
                { value: 'current_liability', label: 'Current Liability' },
                { value: 'long_term_liability', label: 'Long Term Liability' },
                { value: 'other_liability', label: 'Other Liability' }
            ],
            'equity': [
                { value: 'share_capital', label: 'Share Capital' },
                { value: 'retained_earnings', label: 'Retained Earnings' },
                { value: 'other_equity', label: 'Other Equity' }
            ],
            'income': [
                { value: 'sales', label: 'Sales' },
                { value: 'other_income', label: 'Other Income' }
            ],
            'expense': [
                { value: 'cost_of_goods_sold', label: 'Cost of Goods Sold' },
                { value: 'operating_expense', label: 'Operating Expense' },
                { value: 'administrative_expense', label: 'Administrative Expense' },
                { value: 'selling_expense', label: 'Selling Expense' },
                { value: 'other_expense', label: 'Other Expense' }
            ]
        };
        
        return subtypes[accountType] || [];
    }
    
    generateAccountCode(input, accountType) {
        const prefixes = {
            'asset': '1',
            'liability': '2',
            'equity': '3',
            'income': '4',
            'expense': '5'
        };
        
        const prefix = prefixes[accountType] || '9';
        
        // Generate next available code
        this.getNextAccountCode(prefix).then(code => {
            input.value = code;
        });
    }
    
    async getNextAccountCode(prefix) {
        try {
            const response = await fetch('/api/accounting/get_next_account_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prefix: prefix })
            });
            
            const data = await response.json();
            return data.code;
        } catch (error) {
            console.error('Error getting next account code:', error);
            return `${prefix}001`;
        }
    }
    
    onParentAccountChange(parentId) {
        if (parentId) {
            // Update account level and full code
            this.updateAccountHierarchy(parentId);
        }
    }
    
    updateAccountHierarchy(parentId) {
        // This would update the account level and full code
        // based on the parent account selection
        console.log('Updating account hierarchy for parent:', parentId);
    }
    
    viewMoveLines(accountId) {
        // Open move lines view for the account
        window.open(`/accounting/move_lines?account_id=${accountId}`, '_blank');
    }
    
    reconcileAccount(accountId) {
        // Open reconciliation wizard for the account
        window.open(`/accounting/reconcile?account_id=${accountId}`, '_blank');
    }
    
    generateReport(accountId) {
        // Open report generation for the account
        window.open(`/accounting/report?account_id=${accountId}`, '_blank');
    }
    
    selectAccountRow(row) {
        // Remove previous selection
        document.querySelectorAll('.ocean_account_table tbody tr').forEach(r => {
            r.classList.remove('selected');
        });
        
        // Add selection to current row
        row.classList.add('selected');
        
        // Update form with selected account data
        this.loadAccountData(row.dataset.accountId);
    }
    
    loadAccountData(accountId) {
        // Load account data into form
        fetch(`/api/accounting/account/${accountId}`)
            .then(response => response.json())
            .then(data => {
                this.populateForm(data);
            })
            .catch(error => {
                console.error('Error loading account data:', error);
            });
    }
    
    populateForm(data) {
        // Populate form fields with account data
        Object.keys(data).forEach(key => {
            const field = document.querySelector(`.ocean_account_form [name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        });
    }
    
    sortTable(column) {
        // Sort table by column
        const table = document.querySelector('.ocean_account_table');
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
        this.loadAccountStatistics();
        this.loadJournalStatistics();
        this.loadPeriodStatistics();
    }
    
    async loadAccountStatistics() {
        try {
            const response = await fetch('/api/accounting/statistics/accounts');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_total_accounts').textContent = data.total;
            document.querySelector('.ocean_active_accounts').textContent = data.active;
            document.querySelector('.ocean_reconcilable_accounts').textContent = data.reconcilable;
        } catch (error) {
            console.error('Error loading account statistics:', error);
        }
    }
    
    async loadJournalStatistics() {
        try {
            const response = await fetch('/api/accounting/statistics/journals');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_total_journals').textContent = data.total;
            document.querySelector('.ocean_active_journals').textContent = data.active;
        } catch (error) {
            console.error('Error loading journal statistics:', error);
        }
    }
    
    async loadPeriodStatistics() {
        try {
            const response = await fetch('/api/accounting/statistics/periods');
            const data = await response.json();
            
            // Update dashboard elements
            document.querySelector('.ocean_open_periods').textContent = data.open;
            document.querySelector('.ocean_closed_periods').textContent = data.closed;
        } catch (error) {
            console.error('Error loading period statistics:', error);
        }
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
        loading.className = 'ocean_accounting_loading';
        element.appendChild(loading);
    }
    
    hideLoading(element) {
        const loading = element.querySelector('.ocean_accounting_loading');
        if (loading) {
            loading.remove();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OceanAccounting();
});

// Export for use in other modules
window.OceanAccounting = OceanAccounting;