from __future__ import annotations

import json
import shutil
from pathlib import Path

from launcher.restore.models import SettingsRestoreResult


class SettingsRestorer:
    """Copy safe workspace settings into the temporary session directory."""

    def restore_settings(
        self,
        source_directory: str | Path,
        destination_directory: str | Path,
        settings_map: dict[str, bool] | None = None,
    ) -> SettingsRestoreResult:
        result = SettingsRestoreResult()
        settings_map = settings_map or {"vscode": True, "git": True, "terminal": True}
        source_root = Path(source_directory)
        destination_root = Path(destination_directory)

        for key, enabled in settings_map.items():
            if not enabled:
                result.skipped.append(key)
                continue

            if key == "vscode":
                outcome = self.restore_vscode_settings(source_root / "vscode", destination_root)
            elif key == "git":
                outcome = self.restore_git_settings(source_root / "git", destination_root)
            elif key == "terminal":
                outcome = self.restore_terminal_settings(source_root / "terminal", destination_root)
            else:
                result.skipped.append(key)
                continue

            result.restored.extend(outcome.restored)
            result.skipped.extend(outcome.skipped)
            result.failed.extend(outcome.failed)
            result.warnings.extend(outcome.warnings)

        return result

    def restore_vscode_settings(
        self,
        source_directory: str | Path,
        destination_directory: str | Path,
    ) -> SettingsRestoreResult:
        result = SettingsRestoreResult()
        source_root = Path(source_directory)
        destination_root = Path(destination_directory) / "settings" / "vscode"
        destination_root.mkdir(parents=True, exist_ok=True)

        if not source_root.exists():
            result.skipped.extend(["settings.json", "keybindings.json", "snippets"])
            return result

        for file_name in ("settings.json", "keybindings.json"):
            source_file = source_root / file_name
            if not source_file.exists():
                result.skipped.append(file_name)
                continue
            try:
                json.loads(source_file.read_text(encoding="utf-8"))
                shutil.copy2(source_file, destination_root / file_name)
                result.restored.append(file_name)
            except json.JSONDecodeError:
                result.failed.append(file_name)
                result.warnings.append(f"Malformed JSON in {file_name}")
            except OSError as exc:
                result.failed.append(file_name)
                result.warnings.append(f"Unable to copy {file_name}: {exc}")

        snippet_source = source_root / "snippets"
        if snippet_source.exists() and snippet_source.is_dir():
            try:
                shutil.copytree(snippet_source, destination_root / "snippets", dirs_exist_ok=True)
                result.restored.append("snippets")
            except OSError as exc:
                result.failed.append("snippets")
                result.warnings.append(f"Unable to copy VS Code snippets: {exc}")
        else:
            result.skipped.append("snippets")

        return result

    def restore_git_settings(
        self,
        source_directory: str | Path,
        destination_directory: str | Path,
    ) -> SettingsRestoreResult:
        result = SettingsRestoreResult()
        source_root = Path(source_directory)
        destination_root = Path(destination_directory) / "settings" / "git"
        destination_root.mkdir(parents=True, exist_ok=True)

        if not source_root.exists() or not any(source_root.iterdir()):
            result.skipped.append("git")
            return result

        copied = False
        for child in source_root.iterdir():
            target = destination_root / child.name
            try:
                if child.is_dir():
                    shutil.copytree(child, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(child, target)
                copied = True
            except OSError as exc:
                result.failed.append(child.name)
                result.warnings.append(f"Git settings copy failed for {child.name}: {exc}")

        if copied:
            result.restored.append("git")
        else:
            result.skipped.append("git")

        return result

    def restore_terminal_settings(
        self,
        source_directory: str | Path,
        destination_directory: str | Path,
    ) -> SettingsRestoreResult:
        result = SettingsRestoreResult()
        source_root = Path(source_directory)
        destination_root = Path(destination_directory) / "settings" / "terminal"
        destination_root.mkdir(parents=True, exist_ok=True)

        if not source_root.exists() or not any(source_root.iterdir()):
            result.skipped.append("terminal")
            return result

        copied = False
        for child in source_root.iterdir():
            target = destination_root / child.name
            try:
                if child.is_dir():
                    shutil.copytree(child, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(child, target)
                copied = True
            except OSError as exc:
                result.failed.append(child.name)
                result.warnings.append(f"Terminal settings copy failed for {child.name}: {exc}")

        if copied:
            result.restored.append("terminal")
        else:
            result.skipped.append("terminal")

        return result
