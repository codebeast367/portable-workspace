# Portable Workspace

A smart, secure, and adaptive USB-based workspace system that allows students to recreate their personalized computing environment on different computers without carrying a heavy laptop every day.

## Overview

Students often have access to college computer labs, but each computer may have a different software environment and configuration. Setting up development tools, files, applications, extensions, browser tabs, and personal preferences repeatedly is inconvenient and time-consuming.

**Portable Workspace** addresses this problem by storing a portable representation of a user's workspace on a USB device.

When the USB is connected to another computer, the system:

1. Detects the host computer's operating system and available resources.
2. Detects available applications and tools.
3. Reads the user's workspace configuration.
4. Restores selected files and settings.
5. Recreates the user's VS Code development environment.
6. Uses portable or isolated applications where possible.
7. Works within the host computer's security and hardware restrictions.
8. Provides a temporary workspace that can eventually support saving or discarding session changes.

The goal is not to replace the host operating system, but to provide an **adaptive workspace layer** on top of it.

---

## Key Features

### Workspace Portability
Store a user's workspace configuration and selected files on a portable USB device for use across different computers.

### Application Detection
Detect whether required applications are available on the host system, including:
- Visual Studio Code
- Git
- Python
- Node.js
- Other supported development tools

The system can determine:
- Whether an application exists
- Its executable path
- Its installed version
- Whether the application can be used in the current environment

### Workspace Restoration
Restore selected workspace files from the USB to a temporary host workspace. The restoration system is designed to avoid modifying unrelated host files.

### VS Code Environment
Recreate the user's development environment, including:
- Settings & preferences
- Keybindings
- Snippets
- Extensions
- Projects
- Workspace configuration

### Settings Restoration
Restore supported application configurations without unnecessarily overwriting the host user's permanent settings.

### Session Management
Temporary workspace with support for saving or discarding session changes:

```text
USB Workspace
      ↓
Host Detection
      ↓
Temporary Session
      ↓
Workspace Restoration
      ↓
User Works
      ↓
Save / Discard
```

### Security
- Encrypted snapshots using password-based encryption
- PBKDF2 key derivation (390,000 iterations)
- Fernet symmetric encryption
- Secure password handling with getpass

---

## Project Structure

```
portable-workspace/
├── README.md                          # This file
├── launcher/                          # Main application
│   ├── main.py                       # Entry point with CLI menu
│   ├── config.py                     # Configuration and paths
│   ├── session.py                    # Workspace session management
│   ├── cleanup.py                    # Cleanup utilities
│   ├── snapshot.py                   # Snapshot creation and encryption
│   ├── security.py                   # Encryption/decryption utilities
│   ├── system.py                     # System utilities
│   ├── file_ops.py                   # File operations
│   └── restore/                      # Restoration modules
│       ├── __init__.py
│       ├── manager.py                # Restoration orchestrator
│       ├── app_detector.py           # Application detection
│       ├── file_restore.py           # File restoration
│       ├── settings_restore.py       # Settings restoration
│       ├── vscode_restore.py         # VS Code environment restoration
│       └── models.py                 # Data models and classes
├── workspace/                        # Workspace capture and storage
│   ├── __init__.py
│   ├── config.json                  # Workspace configuration
│   ├── capture/                     # Capture modules
│   │   ├── __init__.py
│   │   ├── files.py                 # File capture
│   │   ├── settings.py              # Settings capture
│   │   ├── snapshot.py              # Snapshot capture
│   │   └── wallpaper.py             # Wallpaper capture
│   ├── files/                       # Captured workspace files
│   ├── settings/                    # Captured application settings
│   ├── apps/                        # Application definitions
│   └── .security/                   # Encrypted snapshots
├── tests/                           # Comprehensive test suite
│   ├── __init__.py
│   ├── test_cleanup.py
│   ├── test_security.py
│   ├── test_session.py
│   ├── test_snapshot.py
│   ├── capture/
│   │   ├── __init__.py
│   │   ├── test_files.py
│   │   ├── test_settings.py
│   │   ├── test_snapshot.py
│   │   ├── test_wallpaper.py
│   │   ├── sample_settings/         # Test fixture data
│   │   ├── sample_snapshot/
│   │   ├── sample_wallpaper/
│   │   └── sample_workspace/
│   └── restore/
│       ├── __init__.py
│       ├── test_app_detector.py
│       ├── test_file_restore.py
│       ├── test_settings_restore.py
│       └── test_vscode_restore.py
└── backup/                          # Backup directory (created at runtime)
```

---

## Installation & Setup

### Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux
- Dependencies: `cryptography` library for encryption features

