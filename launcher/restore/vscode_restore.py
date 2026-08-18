from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from pathlib import Path

from launcher.restore.app_detector import ApplicationDetector
from launcher.restore.models import VSCodeRestoreResult
from launcher.restore.settings_restore import SettingsRestorer


class VSCodeRestorer:
    """Restore a temporary VS Code environment without affecting the user's normal profile."""

    def __init__(self, workspace_path: str | Path, session_path: str | Path | None = None):
        self.workspace_path = Path(workspace_path)
        self.session_path = Path(session_path) if session_path else self.workspace_path.parent / "session"
        self.detector = ApplicationDetector()
        self.settings_restorer = SettingsRestorer()

    def detect_vscode(self):
        return self.detector.detect_application("vscode")

    def find_portable_vscode(self) -> Path | None:
        candidates = [
            self.workspace_path / "vscode",
            self.workspace_path / "portable-vscode",
            self.workspace_path / ".vscode",
        ]

        for candidate in candidates:
            if not candidate.exists():
                continue
            if self._looks_like_portable_vscode(candidate):
                return candidate
        return None

    def _looks_like_portable_vscode(self, candidate: Path) -> bool:
        for possible in (
            candidate / "Code.exe",
            candidate / "code",
            candidate / "bin" / "code",
            candidate / "bin" / "code.cmd",
            candidate / "Code",
        ):
            if possible.exists():
                return True
        return False

    def restore_vscode_settings(self, source_directory: str | Path, destination_directory: str | Path):
        return self.settings_restorer.restore_vscode_settings(source_directory, destination_directory)

    def restore_environment(self, project_path: str | Path) -> VSCodeRestoreResult:
        project_path = Path(project_path)
        detection = self.detect_vscode()

        if detection.status != "Available":
            return VSCodeRestoreResult(
                success=False,
                message=f"Visual Studio Code is unavailable. {detection.error or 'No executable found.'}",
                environment_ready=False,
                settings_restored=False,
                project_opened=False,
                details={"application": asdict(detection)},
            )

        self.session_path.mkdir(parents=True, exist_ok=True)
        user_data_dir = self.session_path / "vscode-user-data"
        extensions_dir = self.session_path / "vscode-extensions"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        extensions_dir.mkdir(parents=True, exist_ok=True)

        settings_source = self.workspace_path / "settings" / "vscode"
        settings_result = self.settings_restorer.restore_vscode_settings(settings_source, user_data_dir)

        extensions_file = self.workspace_path / "vscode" / "extensions.json"
        extension_ids: list[str] = []
        if extensions_file.exists():
            try:
                payload = json.loads(extensions_file.read_text(encoding="utf-8"))
                if isinstance(payload, list):
                    extension_ids = [str(item) for item in payload]
                elif isinstance(payload, dict):
                    extension_ids = [str(item) for item in payload.get("recommendations", [])]
                (self.session_path / "vscode-extensions" / "extensions.json").write_text(
                    json.dumps({"recommendations": extension_ids}, indent=2),
                    encoding="utf-8",
                )
            except (json.JSONDecodeError, OSError):
                extension_ids = []

        project_opened = self.open_project(project_path)

        return VSCodeRestoreResult(
            success=True,
            message="Visual Studio Code environment restored successfully.",
            environment_ready=True,
            settings_restored=bool(settings_result.restored or settings_result.skipped),
            project_opened=project_opened,
            details={
                "path": detection.path,
                "user_data_dir": str(user_data_dir),
                "extensions_dir": str(extensions_dir),
                "extensions": extension_ids,
                "portable_detected": bool(self.find_portable_vscode()),
            },
        )

    def build_open_command(self, project_path: str | Path) -> list[str]:
        project_path = Path(project_path)
        base_command = ["code", "--user-data-dir", str(self.session_path / "vscode-user-data"), "--extensions-dir", str(self.session_path / "vscode-extensions"), str(project_path)]
        executable = self._resolve_executable()
        if executable:
            return [str(executable), "--user-data-dir", str(self.session_path / "vscode-user-data"), "--extensions-dir", str(self.session_path / "vscode-extensions"), str(project_path)]
        return base_command

    def open_project(self, project_path: str | Path) -> bool:
        command = self.build_open_command(project_path)
        if not command:
            return False

        try:
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
            return True
        except OSError:
            return False

    def _resolve_executable(self) -> str | None:
        portable = self.find_portable_vscode()
        if portable:
            for candidate in (
                portable / "Code.exe",
                portable / "code",
                portable / "bin" / "code",
                portable / "bin" / "code.cmd",
                portable / "Code",
            ):
                if candidate.exists():
                    return str(candidate)

        detection = self.detect_vscode()
        return detection.path if detection.status == "Available" else None
