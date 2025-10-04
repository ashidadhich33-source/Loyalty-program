/* Accounting JavaScript */

odoo.define('accounting.accounting', function (require) {
    'use strict';

    var core = require('web.core');
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var KanbanView = require('web.KanbanView');
    var AbstractAction = require('web.AbstractAction');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');

    var _t = core._t;

    // Accounting Dashboard
    var AccountingDashboard = AbstractAction.extend({
        template: 'accounting.AccountingDashboard',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadDashboardData();
        },
        
        loadDashboardData: function () {
            var self = this;
            
            // Load account statistics
            rpc.query({
                model: 'account.account',
                method: 'search_count',
                args: [[('active', '=', True)]],
            }).then(function (totalAccounts) {
                self.$('.o_total_accounts_count').text(totalAccounts);
            });
            
            // Load journal statistics
            rpc.query({
                model: 'account.journal',
                method: 'search_count',
                args: [[('active', '=', True)]],
            }).then(function (totalJournals) {
                self.$('.o_total_journals_count').text(totalJournals);
            });
            
            // Load journal entry statistics
            rpc.query({
                model: 'account.move',
                method: 'search_count',
                args: [[('state', '=', 'posted')]],
            }).then(function (totalEntries) {
                self.$('.o_total_entries_count').text(totalEntries);
            });
            
            // Load period statistics
            rpc.query({
                model: 'account.period',
                method: 'search_count',
                args: [[('state', '=', 'open')]],
            }).then(function (openPeriods) {
                self.$('.o_open_periods_count').text(openPeriods);
            });
        }
    });

    // Chart of Accounts Manager
    var ChartOfAccountsManager = AbstractAction.extend({
        template: 'accounting.ChartOfAccountsManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadChartOfAccounts();
        },
        
        loadChartOfAccounts: function () {
            var self = this;
            rpc.query({
                model: 'account.account',
                method: 'search_read',
                args: [[], ['code', 'name', 'account_type', 'account_subtype', 'balance', 'debit', 'credit', 'reconcile', 'active']],
            }).then(function (accounts) {
                self.renderChartOfAccounts(accounts);
            });
        },
        
        renderChartOfAccounts: function (accounts) {
            var self = this;
            var $accountsContainer = this.$('.o_accounts_container');
            
            accounts.forEach(function (account) {
                var $account = self.createAccountElement(account);
                $accountsContainer.append($account);
            });
        },
        
        createAccountElement: function (account) {
            var typeClass = 'o_account_type_' + account.account_type;
            var subtypeClass = 'o_account_subtype_' + account.account_subtype;
            
            var $account = $('<div>')
                .addClass('o_account_card')
                .addClass(typeClass)
                .addClass(subtypeClass)
                .html(
                    '<div class="o_account_header">' +
                        '<h4>' + account.name + '</h4>' +
                        '<span class="o_account_code">' + account.code + '</span>' +
                    '</div>' +
                    '<div class="o_account_body">' +
                        '<p><strong>Type:</strong> ' + account.account_type + '</p>' +
                        '<p><strong>Subtype:</strong> ' + account.account_subtype + '</p>' +
                        '<p><strong>Balance:</strong> ' + account.balance + '</p>' +
                        '<p><strong>Debit:</strong> ' + account.debit + '</p>' +
                        '<p><strong>Credit:</strong> ' + account.credit + '</p>' +
                        '<p><strong>Reconcile:</strong> ' + (account.reconcile ? 'Yes' : 'No') + '</p>' +
                    '</div>' +
                    '<div class="o_account_actions">' +
                        '<button class="o_accounting_btn_primary o_view_lines_btn">View Lines</button>' +
                        '<button class="o_accounting_btn_success o_reconcile_btn">Reconcile</button>' +
                    '</div>'
                );
            
            // Add click handlers
            $account.find('.o_view_lines_btn').on('click', function () {
                self.viewAccountLines(account.id);
            });
            
            $account.find('.o_reconcile_btn').on('click', function () {
                self.reconcileAccount(account.id);
            });
            
            return $account;
        },
        
        viewAccountLines: function (accountId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Account Move Lines',
                res_model: 'account.move.line',
                view_mode: 'tree,form',
                domain: [('account_id', '=', accountId)],
                context: {'default_account_id': accountId},
            });
        },
        
        reconcileAccount: function (accountId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Reconcile Account',
                res_model: 'account.reconciliation',
                view_mode: 'form',
                context: {'default_account_id': accountId},
                target: 'new',
            });
        }
    });

    // Journal Manager
    var JournalManager = AbstractAction.extend({
        template: 'accounting.JournalManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadJournals();
        },
        
        loadJournals: function () {
            var self = this;
            rpc.query({
                model: 'account.journal',
                method: 'search_read',
                args: [[], ['name', 'code', 'type', 'total_entries', 'total_debit', 'total_credit', 'active']],
            }).then(function (journals) {
                self.renderJournals(journals);
            });
        },
        
        renderJournals: function (journals) {
            var self = this;
            var $journalsContainer = this.$('.o_journals_container');
            
            journals.forEach(function (journal) {
                var $journal = self.createJournalElement(journal);
                $journalsContainer.append($journal);
            });
        },
        
        createJournalElement: function (journal) {
            var typeClass = 'o_journal_type_' + journal.type;
            
            var $journal = $('<div>')
                .addClass('o_journal_card')
                .addClass(typeClass)
                .html(
                    '<div class="o_journal_header">' +
                        '<h4>' + journal.name + '</h4>' +
                        '<span class="o_journal_code">' + journal.code + '</span>' +
                    '</div>' +
                    '<div class="o_journal_body">' +
                        '<p><strong>Type:</strong> ' + journal.type + '</p>' +
                        '<p><strong>Entries:</strong> ' + journal.total_entries + '</p>' +
                        '<p><strong>Debit:</strong> ' + journal.total_debit + '</p>' +
                        '<p><strong>Credit:</strong> ' + journal.total_credit + '</p>' +
                    '</div>' +
                    '<div class="o_journal_actions">' +
                        '<button class="o_accounting_btn_primary o_create_entry_btn">Create Entry</button>' +
                        '<button class="o_accounting_btn_success o_view_entries_btn">View Entries</button>' +
                    </div>'
                );
            
            // Add click handlers
            $journal.find('.o_create_entry_btn').on('click', function () {
                self.createJournalEntry(journal.id);
            });
            
            $journal.find('.o_view_entries_btn').on('click', function () {
                self.viewJournalEntries(journal.id);
            });
            
            return $journal;
        },
        
        createJournalEntry: function (journalId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Create Journal Entry',
                res_model: 'account.move',
                view_mode: 'form',
                context: {'default_journal_id': journalId},
                target: 'current',
            });
        },
        
        viewJournalEntries: function (journalId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Journal Entries',
                res_model: 'account.move',
                view_mode: 'tree,form',
                domain: [('journal_id', '=', journalId)],
                context: {'default_journal_id': journalId},
            });
        }
    });

    // Journal Entry Manager
    var JournalEntryManager = AbstractAction.extend({
        template: 'accounting.JournalEntryManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadJournalEntries();
        },
        
        loadJournalEntries: function () {
            var self = this;
            rpc.query({
                model: 'account.move',
                method: 'search_read',
                args: [[], ['name', 'date', 'journal_id', 'ref', 'state', 'total_debit', 'total_credit', 'balance']],
            }).then(function (entries) {
                self.renderJournalEntries(entries);
            });
        },
        
        renderJournalEntries: function (entries) {
            var self = this;
            var $entriesContainer = this.$('.o_journal_entries_container');
            
            entries.forEach(function (entry) {
                var $entry = self.createJournalEntryElement(entry);
                $entriesContainer.append($entry);
            });
        },
        
        createJournalEntryElement: function (entry) {
            var stateClass = 'o_journal_entry_' + entry.state;
            
            var $entry = $('<div>')
                .addClass('o_journal_entry_card')
                .addClass(stateClass)
                .html(
                    '<div class="o_entry_header">' +
                        '<h4>' + entry.name + '</h4>' +
                        '<span class="o_entry_state">' + entry.state + '</span>' +
                    '</div>' +
                    '<div class="o_entry_body">' +
                        '<p><strong>Date:</strong> ' + entry.date + '</p>' +
                        '<p><strong>Journal:</strong> ' + entry.journal_id[1] + '</p>' +
                        '<p><strong>Reference:</strong> ' + entry.ref + '</p>' +
                        '<p><strong>Debit:</strong> ' + entry.total_debit + '</p>' +
                        '<p><strong>Credit:</strong> ' + entry.total_credit + '</p>' +
                        '<p><strong>Balance:</strong> ' + entry.balance + '</p>' +
                    '</div>' +
                    '<div class="o_entry_actions">' +
                        '<button class="o_accounting_btn_primary o_post_btn">Post</button>' +
                        '<button class="o_accounting_btn_success o_view_btn">View</button>' +
                    </div>'
                );
            
            // Add click handlers
            $entry.find('.o_post_btn').on('click', function () {
                self.postJournalEntry(entry.id);
            });
            
            $entry.find('.o_view_btn').on('click', function () {
                self.viewJournalEntry(entry.id);
            });
            
            return $entry;
        },
        
        postJournalEntry: function (entryId) {
            var self = this;
            rpc.query({
                model: 'account.move',
                method: 'action_post',
                args: [entryId],
            }).then(function () {
                self.loadJournalEntries();
            });
        },
        
        viewJournalEntry: function (entryId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Journal Entry',
                res_model: 'account.move',
                res_id: entryId,
                view_mode: 'form',
                target: 'current',
            });
        }
    });

    // Period Manager
    var PeriodManager = AbstractAction.extend({
        template: 'accounting.PeriodManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadPeriods();
        },
        
        loadPeriods: function () {
            var self = this;
            rpc.query({
                model: 'account.period',
                method: 'search_read',
                args: [[], ['name', 'code', 'date_start', 'date_stop', 'state', 'total_entries', 'total_debit', 'total_credit']],
            }).then(function (periods) {
                self.renderPeriods(periods);
            });
        },
        
        renderPeriods: function (periods) {
            var self = this;
            var $periodsContainer = this.$('.o_periods_container');
            
            periods.forEach(function (period) {
                var $period = self.createPeriodElement(period);
                $periodsContainer.append($period);
            });
        },
        
        createPeriodElement: function (period) {
            var stateClass = 'o_period_' + period.state;
            
            var $period = $('<div>')
                .addClass('o_period_card')
                .addClass(stateClass)
                .html(
                    '<div class="o_period_header">' +
                        '<h4>' + period.name + '</h4>' +
                        '<span class="o_period_state">' + period.state + '</span>' +
                    '</div>' +
                    '<div class="o_period_body">' +
                        '<p><strong>Code:</strong> ' + period.code + '</p>' +
                        '<p><strong>Start:</strong> ' + period.date_start + '</p>' +
                        '<p><strong>End:</strong> ' + period.date_stop + '</p>' +
                        '<p><strong>Entries:</strong> ' + period.total_entries + '</p>' +
                        '<p><strong>Debit:</strong> ' + period.total_debit + '</p>' +
                        '<p><strong>Credit:</strong> ' + period.total_credit + '</p>' +
                    '</div>' +
                    '<div class="o_period_actions">' +
                        '<button class="o_accounting_btn_primary o_open_btn">Open</button>' +
                        '<button class="o_accounting_btn_success o_close_btn">Close</button>' +
                    </div>'
                );
            
            // Add click handlers
            $period.find('.o_open_btn').on('click', function () {
                self.openPeriod(period.id);
            });
            
            $period.find('.o_close_btn').on('click', function () {
                self.closePeriod(period.id);
            });
            
            return $period;
        },
        
        openPeriod: function (periodId) {
            var self = this;
            rpc.query({
                model: 'account.period',
                method: 'action_open',
                args: [periodId],
            }).then(function () {
                self.loadPeriods();
            });
        },
        
        closePeriod: function (periodId) {
            var self = this;
            rpc.query({
                model: 'account.period',
                method: 'action_close',
                args: [periodId],
            }).then(function () {
                self.loadPeriods();
            });
        }
    });

    // Report Manager
    var ReportManager = AbstractAction.extend({
        template: 'accounting.ReportManager',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.action = action;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this.loadReports();
        },
        
        loadReports: function () {
            var self = this;
            rpc.query({
                model: 'account.report',
                method: 'search_read',
                args: [[], ['name', 'report_type', 'date_from', 'date_to', 'state', 'total_accounts', 'total_amount']],
            }).then(function (reports) {
                self.renderReports(reports);
            });
        },
        
        renderReports: function (reports) {
            var self = this;
            var $reportsContainer = this.$('.o_reports_container');
            
            reports.forEach(function (report) {
                var $report = self.createReportElement(report);
                $reportsContainer.append($report);
            });
        },
        
        createReportElement: function (report) {
            var stateClass = 'o_report_' + report.state;
            
            var $report = $('<div>')
                .addClass('o_report_card')
                .addClass(stateClass)
                .html(
                    '<div class="o_report_header">' +
                        '<h4>' + report.name + '</h4>' +
                        '<span class="o_report_state">' + report.state + '</span>' +
                    '</div>' +
                    '<div class="o_report_body">' +
                        '<p><strong>Type:</strong> ' + report.report_type + '</p>' +
                        '<p><strong>From:</strong> ' + report.date_from + '</p>' +
                        '<p><strong>To:</strong> ' + report.date_to + '</p>' +
                        '<p><strong>Accounts:</strong> ' + report.total_accounts + '</p>' +
                        '<p><strong>Amount:</strong> ' + report.total_amount + '</p>' +
                    '</div>' +
                    '<div class="o_report_actions">' +
                        '<button class="o_accounting_btn_primary o_generate_btn">Generate</button>' +
                        '<button class="o_accounting_btn_success o_view_btn">View</button>' +
                    </div>'
                );
            
            // Add click handlers
            $report.find('.o_generate_btn').on('click', function () {
                self.generateReport(report.id);
            });
            
            $report.find('.o_view_btn').on('click', function () {
                self.viewReport(report.id);
            });
            
            return $report;
        },
        
        generateReport: function (reportId) {
            var self = this;
            rpc.query({
                model: 'account.report',
                method: 'action_generate',
                args: [reportId],
            }).then(function () {
                self.loadReports();
            });
        },
        
        viewReport: function (reportId) {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Report',
                res_model: 'account.report',
                res_id: reportId,
                view_mode: 'form',
                target: 'current',
            });
        }
    });

    // Utility Functions
    var AccountingUtils = {
        formatCurrency: function (amount) {
            return new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR'
            }).format(amount);
        },
        
        formatNumber: function (number) {
            return new Intl.NumberFormat('en-IN').format(number);
        },
        
        formatDate: function (date) {
            return new Date(date).toLocaleDateString('en-IN');
        },
        
        formatDateTime: function (datetime) {
            return new Date(datetime).toLocaleString('en-IN');
        },
        
        showNotification: function (title, message, type) {
            var notification = new Dialog(this, {
                title: title,
                size: 'medium',
                buttons: [
                    {
                        text: 'OK',
                        click: function () {
                            notification.close();
                        }
                    }
                ]
            });
            
            notification.appendTo($('<div>').html(message));
            notification.open();
        },
        
        showLoading: function (element) {
            var $loading = $('<div>').addClass('o_accounting_loading');
            $(element).append($loading);
        },
        
        hideLoading: function (element) {
            $(element).find('.o_accounting_loading').remove();
        }
    };

    // Register actions
    core.action_registry.add('accounting_dashboard', AccountingDashboard);
    core.action_registry.add('chart_of_accounts_manager', ChartOfAccountsManager);
    core.action_registry.add('journal_manager', JournalManager);
    core.action_registry.add('journal_entry_manager', JournalEntryManager);
    core.action_registry.add('period_manager', PeriodManager);
    core.action_registry.add('report_manager', ReportManager);

    return {
        AccountingDashboard: AccountingDashboard,
        ChartOfAccountsManager: ChartOfAccountsManager,
        JournalManager: JournalManager,
        JournalEntryManager: JournalEntryManager,
        PeriodManager: PeriodManager,
        ReportManager: ReportManager,
        AccountingUtils: AccountingUtils
    };
});