"""
Main window for NBA 2K20 Mobile Modding Center.
Professional interface inspired by RED Modding Center.
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QStatusBar, QToolBar, QMenuBar, QMenu,
    QLabel, QFrame, QFileDialog, QMessageBox, QDialog, QProgressBar,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QApplication, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, Slot, QThread, QSize
from PySide6.QtGui import QIcon, QFont, QKeySequence, QAction

from app.widgets.dashboard import DashboardWidget
from app.widgets.obb_browser import OBBBrowserWidget
from app.widgets.iff_viewer import IFFViewerWidget
from app.widgets.hex_viewer import HexViewerWidget
from app.widgets.resource_analyzer import ResourceAnalyzerWidget
from app.widgets.players_widget import PlayersWidget
from app.widgets.teams_widget import TeamsWidget
from app.widgets.textures_widget import TexturesWidget
from app.widgets.models_widget import ModelsWidget
from app.widgets.logs_widget import LogsWidget
from app.widgets.search_widget import SearchWidget
from core.analysis.report_generator import ReportGenerator


class WorkerThread(QThread):
    """Worker thread for background operations."""
    
    progress = Signal(int, str)
    finished = Signal(object)
    error = Signal(str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Application state
        self.current_obb_path = None
        self.obb_data = None
        self.workspace_path = None
        self.modified_files = {}
        self.log_entries = []
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        self.connect_signals()
        
        # Set window properties
        self.setWindowTitle("NBA 2K20 Mobile Modding Center")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
    
    def setup_ui(self):
        """Setup the main UI components."""
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Create tabs
        self.setup_tabs()
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_tabs(self):
        """Create all application tabs."""
        
        # Dashboard tab
        self.dashboard_tab = DashboardWidget(self)
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        
        # OBB Files tab
        self.obb_browser_tab = OBBBrowserWidget(self)
        self.tab_widget.addTab(self.obb_browser_tab, "OBB Files")
        
        # IFF Viewer tab
        self.iff_viewer_tab = IFFViewerWidget(self)
        self.tab_widget.addTab(self.iff_viewer_tab, "IFF")
        
        # Resources tab
        self.resource_analyzer_tab = ResourceAnalyzerWidget(self)
        self.tab_widget.addTab(self.resource_analyzer_tab, "Resources")
        
        # Players tab
        self.players_tab = PlayersWidget(self)
        self.tab_widget.addTab(self.players_tab, "Players")
        
        # Teams tab
        self.teams_tab = TeamsWidget(self)
        self.tab_widget.addTab(self.teams_tab, "Teams")
        
        # Textures tab
        self.textures_tab = TexturesWidget(self)
        self.tab_widget.addTab(self.textures_tab, "Textures")
        
        # Models tab
        self.models_tab = ModelsWidget(self)
        self.tab_widget.addTab(self.models_tab, "Models")
        
        # Search tab
        self.search_tab = SearchWidget(self)
        self.tab_widget.addTab(self.search_tab, "Search")
        
        # Logs tab
        self.logs_tab = LogsWidget(self)
        self.tab_widget.addTab(self.logs_tab, "Logs")
        
        # Set dashboard as current
        self.tab_widget.setCurrentIndex(0)
    
    def setup_menu(self):
        """Create menu bar."""
        
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        self.open_obb_action = QAction("&Open OBB", self)
        self.open_obb_action.setShortcut(QKeySequence.Open)
        self.open_obb_action.triggered.connect(self.open_obb)
        file_menu.addAction(self.open_obb_action)
        
        self.open_workspace_action = QAction("Open &Workspace", self)
        self.open_workspace_action.triggered.connect(self.open_workspace)
        file_menu.addAction(self.open_workspace_action)
        
        file_menu.addSeparator()
        
        self.recent_obbs_menu = file_menu.addMenu("Recent OBBs")
        
        file_menu.addSeparator()
        
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.save_workspace)
        file_menu.addAction(self.save_action)
        
        self.save_as_action = QAction("Save &As...", self)
        self.save_as_action.triggered.connect(self.save_workspace_as)
        file_menu.addAction(self.save_as_action)
        
        file_menu.addSeparator()
        
        self.extract_selected_action = QAction("E&xtract Selected", self)
        self.extract_selected_action.triggered.connect(self.extract_selected)
        file_menu.addAction(self.extract_selected_action)
        
        self.extract_all_action = QAction("Extract &All", self)
        self.extract_all_action.triggered.connect(self.extract_all)
        file_menu.addAction(self.extract_all_action)
        
        file_menu.addSeparator()
        
        self.rebuild_obb_action = QAction("&Rebuild OBB", self)
        self.rebuild_obb_action.triggered.connect(self.rebuild_obb)
        file_menu.addAction(self.rebuild_obb_action)
        
        self.close_obb_action = QAction("&Close OBB", self)
        self.close_obb_action.triggered.connect(self.close_obb)
        file_menu.addAction(self.close_obb_action)
        
        file_menu.addSeparator()
        
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.Undo)
        edit_menu.addAction(self.undo_action)
        
        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.Redo)
        edit_menu.addAction(self.redo_action)
        
        edit_menu.addSeparator()
        
        self.find_action = QAction("&Find", self)
        self.find_action.setShortcut(QKeySequence.Find)
        self.find_action.triggered.connect(lambda: self.tab_widget.setCurrentWidget(self.search_tab))
        edit_menu.addAction(self.find_action)
        
        # Advanced menu
        advanced_menu = menubar.addMenu("&Advanced")
        
        self.analyze_action = QAction("&Analyze OBB", self)
        self.analyze_action.triggered.connect(self.analyze_obb)
        advanced_menu.addAction(self.analyze_action)
        
        self.developer_mode_action = QAction("Developer &Mode", self)
        self.developer_mode_action.setCheckable(True)
        self.developer_mode_action.triggered.connect(self.toggle_developer_mode)
        advanced_menu.addAction(self.developer_mode_action)
        
        # IFF menu
        iff_menu = menubar.addMenu("&IFF")
        
        self.open_iff_action = QAction("&Open IFF", self)
        self.open_iff_action.triggered.connect(self.open_iff)
        iff_menu.addAction(self.open_iff_action)
        
        self.analyze_iff_action = QAction("&Analyze IFF", self)
        self.analyze_iff_action.triggered.connect(self.analyze_iff)
        iff_menu.addAction(self.analyze_iff_action)
        
        iff_menu.addSeparator()
        
        self.extract_iff_action = QAction("E&xtract IFF", self)
        self.extract_iff_action.triggered.connect(self.extract_iff)
        iff_menu.addAction(self.extract_iff_action)
        
        self.rebuild_iff_action = QAction("&Rebuild IFF", self)
        self.rebuild_iff_action.triggered.connect(self.rebuild_iff)
        iff_menu.addAction(self.rebuild_iff_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.hex_view_action = QAction("&Hex Viewer", self)
        self.hex_view_action.triggered.connect(self.show_hex_viewer)
        view_menu.addAction(self.hex_view_action)
        
        self.property_inspector_action = QAction("&Property Inspector", self)
        self.property_inspector_action.setCheckable(True)
        self.property_inspector_action.setChecked(True)
        view_menu.addAction(self.property_inspector_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        self.compare_files_action = QAction("&Compare Files", self)
        self.compare_files_action.triggered.connect(self.compare_files)
        tools_menu.addAction(self.compare_files_action)
        
        tools_menu.addSeparator()
        
        self.export_report_action = QAction("Export &Report", self)
        self.export_report_action.triggered.connect(self.export_report)
        tools_menu.addAction(self.export_report_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self.show_about)
        help_menu.addAction(self.about_action)
    
    def setup_toolbar(self):
        """Create toolbar."""
        
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(toolbar)
        
        # Add toolbar actions
        toolbar.addAction(self.open_obb_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.extract_all_action)
        toolbar.addSeparator()
        toolbar.addAction(self.find_action)
        toolbar.addSeparator()
        toolbar.addAction(self.analyze_action)
        toolbar.addSeparator()
        toolbar.addAction(self.rebuild_obb_action)
    
    def setup_statusbar(self):
        """Create status bar."""
        
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        statusbar.addWidget(self.status_label)
        
        statusbar.addPermanentWidget(QLabel("|"))
        
        # OBB info
        self.obb_info_label = QLabel("OBB: None")
        statusbar.addPermanentWidget(self.obb_info_label)
        
        statusbar.addPermanentWidget(QLabel("|"))
        
        # Workspace info
        self.workspace_info_label = QLabel("Workspace: None")
        statusbar.addPermanentWidget(self.workspace_info_label)
        
        statusbar.addPermanentWidget(QLabel("|"))
        
        # File count
        self.file_count_label = QLabel("Files: 0")
        statusbar.addPermanentWidget(self.file_count_label)
        
        statusbar.addPermanentWidget(QLabel("|"))
        
        # Resource count
        self.resource_count_label = QLabel("Resources: 0")
        statusbar.addPermanentWidget(self.resource_count_label)
    
    def connect_signals(self):
        """Connect signals and slots."""
        pass
    
    @Slot()
    def open_obb(self):
        """Open an OBB file."""
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open OBB File",
            "",
            "OBB Files (*.obb);;All Files (*)"
        )
        
        if file_path:
            self.load_obb(file_path)
    
    def load_obb(self, file_path: str):
        """Load an OBB file."""
        
        self.set_status(f"Opening OBB: {os.path.basename(file_path)}")
        
        # Create worker thread
        self.worker = WorkerThread(self._load_obb_worker, file_path)
        self.worker.progress.connect(self.on_load_progress)
        self.worker.finished.connect(self.on_obb_loaded)
        self.worker.error.connect(self.on_load_error)
        self.worker.start()
        
        # Show progress dialog
        self.progress_dialog = QDialog(self)
        self.progress_dialog.setWindowTitle("Opening OBB...")
        self.progress_dialog.setModal(True)
        
        layout = QVBoxLayout(self.progress_dialog)
        
        self.progress_label = QLabel("Scanning file structure...")
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.progress_dialog.show()
    
    def _load_obb_worker(self, file_path: str):
        """Worker function to load OBB in background."""
        
        from core.obb.obb_reader import ObbParser, EntryType
        
        parser = ObbParser(file_path)
        
        if not parser.open():
            raise Exception("Failed to parse OBB file")
        
        # Step 1: Basic scan
        self.worker.progress.emit(10, "Scanning file structure...")
        
        # Step 2: Detect IFF files
        self.worker.progress.emit(30, "Detecting IFF files...")
        
        # Step 3: Detect resource blocks
        self.worker.progress.emit(50, "Detecting resource blocks...")
        
        # Step 4: Scan textures
        self.worker.progress.emit(70, "Scanning textures...")
        
        # Step 5: Build asset index - convert parser entries to expected format
        self.worker.progress.emit(90, "Building asset index...")
        
        # Convert ObbParser entries to the format expected by UI
        files_list = []
        for entry in parser.get_entry_list():
            # Determine file type
            if entry.entry_type == EntryType.IFF:
                file_type = "IFF"
            elif entry.entry_type == EntryType.BIN:
                file_type = "BIN"
            else:
                file_type = entry.entry_type.name
            
            # Try to extract actual data to check for IFF signature
            try:
                data = parser.extract_entry(entry.index)
                if data and data[:4] == b'IFF.':
                    file_type = "IFF"
            except:
                pass
            
            file_info = {
                'name': f"{file_type}_{entry.index:04d}",
                'type': file_type,
                'offset': entry.offset,
                'size': entry.decompressed_size if entry.decompressed_size > 0 else entry.compressed_size,
                'compression': 'ZLIB' if entry.is_compressed else 'None',
                'status': 'OK',
                'index': entry.index,
                'entry': entry,
                'parser': parser
            }
            files_list.append(file_info)
        
        self.worker.progress.emit(100, "Analysis complete")
        
        # Attach files list and parser to the parser object
        parser.files = files_list
        
        return parser
    
    @Slot(int, str)
    def on_load_progress(self, value: int, message: str):
        """Handle load progress."""
        
        self.progress_bar.setValue(value)
        self.progress_label.setText(message)
    
    @Slot(object)
    def on_obb_loaded(self, reader):
        """Handle OBB loaded successfully."""
        
        self.progress_dialog.accept()
        
        self.current_obb_path = str(reader.obb_path) if hasattr(reader, "obb_path") else None
        self.obb_data = reader
        
        # Update UI
        self.update_statusbar()
        self.update_tabs()
        
        # Create workspace
        self.create_workspace()
        
        # Generate report
        self.generate_report()
        
        obb_name = os.path.basename(str(reader.obb_path)) if hasattr(reader, "obb_path") else "unknown.obb"
        self.set_status(f"Successfully opened: {obb_name}")
        
        # Switch to dashboard
        self.tab_widget.setCurrentIndex(0)
    
    @Slot(str)
    def on_load_error(self, error: str):
        """Handle load error."""
        
        self.progress_dialog.reject()
        
        QMessageBox.critical(
            self,
            "Error Opening OBB",
            f"Failed to open OBB file:\n\n{error}"
        )
        
        self.set_status("Error opening OBB")
    
    def create_workspace(self):
        """Create workspace directory structure."""
        
        if not self.current_obb_path:
            return
        
        base_name = os.path.splitext(os.path.basename(self.current_obb_path))[0]
        workspace_name = f"NBA2K20_{base_name}"
        
        self.workspace_path = os.path.join("workspace", workspace_name)
        
        # Create directories
        dirs = [
            self.workspace_path,
            os.path.join(self.workspace_path, "extracted"),
            os.path.join(self.workspace_path, "modified"),
            os.path.join(self.workspace_path, "exports"),
            os.path.join(self.workspace_path, "backups"),
            os.path.join(self.workspace_path, "reports"),
            os.path.join(self.workspace_path, "cache"),
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
        
        # Backup original
        backup_dir = os.path.join(self.workspace_path, "backups", "original")
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy original OBB to backups (read-only reference)
        # Note: We don't actually copy, just note the location
        
        self.workspace_info_label.setText(f"Workspace: {workspace_name}")
    
    def update_statusbar(self):
        """Update status bar information."""
        
        if self.obb_data:
            file_size = os.path.getsize(self.current_obb_path)
            size_str = self.format_size(file_size)
            
            self.obb_info_label.setText(f"OBB: {os.path.basename(self.current_obb_path)} ({size_str})")
            
            # Try different attribute names for compatibility
            file_count = 0
            if hasattr(self.obb_data, 'files'):
                file_count = len(self.obb_data.files)
            elif hasattr(self.obb_data, 'entry_count'):
                file_count = self.obb_data.entry_count
            elif hasattr(self.obb_data, 'get_entry_list'):
                file_count = len(list(self.obb_data.get_entry_list()))
            self.file_count_label.setText(f"Files: {file_count}")
            
            resource_count = len(self.obb_data.resources) if hasattr(self.obb_data, 'resources') else 0
            self.resource_count_label.setText(f"Resources: {resource_count}")
    
    def update_tabs(self):
        """Update all tabs with new data."""
        
        if self.obb_data:
            self.obb_browser_tab.load_obb_data(self.obb_data)
            self.dashboard_tab.load_obb_data(self.obb_data)
            self.textures_tab.load_obb_data(self.obb_data)
            self.models_tab.load_obb_data(self.obb_data)
            self.players_tab.load_obb_data(self.obb_data)
            self.teams_tab.load_obb_data(self.obb_data)
    
    def generate_report(self):
        """Generate analysis report."""
        
        if not self.obb_data or not self.workspace_path:
            return
        
        generator = ReportGenerator(self.obb_data, self.workspace_path)
        generator.generate_all_reports()
    
    @Slot()
    def save_workspace(self):
        """Save current workspace."""
        
        if not self.workspace_path:
            self.save_workspace_as()
            return
        
        # Save project state
        self._save_project_state()
        
        self.set_status("Workspace saved")
    
    @Slot()
    def save_workspace_as(self):
        """Save workspace to a new location."""
        
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Workspace Directory",
            ""
        )
        
        if dir_path:
            self.workspace_path = dir_path
            self._save_project_state()
            self.workspace_info_label.setText(f"Workspace: {os.path.basename(dir_path)}")
            self.set_status("Workspace saved")
    
    def _save_project_state(self):
        """Save project state to JSON."""
        
        import json
        
        if not self.workspace_path:
            return
        
        state = {
            "obb_path": self.current_obb_path,
            "modified_files": list(self.modified_files.keys()),
            "timestamp": str(__import__('datetime').datetime.now()),
        }
        
        state_file = os.path.join(self.workspace_path, "project.json")
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    @Slot()
    def extract_selected(self):
        """Extract selected files."""
        
        if not self.obb_data:
            QMessageBox.warning(self, "No OBB", "Please open an OBB file first.")
            return
        
        # Get selected files from browser
        selected = self.obb_browser_tab.get_selected_files()
        
        if not selected:
            QMessageBox.information(self, "No Selection", "No files selected for extraction.")
            return
        
        # Extract files
        self.obb_data.extract_files(selected, self.workspace_path)
        
        self.set_status(f"Extracted {len(selected)} files")
    
    @Slot()
    def extract_all(self):
        """Extract all files."""
        
        if not self.obb_data:
            QMessageBox.warning(self, "No OBB", "Please open an OBB file first.")
            return
        
        # Extract all files
        self.obb_data.extract_all(self.workspace_path)
        
        self.set_status("All files extracted")
    
    @Slot()
    def rebuild_obb(self):
        """Rebuild modified OBB."""
        
        if not self.obb_data:
            QMessageBox.warning(self, "No OBB", "Please open an OBB file first.")
            return
        
        # Confirm safe mode
        reply = QMessageBox.question(
            self,
            "Rebuild OBB",
            "The original OBB will not be overwritten.\n\nCreate modified copy?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Rebuild OBB
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Modified OBB",
                "NBA2K20_MODDED.obb",
                "OBB Files (*.obb)"
            )
            
            if output_path:
                self.obb_data.rebuild(output_path, self.modified_files)
                self.set_status(f"Rebuilt OBB: {output_path}")
    
    @Slot()
    def close_obb(self):
        """Close current OBB."""
        
        if self.obb_data:
            self.current_obb_path = None
            self.obb_data = None
            self.workspace_path = None
            self.modified_files.clear()
            
            self.update_statusbar()
            self.dashboard_tab.reset()
            
            self.set_status("OBB closed")
    
    @Slot()
    def analyze_obb(self):
        """Analyze current OBB."""
        
        if not self.obb_data:
            return
        
        # Re-analyze
        self.load_obb(self.current_obb_path)
    
    @Slot()
    def toggle_developer_mode(self, checked: bool):
        """Toggle developer mode."""
        
        # Pass to all widgets
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if hasattr(widget, 'set_developer_mode'):
                widget.set_developer_mode(checked)
    
    @Slot()
    def open_workspace(self):
        """Open existing workspace."""
        
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Workspace Directory",
            ""
        )
        
        if dir_path:
            self.workspace_path = dir_path
            self.workspace_info_label.setText(f"Workspace: {os.path.basename(dir_path)}")
            self.set_status(f"Opened workspace: {os.path.basename(dir_path)}")
    
    @Slot()
    def open_iff(self):
        """Open IFF file."""
        
        if not self.obb_data:
            QMessageBox.warning(self, "No OBB", "Please open an OBB file first.")
            return
        
        # Get selected IFF from browser
        selected_iff = self.obb_browser_tab.get_selected_iff()
        
        if selected_iff:
            self.iff_viewer_tab.load_iff(selected_iff)
            self.tab_widget.setCurrentWidget(self.iff_viewer_tab)
    
    @Slot()
    def analyze_iff(self):
        """Analyze selected IFF."""
        
        pass
    
    @Slot()
    def extract_iff(self):
        """Extract selected IFF."""
        
        pass
    
    @Slot()
    def rebuild_iff(self):
        """Rebuild selected IFF."""
        
        pass
    
    @Slot()
    def show_hex_viewer(self):
        """Show hex viewer."""
        
        pass
    
    @Slot()
    def compare_files(self):
        """Compare two files."""
        
        pass
    
    @Slot()
    def export_report(self):
        """Export analysis report."""
        
        if not self.workspace_path:
            return
        
        # Export reports
        report_dir = os.path.join(self.workspace_path, "reports")
        
        QMessageBox.information(
            self,
            "Report Exported",
            f"Reports exported to:\n{report_dir}"
        )
    
    @Slot()
    def show_about(self):
        """Show about dialog."""
        
        QMessageBox.about(
            self,
            "About NBA 2K20 Mobile Modding Center",
            "<h2>NBA 2K20 Mobile Modding Center</h2>"
            "<p>Version 1.0.0</p>"
            "<p>A professional modding tool for NBA 2K20 Mobile Android.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>OBB file analysis and extraction</li>"
            "<li>IFF file parsing and editing</li>"
            "<li>Resource detection and analysis</li>"
            "<li>Texture preview and replacement</li>"
            "<li>3D model export</li>"
            "<li>Database editing</li>"
            "</ul>"
        )
    
    def set_status(self, message: str):
        """Set status bar message."""
        
        self.status_label.setText(f"Status: {message}")
        QApplication.processEvents()
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size."""
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        
        return f"{size_bytes:.1f} TB"
    
    def close_tab(self, index: int):
        """Handle tab close request."""
        
        # Don't close essential tabs
        if index == 0:  # Dashboard
            return
        
        self.tab_widget.removeTab(index)
    
    def add_log(self, level: str, message: str):
        """Add log entry."""
        
        timestamp = __import__('datetime').datetime.now().strftime("%H:%M:%S")
        entry = f"[{level}] {timestamp} - {message}"
        
        self.log_entries.append(entry)
        self.logs_tab.add_log(entry)
