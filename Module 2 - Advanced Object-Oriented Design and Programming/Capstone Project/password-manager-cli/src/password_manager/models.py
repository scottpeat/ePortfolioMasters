from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class CredentialEntry:
    """Single stored login (plaintext inside decrypted vault JSON)."""

    title: str
    username: str
    password: str
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.entry_id,
            "title": self.title,
            "username": self.username,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CredentialEntry:
        return cls(
            entry_id=str(data["id"]),
            title=str(data["title"]),
            username=str(data["username"]),
            password=str(data["password"]),
        )


@dataclass
class VaultPayload:
    """In-memory vault before encryption."""

    version: int = 1
    entries: list[CredentialEntry] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "entries": [e.to_dict() for e in self.entries],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VaultPayload:
        entries = [CredentialEntry.from_dict(e) for e in data.get("entries", [])]
        return cls(version=int(data.get("version", 1)), entries=entries)
