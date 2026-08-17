from pathlib import Path

# Find the folder where the launcher is running
APP_DIR = Path(__file__).resolve().parent

# Find the main project folder
PROJECT_DIR = APP_DIR.parent

# Workspace folder
WORKSPACE_DIR = PROJECT_DIR / "workspace"

print("================================")
print("     PORTABLE WORKSPACE")
print("================================")

print(f"Launcher location : {APP_DIR}")
print(f"Project location  : {PROJECT_DIR}")
print(f"Workspace location: {WORKSPACE_DIR}")

if WORKSPACE_DIR.exists():
    print("Workspace detected!")
else:
    print("Workspace not found!")