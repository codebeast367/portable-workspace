from __future__ import annotations

import shutil
from pathlib import Path, PurePosixPath, PureWindowsPath

from launcher.restore.models import FileRestoreResult


class FileRestorer:
    """Safely restore files and directories into a temporary workspace session."""

    def restore_files(
        self,
        source_directory: str | Path,
        relative_paths: list[str],
        destination_directory: str | Path,
    ) -> FileRestoreResult:
        source_root = Path(source_directory).resolve(strict=False)
        destination_root = Path(destination_directory).resolve(strict=False)
        destination_root.mkdir(parents=True, exist_ok=True)

        result = FileRestoreResult(destination_directory=str(destination_root))

        for relative_path in relative_paths:
            safe_path = self._validate_relative_path(relative_path)
            if safe_path is None:
                result.failed.append(relative_path)
                result.warnings.append(f"Rejected unsafe path: {relative_path}")
                continue

            source_path = (source_root / safe_path).resolve(strict=False)
            if not source_path.exists():
                result.failed.append(relative_path)
                result.warnings.append(f"Missing source file or directory: {relative_path}")
                continue

            if not self._is_within_directory(source_root, source_path):
                result.failed.append(relative_path)
                result.warnings.append(f"Path resolves outside source directory: {relative_path}")
                continue

            destination_path = (destination_root / safe_path).resolve(strict=False)
            if not self._is_within_directory(destination_root, destination_path):
                result.failed.append(relative_path)
                result.warnings.append(f"Path resolves outside destination directory: {relative_path}")
                continue

            try:
                if source_path.is_dir():
                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                else:
                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, destination_path)

                result.restored.append(relative_path)
                result.files_copied += 1
            except (OSError, shutil.Error) as exc:
                result.failed.append(relative_path)
                result.warnings.append(f"Failed to copy {relative_path}: {exc}")

        return result

    def _validate_relative_path(self, relative_path: str) -> Path | None:
        if not relative_path or relative_path.strip() == "":
            return None

        if relative_path.startswith(("/", "\\")):
            return None

        if ":" in relative_path and ("\\" in relative_path or relative_path.startswith(("C:", "D:", "E:"))):
            return None

        posix_path = PurePosixPath(relative_path)
        windows_path = PureWindowsPath(relative_path)

        if posix_path.is_absolute() or windows_path.is_absolute():
            return None

        if ".." in posix_path.parts or ".." in windows_path.parts:
            return None

        normalized = Path(*posix_path.parts)
        if normalized.name in {"", "."}:
            return None
        return normalized

    @staticmethod
    def _is_within_directory(base_directory: Path, target_path: Path) -> bool:
        try:
            target_path.relative_to(base_directory)
            return True
        except ValueError:
            return False
