# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField


class ProductAttribute(BaseModel):
    """Product Attribute - Product attributes like size, color, fabric"""
    
    _name = 'product.attribute'
    _description = 'Product Attribute'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Attribute Name', required=True, size=255)
    description = TextField(string='Description')
    code = CharField(string='Attribute Code', size=64)
    
    # Attribute Type
    attribute_type = SelectionField(string='Attribute Type', selection=[
        ('size', 'Size'),
        ('color', 'Color'),
        ('fabric', 'Fabric'),
        ('style', 'Style'),
        ('brand', 'Brand'),
        ('season', 'Season'),
        ('other', 'Other'),
    ], required=True)
    
    # Kids Clothing Specific
    age_group = SelectionField(string='Age Group', selection=[
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], default='all')
    
    gender = SelectionField(string='Gender', selection=[
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('all', 'All Genders'),
    ], default='all')
    
    # Attribute Values
    value_ids = One2ManyField('product.attribute.value', 'attribute_id', string='Attribute Values')
    value_count = IntegerField(string='Value Count', readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='draft')
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_value_count(self):
        """Compute total attribute value count"""
        for record in self:
            record.value_count = len(record.value_ids)
    
    def get_attribute_summary(self):
        """Get attribute summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'attribute_type': self.attribute_type,
            'age_group': self.age_group,
            'gender': self.gender,
            'value_count': self.value_count,
            'active': self.active,
            'state': self.state,
        }
    
    def get_attribute_values(self):
        """Get all attribute values"""
        return self.value_ids
    
    def get_values_by_type(self, value_type):
        """Get attribute values filtered by type"""
        return self.value_ids.filtered(lambda v: v.value_type == value_type)
    
    def activate_attribute(self):
        """Activate the attribute"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_attribute(self):
        """Deactivate the attribute"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def get_attribute_analytics_summary(self):
        """Get comprehensive attribute analytics summary"""
        return {
            'attribute_info': self.get_attribute_summary(),
            'values': [v.get_value_summary() for v in self.value_ids],
            'performance': {
                'value_count': self.value_count,
                'active_values': len(self.value_ids.filtered(lambda v: v.active)),
            },
        }


class ProductAttributeValue(BaseModel):
    """Product Attribute Value - Specific values for attributes"""
    
    _name = 'product.attribute.value'
    _description = 'Product Attribute Value'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Value Name', required=True, size=255)
    description = TextField(string='Description')
    code = CharField(string='Value Code', size=64)
    
    # Attribute
    attribute_id = Many2OneField('product.attribute', string='Attribute', required=True, ondelete='cascade')
    
    # Value Type
    value_type = SelectionField(string='Value Type', selection=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('color', 'Color'),
        ('image', 'Image'),
        ('other', 'Other'),
    ], default='text')
    
    # Value Data
    value_text = CharField(string='Text Value', size=255)
    value_number = FloatField(string='Number Value', digits=(16, 2))
    value_color = CharField(string='Color Value', size=7)  # Hex color code
    value_image = ImageField(string='Value Image', max_width=512, max_height=512)
    
    # Kids Clothing Specific
    age_group = SelectionField(string='Age Group', selection=[
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], default='all')
    
    gender = SelectionField(string='Gender', selection=[
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('all', 'All Genders'),
    ], default='all')
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='draft')
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def get_value_summary(self):
        """Get value summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'attribute': self.attribute_id.name if self.attribute_id else '',
            'value_type': self.value_type,
            'value_text': self.value_text,
            'value_number': self.value_number,
            'value_color': self.value_color,
            'age_group': self.age_group,
            'gender': self.gender,
            'active': self.active,
            'state': self.state,
        }
    
    def get_value_data(self):
        """Get the actual value data based on type"""
        if self.value_type == 'text':
            return self.value_text
        elif self.value_type == 'number':
            return self.value_number
        elif self.value_type == 'color':
            return self.value_color
        elif self.value_type == 'image':
            return self.value_image
        else:
            return self.value_text
    
    def activate_value(self):
        """Activate the value"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_value(self):
        """Deactivate the value"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def get_value_analytics_summary(self):
        """Get comprehensive value analytics summary"""
        return {
            'value_info': self.get_value_summary(),
            'value_data': self.get_value_data(),
            'performance': {
                'active': self.active,
                'state': self.state,
            },
        }