#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Form
===============================

Studio form management for custom form creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioForm(BaseModel, KidsClothingMixin):
    """Studio Form for Custom Form Creation"""
    
    _name = 'studio.form'
    _description = 'Studio Form'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Form Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    model_id = Many2OneField('studio.model', 'Model', required=True)
    
    # Form Configuration
    form_type = SelectionField([
        ('standard', 'Standard Form'),
        ('wizard', 'Wizard Form'),
        ('popup', 'Popup Form'),
        ('inline', 'Inline Form'),
        ('custom', 'Custom Form'),
    ], 'Form Type', default='standard')
    
    # Form Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_default = BooleanField('Default Form', default=False)
    
    # Form Layout
    layout_type = SelectionField([
        ('sheet', 'Sheet Layout'),
        ('group', 'Group Layout'),
        ('tab', 'Tab Layout'),
        ('accordion', 'Accordion Layout'),
        ('freeform', 'Freeform Layout'),
    ], 'Layout Type', default='sheet')
    
    # Form Content
    form_content = TextField('Form Content', 
                           help='XML content for the form')
    form_template = CharField('Form Template', size=100,
                             help='Template to inherit from')
    
    # Form Components
    field_ids = One2ManyField('studio.form.field', 'form_id', 'Fields')
    group_ids = One2ManyField('studio.form.group', 'form_id', 'Groups')
    tab_ids = One2ManyField('studio.form.tab', 'form_id', 'Tabs')
    button_ids = One2ManyField('studio.form.button', 'form_id', 'Buttons')
    
    # Form Validation
    validation_rules = TextField('Validation Rules', 
                               help='JavaScript validation rules')
    required_fields = TextField('Required Fields', 
                              help='Comma-separated list of required fields')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'form_group_ids', 'Access Groups')
    
    def generate_form_xml(self):
        """Generate XML form content"""
        if self.form_content:
            return self.form_content
        
        # Generate default form based on layout type
        if self.layout_type == 'sheet':
            return self._generate_sheet_form()
        elif self.layout_type == 'group':
            return self._generate_group_form()
        elif self.layout_type == 'tab':
            return self._generate_tab_form()
        elif self.layout_type == 'accordion':
            return self._generate_accordion_form()
        else:
            return self._generate_freeform_form()
    
    def _generate_sheet_form(self):
        """Generate sheet form XML"""
        xml_lines = []
        xml_lines.append('<form>')
        xml_lines.append('    <sheet>')
        
        # Add groups
        for group in self.group_ids:
            xml_lines.append(f'        <group string="{group.string}">')
            for field in group.field_ids:
                field_attrs = self._get_field_attrs(field)
                xml_lines.append(f'            <field name="{field.field_name}" {field_attrs}/>')
            xml_lines.append('        </group>')
        
        # Add buttons
        if self.button_ids:
            xml_lines.append('        <div class="oe_button_box">')
            for button in self.button_ids:
                button_attrs = self._get_button_attrs(button)
                xml_lines.append(f'            <button name="{button.method}" type="{button.type}" {button_attrs}>{button.string}</button>')
            xml_lines.append('        </div>')
        
        xml_lines.append('    </sheet>')
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _generate_group_form(self):
        """Generate group form XML"""
        xml_lines = []
        xml_lines.append('<form>')
        xml_lines.append('    <group>')
        
        for field in self.field_ids:
            field_attrs = self._get_field_attrs(field)
            xml_lines.append(f'        <field name="{field.field_name}" {field_attrs}/>')
        
        xml_lines.append('    </group>')
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _generate_tab_form(self):
        """Generate tab form XML"""
        xml_lines = []
        xml_lines.append('<form>')
        xml_lines.append('    <notebook>')
        
        for tab in self.tab_ids:
            xml_lines.append(f'        <page string="{tab.string}">')
            xml_lines.append('            <group>')
            for field in tab.field_ids:
                field_attrs = self._get_field_attrs(field)
                xml_lines.append(f'                <field name="{field.field_name}" {field_attrs}/>')
            xml_lines.append('            </group>')
            xml_lines.append('        </page>')
        
        xml_lines.append('    </notebook>')
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _generate_accordion_form(self):
        """Generate accordion form XML"""
        xml_lines = []
        xml_lines.append('<form>')
        xml_lines.append('    <div class="oe_accordion">')
        
        for group in self.group_ids:
            xml_lines.append(f'        <div class="oe_accordion_group" string="{group.string}">')
            xml_lines.append('            <group>')
            for field in group.field_ids:
                field_attrs = self._get_field_attrs(field)
                xml_lines.append(f'                <field name="{field.field_name}" {field_attrs}/>')
            xml_lines.append('            </group>')
            xml_lines.append('        </div>')
        
        xml_lines.append('    </div>')
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _generate_freeform_form(self):
        """Generate freeform form XML"""
        xml_lines = []
        xml_lines.append('<form>')
        
        for field in self.field_ids:
            field_attrs = self._get_field_attrs(field)
            xml_lines.append(f'    <field name="{field.field_name}" {field_attrs}/>')
        
        xml_lines.append('</form>')
        return '\n'.join(xml_lines)
    
    def _get_field_attrs(self, field):
        """Get field attributes"""
        attrs = []
        if field.string:
            attrs.append(f'string="{field.string}"')
        if field.invisible:
            attrs.append('invisible="1"')
        if field.readonly:
            attrs.append('readonly="1"')
        if field.required:
            attrs.append('required="1"')
        return " ".join(attrs)
    
    def _get_button_attrs(self, button):
        """Get button attributes"""
        attrs = []
        if button.class_name:
            attrs.append(f'class="{button.class_name}"')
        if button.confirm:
            attrs.append(f'confirm="{button.confirm}"')
        return " ".join(attrs)
    
    def deploy_form(self):
        """Deploy form to system"""
        try:
            # Generate form XML
            form_xml = self.generate_form_xml()
            
            # Create form file
            form_file_path = f"addons/{self.model_id.project_id.code}/views/{self.technical_name}.xml"
            
            # Generate complete XML with ocean tags
            complete_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<ocean>
    <ocean.ui.view
        id="{self.technical_name}"
        name="{self.name}"
        model="{self.model_id.technical_name}"
        type="form"
        arch="{form_xml}"/>
