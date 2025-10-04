/* HR Addon JavaScript */

odoo.define('hr.employee', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var ListView = require('web.ListView');

    // Employee Form View Enhancements
    FormView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'hr.employee') {
                this._initEmployeeForm();
            }
        },
        
        _initEmployeeForm: function () {
            // Add employee-specific functionality
            console.log('Employee form initialized');
        }
    });

    // Employee List View Enhancements
    ListView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'hr.employee') {
                this._initEmployeeList();
            }
        },
        
        _initEmployeeList: function () {
            // Add employee-specific functionality
            console.log('Employee list initialized');
        }
    });

});