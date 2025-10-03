/* Kids Clothing ERP - Bulk Import JavaScript */

ocean.define('bulk_import.KidsClothingImport', function (require) {
    'use strict';

    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    var _t = core._t;

    // Import Progress Utilities
    var ImportUtils = {
        formatProgress: function(percentage) {
            return Math.round(percentage) + '%';
        },
        
        getProgressColor: function(percentage) {
            if (percentage < 30) return '#e74c3c'; // Red
            if (percentage < 70) return '#f39c12'; // Orange
            return '#27ae60'; // Green
        },
        
        formatFileSize: function(bytes) {
            if (bytes === 0) return '0 Bytes';
            var k = 1024;
            var sizes = ['Bytes', 'KB', 'MB', 'GB'];
            var i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        validateFileType: function(fileName, allowedTypes) {
            var extension = fileName.split('.').pop().toLowerCase();
            return allowedTypes.includes(extension);
        }
    };

    // Import Wizard Controller
    var ImportWizardController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'change .o_import_file': '_onFileChange',
            'click .o_preview_data': '_onPreviewData',
            'click .o_start_import': '_onStartImport',
            'click .o_reset_wizard': '_onResetWizard'
        }),

        _onFileChange: function(ev) {
            var self = this;
            var file = ev.target.files[0];
            
            if (!file) return;
            
            // Validate file type
            var allowedTypes = ['csv', 'xlsx', 'xls', 'json', 'xml'];
            if (!ImportUtils.validateFileType(file.name, allowedTypes)) {
                Dialog.alert(this, _t('Invalid File Type'), _t('Please select a valid file type (CSV, Excel, JSON, XML)'));
                return;
            }
            
            // Read file content
            var reader = new FileReader();
            reader.onload = function(e) {
                self.model.set('import_data', e.target.result);
                self.model.set('import_file', file.name);
            };
            reader.readAsText(file);
        },

        _onPreviewData: function(ev) {
            ev.preventDefault();
            var self = this;
            
            if (!self.model.get('import_data')) {
                Dialog.alert(this, _t('No Data'), _t('Please upload a file first'));
                return;
            }
            
            self.model.call('action_preview_data').then(function() {
                self.render();
            });
        },

        _onStartImport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            if (!self.model.get('template_id') || !self.model.get('import_data')) {
                Dialog.alert(this, _t('Missing Data'), _t('Please select a template and upload data'));
                return;
            }
            
            Dialog.confirm(this, _t('Start Import'), _t('Are you sure you want to start the import process?'), {
                confirm_callback: function() {
                    self.model.call('action_start_import').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onResetWizard: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Reset Wizard'), _t('Are you sure you want to reset the wizard?'), {
                confirm_callback: function() {
                    self.model.call('action_reset').then(function() {
                        self.render();
                    });
                }
            });
        }
    });

    // Import Job Controller
    var ImportJobController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_start_import': '_onStartImport',
            'click .o_cancel_import': '_onCancelImport',
            'click .o_retry_import': '_onRetryImport',
            'click .o_view_results': '_onViewResults'
        }),

        _onStartImport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Start Import'), _t('Are you sure you want to start this import job?'), {
                confirm_callback: function() {
                    self.model.call('action_start_import').then(function() {
                        self.render();
                        self._startProgressTracking();
                    });
                }
            });
        },

        _onCancelImport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Cancel Import'), _t('Are you sure you want to cancel this import job?'), {
                confirm_callback: function() {
                    self.model.call('action_cancel_import').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onRetryImport: function(ev) {
            ev.preventDefault();
            var self = this;
            
            Dialog.confirm(this, _t('Retry Import'), _t('Are you sure you want to retry this import job?'), {
                confirm_callback: function() {
                    self.model.call('action_retry_import').then(function() {
                        self.render();
                    });
                }
            });
        },

        _onViewResults: function(ev) {
            ev.preventDefault();
            var self = this;
            
            self.model.call('action_view_results').then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },

        _startProgressTracking: function() {
            var self = this;
            var jobId = this.model.get('id');
            
            // Poll for progress updates
            var progressInterval = setInterval(function() {
                rpc.query({
                    model: 'import.job',
                    method: 'read',
                    args: [[jobId], ['progress_percentage', 'state', 'processed_records', 'total_records']]
                }).then(function(result) {
                    if (result && result.length > 0) {
                        var job = result[0];
                        self.model.set('progress_percentage', job.progress_percentage);
                        self.model.set('state', job.state);
                        self.model.set('processed_records', job.processed_records);
                        self.model.set('total_records', job.total_records);
                        
                        // Update progress bar
                        self._updateProgressBar(job.progress_percentage);
                        
                        // Stop polling if job is completed
                        if (job.state === 'completed' || job.state === 'failed' || job.state === 'cancelled') {
                            clearInterval(progressInterval);
                            self.render();
                        }
                    }
                });
            }, 2000); // Poll every 2 seconds
        },

        _updateProgressBar: function(percentage) {
            var $progressBar = this.$('.o_progress_bar');
            if ($progressBar.length) {
                $progressBar.css('width', percentage + '%');
                $progressBar.attr('aria-valuenow', percentage);
                $progressBar.text(ImportUtils.formatProgress(percentage));
            }
        }
    });

    // Import History Controller
    var ImportHistoryController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .o_view_record': '_onViewRecord',
            'click .o_retry_import': '_onRetryImport',
            'click .o_rollback': '_onRollback',
            'click .o_export_errors': '_onExportErrors'
        }),

        _onViewRecord: function(ev) {
            ev.preventDefault();
            var self = this;
            var recordId = $(ev.currentTarget).data('record-id');
            
            rpc.query({
                model: 'import.history',
                method: 'action_view_record',
                args: [recordId]
            }).then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        },

        _onRetryImport: function(ev) {
            ev.preventDefault();
            var self = this;
            var recordId = $(ev.currentTarget).data('record-id');
            
            Dialog.confirm(this, _t('Retry Import'), _t('Are you sure you want to retry importing this record?'), {
                confirm_callback: function() {
                    rpc.query({
                        model: 'import.history',
                        method: 'action_retry_import',
                        args: [recordId]
                    }).then(function() {
                        self.reload();
                    });
                }
            });
        },

        _onRollback: function(ev) {
            ev.preventDefault();
            var self = this;
            var recordId = $(ev.currentTarget).data('record-id');
            
            Dialog.confirm(this, _t('Rollback'), _t('Are you sure you want to rollback this import? This will delete the created record.'), {
                confirm_callback: function() {
                    rpc.query({
                        model: 'import.history',
                        method: 'action_rollback',
                        args: [recordId]
                    }).then(function() {
                        self.reload();
                    });
                }
            });
        },

        _onExportErrors: function(ev) {
            ev.preventDefault();
            var self = this;
            var recordId = $(ev.currentTarget).data('record-id');
            
            rpc.query({
                model: 'import.history',
                method: 'action_export_errors',
                args: [recordId]
            }).then(function(result) {
                if (result) {
                    self.do_action(result);
                }
            });
        }
    });

    return {
        ImportWizardController: ImportWizardController,
        ImportJobController: ImportJobController,
        ImportHistoryController: ImportHistoryController,
        ImportUtils: ImportUtils
    };
});