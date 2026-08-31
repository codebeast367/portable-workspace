from pathlib import Path
import tempfile
import zipfile

try:
    from .security import encrypt_file
except ImportError:
    from security import encrypt_file


def create_workspace_snapshot(workspace_dir, output_file, password):
    """
    Create an encrypted snapshot of the workspace.

    The .security directory is excluded so that an old snapshot
    is never included inside a new snapshot.
    """

    workspace_dir = Path(workspace_dir)
    output_file = Path(output_file)

    if not workspace_dir.exists():
        raise FileNotFoundError(
            f"Workspace not found: {workspace_dir}"
        )

    if not password:
        raise ValueError("Password cannot be empty.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        prefix="workspace_snapshot_",
        suffix=".zip",
        delete=False
    ) as temp_file:
        temp_zip = Path(temp_file.name)

    try:
        with zipfile.ZipFile(
            temp_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:

            for file_path in workspace_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                # Never include the security folder inside itself.
                if ".security" in file_path.parts:
                    continue

                archive.write(
                    file_path,
                    file_path.relative_to(workspace_dir)
                )

        encrypt_file(
            temp_zip,
            output_file,
            password
        )

    finally:
        if temp_zip.exists():
            temp_zip.unlink()

    return output_file