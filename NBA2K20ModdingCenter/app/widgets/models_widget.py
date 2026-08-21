"""
Models widget for viewing and managing 3D models.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QSplitter, QGroupBox, QScrollArea,
    QHeaderView, QFileDialog, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt


class ModelsWidget(QWidget):
    """Widget for viewing and managing 3D models."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        self.models_data = []
        self.current_model = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Model list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search models...")
        toolbar_layout.addWidget(self.search_box)
        
        toolbar_layout.addStretch()
        
        left_layout.addLayout(toolbar_layout)
        
        # Models table
        self.models_table = QTableWidget()
        self.models_table.setColumnCount(5)
        self.models_table.setHorizontalHeaderLabels([
            "Name", "Vertices", "Faces", "Meshes", "Bones"
        ])
        self.models_table.setAlternatingRowColors(True)
        self.models_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.models_table.itemSelectionChanged.connect(self.on_model_selected)
        
        header = self.models_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        left_layout.addWidget(self.models_table)
        
        splitter.addWidget(left_widget)
        
        # Right panel - Model preview
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview group
        preview_group = QGroupBox("MODEL PREVIEW")
        preview_layout = QVBoxLayout(preview_group)
        
        # Placeholder for 3D view
        self.preview_label = QLabel("3D model preview will be displayed here")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            color: #9CA3AF;
            background-color: #181A1F;
            border: 1px solid #343840;
            padding: 50px;
        """)
        preview_layout.addWidget(self.preview_label)
        
        # Info label
        self.model_info_label = QLabel("No model selected")
        self.model_info_label.setAlignment(Qt.AlignCenter)
        self.model_info_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        preview_layout.addWidget(self.model_info_label)
        
        right_layout.addWidget(preview_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.export_obj_btn = QPushButton("Export OBJ")
        self.export_obj_btn.clicked.connect(self.export_obj)
        button_layout.addWidget(self.export_obj_btn)
        
        self.export_gltf_btn = QPushButton("Export glTF")
        self.export_gltf_btn.clicked.connect(self.export_gltf)
        button_layout.addWidget(self.export_gltf_btn)
        
        button_layout.addStretch()
        
        self.replace_btn = QPushButton("Replace")
        self.replace_btn.clicked.connect(self.replace_model)
        button_layout.addWidget(self.replace_btn)
        
        right_layout.addLayout(button_layout)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
    
    def load_obb_data(self, obb_data):
        """Load model data from OBB."""
        
        self.models_data = []
        self.models_table.setRowCount(0)
        
        # TODO: Actually parse model data from OBB
        
        self.main_window.add_log("INFO", "Loading model data...")
    
    def on_model_selected(self):
        """Handle model selection."""
        
        selected_rows = self.models_table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        
        # Load model preview
        # TODO: Implement actual loading
    
    def export_obj(self):
        """Export model as OBJ."""
        
        if not self.current_model:
            QMessageBox.warning(self, "No Model", "Please select a model first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export OBJ",
            "model.obj",
            "OBJ Files (*.obj)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Exporting model to {file_path}")
    
    def export_gltf(self):
        """Export model as glTF."""
        
        if not self.current_model:
            QMessageBox.warning(self, "No Model", "Please select a model first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export glTF",
            "model.gltf",
            "glTF Files (*.gltf *.glb)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Exporting model to {file_path}")
    
    def replace_model(self):
        """Replace model from file."""
        
        if not self.current_model:
            QMessageBox.warning(self, "No Model", "Please select a model first.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Model",
            "",
            "Models (*.obj *.gltf *.glb);;All Files (*)"
        )
        
        if file_path:
            self.main_window.add_log("INFO", f"Replacing model from {file_path}")
