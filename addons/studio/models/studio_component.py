#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Component
===================================

Studio component management for custom component creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioComponent(BaseModel, KidsClothingMixin):
    """Studio Component for Custom Component Creation"""
    
    _name = 'studio.component'
    _description = 'Studio Component'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Component Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    project_id = Many2OneField('studio.project', 'Project', required=True)
    
    # Component Configuration
    component_type = SelectionField([
        ('widget', 'Widget'),
        ('field', 'Custom Field'),
        ('button', 'Custom Button'),
        ('action', 'Custom Action'),
        ('report', 'Custom Report'),
        ('dashboard', 'Dashboard Widget'),
        ('chart', 'Chart Component'),
        ('form', 'Form Component'),
        ('view', 'View Component'),
        ('template', 'Template'),
    ], 'Component Type', required=True)
    
    # Component Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_published = BooleanField('Published', default=False)
    
    # Component Content
    component_code = TextField('Component Code', 
                             help='JavaScript/Python code for the component')
    component_template = TextField('Component Template', 
                                  help='HTML template for the component')
    component_styles = TextField('Component Styles', 
                                help='CSS styles for the component')
    
    # Component Properties
    width = IntegerField('Width', default=100)
    height = IntegerField('Height', default=100)
    position_x = IntegerField('Position X', default=0)
    position_y = IntegerField('Position Y', default=0)
    
    # Component Dependencies
    depends_on_ids = One2ManyField('studio.component.dependency', 'component_id', 'Dependencies')
    required_addons = TextField('Required Addons', 
                               help='Comma-separated list of required addons')
    
    # Component Configuration
    config_data = TextField('Configuration Data', 
                           help='JSON configuration data')
    default_config = TextField('Default Configuration', 
                             help='Default configuration values')
    
    # Component Statistics
    usage_count = IntegerField('Usage Count', default=0)
    download_count = IntegerField('Download Count', default=0)
    rating = FloatField('Rating', digits=(3, 2), default=0.0)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'component_group_ids', 'Access Groups')
    
    def generate_component_code(self):
        """Generate component code"""
        if self.component_code:
            return self.component_code
        
        # Generate default code based on component type
        if self.component_type == 'widget':
            return self._generate_widget_code()
        elif self.component_type == 'field':
            return self._generate_field_code()
        elif self.component_type == 'button':
            return self._generate_button_code()
        elif self.component_type == 'action':
            return self._generate_action_code()
        elif self.component_type == 'chart':
            return self._generate_chart_code()
        else:
            return self._generate_default_code()
    
    def _generate_widget_code(self):
        """Generate widget code"""
        return f'''class {self._get_class_name()}(Widget):
    """{self.description or self.name}"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup widget UI"""
        # Widget setup code
        pass
    
    def update_data(self, data):
        """Update widget data"""
        # Data update code
        pass'''
    
    def _generate_field_code(self):
        """Generate field code"""
        return f'''class {self._get_class_name()}(Field):
    """{self.description or self.name}"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_field()
    
    def setup_field(self):
        """Setup field configuration"""
        # Field setup code
        pass'''
    
    def _generate_button_code(self):
        """Generate button code"""
        return f'''class {self._get_class_name()}(Button):
    """{self.description or self.name}"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_button()
    
    def setup_button(self):
        """Setup button configuration"""
        # Button setup code
        pass
    
    def on_click(self):
        """Handle button click"""
        # Click handler code
        pass'''
    
    def _generate_action_code(self):
        """Generate action code"""
        return f'''class {self._get_class_name()}(Action):
    """{self.description or self.name}"""
    
    def __init__(self):
        super().__init__()
        self.setup_action()
    
    def setup_action(self):
        """Setup action configuration"""
        # Action setup code
        pass
    
    def execute(self, context):
        """Execute action"""
        # Action execution code
        pass'''
    
    def _generate_chart_code(self):
        """Generate chart code"""
        return f'''class {self._get_class_name()}(Chart):
    """{self.description or self.name}"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_chart()
    
    def setup_chart(self):
        """Setup chart configuration"""
        # Chart setup code
        pass
    
    def update_chart(self, data):
        """Update chart data"""
        # Chart update code
        pass'''
    
    def _generate_default_code(self):
        """Generate default code"""
        return f'''class {self._get_class_name()}:
    """{self.description or self.name}"""
    
    def __init__(self):
        self.setup_component()
    
    def setup_component(self):
        """Setup component"""
        # Component setup code
        pass'''
    
    def _get_class_name(self):
        """Get Python class name from technical name"""
        parts = self.technical_name.split('_')
        return ''.join(word.capitalize() for word in parts)
    
    def deploy_component(self):
        """Deploy component to system"""
        try:
            # Generate component code
            component_code = self.generate_component_code()
            
            # Create component file
            component_file_path = f"addons/{self.project_id.code}/components/{self.technical_name}.py"
            
            # Write component file
            with open(component_file_path, 'w') as f:
                f.write(component_code)
            
            # Update statistics
            self.write({
                'usage_count': self.usage_count + 1,
                'is_published': True,
            })
            
            return True
            
        except Exception as e:
            raise e
    
    def get_component_summary(self):
        """Get component summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'component_type': self.component_type,
            'usage_count': self.usage_count,
            'download_count': self.download_count,
            'rating': self.rating,
            'is_published': self.is_published,
        }


class StudioComponentDependency(BaseModel, KidsClothingMixin):
    """Studio Component Dependency"""
    
    _name = 'studio.component.dependency'
    _description = 'Studio Component Dependency'
    
    component_id = Many2OneField('studio.component', 'Component', required=True)
    depends_on_component = CharField('Depends On Component', required=True, size=100)
    dependency_type = SelectionField([
        ('required', 'Required'),
        ('optional', 'Optional'),
        ('conflict', 'Conflict'),
    ], 'Dependency Type', default='required')
    version_requirement = CharField('Version Requirement', size=50)
    description = TextField('Description')