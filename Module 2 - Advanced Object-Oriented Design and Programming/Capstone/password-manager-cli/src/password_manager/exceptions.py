class VaultError(Exception):
    """Base error for vault operations."""


class VaultAuthError(VaultError):
    """Master password verification failed or vault is locked."""


class VaultCorruptError(VaultError):
    """Vault file is missing, truncated, or has an invalid format."""


class VaultValidationError(VaultError):
    """User input failed validation rules."""
