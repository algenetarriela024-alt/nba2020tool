"""
Hex Viewer widget for viewing binary data.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel,
    QSplitter, QLineEdit, QPushButton, QScrollBar
)
from PySide6.QtCore import Qt


class HexViewerWidget(QWidget):
    """Widget for viewing hex data."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.data = b''
        self.offset = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Offset navigation
        toolbar_layout.addWidget(QLabel("Offset:"))
        
        self.offset_edit = QLineEdit("0x00000000")
        self.offset_edit.setFixedWidth(120)
        toolbar_layout.addWidget(self.offset_edit)
        
        go_btn = QPushButton("Go")
        go_btn.clicked.connect(self.go_to_offset)
        toolbar_layout.addWidget(go_btn)
        
        toolbar_layout.addStretch()
        
        # Search
        toolbar_layout.addWidget(QLabel("Search:"))
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Hex or ASCII")
        self.search_edit.setFixedWidth(200)
        toolbar_layout.addWidget(self.search_edit)
        
        search_btn = QPushButton("Find")
        search_btn.clicked.connect(self.search_data)
        toolbar_layout.addWidget(search_btn)
        
        layout.addLayout(toolbar_layout)
        
        # Hex view area
        splitter = QSplitter(Qt.Horizontal)
        
        # Hex display
        self.hex_display = QPlainTextEdit()
        self.hex_display.setFontFamily("Consolas")
        self.hex_display.setReadOnly(True)
        splitter.addWidget(self.hex_display)
        
        # ASCII display
        self.ascii_display = QPlainTextEdit()
        self.ascii_display.setFontFamily("Consolas")
        self.ascii_display.setReadOnly(True)
        splitter.addWidget(self.ascii_display)
        
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def load_data(self, data: bytes, offset: int = 0):
        """Load binary data for viewing."""
        
        self.data = data
        self.offset = offset
        self.render_hex()
    
    def render_hex(self):
        """Render hex display."""
        
        if not self.data:
            return
        
        hex_lines = []
        ascii_lines = []
        
        for i in range(0, min(len(self.data), 1024 * 16), 16):  # Limit to first 16KB for performance
            chunk = self.data[i:i+16]
            
            # Hex part
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            hex_part = hex_part.ljust(47)  # Pad to align
            
            # Offset
            line_offset = self.offset + i
            hex_line = f"{line_offset:08X}  {hex_part}"
            hex_lines.append(hex_line)
            
            # ASCII part
            ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            ascii_lines.append(ascii_part)
        
        self.hex_display.setPlainText("\n".join(hex_lines))
        self.ascii_display.setPlainText("\n".join(ascii_lines))
    
    def go_to_offset(self):
        """Go to specified offset."""
        
        try:
            text = self.offset_edit.text().strip()
            if text.startswith("0x"):
                offset = int(text, 16)
            else:
                offset = int(text)
            
            # TODO: Scroll to offset
            self.main_window.add_log("INFO", f"Jumped to offset 0x{offset:X}")
        except ValueError:
            pass
    
    def search_data(self):
        """Search for data."""
        
        search_text = self.search_edit.text()
        if not search_text:
            return
        
        # Try as hex first
        try:
            hex_bytes = bytes.fromhex(search_text.replace(" ", ""))
            pos = self.data.find(hex_bytes)
            if pos >= 0:
                self.main_window.add_log("INFO", f"Found at offset 0x{pos:X}")
                return
        except ValueError:
            pass
        
        # Try as ASCII
        ascii_bytes = search_text.encode('utf-8', errors='ignore')
        pos = self.data.find(ascii_bytes)
        if pos >= 0:
            self.main_window.add_log("INFO", f"Found at offset 0x{pos:X}")
            return
        
        self.main_window.add_log("WARNING", "Search pattern not found")
