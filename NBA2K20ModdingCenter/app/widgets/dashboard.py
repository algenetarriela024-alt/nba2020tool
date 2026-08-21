"""
Dashboard widget for NBA 2K20 Mobile Modding Center.
Shows overview of opened OBB and quick actions.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QPushButton, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt


class InfoCard(QFrame):
    """Information card widget."""
    
    def __init__(self, title: str, value: str = "", parent=None):
        super().__init__(parent)
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("infoCard")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #9CA3AF;")
        layout.addWidget(self.title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setObjectName("valueLabel")
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #E5E7EB;")
        self.value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.value_label)
    
    def set_value(self, value: str):
        """Set card value."""
        self.value_label.setText(value)


class DashboardWidget(QWidget):
    """Dashboard widget showing OBB overview."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Content widget
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        
        # Welcome section (shown when no OBB is loaded)
        self.welcome_frame = QFrame()
        self.welcome_frame.setObjectName("welcomeFrame")
        welcome_layout = QVBoxLayout(self.welcome_frame)
        welcome_layout.setAlignment(Qt.AlignCenter)
        
        welcome_title = QLabel("NBA 2K20 MOBILE MODDING CENTER")
        welcome_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #E5E7EB;")
        welcome_title.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_title)
        
        welcome_subtitle = QLabel("Professional modding tool for NBA 2K20 Mobile Android")
        welcome_subtitle.setStyleSheet("font-size: 16px; color: #9CA3AF; margin-top: 10px;")
        welcome_subtitle.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_subtitle)
        
        open_button = QPushButton("OPEN OBB")
        open_button.setObjectName("openOBBButton")
        open_button.setStyleSheet("""
            QPushButton {
                background-color: #B91C1C;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 8px;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        open_button.clicked.connect(self._open_obb_clicked)
        welcome_layout.addWidget(open_button, alignment=Qt.AlignCenter)
        
        content_layout.addWidget(self.welcome_frame)
        
        # Dashboard content (shown when OBB is loaded)
        self.dashboard_frame = QFrame()
        dashboard_layout = QVBoxLayout(self.dashboard_frame)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_layout.setSpacing(20)
        
        # Title
        self.obb_title_label = QLabel("")
        self.obb_title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #E5E7EB;")
        dashboard_layout.addWidget(self.obb_title_label)
        
        # Info cards grid
        cards_grid = QGridLayout()
        cards_grid.setSpacing(15)
        
        # Create info cards
        self.cards = {}
        card_info = [
            ("OBB Size", "0 MB"),
            ("IFF Files", "0"),
            ("Resources", "0"),
            ("Textures", "0"),
            ("Models", "0"),
            ("Players", "0"),
            ("Teams", "0"),
            ("Headshapes", "0"),
        ]
        
        row = 0
        col = 0
        for title, value in card_info:
            card = InfoCard(title, value)
            self.cards[title] = card
            cards_grid.addWidget(card, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        dashboard_layout.addLayout(cards_grid)
        
        # Quick actions
        actions_label = QLabel("Quick Actions")
        actions_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #E5E7EB; margin-top: 20px;")
        dashboard_layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        self.extract_btn = QPushButton("Extract All")
        self.extract_btn.clicked.connect(self._extract_all_clicked)
        actions_layout.addWidget(self.extract_btn)
        
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self._analyze_obb_clicked)
        actions_layout.addWidget(self.analyze_btn)
        
        self.rebuild_btn = QPushButton("Rebuild OBB")
        self.rebuild_btn.clicked.connect(self._rebuild_obb_clicked)
        actions_layout.addWidget(self.rebuild_btn)
        
        dashboard_layout.addLayout(actions_layout)
        dashboard_layout.addStretch()
        
        content_layout.addWidget(self.dashboard_frame)
        
        # Initially hide dashboard frame
        self.dashboard_frame.hide()
        
        layout.addWidget(scroll)
    
    def _open_obb_clicked(self):
        """Handle open OBB button click."""
        if hasattr(self.main_window, 'open_obb'):
            self.main_window.open_obb()
    
    def _extract_all_clicked(self):
        """Handle extract all button click."""
        if hasattr(self.main_window, 'extract_all'):
            self.main_window.extract_all()
    
    def _analyze_obb_clicked(self):
        """Handle analyze OBB button click."""
        if hasattr(self.main_window, 'analyze_obb'):
            self.main_window.analyze_obb()
    
    def _rebuild_obb_clicked(self):
        """Handle rebuild OBB button click."""
        if hasattr(self.main_window, 'rebuild_obb'):
            self.main_window.rebuild_obb()
    
    def load_obb_data(self, obb_data):
        """Load OBB data into dashboard."""
        
        self.welcome_frame.hide()
        self.dashboard_frame.show()
        
        # Update title - handle both file_path and obb_path attributes
        import os
        file_path = getattr(obb_data, 'file_path', None)
        if file_path is None:
            file_path = getattr(obb_data, 'obb_path', None)
        
        if file_path:
            self.obb_title_label.setText(os.path.basename(str(file_path)))
        else:
            self.obb_title_label.setText("Unknown OBB")
        
        # Update cards
        if hasattr(obb_data, 'file_size'):
            size_mb = obb_data.file_size / (1024 * 1024)
            self.cards["OBB Size"].set_value(f"{size_mb:.1f} MB")
        
        if hasattr(obb_data, 'iff_files'):
            self.cards["IFF Files"].set_value(str(len(obb_data.iff_files)))
        
        if hasattr(obb_data, 'resources'):
            self.cards["Resources"].set_value(str(len(obb_data.resources)))
        
        if hasattr(obb_data, 'textures'):
            self.cards["Textures"].set_value(str(len(obb_data.textures)))
        
        if hasattr(obb_data, 'models'):
            self.cards["Models"].set_value(str(len(obb_data.models)))
        
        if hasattr(obb_data, 'players'):
            self.cards["Players"].set_value(str(len(obb_data.players)))
        
        if hasattr(obb_data, 'teams'):
            self.cards["Teams"].set_value(str(len(obb_data.teams)))
        
        if hasattr(obb_data, 'headshapes'):
            self.cards["Headshapes"].set_value(str(len(obb_data.headshapes)))
    
    def reset(self):
        """Reset dashboard to initial state."""
        
        self.dashboard_frame.hide()
        self.welcome_frame.show()
