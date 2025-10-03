/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class CategoryScript extends Component {
    static template = "categories.CategoryScript";
    
    setup() {
        super.setup();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Add any JavaScript functionality here
        console.log("Category script loaded");
    }
}

registry.category("web").add("category_script", CategoryScript);