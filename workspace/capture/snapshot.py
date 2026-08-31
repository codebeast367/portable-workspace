import json
from pathlib import Path


def create_workspace_snapshot(
    workspace_dir,
    workspace_name="My College Workspace",
    applications=None,
    settings=None
):
    """
    Create manifest.json describing the captured workspace.
    """

    workspace_dir = Path(workspace_dir)

    if not workspace_dir.exists():
        raise FileNotFoundError(
            f"Workspace directory not found: {workspace_dir}"
        )

    applications = applications or []

    settings = settings or {
        "vscode": True,
        "git": True,
        "terminal": True
    }

    files_dir = workspace_dir / "files"

    captured_files = []

    if files_dir.exists():
        for item in files_dir.iterdir():
            captured_files.append(item.name)

    manifest = {
        "workspace_name": workspace_name,
        "applications": applications,
        "files": captured_files,
        "settings": settings
    }

    manifest_path = workspace_dir / "manifest.json"

    manifest_path.write_text(
        json.dumps(manifest, indent=4),
        encoding="utf-8"
    )

    print(f"[OK] Workspace snapshot created.")
    print(f"[SAVED] {manifest_path}")

    return manifest_path
