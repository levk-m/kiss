from rich.style import Style
from textual.widgets import DirectoryTree, Label

from kiss_editor.widgets import KissDirectoryTree, StartScreen


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
