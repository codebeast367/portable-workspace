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

from session import WorkspaceSession
from cleanup import WorkspaceCleanup

import getpass

from snapshot import create_workspace_snapshot


active_session = None


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
        "Test": PROJECT_DIR / "test"
    }

    for name, path in folders.items():
        if path.exists():
            print(f"[OK] {name}: {path}")
        else:
            print(f"[MISSING] {name}: {path}")


def start_session():
    global active_session

    if active_session is not None:
        print("[ERROR] A temporary session is already active.")
        return

    try:
        active_session = WorkspaceSession(WORKSPACE_DIR)
        session_dir = active_session.start()

        print()
        print("[OK] Temporary workspace started.")
        print(f"[SESSION] {session_dir}")

    except Exception as error:
        active_session = None
        print(f"[ERROR] Could not start session: {error}")


def save_session():
    global active_session

    if active_session is None:
        print("[ERROR] No active temporary session.")
        return

    try:
        active_session.save()
        active_session = None

        print("[OK] Session saved and cleaned up.")

    except Exception as error:
        print(f"[ERROR] Could not save session: {error}")


def discard_session():
    global active_session

    if active_session is None:
        print("[ERROR] No active temporary session.")
        return

    try:
        session_dir = active_session.session_dir

        active_session.discard()

        cleanup = WorkspaceCleanup(session_dir)
        cleanup.cleanup()

        active_session = None

        print("[OK] Session discarded and cleaned up.")

    except Exception as error:
        print(f"[ERROR] Could not discard session: {error}")


def capture_file_menu():
    source_file = input("Enter the file path: ")

    from workspace import capture_file

    capture_file(source_file)


def restore_file_menu():
    file_name = input("Enter the file name to restore: ")
    destination = input("Enter the destination folder: ")

    from workspace import restore_file

    restore_file(file_name, destination)


def capture_folder_menu():
    source_folder = input("Enter the folder path: ")

    from workspace import capture_folder

    capture_folder(source_folder)


def restore_folder_menu():
    folder_name = input("Enter the folder name to restore: ")
    destination = input("Enter the destination folder: ")

    from workspace import restore_folder

    restore_folder(folder_name, destination)


def create_encrypted_snapshot_menu():
    """Create an encrypted snapshot of the workspace."""

    password = getpass.getpass(
        "Enter encryption password: "
    )

    if not password:
        print("[ERROR] Password cannot be empty.")
        return

    try:
        SECURITY_DIR.mkdir(parents=True, exist_ok=True)

        output_file = SECURITY_DIR / "workspace_snapshot.enc"

        create_workspace_snapshot(
            WORKSPACE_DIR,
            output_file,
            password
        )

        print("[OK] Encrypted workspace snapshot created.")
        print(f"[SAVED] {output_file}")

    except Exception as error:
        print(f"[ERROR] Could not create encrypted snapshot: {error}")


def main():
    show_banner()

    print(f"Project location: {PROJECT_DIR}")
    print()

    check_workspace()

    while True:
        print()
        print("================================")
        print("          MAIN MENU")
        print("================================")
        print("1. Capture File")
        print("2. Restore File")
        print("3. Capture Folder")
        print("4. Restore Folder")
        print("5. Start Temporary Workspace")
        print("6. Save Workspace")
        print("7. Discard Workspace")
        print("8. Create Encrypted Snapshot")
        print("9. Exit")
        print()

        choice = input("Choose an option: ")

        if choice == "1":
            print()
            capture_file_menu()

        elif choice == "2":
            print()
            restore_file_menu()

        elif choice == "3":
            print()
            capture_folder_menu()

        elif choice == "4":
            print()
            restore_folder_menu()

        elif choice == "5":
            print()
            start_session()

        elif choice == "6":
            print()
            save_session()

        elif choice == "7":
            print()
            discard_session()

        elif choice == "8":
            print()
            create_encrypted_snapshot_menu()

        elif choice == "9":
            print()

            if active_session is not None:
                print("[WARNING] A temporary session is still active.")
                print("Please save or discard it before exiting.")
            else:
                print("Exiting Portable Workspace...")
                break

        else:
            print("[ERROR] Invalid option.")


if __name__ == "__main__":
    main()