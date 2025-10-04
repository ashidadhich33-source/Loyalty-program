#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Report Category Model
=========================================

Report category management for organizing reports.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, One2ManyField
from addons.core_base.models.base_mixins import KidsClothingMixin


class ReportCategory(BaseModel, KidsClothingMixin):
    """Report Category Model"""
    
    _name = 'report.category'
    _description = 'Report Category'
    _order = 'sequence, name'
    
    name = CharField('Category Name', required=True, size=100)
    code = CharField('Category Code', required=True, size=20)
    description = TextField('Description')
    sequence = CharField('Sequence', default=10)
    parent_id = CharField('Parent Category', size=20)
    child_ids = One2ManyField('report.category', 'parent_id', 'Child Categories')
    active = BooleanField('Active', default=True)
    icon = CharField('Icon', size=50, help='Font Awesome icon class')
    color = CharField('Color', size=20, help='Hex color code')
    
    # Report relationships
    report_ids = One2ManyField('report.template', 'category_id', 'Reports')
    
    def get_category_path(self):
        """Get full category path"""
        path = [self.name]
        if self.parent_id:
            parent = self.env['report.category'].browse([self.parent_id])
            if parent:
                path = parent.get_category_path() + path
        return ' / '.join(path)
    
    def get_all_children(self):
        """Get all child categories recursively"""
        children = []
        for child in self.child_ids:
            children.append(child)
            children.extend(child.get_all_children())
        return children