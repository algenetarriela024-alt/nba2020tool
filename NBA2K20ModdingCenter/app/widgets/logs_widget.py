"""
Logs widget for viewing application logs.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel,
    QPushButton, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt


class LogsWidget(QWidget):
    """Widget for viewing application logs."""
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        
        self.main_window = main_window
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        # Filter combo
        toolbar_layout.addWidget(QLabel("Filter:"))
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("All Levels")
        self.filter_combo.addItem("INFO")
        self.filter_combo.addItem("DEBUG")
        self.filter_combo.addItem("WARNING")
        self.filter_combo.addItem("ERROR")
        self.filter_combo.addItem("CRITICAL")
        toolbar_layout.addWidget(self.filter_combo)
        
        # Auto-scroll checkbox
        self.auto_scroll_check = QCheckBox("Auto-scroll")
        self.auto_scroll_check.setChecked(True)
        toolbar_layout.addWidget(self.auto_scroll_check)
        
        toolbar_layout.addStretch()
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_logs)
        toolbar_layout.addWidget(self.clear_btn)
        
        # Export button
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_logs)
        toolbar_layout.addWidget(self.export_btn)
        
        layout.addLayout(toolbar_layout)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFontFamily("Consolas")
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #181A1F;
                color: #E5E7EB;
                border: 1px solid #343840;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        layout.addWidget(self.log_display)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.count_label = QLabel("Log entries: 0")
        status_layout.addWidget(self.count_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
    
    def add_log(self, entry: str):
        """Add a log entry."""
        
        self.log_display.append(entry)
        self.count_label.setText(f"Log entries: {self.log_display.document().blockCount()}")
        
        if self.auto_scroll_check.isChecked():
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def clear_logs(self):
        """Clear all logs."""
        
        self.log_display.clear()
        self.count_label.setText("Log entries: 0")
        self.main_window.add_log("INFO", "Logs cleared")
    
    def export_logs(self):
        """Export logs to file."""
        
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "logs.txt",
            "Text Files (*.txt)"
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.log_display.toPlainText())
            
            self.main_window.add_log("INFO", f"Logs exported to {file_path}")
