"""
NBA 2K20 OBB Container Parser

Precise parser for the NBA 2K20 Android proprietary container format.
Implements:
- Magic value verification (0xBFxB3x00xAA)
- 2KB block alignment
- Hash-indexed entry table parsing
- ZLIB multi-block decompression
- Type detection (compressed, zlib-image, cdf, dram, filelist, ogg)
"""

from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator, Optional, Dict, List


# Format constants
MAGIC = b"\xbf\xb3\x00\xaa"
ALIGNMENT = 2048
TABLE_OFFSET = 0xF8
RECORD_STRUCT = struct.Struct("<IIII")

# Entry type signatures
TYPE_COMPRESSED = b"\x94\xef\x3b\xff"
TYPE_ZLIB = b"ZLIB"
TYPE_CDF = b"\x30\x50\x98\xf0"
TYPE_DRAM = b"\xdf\x85\xc5\xce"
TYPE_FILELIST = b"\x07\x12\x79\xe4"

TYPE_NAMES = {
    TYPE_COMPRESSED: "compressed",
    TYPE_ZLIB: "zlib-image",
    TYPE_CDF: "cdf",
    TYPE_DRAM: "dram",
    TYPE_FILELIST: "filelist",
    b"OggS": "ogg",
}

# Known filename mappings
KNOWN_NAMES = {
    zlib.crc32(b"TITLEPAGE.IFF"): "TITLEPAGE.IFF",
    zlib.crc32(b"LOADINGFLOWSTATIC.IFF"): "LOADINGFLOWSTATIC.IFF",
    zlib.crc32(b"ENGLISHBOOTUP.IFF"): "ENGLISHBOOTUP.IFF",
    zlib.crc32(b"FRONTEND_SYNC.IFF"): "FRONTEND_SYNC.IFF",
    zlib.crc32(b"GOOEYFRONTEND.IFF"): "GOOEYFRONTEND.IFF",
    zlib.crc32(b"GLOBAL.IFF"): "GLOBAL.IFF",
    zlib.crc32(b"LOGOS_LARGE.CDF"): "LOGOS_LARGE.CDF",
    zlib.crc32(b"LOGOS_MEDIUM.CDF"): "LOGOS_MEDIUM.CDF",
    zlib.crc32(b"LOGOS_SMALL.CDF"): "LOGOS_SMALL.CDF",
    zlib.crc32(b"LOGOS_TINY.CDF"): "LOGOS_TINY.CDF",
}

# Add generated names
for i in range(32):
    KNOWN_NAMES[zlib.crc32(f"F{i:03d}.IFF".encode())] = f"F{i:03d}.IFF"
    KNOWN_NAMES[zlib.crc32(f"LOGO{i:03d}.IFF".encode())] = f"LOGO{i:03d}.IFF"
    KNOWN_NAMES[zlib.crc32(f"UH{i:03d}.IFF".encode())] = f"UH{i:03d}.IFF"
    KNOWN_NAMES[zlib.crc32(f"UA{i:03d}.IFF".encode())] = f"UA{i:03d}.IFF"


@dataclass(frozen=True)
class ObbEntry:
    """Represents a single entry in the NBA 2K20 OBB container."""
    index: int
    name_hash: int
    block: int
    length: int
    reserved: int

    @property
    def offset(self) -> int:
        """Calculate byte offset from block number."""
        return self.block * ALIGNMENT

    @property
    def name(self) -> str:
        """Get known name or hex hash fallback."""
        return KNOWN_NAMES.get(self.name_hash, f"{self.name_hash:08x}")

    @property
    def type_name(self) -> str:
        """Placeholder - actual type determined during read."""
        return "unknown"


