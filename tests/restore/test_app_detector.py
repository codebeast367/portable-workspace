import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from launcher.restore.app_detector import ApplicationDetector


class TestApplicationDetector(unittest.TestCase):
    def test_vscode_available(self):
        detector = ApplicationDetector()
        with patch("launcher.restore.app_detector.shutil.which", return_value="C:/Program Files/Microsoft VS Code/Code.exe"), patch(
            "launcher.restore.app_detector.subprocess.run",
            return_value=type("Result", (), {"stdout": "1.92.0\n", "stderr": "", "returncode": 0})(),
        ):
            result = detector.detect_application("vscode")
            self.assertEqual(result.status, "Available")
            self.assertEqual(result.version, "1.92.0")
            self.assertEqual(result.path, "C:/Program Files/Microsoft VS Code/Code.exe")

    def test_git_available(self):
        detector = ApplicationDetector()
        with patch("launcher.restore.app_detector.shutil.which", return_value="C:/Git/bin/git.exe"), patch(
            "launcher.restore.app_detector.subprocess.run",
            return_value=type("Result", (), {"stdout": "2.45.1\n", "stderr": "", "returncode": 0})(),
        ):
            result = detector.detect_application("git")
            self.assertEqual(result.status, "Available")
            self.assertEqual(result.version, "2.45.1")

    def test_missing_application(self):
        detector = ApplicationDetector()
        with patch("launcher.restore.app_detector.shutil.which", return_value=None):
            result = detector.detect_application("node")
            self.assertEqual(result.status, "Not Available")
            self.assertIsNone(result.version)

    def test_invalid_application_id(self):
        detector = ApplicationDetector()
        result = detector.detect_application("browser")
        self.assertEqual(result.status, "Invalid")
        self.assertIn("Unsupported application ID", result.error)


if __name__ == "__main__":
    unittest.main()
