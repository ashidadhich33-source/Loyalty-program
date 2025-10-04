# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Period Model
=================================

Accounting period management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AccountPeriod(BaseModel, KidsClothingMixin):
    """Account Period Model for Ocean ERP"""
    
    _name = 'account.period'
    _description = 'Account Period'
    _order = 'date_start desc'
    _rec_name = 'name'

    name = CharField(
        string='Period Name',
        required=True,
        help='Name of the period'
    )
    
    code = CharField(
        string='Period Code',
        help='Code for the period'
    )
    
    date_start = DateTimeField(
        string='Start Date',
        required=True,
        help='Start date of the period'
    )
    
    date_stop = DateTimeField(
        string='End Date',
        required=True,
        help='End date of the period'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('closed', 'Closed'),
        ],
        string='Status',
        default='draft',
        help='Status of the period'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for the period'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for the period'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the period'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the period'
    )
    
    color = CharField(
        string='Color',
        help='Color for the period'
    )
    
    # Fiscal Year
    fiscalyear_id = Many2OneField(
        'account.fiscal.year',
        string='Fiscal Year',
        required=True,
        help='Fiscal year this period belongs to'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this period belongs to'
    )
    
    # Special Periods
    special = BooleanField(
        string='Special Period',
        default=False,
        help='Special period (opening/closing)'
    )
    
    # Period Type
    period_type = SelectionField(
        selection=[
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        string='Period Type',
        default='monthly',
        help='Type of period'
    )
    
    # Move Lines
    move_line_ids = One2ManyField(
        'account.move.line',
        'period_id',
        string='Move Lines',
        help='Move lines for this period'
    )
    
    # Move Count
    move_count = IntegerField(
        string='Move Count',
        compute='_compute_move_count',
        help='Number of moves in this period'
    )
    
    def _compute_move_count(self):
        """Compute move count"""
        for record in self:
            record.move_count = len(record.move_line_ids.mapped('move_id'))
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code from date
            date_start = vals.get('date_start')
            if date_start:
                date_obj = datetime.strptime(str(date_start), '%Y-%m-%d')
                vals['code'] = date_obj.strftime('%Y%m')
        
        return super(AccountPeriod, self).create(vals)
    
    def action_open(self):
        """Open the period"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft periods can be opened.')
            
            record.write({'state': 'open'})
    
    def action_close(self):
        """Close the period"""
        for record in self:
            if record.state != 'open':
                raise UserError('Only open periods can be closed.')
            
            # Check if there are any draft moves
            draft_moves = self.env['account.move'].search([
                ('date', '>=', record.date_start),
                ('date', '<=', record.date_stop),
                ('state', '=', 'draft'),
                ('company_id', '=', record.company_id.id)
            ])
            
            if draft_moves:
                raise UserError('Cannot close period with draft moves.')
            
            record.write({'state': 'closed'})
    
    def action_reopen(self):
        """Reopen the period"""
        for record in self:
            if record.state != 'closed':
                raise UserError('Only closed periods can be reopened.')
            
            record.write({'state': 'open'})
    
    def action_view_moves(self):
        """View moves for this period"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Journal Entries',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [
                ('date', '>=', self.date_start),
                ('date', '<=', self.date_stop),
                ('company_id', '=', self.company_id.id)
            ],
            'context': {'default_date': self.date_start},
        }
    
    def get_kids_clothing_periods(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get periods filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)


class AccountFiscalYear(BaseModel, KidsClothingMixin):
    """Account Fiscal Year Model for Ocean ERP"""
    
    _name = 'account.fiscal.year'
    _description = 'Account Fiscal Year'
    _order = 'date_start desc'
    _rec_name = 'name'

    name = CharField(
        string='Fiscal Year Name',
        required=True,
        help='Name of the fiscal year'
    )
    
    code = CharField(
        string='Fiscal Year Code',
        help='Code for the fiscal year'
    )
    
    date_start = DateTimeField(
        string='Start Date',
        required=True,
        help='Start date of the fiscal year'
    )
    
    date_stop = DateTimeField(
        string='End Date',
        required=True,
        help='End date of the fiscal year'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('closed', 'Closed'),
        ],
        string='Status',
        default='draft',
        help='Status of the fiscal year'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for the fiscal year'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the fiscal year'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the fiscal year'
    )
    
    color = CharField(
        string='Color',
        help='Color for the fiscal year'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this fiscal year belongs to'
    )
    
    # Periods
    period_ids = One2ManyField(
        'account.period',
        'fiscalyear_id',
        string='Periods',
        help='Periods for this fiscal year'
    )
    
    # Period Count
    period_count = IntegerField(
        string='Period Count',
        compute='_compute_period_count',
        help='Number of periods in this fiscal year'
    )
    
    def _compute_period_count(self):
        """Compute period count"""
        for record in self:
            record.period_count = len(record.period_ids)
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code from date
            date_start = vals.get('date_start')
            if date_start:
                date_obj = datetime.strptime(str(date_start), '%Y-%m-%d')
                vals['code'] = date_obj.strftime('%Y')
        
        return super(AccountFiscalYear, self).create(vals)
    
    def action_open(self):
        """Open the fiscal year"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft fiscal years can be opened.')
            
            record.write({'state': 'open'})
    
    def action_close(self):
        """Close the fiscal year"""
        for record in self:
            if record.state != 'open':
                raise UserError('Only open fiscal years can be closed.')
            
            # Check if all periods are closed
            open_periods = record.period_ids.filtered(lambda p: p.state != 'closed')
            if open_periods:
                raise UserError('Cannot close fiscal year with open periods.')
            
            record.write({'state': 'closed'})
    
    def action_reopen(self):
        """Reopen the fiscal year"""
        for record in self:
            if record.state != 'closed':
                raise UserError('Only closed fiscal years can be reopened.')
            
            record.write({'state': 'open'})
    
    def action_view_periods(self):
        """View periods for this fiscal year"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Periods',
            'res_model': 'account.period',
            'view_mode': 'tree,form',
            'domain': [('fiscalyear_id', '=', self.id)],
            'context': {'default_fiscalyear_id': self.id},
        }
    
    def generate_periods(self):
        """Generate periods for this fiscal year"""
        for record in self:
            if record.period_ids:
                raise UserError('Periods already exist for this fiscal year.')
            
            # Generate monthly periods
            current_date = record.date_start
            period_num = 1
            
            while current_date <= record.date_stop:
                # Calculate end date for this period
                if period_num == 12:
                    # Last period ends on fiscal year end
                    period_end = record.date_stop
                else:
                    # Other periods end on last day of month
                    if current_date.month == 12:
                        period_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
                    else:
                        period_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
                
                # Create period
                self.env['account.period'].create({
                    'name': f"{record.name} - {current_date.strftime('%B %Y')}",
                    'code': f"{record.code}{period_num:02d}",
                    'date_start': current_date,
                    'date_stop': period_end,
                    'fiscalyear_id': record.id,
                    'company_id': record.company_id.id,
                    'age_group': record.age_group,
                    'season': record.season,
                    'brand': record.brand,
                    'color': record.color,
                })
                
                # Move to next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1, day=1)
                
                period_num += 1
    
    def get_kids_clothing_fiscal_years(self, age_group=None, season=None, brand=None, color=None):
        """Get fiscal years filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)