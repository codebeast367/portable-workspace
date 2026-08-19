import tempfile
import unittest
from pathlib import Path

from launcher.restore.file_restore import FileRestorer


class TestFileRestorer(unittest.TestCase):
    def test_single_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            source.mkdir()
            file_path = source / "notes" / "hello.txt"
            file_path.parent.mkdir(parents=True)
            file_path.write_text("hello world", encoding="utf-8")

            result = FileRestorer().restore_files(source, ["notes/hello.txt"], destination)

            self.assertEqual(result.restored, ["notes/hello.txt"])
            self.assertTrue((destination / "notes" / "hello.txt").exists())
            self.assertEqual((destination / "notes" / "hello.txt").read_text(encoding="utf-8"), "hello world")

    def test_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            folder = source / "projects" / "demo"
            folder.mkdir(parents=True)
            (folder / "main.py").write_text("print('ok')", encoding="utf-8")

            result = FileRestorer().restore_files(source, ["projects"], destination)

            self.assertIn("projects", result.restored)
            self.assertTrue((destination / "projects" / "demo" / "main.py").exists())

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            nested = source / "documents" / "semester" / "notes"
            nested.mkdir(parents=True)
            (nested / "plan.md").write_text("# plan", encoding="utf-8")

            result = FileRestorer().restore_files(source, ["documents/semester"], destination)

            self.assertIn("documents/semester", result.restored)
            self.assertTrue((destination / "documents" / "semester" / "notes" / "plan.md").exists())

    def test_missing_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            result = FileRestorer().restore_files(source, ["missing.txt"], destination)
            self.assertIn("missing.txt", result.failed)

    def test_destination_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            source.mkdir()
            (source / "file.txt").write_text("data", encoding="utf-8")

            FileRestorer().restore_files(source, ["file.txt"], destination)

            self.assertTrue(destination.exists())
            self.assertTrue((destination / "file.txt").exists())

    def test_path_traversal_attack(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            destination = Path(tmpdir) / "dest"
            source.mkdir()
            result = FileRestorer().restore_files(source, ["../../Windows/system32"], destination)
            self.assertIn("../../Windows/system32", result.failed)


if __name__ == "__main__":
    unittest.main()
