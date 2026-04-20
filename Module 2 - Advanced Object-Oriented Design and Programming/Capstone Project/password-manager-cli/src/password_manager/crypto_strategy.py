from __future__ import annotations

import base64
import json
import os
from abc import ABC, abstractmethod

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from password_manager.exceptions import VaultAuthError, VaultCorruptError
from password_manager.models import VaultPayload

MAGIC = b"PWMV"
FORMAT_VERSION = 1
SALT_LEN = 16
PBKDF2_ITERATIONS = 480_000


class KeyDerivation(ABC):
    @abstractmethod
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Return 32-byte key suitable for Fernet."""

    def derive_fernet(self, password: str, salt: bytes) -> Fernet:
        raw = self.derive_key(password, salt)
        return Fernet(base64.urlsafe_b64encode(raw))


class PBKDF2KeyDerivation(KeyDerivation):
    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        return kdf.derive(password.encode("utf-8"))


class CryptoStrategy(ABC):
    @abstractmethod
    def seal(self, payload: VaultPayload) -> bytes:
        """Serialize and encrypt vault payload."""

    @abstractmethod
    def open(self, ciphertext: bytes) -> VaultPayload:
        """Decrypt and deserialize."""


class FernetVaultCrypto(CryptoStrategy):
    def __init__(self, fernet: Fernet) -> None:
        self._fernet = fernet

    def seal(self, payload: VaultPayload) -> bytes:
        raw = json.dumps(payload.to_dict(), separators=(",", ":")).encode("utf-8")
        return self._fernet.encrypt(raw)

    def open(self, ciphertext: bytes) -> VaultPayload:
        try:
            raw = self._fernet.decrypt(ciphertext)
        except InvalidToken as exc:
            raise VaultAuthError("Wrong master password or corrupted vault.") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise VaultCorruptError("Vault decrypted but JSON is invalid.") from exc
        return VaultPayload.from_dict(data)


def pack_vault_file(salt: bytes, ciphertext: bytes) -> bytes:
    if len(salt) != SALT_LEN:
        raise ValueError("salt length")
    return MAGIC + bytes([FORMAT_VERSION]) + salt + ciphertext


def unpack_vault_file(blob: bytes) -> tuple[bytes, bytes]:
    header_len = len(MAGIC) + 1 + SALT_LEN
    if len(blob) < header_len:
        raise VaultCorruptError("Vault file is too short.")
    if blob[: len(MAGIC)] != MAGIC:
        raise VaultCorruptError("Unknown vault file format.")
    ver = blob[len(MAGIC)]
    if ver != FORMAT_VERSION:
        raise VaultCorruptError(f"Unsupported vault format version: {ver}.")
    salt = blob[len(MAGIC) + 1 : header_len]
    ciphertext = blob[header_len:]
    return salt, ciphertext


def random_salt() -> bytes:
    return os.urandom(SALT_LEN)
