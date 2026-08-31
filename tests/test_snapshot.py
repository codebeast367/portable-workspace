from launcher.snapshot import create_workspace_snapshot


def test_workspace_snapshot(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    test_file = workspace / "hello.txt"
    test_file.write_text("private workspace data")

    encrypted_file = tmp_path / "snapshot.enc"

    result = create_workspace_snapshot(
        workspace,
        encrypted_file,
        "test-password"
    )

    assert result.exists()
    assert result.stat().st_size > 0

    # The encrypted file must not contain the plaintext.
    encrypted_data = encrypted_file.read_bytes()

    assert b"private workspace data" not in encrypted_data