### Quick Start

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd portable-workspace
   ```

2. **Install dependencies:**
   ```bash
   pip install cryptography
   ```

3. **Run the application:**
   ```bash
   cd launcher
   python main.py
   ```

The application will display a menu with various options to manage your workspace.

---

## Usage & Getting Started

### Starting the Application

From the `launcher` directory:
```bash
python main.py
```

### Main Menu Options

#### 1. **Capture File**
Capture a single file from your computer into the portable workspace.
- Input: Full path to the file to capture
- Result: File is copied to `workspace/files/`

#### 2. **Restore File**
Restore a previously captured file to a destination on your computer.
- Input: File name to restore and destination folder path
- Result: File is copied from `workspace/files/` to the destination

#### 3. **Capture Folder**
Capture an entire folder (and all its contents) into the portable workspace.
- Input: Full path to the folder to capture
- Result: Folder and contents are copied to `workspace/files/`

#### 4. **Restore Folder**
Restore a previously captured folder to a destination on your computer.
- Input: Folder name to restore and destination folder path
- Result: Folder and all contents are copied to the destination

#### 5. **Start Temporary Workspace**
Create an isolated temporary copy of your entire workspace for testing or experimentation.
- Process:
  1. Creates a temporary directory in system temp folder (prefix: `portable_workspace_`)
  2. Copies entire workspace to this temporary location
  3. All changes are isolated and don't affect the original
- Result: Temporary workspace ready for use; you can modify files safely

#### 6. **Save Workspace**
Save all changes made in the temporary workspace back to the original workspace.
- Process:
  1. Copies all changes from temporary workspace back to original
  2. Removes old workspace contents
  3. Cleans up the temporary workspace
- Result: Changes are permanent; temporary workspace is deleted

#### 7. **Discard Workspace**
Discard all changes made in the temporary workspace without saving.
- Process:
  1. Deletes the temporary workspace
  2. Reverts to the state before "Start Temporary Workspace" was called
- Result: All experimental changes are lost; original workspace unchanged

#### 8. **Create Encrypted Snapshot**
Create a password-protected encrypted backup of your entire workspace.
- Input: Encryption password (entered securely via getpass)
- Process:
  1. Zips the entire workspace
  2. Encrypts the zip file using your password
  3. Stores encrypted snapshot in `workspace/.security/workspace_snapshot.enc`
- Result: Secure backup that requires password to restore
- Security: Uses Fernet encryption with PBKDF2 key derivation (390,000 iterations)

#### 9. **Exit**
Exit the application.
- Warning: If a temporary session is active, you'll be warned to save or discard it first

---

## Architecture & Core Modules

### Launcher Module (`launcher/`)

#### `main.py`
- Entry point for the entire application
- Provides interactive CLI menu
- Manages application state and user interaction
- Coordinates workspace operations

#### `config.py`
- Centralized configuration management
- Defines all project paths and directories
- Environment setup and initialization

#### `session.py`
- **WorkspaceSession** class manages temporary workspace lifecycles
- Creates isolated temporary copies of the workspace
- Handles saving changes back to original workspace
- Implements session cleanup and resource management

#### `cleanup.py`
- **WorkspaceCleanup** class handles removal of temporary workspaces
- Safely deletes temporary directories
- Verifies cleanup completion
- Error handling and reporting

#### `snapshot.py`
- Creates encrypted snapshots of entire workspace
- Integrates with security module for encryption
- Manages snapshot storage and metadata

#### `security.py`
- **Encryption utilities** for secure data protection
- PBKDF2 key derivation with high iteration count
- Fernet symmetric encryption/decryption
- Password-based encryption key management
- Functions:
  - `_derive_key()` - Derives encryption key from password and salt
  - `encrypt_data()` - Encrypts data using password
  - `decrypt_data()` - Decrypts data using password

#### `system.py`
- System-level utilities and helpers
- OS detection and compatibility checks

#### `file_ops.py`
- Low-level file operation utilities
- File copying, moving, and deletion operations

### Restore Module (`launcher/restore/`)

#### `manager.py`
- **WorkspaceRestoreManager** - Main orchestrator for workspace restoration
- Coordinates all restore operations
- Detects available applications
- Restores files, settings, and VS Code environment
- Generates restoration reports with compatibility metrics

#### `app_detector.py`
- **ApplicationDetector** - Detects installed applications
- Checks for availability of required tools (Git, Python, Node.js, VS Code)
- Determines executable paths and versions
- Validates application compatibility

#### `file_restore.py`
- **FileRestorer** - Handles file restoration operations
- Supports cross-platform path handling (POSIX/Windows)
- Restores files with preserved directory structure
- Error handling and validation

#### `settings_restore.py`
- **SettingsRestorer** - Restores application settings
- Handles settings for Git, Terminal, VS Code, and other applications
- Preserves host settings while applying portable workspace settings
- Configuration merging and conflict resolution

#### `vscode_restore.py`
- **VSCodeRestorer** - Restores VS Code development environment
- Installs captured extensions
- Restores VS Code settings and keybindings
- Sets up workspace configuration
- Handles both local and portable VS Code installations

#### `models.py`
- Data models and type definitions
- Classes:
  - `ApplicationDefinition` - Defines supported applications
  - `ApplicationDetection` - Represents detected application info
  - `FileRestoreResult` - File restoration operation results
  - `SettingsRestoreResult` - Settings restoration results
  - `VSCodeRestoreResult` - VS Code restoration results
  - `WorkspaceManifest` - Workspace configuration manifest
  - `RestoreReport` - Overall restoration report with metrics

### Workspace Module (`workspace/`)

#### `capture/files.py`
- `capture_files()` - Captures files from source to destination

#### `capture/settings.py`
- `capture_settings()` - Captures application settings (Git, Terminal, VS Code)

#### `capture/snapshot.py`
- `create_workspace_snapshot()` - Creates workspace snapshots with metadata

#### `capture/wallpaper.py`
- `capture_wallpaper()` - Captures desktop wallpaper settings

---

## Security Features

### Encryption
- **Algorithm**: Fernet (symmetric encryption)
- **Key Derivation**: PBKDF2 with 390,000 iterations
- **Salt Size**: 16 bytes
- **Key Length**: 32 bytes (256-bit)
- **Hash Function**: SHA-256

### Secure Password Handling
- Uses Python's `getpass` module for secure password input
- Passwords are never logged or displayed
- Encryption keys are derived at runtime and not stored

### Workspace Isolation
- Temporary workspaces created in system temp directory
- All changes are isolated until explicitly saved
- Original workspace never modified during experimentation

---

## Testing

Comprehensive test suite included in `tests/` directory:

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Test Coverage
- **Session Management**: Temporary workspace creation, saving, discarding
- **Cleanup Operations**: Temporary directory removal and verification
- **Security**: Encryption/decryption with various passwords
- **Snapshot Operations**: Snapshot creation and validation
- **File Capture**: File and folder capture operations
- **Settings Capture**: Application settings capture
- **Application Detection**: Detecting installed applications
- **File Restoration**: Cross-platform file restoration
- **Settings Restoration**: Application settings restoration
- **VS Code Restoration**: Environment restoration

### Test Fixtures
Located in `tests/capture/` and `tests/restore/`:
- Sample settings (Git, Terminal, VS Code configurations)
- Sample workspaces and files
- Sample wallpaper data
- Sample manifests and snapshots

---

## Configuration

### Directory Structure
Configured in `launcher/config.py`:
- **WORKSPACE_DIR**: Main workspace directory
- **FILES_DIR**: Captured workspace files
- **SETTINGS_DIR**: Captured application settings
- **APPS_DIR**: Application definitions
- **BACKUP_DIR**: Backup location
- **SECURITY_DIR**: Encrypted snapshots location

### Workspace Manifest
Located at `workspace/config.json`, defines:
- Workspace name and metadata
- Captured files and folders
- Application requirements and configurations
- Settings to restore

---

## How It Works: Example Workflow

### Scenario: Student Setup on USB

**Day 1 - Preparation (Your Personal Laptop)**
```
1. Run main.py
2. Capture File → Add your Python scripts
3. Capture Folder → Add your projects
4. Menu → VS Code settings already captured
5. Create Encrypted Snapshot → Backup everything securely
```

**Day 2 - Use in Lab Computer**
```
1. Insert USB on lab computer (Windows/Mac/Linux)
2. Run main.py from USB
3. Start Temporary Workspace → Creates isolated copy
4. Open VS Code → Loads your settings from USB
5. Work on projects → All changes in temporary workspace
6. Save Workspace → OR Discard Workspace
```

---

## Key Use Cases

1. **Multi-Computer Development**
   - Maintain consistent development environment across lab computers
   - No need to reinstall tools or configure settings on each computer

2. **Secure Backups**
   - Create password-protected encrypted snapshots
   - Backup important workspace configurations

3. **Experimentation**
   - Start temporary workspace to test changes
   - Safe to discard if something goes wrong

4. **Setup Sharing**
   - Share your workspace configuration with classmates
   - Portable between operating systems (if tools available)

5. **Configuration Management**
   - Centralized management of workspace settings
   - Easy to update and sync across multiple instances

---

## Supported Platforms

- ✅ Windows (10, 11)
- ✅ macOS (10.12+)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

---

## Known Limitations

- Requires Python to be installed on target computer (for restore operations)
- Some VS Code extensions may not be portable due to native dependencies
- Settings restoration limited to commonly used applications (Git, Terminal, VS Code)
- Application detection works for standard installation paths

---

## Future Enhancements

- GUI interface for easier navigation
- Support for additional applications (Node.js package managers, Docker, etc.)
- Browser bookmark and extension synchronization
- Automatic scheduling for snapshots
- Cloud storage integration for backups
- Multi-profile support for different work contexts

---

## Contributing

To contribute improvements:
1. Create feature branches
2. Add tests for new functionality
3. Ensure all existing tests pass
4. Update documentation as needed

---

## License

[Add appropriate license here]

---

## Support & Troubleshooting

### Issue: "Workspace not found"
- Ensure the `workspace/` directory exists in the project root

### Issue: "No active session"
- Run "Start Temporary Workspace" (option 5) before using save/discard options

### Issue: Encryption fails
- Ensure `cryptography` library is installed: `pip install cryptography`
- Verify password is not empty when creating snapshots

### Issue: Application detection fails
- Install required applications in standard locations
- Check that executable paths are in system PATH

---

## Contact & Questions

For issues, questions, or suggestions, please open an issue in the project repository.