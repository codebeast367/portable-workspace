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
    print("3. Exit")
    print()

    choice = input("Choose an option: ")

    if choice == "1":
        print()
        source_file = input("Enter the file path: ")

        from workspace import capture_file

        capture_file(source_file)

    elif choice == "2":
        print()

        file_name = input("Enter the file name to restore: ")
        destination = input("Enter the destination folder: ")

        from workspace import restore_file

        restore_file(file_name, destination)

    elif choice == "3":
        print("Exiting Portable Workspace...")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()