class ObbParser:
    """
    Parses NBA 2K20 OBB container format.
    
    Structure:
    - 0xF8 byte header with magic, alignment, counts
    - Entry table (0xD0 bytes per entry)
    - Data blocks (2KB aligned)
    """
    
    def __init__(self, obb_path: Path):
        self.obb_path = Path(obb_path)
        self.entries: List[ObbEntry] = []
        self.entry_by_hash: Dict[int, ObbEntry] = {}
        self.file_size = 0
        self.header_hash: Optional[str] = None
        self._next_offsets: Dict[int, int] = {}
        self._file_handle: Optional[BinaryIO] = None
    
    def open(self) -> bool:
        """Open and parse the OBB file structure."""
        try:
            self.file_size = self.obb_path.stat().st_size
            
            with self.obb_path.open("rb") as stream:
                # Verify magic
                magic = stream.read(4)
                if magic != MAGIC:
                    print(f"Error: Invalid OBB magic. Expected {MAGIC.hex()}, got {magic.hex()}")
                    return False
                
                # Verify alignment
                align_val = self._read_u32le(stream, 4)
                if align_val != ALIGNMENT:
                    print(f"Error: Unexpected alignment {align_val}, expected {ALIGNMENT}")
                    return False
                
                # Verify archive count
                archive_count = self._read_u64le(stream, 8)
                if archive_count != 1:
                    print(f"Warning: Unexpected archive count {archive_count}")
                
                # Read entry count
                count = self._read_u64le(stream, 0x18)
                
                # Parse entry table
                stream.seek(TABLE_OFFSET)
                self.entries.clear()
                self.entry_by_hash.clear()
                
                for index in range(count):
                    record_data = stream.read(RECORD_STRUCT.size)
                    if len(record_data) < RECORD_STRUCT.size:
                        print(f"Error: Truncated entry table at index {index}")
                        break
                    
                    length, reserved, name_hash, block = RECORD_STRUCT.unpack(record_data)
                    entry = ObbEntry(
                        index=index,
                        name_hash=name_hash,
                        block=block,
                        length=length,
                        reserved=reserved
                    )
                    
                    # Validate offset
                    if entry.offset >= self.file_size:
                        print(f"Warning: Entry {index} offset {entry.offset} beyond file size")
                        continue
                    
                    self.entries.append(entry)
                    self.entry_by_hash[name_hash] = entry
                
                # Build offset map for stored_size calculation
                offsets = sorted({e.offset for e in self.entries})
                self._next_offsets = {
                    offset: offsets[i + 1] if i + 1 < len(offsets) else self.file_size
                    for i, offset in enumerate(offsets)
                }
            
            return len(self.entries) > 0
            
        except Exception as e:
            print(f"Error opening OBB: {e}")
            return False
    
    def close(self):
        """Close any open file handles."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
    
    def stored_size(self, entry: ObbEntry) -> int:
        """Return physical span including padding to next entry."""
        return self._next_offsets.get(entry.offset, self.file_size) - entry.offset
    
    def get_entry_type(self, stream: BinaryIO, entry: ObbEntry) -> bytes:
        """Read 4-byte type signature from entry start."""
        stream.seek(entry.offset)
        return stream.read(4)
    
    def get_type_name(self, stream: BinaryIO, entry: ObbEntry) -> str:
        """Get human-readable type name."""
        sig = self.get_entry_type(stream, entry)
        return TYPE_NAMES.get(sig, sig.hex() if sig else "empty")
    
    def decompressed_chunks(self, stream: BinaryIO, entry: ObbEntry) -> Iterator[bytes]:
        """
        Decompress ZLIB-wrapped entry data.
        Yields uncompressed chunks.
        """
        stream.seek(entry.offset)
        entry_type = stream.read(4)
        
        if entry_type == TYPE_COMPRESSED:
            # Skip relative offset field
            rel_offset = struct.unpack("<I", stream.read(4))[0]
            if rel_offset < 8 or rel_offset >= self.stored_size(entry):
                raise ValueError(f"Invalid payload offset {rel_offset} for entry {entry.index}")
            position = entry.offset + rel_offset
        elif entry_type == TYPE_ZLIB:
            position = entry.offset
        else:
            raise ValueError(f"Entry {entry.index} is not ZLIB-wrapped (type: {entry_type.hex()})")
        
        end = entry.offset + self.stored_size(entry)
        block_num = 0
        
        while position + 16 <= end:
            stream.seek(position)
            if stream.read(4) != TYPE_ZLIB:
                break
            
            # Read ZLIB block header (big-endian)
            header = stream.read(12)
            if len(header) < 12:
                break
            
            unpacked_size, stored_size, flags = struct.unpack(">III", header)
            packed_size = stored_size - 16
            
            if packed_size <= 0 or position + stored_size > end:
                raise ValueError(f"Invalid ZLIB block {block_num} in entry {entry.index}")
            
            # Read and decompress
            packed_data = stream.read(packed_size)
            if len(packed_data) != packed_size:
                raise EOFError(f"Truncated ZLIB block {block_num}")
            
            unpacked_data = zlib.decompress(packed_data)
            if len(unpacked_data) != unpacked_size:
                raise ValueError(f"Decompressed size mismatch in block {block_num}")
            
            yield unpacked_data
            position += stored_size
            block_num += 1
        
        if block_num == 0:
            raise ValueError(f"No valid ZLIB blocks found in entry {entry.index}")
    
    def extract_entry(self, entry: ObbEntry, decompress: bool = False) -> Optional[bytes]:
        """
        Extract entry data.
        
        Args:
            entry: The entry to extract
            decompress: If True, decompress ZLIB data; if False, return raw bytes
        
        Returns:
            Extracted data or None on error
        """
        try:
            with self.obb_path.open("rb") as stream:
                if decompress:
                    chunks = list(self.decompressed_chunks(stream, entry))
                    return b"".join(chunks)
                else:
                    stream.seek(entry.offset)
                    size = self.stored_size(entry)
                    return stream.read(size)
        except Exception as e:
            print(f"Error extracting entry {entry.index}: {e}")
            return None
    
    def get_entry_list(self) -> List[ObbEntry]:
        """Get all entries sorted by index."""
        return sorted(self.entries, key=lambda e: e.index)
    
    def get_entry_info(self, index: int) -> Optional[ObbEntry]:
        """Get entry by index."""
        if 0 <= index < len(self.entries):
            return self.entries[index]
        return None
    
    def list_entries(self) -> List[Dict]:
        """Get human-readable entry information."""
        result = []
        with self.obb_path.open("rb") as stream:
            for entry in self.entries:
                type_name = self.get_type_name(stream, entry)
                result.append({
                    'index': entry.index,
                    'name': entry.name,
                    'hash': f"0x{entry.name_hash:08x}",
                    'block': entry.block,
                    'offset': f"0x{entry.offset:08x}",
                    'length': entry.length,
                    'stored_size': self.stored_size(entry),
                    'type': type_name,
                })
        return result
    
    @property
    def entry_count(self) -> int:
        """Total number of entries."""
        return len(self.entries)
    
    def _read_u32le(self, stream: BinaryIO, offset: int) -> int:
        """Read 32-bit little-endian integer."""
        stream.seek(offset)
        data = stream.read(4)
        return struct.unpack("<I", data)[0]
    
    def _read_u64le(self, stream: BinaryIO, offset: int) -> int:
        """Read 64-bit little-endian integer."""
        stream.seek(offset)
        data = stream.read(8)
        return struct.unpack("<Q", data)[0]


def load_obb(obb_path: Path) -> Optional[ObbParser]:
    """
    Convenience function to load an OBB file.
    
    Usage:
        parser = load_obb(Path("main.obb"))
        if parser:
            for entry in parser.entries:
                print(entry.name)
    """
    parser = ObbParser(obb_path)
    if parser.open():
        return parser
    parser.close()
    return None
