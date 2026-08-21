"""
Resource Analyzer widget for analyzing binary resources.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QPushButton, QTextEdit, QSplitter, QGroupBox
)
from PySide6.QtCore import Qt


class ResourceAnalyzerWidget(QWidget):
    """Widget for analyzing resources."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.current_resource = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Top panel - Analysis results
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Detected structures tree
        self.structures_tree = QTreeWidget()
        self.structures_tree.setHeaderLabels([
            "Type", "Offset", "Size", "Confidence"
        ])
        top_layout.addWidget(self.structures_tree)
        
        splitter.addWidget(top_widget)
        
        # Bottom panel - Details
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Info text
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(200)
        bottom_layout.addWidget(self.info_text)
        
        splitter.addWidget(bottom_widget)
        
        layout.addWidget(splitter)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("Analyze Resource")
        self.analyze_btn.clicked.connect(self.analyze_resource)
        toolbar_layout.addWidget(self.analyze_btn)
        
        self.export_btn = QPushButton("Export Raw")
        self.export_btn.clicked.connect(self.export_resource)
        toolbar_layout.addWidget(self.export_btn)
        
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
    
    def load_resource(self, resource_data: dict):
        """Load a resource for analysis."""
        
        self.current_resource = resource_data
        
        # Clear previous results
        self.structures_tree.clear()
        self.info_text.clear()
        
        # Show basic info
        name = resource_data.get('name', 'Unknown')
        size = resource_data.get('size', 0)
        offset = resource_data.get('offset', 0)
        
        self.info_text.setText(f"""RESOURCE INFORMATION

Name: {name}
Offset: 0x{offset:08X}
Size: {size} bytes ({self.format_size(size)})

Status: Ready for analysis
""")
    
    def format_size(self, size: int) -> str:
        """Format file size."""
        
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def analyze_resource(self):
        """Analyze current resource."""
        
        if not self.current_resource:
            return
        
        self.main_window.add_log("INFO", "Analyzing resource...")
        
        # Clear previous results
        self.structures_tree.clear()
        
        # TODO: Implement actual analysis
        # For now, show placeholder
        
        # Add placeholder entries
        texture_item = QTreeWidgetItem([
            "Texture Candidate",
            "0x00000000",
            "0",
            "Unknown"
        ])
        self.structures_tree.addTopLevelItem(texture_item)
        
        string_item = QTreeWidgetItem([
            "String Table",
            "0x00000000",
            "0",
            "Unknown"
        ])
        self.structures_tree.addTopLevelItem(string_item)
        
        self.info_text.append("\nAnalysis complete.\nNo structures detected yet.")
    
    def export_resource(self):
        """Export raw resource data."""
        
        if not self.current_resource:
            return
        
        self.main_window.add_log("INFO", "Export functionality coming soon")
