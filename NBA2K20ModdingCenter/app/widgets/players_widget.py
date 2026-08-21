"""
Players widget for viewing and editing player database.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QPushButton, QSplitter, QGroupBox, QScrollArea,
    QHeaderView, QTabWidget, QComboBox
)
from PySide6.QtCore import Qt


class PlayersWidget(QWidget):
    """Widget for viewing and editing players."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.players_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Player list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search players...")
        toolbar_layout.addWidget(self.search_box)
        
        # Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Players")
        self.filter_combo.addItem("Active")
        self.filter_combo.addItem("Free Agents")
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        left_layout.addLayout(toolbar_layout)
        
        # Players table
        self.players_table = QTableWidget()
        self.players_table.setColumnCount(6)
        self.players_table.setHorizontalHeaderLabels([
            "ID", "Last_Name", "First_Name", "Nickname", "ID2", "Status"
        ])
        self.players_table.setAlternatingRowColors(True)
        self.players_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.players_table.itemSelectionChanged.connect(self.on_player_selected)
        
        header = self.players_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        left_layout.addWidget(self.players_table)
        
        splitter.addWidget(left_widget)
        
        # Right panel - Player editor
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for editor
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        editor_widget = QWidget()
        scroll.setWidget(editor_widget)
        
        editor_layout = QVBoxLayout(editor_widget)
        
        # Player info group
        info_group = QGroupBox("PLAYER INFORMATION")
        info_layout = QVBoxLayout(info_group)
        
        # Create form fields
        self.player_fields = {}
        fields = [
            ("ID", "player_id"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Nickname", "nickname"),
            ("Position", "position"),
            ("Height", "height"),
            ("Weight", "weight"),
            ("Overall", "overall"),
        ]
        
        for label_text, field_name in fields:
            field_layout = QHBoxLayout()
            label = QLabel(label_text + ":")
            label.setFixedWidth(100)
            field_layout.addWidget(label)
            
            if field_name == "overall":
                field = QLineEdit()
                field.setFixedWidth(100)
            else:
                field = QLineEdit()
            
            self.player_fields[field_name] = field
            field_layout.addWidget(field)
            field_layout.addStretch()
            info_layout.addLayout(field_layout)
        
        editor_layout.addWidget(info_group)
        
        # Ratings group
        ratings_group = QGroupBox("RATINGS")
        ratings_layout = QVBoxLayout(ratings_group)
        
        # Add some rating fields
        rating_fields = [
            ("Speed", "speed"),
            ("Ball Handle", "ball_handle"),
            ("Shooting", "shooting"),
            ("Defense", "defense"),
        ]
        
        self.rating_fields = {}
        for label_text, field_name in rating_fields:
            field_layout = QHBoxLayout()
            label = QLabel(label_text + ":")
            label.setFixedWidth(100)
            field_layout.addWidget(label)
            
            field = QLineEdit()
            field.setFixedWidth(100)
            self.rating_fields[field_name] = field
            field_layout.addWidget(field)
            field_layout.addStretch()
            ratings_layout.addLayout(field_layout)
        
        editor_layout.addWidget(ratings_group)
        
        editor_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_btn)
        
        self.revert_btn = QPushButton("Revert")
        self.revert_btn.clicked.connect(self.revert_changes)
        button_layout.addWidget(self.revert_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_changes)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        editor_layout.addLayout(button_layout)
        
        right_layout.addWidget(scroll)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def load_obb_data(self, obb_data):
        """Load player data from OBB."""
        
        self.players_data = []
        self.players_table.setRowCount(0)
        
        # TODO: Actually parse player data from OBB
        # For now, show placeholder
        
        self.main_window.add_log("INFO", "Loading player data...")
    
    def on_player_selected(self):
        """Handle player selection."""
        
        selected_rows = self.players_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        # Load player data into editor
        # TODO: Implement actual loading
    
    def apply_changes(self):
        """Apply changes to current player."""
        
        self.main_window.add_log("INFO", "Applying player changes")
    
    def revert_changes(self):
        """Revert changes to current player."""
        
        self.main_window.add_log("INFO", "Reverting player changes")
    
    def reset_changes(self):
        """Reset all changes."""
        
        self.main_window.add_log("INFO", "Resetting all changes")
