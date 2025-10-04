#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Document Model
=================================

Document management for file storage and organization.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField,
    BinaryField, ImageField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class Document(BaseModel, KidsClothingMixin):
    """Document Model"""
    
    _name = 'document.document'
    _description = 'Document'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Document Name', required=True, size=200)
    description = TextField('Description')
    filename = CharField('Filename', size=255)
    
    # File Information
    file_data = BinaryField('File Data')
    file_size = IntegerField('File Size (bytes)', default=0)
    mime_type = CharField('MIME Type', size=100)
    file_extension = CharField('File Extension', size=10)
    
    # Document Properties
    document_type = SelectionField([
        ('image', 'Image'),
        ('pdf', 'PDF Document'),
        ('word', 'Word Document'),
        ('excel', 'Excel Spreadsheet'),
        ('powerpoint', 'PowerPoint Presentation'),
        ('text', 'Text File'),
        ('video', 'Video File'),
        ('audio', 'Audio File'),
        ('archive', 'Archive'),
        ('other', 'Other'),
    ], 'Document Type')
    
    # Organization
    folder_id = Many2OneField('document.folder', 'Folder')
    tag_ids = One2ManyField('document.tag', 'document_ids', 'Tags')
    category_id = Many2OneField('document.category', 'Category')
    
    # Version Control
    version = CharField('Version', size=20, default='1.0')
    version_ids = One2ManyField('document.version', 'document_id', 'Versions')
    is_latest_version = BooleanField('Latest Version', default=True)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'document_group_ids', 'Access Groups')
    is_public = BooleanField('Public Document', default=False)
    
    # Sharing
    share_ids = One2ManyField('document.share', 'document_id', 'Shared With')
    share_token = CharField('Share Token', size=100)
    
    # Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], 'Status', default='draft')
    
    # Workflow
    workflow_id = Many2OneField('workflow.workflow', 'Workflow')
    workflow_state = CharField('Workflow State', size=100)
    
    # Analytics
    view_count = IntegerField('View Count', default=0)
    download_count = IntegerField('Download Count', default=0)
    last_accessed = DateTimeField('Last Accessed')
    
    def upload_file(self, file_data, filename, mime_type):
        """Upload file to document"""
        try:
            import os
            
            # Calculate file size
            file_size = len(file_data) if file_data else 0
            
            # Get file extension
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Determine document type
            document_type = self._get_document_type(mime_type, file_extension)
            
            # Update document
            self.write({
                'file_data': file_data,
                'filename': filename,
                'file_size': file_size,
                'mime_type': mime_type,
                'file_extension': file_extension,
                'document_type': document_type,
            })
            
            # Create version record
            self._create_version_record(file_data, filename)
            
            return True
            
        except Exception as e:
            raise e
    
    def _get_document_type(self, mime_type, file_extension):
        """Determine document type from MIME type and extension"""
        if mime_type.startswith('image/'):
            return 'image'
        elif mime_type == 'application/pdf':
            return 'pdf'
        elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'word'
        elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return 'excel'
        elif mime_type in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
            return 'powerpoint'
        elif mime_type.startswith('text/'):
            return 'text'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type in ['application/zip', 'application/x-rar-compressed']:
            return 'archive'
        else:
            return 'other'
    
    def _create_version_record(self, file_data, filename):
        """Create version record"""
        version_data = {
            'document_id': self.id,
            'version': self.version,
            'file_data': file_data,
            'filename': filename,
            'file_size': len(file_data) if file_data else 0,
            'user_id': self.env.uid,
        }
        
        self.env['document.version'].create(version_data)
    
    def create_new_version(self, file_data, filename, mime_type):
        """Create new version of document"""
        try:
            # Increment version
            version_parts = self.version.split('.')
            if len(version_parts) == 2:
                major, minor = version_parts
                new_version = f"{major}.{int(minor) + 1}"
            else:
                new_version = f"{self.version}.1"
            
            # Mark current version as not latest
            self.write({'is_latest_version': False})
            
            # Create new document version
            new_document = self.create({
                'name': self.name,
                'description': self.description,
                'folder_id': self.folder_id.id,
                'tag_ids': [(6, 0, [tag.id for tag in self.tag_ids])],
                'category_id': self.category_id.id,
                'version': new_version,
                'user_id': self.user_id.id,
                'group_ids': [(6, 0, [group.id for group in self.group_ids])],
                'is_public': self.is_public,
                'status': self.status,
                'workflow_id': self.workflow_id.id,
                'workflow_state': self.workflow_state,
                'is_latest_version': True,
            })
            
            # Upload file to new version
            new_document.upload_file(file_data, filename, mime_type)
            
            return new_document
            
        except Exception as e:
            raise e
    
    def share_document(self, user_ids=None, group_ids=None, expires_at=None, access_level='read'):
        """Share document with users or groups"""
        try:
            share_data = {
                'document_id': self.id,
                'access_level': access_level,
                'expires_at': expires_at,
                'user_id': self.env.uid,
            }
            
            if user_ids:
                share_data['user_ids'] = [(6, 0, user_ids)]
            
            if group_ids:
                share_data['group_ids'] = [(6, 0, group_ids)]
            
            share_record = self.env['document.share'].create(share_data)
            
            # Generate share token
            import secrets
            share_token = secrets.token_urlsafe(32)
            share_record.write({'share_token': share_token})
            
            return share_record
            
        except Exception as e:
            raise e
    
    def download_document(self):
        """Download document"""
        try:
            # Update download count
            self.write({
                'download_count': self.download_count + 1,
                'last_accessed': self.env.cr.now(),
            })
            
            return {
                'file_data': self.file_data,
                'filename': self.filename,
                'mime_type': self.mime_type,
            }
            
        except Exception as e:
            raise e
    
    def view_document(self):
        """View document"""
        try:
            # Update view count
            self.write({
                'view_count': self.view_count + 1,
                'last_accessed': self.env.cr.now(),
            })
            
            return True
            
        except Exception as e:
            raise e
    
    def archive_document(self):
        """Archive document"""
        self.write({'status': 'archived'})
    
    def restore_document(self):
        """Restore archived document"""
        self.write({'status': 'draft'})
    
    def delete_document(self):
        """Delete document"""
        # Mark as deleted instead of actually deleting
        self.write({'active': False})
    
    def get_document_summary(self):
        """Get document summary"""
        return {
            'id': self.id,
            'name': self.name,
            'filename': self.filename,
            'document_type': self.document_type,
            'file_size': self.file_size,
            'version': self.version,
            'status': self.status,
            'view_count': self.view_count,
            'download_count': self.download_count,
            'create_date': self.create_date,
            'last_accessed': self.last_accessed,
        }