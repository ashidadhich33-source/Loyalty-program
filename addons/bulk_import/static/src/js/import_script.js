/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class ImportTemplateWidget extends Component {
    static template = "bulk_import.ImportTemplateWidget";
    
    setup() {
        super.setup();
    }
    
    get templateType() {
        const types = {
            'excel': 'Excel',
            'csv': 'CSV',
            'json': 'JSON',
            'xml': 'XML'
        };
        return types[this.props.record.data.template_type] || 'Unknown';
    }
    
    get isKidsSpecific() {
        return this.props.record.data.is_kids_specific;
    }
    
    get validationFlags() {
        const flags = [];
        if (this.props.record.data.age_group_validation) flags.push('Age Group');
        if (this.props.record.data.gender_validation) flags.push('Gender');
        if (this.props.record.data.size_validation) flags.push('Size');
        if (this.props.record.data.gstin_validation) flags.push('GSTIN');
        if (this.props.record.data.pan_validation) flags.push('PAN');
        if (this.props.record.data.mobile_validation) flags.push('Mobile');
        return flags;
    }
    
    get usageStats() {
        return {
            count: this.props.record.data.usage_count || 0,
            lastUsed: this.props.record.data.last_used || 'Never'
        };
    }
}

registry.category("view_widgets").add("import_template_widget", ImportTemplateWidget);

// Import Job Widget
export class ImportJobWidget extends Component {
    static template = "bulk_import.ImportJobWidget";
    
    setup() {
        super.setup();
    }
    
    get jobStatus() {
        const statuses = {
            'draft': 'Draft',
            'validating': 'Validating',
            'validated': 'Validated',
            'importing': 'Importing',
            'completed': 'Completed',
            'failed': 'Failed',
            'cancelled': 'Cancelled'
        };
        return statuses[this.props.record.data.state] || 'Unknown';
    }
    
    get progressInfo() {
        return {
            total: this.props.record.data.total_rows || 0,
            processed: this.props.record.data.processed_rows || 0,
            success: this.props.record.data.success_rows || 0,
            error: this.props.record.data.error_rows || 0,
            percentage: this.props.record.data.progress_percentage || 0
        };
    }
    
    get fileInfo() {
        return {
            name: this.props.record.data.import_filename || 'Unknown',
            size: this.props.record.data.file_size || 0,
            sizeFormatted: this.formatFileSize(this.props.record.data.file_size || 0)
        };
    }
    
    get timingInfo() {
        return {
            start: this.props.record.data.start_time,
            end: this.props.record.data.end_time,
            duration: this.props.record.data.duration || 0,
            durationFormatted: this.formatDuration(this.props.record.data.duration || 0)
        };
    }
    
    formatFileSize(sizeKB) {
        if (sizeKB < 1024) {
            return `${sizeKB.toFixed(1)} KB`;
        } else if (sizeKB < 1024 * 1024) {
            return `${(sizeKB / 1024).toFixed(1)} MB`;
        } else {
            return `${(sizeKB / (1024 * 1024)).toFixed(1)} GB`;
        }
    }
    
    formatDuration(seconds) {
        if (seconds < 60) {
            return `${seconds.toFixed(1)}s`;
        } else if (seconds < 3600) {
            return `${(seconds / 60).toFixed(1)}m`;
        } else {
            return `${(seconds / 3600).toFixed(1)}h`;
        }
    }
}

registry.category("view_widgets").add("import_job_widget", ImportJobWidget);

// Import Mapping Widget
export class ImportMappingWidget extends Component {
    static template = "bulk_import.ImportMappingWidget";
    
    setup() {
        super.setup();
    }
    
    get dataType() {
        const types = {
            'char': 'Text',
            'text': 'Long Text',
            'integer': 'Integer',
            'float': 'Float',
            'boolean': 'Boolean',
            'date': 'Date',
            'datetime': 'DateTime',
            'selection': 'Selection',
            'many2one': 'Many2one',
            'many2many': 'Many2many',
            'one2many': 'One2many'
        };
        return types[this.props.record.data.data_type] || 'Unknown';
    }
    
