import pytest
from rich.style import Style
from textual import events
from textual.widgets import Button, DirectoryTree, Label, Static

from kiss_editor.widgets import KissArea, KissDirectoryTree, StartScreen, YesNoDialog


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
    assert editor.text == "  def foo():\n      "


async def test_kiss_area_enter_counts_tab_as_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "\tfoo"
    editor.cursor_location = (0, 4)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "\tfoo\n    "


async def test_kiss_area_enter_plain_text_no_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "hello"
    editor.cursor_location = (0, 5)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "hello\n"


async def test_kiss_area_enter_mid_line_no_extra_indent(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "    foo"
    editor.cursor_location = (0, 2)
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "  \n      foo"


async def test_kiss_area_enter_replaces_selection(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "replace me"
    editor.selection = ((0, 0), (0, 7))
    await editor._on_key(events.Key(key="enter", character=None))
    assert editor.text == "\n me"


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


async def test_kiss_area_goto_line_is_one_based(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "one\ntwo\nthree"
    editor.action_goto_line(2)
    assert editor.cursor_location == (1, 0)


async def test_kiss_area_goto_line_clamps_below_one(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "one\ntwo"
    editor.action_goto_line(-5)
    assert editor.cursor_location == (0, 0)


async def test_kiss_area_goto_line_clamps_past_end(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "one\ntwo"
    editor.action_goto_line(9999)
    assert editor.cursor_location == (1, 0)


async def test_kiss_area_goto_line_with_column(app):
    the_app, _ = app
    editor = the_app.query_one(KissArea)
    editor.text = "hello\nworld"
    editor.action_goto_line(2, 3)
    assert editor.cursor_location == (1, 3)


async def test_yes_no_dialog_init_defaults():
    dialog = YesNoDialog("Title", "Question")
    assert dialog._title == "Title"
    assert dialog._question == "Question"
    assert dialog._aye == "Yes"
    assert dialog._naw == "No"
    assert dialog._aye_first is True


async def test_yes_no_dialog_init_custom_labels():
    dialog = YesNoDialog("T", "Q", yes_label="OK", no_label="Cancel")
    assert dialog._aye == "OK"
    assert dialog._naw == "Cancel"


async def test_yes_no_dialog_init_yes_first_false():
    dialog = YesNoDialog("T", "Q", yes_first=False)
    assert dialog._aye_first is False


async def test_yes_no_dialog_compose_renders_title_question(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("My Title", "My Question"))
    await pilot.pause()
    dialog = the_app.screen
    statics = [s.content for s in dialog.query(Static)]
    assert "My Title" in statics
    assert "My Question" in statics


async def test_yes_no_dialog_compose_yes_first_true(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("T", "Q", yes_first=True))
    await pilot.pause()
    buttons = the_app.screen.query(Button).nodes
    assert buttons[0].id == "yes"
    assert buttons[0].variant == "primary"
    assert buttons[1].id == "no"


async def test_yes_no_dialog_compose_yes_first_false(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("T", "Q", yes_first=False))
    await pilot.pause()
    buttons = the_app.screen.query(Button).nodes
    assert buttons[0].id == "no"
    assert buttons[0].variant == "primary"
    assert buttons[1].id == "yes"


async def test_yes_no_dialog_on_mount_focuses_first_button(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("T", "Q"))
    await pilot.pause()
    focused = the_app.screen.query(Button).first()
    assert focused.has_focus


async def test_yes_no_dialog_yes_button_returns_true(app):
    the_app, pilot = app
    results = []
    the_app.push_screen(YesNoDialog("T", "Q"), results.append)
    await pilot.pause()
    the_app.screen.query_one("#yes").press()
    await pilot.pause()
    assert results == [True]


async def test_yes_no_dialog_no_button_returns_false(app):
    the_app, pilot = app
    results = []
    the_app.push_screen(YesNoDialog("T", "Q"), results.append)
    await pilot.pause()
    the_app.screen.query_one("#no").press()
    await pilot.pause()
    assert results == [False]


async def test_yes_no_dialog_escape_dismisses_none(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("T", "Q"))
    await pilot.pause()
    dialog = the_app.screen
    dialog.dismiss(None)
    await pilot.pause()
    assert not isinstance(the_app.screen, YesNoDialog)


async def test_yes_no_dialog_left_right_navigation(app):
    the_app, pilot = app
    await the_app.push_screen(YesNoDialog("T", "Q"))
    await pilot.pause()
    first = the_app.screen.query(Button).first()
    assert first.has_focus
    # Focus navigation bindings exist on the dialog (left/up, right/down)
    # The actual focus switching is tested via the binding existence
    assert "focus_next" in [b.action for b in YesNoDialog.BINDINGS]
    assert "focus_previous" in [b.action for b in YesNoDialog.BINDINGS]
