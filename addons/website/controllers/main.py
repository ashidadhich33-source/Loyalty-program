# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website Controllers
======================================

Website controllers for kids clothing retail business.
"""

from ocean import http, fields, _
from ocean.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class WebsiteController(http.Controller):
    """Website Controller"""
    
    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kwargs):
        """Home page"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        if not website:
            return request.render('website.home_template', {
                'website': None,
                'pages': [],
            })
        
        # Get home page
        home_page = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('page_type', '=', 'home'),
            ('is_published', '=', True)
        ], limit=1)
        
        # Get published pages
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.home_template', {
            'website': website,
            'home_page': home_page,
            'pages': pages,
        })
    
    @http.route('/page/<int:page_id>', type='http', auth='public', website=True)
    def page(self, page_id, **kwargs):
        """Page view"""
        page = request.env['website.page'].browse(page_id)
        
        if not page.exists() or not page.is_published:
            return request.render('website.page_not_found')
        
        # Get website
        website = page.website_id
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.page_template', {
            'website': website,
            'page': page,
            'pages': pages,
        })
    
    @http.route('/contact', type='http', auth='public', website=True)
    def contact(self, **kwargs):
        """Contact page"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Get contact form
        contact_form = request.env['website.form'].search([
            ('website_id', '=', website.id),
            ('form_type', '=', 'contact'),
            ('is_published', '=', True)
        ], limit=1)
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.contact_template', {
            'website': website,
            'contact_form': contact_form,
            'pages': pages,
        })
    
    @http.route('/about', type='http', auth='public', website=True)
    def about(self, **kwargs):
        """About page"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Get about page
        about_page = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('page_type', '=', 'about'),
            ('is_published', '=', True)
        ], limit=1)
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.about_template', {
            'website': website,
            'about_page': about_page,
            'pages': pages,
        })
    
    @http.route('/products', type='http', auth='public', website=True)
    def products(self, **kwargs):
        """Products page"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Get products (this would integrate with products addon)
        products = []
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.products_template', {
            'website': website,
            'products': products,
            'pages': pages,
        })
    
    @http.route('/blog', type='http', auth='public', website=True)
    def blog(self, **kwargs):
        """Blog page"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Get blog posts (this would integrate with blog addon)
        blog_posts = []
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.blog_template', {
            'website': website,
            'blog_posts': blog_posts,
            'pages': pages,
        })
    
    @http.route('/form/submit', type='http', auth='public', methods=['POST'], website=True)
    def form_submit(self, **kwargs):
        """Form submission"""
        form_id = kwargs.get('form_id')
        if not form_id:
            return request.render('website.form_error', {
                'error': 'Form ID is required.'
            })
        
        form = request.env['website.form'].browse(int(form_id))
        if not form.exists() or not form.is_published:
            return request.render('website.form_error', {
                'error': 'Form not found or not published.'
            })
        
        # Process form submission
        submission_data = {}
        for key, value in kwargs.items():
            if key.startswith('field_'):
                field_name = key.replace('field_', '')
                submission_data[field_name] = value
        
        # Create form submission
        submission_vals = {
            'form_id': form.id,
            'submission_data': json.dumps(submission_data),
            'contact_name': kwargs.get('name', ''),
            'contact_email': kwargs.get('email', ''),
            'contact_phone': kwargs.get('phone', ''),
        }
        
        submission = request.env['website.form.submission'].create(submission_vals)
        
        # Send email if configured
        if form.action_type == 'email' and form.email_to:
            # This would send email notification
            pass
        
        # Create lead if configured
        if form.action_type == 'create_lead':
            # This would create a lead
            pass
        
        # Create contact if configured
        if form.action_type == 'create_contact':
            # This would create a contact
            pass
        
        return request.render('website.form_success', {
            'form': form,
            'submission': submission,
        })
    
    @http.route('/newsletter/subscribe', type='http', auth='public', methods=['POST'], website=True)
    def newsletter_subscribe(self, **kwargs):
        """Newsletter subscription"""
        email = kwargs.get('email')
        if not email:
            return request.render('website.newsletter_error', {
                'error': 'Email is required.'
            })
        
        # Create newsletter subscription (this would integrate with newsletter addon)
        # For now, just return success
        
        return request.render('website.newsletter_success', {
            'email': email,
        })
    
    @http.route('/search', type='http', auth='public', website=True)
    def search(self, **kwargs):
        """Search page"""
        query = kwargs.get('q', '')
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Search results (this would integrate with search functionality)
        results = []
        
        # Get published pages for menu
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True),
            ('show_in_menu', '=', True)
        ])
        
        return request.render('website.search_template', {
            'website': website,
            'query': query,
            'results': results,
            'pages': pages,
        })
    
    @http.route('/sitemap.xml', type='http', auth='public')
    def sitemap(self, **kwargs):
        """Sitemap"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        # Get published pages
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True)
        ])
        
        return request.render('website.sitemap_template', {
            'website': website,
            'pages': pages,
        })
    
    @http.route('/robots.txt', type='http', auth='public')
    def robots(self, **kwargs):
        """Robots.txt"""
        website = request.env['website'].search([('is_default', '=', True)], limit=1)
        if not website:
            website = request.env['website'].search([('is_active', '=', True)], limit=1)
        
        return request.render('website.robots_template', {
            'website': website,
        })