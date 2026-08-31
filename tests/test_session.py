from pathlib import Path

from launcher.session import WorkspaceSession


def test_session_save(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    original_file = workspace / "test.txt"
    original_file.write_text("original")

    session = WorkspaceSession(workspace)

    temporary_dir = session.start()

    temporary_file = temporary_dir / "test.txt"
    temporary_file.write_text("changed")

    session.save()

    assert original_file.read_text() == "changed"


def test_session_discard(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    original_file = workspace / "test.txt"
    original_file.write_text("original")

    session = WorkspaceSession(workspace)

    temporary_dir = session.start()

    temporary_file = temporary_dir / "test.txt"
    temporary_file.write_text("changed")

    session.discard()

    assert original_file.read_text() == "original"
    assert not temporary_dir.exists()