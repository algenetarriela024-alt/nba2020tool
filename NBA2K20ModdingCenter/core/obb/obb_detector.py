"""
OBB Detection and Analysis Module

Detects:
- OBB file format
- Entry count
- Compression types present
- File types contained
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from .obb_reader import ObbParser, ObbEntry, EntryType, load_obb


class ObbDetector:
    """Detects and analyzes OBB file structure"""
    
    def __init__(self, obb_path: Path):
        self.obb_path = Path(obb_path)
        self.parser: Optional[ObbParser] = None
        self.analysis_result: Dict[str, Any] = {}
    
    def analyze(self) -> Dict[str, Any]:
        """Perform complete OBB analysis"""
        self.analysis_result = {
            'path': str(self.obb_path),
            'exists': self.obb_path.exists(),
            'size': 0,
            'entry_count': 0,
            'iff_files': [],
            'bin_resources': [],
            'other_files': [],
            'textures_detected': 0,
            'models_detected': 0,
            'audio_detected': 0,
            'database_detected': 0,
            'compression_types': set(),
            'status': 'unknown',
            'error': None
        }
        
        if not self.obb_path.exists():
            self.analysis_result['status'] = 'error'
            self.analysis_result['error'] = 'File does not exist'
            return self.analysis_result
        
        try:
            self.analysis_result['size'] = self.obb_path.stat().st_size
            
            # Load and parse OBB
            self.parser = load_obb(self.obb_path)
            
            if not self.parser:
                self.analysis_result['status'] = 'error'
                self.analysis_result['error'] = 'Failed to parse OBB file'
                return self.analysis_result
            
            self.analysis_result['entry_count'] = self.parser.entry_count
            
            # Categorize entries
            for entry in self.parser.get_entry_list():
                self._categorize_entry(entry)
            
            self.analysis_result['compression_types'] = list(self.analysis_result['compression_types'])
            self.analysis_result['status'] = 'success'
            
        except Exception as e:
            self.analysis_result['status'] = 'error'
            self.analysis_result['error'] = str(e)
        
        return self.analysis_result
    
    def _categorize_entry(self, entry: ObbEntry):
        """Categorize an entry by type"""
        # Track compression
        if entry.is_compressed:
            self.analysis_result['compression_types'].add('zlib' if entry.has_zlib_wrapper else 'raw')
        
        # Categorize by type
        if entry.entry_type == EntryType.IFF:
            self.analysis_result['iff_files'].append({
                'index': entry.index,
                'offset': entry.offset,
                'size': entry.decompressed_size,
                'compressed_size': entry.compressed_size,
                'hash': f'0x{entry.name_hash:08x}'
            })
        elif entry.entry_type == EntryType.BIN:
            self.analysis_result['bin_resources'].append({
                'index': entry.index,
                'offset': entry.offset,
                'size': entry.decompressed_size,
                'compressed_size': entry.compressed_size
            })
        else:
            self.analysis_result['other_files'].append({
                'index': entry.index,
                'offset': entry.offset,
                'size': entry.decompressed_size,
                'type': entry.entry_type.name
            })
    
    def get_parser(self) -> Optional[ObbParser]:
        """Get the underlying parser instance"""
        return self.parser
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        if not self.analysis_result:
            return "No analysis performed"
        
        lines = [
            f"OBB Analysis: {self.analysis_result.get('path', 'Unknown')}",
            f"Size: {self.analysis_result.get('size', 0) / (1024*1024):.2f} MB",
            f"Status: {self.analysis_result.get('status', 'unknown')}",
            f"Entries: {self.analysis_result.get('entry_count', 0)}",
            f"IFF Files: {len(self.analysis_result.get('iff_files', []))}",
            f"BIN Resources: {len(self.analysis_result.get('bin_resources', []))}",
            f"Other: {len(self.analysis_result.get('other_files', []))}",
        ]
        
        if self.analysis_result.get('error'):
            lines.append(f"Error: {self.analysis_result['error']}")
        
        return "\n".join(lines)


def detect_obb(obb_path: Path) -> Dict[str, Any]:
    """Convenience function to detect and analyze OBB"""
    detector = ObbDetector(obb_path)
    return detector.analyze()
