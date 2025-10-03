# -*- coding: utf-8 -*-
"""
Ocean ERP - UI Framework
========================

Custom UI framework for Ocean ERP system.
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class OceanUIView:
    """Ocean ERP UI View"""
    
    def __init__(self, name: str, model: str, arch: str, type: str = 'form'):
        self.name = name
        self.model = model
        self.arch = arch
        self.type = type
        
    def render(self, context: Dict[str, Any] = None):
        """Render the view"""
        if context is None:
            context = {}
        return self.arch

class OceanAction:
    """Ocean ERP Action"""
    
    def __init__(self, name: str, res_model: str, view_mode: str = 'tree,form', **kwargs):
        self.name = name
        self.res_model = res_model
        self.view_mode = view_mode
        self.kwargs = kwargs
        
    def execute(self, context: Dict[str, Any] = None):
        """Execute the action"""
        if context is None:
            context = {}
        return {
            'name': self.name,
            'model': self.res_model,
            'view_mode': self.view_mode,
            **self.kwargs
        }

class OceanMenu:
    """Ocean ERP Menu"""
    
    def __init__(self, name: str, sequence: int = 10, parent: str = None, action: str = None, **kwargs):
        self.name = name
        self.sequence = sequence
        self.parent = parent
        self.action = action
        self.kwargs = kwargs
        
    def render(self, context: Dict[str, Any] = None):
        """Render the menu"""
        if context is None:
            context = {}
        return {
            'name': self.name,
            'sequence': self.sequence,
            'parent': self.parent,
            'action': self.action,
            **self.kwargs
        }

class OceanGroup:
    """Ocean ERP Group"""
    
    def __init__(self, name: str, category: str = None, comment: str = None):
        self.name = name
        self.category = category
        self.comment = comment
        
    def render(self, context: Dict[str, Any] = None):
        """Render the group"""
        if context is None:
            context = {}
        return {
            'name': self.name,
            'category': self.category,
            'comment': self.comment
        }