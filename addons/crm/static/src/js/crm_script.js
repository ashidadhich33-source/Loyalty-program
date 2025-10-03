// CRM Script for Ocean ERP
ocean.define('crm.CrmController', function (require) {
    'use strict';
    
    var core = require('ocean.core');
    var FormController = require('ocean.FormController');
    var ListController = require('ocean.ListController');
    var AbstractController = require('ocean.AbstractController');
    var Dialog = require('ocean.Dialog');
    var rpc = require('ocean.rpc');
    
    // CRM Lead Controller
    var CrmLeadController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_crm_lead_convert': '_onConvertLead',
            'click .o_crm_lead_schedule_activity': '_onScheduleActivity',
            'click .o_crm_lead_send_communication': '_onSendCommunication',
        }),
        
        _onConvertLead: function (event) {
            event.preventDefault();
            var self = this;
            var leadId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to convert this lead?', {
                title: 'Convert Lead',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.lead',
                        method: 'action_convert_to_customer',
                        args: [leadId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onScheduleActivity: function (event) {
            event.preventDefault();
            var self = this;
            var leadId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to schedule an activity for this lead?', {
                title: 'Schedule Activity',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.lead',
                        method: 'action_schedule_activity',
                        args: [leadId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onSendCommunication: function (event) {
            event.preventDefault();
            var self = this;
            var leadId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to send a communication to this lead?', {
                title: 'Send Communication',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.lead',
                        method: 'action_send_communication',
                        args: [leadId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // CRM Opportunity Controller
    var CrmOpportunityController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_crm_opportunity_convert': '_onConvertOpportunity',
            'click .o_crm_opportunity_schedule_activity': '_onScheduleActivity',
            'click .o_crm_opportunity_send_communication': '_onSendCommunication',
        }),
        
        _onConvertOpportunity: function (event) {
            event.preventDefault();
            var self = this;
            var opportunityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to convert this opportunity to a sale?', {
                title: 'Convert Opportunity',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.opportunity',
                        method: 'action_convert_to_sale',
                        args: [opportunityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onScheduleActivity: function (event) {
            event.preventDefault();
            var self = this;
            var opportunityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to schedule an activity for this opportunity?', {
                title: 'Schedule Activity',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.opportunity',
                        method: 'action_schedule_activity',
                        args: [opportunityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onSendCommunication: function (event) {
            event.preventDefault();
            var self = this;
            var opportunityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Do you want to send a communication to this opportunity?', {
                title: 'Send Communication',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.opportunity',
                        method: 'action_send_communication',
                        args: [opportunityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // CRM Activity Controller
    var CrmActivityController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_crm_activity_mark_done': '_onMarkDone',
            'click .o_crm_activity_mark_in_progress': '_onMarkInProgress',
            'click .o_crm_activity_cancel': '_onCancel',
        }),
        
        _onMarkDone: function (event) {
            event.preventDefault();
            var self = this;
            var activityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to mark this activity as done?', {
                title: 'Mark Activity Done',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.activity',
                        method: 'action_mark_done',
                        args: [activityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onMarkInProgress: function (event) {
            event.preventDefault();
            var self = this;
            var activityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to mark this activity as in progress?', {
                title: 'Mark Activity In Progress',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.activity',
                        method: 'action_mark_in_progress',
                        args: [activityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onCancel: function (event) {
            event.preventDefault();
            var self = this;
            var activityId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to cancel this activity?', {
                title: 'Cancel Activity',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.activity',
                        method: 'action_cancel',
                        args: [activityId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // CRM Communication Controller
    var CrmCommunicationController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_crm_communication_send': '_onSend',
            'click .o_crm_communication_resend': '_onResend',
            'click .o_crm_communication_cancel': '_onCancel',
        }),
        
        _onSend: function (event) {
            event.preventDefault();
            var self = this;
            var communicationId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to send this communication?', {
                title: 'Send Communication',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.communication',
                        method: 'action_send',
                        args: [communicationId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onResend: function (event) {
            event.preventDefault();
            var self = this;
            var communicationId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to resend this communication?', {
                title: 'Resend Communication',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.communication',
                        method: 'action_resend',
                        args: [communicationId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onCancel: function (event) {
            event.preventDefault();
            var self = this;
            var communicationId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to cancel this communication?', {
                title: 'Cancel Communication',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.communication',
                        method: 'action_cancel',
                        args: [communicationId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    // CRM Campaign Controller
    var CrmCampaignController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            'click .o_crm_campaign_activate': '_onActivate',
            'click .o_crm_campaign_pause': '_onPause',
            'click .o_crm_campaign_cancel': '_onCancel',
        }),
        
        _onActivate: function (event) {
            event.preventDefault();
            var self = this;
            var campaignId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to activate this campaign?', {
                title: 'Activate Campaign',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.campaign',
                        method: 'action_activate',
                        args: [campaignId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onPause: function (event) {
            event.preventDefault();
            var self = this;
            var campaignId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to pause this campaign?', {
                title: 'Pause Campaign',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.campaign',
                        method: 'action_pause',
                        args: [campaignId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
        
        _onCancel: function (event) {
            event.preventDefault();
            var self = this;
            var campaignId = this.getSelectedIds()[0];
            
            Dialog.confirm(this, 'Are you sure you want to cancel this campaign?', {
                title: 'Cancel Campaign',
                confirm_callback: function () {
                    rpc.query({
                        model: 'crm.campaign',
                        method: 'action_cancel',
                        args: [campaignId],
                    }).then(function (result) {
                        if (result) {
                            self.reload();
                        }
                    });
                }
            });
        },
    });
    
    return {
        CrmLeadController: CrmLeadController,
        CrmOpportunityController: CrmOpportunityController,
        CrmActivityController: CrmActivityController,
        CrmCommunicationController: CrmCommunicationController,
        CrmCampaignController: CrmCampaignController,
    };
});