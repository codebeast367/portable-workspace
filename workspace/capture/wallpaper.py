from pathlib import Path
import shutil


SUPPORTED_IMAGE_TYPES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def capture_wallpaper(source_file, destination_dir):
    """
    Capture a wallpaper image into the portable workspace.

    Parameters:
        source_file: Path to the wallpaper image.
        destination_dir: Directory where the wallpaper is stored.

    Returns:
        Path to the captured wallpaper, or None on failure.
    """

    source = Path(source_file)
    destination_dir = Path(destination_dir)

    if not source.exists():
        print("[ERROR] Wallpaper file not found.")
        return None

    if not source.is_file():
        print("[ERROR] Wallpaper path is not a file.")
        return None

    if source.suffix.lower() not in SUPPORTED_IMAGE_TYPES:
        print("[ERROR] Unsupported wallpaper image format.")
        return None

    destination_dir.mkdir(parents=True, exist_ok=True)

    destination = destination_dir / source.name

    try:
        shutil.copy2(source, destination)

        print(f"[OK] Wallpaper captured: {source.name}")
        print(f"[SAVED] {destination}")

        return destination

    except Exception as error:
        print(f"[ERROR] Could not capture wallpaper: {error}")
        return None