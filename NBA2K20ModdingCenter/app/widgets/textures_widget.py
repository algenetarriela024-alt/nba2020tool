"""
Textures widget for viewing and managing textures.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QSplitter, QGroupBox, QScrollArea,
    QHeaderView, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QFileDialog, QMessageBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage


class TexturesWidget(QWidget):
    """Widget for viewing and managing textures."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.textures_data = []
        self.current_texture = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Texture list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search textures...")
        toolbar_layout.addWidget(self.search_box)
        
        # Filter combo
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Textures")
        self.filter_combo.addItem("DXT1")
        self.filter_combo.addItem("DXT5")
        self.filter_combo.addItem("RGBA")
        toolbar_layout.addWidget(self.filter_combo)
        
        toolbar_layout.addStretch()
        
        left_layout.addLayout(toolbar_layout)
        
        # Textures table
        self.textures_table = QTableWidget()
        self.textures_table.setColumnCount(6)
        self.textures_table.setHorizontalHeaderLabels([
            "Name", "Width", "Height", "Format", "Size", "Mipmaps"
        ])
        self.textures_table.setAlternatingRowColors(True)
        self.textures_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.textures_table.itemSelectionChanged.connect(self.on_texture_selected)
        
        header = self.textures_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        left_layout.addWidget(self.textures_table)
        
        splitter.addWidget(left_widget)
        
        # Right panel - Texture preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview group
        preview_group = QGroupBox("TEXTURE PREVIEW")
        preview_layout = QVBoxLayout(preview_group)
        
        # Graphics view for preview
        self.preview_scene = QGraphicsScene()
        self.preview_view = QGraphicsView(self.preview_scene)
        self.preview_view.setAlignment(Qt.AlignCenter)
        self.preview_view.setStyleSheet("""
            QGraphicsView {
                background-color: #181A1F;
                border: 1px solid #343840;
            }
        """)
        preview_layout.addWidget(self.preview_view)
        
        # Info label
        self.preview_info_label = QLabel("No texture selected")
        self.preview_info_label.setAlignment(Qt.AlignCenter)
        self.preview_info_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        preview_layout.addWidget(self.preview_info_label)
        
        right_layout.addWidget(preview_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.export_png_btn = QPushButton("Export PNG")
        self.export_png_btn.clicked.connect(self.export_png)
        button_layout.addWidget(self.export_png_btn)
        
        self.export_dds_btn = QPushButton("Export DDS")
        self.export_dds_btn.clicked.connect(self.export_dds)
        button_layout.addWidget(self.export_dds_btn)
        
        button_layout.addStretch()
        
        self.replace_btn = QPushButton("Replace")
        self.replace_btn.clicked.connect(self.replace_texture)
        button_layout.addWidget(self.replace_btn)
        
        right_layout.addLayout(button_layout)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
    
    def load_obb_data(self, obb_data):
        """Load texture data from OBB."""
        
        self.textures_data = []
        self.textures_table.setRowCount(0)
        
        # TODO: Actually parse texture data from OBB
        
        self.main_window.add_log("INFO", "Loading texture data...")
    
    def on_texture_selected(self):
        """Handle texture selection."""
        
        selected_rows = self.textures_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        # Load texture preview
        # TODO: Implement actual loading
    
    def export_png(self):
        """Export texture as PNG."""
        
        if not self.current_texture:
            QMessageBox.warning(self, "No Texture", "Please select a texture first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export PNG",
            "texture.png",
            "PNG Files (*.png)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Exporting texture to {file_path}")
    
    def export_dds(self):
        """Export texture as DDS."""
        
        if not self.current_texture:
            QMessageBox.warning(self, "No Texture", "Please select a texture first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export DDS",
            "texture.dds",
            "DDS Files (*.dds)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Exporting texture to {file_path}")
    
    def replace_texture(self):
        """Replace texture from file."""
        
        if not self.current_texture:
            QMessageBox.warning(self, "No Texture", "Please select a texture first.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Texture",
            "",
            "Images (*.png *.dds);;All Files (*)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Replacing texture from {file_path}")
