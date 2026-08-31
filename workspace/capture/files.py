from pathlib import Path
import shutil


def capture_files(source_dir, destination_dir):
    """
    Capture selected workspace files into the portable workspace.

    Parameters:
        source_dir: Folder containing the files to capture.
        destination_dir: Folder where the captured files will be stored.
    """

    source = Path(source_dir)
    destination = Path(destination_dir)

    if not source.exists():
        raise FileNotFoundError(f"Source folder not found: {source}")

    if not source.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        target = destination / item.name

        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    return destination