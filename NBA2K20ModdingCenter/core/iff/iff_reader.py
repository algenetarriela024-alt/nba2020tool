"""
IFF Reader for NBA 2K20 Mobile IFF files.
Format-driven parser that detects structure from binary evidence.
"""

import struct
from typing import List, Dict, Any, Optional


class IFFReader:
    """Reader for IFF (Interchange File Format) files."""
    
    def __init__(self, data: bytes = None, file_path: str = None):
        self.data = data
        self.file_path = file_path
        self.blocks: List[Dict[str, Any]] = []
        self.header: Dict[str, Any] = {}
        self.format_detected = False
        
        if file_path and not data:
            with open(file_path, 'rb') as f:
                self.data = f.read()
        
        if self.data:
            self.parse()
    
    def parse(self):
        """Parse IFF file structure."""
        
        if not self.data or len(self.data) < 12:
            return
        
        # Try to detect IFF format
        # Common IFF variants have different headers
        
        offset = 0
        
        # Check for standard IFF header: 4CC ID + size (big endian)
        if len(self.data) >= 8:
            iff_id = self.data[:4]
            
            # Try different interpretations
            try:
                chunk_size = struct.unpack('>I', self.data[4:8])[0]
                self.header['iff_id'] = iff_id.decode('ascii', errors='replace')
                self.header['chunk_size'] = chunk_size
                self.header['endian'] = 'big'
                self.format_detected = True
            except Exception:
                pass
            
            # Try little endian
            if not self.format_detected:
                try:
                    chunk_size = struct.unpack('<I', self.data[4:8])[0]
                    self.header['iff_id'] = iff_id.decode('ascii', errors='replace')
                    self.header['chunk_size'] = chunk_size
                    self.header['endian'] = 'little'
                    self.format_detected = True
                except Exception:
                    pass
        
        # Parse blocks/chunks
        self._parse_blocks()
    
    def _parse_blocks(self):
        """Parse IFF blocks/chunks."""
        
        if not self.data:
            return
        
        offset = 0
        block_num = 0
        
        while offset < len(self.data):
            if offset + 8 > len(self.data):
                break
            
            # Read block header
            block_id = self.data[offset:offset+4]
            
            try:
                block_size = struct.unpack('>I', self.data[offset+4:offset+8])[0]
            except Exception:
                try:
                    block_size = struct.unpack('<I', self.data[offset+4:offset+8])[0]
                except Exception:
                    break
            
            # Validate size
            if block_size == 0 or block_size > len(self.data) - offset - 8:
                break
            
            block_info = {
                'number': block_num,
                'name': f"Block_{block_num:02d}",
                'offset': offset,
                'size': block_size + 8,
                'type': self._detect_block_type(block_id),
                'block_id': block_id.decode('ascii', errors='replace'),
            }
            
            self.blocks.append(block_info)
            
            offset += block_size + 8
            block_num += 1
            
            # Safety limit
            if block_num > 1000:
                break
    
    def _detect_block_type(self, block_id: bytes) -> str:
        """Detect block type from ID."""
        
        # Check for known block types
        known_types = {
            b'FORM': 'Container',
            b'LIST': 'List',
            b'CAT ': 'Category',
            b'PROP': 'Properties',
        }
        
        return known_types.get(block_id, 'Unknown')
    
    def get_block_data(self, block_index: int) -> bytes:
        """Get data for a specific block."""
        
        if block_index < 0 or block_index >= len(self.blocks):
            return b''
        
        block = self.blocks[block_index]
        offset = block['offset'] + 8  # Skip header
        size = block['size'] - 8
        
        return self.data[offset:offset+size]
    
    def save(self, output_path: str):
        """Save modified IFF file."""
        
        if not self.data:
            return
        
        with open(output_path, 'wb') as f:
            f.write(self.data)
