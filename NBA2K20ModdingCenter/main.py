"""
NBA 2K20 Mobile Modding Center
Main entry point for the application.
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from app.main_window import MainWindow
from app.theme import apply_theme


def main():
    """Main entry point for the application."""
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("NBA 2K20 Mobile Modding Center")
    app.setOrganizationName("NBA2K20Modding")
    app.setStyle("Fusion")
    
    # Apply dark theme
    apply_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
