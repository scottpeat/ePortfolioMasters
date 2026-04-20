from __future__ import annotations

import re

from password_manager.exceptions import VaultValidationError

_MASTER_MIN_LEN = 12
_TITLE_MAX = 200
_USERNAME_MAX = 200
_PASSWORD_MAX = 2000


def validate_master_password(password: str) -> None:
    if len(password) < _MASTER_MIN_LEN:
        raise VaultValidationError(
            f"Master password must be at least {_MASTER_MIN_LEN} characters."
        )


def validate_entry_field(name: str, value: str, max_len: int) -> None:
    stripped = value.strip()
    if not stripped:
        raise VaultValidationError(f"{name} cannot be empty.")
    if len(stripped) > max_len:
        raise VaultValidationError(f"{name} exceeds maximum length ({max_len}).")


def validate_new_entry(title: str, username: str, password: str) -> None:
    validate_entry_field("Title", title, _TITLE_MAX)
    validate_entry_field("Username", username, _USERNAME_MAX)
    validate_entry_field("Password", password, _PASSWORD_MAX)
    if not re.search(r"\S", password):
        raise VaultValidationError("Password must contain non-whitespace characters.")


def confirm_master_password_match(first: str, second: str) -> None:
    if first != second:
        raise VaultValidationError("Master passwords do not match.")