    get transformationRule() {
        const rules = {
            'none': 'No Transformation',
            'uppercase': 'Uppercase',
            'lowercase': 'Lowercase',
            'title': 'Title Case',
            'trim': 'Trim Whitespace',
            'replace': 'Replace Text',
            'split': 'Split Text',
            'join': 'Join Text',
            'format': 'Format Text',
            'validate': 'Validate Format'
        };
        return rules[this.props.record.data.transformation_rule] || 'None';
    }
    
    get validationRule() {
        const rules = {
            'none': 'No Validation',
            'email': 'Email Format',
            'phone': 'Phone Number',
            'url': 'URL Format',
            'numeric': 'Numeric Only',
            'alpha': 'Alphabetic Only',
            'alphanumeric': 'Alphanumeric Only',
            'length': 'Length Check',
            'range': 'Range Check',
            'pattern': 'Pattern Match',
            'custom': 'Custom Validation'
        };
        return rules[this.props.record.data.validation_rule] || 'None';
    }
    
    get isKidsSpecific() {
        return this.props.record.data.is_kids_specific;
    }
    
    get validationFlags() {
        const flags = [];
        if (this.props.record.data.age_group_validation) flags.push('Age Group');
        if (this.props.record.data.gender_validation) flags.push('Gender');
        if (this.props.record.data.size_validation) flags.push('Size');
        if (this.props.record.data.gstin_validation) flags.push('GSTIN');
        if (this.props.record.data.pan_validation) flags.push('PAN');
        if (this.props.record.data.mobile_validation) flags.push('Mobile');
        return flags;
    }
    
    get usageStats() {
        return {
            total: this.props.record.data.usage_count || 0,
            success: this.props.record.data.success_count || 0,
            error: this.props.record.data.error_count || 0,
            successRate: this.calculateSuccessRate()
        };
    }
    
    calculateSuccessRate() {
        const total = this.props.record.data.usage_count || 0;
        const success = this.props.record.data.success_count || 0;
        if (total === 0) return 0;
        return ((success / total) * 100).toFixed(1);
    }
}

registry.category("view_widgets").add("import_mapping_widget", ImportMappingWidget);

// Import History Widget
export class ImportHistoryWidget extends Component {
    static template = "bulk_import.ImportHistoryWidget";
    
    setup() {
        super.setup();
    }
    
    get importStatus() {
        const statuses = {
            'completed': 'Completed',
            'failed': 'Failed',
            'cancelled': 'Cancelled',
            'partial': 'Partial Success'
        };
        return statuses[this.props.record.data.status] || 'Unknown';
    }
    
    get recordStats() {
        return {
            total: this.props.record.data.total_records || 0,
            success: this.props.record.data.success_records || 0,
            error: this.props.record.data.error_records || 0,
            warning: this.props.record.data.warning_records || 0
        };
    }
    
    get performanceStats() {
        return {
            duration: this.props.record.data.duration || 0,
            recordsPerSecond: this.props.record.data.records_per_second || 0,
            durationFormatted: this.formatDuration(this.props.record.data.duration || 0)
        };
    }
    
    get dataQualityStats() {
        return {
            overall: this.props.record.data.data_quality_score || 0,
            completeness: this.props.record.data.completeness_score || 0,
            accuracy: this.props.record.data.accuracy_score || 0,
            consistency: this.props.record.data.consistency_score || 0
        };
    }
    
    get businessImpact() {
        const impacts = {
            'low': 'Low Impact',
            'medium': 'Medium Impact',
            'high': 'High Impact',
            'critical': 'Critical Impact'
        };
        return impacts[this.props.record.data.business_impact] || 'Unknown';
    }
    
    get costSavings() {
        return {
            cost: this.props.record.data.cost_savings || 0,
            time: this.props.record.data.time_savings || 0,
            costFormatted: this.formatCurrency(this.props.record.data.cost_savings || 0),
            timeFormatted: this.formatTime(this.props.record.data.time_savings || 0)
        };
    }
    
