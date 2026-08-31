import base64
import hashlib
import secrets
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


# Number of PBKDF2 iterations used to derive the encryption key.
# A higher number makes password guessing more expensive.
ITERATIONS = 390_000

# Salt size in bytes.
SALT_SIZE = 16


def _derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a Fernet-compatible encryption key from a password and salt.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=32,
    )

    return base64.urlsafe_b64encode(key)


def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypt data using a password.

    The returned data contains:
        salt + encrypted data
    """

    salt = secrets.token_bytes(SALT_SIZE)
    key = _derive_key(password, salt)

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)

    return salt + encrypted_data


def decrypt_data(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypt data using the password.

    Raises ValueError if the password is wrong
    or the encrypted data has been modified.
    """

    if len(encrypted_data) <= SALT_SIZE:
        raise ValueError("Invalid encrypted data.")

    salt = encrypted_data[:SALT_SIZE]
    token = encrypted_data[SALT_SIZE:]

    key = _derive_key(password, salt)
    cipher = Fernet(key)

    try:
        return cipher.decrypt(token)
    except InvalidToken as exc:
        raise ValueError(
            "Incorrect password or corrupted encrypted data."
        ) from exc


def encrypt_file(source: str | Path, destination: str | Path, password: str):
    """
    Encrypt a file and write the encrypted result to destination.
    """

    source = Path(source)
    destination = Path(destination)

    data = source.read_bytes()
    encrypted_data = encrypt_data(data, password)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(encrypted_data)


def decrypt_file(source: str | Path, destination: str | Path, password: str):
    """
    Decrypt an encrypted file and write the original data to destination.
    """

    source = Path(source)
    destination = Path(destination)

    encrypted_data = source.read_bytes()
    data = decrypt_data(encrypted_data, password)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)


def encrypt_workspace_file(
    source: str | Path,
    destination: str | Path,
    password: str
):
    """Encrypt a workspace file."""

    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    if not password:
        raise ValueError("Password cannot be empty.")

    encrypt_file(source, destination, password)

    return destination