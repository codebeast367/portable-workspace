import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from launcher.restore.app_detector import ApplicationDetection
from launcher.restore.vscode_restore import VSCodeRestorer


class TestVSCodeRestorer(unittest.TestCase):
    def test_vscode_unavailable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            workspace.mkdir()
            session = root / "session"
            detector_result = ApplicationDetection(
                application_id="vscode",
                name="Visual Studio Code",
                required=True,
                status="Not Available",
                version=None,
                path=None,
                error="Executable not found in PATH",
            )
            with patch("launcher.restore.vscode_restore.ApplicationDetector.detect_application", return_value=detector_result):
                restorer = VSCodeRestorer(workspace_path=workspace, session_path=session)
                result = restorer.restore_environment(project_path=workspace / "projects")
                self.assertFalse(result.success)
                self.assertIn("Visual Studio Code", result.message)

    def test_vscode_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            workspace.mkdir()
            session = root / "session"
            detector_result = ApplicationDetection(
                application_id="vscode",
                name="Visual Studio Code",
                required=True,
                status="Available",
                version="1.92.0",
                path="C:/Program Files/Microsoft VS Code/Code.exe",
            )
            project = workspace / "projects" / "demo"
            project.mkdir(parents=True)
            (project / "main.py").write_text("print('demo')", encoding="utf-8")

            with patch("launcher.restore.vscode_restore.ApplicationDetector.detect_application", return_value=detector_result), patch.object(
                VSCodeRestorer,
                "open_project",
                return_value=True,
            ):
                restorer = VSCodeRestorer(workspace_path=workspace, session_path=session)
                result = restorer.restore_environment(project_path=project)
                self.assertTrue(result.success)
                self.assertTrue(result.environment_ready)

    def test_settings_restoration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            workspace.mkdir()
            session = root / "session"
            settings_dir = workspace / "settings" / "vscode"
            settings_dir.mkdir(parents=True)
            (settings_dir / "settings.json").write_text('{"editor.tabSize": 2}', encoding="utf-8")
            (settings_dir / "keybindings.json").write_text('[]', encoding="utf-8")
            snippet_dir = settings_dir / "snippets"
            snippet_dir.mkdir()
            (snippet_dir / "sample.code-snippets").write_text('{}', encoding="utf-8")

            restorer = VSCodeRestorer(workspace_path=workspace, session_path=session)
            result = restorer.restore_vscode_settings(settings_dir, session)
            self.assertEqual(len(result.restored), 3)

    def test_workspace_opening_logic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            workspace.mkdir()
            session = root / "session"
            project = workspace / "projects" / "demo"
            project.mkdir(parents=True)

            restorer = VSCodeRestorer(workspace_path=workspace, session_path=session)
            command = restorer.build_open_command(project)
            self.assertTrue(any("code" in str(part).lower() for part in command))
            self.assertIn(str(project), command)


if __name__ == "__main__":
    unittest.main()
