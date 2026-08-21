"""
Teams widget for viewing and editing team database.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QPushButton, QSplitter, QGroupBox, QScrollArea,
    QHeaderView, QComboBox
)
from PySide6.QtCore import Qt


class TeamsWidget(QWidget):
    """Widget for viewing and editing teams."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.teams_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Team list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search teams...")
        toolbar_layout.addWidget(self.search_box)
        
        # Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Teams")
        self.filter_combo.addItem("Eastern Conference")
        self.filter_combo.addItem("Western Conference")
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        left_layout.addLayout(toolbar_layout)
        
        # Teams table
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(5)
        self.teams_table.setHorizontalHeaderLabels([
            "ID", "Team Name", "Short Name", "City", "Conference"
        ])
        self.teams_table.setAlternatingRowColors(True)
        self.teams_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        header = self.teams_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        left_layout.addWidget(self.teams_table)
        
        splitter.addWidget(left_widget)
        
        # Right panel - Team editor
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area for editor
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        editor_widget = QWidget()
        scroll.setWidget(editor_widget)
        
        editor_layout = QVBoxLayout(editor_widget)
        
        # Team info group
        info_group = QGroupBox("TEAM INFORMATION")
        info_layout = QVBoxLayout(info_group)
        
        # Create form fields
        self.team_fields = {}
        fields = [
            ("Team ID", "team_id"),
            ("Team Name", "team_name"),
            ("Short Name", "short_name"),
            ("City", "city"),
            ("Conference", "conference"),
            ("Division", "division"),
            ("Arena", "arena"),
        ]
        
        for label_text, field_name in fields:
            field_layout = QHBoxLayout()
            label = QLabel(label_text + ":")
            label.setFixedWidth(100)
            field_layout.addWidget(label)
            
            field = QLineEdit()
            self.team_fields[field_name] = field
            field_layout.addWidget(field)
            field_layout.addStretch()
            info_layout.addLayout(field_layout)
        
        editor_layout.addWidget(info_group)
        
        # Colors group
        colors_group = QGroupBox("TEAM COLORS")
        colors_layout = QVBoxLayout(colors_group)
        
        color_fields = [
            ("Primary Color", "primary_color"),
            ("Secondary Color", "secondary_color"),
        ]
        
        self.color_fields = {}
        for label_text, field_name in color_fields:
            field_layout = QHBoxLayout()
            label = QLabel(label_text + ":")
            label.setFixedWidth(100)
            field_layout.addWidget(label)
            
            field = QLineEdit()
            field.setPlaceholderText("#RRGGBB")
            self.color_fields[field_name] = field
            field_layout.addWidget(field)
            field_layout.addStretch()
            colors_layout.addLayout(field_layout)
        
        editor_layout.addWidget(colors_group)
        
        editor_layout.addStretch()
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_btn)
        
        self.revert_btn = QPushButton("Revert")
        self.revert_btn.clicked.connect(self.revert_changes)
        button_layout.addWidget(self.revert_btn)
        
        button_layout.addStretch()
        
        editor_layout.addLayout(button_layout)
        
        right_layout.addWidget(scroll)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def load_obb_data(self, obb_data):
        """Load team data from OBB."""
        
        self.teams_data = []
        self.teams_table.setRowCount(0)
        
        # TODO: Actually parse team data from OBB
        
        self.main_window.add_log("INFO", "Loading team data...")
    
    def apply_changes(self):
        """Apply changes to current team."""
        
        self.main_window.add_log("INFO", "Applying team changes")
    
    def revert_changes(self):
        """Revert changes to current team."""
        
        self.main_window.add_log("INFO", "Reverting team changes")
