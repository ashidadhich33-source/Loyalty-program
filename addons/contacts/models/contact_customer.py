# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactCustomer(models.Model):
    _name = 'contact.customer'
    _description = 'Customer Contact'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True)
    customer_code = fields.Char(string='Customer Code', readonly=True, copy=False)
    customer_type = fields.Selection([
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
    ], string='Customer Type', default='individual')
    
    loyalty_points = fields.Integer(string='Loyalty Points', default=0)
    loyalty_level = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Loyalty Level', compute='_compute_loyalty_level')
    
    credit_limit = fields.Float(string='Credit Limit')
    credit_balance = fields.Float(string='Credit Balance', compute='_compute_credit_balance')
    payment_terms = fields.Many2one('account.payment.term', string='Payment Terms')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ], string='Status', default='active')
    
    @api.model
    def create(self, vals):
        if not vals.get('customer_code'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('contact.customer') or '/'
        return super().create(vals)
    
    @api.depends('loyalty_points')
    def _compute_loyalty_level(self):
        for record in self:
            if record.loyalty_points >= 10000:
                record.loyalty_level = 'platinum'
            elif record.loyalty_points >= 5000:
                record.loyalty_level = 'gold'
            elif record.loyalty_points >= 2000:
                record.loyalty_level = 'silver'
            else:
                record.loyalty_level = 'bronze'
    
    def _compute_credit_balance(self):
        for record in self:
            record.credit_balance = 0.0  # TODO: Implement credit balance calculation
