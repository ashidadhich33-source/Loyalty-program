# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Website API Controllers
===========================================

Website API controllers for kids clothing retail business.
"""

from ocean import http, fields, _
from ocean.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class WebsiteAPIController(http.Controller):
    """Website API Controller"""
    
    @http.route('/api/website/data', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_data(self, **kwargs):
        """Get website data"""
        website_id = kwargs.get('website_id')
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        data = {
            'id': website.id,
            'name': website.name,
            'domain': website.domain,
            'url': website.url,
            'is_active': website.is_active,
            'meta_title': website.meta_title,
            'meta_description': website.meta_description,
            'contact_email': website.contact_email,
            'contact_phone': website.contact_phone,
            'contact_address': website.contact_address,
            'social_media': {
                'facebook': website.facebook_url,
                'instagram': website.instagram_url,
                'twitter': website.twitter_url,
                'youtube': website.youtube_url,
            },
            'analytics': {
                'google_analytics_id': website.google_analytics_id,
                'google_tag_manager_id': website.google_tag_manager_id,
                'facebook_pixel_id': website.facebook_pixel_id,
            },
        }
        
        return request.make_json_response(data)
    
    @http.route('/api/website/pages', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_pages(self, **kwargs):
        """Get website pages"""
        website_id = kwargs.get('website_id')
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        pages = request.env['website.page'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True)
        ])
        
        data = []
        for page in pages:
            data.append({
                'id': page.id,
                'name': page.name,
                'url': page.url,
                'title': page.title,
                'page_type': page.page_type,
                'meta_title': page.meta_title,
                'meta_description': page.meta_description,
                'show_in_menu': page.show_in_menu,
            })
        
        return request.make_json_response(data)
    
    @http.route('/api/website/page/<int:page_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_page(self, page_id, **kwargs):
        """Get page data"""
        page = request.env['website.page'].browse(page_id)
        
        if not page.exists() or not page.is_published:
            return request.make_json_response({'error': 'Page not found'}, 404)
        
        data = {
            'id': page.id,
            'name': page.name,
            'url': page.url,
            'title': page.title,
            'page_type': page.page_type,
            'content': page.content,
            'meta_title': page.meta_title,
            'meta_description': page.meta_description,
            'meta_keywords': page.meta_keywords,
            'website': {
                'id': page.website_id.id,
                'name': page.website_id.name,
                'domain': page.website_id.domain,
            },
        }
        
        return request.make_json_response(data)
    
    @http.route('/api/website/forms', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_forms(self, **kwargs):
        """Get website forms"""
        website_id = kwargs.get('website_id')
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        forms = request.env['website.form'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True)
        ])
        
        data = []
        for form in forms:
            fields_data = []
            for field in form.field_ids:
                options_data = []
                for option in field.option_ids:
                    options_data.append({
                        'name': option.name,
                        'value': option.value,
                        'is_default': option.is_default,
                    })
                
                fields_data.append({
                    'id': field.id,
                    'name': field.name,
                    'label': field.label,
                    'field_type': field.field_type,
                    'is_required': field.is_required,
                    'placeholder': field.placeholder,
                    'help_text': field.help_text,
                    'options': options_data,
                })
            
            data.append({
                'id': form.id,
                'name': form.name,
                'title': form.title,
                'form_type': form.form_type,
                'description': form.description,
                'fields': fields_data,
                'action_type': form.action_type,
                'success_message': form.success_message,
            })
        
        return request.make_json_response(data)
    
    @http.route('/api/website/form/<int:form_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_form(self, form_id, **kwargs):
        """Get form data"""
        form = request.env['website.form'].browse(form_id)
        
        if not form.exists() or not form.is_published:
            return request.make_json_response({'error': 'Form not found'}, 404)
        
        fields_data = []
        for field in form.field_ids:
            options_data = []
            for option in field.option_ids:
                options_data.append({
                    'name': option.name,
                    'value': option.value,
                    'is_default': option.is_default,
                })
            
            fields_data.append({
                'id': field.id,
                'name': field.name,
                'label': field.label,
                'field_type': field.field_type,
                'is_required': field.is_required,
                'placeholder': field.placeholder,
                'help_text': field.help_text,
                'options': options_data,
            })
        
        data = {
            'id': form.id,
            'name': form.name,
            'title': form.title,
            'form_type': form.form_type,
            'description': form.description,
            'fields': fields_data,
            'action_type': form.action_type,
            'success_message': form.success_message,
        }
        
        return request.make_json_response(data)
    
    @http.route('/api/website/analytics', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_analytics(self, **kwargs):
        """Get website analytics"""
        website_id = kwargs.get('website_id')
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        
        # Get analytics data
        analytics = request.env['website.analytics'].search([
            ('website_id', '=', website.id),
            ('date', '>=', date_from) if date_from else (1, '=', 1),
            ('date', '<=', date_to) if date_to else (1, '=', 1),
        ])
        
        data = {
            'website_id': website.id,
            'total_visitors': sum(analytics.mapped('total_visitors')),
            'unique_visitors': sum(analytics.mapped('unique_visitors')),
            'total_page_views': sum(analytics.mapped('total_page_views')),
            'avg_session_duration': sum(analytics.mapped('avg_session_duration')) / len(analytics) if analytics else 0,
            'bounce_rate': sum(analytics.mapped('bounce_rate')) / len(analytics) if analytics else 0,
            'conversion_rate': sum(analytics.mapped('conversion_rate')) / len(analytics) if analytics else 0,
            'total_revenue': sum(analytics.mapped('total_revenue')),
        }
        
        return request.make_json_response(data)
    
    @http.route('/api/website/content', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_content(self, **kwargs):
        """Get website content"""
        website_id = kwargs.get('website_id')
        page_id = kwargs.get('page_id')
        
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        domain = [('website_id', '=', website.id), ('is_published', '=', True)]
        if page_id:
            domain.append(('page_id', '=', int(page_id)))
        
        content = request.env['website.content'].search(domain)
        
        data = []
        for item in content:
            data.append({
                'id': item.id,
                'name': item.name,
                'title': item.title,
                'content_type': item.content_type,
                'text_content': item.text_content,
                'image_url': item.image_url,
                'video_url': item.video_url,
                'display_position': item.display_position,
                'display_style': item.display_style,
            })
        
        return request.make_json_response(data)
    
    @http.route('/api/website/galleries', type='http', auth='public', methods=['GET'], csrf=False)
    def get_website_galleries(self, **kwargs):
        """Get website galleries"""
        website_id = kwargs.get('website_id')
        if website_id:
            website = request.env['website'].browse(int(website_id))
        else:
            website = request.env['website'].search([('is_default', '=', True)], limit=1)
        
        if not website:
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        galleries = request.env['website.gallery'].search([
            ('website_id', '=', website.id),
            ('is_published', '=', True)
        ])
        
        data = []
        for gallery in galleries:
            images_data = []
            for image in gallery.image_ids:
                images_data.append({
                    'id': image.id,
                    'name': image.name,
                    'image_url': image.image_url,
                    'alt_text': image.alt_text,
                    'caption': image.caption,
                })
            
            data.append({
                'id': gallery.id,
                'name': gallery.name,
                'description': gallery.description,
                'gallery_type': gallery.gallery_type,
                'images': images_data,
            })
        
        return request.make_json_response(data)
    
    @http.route('/api/website/track', type='http', auth='public', methods=['POST'], csrf=False)
    def track_visit(self, **kwargs):
        """Track website visit"""
        data = json.loads(request.httprequest.data.decode('utf-8'))
        
        website_id = data.get('website_id')
        page_id = data.get('page_id')
        visitor_id = data.get('visitor_id')
        
        if not website_id or not visitor_id:
            return request.make_json_response({'error': 'Missing required data'}, 400)
        
        website = request.env['website'].browse(int(website_id))
        if not website.exists():
            return request.make_json_response({'error': 'Website not found'}, 404)
        
        # Create or update visitor
        visitor = request.env['website.visitor'].search([
            ('visitor_id', '=', visitor_id),
            ('website_id', '=', website.id)
        ], limit=1)
        
        if not visitor:
            visitor_vals = {
                'visitor_id': visitor_id,
                'website_id': website.id,
                'first_visit': fields.Datetime.now(),
                'last_visit': fields.Datetime.now(),
                'total_visits': 1,
                'country': data.get('country'),
                'state': data.get('state'),
                'city': data.get('city'),
                'device_type': data.get('device_type'),
                'browser': data.get('browser'),
                'operating_system': data.get('operating_system'),
            }
            visitor = request.env['website.visitor'].create(visitor_vals)
        else:
            visitor.write({
                'last_visit': fields.Datetime.now(),
                'total_visits': visitor.total_visits + 1,
            })
        
        # Create analytics record
        analytics_vals = {
            'website_id': website.id,
            'page_id': page_id,
            'date': fields.Date.context_today(request),
            'total_visitors': 1,
            'unique_visitors': 1,
            'total_page_views': 1,
            'country': data.get('country'),
            'state': data.get('state'),
            'city': data.get('city'),
            'device_type': data.get('device_type'),
            'browser': data.get('browser'),
            'operating_system': data.get('operating_system'),
            'traffic_source': data.get('traffic_source'),
            'referrer_url': data.get('referrer_url'),
        }
        
        request.env['website.analytics'].create(analytics_vals)
        
        return request.make_json_response({'success': True})