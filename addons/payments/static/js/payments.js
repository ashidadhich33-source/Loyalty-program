/* Payments Addon JavaScript */

odoo.define('payments.payment', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var ListView = require('web.ListView');

    // Payment Form View Enhancements
    FormView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'account.payment') {
                this._initPaymentForm();
            }
        },
        
        _initPaymentForm: function () {
            // Add payment-specific functionality
            console.log('Payment form initialized');
        }
    });

    // Payment List View Enhancements
    ListView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'account.payment') {
                this._initPaymentList();
            }
        },
        
        _initPaymentList: function () {
            // Add payment-specific functionality
            console.log('Payment list initialized');
        }
    });

});