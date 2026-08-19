from launcher.security import encrypt_data, decrypt_data


def test_encryption():
    original = b"My private college workspace"

    encrypted = encrypt_data(original, "test-password")

    assert encrypted != original

    decrypted = decrypt_data(encrypted, "test-password")

    assert decrypted == original


def test_wrong_password():
    original = b"Secret workspace data"

    encrypted = encrypt_data(original, "correct-password")

    try:
        decrypt_data(encrypted, "wrong-password")
        assert False, "Wrong password should fail"
    except ValueError:
        assert True