    formatDuration(seconds) {
        if (seconds < 60) {
            return `${seconds.toFixed(1)}s`;
        } else if (seconds < 3600) {
            return `${(seconds / 60).toFixed(1)}m`;
        } else {
            return `${(seconds / 3600).toFixed(1)}h`;
        }
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    formatTime(hours) {
        if (hours < 1) {
            return `${(hours * 60).toFixed(0)}m`;
        } else if (hours < 24) {
            return `${hours.toFixed(1)}h`;
        } else {
            return `${(hours / 24).toFixed(1)}d`;
        }
    }
}

registry.category("view_widgets").add("import_history_widget", ImportHistoryWidget);

// Import Statistics Widget
export class ImportStatisticsWidget extends Component {
    static template = "bulk_import.ImportStatisticsWidget";
    
    setup() {
        super.setup();
    }
    
    get period() {
        const periods = {
            'daily': 'Daily',
            'weekly': 'Weekly',
            'monthly': 'Monthly',
            'quarterly': 'Quarterly',
            'yearly': 'Yearly'
        };
        return periods[this.props.record.data.period] || 'Unknown';
    }
    
    get importStats() {
        return {
            total: this.props.record.data.total_imports || 0,
            successful: this.props.record.data.successful_imports || 0,
            failed: this.props.record.data.failed_imports || 0,
            cancelled: this.props.record.data.cancelled_imports || 0
        };
    }
    
    get recordStats() {
        return {
            total: this.props.record.data.total_records || 0,
            successful: this.props.record.data.successful_records || 0,
            error: this.props.record.data.error_records || 0,
            warning: this.props.record.data.warning_records || 0
        };
    }
    
    get performanceStats() {
        return {
            avgDuration: this.props.record.data.avg_duration || 0,
            minDuration: this.props.record.data.min_duration || 0,
            maxDuration: this.props.record.data.max_duration || 0,
            avgRecordsPerSecond: this.props.record.data.avg_records_per_second || 0
        };
    }
    
    get fileStats() {
        return {
            totalSize: this.props.record.data.total_file_size || 0,
            avgSize: this.props.record.data.avg_file_size || 0,
            totalSizeFormatted: this.formatFileSize(this.props.record.data.total_file_size || 0),
            avgSizeFormatted: this.formatFileSize(this.props.record.data.avg_file_size || 0)
        };
    }
    
    get dataQualityStats() {
        return {
            overall: this.props.record.data.data_quality_score || 0,
            completeness: this.props.record.data.completeness_score || 0,
            accuracy: this.props.record.data.accuracy_score || 0,
            consistency: this.props.record.data.consistency_score || 0
        };
    }
    
    get businessImpact() {
        return {
            costSavings: this.props.record.data.cost_savings || 0,
            timeSavings: this.props.record.data.time_savings || 0,
            efficiencyImprovement: this.props.record.data.efficiency_improvement || 0,
            costFormatted: this.formatCurrency(this.props.record.data.cost_savings || 0),
            timeFormatted: this.formatTime(this.props.record.data.time_savings || 0)
        };
    }
    
    get trends() {
        return {
            importTrend: this.props.record.data.import_trend || 'stable',
            successRateTrend: this.props.record.data.success_rate_trend || 'stable'
        };
    }
    
    formatFileSize(sizeMB) {
        if (sizeMB < 1024) {
            return `${sizeMB.toFixed(1)} MB`;
        } else {
            return `${(sizeMB / 1024).toFixed(1)} GB`;
        }
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    formatTime(hours) {
        if (hours < 1) {
            return `${(hours * 60).toFixed(0)}m`;
        } else if (hours < 24) {
            return `${hours.toFixed(1)}h`;
        } else {
            return `${(hours / 24).toFixed(1)}d`;
        }
    }
}

registry.category("view_widgets").add("import_statistics_widget", ImportStatisticsWidget);