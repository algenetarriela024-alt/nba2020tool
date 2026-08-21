"""
IFF Viewer widget for viewing and editing IFF files.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QSplitter, QGroupBox, QTextEdit, QMenu,
    QFileDialog, QMessageBox, QHeaderView, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class IFFViewerWidget(QWidget):
    """Widget for viewing IFF files."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.current_iff = None
        self.blocks = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Block list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # IFF info group
        info_group = QGroupBox("IFF FILE")
        info_layout = QVBoxLayout(info_group)
        
        self.iff_info_text = QTextEdit()
        self.iff_info_text.setReadOnly(True)
        self.iff_info_text.setMaximumHeight(150)
        info_layout.addWidget(self.iff_info_text)
        
        left_layout.addWidget(info_group)
        
        # Blocks table
        self.blocks_table = QTableWidget()
        self.blocks_table.setColumnCount(5)
        self.blocks_table.setHorizontalHeaderLabels([
            "#", "Block", "Offset", "Size", "Type"
        ])
        self.blocks_table.setAlternatingRowColors(True)
        self.blocks_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.blocks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.blocks_table.customContextMenuRequested.connect(self.show_block_context_menu)
        self.blocks_table.itemSelectionChanged.connect(self.on_block_selected)
        
        header = self.blocks_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        left_layout.addWidget(self.blocks_table)
        
        splitter.addWidget(left_widget)
        
        # Right panel - Preview/Hex view
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder for now
        self.preview_label = QLabel("Select a block to view its contents")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("color: #9CA3AF; font-size: 16px;")
        right_layout.addWidget(self.preview_label)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        # Bottom toolbar
        toolbar_layout = QHBoxLayout()
        
        self.extract_block_btn = QPushButton("Extract Block")
        self.extract_block_btn.clicked.connect(self.extract_block)
        toolbar_layout.addWidget(self.extract_block_btn)
        
        self.analyze_block_btn = QPushButton("Analyze Block")
        self.analyze_block_btn.clicked.connect(self.analyze_block)
        toolbar_layout.addWidget(self.analyze_block_btn)
        
        self.hex_view_btn = QPushButton("Hex View")
        self.hex_view_btn.clicked.connect(self.show_hex_view)
        toolbar_layout.addWidget(self.hex_view_btn)
        
        toolbar_layout.addStretch()
        
        self.save_iff_btn = QPushButton("Save IFF")
        self.save_iff_btn.clicked.connect(self.save_iff)
        toolbar_layout.addWidget(self.save_iff_btn)
        
        layout.addLayout(toolbar_layout)
    
    def load_iff(self, iff_info: dict):
        """Load an IFF file for viewing."""
        
        self.current_iff = iff_info
        
        # Update info panel
        name = iff_info.get('name', 'Unknown')
        size = iff_info.get('size', 0)
        
        info_text = f"""Name:
{name}

Size:
{self.format_size(size)}

Blocks:
Loading...

Format:
Detecting...

Architecture:
Auto-detected
"""
        self.iff_info_text.setText(info_text)
        
        # Clear blocks table
        self.blocks_table.setRowCount(0)
        self.blocks = []
        
        # TODO: Actually parse the IFF file
        # For now, show placeholder
        self.main_window.add_log("INFO", f"Opening IFF: {name}")
    
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
    
    def on_block_selected(self):
        """Handle block selection."""
        
        selected_rows = self.blocks_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        block = self.blocks[row] if row < len(self.blocks) else None
        
        if block:
            self.main_window.add_log("INFO", f"Selected block: {block.get('name', 'Unknown')}")
    
    def show_block_context_menu(self, position):
        """Show context menu for blocks."""
        
        menu = QMenu(self)
        
        view_action = menu.addAction("View")
        view_action.triggered.connect(self.view_block)
        
        extract_action = menu.addAction("Extract")
        extract_action.triggered.connect(self.extract_block)
        
        menu.addSeparator()
        
        analyze_action = menu.addAction("Analyze")
        analyze_action.triggered.connect(self.analyze_block)
        
        replace_action = menu.addAction("Replace")
        replace_action.triggered.connect(self.replace_block)
        
        menu.exec_(self.blocks_table.viewport().mapToGlobal(position))
    
    def view_block(self):
        """View selected block."""
        
        pass
    
    def extract_block(self):
        """Extract selected block."""
        
        pass
    
    def analyze_block(self):
        """Analyze selected block."""
        
        pass
    
    def show_hex_view(self):
        """Show hex view of selected block."""
        
        pass
    
    def replace_block(self):
        """Replace selected block."""
        
        pass
    
    def save_iff(self):
        """Save modified IFF."""
        
        if not self.current_iff:
            return
        
        QMessageBox.information(
            self,
            "Save IFF",
            "IFF saving functionality will be implemented in Phase 5."
        )
