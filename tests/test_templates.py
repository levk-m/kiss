import kiss_editor.templates as templates


def _set_path(monkeypatch, tmp_path, content=None, *, exists=True):
    path = tmp_path / "templates.ini"
    if content is not None:
        path.write_text(content)
    monkeypatch.setattr(templates, "FILE_PATH", str(path))
    if not exists:
        monkeypatch.setattr(templates.os.path, "exists", lambda p: False)
    return path


def test_load_templates_missing_file_returns_empty(monkeypatch, tmp_path):
    _set_path(monkeypatch, tmp_path, exists=False)
    assert templates.load_templates() == {}


def test_load_templates_no_section_returns_empty(monkeypatch, tmp_path):
    _set_path(monkeypatch, tmp_path, "[other]\nkey = value\n")
    assert templates.load_templates() == {}


def test_load_templates_reads_section(monkeypatch, tmp_path):
    _set_path(monkeypatch, tmp_path, "[templates]\nhello = print('hello')\n")
    assert templates.load_templates() == {"hello": "print('hello')"}


def test_load_templates_multiline_value(monkeypatch, tmp_path):
    _set_path(
        monkeypatch,
        tmp_path,
        "[templates]\nfunc = def foo():\n    return 1\n",
    )
    assert templates.load_templates()["func"] == "def foo():\nreturn 1"


def test_load_templates_percent_sign_is_literal(monkeypatch, tmp_path):
    _set_path(
        monkeypatch,
        tmp_path,
        "[templates]\nf = '%s' % name\n",
    )
    assert templates.load_templates() == {"f": "'%s' % name"}


def test_load_templates_bad_encoding_returns_empty(monkeypatch, tmp_path):
    path = _set_path(monkeypatch, tmp_path)
    path.write_bytes(b"\xff\xfb\xbe")
    assert templates.load_templates() == {}
