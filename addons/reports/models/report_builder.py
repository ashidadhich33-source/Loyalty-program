#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Report Builder Model
=======================================

Custom report builder for creating reports without coding.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class ReportBuilder(BaseModel, KidsClothingMixin):
    """Report Builder Model"""
    
    _name = 'report.builder'
    _description = 'Report Builder'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Report Name', required=True, size=200)
    description = TextField('Description')
    user_id = Many2OneField('users.user', 'Created By', required=True)
    
    # Report Configuration
    report_type = SelectionField([
        ('list', 'List Report'),
        ('pivot', 'Pivot Table'),
        ('graph', 'Graph/Chart'),
        ('summary', 'Summary Report'),
    ], 'Report Type', required=True, default='list')
    
    # Data Source
    model_name = CharField('Model Name', required=True, size=100)
    domain = TextField('Domain', help='Search domain')
    
    # Fields Configuration
    field_ids = One2ManyField('report.builder.field', 'builder_id', 'Fields')
    group_by_ids = One2ManyField('report.builder.group', 'builder_id', 'Group By')
    filter_ids = One2ManyField('report.builder.filter', 'builder_id', 'Filters')
    
    # Display Configuration
    limit = IntegerField('Record Limit', default=100)
    order_by = CharField('Order By', size=200)
    
    # Chart Configuration (for graph reports)
    chart_type = SelectionField([
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
    ], 'Chart Type')
    
    chart_x_axis = CharField('X Axis Field', size=100)
    chart_y_axis = CharField('Y Axis Field', size=100)
    chart_group_by = CharField('Group By Field', size=100)
    
    # Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], 'Status', default='draft')
    
    # Sharing
    is_public = BooleanField('Public Report', default=False)
    shared_with_ids = One2ManyField('users.user', 'shared_report_ids', 'Shared With')
    
    # Generated Report
    generated_template_id = Many2OneField('report.template', 'Generated Template')
    
    def generate_report_template(self):
        """Generate report template from builder configuration"""
        try:
            # Create report template
            template = self.env['report.template'].create({
                'name': self.name,
                'code': f"builder_{self.id}",
                'description': self.description,
                'category_id': self._get_default_category().id,
                'report_type': 'custom',
                'model_name': self.model_name,
                'view_type': self.report_type,
                'python_code': self._generate_python_code(),
                'default_filters': self.domain,
            })
            
            # Update builder with generated template
            self.write({'generated_template_id': template.id})
            
            return template
            
        except Exception as e:
            raise e
    
    def _get_default_category(self):
        """Get default report category"""
        category = self.env['report.category'].search([('code', '=', 'custom')], limit=1)
        if not category:
            category = self.env['report.category'].create({
                'name': 'Custom Reports',
                'code': 'custom',
                'description': 'User-created custom reports',
            })
        return category
    
    def _generate_python_code(self):
        """Generate Python code for the report"""
        code_lines = [
            "# Generated report code",
            "model = env['{}']".format(self.model_name),
            "",
            "# Apply domain",
            "domain = {}".format(self.domain or '[]'),
            "records = model.search(domain)",
            "",
            "# Apply limit",
            "if {}:".format(self.limit),
            "    records = records[:{}]".format(self.limit),
            "",
            "# Apply ordering",
            "if '{}':".format(self.order_by or ''),
            "    records = records.sorted('{}')".format(self.order_by or 'id'),
            "",
            "# Prepare data based on report type",
        ]
        
        if self.report_type == 'list':
            code_lines.extend([
                "# List report data",
                "data = []",
                "for record in records:",
                "    row = {}",
            ])
            
            # Add field mappings
            for field in self.field_ids:
                code_lines.append(f"    row['{field.field_name}'] = record.{field.field_name}")
            
            code_lines.extend([
                "    data.append(row)",
                "",
                "result = {",
                "    'records': data,",
                "    'total_count': len(data),",
                "    'model': '{}',".format(self.model_name),
                "}",
            ])
            
        elif self.report_type == 'pivot':
            code_lines.extend([
                "# Pivot table data",
                "pivot_data = {}",
                "for record in records:",
                "    # Group by fields",
                "    group_key = tuple()",
                "    for group_field in {}:".format([g.field_name for g in self.group_by_ids]),
                "        group_key += (getattr(record, group_field, ''),)",
                "    ",
                "    if group_key not in pivot_data:",
                "        pivot_data[group_key] = {}",
                "    ",
                "    # Aggregate data",
                "    for field in {}:".format([f.field_name for f in self.field_ids]),
                "        value = getattr(record, field.field_name, 0)",
                "        if field.field_name not in pivot_data[group_key]:",
                "            pivot_data[group_key][field.field_name] = 0",
                "        pivot_data[group_key][field.field_name] += value",
                "",
                "result = {",
                "    'pivot_data': pivot_data,",
                "    'group_fields': {},".format([g.field_name for g in self.group_by_ids]),
                "    'value_fields': {},".format([f.field_name for f in self.field_ids]),
                "}",
            ])
            
        elif self.report_type == 'graph':
            code_lines.extend([
                "# Graph data",
                "chart_data = {}",
                "for record in records:",
                "    x_value = getattr(record, '{}', '')".format(self.chart_x_axis or 'id'),
                "    y_value = getattr(record, '{}', 0)".format(self.chart_y_axis or 'id'),
                "    ",
                "    if x_value not in chart_data:",
                "        chart_data[x_value] = 0",
                "    chart_data[x_value] += y_value",
                "",
                "result = {",
                "    'chart_data': chart_data,",
                "    'chart_type': '{}',".format(self.chart_type),
                "    'x_axis': '{}',".format(self.chart_x_axis),
                "    'y_axis': '{}',".format(self.chart_y_axis),
                "}",
            ])
        
        return '\n'.join(code_lines)
    
    def execute_report(self, filters=None):
        """Execute the built report"""
        if not self.generated_template_id:
            self.generate_report_template()
        
        return self.generated_template_id.generate_report(filters)
    
    def publish_report(self):
        """Publish the report"""
        if not self.generated_template_id:
            self.generate_report_template()
        
        self.write({'status': 'published'})
    
    def archive_report(self):
        """Archive the report"""
        self.write({'status': 'archived'})
    
    def duplicate_report(self, new_name=None):
        """Duplicate the report"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_builder = self.create({
            'name': new_name,
            'description': self.description,
            'user_id': self.user_id.id,
            'report_type': self.report_type,
            'model_name': self.model_name,
            'domain': self.domain,
            'limit': self.limit,
            'order_by': self.order_by,
            'chart_type': self.chart_type,
            'chart_x_axis': self.chart_x_axis,
            'chart_y_axis': self.chart_y_axis,
            'chart_group_by': self.chart_group_by,
            'status': 'draft',
        })
        
        # Duplicate fields
        for field in self.field_ids:
            field.create({
                'builder_id': new_builder.id,
                'field_name': field.field_name,
                'field_label': field.field_label,
                'field_type': field.field_type,
                'aggregation': field.aggregation,
                'sequence': field.sequence,
            })
        
        # Duplicate groups
        for group in self.group_by_ids:
            group.create({
                'builder_id': new_builder.id,
                'field_name': group.field_name,
                'field_label': group.field_label,
                'sequence': group.sequence,
            })
        
        # Duplicate filters
        for filter_item in self.filter_ids:
            filter_item.create({
                'builder_id': new_builder.id,
                'field_name': filter_item.field_name,
                'field_label': filter_item.field_label,
                'operator': filter_item.operator,
                'value': filter_item.value,
                'sequence': filter_item.sequence,
            })
        
        return new_builder


class ReportBuilderField(BaseModel, KidsClothingMixin):
    """Report Builder Field Model"""
    
    _name = 'report.builder.field'
    _description = 'Report Builder Field'
    _order = 'sequence'
    
    builder_id = Many2OneField('report.builder', 'Report Builder', required=True)
    field_name = CharField('Field Name', required=True, size=100)
    field_label = CharField('Field Label', size=200)
    field_type = SelectionField([
        ('char', 'Text'),
        ('text', 'Long Text'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('selection', 'Selection'),
        ('many2one', 'Many2One'),
        ('one2many', 'One2Many'),
        ('many2many', 'Many2Many'),
    ], 'Field Type')
    
    aggregation = SelectionField([
        ('sum', 'Sum'),
        ('avg', 'Average'),
        ('count', 'Count'),
        ('min', 'Minimum'),
        ('max', 'Maximum'),
    ], 'Aggregation')
    
    sequence = IntegerField('Sequence', default=10)


class ReportBuilderGroup(BaseModel, KidsClothingMixin):
    """Report Builder Group Model"""
    
    _name = 'report.builder.group'
    _description = 'Report Builder Group'
    _order = 'sequence'
    
    builder_id = Many2OneField('report.builder', 'Report Builder', required=True)
    field_name = CharField('Field Name', required=True, size=100)
    field_label = CharField('Field Label', size=200)
    sequence = IntegerField('Sequence', default=10)


class ReportBuilderFilter(BaseModel, KidsClothingMixin):
    """Report Builder Filter Model"""
    
    _name = 'report.builder.filter'
    _description = 'Report Builder Filter'
    _order = 'sequence'
    
    builder_id = Many2OneField('report.builder', 'Report Builder', required=True)
    field_name = CharField('Field Name', required=True, size=100)
    field_label = CharField('Field Label', size=200)
    operator = SelectionField([
        ('=', 'Equal'),
        ('!=', 'Not Equal'),
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('>=', 'Greater or Equal'),
        ('<=', 'Less or Equal'),
        ('like', 'Contains'),
        ('ilike', 'Contains (Case Insensitive)'),
        ('in', 'In'),
        ('not in', 'Not In'),
        ('between', 'Between'),
    ], 'Operator', required=True)
    value = CharField('Value', size=500)
    sequence = IntegerField('Sequence', default=10)