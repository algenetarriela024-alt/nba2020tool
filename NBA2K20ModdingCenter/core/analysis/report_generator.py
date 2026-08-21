"""
Report Generator for NBA 2K20 Modding Center.
Generates analysis reports in JSON and TXT formats.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any


class ReportGenerator:
    """Generator for analysis reports."""
    
    def __init__(self, obb_data, workspace_path: str):
        self.obb_data = obb_data
        self.workspace_path = workspace_path
        self.reports_dir = os.path.join(workspace_path, "reports")
        
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_all_reports(self):
        """Generate all analysis reports."""
        
        self.generate_obb_report()
        self.generate_iff_report()
        self.generate_resources_report()
        self.generate_textures_report()
        self.generate_models_report()
        self.generate_database_report()
        self.generate_summary_report()
    
    def generate_obb_report(self):
        """Generate OBB analysis report."""
        
        report = {
            'report_type': 'OBB Analysis',
            'generated_at': datetime.now().isoformat(),
            'file_path': self.obb_data.file_path if hasattr(self.obb_data, 'file_path') else 'Unknown',
            'file_size': self.obb_data.file_size if hasattr(self.obb_data, 'file_size') else 0,
            'total_files': len(self.obb_data.files) if hasattr(self.obb_data, 'files') else 0,
            'iff_count': len(self.obb_data.iff_files) if hasattr(self.obb_data, 'iff_files') else 0,
            'resource_count': len(self.obb_data.resources) if hasattr(self.obb_data, 'resources') else 0,
        }
        
        self._save_json_report('obb_report.json', report)
        self._save_txt_report('obb_report.txt', self._format_obb_report(report))
    
    def _format_obb_report(self, report: Dict) -> str:
        """Format OBB report as text."""
        
        lines = [
            "=" * 60,
            "NBA 2K20 MOBILE MODDING CENTER",
            "OBB Analysis Report",
            "=" * 60,
            "",
            f"Generated: {report['generated_at']}",
            f"File: {report['file_path']}",
            f"Size: {self._format_size(report['file_size'])}",
            "",
            "SUMMARY",
            "-" * 40,
            f"Total Files: {report['total_files']}",
            f"IFF Files: {report['iff_count']}",
            f"Resources: {report['resource_count']}",
            "",
            "=" * 60,
        ]
        
        return "\n".join(lines)
    
    def generate_iff_report(self):
        """Generate IFF files report."""
        
        iff_files = []
        if hasattr(self.obb_data, 'iff_files'):
            iff_files = self.obb_data.iff_files
        
        report = {
            'report_type': 'IFF Files',
            'generated_at': datetime.now().isoformat(),
            'count': len(iff_files),
            'files': iff_files,
        }
        
        self._save_json_report('iff_report.json', report)
    
    def generate_resources_report(self):
        """Generate resources report."""
        
        resources = []
        if hasattr(self.obb_data, 'resources'):
            resources = self.obb_data.resources
        
        report = {
            'report_type': 'Resources',
            'generated_at': datetime.now().isoformat(),
            'count': len(resources),
            'resources': resources,
        }
        
        self._save_json_report('resources_report.json', report)
    
    def generate_textures_report(self):
        """Generate textures report."""
        
        textures = []
        if hasattr(self.obb_data, 'textures'):
            textures = self.obb_data.textures
        
        report = {
            'report_type': 'Textures',
            'generated_at': datetime.now().isoformat(),
            'count': len(textures),
            'textures': textures,
        }
        
        self._save_json_report('textures_report.json', report)
    
    def generate_models_report(self):
        """Generate models report."""
        
        models = []
        if hasattr(self.obb_data, 'models'):
            models = self.obb_data.models
        
        report = {
            'report_type': 'Models',
            'generated_at': datetime.now().isoformat(),
            'count': len(models),
            'models': models,
        }
        
        self._save_json_report('models_report.json', report)
    
    def generate_database_report(self):
        """Generate database report."""
        
        report = {
            'report_type': 'Database',
            'generated_at': datetime.now().isoformat(),
            'players': self.obb_data.players if hasattr(self.obb_data, 'players') else [],
            'teams': self.obb_data.teams if hasattr(self.obb_data, 'teams') else [],
            'headshapes': self.obb_data.headshapes if hasattr(self.obb_data, 'headshapes') else [],
        }
        
        self._save_json_report('database_report.json', report)
    
    def generate_summary_report(self):
        """Generate summary report."""
        
        summary = {
            'report_type': 'Summary',
            'generated_at': datetime.now().isoformat(),
            'obb_file': self.obb_data.file_path if hasattr(self.obb_data, 'file_path') else 'Unknown',
            'statistics': {
                'total_files': len(self.obb_data.files) if hasattr(self.obb_data, 'files') else 0,
                'iff_files': len(self.obb_data.iff_files) if hasattr(self.obb_data, 'iff_files') else 0,
                'resources': len(self.obb_data.resources) if hasattr(self.obb_data, 'resources') else 0,
                'textures': len(self.obb_data.textures) if hasattr(self.obb_data, 'textures') else 0,
                'models': len(self.obb_data.models) if hasattr(self.obb_data, 'models') else 0,
                'players': len(self.obb_data.players) if hasattr(self.obb_data, 'players') else 0,
                'teams': len(self.obb_data.teams) if hasattr(self.obb_data, 'teams') else 0,
            },
        }
        
        self._save_json_report('summary_report.json', summary)
        self._save_txt_report('summary_report.txt', self._format_summary_report(summary))
    
    def _format_summary_report(self, report: Dict) -> str:
        """Format summary report as text."""
        
        stats = report.get('statistics', {})
        
        lines = [
            "=" * 60,
            "NBA 2K20 MOBILE MODDING CENTER",
            "Analysis Summary",
            "=" * 60,
            "",
            f"Generated: {report['generated_at']}",
            f"OBB File: {report['obb_file']}",
            "",
            "STATISTICS",
            "-" * 40,
            f"Total Files: {stats.get('total_files', 0)}",
            f"IFF Files: {stats.get('iff_files', 0)}",
            f"Resources: {stats.get('resources', 0)}",
            f"Textures: {stats.get('textures', 0)}",
            f"Models: {stats.get('models', 0)}",
            f"Players: {stats.get('players', 0)}",
            f"Teams: {stats.get('teams', 0)}",
            "",
            "=" * 60,
        ]
        
        return "\n".join(lines)
    
    def _save_json_report(self, filename: str, data: Dict):
        """Save report as JSON."""
        
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _save_txt_report(self, filename: str, content: str):
        """Save report as text."""
        
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
    
    def _format_size(self, size: int) -> str:
        """Format file size."""
        
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
