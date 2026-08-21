"""
Search widget for global search functionality.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QTreeWidget, QTreeWidgetItem,
    QHeaderView, QTabWidget, QComboBox
)
from PySide6.QtCore import Qt


class SearchWidget(QWidget):
    """Widget for global search."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Search bar
        search_layout = QHBoxLayout()
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search: filename, player name, team name, texture, model, string, hex bytes, offset...")
        self.search_box.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_box)
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItem("All")
        self.search_type_combo.addItem("Files")
        self.search_type_combo.addItem("Players")
        self.search_type_combo.addItem("Teams")
        self.search_type_combo.addItem("Textures")
        self.search_type_combo.addItem("Models")
        self.search_type_combo.addItem("Strings")
        self.search_type_combo.addItem("Hex")
        search_layout.addWidget(self.search_type_combo)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Results tabs
        self.results_tabs = QTabWidget()
        
        # All results tab
        self.all_results_tree = QTreeWidget()
        self.all_results_tree.setHeaderLabels(["Type", "Name", "Location", "Details"])
        self.results_tabs.addTab(self.all_results_tree, "All Results")
        
        # Files results tab
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Name", "Type", "Offset", "Size"])
        self.results_tabs.addTab(self.files_table, "Files")
        
        # Players results tab
        self.players_table = QTableWidget()
        self.players_table.setColumnCount(5)
        self.players_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Nickname", "Status"])
        self.results_tabs.addTab(self.players_table, "Players")
        
        # Teams results tab
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(4)
        self.teams_table.setHorizontalHeaderLabels(["ID", "Team Name", "City", "Conference"])
        self.results_tabs.addTab(self.teams_table, "Teams")
        
        # Textures results tab
        self.textures_table = QTableWidget()
        self.textures_table.setColumnCount(5)
        self.textures_table.setHorizontalHeaderLabels(["Name", "Width", "Height", "Format", "Size"])
        self.results_tabs.addTab(self.textures_table, "Textures")
        
        # Strings results tab
        self.strings_table = QTableWidget()
        self.strings_table.setColumnCount(3)
        self.strings_table.setHorizontalHeaderLabels(["Offset", "String", "Context"])
        self.results_tabs.addTab(self.strings_table, "Strings")
        
        layout.addWidget(self.results_tabs)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.results_count_label = QLabel("Results: 0")
        status_layout.addWidget(self.results_count_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
    
    def perform_search(self):
        """Perform search."""
        
        query = self.search_box.text().strip()
        if not query:
            return
        
        search_type = self.search_type_combo.currentText()
        
        self.main_window.add_log("INFO", f"Searching for: {query} ({search_type})")
        
        # Clear previous results
        self.all_results_tree.clear()
        self.files_table.setRowCount(0)
        self.players_table.setRowCount(0)
        self.teams_table.setRowCount(0)
        self.textures_table.setRowCount(0)
        self.strings_table.setRowCount(0)
        
        # TODO: Implement actual search across OBB data
        
        # Add placeholder result
        item = QTreeWidgetItem([
            "Info",
            "Search functionality",
            "Coming soon",
            "Full search will be implemented in Phase 6"
        ])
        self.all_results_tree.addTopLevelItem(item)
        
        self.results_count_label.setText("Results: 1")
