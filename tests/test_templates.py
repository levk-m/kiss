from kiss_editor import templates


def _make_dir(monkeypatch, tmp_path, files=None):
    d = tmp_path / "templates"
    d.mkdir()
    for name, content in (files or {}).items():
        (d / name).write_text(content)
    monkeypatch.setattr(templates, "DIR_PATH", str(d))
    return d


def test_load_templates_missing_dir_returns_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(templates, "DIR_PATH", str(tmp_path / "nope"))
    assert templates.load_templates() == {}


def test_load_templates_reads_files(monkeypatch, tmp_path):
    _make_dir(monkeypatch, tmp_path, {"hello.py": "print('hello')"})
    assert templates.load_templates() == {"hello": "print('hello')"}
    assert isinstance(templates.load_templates()["hello"], str)


def test_load_templates_preserves_content(monkeypatch, tmp_path):
    _make_dir(
        monkeypatch,
        tmp_path,
        {"func.py": "def foo():\n    return 1\n\n    # keep me\n"},
    )
    assert (
        templates.load_templates()["func"]
        == "def foo():\n    return 1\n\n    # keep me\n"
    )


def test_load_templates_ignores_subdirs_and_hidden(monkeypatch, tmp_path):
    d = _make_dir(monkeypatch, tmp_path, {"a.py": "1", ".hidden": "2"})
    (d / "sub").mkdir()
    (d / "sub" / "b.py").write_text("3")
    assert templates.load_templates() == {"a": "1"}


def test_load_templates_skips_unreadable(monkeypatch, tmp_path):
    d = _make_dir(monkeypatch, tmp_path)
    (d / "bad.py").write_bytes(b"\xff\xfb\xbe")
    assert templates.load_templates() == {}


def test_load_templates_sorted(monkeypatch, tmp_path):
    _make_dir(monkeypatch, tmp_path, {"b.py": "1", "a.py": "2", "c.py": "3"})
    assert list(templates.load_templates()) == ["a", "b", "c"]
