/* Database Management JavaScript */

odoo.define('database.database_script', function (require) {
    'use strict';

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var utils = require('web.utils');

    var _t = core._t;
    var QWeb = core.qweb;

    // Database Connection Widget
    var DatabaseConnectionWidget = AbstractAction.extend({
        template: 'database.connection_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.connection_status = 'disconnected';
            this.connection_interval = null;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._start_connection_monitoring();
            this._bind_events();
        },
        
        _start_connection_monitoring: function () {
            var self = this;
            this.connection_interval = setInterval(function () {
                self._check_connection_status();
            }, 5000);
        },
        
        _check_connection_status: function () {
            var self = this;
            rpc.query({
                model: 'database.connection',
                method: 'check_connection_status',
                args: [this.database_id]
            }).then(function (result) {
                self.connection_status = result.status;
                self._update_connection_display();
            });
        },
        
        _update_connection_display: function () {
            var $status = this.$('.database-connection-status');
            $status.removeClass('connected disconnected connecting');
            $status.addClass(this.connection_status);
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-connect').on('click', function () {
                self._connect_database();
            });
            this.$('.btn-disconnect').on('click', function () {
                self._disconnect_database();
            });
            this.$('.btn-test-connection').on('click', function () {
                self._test_connection();
            });
        },
        
        _connect_database: function () {
            var self = this;
            rpc.query({
                model: 'database.connection',
                method: 'connect',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self.connection_status = 'connected';
                    self._update_connection_display();
                    self._show_notification(_t('Database connected successfully'), 'success');
                } else {
                    self._show_notification(_t('Failed to connect to database'), 'danger');
                }
            });
        },
        
        _disconnect_database: function () {
            var self = this;
            rpc.query({
                model: 'database.connection',
                method: 'disconnect',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self.connection_status = 'disconnected';
                    self._update_connection_display();
                    self._show_notification(_t('Database disconnected successfully'), 'success');
                } else {
                    self._show_notification(_t('Failed to disconnect database'), 'danger');
                }
            });
        },
        
        _test_connection: function () {
            var self = this;
            rpc.query({
                model: 'database.connection',
                method: 'test_connection',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._show_notification(_t('Connection test successful'), 'success');
                } else {
                    self._show_notification(_t('Connection test failed'), 'danger');
                }
            });
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Management'), message, type);
        },
        
        destroy: function () {
            if (this.connection_interval) {
                clearInterval(this.connection_interval);
            }
            this._super.apply(this, arguments);
        }
    });

    // Database Backup Widget
    var DatabaseBackupWidget = AbstractAction.extend({
        template: 'database.backup_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.backup_progress = 0;
            this.backup_status = 'idle';
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._bind_events();
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-start-backup').on('click', function () {
                self._start_backup();
            });
            this.$('.btn-stop-backup').on('click', function () {
                self._stop_backup();
            });
            this.$('.btn-restore-backup').on('click', function () {
                self._restore_backup();
            });
        },
        
        _start_backup: function () {
            var self = this;
            this.backup_status = 'running';
            this.backup_progress = 0;
            this._update_backup_display();
            
            rpc.query({
                model: 'database.backup',
                method: 'start_backup',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._monitor_backup_progress(result.backup_id);
                } else {
                    self.backup_status = 'failed';
                    self._update_backup_display();
                    self._show_notification(_t('Backup failed to start'), 'danger');
                }
            });
        },
        
        _stop_backup: function () {
            var self = this;
            rpc.query({
                model: 'database.backup',
                method: 'stop_backup',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self.backup_status = 'stopped';
                    self._update_backup_display();
                    self._show_notification(_t('Backup stopped'), 'warning');
                } else {
                    self._show_notification(_t('Failed to stop backup'), 'danger');
                }
            });
        },
        
        _restore_backup: function () {
            var self = this;
            Dialog.confirm(this, _t('Are you sure you want to restore this backup? This will overwrite the current database.'), {
                title: _t('Confirm Restore'),
                confirm_callback: function () {
                    self._perform_restore();
                }
            });
        },
        
        _perform_restore: function () {
            var self = this;
            rpc.query({
                model: 'database.backup',
                method: 'restore_backup',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._show_notification(_t('Backup restored successfully'), 'success');
                } else {
                    self._show_notification(_t('Backup restore failed'), 'danger');
                }
            });
        },
        
        _monitor_backup_progress: function (backup_id) {
            var self = this;
            var progress_interval = setInterval(function () {
                rpc.query({
                    model: 'database.backup',
                    method: 'get_backup_progress',
                    args: [backup_id]
                }).then(function (result) {
                    self.backup_progress = result.progress;
                    self._update_backup_display();
                    
                    if (result.status === 'completed') {
                        clearInterval(progress_interval);
                        self.backup_status = 'completed';
                        self._update_backup_display();
                        self._show_notification(_t('Backup completed successfully'), 'success');
                    } else if (result.status === 'failed') {
                        clearInterval(progress_interval);
                        self.backup_status = 'failed';
                        self._update_backup_display();
                        self._show_notification(_t('Backup failed'), 'danger');
                    }
                });
            }, 1000);
        },
        
        _update_backup_display: function () {
            var $progress = this.$('.database-backup-progress-bar');
            $progress.css('width', this.backup_progress + '%');
            
            var $status = this.$('.backup-status');
            $status.text(this.backup_status);
            $status.removeClass('idle running completed failed stopped');
            $status.addClass(this.backup_status);
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Backup'), message, type);
        }
    });

    // Database Monitoring Widget
    var DatabaseMonitoringWidget = AbstractAction.extend({
        template: 'database.monitoring_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.monitoring_data = {};
            this.monitoring_interval = null;
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._start_monitoring();
            this._bind_events();
        },
        
        _start_monitoring: function () {
            var self = this;
            this._update_monitoring_data();
            this.monitoring_interval = setInterval(function () {
                self._update_monitoring_data();
            }, 5000);
        },
        
        _update_monitoring_data: function () {
            var self = this;
            rpc.query({
                model: 'database.monitoring',
                method: 'get_monitoring_data',
                args: [this.database_id]
            }).then(function (result) {
                self.monitoring_data = result;
                self._update_monitoring_display();
            });
        },
        
        _update_monitoring_display: function () {
            var data = this.monitoring_data;
            
            // Update CPU usage
            this.$('.cpu-usage').text(data.cpu_usage + '%');
            this.$('.cpu-usage').removeClass('low medium high critical');
            this.$('.cpu-usage').addClass(this._get_usage_class(data.cpu_usage));
            
            // Update Memory usage
            this.$('.memory-usage').text(data.memory_usage + '%');
            this.$('.memory-usage').removeClass('low medium high critical');
            this.$('.memory-usage').addClass(this._get_usage_class(data.memory_usage));
            
            // Update Disk I/O
            this.$('.disk-io').text(data.disk_io + ' MB/s');
            
            // Update Active Connections
            this.$('.active-connections').text(data.active_connections);
            
            // Update Query Performance
            this.$('.query-performance').text(data.query_performance + ' ms');
        },
        
        _get_usage_class: function (usage) {
            if (usage < 50) return 'low';
            if (usage < 75) return 'medium';
            if (usage < 90) return 'high';
            return 'critical';
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-refresh').on('click', function () {
                self._update_monitoring_data();
            });
            this.$('.btn-export-data').on('click', function () {
                self._export_monitoring_data();
            });
        },
        
        _export_monitoring_data: function () {
            var self = this;
            rpc.query({
                model: 'database.monitoring',
                method: 'export_monitoring_data',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._download_file(result.file_url, 'monitoring_data.csv');
                    self._show_notification(_t('Monitoring data exported successfully'), 'success');
                } else {
                    self._show_notification(_t('Failed to export monitoring data'), 'danger');
                }
            });
        },
        
        _download_file: function (url, filename) {
            var link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Monitoring'), message, type);
        },
        
        destroy: function () {
            if (this.monitoring_interval) {
                clearInterval(this.monitoring_interval);
            }
            this._super.apply(this, arguments);
        }
    });

    // Database Analytics Widget
    var DatabaseAnalyticsWidget = AbstractAction.extend({
        template: 'database.analytics_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.analytics_data = {};
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._load_analytics_data();
            this._bind_events();
        },
        
        _load_analytics_data: function () {
            var self = this;
            rpc.query({
                model: 'database.analytics',
                method: 'get_analytics_data',
                args: [this.database_id]
            }).then(function (result) {
                self.analytics_data = result;
                self._update_analytics_display();
            });
        },
        
        _update_analytics_display: function () {
            var data = this.analytics_data;
            
            // Update usage patterns
            this.$('.usage-patterns').text(data.usage_patterns);
            
            // Update performance trends
            this.$('.performance-trends').text(data.performance_trends);
            
            // Update capacity planning
            this.$('.capacity-planning').text(data.capacity_planning);
            
            // Update recommendations
            this.$('.recommendations').text(data.recommendations);
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-refresh').on('click', function () {
                self._load_analytics_data();
            });
            this.$('.btn-export-analytics').on('click', function () {
                self._export_analytics_data();
            });
        },
        
        _export_analytics_data: function () {
            var self = this;
            rpc.query({
                model: 'database.analytics',
                method: 'export_analytics_data',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._download_file(result.file_url, 'analytics_data.csv');
                    self._show_notification(_t('Analytics data exported successfully'), 'success');
                } else {
                    self._show_notification(_t('Failed to export analytics data'), 'danger');
                }
            });
        },
        
        _download_file: function (url, filename) {
            var link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Analytics'), message, type);
        }
    });

    // Database Security Widget
    var DatabaseSecurityWidget = AbstractAction.extend({
        template: 'database.security_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.security_data = {};
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._load_security_data();
            this._bind_events();
        },
        
        _load_security_data: function () {
            var self = this;
            rpc.query({
                model: 'database.security',
                method: 'get_security_data',
                args: [this.database_id]
            }).then(function (result) {
                self.security_data = result;
                self._update_security_display();
            });
        },
        
        _update_security_display: function () {
            var data = this.security_data;
            
            // Update security status
            this.$('.security-status').text(data.status);
            this.$('.security-status').removeClass('active inactive warning critical');
            this.$('.security-status').addClass(data.status);
            
            // Update encryption status
            this.$('.encryption-status').text(data.encryption_enabled ? 'Enabled' : 'Disabled');
            this.$('.encryption-status').removeClass('enabled disabled');
            this.$('.encryption-status').addClass(data.encryption_enabled ? 'enabled' : 'disabled');
            
            // Update SSL status
            this.$('.ssl-status').text(data.ssl_enabled ? 'Enabled' : 'Disabled');
            this.$('.ssl-status').removeClass('enabled disabled');
            this.$('.ssl-status').addClass(data.ssl_enabled ? 'enabled' : 'disabled');
            
            // Update firewall status
            this.$('.firewall-status').text(data.firewall_enabled ? 'Enabled' : 'Disabled');
            this.$('.firewall-status').removeClass('enabled disabled');
            this.$('.firewall-status').addClass(data.firewall_enabled ? 'enabled' : 'disabled');
            
            // Update audit status
            this.$('.audit-status').text(data.audit_enabled ? 'Enabled' : 'Disabled');
            this.$('.audit-status').removeClass('enabled disabled');
            this.$('.audit-status').addClass(data.audit_enabled ? 'enabled' : 'disabled');
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-scan-security').on('click', function () {
                self._scan_security();
            });
            this.$('.btn-update-security').on('click', function () {
                self._update_security_settings();
            });
        },
        
        _scan_security: function () {
            var self = this;
            rpc.query({
                model: 'database.security',
                method: 'scan_security',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._load_security_data();
                    self._show_notification(_t('Security scan completed'), 'success');
                } else {
                    self._show_notification(_t('Security scan failed'), 'danger');
                }
            });
        },
        
        _update_security_settings: function () {
            var self = this;
            rpc.query({
                model: 'database.security',
                method: 'update_security_settings',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._load_security_data();
                    self._show_notification(_t('Security settings updated'), 'success');
                } else {
                    self._show_notification(_t('Failed to update security settings'), 'danger');
                }
            });
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Security'), message, type);
        }
    });

    // Database Maintenance Widget
    var DatabaseMaintenanceWidget = AbstractAction.extend({
        template: 'database.maintenance_widget',
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.database_id = action.context.database_id;
            this.maintenance_data = {};
        },
        
        start: function () {
            this._super.apply(this, arguments);
            this._load_maintenance_data();
            this._bind_events();
        },
        
        _load_maintenance_data: function () {
            var self = this;
            rpc.query({
                model: 'database.maintenance',
                method: 'get_maintenance_data',
                args: [this.database_id]
            }).then(function (result) {
                self.maintenance_data = result;
                self._update_maintenance_display();
            });
        },
        
        _update_maintenance_display: function () {
            var data = this.maintenance_data;
            
            // Update maintenance status
            this.$('.maintenance-status').text(data.status);
            this.$('.maintenance-status').removeClass('active inactive scheduled running completed failed');
            this.$('.maintenance-status').addClass(data.status);
            
            // Update maintenance progress
            this.$('.maintenance-progress-bar').css('width', data.progress + '%');
            
            // Update maintenance logs
            this.$('.maintenance-logs').html(data.logs);
        },
        
        _bind_events: function () {
            var self = this;
            this.$('.btn-start-maintenance').on('click', function () {
                self._start_maintenance();
            });
            this.$('.btn-stop-maintenance').on('click', function () {
                self._stop_maintenance();
            });
            this.$('.btn-schedule-maintenance').on('click', function () {
                self._schedule_maintenance();
            });
        },
        
        _start_maintenance: function () {
            var self = this;
            rpc.query({
                model: 'database.maintenance',
                method: 'start_maintenance',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._load_maintenance_data();
                    self._show_notification(_t('Maintenance started'), 'success');
                } else {
                    self._show_notification(_t('Failed to start maintenance'), 'danger');
                }
            });
        },
        
        _stop_maintenance: function () {
            var self = this;
            rpc.query({
                model: 'database.maintenance',
                method: 'stop_maintenance',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._load_maintenance_data();
                    self._show_notification(_t('Maintenance stopped'), 'warning');
                } else {
                    self._show_notification(_t('Failed to stop maintenance'), 'danger');
                }
            });
        },
        
        _schedule_maintenance: function () {
            var self = this;
            Dialog.confirm(this, _t('Are you sure you want to schedule maintenance?'), {
                title: _t('Confirm Schedule'),
                confirm_callback: function () {
                    self._perform_schedule();
                }
            });
        },
        
        _perform_schedule: function () {
            var self = this;
            rpc.query({
                model: 'database.maintenance',
                method: 'schedule_maintenance',
                args: [this.database_id]
            }).then(function (result) {
                if (result.success) {
                    self._load_maintenance_data();
                    self._show_notification(_t('Maintenance scheduled'), 'success');
                } else {
                    self._show_notification(_t('Failed to schedule maintenance'), 'danger');
                }
            });
        },
        
        _show_notification: function (message, type) {
            this.do_notify(_t('Database Maintenance'), message, type);
        }
    });

    // Register widgets
    core.action_registry.add('database_connection_widget', DatabaseConnectionWidget);
    core.action_registry.add('database_backup_widget', DatabaseBackupWidget);
    core.action_registry.add('database_monitoring_widget', DatabaseMonitoringWidget);
    core.action_registry.add('database_analytics_widget', DatabaseAnalyticsWidget);
    core.action_registry.add('database_security_widget', DatabaseSecurityWidget);
    core.action_registry.add('database_maintenance_widget', DatabaseMaintenanceWidget);

    return {
        DatabaseConnectionWidget: DatabaseConnectionWidget,
        DatabaseBackupWidget: DatabaseBackupWidget,
        DatabaseMonitoringWidget: DatabaseMonitoringWidget,
        DatabaseAnalyticsWidget: DatabaseAnalyticsWidget,
        DatabaseSecurityWidget: DatabaseSecurityWidget,
        DatabaseMaintenanceWidget: DatabaseMaintenanceWidget
    };
});