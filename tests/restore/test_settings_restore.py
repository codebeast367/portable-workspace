import json
import tempfile
import unittest
from pathlib import Path

from launcher.restore.settings_restore import SettingsRestorer


class TestSettingsRestorer(unittest.TestCase):
    def test_valid_vscode_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "source"
            dst = root / "dest"
            vscode_dir = src / "settings" / "vscode"
            vscode_dir.mkdir(parents=True)
            (vscode_dir / "settings.json").write_text(json.dumps({"files.autoSave": "afterDelay"}), encoding="utf-8")
            (vscode_dir / "keybindings.json").write_text("[]", encoding="utf-8")
            snippet_dir = vscode_dir / "snippets"
            snippet_dir.mkdir()
            (snippet_dir / "sample.code-snippets").write_text("{}", encoding="utf-8")

            result = SettingsRestorer().restore_vscode_settings(src / "settings" / "vscode", dst)

            self.assertIn("settings.json", result.restored)
            self.assertIn("keybindings.json", result.restored)
            self.assertIn("snippets", result.restored)

    def test_missing_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "source"
            dst = root / "dest"
            src.mkdir()
            result = SettingsRestorer().restore_vscode_settings(src, dst)
            self.assertIn("settings.json", result.skipped)

    def test_malformed_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "source"
            dst = root / "dest"
            vscode_dir = src / "settings" / "vscode"
            vscode_dir.mkdir(parents=True)
            (vscode_dir / "settings.json").write_text("{not valid json}", encoding="utf-8")

            result = SettingsRestorer().restore_vscode_settings(src / "settings" / "vscode", dst)

            self.assertIn("settings.json", result.failed)

    def test_skipped_unsupported_settings(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "source"
            dst = root / "dest"
            src.mkdir()
            result = SettingsRestorer().restore_settings(src, dst, {"vscode": True, "git": True, "terminal": True, "browser": True})
            self.assertIn("browser", result.skipped)


if __name__ == "__main__":
    unittest.main()
