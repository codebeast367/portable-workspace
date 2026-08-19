from pathlib import Path
import shutil


def copy_directory_contents(source_dir, destination_dir):
    source = Path(source_dir)
    destination = Path(destination_dir)

    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    if not source.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        target = destination / item.name

        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def capture_vscode_settings(source_dir, destination_dir):
    copy_directory_contents(source_dir, Path(destination_dir))


def capture_git_settings(source_dir, destination_dir):
    copy_directory_contents(source_dir, Path(destination_dir))


def capture_terminal_settings(source_dir, destination_dir):
    copy_directory_contents(source_dir, Path(destination_dir))


def capture_settings(sources, destination_dir):
    """
    Capture supported settings into the portable workspace.

    Expected sources:
        {
            "vscode": Path(...),
            "git": Path(...),
            "terminal": Path(...)
        }
    """

    destination = Path(destination_dir)
    destination.mkdir(parents=True, exist_ok=True)

    captured = []

    handlers = {
        "vscode": capture_vscode_settings,
        "git": capture_git_settings,
        "terminal": capture_terminal_settings,
    }

    for name, source in sources.items():
        if name not in handlers:
            continue

        target = destination / name
        handlers[name](source, target)
        captured.append(name)

    return captured