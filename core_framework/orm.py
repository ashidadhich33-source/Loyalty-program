#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - ORM Manager
==============================

Custom ORM system similar to Odoo's ORM for the standalone ERP system.
"""

import logging
from typing import Dict, List, Any, Optional, Type
from abc import ABC, abstractmethod
from datetime import datetime
import json

class Field:
    """Base field class for ORM"""
    
    def __init__(self, string: str = None, required: bool = False, 
                 default: Any = None, help: str = None, **kwargs):
        self.string = string
        self.required = required
        self.default = default
        self.help = help
        self.kwargs = kwargs

class CharField(Field):
    """Character field"""
    def __init__(self, size: int = 255, **kwargs):
        super().__init__(**kwargs)
        self.size = size

class TextField(Field):
    """Text field"""
    pass

class IntegerField(Field):
    """Integer field"""
    pass

class FloatField(Field):
    """Float field"""
    pass

class BooleanField(Field):
    """Boolean field"""
    pass

class DateField(Field):
    """Date field"""
    pass

class DateTimeField(Field):
    """DateTime field"""
    pass

class Many2OneField(Field):
    """Many2One relationship field"""
    def __init__(self, comodel_name: str, **kwargs):
        super().__init__(**kwargs)
        self.comodel_name = comodel_name

class One2ManyField(Field):
    """One2Many relationship field"""
    def __init__(self, comodel_name: str, inverse_name: str, **kwargs):
        super().__init__(**kwargs)
        self.comodel_name = comodel_name
        self.inverse_name = inverse_name

class Many2ManyField(Field):
    """Many2Many relationship field"""
    def __init__(self, comodel_name: str, **kwargs):
        super().__init__(**kwargs)
        self.comodel_name = comodel_name

class BaseModel(ABC):
    """Base model class for ORM"""
    
    _name = None
    _description = None
    _table = None
    _fields = {}
    _fields_definitions = {}
    
    def __init__(self, env, cr=None, uid=None, context=None):
        self.env = env
        self.cr = cr
        self.uid = uid
        self.context = context or {}
        self._ids = []
        self._records = []
        
    @classmethod
    def _get_fields(cls):
        """Get model fields"""
        if not cls._fields_definitions:
            cls._fields_definitions = {}
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                if isinstance(attr, Field):
                    cls._fields_definitions[attr_name] = attr
        return cls._fields_definitions
    
    @classmethod
    def _get_table_name(cls):
        """Get table name for model"""
        if cls._table:
            return cls._table
        return cls._name.replace('.', '_')
    
    def create(self, vals_list):
        """Create new records"""
        if not isinstance(vals_list, list):
            vals_list = [vals_list]
        
        created_ids = []
        for vals in vals_list:
            # Add default values
            vals = self._add_default_values(vals)
            
            # Create record in database
            record_id = self.env.db.insert_record(self._get_table_name(), vals)
            created_ids.append(record_id)
        
        # Return new recordset
        return self.browse(created_ids)
    
    def browse(self, ids):
        """Browse records by IDs"""
        if not isinstance(ids, list):
            ids = [ids]
        
        new_recordset = self.__class__(self.env, self.cr, self.uid, self.context)
        new_recordset._ids = ids
        return new_recordset
    
    def read(self, fields=None):
        """Read record data"""
        if not self._ids:
            return []
        
        # Get all fields if not specified
        if not fields:
            fields = list(self._get_fields().keys())
        
        # Add id field
        if 'id' not in fields:
            fields.insert(0, 'id')
        
        # Read from database
        results = []
        for record_id in self._ids:
            record_data = self.env.db.get_record(self._get_table_name(), record_id)
            if record_data:
                # Filter fields
                filtered_data = {field: record_data.get(field) for field in fields if field in record_data}
                results.append(filtered_data)
        
        return results
    
    def write(self, vals):
        """Write values to records"""
        if not self._ids:
            return True
        
        # Update each record
        for record_id in self._ids:
            self.env.db.update_record(self._get_table_name(), record_id, vals)
        
        return True
    
    def unlink(self):
        """Delete records"""
        if not self._ids:
            return True
        
        # Delete each record
        for record_id in self._ids:
            self.env.db.delete_record(self._get_table_name(), record_id)
        
        return True
    
    def search(self, domain=None, limit=None, offset=None, order=None):
        """Search records"""
        if not domain:
            domain = []
        
        # Convert domain to SQL filters
        filters = self._domain_to_filters(domain)
        
        # Search in database
        results = self.env.db.search_records(
            self._get_table_name(), 
            filters, 
            limit, 
            offset
        )
        
        # Get IDs
        ids = [record['id'] for record in results]
        
        # Return recordset
        return self.browse(ids)
    
    def _domain_to_filters(self, domain):
        """Convert domain to database filters"""
        filters = {}
        i = 0
        while i < len(domain):
            if i + 2 < len(domain):
                field, operator, value = domain[i], domain[i+1], domain[i+2]
                if operator == '=':
                    filters[field] = value
                elif operator == '!=':
                    # Handle not equal in search_records method
                    pass
                elif operator == 'in':
                    # Handle in operator
                    pass
                elif operator == 'not in':
                    # Handle not in operator
                    pass
                i += 3
            else:
                i += 1
        
        return filters
    
    def _add_default_values(self, vals):
        """Add default values to vals"""
        fields = self._get_fields()
        for field_name, field_def in fields.items():
            if field_name not in vals and field_def.default is not None:
                if callable(field_def.default):
                    vals[field_name] = field_def.default()
                else:
                    vals[field_name] = field_def.default
        
        # Add create_date and write_date
        now = datetime.now()
        if 'create_date' not in vals:
            vals['create_date'] = now
        if 'write_date' not in vals:
            vals['write_date'] = now
        
        return vals
    
    def __getitem__(self, key):
        """Get record by index"""
        if isinstance(key, int):
            if 0 <= key < len(self._ids):
                return self.browse([self._ids[key]])
        elif isinstance(key, slice):
            return self.browse(self._ids[key])
        raise IndexError("Record index out of range")
    
    def __len__(self):
        """Get number of records"""
        return len(self._ids)
    
    def __iter__(self):
        """Iterate over records"""
        for i in range(len(self._ids)):
            yield self[i]

class ORMManager:
    """ORM Manager for ERP System"""
    
    def __init__(self, config):
        """Initialize ORM manager"""
        self.config = config
        self.models = {}
        self.logger = logging.getLogger('ERP.ORM')
        
    def initialize(self):
        """Initialize ORM"""
        try:
            self.logger.info("Initializing ORM...")
            
            # Register base models
            self._register_base_models()
            
            self.logger.info("ORM initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ORM: {e}")
            return False
    
    def _register_base_models(self):
        """Register base models"""
        # This will be populated by addons
        pass
    
    def register_model(self, model_class):
        """Register a model class"""
        if hasattr(model_class, '_name') and model_class._name:
            self.models[model_class._name] = model_class
            self.logger.info(f"Registered model: {model_class._name}")
    
    def get_model(self, model_name):
        """Get model class by name"""
        return self.models.get(model_name)
    
    def create_tables(self):
        """Create database tables for all models"""
        for model_name, model_class in self.models.items():
            self._create_model_table(model_class)
    
    def _create_model_table(self, model_class):
        """Create table for a model"""
        try:
            table_name = model_class._get_table_name()
            fields = model_class._get_fields()
            
            # Build column definitions
            columns = {'id': 'SERIAL PRIMARY KEY'}
            
            for field_name, field_def in fields.items():
                if isinstance(field_def, CharField):
                    columns[field_name] = f"VARCHAR({field_def.size})"
                elif isinstance(field_def, TextField):
                    columns[field_name] = "TEXT"
                elif isinstance(field_def, IntegerField):
                    columns[field_name] = "INTEGER"
                elif isinstance(field_def, FloatField):
                    columns[field_name] = "FLOAT"
                elif isinstance(field_def, BooleanField):
                    columns[field_name] = "BOOLEAN"
                elif isinstance(field_def, DateField):
                    columns[field_name] = "DATE"
                elif isinstance(field_def, DateTimeField):
                    columns[field_name] = "TIMESTAMP"
                elif isinstance(field_def, Many2OneField):
                    columns[field_name] = "INTEGER"
                else:
                    columns[field_name] = "VARCHAR(255)"
            
            # Add standard fields
            columns['create_date'] = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            columns['write_date'] = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            columns['create_uid'] = "INTEGER"
            columns['write_uid'] = "INTEGER"
            
            # Create table
            # This would use the database manager to create the table
            self.logger.info(f"Table structure defined for {table_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to create table for {model_class._name}: {e}")