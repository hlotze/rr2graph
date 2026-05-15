from rr2graph.tools import bump_version


def test_bump_version(tmp_path, monkeypatch, capsys):
    """Testet die Funktion bump() mit einem Fake pyproject.toml."""

    # Fake pyproject.toml im tmp_path erzeugen
    py = tmp_path / "pyproject.toml"
    py.write_text(
        "[project]\n"
        'version = "1.2.3"\n'
    )

    # PYPROJECT im Modul auf die Fake-Datei umbiegen
    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    # bump() aufrufen
    bump_version.bump("minor")

    # Ausgabe prüfen
    out = capsys.readouterr().out
    assert "Bumped version: 1.2.3 → 1.3.0" in out

    # Dateiinhalt prüfen
    content = py.read_text()
    assert 'version = "1.3.0"' in content


def test_bump_version_patch(tmp_path, monkeypatch, capsys):
    from rr2graph.tools import bump_version

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("patch")

    out = capsys.readouterr().out
    assert "1.2.3 → 1.2.4" in out
    assert 'version = "1.2.4"' in py.read_text()


def test_bump_version_major(tmp_path, monkeypatch, capsys):
    from rr2graph.tools import bump_version

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    bump_version.bump("major")

    out = capsys.readouterr().out
    assert "1.2.3 → 2.0.0" in out
    assert 'version = "2.0.0"' in py.read_text()


def test_bump_version_invalid(tmp_path, monkeypatch, capsys):
    from rr2graph.tools import bump_version
    import pytest

    py = tmp_path / "pyproject.toml"
    py.write_text('[project]\nversion = "1.2.3"\n')

    monkeypatch.setattr(bump_version, "PYPROJECT", py)

    with pytest.raises(SystemExit):
        bump_version.bump("nonsense")

    out = capsys.readouterr().out
    assert "Unknown bump type:" in out
