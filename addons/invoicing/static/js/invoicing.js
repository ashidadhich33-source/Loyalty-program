/* Invoicing Addon JavaScript */

odoo.define('invoicing.invoice', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var ListView = require('web.ListView');

    // Invoice Form View Enhancements
    FormView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'account.invoice') {
                this._initInvoiceForm();
            }
        },
        
        _initInvoiceForm: function () {
            // Add invoice-specific functionality
            console.log('Invoice form initialized');
        }
    });

    // Invoice List View Enhancements
    ListView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.modelName === 'account.invoice') {
                this._initInvoiceList();
            }
        },
        
        _initInvoiceList: function () {
            // Add invoice-specific functionality
            console.log('Invoice list initialized');
        }
    });

});