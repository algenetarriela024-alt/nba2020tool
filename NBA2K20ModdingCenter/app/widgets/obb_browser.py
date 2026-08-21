"""
OBB Browser widget for viewing files in the OBB.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QLineEdit, QPushButton, QHeaderView, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class OBBBrowserWidget(QWidget):
    """Widget for browsing OBB files."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.obb_data = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files...")
        self.search_box.textChanged.connect(self.filter_files)
        toolbar_layout.addWidget(self.search_box)
        
        # Filter combo
        # TODO: Add filter dropdown
        
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # File tree
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels([
            "Name", "Type", "Offset", "Size", "Compression", "Status"
        ])
        self.file_tree.setAlternatingRowColors(True)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        header = self.file_tree.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.file_tree)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.file_count_label = QLabel("Files: 0")
        status_layout.addWidget(self.file_count_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
    
    def load_obb_data(self, obb_data):
        """Load OBB data into browser."""
        
        self.obb_data = obb_data
        self.file_tree.clear()
        
        if not hasattr(obb_data, 'files'):
            return
        
        # Create root items for different categories
        iff_root = QTreeWidgetItem(["IFF Files", "", "", "", "", ""])
        iff_root.setExpanded(True)
        self.file_tree.addTopLevelItem(iff_root)
        
        resource_root = QTreeWidgetItem(["Resources", "", "", "", "", ""])
        resource_root.setExpanded(False)
        self.file_tree.addTopLevelItem(resource_root)
        
        other_root = QTreeWidgetItem(["Other Files", "", "", "", "", ""])
        other_root.setExpanded(False)
        self.file_tree.addTopLevelItem(other_root)
        
        # Add files to appropriate categories
        for file_info in obb_data.files:
            name = file_info.get('name', 'Unknown')
            file_type = file_info.get('type', 'Unknown')
            offset = file_info.get('offset', 0)
            size = file_info.get('size', 0)
            compression = file_info.get('compression', '-')
            status = file_info.get('status', 'OK')
            
            item = QTreeWidgetItem([
                name,
                file_type,
                f"0x{offset:08X}",
                self.format_size(size),
                compression,
                status
            ])
            
            # Store file info in item
            item.setData(0, Qt.UserRole, file_info)
            
            # Add to appropriate category
            if file_type.upper() == 'IFF':
                iff_root.addChild(item)
            elif file_type.upper() in ['BIN', 'RESOURCE']:
                resource_root.addChild(item)
            else:
                other_root.addChild(item)
        
        # Update count
        self.file_count_label.setText(f"Files: {len(obb_data.files)}")
    
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
    
    def filter_files(self, text: str):
        """Filter files based on search text."""
        
        text = text.lower()
        
        for i in range(self.file_tree.topLevelItemCount()):
            root = self.file_tree.topLevelItem(i)
            self.filter_item(root, text)
    
    def filter_item(self, item: QTreeWidgetItem, text: str):
        """Recursively filter items."""
        
        visible = False
        
        # Check if item matches
        if text in item.text(0).lower():
            visible = True
        
        # Check children
        for i in range(item.childCount()):
            child = item.child(i)
            if self.filter_item(child, text):
                visible = True
        
        item.setHidden(not visible)
        return visible
    
    def show_context_menu(self, position):
        """Show context menu for file tree."""
        
        item = self.file_tree.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        
        open_action = menu.addAction("Open")
        open_action.triggered.connect(lambda: self.open_selected())
        
        analyze_action = menu.addAction("Analyze")
        analyze_action.triggered.connect(lambda: self.analyze_selected())
        
        menu.addSeparator()
        
        extract_action = menu.addAction("Extract")
        extract_action.triggered.connect(lambda: self.extract_selected())
        
        export_action = menu.addAction("Export")
        export_action.triggered.connect(lambda: self.export_selected())
        
        menu.addSeparator()
        
        replace_action = menu.addAction("Replace")
        replace_action.triggered.connect(lambda: self.replace_selected())
        
        menu.addSeparator()
        
        hex_action = menu.addAction("Hex View")
        hex_action.triggered.connect(lambda: self.show_hex_view())
        
        properties_action = menu.addAction("Properties")
        properties_action.triggered.connect(lambda: self.show_properties())
        
        menu.exec_(self.file_tree.viewport().mapToGlobal(position))
    
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle double-click on item."""
        
        file_info = item.data(0, Qt.UserRole)
        if not file_info:
            return
        
        file_type = file_info.get('type', '').upper()
        
        if file_type == 'IFF':
            # Open IFF viewer
            self.main_window.iff_viewer_tab.load_iff(file_info)
            self.main_window.tab_widget.setCurrentWidget(self.main_window.iff_viewer_tab)
    
    def get_selected_files(self):
        """Get selected files."""
        
        selected = []
        for item in self.file_tree.selectedItems():
            file_info = item.data(0, Qt.UserRole)
            if file_info:
                selected.append(file_info)
        
        return selected
    
    def get_selected_iff(self):
        """Get selected IFF file."""
        
        selected = self.file_tree.selectedItems()
        if not selected:
            return None
        
        item = selected[0]
        file_info = item.data(0, Qt.UserRole)
        
        if file_info and file_info.get('type', '').upper() == 'IFF':
            return file_info
        
        return None
    
    def open_selected(self):
        """Open selected file."""
        
        pass
    
    def analyze_selected(self):
        """Analyze selected file."""
        
        pass
    
    def extract_selected(self):
        """Extract selected file."""
        
        self.main_window.extract_selected()
    
    def export_selected(self):
        """Export selected file."""
        
        pass
    
    def replace_selected(self):
        """Replace selected file."""
        
        pass
    
    def show_hex_view(self):
        """Show hex view of selected file."""
        
        pass
    
    def show_properties(self):
        """Show properties of selected file."""
        
        pass
