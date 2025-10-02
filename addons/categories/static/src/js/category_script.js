/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class CategoryWidget extends Component {
    static template = "categories.CategoryWidget";
    
    setup() {
        super.setup();
    }
    
    get categoryColor() {
        return this.props.record.data.color || '#007bff';
    }
    
    get categoryIcon() {
        return this.props.record.data.icon || 'fa fa-tag';
    }
    
    get categoryStats() {
        return {
            products: this.props.record.data.product_count || 0,
            sales: this.props.record.data.total_sales || 0,
            rating: this.props.record.data.avg_rating || 0
        };
    }
}

registry.category("view_widgets").add("category_widget", CategoryWidget);

// Category Analytics Widget
export class CategoryAnalyticsWidget extends Component {
    static template = "categories.CategoryAnalyticsWidget";
    
    setup() {
        super.setup();
    }
    
    get analyticsData() {
        return {
            totalSales: this.props.record.data.total_sales || 0,
            salesCount: this.props.record.data.sales_count || 0,
            avgOrderValue: this.props.record.data.avg_order_value || 0,
            productCount: this.props.record.data.product_count || 0,
            customerCount: this.props.record.data.customer_count || 0,
            revenue: this.props.record.data.revenue || 0,
            profit: this.props.record.data.profit || 0,
            profitMargin: this.props.record.data.profit_margin || 0
        };
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    formatPercentage(value) {
        return `${value.toFixed(2)}%`;
    }
}

registry.category("view_widgets").add("category_analytics_widget", CategoryAnalyticsWidget);

// Category Rule Widget
export class CategoryRuleWidget extends Component {
    static template = "categories.CategoryRuleWidget";
    
    setup() {
        super.setup();
    }
    
    get ruleStatus() {
        return this.props.record.data.is_active ? 'Active' : 'Inactive';
    }
    
    get rulePriority() {
        const priorities = {
            '1': 'Very High',
            '2': 'High',
            '3': 'Medium',
            '4': 'Low',
            '5': 'Very Low'
        };
        return priorities[this.props.record.data.priority] || 'Medium';
    }
    
    get executionStats() {
        return {
            total: this.props.record.data.execution_count || 0,
            success: this.props.record.data.success_count || 0,
            failure: this.props.record.data.failure_count || 0
        };
    }
    
    get successRate() {
        const stats = this.executionStats;
        if (stats.total === 0) return 0;
        return (stats.success / stats.total) * 100;
    }
}

registry.category("view_widgets").add("category_rule_widget", CategoryRuleWidget);

// Category Attribute Widget
export class CategoryAttributeWidget extends Component {
    static template = "categories.CategoryAttributeWidget";
    
    setup() {
        super.setup();
    }
    
    get attributeType() {
        const types = {
            'text': 'Text',
            'number': 'Number',
            'boolean': 'Boolean',
            'selection': 'Selection',
            'date': 'Date',
            'datetime': 'DateTime',
            'float': 'Float',
            'integer': 'Integer'
        };
        return types[this.props.record.data.attribute_type] || 'Text';
    }
    
    get displayType() {
        const types = {
            'text': 'Text',
            'radio': 'Radio Buttons',
            'checkbox': 'Checkboxes',
            'select': 'Dropdown',
            'multiselect': 'Multi-select'
        };
        return types[this.props.record.data.display_type] || 'Text';
    }
    
    get isKidsSpecific() {
        return this.props.record.data.is_kids_specific;
    }
    
    get ageGroupFilter() {
        const ageGroups = {
            '0-2': '0-2 Years (Baby)',
            '2-4': '2-4 Years (Toddler)',
            '4-6': '4-6 Years (Pre-school)',
            '6-8': '6-8 Years (Early School)',
            '8-10': '8-10 Years (Middle School)',
            '10-12': '10-12 Years (Pre-teen)',
            '12-14': '12-14 Years (Teen)',
            '14-16': '14-16 Years (Young Adult)',
            'all': 'All Ages'
        };
        return ageGroups[this.props.record.data.age_group_filter] || 'All Ages';
    }
    
    get genderFilter() {
        const genders = {
            'boys': 'Boys',
            'girls': 'Girls',
            'unisex': 'Unisex'
        };
        return genders[this.props.record.data.gender_filter] || 'Unisex';
    }
}

registry.category("view_widgets").add("category_attribute_widget", CategoryAttributeWidget);