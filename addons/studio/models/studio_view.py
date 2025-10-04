#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio View
===============================

Studio view management for custom view creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioView(BaseModel, KidsClothingMixin):
    """Studio View for Custom View Creation"""
    
    _name = 'studio.view'
    _description = 'Studio View'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('View Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    model_id = Many2OneField('studio.model', 'Model', required=True)
    
    # View Configuration
    view_type = SelectionField([
        ('tree', 'List View'),
        ('form', 'Form View'),
        ('kanban', 'Kanban View'),
        ('calendar', 'Calendar View'),
        ('pivot', 'Pivot View'),
        ('graph', 'Graph View'),
        ('search', 'Search View'),
        ('qweb', 'QWeb View'),
    ], 'View Type', required=True)
    
    # View Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_default = BooleanField('Default View', default=False)
    
    # View Content
    arch_content = TextField('Architecture Content', 
                           help='XML content for the view')
    view_template = CharField('View Template', size=100,
                             help='Template to inherit from')
    
    # View Components
    field_ids = One2ManyField('studio.view.field', 'view_id', 'Fields')
    button_ids = One2ManyField('studio.view.button', 'view_id', 'Buttons')
    group_ids = One2ManyField('studio.view.group', 'view_id', 'Groups')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'view_group_ids', 'Access Groups')
    
    def generate_view_xml(self):
        """Generate XML view content"""
        if self.arch_content:
            return self.arch_content
        
        # Generate default view based on type
        if self.view_type == 'tree':
            return self._generate_tree_view()
        elif self.view_type == 'form':
            return self._generate_form_view()
        elif self.view_type == 'kanban':
            return self._generate_kanban_view()
        elif self.view_type == 'search':
            return self._generate_search_view()
        else:
            return self._generate_default_view()
    
    def _generate_tree_view(self):
        """Generate tree view XML"""
        xml_lines = []
        xml_lines.append('<tree>')
        
        for field in self.field_ids:
            field_attrs = []
            if field.string:
                field_attrs.append(f'string="{field.string}"')
            if field.invisible:
                field_attrs.append('invisible="1"')
            if field.readonly:
                field_attrs.append('readonly="1"')
            
            attrs_str = " ".join(field_attrs)
            xml_lines.append(f'    <field name="{field.field_name}" {attrs_str}/>')
        
        xml_lines.append('</tree>')
        return '\n'.join(xml_lines)
    
    def _generate_form_view(self):
        """Generate form view XML"""
        xml_lines = []
        xml_lines.append('<form>')
        xml_lines.append('    <sheet>')
        xml_lines.append('        <group>')
        
        for field in self.field_ids:
            field_attrs = []
            if field.string:
                field_attrs.append(f'string="{field.string}"')
            if field.invisible:
                field_attrs.append('invisible="1"')
            if field.readonly:
                field_attrs.append('readonly="1"')
            
            attrs_str = " ".join(field_attrs)
            xml_lines.append(f'            <field name="{field.field_name}" {attrs_str}/>')
        
        xml_lines.append('        </group>')
        xml_lines.append('    </sheet>')
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _generate_kanban_view(self):
        """Generate kanban view XML"""
        xml_lines = []
        xml_lines.append('<kanban>')
        xml_lines.append('    <field name="name"/>')
        xml_lines.append('    <templates>')
        xml_lines.append('        <t t-name="kanban-box">')
        xml_lines.append('            <div class="oe_kanban_card">')
        xml_lines.append('                <div class="oe_kanban_content">')
        xml_lines.append('                    <div class="o_kanban_record_title">')
        xml_lines.append('                        <field name="name"/>')
        xml_lines.append('                    </div>')
        xml_lines.append('                </div>')
        xml_lines.append('            </div>')
        xml_lines.append('        </t>')
        xml_lines.append('    </templates>')
        xml_lines.append('</kanban>')
        return '\n'.join(xml_lines)
    
    def _generate_search_view(self):
        """Generate search view XML"""
        xml_lines = []
        xml_lines.append('<search>')
        xml_lines.append('    <field name="name"/>')
        xml_lines.append('    <filter string="Active" name="active" domain="[(\'active\', \'=\', True)]"/>')
        xml_lines.append('    <group expand="0" string="Group By">')
        xml_lines.append('        <filter string="Created By" name="group_by_user" context="{\'group_by\': \'create_uid\'}"/>')
        xml_lines.append('    </group>')
        xml_lines.append('</search>')
        return '\n'.join(xml_lines)
    
    def _generate_default_view(self):
        """Generate default view XML"""
        return f'<{self.view_type}>\n    <field name="name"/>\n</{self.view_type}>'
    
    def deploy_view(self):
        """Deploy view to system"""
        try:
            # Generate view XML
            view_xml = self.generate_view_xml()
            
            # Create view file
            view_file_path = f"addons/{self.model_id.project_id.code}/views/{self.technical_name}.xml"
            
            # Generate complete XML with ocean tags
            complete_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<ocean>
    <ocean.ui.view
        id="{self.technical_name}"
        name="{self.name}"
        model="{self.model_id.technical_name}"
        type="{self.view_type}"
        arch="{view_xml}"/>
</ocean>'''
            
            # Write view file
            with open(view_file_path, 'w') as f:
                f.write(complete_xml)
            
            return True
            
        except Exception as e:
            raise e
    
    def get_view_summary(self):
        """Get view summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'view_type': self.view_type,
            'model_name': self.model_id.technical_name,
            'is_default': self.is_default,
        }


class StudioViewField(BaseModel, KidsClothingMixin):
    """Studio View Field"""
    
    _name = 'studio.view.field'
    _description = 'Studio View Field'
    
    view_id = Many2OneField('studio.view', 'View', required=True)
    field_name = CharField('Field Name', required=True, size=100)
    string = CharField('String', size=200)
    invisible = BooleanField('Invisible', default=False)
    readonly = BooleanField('Readonly', default=False)
    required = BooleanField('Required', default=False)
    sequence = IntegerField('Sequence', default=10)


class StudioViewButton(BaseModel, KidsClothingMixin):
    """Studio View Button"""
    
    _name = 'studio.view.button'
    _description = 'Studio View Button'
    
    view_id = Many2OneField('studio.view', 'View', required=True)
    name = CharField('Button Name', required=True, size=200)
    string = CharField('Button Label', required=True, size=200)
    type = SelectionField([
        ('object', 'Object'),
        ('action', 'Action'),
        ('workflow', 'Workflow'),
    ], 'Button Type', default='object')
    method = CharField('Method', size=100)
    action_id = Many2OneField('ocean.actions.act_window', 'Action')
    sequence = IntegerField('Sequence', default=10)


class StudioViewGroup(BaseModel, KidsClothingMixin):
    """Studio View Group"""
    
    _name = 'studio.view.group'
    _description = 'Studio View Group'
    
    view_id = Many2OneField('studio.view', 'View', required=True)
    name = CharField('Group Name', required=True, size=200)
    string = CharField('Group Label', required=True, size=200)
    sequence = IntegerField('Sequence', default=10)