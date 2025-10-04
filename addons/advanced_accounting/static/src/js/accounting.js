/* Advanced Accounting JavaScript for Kids Clothing ERP */

// Accounting Dashboard functionality
class AccountingDashboard {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadDashboardData();
    }
    
    bindEvents() {
        // Bind dashboard refresh button
        $(document).on('click', '.accounting-refresh-btn', () => {
            this.refreshDashboard();
        });
        
        // Bind account balance button
        $(document).on('click', '.account-balance-btn', (e) => {
            const accountId = $(e.currentTarget).data('account-id');
            this.showAccountBalance(accountId);
        });
        
        // Bind journal entry button
        $(document).on('click', '.create-journal-entry-btn', () => {
            this.createJournalEntry();
        });
        
        // Bind budget analysis button
        $(document).on('click', '.budget-analysis-btn', () => {
            this.showBudgetAnalysis();
        });
    }
    
    loadDashboardData() {
        // Load dashboard data via AJAX
        $.ajax({
            url: '/advanced_accounting/dashboard_data',
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
        // Update account statistics
        $('.total-accounts').text(data.total_accounts);
        $('.active-accounts').text(data.active_accounts);
        $('.reconcilable-accounts').text(data.reconcilable_accounts);
        
        // Update journal statistics
        $('.total-journals').text(data.total_journals);
        $('.active-journals').text(data.active_journals);
        $('.total-entries').text(data.total_entries);
        
        // Update budget statistics
        $('.total-budgets').text(data.total_budgets);
        $('.approved-budgets').text(data.approved_budgets);
        $('.budget-variance').text(this.formatCurrency(data.budget_variance));
        
        // Update cost center statistics
        $('.total-cost-centers').text(data.total_cost_centers);
        $('.active-cost-centers').text(data.active_cost_centers);
        $('.total-expenses').text(this.formatCurrency(data.total_expenses));
        $('.total-revenue').text(this.formatCurrency(data.total_revenue));
    }
    
    refreshDashboard() {
        this.loadDashboardData();
        this.showNotification('Dashboard refreshed', 'success');
    }
    
    showAccountBalance(accountId) {
        // Show account balance in a modal
        $.ajax({
            url: '/advanced_accounting/account_balance',
            type: 'GET',
            data: { account_id: accountId },
            success: (balanceData) => {
                this.displayAccountBalance(balanceData);
            },
            error: (error) => {
                this.showNotification('Error loading account balance', 'error');
            }
        });
    }
    
    displayAccountBalance(balanceData) {
        const modal = $(`
            <div class="modal fade" id="accountBalanceModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Account Balance - ${balanceData.account_name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <strong>Opening Balance:</strong> ${this.formatCurrency(balanceData.opening_balance)}
                                </div>
                                <div class="col-md-6">
                                    <strong>Current Balance:</strong> ${this.formatCurrency(balanceData.current_balance)}
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <strong>Total Debit:</strong> ${this.formatCurrency(balanceData.total_debit)}
                                </div>
                                <div class="col-md-6">
                                    <strong>Total Credit:</strong> ${this.formatCurrency(balanceData.total_credit)}
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $('body').append(modal);
        modal.modal('show');
        
        modal.on('hidden.bs.modal', function() {
            modal.remove();
        });
    }
    
    createJournalEntry() {
        // Open journal entry creation form
        window.open('/advanced_accounting/journal_entry_form', '_blank', 'width=1000,height=700');
    }
    
    showBudgetAnalysis() {
        // Show budget analysis in a modal
        $.ajax({
            url: '/advanced_accounting/budget_analysis',
            type: 'GET',
            success: (budgetData) => {
                this.displayBudgetAnalysis(budgetData);
            },
            error: (error) => {
                this.showNotification('Error loading budget analysis', 'error');
            }
        });
    }
    
    displayBudgetAnalysis(budgetData) {
        const modal = $(`
            <div class="modal fade" id="budgetAnalysisModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Budget Analysis</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Total Budget</h6>
                                            <h4 class="text-primary">${this.formatCurrency(budgetData.total_budget)}</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Total Actual</h6>
                                            <h4 class="text-info">${this.formatCurrency(budgetData.total_actual)}</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Variance</h6>
                                            <h4 class="${budgetData.variance >= 0 ? 'text-success' : 'text-danger'}">${this.formatCurrency(budgetData.variance)}</h4>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3">
                                <h6>Budget Lines</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Account</th>
                                                <th>Budget</th>
                                                <th>Actual</th>
                                                <th>Variance</th>
                                                <th>%</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${budgetData.lines.map(line => `
                                                <tr>
                                                    <td>${line.account_name}</td>
                                                    <td>${this.formatCurrency(line.budget_amount)}</td>
                                                    <td>${this.formatCurrency(line.actual_amount)}</td>
                                                    <td class="${line.variance >= 0 ? 'text-success' : 'text-danger'}">${this.formatCurrency(line.variance)}</td>
                                                    <td class="${line.variance_percentage >= 0 ? 'text-success' : 'text-danger'}">${line.variance_percentage.toFixed(1)}%</td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $('body').append(modal);
        modal.modal('show');
        
        modal.on('hidden.bs.modal', function() {
            modal.remove();
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
            <div class="accounting-notification accounting-notification-${type} accounting-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Journal Entry functionality
class JournalEntryManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind add line button
        $(document).on('click', '.add-journal-line-btn', () => {
            this.addJournalLine();
        });
        
        // Bind remove line button
        $(document).on('click', '.remove-journal-line-btn', (e) => {
            $(e.currentTarget).closest('.journal-line').remove();
            this.updateTotals();
        });
        
        // Bind line change events
        $(document).on('change', '.journal-line input', () => {
            this.updateTotals();
        });
        
        // Bind post button
        $(document).on('click', '.post-journal-entry-btn', () => {
            this.postJournalEntry();
        });
    }
    
    addJournalLine() {
        const lineTemplate = `
            <div class="journal-line row mb-2">
                <div class="col-md-3">
                    <select class="form-select account-select">
                        <option value="">Select Account</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <input type="text" class="form-control description-input" placeholder="Description">
                </div>
                <div class="col-md-2">
                    <input type="number" class="form-control debit-input" placeholder="Debit" step="0.01">
                </div>
                <div class="col-md-2">
                    <input type="number" class="form-control credit-input" placeholder="Credit" step="0.01">
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-danger btn-sm remove-journal-line-btn">Remove</button>
                </div>
            </div>
        `;
        
        $('.journal-lines').append(lineTemplate);
        this.loadAccounts();
    }
    
    loadAccounts() {
        // Load accounts for select dropdowns
        $.ajax({
            url: '/advanced_accounting/get_accounts',
            type: 'GET',
            success: (accounts) => {
                $('.account-select').each(function() {
                    const select = $(this);
                    if (select.find('option').length <= 1) {
                        accounts.forEach(account => {
                            select.append(`<option value="${account.id}">${account.code} - ${account.name}</option>`);
                        });
                    }
                });
            },
            error: (error) => {
                console.error('Error loading accounts:', error);
            }
        });
    }
    
    updateTotals() {
        let totalDebit = 0;
        let totalCredit = 0;
        
        $('.journal-line').each(function() {
            const debit = parseFloat($(this).find('.debit-input').val()) || 0;
            const credit = parseFloat($(this).find('.credit-input').val()) || 0;
            
            totalDebit += debit;
            totalCredit += credit;
        });
        
        $('.total-debit').text(this.formatCurrency(totalDebit));
        $('.total-credit').text(this.formatCurrency(totalCredit));
        
        const difference = totalDebit - totalCredit;
        $('.total-difference').text(this.formatCurrency(difference));
        
        if (Math.abs(difference) < 0.01) {
            $('.total-difference').removeClass('text-danger').addClass('text-success');
            $('.post-journal-entry-btn').prop('disabled', false);
        } else {
            $('.total-difference').removeClass('text-success').addClass('text-danger');
            $('.post-journal-entry-btn').prop('disabled', true);
        }
    }
    
    postJournalEntry() {
        const entryData = {
            name: $('.entry-name').val(),
            ref: $('.entry-ref').val(),
            date: $('.entry-date').val(),
            journal_id: $('.journal-select').val(),
            narration: $('.entry-narration').val(),
            lines: []
        };
        
        $('.journal-line').each(function() {
            const line = {
                account_id: $(this).find('.account-select').val(),
                name: $(this).find('.description-input').val(),
                debit: parseFloat($(this).find('.debit-input').val()) || 0,
                credit: parseFloat($(this).find('.credit-input').val()) || 0
            };
            
            if (line.account_id && (line.debit > 0 || line.credit > 0)) {
                entryData.lines.push(line);
            }
        });
        
        $.ajax({
            url: '/advanced_accounting/post_journal_entry',
            type: 'POST',
            data: JSON.stringify(entryData),
            contentType: 'application/json',
            success: (response) => {
                this.showNotification('Journal entry posted successfully', 'success');
                this.resetForm();
            },
            error: (error) => {
                this.showNotification('Error posting journal entry', 'error');
            }
        });
    }
    
    resetForm() {
        $('.journal-lines').empty();
        $('.entry-name').val('');
        $('.entry-ref').val('');
        $('.entry-narration').val('');
        this.updateTotals();
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="accounting-notification accounting-notification-${type} accounting-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize accounting components when document is ready
$(document).ready(function() {
    // Initialize dashboard if element exists
    if ($('.accounting-dashboard').length) {
        new AccountingDashboard();
    }
    
    // Initialize journal entry manager if element exists
    if ($('.journal-entry-form').length) {
        new JournalEntryManager();
    }
});