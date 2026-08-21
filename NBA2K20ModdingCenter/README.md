# NBA 2K20 Mobile Modding Center

A professional desktop application for modding NBA 2K20 Mobile Android game files.

## Features

- **OBB File Analysis**: Open and analyze NBA 2K20 Mobile OBB files
- **IFF File Parsing**: Parse and view IFF container files
- **Resource Detection**: Detect textures, models, and other resources
- **Hex Viewer**: View binary data in hexadecimal format
- **Database Editing**: Edit player and team databases
- **Texture Management**: Preview, export, and replace textures
- **3D Model Export**: Export models to OBJ, glTF formats
- **Safe Mode**: Never modifies original files without explicit confirmation
- **Workspace System**: Organized project structure with backups
- **Report Generation**: JSON and TXT analysis reports
- **Logging**: Detailed operation logs

## Requirements

- Python 3.12+
- PySide6
- numpy
- Pillow

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
NBA2K20ModdingCenter/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
│
├── app/                    # GUI components
│   ├── main_window.py      # Main application window
│   ├── theme.py            # Dark/Light theme configuration
│   ├── widgets/            # UI widgets
│   │   ├── dashboard.py
│   │   ├── obb_browser.py
│   │   ├── iff_viewer.py
│   │   ├── hex_viewer.py
│   │   ├── resource_analyzer.py
│   │   ├── players_widget.py
│   │   ├── teams_widget.py
│   │   ├── textures_widget.py
│   │   ├── models_widget.py
│   │   ├── logs_widget.py
│   │   └── search_widget.py
│   ├── dialogs/            # Dialog windows
│   └── models/             # Data models
│
├── core/                   # Core functionality
│   ├── obb/                # OBB file handling
│   │   ├── obb_reader.py
│   │   ├── obb_writer.py
│   │   └── obb_detector.py
│   ├── iff/                # IFF file handling
│   │   ├── iff_reader.py
│   │   ├── iff_writer.py
│   │   └── iff_block.py
│   ├── resources/          # Resource detection
│   ├── textures/           # Texture handling
│   ├── models3d/           # 3D model handling
│   ├── database/           # Database parsing
│   └── analysis/           # Analysis tools
│       └── report_generator.py
│
├── plugins/                # Plugin system
├── workspace/              # Project workspace
├── exports/                # Exported files
├── backups/                # File backups
├── reports/                # Analysis reports
└── tests/                  # Unit tests
```

## Development Phases

### Phase 1 (Implemented)
- PySide6 GUI framework
- OBB file opening and scanning
- IFF detection
- Hex viewer
- Workspace system
- Logging

### Phase 2 (Planned)
- Texture detection
- Texture preview
- Texture export/replacement

### Phase 3 (Planned)
- Database detection
- Player tables
- Team tables
- Player editor

### Phase 4 (Planned)
- Model detection
- 3D preview
- Model export/import

### Phase 5 (Planned)
- IFF rebuilding
- OBB rebuilding
- Validation

### Phase 6 (Planned)
- Advanced reverse-engineering tools
- Plugin system
- Automatic signatures
- Advanced asset classification

## Important Notes

1. **Format-Driven Parsing**: The application detects file structures from binary evidence, not filename assumptions.

2. **Original File Safety**: The original OBB is never modified directly. All modifications go through a workspace system.

3. **Unknown Format Handling**: Unknown resources are preserved and can be exported as raw binary data.

4. **Safe Mode**: Before any modification, the application requires explicit confirmation and creates backups.

## License

This tool is for educational and personal use only.

## Disclaimer

This software is not affiliated with or endorsed by Take-Two Interactive or 2K Sports.
