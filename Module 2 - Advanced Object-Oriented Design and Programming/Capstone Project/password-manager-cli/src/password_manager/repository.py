from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from password_manager.crypto_strategy import (
    CryptoStrategy,
    FernetVaultCrypto,
    PBKDF2KeyDerivation,
    pack_vault_file,
    random_salt,
    unpack_vault_file,
)
from password_manager.exceptions import VaultCorruptError
from password_manager.models import VaultPayload


class VaultRepository(ABC):
    """Persistence boundary for encrypted vault bytes."""

    @abstractmethod
    def exists(self) -> bool:
        ...

    @abstractmethod
    def read_encrypted(self) -> tuple[bytes, bytes]:
        """Return (salt, ciphertext) for the sealed vault body."""

    @abstractmethod
    def write_encrypted(self, salt: bytes, ciphertext: bytes) -> None:
        ...


class FileVaultRepository(VaultRepository):
    def __init__(self, path: Path) -> None:
        self._path = path

    def exists(self) -> bool:
        return self._path.is_file()

    def read_encrypted(self) -> tuple[bytes, bytes]:
        try:
            blob = self._path.read_bytes()
        except OSError as exc:
            raise VaultCorruptError(f"Cannot read vault: {exc}") from exc
        return unpack_vault_file(blob)

    def write_encrypted(self, salt: bytes, ciphertext: bytes) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = pack_vault_file(salt, ciphertext)
        try:
            self._path.write_bytes(data)
        except OSError as exc:
            raise VaultCorruptError(f"Cannot write vault: {exc}") from exc


class VaultSession:
    """Binds repository + crypto after successful unlock (Facade-style orchestration)."""

    def __init__(
        self,
        repository: VaultRepository,
        crypto: CryptoStrategy,
        salt: bytes,
    ) -> None:
        self._repository = repository
        self._crypto = crypto
        self._salt = salt

    @property
    def salt(self) -> bytes:
        return self._salt

    def load_payload(self) -> VaultPayload:
        _, ciphertext = self._repository.read_encrypted()
        return self._crypto.open(ciphertext)

    def save_payload(self, payload: VaultPayload) -> None:
        ciphertext = self._crypto.seal(payload)
        self._repository.write_encrypted(self._salt, ciphertext)

    @classmethod
    def create_new(
        cls,
        repository: VaultRepository,
        master_password: str,
        kdf: PBKDF2KeyDerivation | None = None,
    ) -> VaultSession:
        if repository.exists():
            raise VaultCorruptError("Vault already exists at this path.")
        kdf = kdf or PBKDF2KeyDerivation()
        salt = random_salt()
        fernet = kdf.derive_fernet(master_password, salt)
        crypto = FernetVaultCrypto(fernet)
        session = cls(repository, crypto, salt)
        session.save_payload(VaultPayload())
        return session

    @classmethod
    def unlock(
        cls,
        repository: VaultRepository,
        master_password: str,
        kdf: PBKDF2KeyDerivation | None = None,
    ) -> VaultSession:
        if not repository.exists():
            raise VaultCorruptError("No vault found. Run `pwm init` first.")
        kdf = kdf or PBKDF2KeyDerivation()
        salt, _ = repository.read_encrypted()
        fernet = kdf.derive_fernet(master_password, salt)
        crypto = FernetVaultCrypto(fernet)
        session = cls(repository, crypto, salt)
        session.load_payload()
        return session
