#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Document Tests
==================================

Test cases for document management functionality.
"""

import unittest
import tempfile
import os


class TestDocument(unittest.TestCase):
    """Test Document Model"""
    
    def setUp(self):
        """Set up test data"""
        self.env = None  # Would be initialized with test environment
        self.test_user = None
        self.test_folder = None
        self.test_file_data = b"Test file content"
        self.test_filename = "test_document.txt"
        self.test_mime_type = "text/plain"
    
    def test_document_creation(self):
        """Test document creation"""
        document_data = {
            'name': 'Test Document',
            'description': 'This is a test document',
            'user_id': self.test_user.id if self.test_user else 1,
            'status': 'draft',
        }
        
        # Create document
        document = self.env['document.document'].create(document_data)
        
        # Assertions
        self.assertEqual(document.name, 'Test Document')
        self.assertEqual(document.description, 'This is a test document')
        self.assertEqual(document.status, 'draft')
        self.assertEqual(document.version, '1.0')
        self.assertTrue(document.is_latest_version)
    
    def test_file_upload(self):
        """Test file upload"""
        document_data = {
            'name': 'Upload Test Document',
            'description': 'Testing file upload',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document and upload file
        document = self.env['document.document'].create(document_data)
        result = document.upload_file(self.test_file_data, self.test_filename, self.test_mime_type)
        
        # Assertions
        self.assertTrue(result)
        self.assertEqual(document.filename, self.test_filename)
        self.assertEqual(document.file_size, len(self.test_file_data))
        self.assertEqual(document.mime_type, self.test_mime_type)
        self.assertEqual(document.file_extension, '.txt')
        self.assertEqual(document.document_type, 'text')
    
    def test_document_type_detection(self):
        """Test document type detection"""
        test_cases = [
            ('image.jpg', 'image/jpeg', 'image'),
            ('document.pdf', 'application/pdf', 'pdf'),
            ('spreadsheet.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'excel'),
            ('presentation.pptx', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'powerpoint'),
            ('video.mp4', 'video/mp4', 'video'),
            ('audio.mp3', 'audio/mpeg', 'audio'),
            ('archive.zip', 'application/zip', 'archive'),
        ]
        
        for filename, mime_type, expected_type in test_cases:
            document_data = {
                'name': f'Test {expected_type.title()} Document',
                'user_id': self.test_user.id if self.test_user else 1,
            }
            
            document = self.env['document.document'].create(document_data)
            document.upload_file(b"test content", filename, mime_type)
            
            # Assertions
            self.assertEqual(document.document_type, expected_type)
    
    def test_version_creation(self):
        """Test document version creation"""
        document_data = {
            'name': 'Version Test Document',
            'description': 'Testing version creation',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document and upload initial file
        document = self.env['document.document'].create(document_data)
        document.upload_file(self.test_file_data, self.test_filename, self.test_mime_type)
        
        # Create new version
        new_file_data = b"Updated file content"
        new_filename = "test_document_v2.txt"
        new_document = document.create_new_version(new_file_data, new_filename, self.test_mime_type)
        
        # Assertions
        self.assertNotEqual(document.id, new_document.id)
        self.assertEqual(new_document.version, '1.1')
        self.assertTrue(new_document.is_latest_version)
        self.assertFalse(document.is_latest_version)
        self.assertEqual(new_document.filename, new_filename)
    
    def test_document_sharing(self):
        """Test document sharing"""
        document_data = {
            'name': 'Share Test Document',
            'description': 'Testing document sharing',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document
        document = self.env['document.document'].create(document_data)
        
        # Share document
        user_ids = [2, 3] if self.test_user else [1, 2]
        share_record = document.share_document(
            user_ids=user_ids,
            expires_at=None,
            access_level='read'
        )
        
        # Assertions
        self.assertIsNotNone(share_record)
        self.assertIsNotNone(share_record.share_token)
        self.assertEqual(share_record.access_level, 'read')
    
    def test_document_download(self):
        """Test document download"""
        document_data = {
            'name': 'Download Test Document',
            'description': 'Testing document download',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document and upload file
        document = self.env['document.document'].create(document_data)
        document.upload_file(self.test_file_data, self.test_filename, self.test_mime_type)
        
        # Download document
        download_result = document.download_document()
        
        # Assertions
        self.assertIn('file_data', download_result)
        self.assertIn('filename', download_result)
        self.assertIn('mime_type', download_result)
        self.assertEqual(download_result['filename'], self.test_filename)
        self.assertEqual(download_result['mime_type'], self.test_mime_type)
        self.assertEqual(document.download_count, 1)
    
    def test_document_view(self):
        """Test document viewing"""
        document_data = {
            'name': 'View Test Document',
            'description': 'Testing document viewing',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document
        document = self.env['document.document'].create(document_data)
        
        # View document
        result = document.view_document()
        
        # Assertions
        self.assertTrue(result)
        self.assertEqual(document.view_count, 1)
        self.assertIsNotNone(document.last_accessed)
    
    def test_document_archive(self):
        """Test document archiving"""
        document_data = {
            'name': 'Archive Test Document',
            'description': 'Testing document archiving',
            'user_id': self.test_user.id if self.test_user else 1,
            'status': 'published',
        }
        
        # Create document
        document = self.env['document.document'].create(document_data)
        
        # Archive document
        document.archive_document()
        
        # Assertions
        self.assertEqual(document.status, 'archived')
    
    def test_document_restore(self):
        """Test document restoration"""
        document_data = {
            'name': 'Restore Test Document',
            'description': 'Testing document restoration',
            'user_id': self.test_user.id if self.test_user else 1,
            'status': 'archived',
        }
        
        # Create archived document
        document = self.env['document.document'].create(document_data)
        
        # Restore document
        document.restore_document()
        
        # Assertions
        self.assertEqual(document.status, 'draft')
    
    def test_document_delete(self):
        """Test document deletion"""
        document_data = {
            'name': 'Delete Test Document',
            'description': 'Testing document deletion',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document
        document = self.env['document.document'].create(document_data)
        
        # Delete document
        document.delete_document()
        
        # Assertions
        self.assertFalse(document.active)
    
    def test_document_summary(self):
        """Test document summary"""
        document_data = {
            'name': 'Summary Test Document',
            'description': 'Testing document summary',
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create document and upload file
        document = self.env['document.document'].create(document_data)
        document.upload_file(self.test_file_data, self.test_filename, self.test_mime_type)
        
        # Get document summary
        summary = document.get_document_summary()
        
        # Assertions
        self.assertIn('id', summary)
        self.assertIn('name', summary)
        self.assertIn('filename', summary)
        self.assertIn('document_type', summary)
        self.assertIn('file_size', summary)
        self.assertIn('version', summary)
        self.assertIn('status', summary)
        self.assertIn('view_count', summary)
        self.assertIn('download_count', summary)
        self.assertEqual(summary['name'], 'Summary Test Document')


class TestDocumentVersion(unittest.TestCase):
    """Test Document Version Model"""
    
    def setUp(self):
        """Set up test data"""
        self.env = None  # Would be initialized with test environment
        self.test_user = None
        self.test_document = None
    
    def test_version_creation(self):
        """Test version creation"""
        version_data = {
            'document_id': self.test_document.id if self.test_document else 1,
            'version': '1.0',
            'file_data': b"Version 1.0 content",
            'filename': 'document_v1.txt',
            'file_size': 20,
            'user_id': self.test_user.id if self.test_user else 1,
        }
        
        # Create version
        version = self.env['document.version'].create(version_data)
        
        # Assertions
        self.assertEqual(version.version, '1.0')
        self.assertEqual(version.filename, 'document_v1.txt')
        self.assertEqual(version.file_size, 20)
    
    def test_version_comparison(self):
        """Test version comparison"""
        # Create multiple versions
        versions_data = [
            {'version': '1.0', 'filename': 'doc_v1.txt'},
            {'version': '1.1', 'filename': 'doc_v1.1.txt'},
            {'version': '2.0', 'filename': 'doc_v2.txt'},
        ]
        
        created_versions = []
        for version_data in versions_data:
            version_data.update({
                'document_id': self.test_document.id if self.test_document else 1,
                'file_data': b"test content",
                'file_size': 10,
                'user_id': self.test_user.id if self.test_user else 1,
            })
            version = self.env['document.version'].create(version_data)
            created_versions.append(version)
        
        # Test version ordering
        sorted_versions = sorted(created_versions, key=lambda v: v.version)
        
        # Assertions
        self.assertEqual(sorted_versions[0].version, '1.0')
        self.assertEqual(sorted_versions[1].version, '1.1')
        self.assertEqual(sorted_versions[2].version, '2.0')


if __name__ == '__main__':
    unittest.main()