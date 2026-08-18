from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ApplicationDefinition:
    id: str
    name: str
    required: bool = False


@dataclass(slots=True)
class ApplicationDetection:
    application_id: str
    name: str
    required: bool
    status: str
    version: str | None = None
    path: str | None = None
    error: str | None = None


@dataclass(slots=True)
class FileRestoreResult:
    restored: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    destination_directory: str | None = None
    files_copied: int = 0


@dataclass(slots=True)
class SettingsRestoreResult:
    restored: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class VSCodeRestoreResult:
    success: bool
    message: str
    environment_ready: bool = False
    settings_restored: bool = False
    project_opened: bool = False
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkspaceManifest:
    workspace_name: str
    applications: list[ApplicationDefinition] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    settings: dict[str, bool] = field(default_factory=dict)


@dataclass(slots=True)
class RestoreReport:
    workspace_name: str
    applications: list[ApplicationDetection]
    files: FileRestoreResult
    settings: SettingsRestoreResult
    vscode: VSCodeRestoreResult
    compatibility: int
    session_path: str | None = None
    workspace_path: str | None = None
