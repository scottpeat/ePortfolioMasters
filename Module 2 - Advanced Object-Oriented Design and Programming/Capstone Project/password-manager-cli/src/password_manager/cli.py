from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from password_manager import __version__
from password_manager.commands import (
    AddCommand,
    DeleteCommand,
    GetCommand,
    InitCommand,
    ListCommand,
    default_vault_path,
)


def _vault_path_from_env() -> Path:
    raw = os.environ.get("PWM_VAULT_PATH", "").strip()
    return Path(raw).expanduser() if raw else default_vault_path()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pwm",
        description="Encrypted CLI password vault (capstone scaffold).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--vault",
        type=Path,
        default=None,
        help=f"Vault file path (default: {default_vault_path()} or $PWM_VAULT_PATH)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create a new empty encrypted vault")

    sub.add_parser("add", help="Add a credential after unlocking the vault")

    sub.add_parser("list", help="List credential ids and labels (no secrets)")

    g = sub.add_parser(
        "get",
        help="Print one entry by id or title including password (shoulder-surfing risk)",
    )
    g.add_argument(
        "query",
        metavar="ENTRY_ID_OR_TITLE",
        help="Entry id from `pwm list` or the entry title",
    )

    d = sub.add_parser("delete", help="Remove an entry by id")
    d.add_argument("id", metavar="ENTRY_ID", help="Entry id from `pwm list`")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    vault_path = (args.vault or _vault_path_from_env()).expanduser()

    cmd = args.command
    if cmd == "init":
        return InitCommand(vault_path).execute()
    if cmd == "add":
        return AddCommand(vault_path).execute()
    if cmd == "list":
        return ListCommand(vault_path).execute()
    if cmd == "get":
        return GetCommand(vault_path, args.query).execute()
    if cmd == "delete":
        return DeleteCommand(vault_path, args.id).execute()
    raise AssertionError(f"unhandled command {cmd!r}")


def run() -> None:
    sys.exit(main())


if __name__ == "__main__":
    run()
