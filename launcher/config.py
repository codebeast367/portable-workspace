from pathlib import Path

# Project location
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Main folders
WORKSPACE_DIR = PROJECT_DIR / "workspace"
FILES_DIR = WORKSPACE_DIR / "files"
SETTINGS_DIR = WORKSPACE_DIR / "settings"
APPS_DIR = WORKSPACE_DIR / "apps"

BACKUP_DIR = PROJECT_DIR / "backup"
SECURITY_DIR = WORKSPACE_DIR / ".security"