</ocean>'''
            
            # Write form file
            with open(form_file_path, 'w') as f:
                f.write(complete_xml)
            
            return True
            
        except Exception as e:
            raise e
    
    def get_form_summary(self):
        """Get form summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'form_type': self.form_type,
            'layout_type': self.layout_type,
            'model_name': self.model_id.technical_name,
            'is_default': self.is_default,
        }


class StudioFormField(BaseModel, KidsClothingMixin):
    """Studio Form Field"""
    
    _name = 'studio.form.field'
    _description = 'Studio Form Field'
    
    form_id = Many2OneField('studio.form', 'Form', required=True)
    field_name = CharField('Field Name', required=True, size=100)
    string = CharField('String', size=200)
    invisible = BooleanField('Invisible', default=False)
    readonly = BooleanField('Readonly', default=False)
    required = BooleanField('Required', default=False)
    sequence = IntegerField('Sequence', default=10)


class StudioFormGroup(BaseModel, KidsClothingMixin):
    """Studio Form Group"""
    
    _name = 'studio.form.group'
    _description = 'Studio Form Group'
    
    form_id = Many2OneField('studio.form', 'Form', required=True)
    name = CharField('Group Name', required=True, size=200)
    string = CharField('Group Label', required=True, size=200)
    sequence = IntegerField('Sequence', default=10)
    field_ids = One2ManyField('studio.form.field', 'group_id', 'Fields')


class StudioFormTab(BaseModel, KidsClothingMixin):
    """Studio Form Tab"""
    
    _name = 'studio.form.tab'
    _description = 'Studio Form Tab'
    
    form_id = Many2OneField('studio.form', 'Form', required=True)
    name = CharField('Tab Name', required=True, size=200)
    string = CharField('Tab Label', required=True, size=200)
    sequence = IntegerField('Sequence', default=10)
    field_ids = One2ManyField('studio.form.field', 'tab_id', 'Fields')


class StudioFormButton(BaseModel, KidsClothingMixin):
    """Studio Form Button"""
    
    _name = 'studio.form.button'
    _description = 'Studio Form Button'
    
    form_id = Many2OneField('studio.form', 'Form', required=True)
    name = CharField('Button Name', required=True, size=200)
    string = CharField('Button Label', required=True, size=200)
    type = SelectionField([
        ('object', 'Object'),
        ('action', 'Action'),
        ('workflow', 'Workflow'),
    ], 'Button Type', default='object')
    method = CharField('Method', size=100)
    class_name = CharField('CSS Class', size=100)
    confirm = CharField('Confirmation Message', size=200)
    sequence = IntegerField('Sequence', default=10)