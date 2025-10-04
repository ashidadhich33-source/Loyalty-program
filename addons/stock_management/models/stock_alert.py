# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class StockAlert(models.Model):
    _name = 'stock.alert'
    _description = 'Stock Alert'
    _order = 'priority desc, create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Alert Name',
        required=True,
        help='Name of the stock alert'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help='Product for which the alert is generated'
    )
    
    product_template_id = fields.Many2one(
        'product.template',
        related='product_id.product_tmpl_id',
        string='Product Template',
        store=True,
        help='Product template'
    )
    
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse where the alert is generated'
    )
    
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        help='Specific location within the warehouse'
    )
    
    current_stock = fields.Float(
        string='Current Stock',
        digits='Product Unit of Measure',
        help='Current stock quantity'
    )
    
    minimum_stock = fields.Float(
        string='Minimum Stock',
        digits='Product Unit of Measure',
        help='Minimum stock threshold'
    )
    
    maximum_stock = fields.Float(
        string='Maximum Stock',
        digits='Product Unit of Measure',
        help='Maximum stock threshold'
    )
    
    alert_type = fields.Selection([
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('overstock', 'Overstock'),
        ('expiry_warning', 'Expiry Warning'),
        ('seasonal_alert', 'Seasonal Alert'),
        ('size_alert', 'Size Alert'),
        ('brand_alert', 'Brand Alert'),
        ('color_alert', 'Color Alert'),
    ], string='Alert Type', required=True, help='Type of stock alert')
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Priority', default='medium', required=True, help='Priority level of the alert')
    
    status = fields.Selection([
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='active', required=True, help='Status of the alert')
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
    ], string='Age Group', help='Age group for the product')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ], string='Size', help='Size of the product')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the product')
    
    brand = fields.Char(
        string='Brand',
        help='Brand of the product'
    )
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    # Alert Details
    alert_message = fields.Text(
        string='Alert Message',
        help='Detailed message about the alert'
    )
    
    recommended_action = fields.Selection([
        ('reorder', 'Reorder'),
        ('promote', 'Promote'),
        ('discount', 'Discount'),
        ('clearance', 'Clearance'),
        ('transfer', 'Transfer'),
        ('adjust', 'Adjust'),
        ('return', 'Return'),
        ('dispose', 'Dispose'),
    ], string='Recommended Action', help='Recommended action to resolve the alert')
    
    action_notes = fields.Text(
        string='Action Notes',
        help='Notes about the recommended action'
    )
    
    # Notification Fields
    notify_users = fields.Many2many(
        'res.users',
        'stock_alert_user_rel',
        'alert_id',
        'user_id',
        string='Notify Users',
        help='Users to notify about this alert'
    )
    
    email_sent = fields.Boolean(
        string='Email Sent',
        default=False,
        help='Whether email notification has been sent'
    )
    
    sms_sent = fields.Boolean(
        string='SMS Sent',
        default=False,
        help='Whether SMS notification has been sent'
    )
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the alert was created'
    )
    
    acknowledge_date = fields.Datetime(
        string='Acknowledged On',
        readonly=True,
        help='Date when the alert was acknowledged'
    )
    
    resolve_date = fields.Datetime(
        string='Resolved On',
        readonly=True,
        help='Date when the alert was resolved'
    )
    
    acknowledged_by = fields.Many2one(
        'res.users',
        string='Acknowledged By',
        readonly=True,
        help='User who acknowledged the alert'
    )
    
    resolved_by = fields.Many2one(
        'res.users',
        string='Resolved By',
        readonly=True,
        help='User who resolved the alert'
    )
    
    # Computed Fields
    days_since_created = fields.Integer(
        string='Days Since Created',
        compute='_compute_days_since_created',
        help='Number of days since the alert was created'
    )
    
    stock_variance = fields.Float(
        string='Stock Variance',
        compute='_compute_stock_variance',
        help='Difference between current and minimum stock'
    )
    
    @api.depends('create_date')
    def _compute_days_since_created(self):
        for record in self:
            if record.create_date:
                delta = fields.Datetime.now() - record.create_date
                record.days_since_created = delta.days
            else:
                record.days_since_created = 0
    
    @api.depends('current_stock', 'minimum_stock')
    def _compute_stock_variance(self):
        for record in self:
            record.stock_variance = record.current_stock - record.minimum_stock
    
    @api.model
    def create(self, vals):
        """Override create to set default values and generate alert message"""
        if not vals.get('name'):
            product = self.env['product.product'].browse(vals.get('product_id'))
            warehouse = self.env['stock.warehouse'].browse(vals.get('warehouse_id'))
            vals['name'] = f"{product.name} - {warehouse.name} - {vals.get('alert_type', '').replace('_', ' ').title()}"
        
        # Generate alert message
        if not vals.get('alert_message'):
            vals['alert_message'] = self._generate_alert_message(vals)
        
        return super(StockAlert, self).create(vals)
    
    def _generate_alert_message(self, vals):
        """Generate alert message based on alert type and product details"""
        product = self.env['product.product'].browse(vals.get('product_id'))
        alert_type = vals.get('alert_type', '')
        current_stock = vals.get('current_stock', 0)
        minimum_stock = vals.get('minimum_stock', 0)
        
        messages = {
            'low_stock': f"Low stock alert for {product.name}. Current stock: {current_stock}, Minimum required: {minimum_stock}",
            'out_of_stock': f"Out of stock alert for {product.name}. Current stock: {current_stock}",
            'overstock': f"Overstock alert for {product.name}. Current stock: {current_stock}",
            'expiry_warning': f"Expiry warning for {product.name}. Check expiry dates.",
            'seasonal_alert': f"Seasonal alert for {product.name}. Consider seasonal stock adjustments.",
            'size_alert': f"Size alert for {product.name}. Check size availability.",
            'brand_alert': f"Brand alert for {product.name}. Check brand-specific stock.",
            'color_alert': f"Color alert for {product.name}. Check color availability.",
        }
        
        return messages.get(alert_type, f"Stock alert for {product.name}")
    
    def action_acknowledge(self):
        """Acknowledge the alert"""
        for record in self:
            if record.status == 'active':
                record.write({
                    'status': 'acknowledged',
                    'acknowledge_date': fields.Datetime.now(),
                    'acknowledged_by': self.env.user.id,
                })
    
    def action_resolve(self):
        """Resolve the alert"""
        for record in self:
            if record.status in ['active', 'acknowledged']:
                record.write({
                    'status': 'resolved',
                    'resolve_date': fields.Datetime.now(),
                    'resolved_by': self.env.user.id,
                })
    
    def action_cancel(self):
        """Cancel the alert"""
        for record in self:
            record.write({'status': 'cancelled'})
    
    def action_send_notification(self):
        """Send notification to users"""
        for record in self:
            if record.notify_users:
                # Send email notification
                self._send_email_notification(record)
                # Send SMS notification
                self._send_sms_notification(record)
    
    def _send_email_notification(self, record):
        """Send email notification"""
        try:
            template = self.env.ref('stock_management.email_template_stock_alert')
            for user in record.notify_users:
                template.send_mail(record.id, force_send=True)
            record.email_sent = True
        except Exception as e:
            _logger.error(f"Failed to send email notification: {e}")
    
    def _send_sms_notification(self, record):
        """Send SMS notification"""
        try:
            # SMS notification logic would go here
            # This would integrate with SMS gateway
            record.sms_sent = True
        except Exception as e:
            _logger.error(f"Failed to send SMS notification: {e}")
    
    @api.model
    def generate_stock_alerts(self):
        """Generate stock alerts based on current stock levels"""
        # This method would be called by a cron job
        products = self.env['product.product'].search([('type', '=', 'product')])
        
        for product in products:
            # Check low stock alerts
            self._check_low_stock_alert(product)
            # Check out of stock alerts
            self._check_out_of_stock_alert(product)
            # Check overstock alerts
            self._check_overstock_alert(product)
            # Check expiry warnings
            self._check_expiry_warning(product)
    
    def _check_low_stock_alert(self, product):
        """Check and create low stock alerts"""
        warehouses = self.env['stock.warehouse'].search([])
        
        for warehouse in warehouses:
            stock_location = warehouse.lot_stock_id
            current_stock = self.env['stock.quant']._get_available_quantity(
                product, stock_location
            )
            
            # Get minimum stock from reorder rules
            reorder_rules = self.env['stock.reorder.rule'].search([
                ('product_id', '=', product.id),
                ('warehouse_id', '=', warehouse.id),
            ])
            
            if reorder_rules:
                minimum_stock = reorder_rules[0].minimum_stock
                
                if current_stock <= minimum_stock:
                    # Check if alert already exists
                    existing_alert = self.search([
                        ('product_id', '=', product.id),
                        ('warehouse_id', '=', warehouse.id),
                        ('alert_type', '=', 'low_stock'),
                        ('status', '=', 'active'),
                    ])
                    
                    if not existing_alert:
                        self.create({
                            'product_id': product.id,
                            'warehouse_id': warehouse.id,
                            'location_id': stock_location.id,
                            'current_stock': current_stock,
                            'minimum_stock': minimum_stock,
                            'alert_type': 'low_stock',
                            'priority': 'high' if current_stock == 0 else 'medium',
                            'age_group': product.age_group,
                            'size': product.size,
                            'season': product.season,
                            'brand': product.brand,
                            'color': product.color,
                        })
    
    def _check_out_of_stock_alert(self, product):
        """Check and create out of stock alerts"""
        warehouses = self.env['stock.warehouse'].search([])
        
        for warehouse in warehouses:
            stock_location = warehouse.lot_stock_id
            current_stock = self.env['stock.quant']._get_available_quantity(
                product, stock_location
            )
            
            if current_stock == 0:
                # Check if alert already exists
                existing_alert = self.search([
                    ('product_id', '=', product.id),
                    ('warehouse_id', '=', warehouse.id),
                    ('alert_type', '=', 'out_of_stock'),
                    ('status', '=', 'active'),
                ])
                
                if not existing_alert:
                    self.create({
                        'product_id': product.id,
                        'warehouse_id': warehouse.id,
                        'location_id': stock_location.id,
                        'current_stock': current_stock,
                        'alert_type': 'out_of_stock',
                        'priority': 'critical',
                        'age_group': product.age_group,
                        'size': product.size,
                        'season': product.season,
                        'brand': product.brand,
                        'color': product.color,
                    })
    
    def _check_overstock_alert(self, product):
        """Check and create overstock alerts"""
        warehouses = self.env['stock.warehouse'].search([])
        
        for warehouse in warehouses:
            stock_location = warehouse.lot_stock_id
            current_stock = self.env['stock.quant']._get_available_quantity(
                product, stock_location
            )
            
            # Get maximum stock from reorder rules
            reorder_rules = self.env['stock.reorder.rule'].search([
                ('product_id', '=', product.id),
                ('warehouse_id', '=', warehouse.id),
            ])
            
            if reorder_rules:
                maximum_stock = reorder_rules[0].maximum_stock
                
                if current_stock > maximum_stock:
                    # Check if alert already exists
                    existing_alert = self.search([
                        ('product_id', '=', product.id),
                        ('warehouse_id', '=', warehouse.id),
                        ('alert_type', '=', 'overstock'),
                        ('status', '=', 'active'),
                    ])
                    
                    if not existing_alert:
                        self.create({
                            'product_id': product.id,
                            'warehouse_id': warehouse.id,
                            'location_id': stock_location.id,
                            'current_stock': current_stock,
                            'maximum_stock': maximum_stock,
                            'alert_type': 'overstock',
                            'priority': 'medium',
                            'age_group': product.age_group,
                            'size': product.size,
                            'season': product.season,
                            'brand': product.brand,
                            'color': product.color,
                        })
    
    def _check_expiry_warning(self, product):
        """Check and create expiry warnings"""
        # This would check for products with expiry dates
        # Implementation depends on how expiry is tracked
        pass