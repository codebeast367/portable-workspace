from pathlib import Path
import shutil


class WorkspaceCleanup:
    def __init__(self, session_dir):
        self.session_dir = Path(session_dir) if session_dir else None

    def cleanup(self):
        """Remove only the temporary workspace created by the launcher."""

        if self.session_dir is None:
            print("[INFO] No temporary session to clean.")
            return True

        if not self.session_dir.exists():
            print("[INFO] Temporary session already cleaned.")
            return True

        if not self.session_dir.is_dir():
            print("[ERROR] Session path is not a directory.")
            return False

        try:
            shutil.rmtree(self.session_dir)

            if self.session_dir.exists():
                print("[ERROR] Cleanup verification failed.")
                return False

            print("[OK] Temporary workspace cleaned.")
            return True

        except Exception as error:
            print(f"[ERROR] Cleanup failed: {error}")
            return False