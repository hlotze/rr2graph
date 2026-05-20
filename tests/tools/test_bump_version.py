"""Unit tests for rr2graph.tools.bump_version."""

import sys

import pytest

from rr2graph.tools import bump_version


def test_bump_version(tmp_path, monkeypatch, capsys):
    """Bump the minor version successfully."""

    py = tmp_path / "pyproject.toml"
    py.write_text(
        "[project]\n"
        'version = "1.2.3"\n'
    )

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("minor")

    out = capsys.readouterr().out

    assert "Bumped version: 1.2.3 → 1.3.0" in out
    assert 'version = "1.3.0"' in py.read_text()


def test_bump_version_patch(tmp_path, monkeypatch, capsys):
    """Bump the patch version successfully."""

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("patch")

    out = capsys.readouterr().out

    assert "1.2.3 → 1.2.4" in out
    assert 'version = "1.2.4"' in py.read_text()


def test_bump_version_major(tmp_path, monkeypatch, capsys):
    """Bump the major version successfully."""

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("major")

    out = capsys.readouterr().out

    assert "1.2.3 → 2.0.0" in out
    assert 'version = "2.0.0"' in py.read_text()


def test_bump_version_invalid(tmp_path, monkeypatch, capsys):
    """Reject unsupported version bump types."""

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    with pytest.raises(SystemExit):
        bump_version.bump("nonsense")

    out = capsys.readouterr().out

    assert "Unknown bump type:" in out


def test_bump_version_dry_run(tmp_path, monkeypatch, capsys):
    """Ensure dry-run mode does not modify pyproject.toml."""

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("minor", dry_run=True)

    out = capsys.readouterr().out

    assert "[DRY-RUN] Version bump: 1.2.3 → 1.3.0" in out
    assert 'version = "1.2.3"' in py.read_text()


def test_validate_version_valid():
    """Validate correct semantic version parsing."""

    assert bump_version.validate_version("1.2.3") == (1, 2, 3)


@pytest.mark.parametrize(
    "version",
    ["1.2", "1", "abc", "1.2.3.4", "v1.2.3", ""],
)
def test_validate_version_invalid(version):
    """Reject invalid semantic version strings."""

    with pytest.raises(ValueError):
        bump_version.validate_version(version)


def test_load_version_missing_file(tmp_path, monkeypatch):
    """Raise FileNotFoundError when pyproject.toml is missing."""

    missing = tmp_path / "does_not_exist.toml"
    monkeypatch.setattr(bump_version, "PYPROJECT", missing)

    with pytest.raises(FileNotFoundError):
        bump_version.load_version()


def test_parse_args_patch(monkeypatch):
    """Parse a standard patch CLI invocation."""

    monkeypatch.setattr(sys, "argv", ["bump_version.py", "patch"])
    args = bump_version.parse_args()

    assert args.kind == "patch"
    assert args.dry_run is False


def test_parse_args_dry_run(monkeypatch):
    """Parse a dry-run CLI invocation."""

    monkeypatch.setattr(sys, "argv", ["bump_version.py", "minor", "--dry-run"])
    args = bump_version.parse_args()

    assert args.kind == "minor"
    assert args.dry_run is True


def test_main_success(monkeypatch):
    """Execute main CLI workflow successfully."""

    class DummyArgs:
        kind = "patch"
        dry_run = True

    monkeypatch.setattr(bump_version, "parse_args", lambda: DummyArgs())

    called = {}

    def fake_bump(kind, dry_run=False):
        called["kind"] = kind
        called["dry_run"] = dry_run
        return "1.2.4"

    monkeypatch.setattr(bump_version, "bump", fake_bump)

    bump_version.main()

    assert called["kind"] == "patch"
    assert called["dry_run"] is True


def test_main_exception(monkeypatch, capsys):
    """Handle CLI exception and exit."""

    class DummyArgs:
        kind = "patch"
        dry_run = False

    monkeypatch.setattr(bump_version, "parse_args", lambda: DummyArgs())

    def fake_bump(kind, dry_run=False):
        raise RuntimeError("boom")

    monkeypatch.setattr(bump_version, "bump", fake_bump)

    with pytest.raises(SystemExit):
        bump_version.main()

    out = capsys.readouterr().out
    assert "Error: boom" in out
