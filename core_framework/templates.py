#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Template Rendering System
============================================

Template rendering system for dynamic page generation.
"""

import os
import re
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TemplateEngine:
    """Template Engine for ERP System"""
    
    def __init__(self, config):
        """Initialize template engine"""
        self.config = config
        self.template_path = config.get('web.template_path', 'templates')
        self.templates = {}
        self.template_cache = {}
        self.load_templates()
    
    def load_templates(self):
        """Load all templates from template directory"""
        try:
            template_dir = Path(self.template_path)
            if not template_dir.exists():
                template_dir.mkdir(parents=True, exist_ok=True)
                return
            
            for template_file in template_dir.glob('**/*.html'):
                template_name = str(template_file.relative_to(template_dir))
                self.templates[template_name] = template_file
            
            logger.info(f"Loaded {len(self.templates)} templates")
            
        except Exception as e:
            logger.error(f"Template loading error: {e}")
    
    def render_template(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """Render template with context"""
        try:
            if context is None:
                context = {}
            
            # Get template content
            template_content = self._get_template_content(template_name)
            if not template_content:
                return f"Template '{template_name}' not found"
            
            # Process template
            rendered_content = self._process_template(template_content, context)
            
            return rendered_content
            
        except Exception as e:
            logger.error(f"Template rendering error: {e}")
            return f"Template rendering error: {str(e)}"
    
    def _get_template_content(self, template_name: str) -> Optional[str]:
        """Get template content"""
        try:
            # Check cache first
            if template_name in self.template_cache:
                return self.template_cache[template_name]
            
            # Load from file
            if template_name in self.templates:
                with open(self.templates[template_name], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Cache template
                self.template_cache[template_name] = content
                return content
            
            return None
            
        except Exception as e:
            logger.error(f"Template content retrieval error: {e}")
            return None
    
    def _process_template(self, template_content: str, context: Dict[str, Any]) -> str:
        """Process template with context"""
        try:
            # Process variables {{ variable }}
            template_content = self._process_variables(template_content, context)
            
            # Process conditionals {% if condition %}
            template_content = self._process_conditionals(template_content, context)
            
            # Process loops {% for item in items %}
            template_content = self._process_loops(template_content, context)
            
            # Process includes {% include template %}
            template_content = self._process_includes(template_content, context)
            
            return template_content
            
        except Exception as e:
            logger.error(f"Template processing error: {e}")
            return template_content
    
    def _process_variables(self, content: str, context: Dict[str, Any]) -> str:
        """Process template variables"""
        def replace_variable(match):
            var_name = match.group(1).strip()
            return str(self._get_context_value(var_name, context))
        
        return re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_variable, content)
    
    def _process_conditionals(self, content: str, context: Dict[str, Any]) -> str:
        """Process template conditionals"""
        def process_if_block(match):
            condition = match.group(1).strip()
            if_content = match.group(2)
            else_content = match.group(3) if match.group(3) else ''
            
            if self._evaluate_condition(condition, context):
                return if_content
            else:
                return else_content
        
        # Process {% if condition %} ... {% else %} ... {% endif %}
        pattern = r'\{%\s*if\s+([^%]+)\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}'
        content = re.sub(pattern, process_if_block, content, flags=re.DOTALL)
        
        # Process {% if condition %} ... {% endif %}
        pattern = r'\{%\s*if\s+([^%]+)\s*%\}(.*?)\{%\s*endif\s*%\}'
        content = re.sub(pattern, process_if_block, content, flags=re.DOTALL)
        
        return content
    
    def _process_loops(self, content: str, context: Dict[str, Any]) -> str:
        """Process template loops"""
        def process_for_block(match):
            loop_var = match.group(1).strip()
            iterable_name = match.group(2).strip()
            loop_content = match.group(3)
            
            iterable = self._get_context_value(iterable_name, context)
            if not isinstance(iterable, (list, tuple)):
                return ''
            
            result = ''
            for i, item in enumerate(iterable):
                loop_context = context.copy()
                loop_context[loop_var] = item
                loop_context['loop'] = {
                    'index': i,
                    'index0': i,
                    'first': i == 0,
                    'last': i == len(iterable) - 1,
                    'length': len(iterable)
                }
                
                # Process loop content with loop context
                processed_content = self._process_template(loop_content, loop_context)
                result += processed_content
            
            return result
        
        pattern = r'\{%\s*for\s+(\w+)\s+in\s+([^%]+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        content = re.sub(pattern, process_for_block, content, flags=re.DOTALL)
        
        return content
    
    def _process_includes(self, content: str, context: Dict[str, Any]) -> str:
        """Process template includes"""
        def process_include(match):
            include_template = match.group(1).strip()
            include_context = context.copy()
            
            # Process include template
            included_content = self.render_template(include_template, include_context)
            return included_content
        
        pattern = r'\{%\s*include\s+([^%]+)\s*%\}'
        content = re.sub(pattern, process_include, content)
        
        return content
    
    def _get_context_value(self, var_name: str, context: Dict[str, Any]) -> Any:
        """Get value from context using dot notation"""
        try:
            parts = var_name.split('.')
            value = context
            
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                elif hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return ''
            
            return value if value is not None else ''
            
        except Exception as e:
            logger.error(f"Context value retrieval error: {e}")
            return ''
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate condition expression"""
        try:
            # Simple condition evaluation
            # In production, use a proper expression evaluator
            
            # Handle simple comparisons
            if '==' in condition:
                left, right = condition.split('==', 1)
                left_val = self._get_context_value(left.strip(), context)
                right_val = self._get_context_value(right.strip(), context)
                return str(left_val) == str(right_val)
            
            elif '!=' in condition:
                left, right = condition.split('!=', 1)
                left_val = self._get_context_value(left.strip(), context)
                right_val = self._get_context_value(right.strip(), context)
                return str(left_val) != str(right_val)
            
            elif 'in' in condition:
                left, right = condition.split('in', 1)
                left_val = self._get_context_value(left.strip(), context)
                right_val = self._get_context_value(right.strip(), context)
                return str(left_val) in str(right_val)
            
            else:
                # Simple truthiness check
                value = self._get_context_value(condition.strip(), context)
                return bool(value)
                
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return False
    
    def create_template(self, template_name: str, content: str) -> bool:
        """Create new template"""
        try:
            template_path = Path(self.template_path) / template_name
            template_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update templates cache
            self.templates[template_name] = template_path
            self.template_cache[template_name] = content
            
            logger.info(f"Created template: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Template creation error: {e}")
            return False
    
    def delete_template(self, template_name: str) -> bool:
        """Delete template"""
        try:
            if template_name in self.templates:
                template_path = self.templates[template_name]
                if template_path.exists():
                    template_path.unlink()
                
                # Remove from cache
                del self.templates[template_name]
                if template_name in self.template_cache:
                    del self.template_cache[template_name]
                
                logger.info(f"Deleted template: {template_name}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Template deletion error: {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.templates.keys())
    
    def clear_cache(self):
        """Clear template cache"""
        self.template_cache.clear()
        logger.info("Template cache cleared")


class TemplateRenderer:
    """Template Renderer for ERP Views"""
    
    def __init__(self, template_engine):
        """Initialize template renderer"""
        self.template_engine = template_engine
    
    def render_view(self, view_name: str, context: Dict[str, Any] = None) -> str:
        """Render ERP view"""
        try:
            if context is None:
                context = {}
            
            # Add default context
            context.update(self._get_default_context())
            
            # Render template
            return self.template_engine.render_template(view_name, context)
            
        except Exception as e:
            logger.error(f"View rendering error: {e}")
            return f"View rendering error: {str(e)}"
    
    def render_form(self, form_name: str, context: Dict[str, Any] = None) -> str:
        """Render ERP form"""
        try:
            if context is None:
                context = {}
            
            # Add form-specific context
            context.update(self._get_form_context())
            
            # Render form template
            return self.template_engine.render_template(f"forms/{form_name}", context)
            
        except Exception as e:
            logger.error(f"Form rendering error: {e}")
            return f"Form rendering error: {str(e)}"
    
    def render_report(self, report_name: str, context: Dict[str, Any] = None) -> str:
        """Render ERP report"""
        try:
            if context is None:
                context = {}
            
            # Add report-specific context
            context.update(self._get_report_context())
            
            # Render report template
            return self.template_engine.render_template(f"reports/{report_name}", context)
            
        except Exception as e:
            logger.error(f"Report rendering error: {e}")
            return f"Report rendering error: {str(e)}"
    
    def _get_default_context(self) -> Dict[str, Any]:
        """Get default template context"""
        return {
            'app_name': 'Kids Clothing ERP',
            'version': '1.0.0',
            'current_year': 2024,
            'theme': 'kids_clothing',
            'user': {
                'name': 'Admin User',
                'email': 'admin@example.com'
            }
        }
    
    def _get_form_context(self) -> Dict[str, Any]:
        """Get form-specific context"""
        return {
            'form_helpers': {
                'csrf_token': 'dummy_csrf_token',
                'form_action': '/api/form/submit',
                'form_method': 'POST'
            }
        }
    
    def _get_report_context(self) -> Dict[str, Any]:
        """Get report-specific context"""
        return {
            'report_helpers': {
                'format_date': self._format_date,
                'format_currency': self._format_currency,
                'format_number': self._format_number
            }
        }
    
    def _format_date(self, date_value, format_str='%Y-%m-%d'):
        """Format date value"""
        try:
            if hasattr(date_value, 'strftime'):
                return date_value.strftime(format_str)
            return str(date_value)
        except:
            return str(date_value)
    
    def _format_currency(self, amount, currency='INR'):
        """Format currency value"""
        try:
            if currency == 'INR':
                return f"₹{amount:,.2f}"
            else:
                return f"{currency} {amount:,.2f}"
        except:
            return str(amount)
    
    def _format_number(self, number, decimals=2):
        """Format number value"""
        try:
            return f"{number:,.{decimals}f}"
        except:
            return str(number)