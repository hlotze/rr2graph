#!/usr/bin/env python3
"""
Semantic version bump utility for rr2graph.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
import tomllib

PYPROJECT: Path = Path("pyproject.toml")
SEMVER_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def load_version() -> str:
    """Load version from pyproject.toml."""
    if not PYPROJECT.exists():
        raise FileNotFoundError(f"Missing file: {PYPROJECT}")

    data = tomllib.loads(PYPROJECT.read_text())
    return data["project"]["version"]


def save_version(old: str, new: str) -> None:
    """Write updated version back into pyproject.toml."""
    text = PYPROJECT.read_text()
    text = text.replace(f'version = "{old}"', f'version = "{new}"')
    PYPROJECT.write_text(text)


def validate_version(version: str) -> tuple[int, int, int]:
    """Validate semantic version string."""
    match = SEMVER_PATTERN.match(version)
    if not match:
        raise ValueError(f"Invalid semantic version: {version}")

    return tuple(map(int, match.groups()))


def bump(kind: str, dry_run: bool = False) -> str:
    """Bump semantic version."""
    old = load_version()
    major, minor, patch = validate_version(old)

    if kind == "patch":
        patch += 1
    elif kind == "minor":
        minor += 1
        patch = 0
    elif kind == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        print(f"Unknown bump type: {kind}")
        sys.exit(1)

    new = f"{major}.{minor}.{patch}"

    if dry_run:
        print(f"[DRY-RUN] Version bump: {old} → {new}")
        return new

    save_version(old, new)
    print(f"Bumped version: {old} → {new}")

    return new


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bump semantic version")

    parser.add_argument(
        "kind",
        choices=["patch", "minor", "major"],
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        bump(args.kind, args.dry_run)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
