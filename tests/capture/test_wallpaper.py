from pathlib import Path
import shutil

from workspace.capture.wallpaper import capture_wallpaper


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAMPLE_DIR = PROJECT_ROOT / "tests" / "capture" / "sample_wallpaper"
OUTPUT_DIR = PROJECT_ROOT / "tests" / "capture" / "captured_wallpaper"


def create_sample_wallpaper():
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    sample_file = SAMPLE_DIR / "sample_wallpaper.png"

    # Fake image data for testing only.
    sample_file.write_bytes(b"FAKE-WALLPAPER-DATA")

    return sample_file


def main():
    sample_file = create_sample_wallpaper()

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    captured = capture_wallpaper(sample_file, OUTPUT_DIR)

    if captured is None:
        print("[FAIL] Wallpaper capture failed.")
        return

    captured = Path(captured)

    if captured.exists():
        print("[PASS] Wallpaper capture test succeeded.")
        print(f"Captured wallpaper: {captured}")
    else:
        print("[FAIL] Captured wallpaper was not found.")


if __name__ == "__main__":
    main()