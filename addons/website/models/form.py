# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Form Management
===========================================

Website form management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class WebsiteForm(models.Model):
    """Website Form"""
    
    _name = 'website.form'
    _description = 'Website Form'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Form Name',
        required=True,
        help='Form name'
    )
    
    title = fields.Char(
        string='Form Title',
        help='Form title displayed to users'
    )
    
    description = fields.Text(
        string='Description',
        help='Form description'
    )
    
    # Form Type
    form_type = fields.Selection([
        ('contact', 'Contact Form'),
        ('newsletter', 'Newsletter Signup'),
        ('inquiry', 'Product Inquiry'),
        ('feedback', 'Feedback Form'),
        ('survey', 'Survey Form'),
        ('registration', 'Registration Form'),
        ('custom', 'Custom Form'),
    ], string='Form Type', required=True, help='Type of form')
    
    # Website Information
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help='Website this form belongs to'
    )
    
    page_id = fields.Many2one(
        'website.page',
        string='Page',
        help='Page this form belongs to'
    )
    
    # Form Settings
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this form is active'
    )
    
    is_published = fields.Boolean(
        string='Published',
        default=False,
        help='Whether this form is published'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering forms'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this form')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this form')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this form focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this form')
    
    # Form Fields
    field_ids = fields.One2many(
        'website.form.field',
        'form_id',
        string='Form Fields',
        help='Form fields'
    )
    
    # Form Actions
    action_type = fields.Selection([
        ('email', 'Send Email'),
        ('create_lead', 'Create Lead'),
        ('create_contact', 'Create Contact'),
        ('redirect', 'Redirect'),
        ('custom', 'Custom Action'),
    ], string='Action Type', default='email', help='What to do when form is submitted')
    
    email_to = fields.Char(
        string='Email To',
        help='Email address to send form submissions to'
    )
    
    email_subject = fields.Char(
        string='Email Subject',
        help='Email subject for form submissions'
    )
    
    redirect_url = fields.Char(
        string='Redirect URL',
        help='URL to redirect to after form submission'
    )
    
    success_message = fields.Text(
        string='Success Message',
        default='Thank you for your submission!',
        help='Message to show after successful form submission'
    )
    
    # Analytics
    total_submissions = fields.Integer(
        string='Total Submissions',
        compute='_compute_analytics',
        store=True,
        help='Total number of form submissions'
    )
    
    conversion_rate = fields.Float(
        string='Conversion Rate (%)',
        compute='_compute_analytics',
        store=True,
        help='Form conversion rate percentage'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this form'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for form in self:
            # This would be computed from submission data
            form.total_submissions = 0
            form.conversion_rate = 0.0
    
    def action_publish(self):
        """Publish form"""
        for form in self:
            if not form.is_active:
                raise UserError(_('Only active forms can be published.'))
            
            form.is_published = True
    
    def action_unpublish(self):
        """Unpublish form"""
        for form in self:
            form.is_published = False
    
    def action_preview(self):
        """Preview form"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/website/form_preview/{self.id}',
            'target': 'new',
        }
    
    def action_view_submissions(self):
        """View form submissions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Form Submissions'),
            'res_model': 'website.form.submission',
            'view_mode': 'tree,form',
            'domain': [('form_id', '=', self.id)],
            'context': {'default_form_id': self.id},
        }
    
    def get_form_analytics(self, date_from=None, date_to=None):
        """Get form analytics for date range"""
        self.ensure_one()
        # This would query submission data
        # For now, returning basic info
        return {
            'total_submissions': self.total_submissions,
            'conversion_rate': self.conversion_rate,
        }


