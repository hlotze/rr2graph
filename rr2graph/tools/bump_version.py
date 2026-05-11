#!/usr/bin/env python3
import tomllib
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")


def load_version():
    data = tomllib.loads(PYPROJECT.read_text())
    return data["project"]["version"]


def save_version(old, new):
    text = PYPROJECT.read_text()
    text = text.replace(f'version = "{old}"', f'version = "{new}"')
    PYPROJECT.write_text(text)


def bump(kind):
    old = load_version()
    major, minor, patch = map(int, old.split("."))

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
        print("Unknown bump type:", kind)
        sys.exit(1)

    new = f"{major}.{minor}.{patch}"
    save_version(old, new)
    print(f"Bumped version: {old} → {new}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bump_version.py [patch|minor|major]")
        sys.exit(1)
    bump(sys.argv[1])
