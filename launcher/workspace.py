from pathlib import Path
import shutil

from config import FILES_DIR


def capture_file(source_file):
    """
    Copy a selected file into the portable workspace.
    """

    source = Path(source_file)

    if not source.exists():
        print("[ERROR] File not found.")
        return False

    if not source.is_file():
        print("[ERROR] The selected path is not a file.")
        return False

    destination = FILES_DIR / source.name

    try:
        shutil.copy2(source, destination)
        print(f"[OK] File captured: {source.name}")
        print(f"[SAVED] {destination}")
        return True

    except Exception as error:
        print(f"[ERROR] Could not capture file: {error}")
        return False

def restore_file(file_name, destination_folder):
    """
    Restore a captured file to a selected folder.
    """

    source = FILES_DIR / file_name
    destination_folder = Path(destination_folder)

    if not source.exists():
        print("[ERROR] File not found in workspace.")
        return False

    if not destination_folder.exists():
        print("[ERROR] Destination folder does not exist.")
        return False

    destination = destination_folder / source.name

    try:
        shutil.copy2(source, destination)

        print(f"[OK] File restored: {source.name}")
        print(f"[RESTORED TO] {destination}")

        return True

    except Exception as error:
        print(f"[ERROR] Could not restore file: {error}")
        return False
 



def capture_folder(source_folder):
    """
    Copy an entire folder into the portable workspace.
    """

    source = Path(source_folder)

    if not source.exists():
        print("[ERROR] Folder not found.")
        return False

    if not source.is_dir():
        print("[ERROR] The selected path is not a folder.")
        return False

    destination = FILES_DIR / source.name

    try:
        if destination.exists():
            print("[ERROR] Folder already exists in workspace.")
            return False

        shutil.copytree(source, destination)

        print(f"[OK] Folder captured: {source.name}")
        print(f"[SAVED] {destination}")

        return True

    except Exception as error:
        print(f"[ERROR] Could not capture folder: {error}")
        return False

def restore_folder(folder_name, destination_folder):
    """
    Restore an entire captured folder.
    """

    source = FILES_DIR / folder_name
    destination_folder = Path(destination_folder)
    destination = destination_folder / folder_name

    if not source.exists():
        print("[ERROR] Folder not found in workspace.")
        return False

    if not source.is_dir():
        print("[ERROR] Selected item is not a folder.")
        return False

    if not destination_folder.exists():
        print("[ERROR] Destination folder does not exist.")
        return False

    try:
        if destination.exists():
            print("[ERROR] Folder already exists at destination.")
            return False

        shutil.copytree(source, destination)

        print(f"[OK] Folder restored: {folder_name}")
        print(f"[RESTORED TO] {destination}")

        return True

    except Exception as error:
        print(f"[ERROR] Could not restore folder: {error}")
        return False

if __name__ == "__main__":
    test_file = r"D:\Portable Workspace\test\sample.txt"

    capture_file(test_file)