from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from launcher.restore.models import ApplicationDefinition, ApplicationDetection


class ApplicationDetector:
    """Detect whether required applications are present on the host machine."""

    SUPPORTED_APPLICATIONS: dict[str, ApplicationDefinition] = {
        "vscode": ApplicationDefinition(id="vscode", name="Visual Studio Code", required=True),
        "git": ApplicationDefinition(id="git", name="Git", required=True),
        "python": ApplicationDefinition(id="python", name="Python", required=False),
        "node": ApplicationDefinition(id="node", name="Node.js", required=False),
    }

    def detect_application(self, application_id: str) -> ApplicationDetection:
        definition = self.SUPPORTED_APPLICATIONS.get(application_id)
        if definition is None:
            return ApplicationDetection(
                application_id=application_id,
                name="Unknown",
                required=False,
                status="Invalid",
                error=f"Unsupported application ID: {application_id}",
            )

        executable = self._find_executable(definition.id)
        if executable is None:
            return ApplicationDetection(
                application_id=definition.id,
                name=definition.name,
                required=definition.required,
                status="Not Available",
                version=None,
                path=None,
                error=f"{definition.name} was not found in PATH.",
            )

        version = self._get_version(executable, definition.id)
        return ApplicationDetection(
            application_id=definition.id,
            name=definition.name,
            required=definition.required,
            status="Available",
            version=version,
            path=str(executable),
        )

    def detect_all(self, applications: Iterable[str | ApplicationDefinition]) -> dict[str, ApplicationDetection]:
        detected: dict[str, ApplicationDetection] = {}
        for candidate in applications:
            if isinstance(candidate, ApplicationDefinition):
                app_id = candidate.id
            else:
                app_id = str(candidate)
            detected[app_id] = self.detect_application(app_id)
        return detected

    def _find_executable(self, application_id: str) -> str | None:
        candidates = self._candidate_names(application_id)
        for name in candidates:
            path = shutil.which(name)
            if path:
                return path
        return None

    def _candidate_names(self, application_id: str) -> list[str]:
        if application_id == "vscode":
            return ["code", "code.cmd", "Code.exe", "Code", "code-insiders"]
        if application_id == "git":
            return ["git", "git.exe"]
        if application_id == "python":
            return ["python", "python3", "py"]
        if application_id == "node":
            return ["node", "node.exe"]
        return [application_id]

    def _get_version(self, executable: str, application_id: str) -> str | None:
        command = self._version_command(executable, application_id)
        if not command:
            return None

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        except OSError:
            return None

        output = (completed.stdout or completed.stderr or "").strip()
        if not output:
            return None

        version_text = self._extract_version(output)
        return version_text

    def _version_command(self, executable: str, application_id: str) -> list[str] | None:
        if application_id == "vscode":
            return [executable, "--version"]
        if application_id == "git":
            return [executable, "--version"]
        if application_id == "python":
            if Path(executable).name.lower() == "py":
                return [executable, "-V"]
            return [executable, "--version"]
        if application_id == "node":
            return [executable, "--version"]
        return None

    @staticmethod
    def _extract_version(output: str) -> str | None:
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        if not lines:
            return None
        first = lines[0]
        match = re.search(r"(\d+\.\d+\.\d+|\d+\.\d+|\d+)", first)
        if match:
            return match.group(1)
        return first
