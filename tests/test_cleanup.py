from launcher.cleanup import WorkspaceCleanup


def test_cleanup_removes_session(tmp_path):
    session_dir = tmp_path / "temporary_session"
    session_dir.mkdir()

    test_file = session_dir / "test.txt"
    test_file.write_text("temporary data")

    cleanup = WorkspaceCleanup(session_dir)
    cleanup.cleanup()

    assert not session_dir.exists()


def test_cleanup_with_missing_session(tmp_path):
    session_dir = tmp_path / "does_not_exist"

    cleanup = WorkspaceCleanup(session_dir)

    cleanup.cleanup()

    assert not session_dir.exists()