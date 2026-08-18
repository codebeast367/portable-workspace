from pathlib import Path

from workspace.capture.files import capture_files


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE = PROJECT_ROOT / "tests" / "capture" / "sample_workspace"
DESTINATION = PROJECT_ROOT / "tests" / "capture" / "captured_workspace"


capture_files(SOURCE, DESTINATION)

print("File capture completed successfully.")
print(f"Captured files are in: {DESTINATION}")