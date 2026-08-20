import pytest
from rich.style import Style
from textual import events
from textual.widgets import DirectoryTree, Label

from kiss_editor.widgets import KissArea, KissDirectoryTree, StartScreen


async def test_start_screen_shows_ascii_art(app):
    the_app, pilot = app
    await the_app.push_screen(StartScreen())
    await pilot.pause()
    assert isinstance(the_app.screen, StartScreen)
    screen = the_app.screen
    label = screen.query_one(Label)
    content = str(label.content)
    assert "__ __" in content
    assert "/_/ |_/" in content


async def test_compose_uses_kiss_directory_tree(app):
    the_app, _ = app
    assert the_app.query_one(KissDirectoryTree)
    assert the_app.query_one(DirectoryTree)


async def test_kiss_directory_tree_icon_known_extension(app, tmp_path):
    the_app, pilot = app
    (tmp_path / "main.py").write_text("x")
    tree = the_app.query_one(KissDirectoryTree)
    tree.path = tmp_path
    await pilot.pause()
    tree.root.expand_all()
    await pilot.pause()
    py_node = None
    for node in tree.root.children:
        if node.data and node.data.path.name == "main.py":
            py_node = node
            break
    assert py_node is not None
    rendered = tree.render_label(py_node, Style(), Style())
    assert "\U0001f40d" in rendered.plain


async def test_kiss_directory_tree_icon_unknown_extension(app, tmp_path):
    the_app, pilot = app
    (tmp_path / "data.xyz").write_text("x")
    tree = the_app.query_one(KissDirectoryTree)
    tree.path = tmp_path
    await pilot.pause()
    tree.root.expand_all()
    await pilot.pause()
    xyz_node = None
    for node in tree.root.children:
        if node.data and node.data.path.name == "data.xyz":
            xyz_node = node
            break
    assert xyz_node is not None
    rendered = tree.render_label(xyz_node, Style(), Style())
    assert "\U0001f4c4" in rendered.plain


async def test_kiss_directory_tree_directory_no_icon_swap(app, tmp_path):
    the_app, pilot = app
    sub = tmp_path / "subdir"
    sub.mkdir()
    tree = the_app.query_one(KissDirectoryTree)
    tree.path = tmp_path
    await pilot.pause()
    tree.root.expand_all()
    await pilot.pause()
    dir_node = None
    for node in tree.root.children:
        if node.data and node.data.path.is_dir():
            dir_node = node
            break
    assert dir_node is not None
    rendered = tree.render_label(dir_node, Style(), Style())
    assert "\U0001f4c4" not in rendered.plain


async def test_kiss_directory_tree_img_icon(app, tmp_path):
    the_app, pilot = app
    (tmp_path / "photo.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    tree = the_app.query_one(KissDirectoryTree)
    tree.path = tmp_path
    await pilot.pause()
    tree.root.expand_all()
    await pilot.pause()
    png_node = None
    for node in tree.root.children:
        if node.data and node.data.path.name == "photo.png":
            png_node = node
            break
    assert png_node is not None
    rendered = tree.render_label(png_node, Style(), Style())
    assert "\U0001f5bc" in rendered.plain


async def test_kiss_directory_tree_node_without_data(app, tmp_path):
    the_app, pilot = app
    (tmp_path / "hello.py").write_text("x")
    tree = the_app.query_one(KissDirectoryTree)
    tree.path = tmp_path
    await pilot.pause()
    tree.root.expand_all()
    await pilot.pause()
    node = next(
        n for n in tree.root.children if n.data and n.data.path.name == "hello.py"
    )
    saved = node.data
    node.data = None
    try:
        rendered = tree.render_label(node, Style(), Style())
        assert rendered is not None
    finally:
        node.data = saved


async def test_kiss_area_enter_adds_extra_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "  def foo():"
    editor.cursor_location = (0, 12)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "  def foo():\n\n      "


async def test_kiss_area_enter_counts_tab_as_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "\tfoo"
    editor.cursor_location = (0, 4)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "\tfoo\n\n    "


async def test_kiss_area_enter_plain_text_no_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "hello"
    editor.cursor_location = (0, 5)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "hello\n\n"


async def test_kiss_area_enter_mid_line_no_extra_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "    foo"
    editor.cursor_location = (0, 2)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "  \n\n      foo"


async def test_kiss_area_enter_replaces_selection(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "replace me"
    editor.selection = ((0, 0), (0, 7))
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "\n\n me"


async def test_kiss_area_non_enter_key_delegates_to_super(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "ab"
    editor.cursor_location = (0, 2)
    await editor._on_key(events.Key(key="x", character="x"))
    assert editor.text == "abx"


@pytest.mark.parametrize(
    "key,character,pair",
    [
        ("left_curly_bracket", "{", "{}"),
        ("left_square_bracket", "[", "[]"),
        ("left_parenthesis", "(", "()"),
    ],
)
async def test_kiss_area_open_bracket_autocloses(app, key, character, pair):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "ab"
    editor.cursor_location = (0, 2)
    await editor._on_key(events.Key(key=key, character=character))
    assert editor.text == "ab" + pair


@pytest.mark.parametrize(
    "key,character",
    [
        ("right_curly_bracket", "}"),
        ("right_square_bracket", "]"),
        ("right_parenthesis", ")"),
    ],
)
async def test_kiss_area_close_bracket_delegates_to_super(app, key, character):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "ab"
    editor.cursor_location = (0, 2)
    await editor._on_key(events.Key(key=key, character=character))
    assert editor.text == "ab" + character


async def test_kiss_area_open_bracket_replaces_selection(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "replace me"
    editor.selection = ((0, 0), (0, 7))
    await editor._on_key(events.Key(key="left_curly_bracket", character="{"))
    assert editor.text == "{} me"


async def test_kiss_area_open_bracket_via_pilot(app):
    the_app, pilot = app
    editor = the_app.query_one(KissArea)
    editor.focus()
    await pilot.press("{")
    assert editor.text == "{}"


async def test_kiss_area_keeps_id_and_text():
    editor = KissArea("hello", id="editor", config={})
    assert editor.id == "editor"
    assert editor.text == "hello"
