from __future__ import annotations

import json
from pathlib import Path

from launcher.restore.app_detector import ApplicationDetector
from launcher.restore.file_restore import FileRestorer
from launcher.restore.models import ApplicationDefinition, RestoreReport, WorkspaceManifest
from launcher.restore.settings_restore import SettingsRestorer
from launcher.restore.vscode_restore import VSCodeRestorer


class WorkspaceRestoreManager:
    """Coordinates only the workspace restore responsibilities for this module."""

    def __init__(self, workspace_path: str | Path):
        self.workspace_path = Path(workspace_path)
        self.session_path = self._create_session_directory()
        self.detector = ApplicationDetector()
        self.file_restorer = FileRestorer()
        self.settings_restorer = SettingsRestorer()
        self.vscode_restorer = VSCodeRestorer(self.workspace_path, self.session_path)

    def restore(self) -> RestoreReport:
        manifest = self._read_manifest()
        applications = self._validate_manifest(manifest)

        detected = self.detector.detect_all([app.id for app in applications])
        required_count = sum(1 for app in applications if app.required)
        available_required = sum(
            1 for app in applications if app.required and detected.get(app.id) and detected.get(app.id).status == "Available"
        )
        compatibility = 100 if required_count == 0 else int((available_required / required_count) * 100)

        source_files_dir = self.workspace_path / "files"
        relative_paths = manifest.files
        file_result = self.file_restorer.restore_files(source_files_dir, relative_paths, self.session_path / "workspace")

        settings_result = self.settings_restorer.restore_settings(
            self.workspace_path / "settings",
            self.session_path,
            manifest.settings,
        )

        project_path = self.session_path / "workspace"
        vscode_result = self.vscode_restorer.restore_environment(project_path)

        report = RestoreReport(
            workspace_name=manifest.workspace_name,
            applications=[detected.get(app.id) for app in applications if detected.get(app.id) is not None],
            files=file_result,
            settings=settings_result,
            vscode=vscode_result,
            compatibility=compatibility,
            session_path=str(self.session_path),
            workspace_path=str(self.workspace_path),
        )
        return report

    def _create_session_directory(self) -> Path:
        import os

        base_directory = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "SmartWorkspace" / "sessions"
        base_directory.mkdir(parents=True, exist_ok=True)
        session_id = __import__("uuid").uuid4().hex[:8]
        session_path = base_directory / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        return session_path

    def _read_manifest(self) -> WorkspaceManifest:
        manifest_path = self.workspace_path / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        applications = [
            ApplicationDefinition(
                id=item["id"],
                name=item.get("name", item["id"]),
                required=item.get("required", False),
            )
            for item in payload.get("applications", [])
        ]
        return WorkspaceManifest(
            workspace_name=payload.get("workspace_name", "Workspace"),
            applications=applications,
            files=payload.get("files", []),
            settings=payload.get("settings", {"vscode": True, "git": True, "terminal": True}),
        )

    def _validate_manifest(self, manifest: WorkspaceManifest) -> list:
        if not manifest.workspace_name:
            raise ValueError("Manifest is missing workspace_name.")
        if not isinstance(manifest.applications, list):
            raise ValueError("Manifest applications must be a list.")
        if not isinstance(manifest.files, list):
            raise ValueError("Manifest files must be a list.")
        if not isinstance(manifest.settings, dict):
            raise ValueError("Manifest settings must be a dictionary.")
        return manifest.applications
