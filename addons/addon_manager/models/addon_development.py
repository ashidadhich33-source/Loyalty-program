# -*- coding: utf-8 -*-
"""
Ocean ERP - Addon Development Models
==================================

Addon development models for Ocean ERP.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, SelectionField, FloatField
from typing import Dict, Any, Optional, List
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AddonDevelopment(BaseModel):
    """Addon Development model for Ocean ERP"""
    
    _name = 'addon.development'
    _description = 'Addon Development'
    _table = 'addon_development'
    
    # Basic fields
    name = CharField(
        string='Addon Name',
        size=255,
        required=True,
        help='Name of the addon'
    )
    
    technical_name = CharField(
        string='Technical Name',
        size=255,
        required=True,
        help='Technical name of the addon'
    )
    
    version = CharField(
        string='Version',
        size=50,
        default='1.0.0',
        help='Addon version'
    )
    
    description = TextField(
        string='Description',
        help='Description of the addon'
    )
    
    # Development status
    status = SelectionField(
        string='Development Status',
        selection=[
            ('planning', 'Planning'),
            ('development', 'Development'),
            ('testing', 'Testing'),
            ('stable', 'Stable'),
            ('deprecated', 'Deprecated'),
        ],
        default='planning',
        help='Development status'
    )
    
    progress = IntegerField(
        string='Progress (%)',
        default=0,
        help='Development progress percentage'
    )
    
    # Development team
    developer = CharField(
        string='Developer',
        size=255,
        help='Main developer'
    )
    
    team_members = TextField(
        string='Team Members',
        help='Development team members (JSON format)'
    )
    
    # Development timeline
    start_date = DateTimeField(
        string='Start Date',
        help='Development start date'
    )
    
    target_date = DateTimeField(
        string='Target Date',
        help='Target completion date'
    )
    
    completion_date = DateTimeField(
        string='Completion Date',
        help='Actual completion date'
    )
    
    # Development details
    features = TextField(
        string='Features',
        help='Planned features (JSON format)'
    )
    
    requirements = TextField(
        string='Requirements',
        help='Development requirements'
    )
    
    dependencies = TextField(
        string='Dependencies',
        help='Development dependencies (JSON format)'
    )
    
    # Development tools
    repository_url = CharField(
        string='Repository URL',
        size=255,
        help='Git repository URL'
    )
    
    documentation_url = CharField(
        string='Documentation URL',
        size=255,
        help='Documentation URL'
    )
    
    issue_tracker_url = CharField(
        string='Issue Tracker URL',
        size=255,
        help='Issue tracker URL'
    )
    
    # Development metrics
    lines_of_code = IntegerField(
        string='Lines of Code',
        default=0,
        help='Total lines of code'
    )
    
    test_coverage = FloatField(
        string='Test Coverage (%)',
        default=0.0,
        help='Test coverage percentage'
    )
    
    bugs_count = IntegerField(
        string='Bugs Count',
        default=0,
        help='Number of bugs'
    )
    
    features_count = IntegerField(
        string='Features Count',
        default=0,
        help='Number of features'
    )
    
    # Development notes
    notes = TextField(
        string='Development Notes',
        help='Development notes and comments'
    )
    
    changelog = TextField(
        string='Changelog',
        help='Development changelog'
    )
    
    # Development templates
    is_template = BooleanField(
        string='Template',
        default=False,
        help='Whether this is a development template'
    )
    
    template_type = SelectionField(
        string='Template Type',
        selection=[
            ('basic', 'Basic Addon'),
            ('model', 'Model Addon'),
            ('view', 'View Addon'),
            ('wizard', 'Wizard Addon'),
            ('report', 'Report Addon'),
            ('integration', 'Integration Addon'),
        ],
        help='Template type'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        if 'technical_name' not in vals and 'name' in vals:
            vals['technical_name'] = vals['name'].lower().replace(' ', '_')
        
        if 'start_date' not in vals:
            vals['start_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle updates"""
        result = super().write(vals)
        
        # Update completion date when status changes to stable
        if 'status' in vals and vals['status'] == 'stable':
            for addon in self:
                if not addon.completion_date:
                    addon.completion_date = datetime.now()
        
        return result
    
    def action_start_development(self):
        """Start development"""
        self.ensure_one()
        
        self.write({
            'status': 'development',
            'start_date': datetime.now()
        })
        return True
    
    def action_complete_development(self):
        """Complete development"""
        self.ensure_one()
        
        self.write({
            'status': 'stable',
            'progress': 100,
            'completion_date': datetime.now()
        })
        return True
    
    def action_create_template(self):
        """Create development template"""
        self.ensure_one()
        
        try:
            # This would create template files
            template_data = {
                'name': self.name,
                'technical_name': self.technical_name,
                'version': self.version,
                'description': self.description,
                'template_type': self.template_type,
                'features': self.get_features(),
                'dependencies': self.get_dependencies(),
            }
            
            # Create template files
            self._create_template_files(template_data)
            
            self.write({
                'is_template': True
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create template: {e}")
            return False
    
    def _create_template_files(self, template_data: Dict[str, Any]):
        """Create template files"""
        try:
            # Create addon directory structure
            addon_path = Path(f"addons/{template_data['technical_name']}")
            addon_path.mkdir(parents=True, exist_ok=True)
            
            # Create __manifest__.py
            manifest_content = self._generate_manifest(template_data)
            with open(addon_path / '__manifest__.py', 'w') as f:
                f.write(manifest_content)
            
            # Create __init__.py
            with open(addon_path / '__init__.py', 'w') as f:
                f.write("# -*- coding: utf-8 -*-\n")
            
            # Create models directory
            models_path = addon_path / 'models'
            models_path.mkdir(exist_ok=True)
            
            # Create models/__init__.py
            with open(models_path / '__init__.py', 'w') as f:
                f.write("# -*- coding: utf-8 -*-\n")
            
            # Create views directory
            views_path = addon_path / 'views'
            views_path.mkdir(exist_ok=True)
            
            # Create security directory
            security_path = addon_path / 'security'
            security_path.mkdir(exist_ok=True)
            
            # Create data directory
            data_path = addon_path / 'data'
            data_path.mkdir(exist_ok=True)
            
            # Create static directory
            static_path = addon_path / 'static'
            static_path.mkdir(exist_ok=True)
            
            logger.info(f"Created template files for {template_data['technical_name']}")
            
        except Exception as e:
            logger.error(f"Failed to create template files: {e}")
            raise
    
    def _generate_manifest(self, template_data: Dict[str, Any]) -> str:
        """Generate manifest file content"""
        manifest = f"""# -*- coding: utf-8 -*-
{{
    'name': '{template_data['name']}',
    'version': '{template_data['version']}',
    'category': 'Custom',
    'summary': '{template_data['description'][:100]}...',
    'description': \"\"\"
        {template_data['description']}
    \"\"\",
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'license': 'LGPL-3',
    'depends': {template_data.get('dependencies', [])},
    'data': [
        'security/ocean.model.access.csv',
        'views/menu.xml',
    ],
    'demo': [],
    'assets': {{
        'web.assets_backend': [],
    }},
    'installable': True,
    'application': False,
    'auto_install': False,
}}"""
        return manifest
    
    def get_features(self) -> List[Dict[str, Any]]:
        """Get planned features"""
        try:
            if self.features:
                return json.loads(self.features)
            return []
        except:
            return []
    
    def set_features(self, features: List[Dict[str, Any]]):
        """Set planned features"""
        self.ensure_one()
        
        self.write({
            'features': json.dumps(features),
            'features_count': len(features)
        })
        return True
    
    def get_dependencies(self) -> List[str]:
        """Get development dependencies"""
        try:
            if self.dependencies:
                return json.loads(self.dependencies)
            return []
        except:
            return []
    
    def set_dependencies(self, dependencies: List[str]):
        """Set development dependencies"""
        self.ensure_one()
        
        self.write({
            'dependencies': json.dumps(dependencies)
        })
        return True
    
    def get_team_members(self) -> List[Dict[str, Any]]:
        """Get team members"""
        try:
            if self.team_members:
                return json.loads(self.team_members)
            return []
        except:
            return []
    
    def set_team_members(self, team_members: List[Dict[str, Any]]):
        """Set team members"""
        self.ensure_one()
        
        self.write({
            'team_members': json.dumps(team_members)
        })
        return True
    
    @classmethod
    def get_active_development(cls):
        """Get active development projects"""
        return cls.search([('status', 'in', ['planning', 'development', 'testing'])])
    
    @classmethod
    def get_completed_projects(cls):
        """Get completed projects"""
        return cls.search([('status', '=', 'stable')])
    
    @classmethod
    def get_templates(cls):
        """Get development templates"""
        return cls.search([('is_template', '=', True)])