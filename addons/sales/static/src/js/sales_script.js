/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onMounted } from "@odoo/owl";

// Sales Order Scripts
export class SalesOrderScript extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: false,
            error: null,
        });
    }

    async onMounted() {
        // Initialize sales order functionality
        this.initializeSalesOrder();
    }

    async initializeSalesOrder() {
        try {
            this.state.loading = true;
            // Initialize sales order specific functionality
            console.log("Sales Order initialized");
        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async calculateOrderTotal() {
        // Calculate order total with kids clothing specific logic
        const orderLines = this.props.orderLines || [];
        let total = 0;
        
        for (const line of orderLines) {
            if (line.product_id && line.product_id.age_group !== 'all') {
                // Kids clothing specific pricing
                total += line.price_total;
            }
        }
        
        return total;
    }

    async validateKidsClothingOrder() {
        // Validate kids clothing specific requirements
        const order = this.props.order;
        const errors = [];
        
        if (order.age_group && order.age_group !== 'all') {
            // Validate age group requirements
            if (!order.child_profile_id) {
                errors.push("Child profile is required for age-specific orders");
            }
        }
        
        if (order.gender && order.gender !== 'unisex') {
            // Validate gender requirements
            if (!order.child_profile_id) {
                errors.push("Child profile is required for gender-specific orders");
            }
        }
        
        return errors;
    }
}

// Sales Quotation Scripts
export class SalesQuotationScript extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: false,
            error: null,
        });
    }

    async onMounted() {
        // Initialize sales quotation functionality
        this.initializeSalesQuotation();
    }

    async initializeSalesQuotation() {
        try {
            this.state.loading = true;
            // Initialize sales quotation specific functionality
            console.log("Sales Quotation initialized");
        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async convertQuotationToOrder() {
        // Convert quotation to order with kids clothing specific logic
        const quotation = this.props.quotation;
        
        if (quotation.state !== 'accepted') {
            throw new Error('Only accepted quotations can be converted to orders');
        }
        
        // Create sales order with kids clothing specific fields
        const orderData = {
            partner_id: quotation.partner_id.id,
            child_profile_id: quotation.child_profile_id?.id,
            age_group: quotation.age_group,
            gender: quotation.gender,
            season: quotation.season,
            team_id: quotation.team_id?.id,
            user_id: quotation.user_id?.id,
            territory_id: quotation.territory_id?.id,
            commission_id: quotation.commission_id?.id,
        };
        
        return await this.orm.create('sale.order', orderData);
    }
}

// Sales Delivery Scripts
export class SalesDeliveryScript extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: false,
            error: null,
        });
    }

    async onMounted() {
        // Initialize sales delivery functionality
        this.initializeSalesDelivery();
    }

    async initializeSalesDelivery() {
        try {
            this.state.loading = true;
            // Initialize sales delivery specific functionality
            console.log("Sales Delivery initialized");
        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async trackDelivery() {
        // Track delivery with kids clothing specific logic
        const delivery = this.props.delivery;
        
        if (delivery.tracking_number) {
            // Update delivery status
            await this.orm.write('sale.delivery', [delivery.id], {
                state: 'in_transit',
            });
        }
    }

    async confirmDelivery() {
        // Confirm delivery with kids clothing specific logic
        const delivery = this.props.delivery;
        
        await this.orm.write('sale.delivery', [delivery.id], {
            state: 'delivered',
            delivery_confirmed: true,
        });
    }
}

// Sales Return Scripts
export class SalesReturnScript extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: false,
            error: null,
        });
    }

    async onMounted() {
        // Initialize sales return functionality
        this.initializeSalesReturn();
    }

    async initializeSalesReturn() {
        try {
            this.state.loading = true;
            // Initialize sales return specific functionality
            console.log("Sales Return initialized");
        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async processReturn() {
        // Process return with kids clothing specific logic
        const returnOrder = this.props.returnOrder;
        
        if (returnOrder.return_type === 'exchange') {
            // Create exchange order
            const exchangeOrder = await this.createExchangeOrder(returnOrder);
            await this.orm.write('sale.return', [returnOrder.id], {
                exchange_order_id: exchangeOrder.id,
                state: 'exchanged',
            });
        } else if (returnOrder.return_type === 'refund') {
            // Process refund
            await this.orm.write('sale.return', [returnOrder.id], {
                state: 'refunded',
            });
        }
    }

    async createExchangeOrder(returnOrder) {
        // Create exchange order with kids clothing specific logic
        const orderData = {
            partner_id: returnOrder.partner_id.id,
            child_profile_id: returnOrder.child_profile_id?.id,
            age_group: returnOrder.age_group,
            gender: returnOrder.gender,
            season: returnOrder.season,
            team_id: returnOrder.team_id?.id,
            user_id: returnOrder.user_id?.id,
            territory_id: returnOrder.territory_id?.id,
            commission_id: returnOrder.commission_id?.id,
        };
        
        return await this.orm.create('sale.order', orderData);
    }
}

// Sales Analytics Scripts
export class SalesAnalyticsScript extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: false,
            error: null,
            analytics: null,
        });
    }

    async onMounted() {
        // Initialize sales analytics functionality
        this.initializeSalesAnalytics();
    }

    async initializeSalesAnalytics() {
        try {
            this.state.loading = true;
            // Initialize sales analytics specific functionality
            console.log("Sales Analytics initialized");
        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async generateKidsClothingAnalytics() {
        // Generate kids clothing specific analytics
        const analytics = await this.orm.call('sale.analytics', 'generate_kids_analytics', []);
        this.state.analytics = analytics;
        return analytics;
    }

    async getAgeGroupSales() {
        // Get sales by age group
        const ageGroupSales = await this.orm.call('sale.analytics', 'get_age_group_sales', []);
        return ageGroupSales;
    }

    async getGenderSales() {
        // Get sales by gender
        const genderSales = await this.orm.call('sale.analytics', 'get_gender_sales', []);
        return genderSales;
    }

    async getSeasonSales() {
        // Get sales by season
        const seasonSales = await this.orm.call('sale.analytics', 'get_season_sales', []);
        return seasonSales;
    }
}

// Register components
registry.category("components").add("SalesOrderScript", SalesOrderScript);
registry.category("components").add("SalesQuotationScript", SalesQuotationScript);
registry.category("components").add("SalesDeliveryScript", SalesDeliveryScript);
registry.category("components").add("SalesReturnScript", SalesReturnScript);
registry.category("components").add("SalesAnalyticsScript", SalesAnalyticsScript);