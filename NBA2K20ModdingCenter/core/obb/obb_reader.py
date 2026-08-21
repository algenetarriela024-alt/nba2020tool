"""
OBB Reader for NBA 2K20 Mobile OBB files.
Format-driven parser that detects structure from binary evidence.
"""

import os
import struct
from typing import List, Dict, Any, Optional


class OBBReader:
    """Reader for NBA 2K20 Mobile OBB files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.files: List[Dict[str, Any]] = []
        self.iff_files: List[Dict[str, Any]] = []
        self.resources: List[Dict[str, Any]] = []
        self.textures: List[Dict[str, Any]] = []
        self.models: List[Dict[str, Any]] = []
        self.players: List[Dict[str, Any]] = []
        self.teams: List[Dict[str, Any]] = []
        self.headshapes: List[Dict[str, Any]] = []
        self.index: Dict[str, Any] = {}
        
        # File handle for reading
        self._file = None
    
    def __enter__(self):
        self._file = open(self.file_path, 'rb')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def scan(self):
        """Perform initial scan of OBB file structure."""
        
        # Open file for reading if not already open
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            # OBB files are typically simple archive formats
            # We'll scan for known signatures
            
            self._file.seek(0)
            
            # Read first bytes to detect format
            magic = self._file.read(16)
            
            # Check for common archive signatures
            # Android OBB files are often just concatenated files or use a simple format
            
            self._file.seek(0)
            
            # For now, treat as a raw container and scan for IFF signatures
            self._scan_for_signatures()
        finally:
            # Close the file handle we opened (if any)
            if file_handle:
                file_handle.close()
                self._file = None
    
    def _scan_for_signatures(self):
        """Scan for known file signatures in the OBB."""
        
        # Open file if needed
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            # IFF signature: "IFF." or similar
            iff_signatures = [b'IFF.', b'IFF ', b'\x49\x46\x46\x00']
            
            # Scan through file looking for signatures
            chunk_size = 1024 * 1024  # 1MB chunks
            self._file.seek(0)
            
            position = 0
            while position < self.file_size:
                self._file.seek(position)
                chunk = self._file.read(min(chunk_size, self.file_size - position))
                
                # Search for IFF signatures
                for sig in iff_signatures:
                    offset = chunk.find(sig)
                    while offset != -1:
                        absolute_offset = position + offset
                        self._process_iff_candidate(absolute_offset)
                        offset = chunk.find(sig, offset + 1)
                
                position += chunk_size - len(sig)  # Overlap to catch boundaries
        finally:
            if file_handle:
                file_handle.close()
                self._file = None
    
    def _process_iff_candidate(self, offset: int):
        """Process a potential IFF file at given offset."""
        
        # Open file if needed
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            self._file.seek(offset)
            
            # Read potential IFF header
            header = self._file.read(12)
            if len(header) < 12:
                return
            
            # Try to parse IFF structure
            # Standard IFF format: 4CC ID + size + data
            
            try:
                # Read IFF chunk header
                iff_id = header[:4]
                chunk_size = struct.unpack('>I', header[4:8])[0]
                
                # Validate size
                if chunk_size > 100 * 1024 * 1024:  # > 100MB is suspicious
                    return
                
                # Extract filename from nearby data if possible
                filename = f"IFF_{offset:08X}.iff"
                
                file_info = {
                    'name': filename,
                    'type': 'IFF',
                    'offset': offset,
                    'size': chunk_size + 8,
                    'compression': '-',
                    'status': 'OK',
                    'iff_id': iff_id.decode('ascii', errors='replace'),
                }
                
                self.files.append(file_info)
                self.iff_files.append(file_info)
                
            except Exception:
                pass
        finally:
            if file_handle:
                file_handle.close()
                self._file = None
    
    def detect_iff_files(self):
        """Detect IFF files in the OBB."""
        
        # Already done in scan, but can be called separately
        pass
    
    def detect_resources(self):
        """Detect resource blocks in the OBB."""
        
        # Open file if needed
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            # Scan for BIN/resource signatures
            # Look for common resource patterns
            resource_signatures = [
                b'\x00\x00\x00\x00',  # Null padding (potential resource boundary)
            ]
            
            # For now, mark large contiguous regions as potential resources
            for file_info in self.files:
                if file_info['type'] != 'IFF':
                    self.resources.append({
                        'name': file_info['name'],
                        'type': 'BIN',
                        'offset': file_info['offset'],
                        'size': file_info['size'],
                        'parent': file_info.get('name'),
                    })
        finally:
            if file_handle:
                file_handle.close()
                self._file = None
    
    def scan_textures(self):
        """Scan for texture data in resources."""
        
        # Texture detection will be implemented based on actual file analysis
        # Common texture signatures: DXT1, DXT5, etc.
        pass
    
    def build_index(self):
        """Build asset index for quick lookup."""
        
        self.index = {
            'obb': os.path.basename(self.file_path),
            'file_size': self.file_size,
            'files': self.files,
            'iff': self.iff_files,
            'resources': self.resources,
            'textures': self.textures,
            'models': self.models,
            'players': self.players,
            'teams': self.teams,
            'headshapes': self.headshapes,
        }
    
    def extract_files(self, files: List[Dict], output_dir: str):
        """Extract specified files to output directory."""
        
        # Open file if needed
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            for file_info in files:
                offset = file_info.get('offset', 0)
                size = file_info.get('size', 0)
                name = file_info.get('name', 'unknown')
                
                self._file.seek(offset)
                data = self._file.read(size)
                
                output_path = os.path.join(output_dir, name)
                with open(output_path, 'wb') as f:
                    f.write(data)
        finally:
            if file_handle:
                file_handle.close()
                self._file = None
    
    def extract_all(self, output_dir: str):
        """Extract all files to output directory."""
        
        self.extract_files(self.files, output_dir)
    
    def rebuild(self, output_path: str, modified_files: Dict):
        """Rebuild OBB with modifications."""
        
        # This is a placeholder - full implementation requires understanding
        # the exact OBB format used by NBA 2K20 Mobile
        
        # Safe mode: never overwrite original
        if output_path == self.file_path:
            raise ValueError("Cannot overwrite original OBB file")
        
        # TODO: Implement proper OBB rebuilding
        # For now, just copy the original
        with open(self.file_path, 'rb') as src:
            with open(output_path, 'wb') as dst:
                dst.write(src.read())
    
    def read_at(self, offset: int, size: int) -> bytes:
        """Read data at specific offset."""
        
        # Open file if needed
        file_handle = None
        if not self._file:
            file_handle = open(self.file_path, 'rb')
            self._file = file_handle
        
        try:
            self._file.seek(offset)
            return self._file.read(size)
        finally:
            if file_handle:
                file_handle.close()
                self._file = None
    
    def get_file_data(self, file_info: Dict) -> bytes:
        """Get complete data for a file."""
        
        offset = file_info.get('offset', 0)
        size = file_info.get('size', 0)
        
        return self.read_at(offset, size)
