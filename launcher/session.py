from pathlib import Path
import shutil
import tempfile


class WorkspaceSession:
    def __init__(self, workspace_dir):
        self.workspace_dir = Path(workspace_dir)
        self.session_dir = None

    def start(self):
        """Create a temporary copy of the workspace."""

        if not self.workspace_dir.exists():
            raise FileNotFoundError(
                f"Workspace not found: {self.workspace_dir}"
            )

        self.session_dir = Path(
            tempfile.mkdtemp(prefix="portable_workspace_")
        )

        shutil.copytree(
            self.workspace_dir,
            self.session_dir,
            dirs_exist_ok=True
        )

        print("[OK] Temporary session created:")
        print(self.session_dir)

        return self.session_dir

    def save(self):
        """Save temporary workspace changes back to the workspace."""

        if self.session_dir is None:
            raise RuntimeError("No active session.")

        if not self.session_dir.exists():
            raise RuntimeError("Temporary session no longer exists.")

        # Remove old workspace contents.
        for item in self.workspace_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # Copy temporary workspace back.
        shutil.copytree(
            self.session_dir,
            self.workspace_dir,
            dirs_exist_ok=True
        )

        print("[OK] Workspace changes saved.")

        # Clean temporary session after saving.
        self.discard()

    def discard(self):
        """Discard all temporary workspace changes."""

        if self.session_dir is None:
            print("[INFO] No active session.")
            return

        if self.session_dir.exists():
            shutil.rmtree(self.session_dir)

        self.session_dir = None

        print("[OK] Workspace changes discarded.")

    def close(self):
        """Safely close the session without saving."""

        self.discard()