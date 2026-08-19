import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    PROJECT_DIR,
    WORKSPACE_DIR,
    FILES_DIR,
    SETTINGS_DIR,
    APPS_DIR,
    BACKUP_DIR,
    SECURITY_DIR
)


def show_banner():
    print()
    print("================================")
    print("       PORTABLE WORKSPACE")
    print("================================")
    print()


def check_workspace():
    print("Checking workspace...")

    folders = {
        "Workspace": WORKSPACE_DIR,
        "Files": FILES_DIR,
        "Settings": SETTINGS_DIR,
        "Apps": APPS_DIR,
        "Backup": BACKUP_DIR,
        "test": PROJECT_DIR / "test"
    }

    for name, path in folders.items():
        if path.exists():
            print(f"[OK] {name}: {path}")
        else:
            print(f"[MISSING] {name}: {path}")


def main():
    show_banner()

    print(f"Project location: {PROJECT_DIR}")
    print()

    check_workspace()

    print()
    print("================================")
    print("          MAIN MENU")
    print("================================")
    print("1. Capture File")
    print("2. Restore File")
    print("3. Capture Folder")
    print("4. Restore Folder")
    print("5. Capture Directory Contents")
    print("6. Exit")
    print()

    choice = input("Choose an option: ")

    if choice == "1":
        print()

        source_file = input("Enter the file path: ")

        from file_ops import capture_file

        capture_file(source_file)

    elif choice == "2":
        print()

        file_name = input("Enter the file name to restore: ")
        destination = input("Enter the destination folder: ")

        from file_ops import restore_file

        restore_file(file_name, destination)

    elif choice == "3":
        print()

        source_folder = input("Enter the folder path: ")

        from file_ops import capture_folder

        capture_folder(source_folder)

    elif choice == "4":
        print()

        folder_name = input("Enter the folder name to restore: ")
        destination = input("Enter the destination folder: ")

        from file_ops import restore_folder

        restore_folder(folder_name, destination)

    elif choice == "5":
        print()

        source_dir = input("Enter the folder path whose CONTENTS you want to capture: ")
        folder_name = input("Enter a name to save this capture as: ")

        from workspace.capture.files import capture_files

        destination = FILES_DIR / folder_name
        capture_files(source_dir, destination)

    elif choice == "6":
        print("Exiting Portable Workspace...")

    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()