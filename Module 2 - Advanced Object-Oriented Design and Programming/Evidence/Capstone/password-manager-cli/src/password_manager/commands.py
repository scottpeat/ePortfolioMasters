from __future__ import annotations

from abc import ABC, abstractmethod
from getpass import getpass
from pathlib import Path

from password_manager.exceptions import VaultError
from password_manager.models import CredentialEntry, VaultPayload
from password_manager.repository import FileVaultRepository, VaultSession
from password_manager.validation import (
    confirm_master_password_match,
    validate_master_password,
    validate_new_entry,
)


def default_vault_path() -> Path:
    return Path.home() / ".pwm" / "vault.pwm"


class VaultCommand(ABC):
    def __init__(self, vault_path: Path) -> None:
        self._vault_path = vault_path

    @abstractmethod
    def execute(self) -> int:
        """Return process exit code."""


class InitCommand(VaultCommand):
    def execute(self) -> int:
        repo = FileVaultRepository(self._vault_path)
        if repo.exists():
            print(f"Vault already exists at {self._vault_path}. Nothing to do.")
            return 1
        p1 = getpass("Choose master password: ")
        p2 = getpass("Confirm master password: ")
        try:
            validate_master_password(p1)
            confirm_master_password_match(p1, p2)
            VaultSession.create_new(repo, p1)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        print(f"Empty vault created at {self._vault_path}")
        return 0


class AddCommand(VaultCommand):
    def execute(self) -> int:
        repo = FileVaultRepository(self._vault_path)
        master = getpass("Master password: ")
        try:
            session = VaultSession.unlock(repo, master)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        title = input("Title / service name: ").strip()
        username = input("Username: ").strip()
        secret = getpass("Password to store: ")
        try:
            validate_new_entry(title, username, secret)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        payload = session.load_payload()
        payload.entries.append(CredentialEntry(title=title, username=username, password=secret))
        session.save_payload(payload)
        print("Entry saved.")
        return 0


class ListCommand(VaultCommand):
    def execute(self) -> int:
        repo = FileVaultRepository(self._vault_path)
        master = getpass("Master password: ")
        try:
            session = VaultSession.unlock(repo, master)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        payload = session.load_payload()
        if not payload.entries:
            print("No entries yet.")
            return 0
        for e in payload.entries:
            print(f"{e.entry_id}\t{e.title}\t{e.username}")
        return 0


class GetCommand(VaultCommand):
    def __init__(self, vault_path: Path, query: str) -> None:
        super().__init__(vault_path)
        self._query = query.strip()

    def execute(self) -> int:
        repo = FileVaultRepository(self._vault_path)
        master = getpass("Master password: ")
        try:
            session = VaultSession.unlock(repo, master)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        payload = session.load_payload()
        for e in payload.entries:
            if e.entry_id == self._query:
                print(f"Title: {e.title}\nUsername: {e.username}\nPassword: {e.password}")
                return 0

        title_matches = [e for e in payload.entries if e.title.lower() == self._query.lower()]
        if len(title_matches) == 1:
            entry = title_matches[0]
            print(f"Title: {entry.title}\nUsername: {entry.username}\nPassword: {entry.password}")
            return 0
        if len(title_matches) > 1:
            print("Multiple entries have this title. Use the entry id from `pwm list`.")
            for e in title_matches:
                print(f"{e.entry_id}\t{e.title}\t{e.username}")
            return 1

        print("No entry with that id or title.")
        return 1


class DeleteCommand(VaultCommand):
    def __init__(self, vault_path: Path, entry_id: str) -> None:
        super().__init__(vault_path)
        self._entry_id = entry_id

    def execute(self) -> int:
        repo = FileVaultRepository(self._vault_path)
        master = getpass("Master password: ")
        try:
            session = VaultSession.unlock(repo, master)
        except VaultError as exc:
            print(f"Error: {exc}")
            return 1
        payload = session.load_payload()
        before = len(payload.entries)
        payload.entries = [e for e in payload.entries if e.entry_id != self._entry_id]
        if len(payload.entries) == before:
            print("No entry with that id.")
            return 1
        session.save_payload(payload)
        print("Entry deleted.")
        return 0
