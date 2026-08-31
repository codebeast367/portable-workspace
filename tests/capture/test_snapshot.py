from pathlib import Path
import json
import shutil

from workspace.capture.snapshot import create_workspace_snapshot


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_DIR = PROJECT_ROOT / "tests" / "capture" / "sample_snapshot"


def main():
    if WORKSPACE_DIR.exists():
        shutil.rmtree(WORKSPACE_DIR)

    files_dir = WORKSPACE_DIR / "files"
    files_dir.mkdir(parents=True)

    (files_dir / "hello.txt").write_text(
        "Sample workspace file",
        encoding="utf-8"
    )

    (files_dir / "project").mkdir()

    manifest_path = create_workspace_snapshot(
        WORKSPACE_DIR,
        workspace_name="Test Workspace"
    )

    print()
    print("Generated manifest:")
    print(manifest_path.read_text(encoding="utf-8"))

    data = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    assert data["workspace_name"] == "Test Workspace"
    assert "hello.txt" in data["files"]
    assert "project" in data["files"]
    assert data["settings"]["vscode"] is True

    print()
    print("[PASS] Workspace snapshot test succeeded.")


if __name__ == "__main__":
    main()
    