"""
Theme configuration for NBA 2K20 Mobile Modding Center.
Professional dark theme inspired by engineering/modding software.
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor


# Color palette - Dark theme (default)
DARK_COLORS = {
    "bg_primary": "#181A1F",
    "bg_secondary": "#22252B",
    "bg_tertiary": "#2D3139",
    "border": "#343840",
    "text_primary": "#E5E7EB",
    "text_secondary": "#9CA3AF",
    "accent": "#B91C1C",
    "accent_hover": "#DC2626",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6",
}

LIGHT_COLORS = {
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F3F4F6",
    "bg_tertiary": "#E5E7EB",
    "border": "#D1D5DB",
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "accent": "#B91C1C",
    "accent_hover": "#DC2626",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6",
}


def apply_theme(app: QApplication, theme: str = "dark"):
    """Apply theme to the application."""
    
    if theme == "light":
        colors = LIGHT_COLORS
    else:
        colors = DARK_COLORS
    
    palette = QPalette()
    
    # Base colors
    palette.setColor(QPalette.Window, QColor(colors["bg_primary"]))
    palette.setColor(QPalette.WindowText, QColor(colors["text_primary"]))
    palette.setColor(QPalette.Base, QColor(colors["bg_secondary"]))
    palette.setColor(QPalette.AlternateBase, QColor(colors["bg_tertiary"]))
    palette.setColor(QPalette.ToolTipBase, QColor(colors["bg_primary"]))
    palette.setColor(QPalette.ToolTipText, QColor(colors["text_primary"]))
    palette.setColor(QPalette.Text, QColor(colors["text_primary"]))
    palette.setColor(QPalette.Button, QColor(colors["bg_secondary"]))
    palette.setColor(QPalette.ButtonText, QColor(colors["text_primary"]))
    palette.setColor(QPalette.BrightText, QColor(colors["text_primary"]))
    palette.setColor(QPalette.Link, QColor(colors["info"]))
    palette.setColor(QPalette.Highlight, QColor(colors["accent"]))
    palette.setColor(QPalette.HighlightedText, QColor(colors["text_primary"]))
    
    app.setPalette(palette)
    
    # Apply stylesheet for more detailed styling
    stylesheet = f"""
    QMainWindow {{
        background-color: {colors["bg_primary"]};
    }}
    
    QWidget {{
        background-color: {colors["bg_primary"]};
        color: {colors["text_primary"]};
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }}
    
    QMenuBar {{
        background-color: {colors["bg_secondary"]};
        color: {colors["text_primary"]};
        border-bottom: 1px solid {colors["border"]};
        padding: 2px;
    }}
    
    QMenuBar::item {{
        padding: 4px 8px;
        border-radius: 3px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {colors["bg_tertiary"]};
    }}
    
    QMenu {{
        background-color: {colors["bg_secondary"]};
        border: 1px solid {colors["border"]};
        border-radius: 5px;
        padding: 5px;
    }}
    
    QMenu::item {{
        padding: 6px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {colors["accent"]};
    }}
    
    QToolBar {{
        background-color: {colors["bg_secondary"]};
        border-bottom: 1px solid {colors["border"]};
        padding: 5px;
        spacing: 5px;
    }}
    
    QToolButton {{
        background-color: {colors["bg_secondary"]};
        border: 1px solid {colors["border"]};
        border-radius: 4px;
        padding: 6px 12px;
        color: {colors["text_primary"]};
    }}
    
    QToolButton:hover {{
        background-color: {colors["bg_tertiary"]};
        border-color: {colors["accent"]};
    }}
    
    QTabWidget::pane {{
        border: 1px solid {colors["border"]};
        border-radius: 5px;
        background-color: {colors["bg_primary"]};
    }}
    
    QTabBar::tab {{
        background-color: {colors["bg_secondary"]};
        color: {colors["text_secondary"]};
        padding: 8px 16px;
        border: 1px solid {colors["border"]};
        border-bottom: none;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {colors["bg_primary"]};
        color: {colors["text_primary"]};
        border-top: 2px solid {colors["accent"]};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {colors["bg_tertiary"]};
    }}
    
    QPushButton {{
        background-color: {colors["bg_tertiary"]};
        border: 1px solid {colors["border"]};
        border-radius: 4px;
        padding: 8px 16px;
        color: {colors["text_primary"]};
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {colors["bg_secondary"]};
        border-color: {colors["accent"]};
    }}
    
    QPushButton:pressed {{
        background-color: {colors["accent"]};
    }}
    
    QPushButton:disabled {{
        background-color: {colors["bg_tertiary"]};
        color: {colors["text_secondary"]};
        border-color: {colors["border"]};
    }}
    
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {colors["bg_secondary"]};
        border: 1px solid {colors["border"]};
        border-radius: 4px;
        padding: 6px 10px;
        color: {colors["text_primary"]};
        selection-background-color: {colors["accent"]};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {colors["accent"]};
    }}
    
    QTableWidget, QTreeWidget, QListWidget {{
        background-color: {colors["bg_secondary"]};
        alternate-background-color: {colors["bg_tertiary"]};
        border: 1px solid {colors["border"]};
        border-radius: 5px;
        gridline-color: {colors["border"]};
        selection-background-color: {colors["accent"]};
    }}
    
    QTableWidget::item, QTreeWidget::item, QListWidget::item {{
        padding: 4px;
        border-radius: 3px;
    }}
    
    QHeaderView::section {{
        background-color: {colors["bg_tertiary"]};
        color: {colors["text_primary"]};
        padding: 6px;
        border: 1px solid {colors["border"]};
        font-weight: bold;
    }}
    
    QScrollBar:vertical {{
        background-color: {colors["bg_secondary"]};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors["bg_tertiary"]};
        border-radius: 6px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors["accent"]};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {colors["bg_secondary"]};
        height: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {colors["bg_tertiary"]};
        border-radius: 6px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {colors["accent"]};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    QProgressBar {{
        background-color: {colors["bg_tertiary"]};
        border: 1px solid {colors["border"]};
        border-radius: 5px;
        text-align: center;
        color: {colors["text_primary"]};
    }}
    
    QProgressBar::chunk {{
        background-color: {colors["accent"]};
        border-radius: 4px;
    }}
    
    QGroupBox {{
        border: 1px solid {colors["border"]};
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: {colors["text_primary"]};
    }}
    
    QLabel {{
        color: {colors["text_primary"]};
    }}
    
    QComboBox {{
        background-color: {colors["bg_secondary"]};
        border: 1px solid {colors["border"]};
        border-radius: 4px;
        padding: 6px 10px;
        color: {colors["text_primary"]};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {colors["bg_secondary"]};
        border: 1px solid {colors["border"]};
        selection-background-color: {colors["accent"]};
    }}
    
    QCheckBox::indicator {{
        border: 1px solid {colors["border"]};
        border-radius: 3px;
        width: 16px;
        height: 16px;
        background-color: {colors["bg_secondary"]};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {colors["accent"]};
    }}
    
    QRadioButton::indicator {{
        border: 1px solid {colors["border"]};
        border-radius: 8px;
        width: 16px;
        height: 16px;
        background-color: {colors["bg_secondary"]};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {colors["accent"]};
        border-color: {colors["accent"]};
    }}
    
    QStatusBar {{
        background-color: {colors["bg_secondary"]};
        border-top: 1px solid {colors["border"]};
        color: {colors["text_secondary"]};
    }}
    
    QSplitter::handle {{
        background-color: {colors["border"]};
    }}
    
    QSplitter::handle:horizontal {{
        width: 2px;
    }}
    
    QSplitter::handle:vertical {{
        height: 2px;
    }}
    
    /* Custom classes */
    .accent-button {{
        background-color: {colors["accent"]};
        color: white;
    }}
    
    .accent-button:hover {{
        background-color: {colors["accent_hover"]};
    }}
    
    .success-label {{
        color: {colors["success"]};
    }}
    
    .warning-label {{
        color: {colors["warning"]};
    }}
    
    .error-label {{
        color: {colors["error"]};
    }}
    
    .info-label {{
        color: {colors["info"]};
    }}
    
    .secondary-text {{
        color: {colors["text_secondary"]};
    }}
    
    QToolTip {{
        background-color: {colors["bg_tertiary"]};
        color: {colors["text_primary"]};
        border: 1px solid {colors["border"]};
        border-radius: 3px;
        padding: 4px;
    }}
    """
    
    app.setStyleSheet(stylesheet)
    
    return colors