class WebsiteFormField(models.Model):
    """Website Form Field"""
    
    _name = 'website.form.field'
    _description = 'Website Form Field'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Field Name',
        required=True,
        help='Field name'
    )
    
    label = fields.Char(
        string='Field Label',
        required=True,
        help='Field label displayed to users'
    )
    
    # Form Information
    form_id = fields.Many2one(
        'website.form',
        string='Form',
        required=True,
        ondelete='cascade',
        help='Form this field belongs to'
    )
    
    # Field Type
    field_type = fields.Selection([
        ('text', 'Text'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('number', 'Number'),
        ('textarea', 'Text Area'),
        ('select', 'Select'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('date', 'Date'),
        ('file', 'File Upload'),
        ('hidden', 'Hidden'),
    ], string='Field Type', required=True, help='Type of field')
    
    # Field Settings
    is_required = fields.Boolean(
        string='Required',
        default=False,
        help='Whether this field is required'
    )
    
    placeholder = fields.Char(
        string='Placeholder',
        help='Field placeholder text'
    )
    
    help_text = fields.Text(
        string='Help Text',
        help='Help text for this field'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering fields'
    )
    
    # Field Options (for select, radio, checkbox)
    option_ids = fields.One2many(
        'website.form.field.option',
        'field_id',
        string='Field Options',
        help='Options for select/radio/checkbox fields'
    )
    
    # Validation
    min_length = fields.Integer(
        string='Minimum Length',
        help='Minimum length for text fields'
    )
    
    max_length = fields.Integer(
        string='Maximum Length',
        help='Maximum length for text fields'
    )
    
    min_value = fields.Float(
        string='Minimum Value',
        help='Minimum value for number fields'
    )
    
    max_value = fields.Float(
        string='Maximum Value',
        help='Maximum value for number fields'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this field')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this field')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this field focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this field')
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this field'
    )


class WebsiteFormFieldOption(models.Model):
    """Website Form Field Option"""
    
    _name = 'website.form.field.option'
    _description = 'Website Form Field Option'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Option Name',
        required=True,
        help='Option name'
    )
    
    value = fields.Char(
        string='Option Value',
        required=True,
        help='Option value'
    )
    
    # Field Information
    field_id = fields.Many2one(
        'website.form.field',
        string='Field',
        required=True,
        ondelete='cascade',
        help='Field this option belongs to'
    )
    
    # Option Settings
    is_default = fields.Boolean(
        string='Default',
        default=False,
        help='Whether this is the default option'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering options'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this option')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this option')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this option focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this option')


class WebsiteFormSubmission(models.Model):
    """Website Form Submission"""
    
    _name = 'website.form.submission'
    _description = 'Website Form Submission'
    _order = 'create_date desc'
    
    # Basic Information
    name = fields.Char(
        string='Submission Name',
        compute='_compute_name',
        store=True,
        help='Submission name'
    )
    
    # Form Information
    form_id = fields.Many2one(
        'website.form',
        string='Form',
        required=True,
        help='Form this submission belongs to'
    )
    
    # Submission Data
    submission_data = fields.Text(
        string='Submission Data',
        help='Form submission data in JSON format'
    )
    
    # Contact Information
    contact_name = fields.Char(
        string='Contact Name',
        help='Contact name from submission'
    )
    
    contact_email = fields.Char(
        string='Contact Email',
        help='Contact email from submission'
    )
    
    contact_phone = fields.Char(
        string='Contact Phone',
        help='Contact phone from submission'
    )
    
    # Status
    state = fields.Selection([
        ('new', 'New'),
        ('processed', 'Processed'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ], string='Status', default='new', help='Submission status')
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this submission')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this submission')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this submission focuses on'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this submission')
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this submission'
    )
    
    @api.depends('form_id', 'contact_name', 'create_date')
    def _compute_name(self):
        """Compute submission name"""
        for submission in self:
            if submission.contact_name:
                submission.name = f"{submission.form_id.name} - {submission.contact_name}"
            else:
                submission.name = f"{submission.form_id.name} - {submission.create_date}"
    
    def action_process(self):
        """Process submission"""
        for submission in self:
            if submission.state != 'new':
                raise UserError(_('Only new submissions can be processed.'))
            
            submission.state = 'processed'
    
    def action_reply(self):
        """Mark as replied"""
        for submission in self:
            if submission.state not in ['new', 'processed']:
                raise UserError(_('Only new or processed submissions can be marked as replied.'))
            
            submission.state = 'replied'
    
    def action_close(self):
        """Close submission"""
        for submission in self:
            submission.state = 'closed'