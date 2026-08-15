import json
from pathlib import Path
from types import SimpleNamespace

from textual.command import CommandPalette
from textual.widgets import DirectoryTree, Footer

from kiss_editor.app import Kiss, StatusBar
from kiss_editor.dialogs import ErrorDialog, HelpDialog
from kiss_editor.screens import StartScreen


async def test_compose_mounts_expected_widgets(app):
    the_app, _ = app
    assert the_app.query_one(StatusBar)
    assert the_app.query_one("#editor")
    assert the_app.query_one(DirectoryTree)
    assert the_app.query_one(Footer)


async def test_theme_from_config(config_path, tmp_path):
    config_path.write_text(json.dumps({"kiss": {"theme": "nord"}}))
    the_app = Kiss(folder=tmp_path)
    async with the_app.run_test():
        assert the_app.theme == "nord"


async def test_mount_applies_editor_settings(config_path, tmp_path, sample_dir):
    config_path.write_text(
        json.dumps(
            {
                "kiss": {
                    "editor-theme": "monokai",
                    "show_line_numbers": False,
                    "soft_wrap": False,
                    "highlight_cursor_line": True,
                }
            }
        )
    )
    the_app = Kiss(folder=tmp_path)
    async with the_app.run_test() as pilot:
        the_app.edit_file(sample_dir / "hello.py")
        await pilot.pause()
        editor = the_app.query_one("#editor")
        assert editor.show_line_numbers is False
        assert editor.soft_wrap is False
        assert editor.highlight_cursor_line is True
        assert editor.theme == "monokai"
        assert editor.indent_type == "spaces"
        assert editor.indent_width == 4


async def test_on_mount_start_screen(config_path, tmp_path):
    config_path.write_text(json.dumps({"kiss": {"start-screen": True}}))
    the_app = Kiss(folder=tmp_path)
    async with the_app.run_test():
        assert isinstance(the_app.screen, StartScreen)


async def test_on_mount_edits_preset_file(config_path, tmp_path, sample_dir):
    the_app = Kiss(folder=tmp_path)
    the_app.file = sample_dir / "hello.py"
    async with the_app.run_test():
        editor = the_app.query_one("#editor")
        assert editor.text == "print('hi')\n"
        assert editor.language == "python"


async def test_edit_file_opens_content(app, sample_dir):
    the_app, pilot = app
    target = sample_dir / "hello.py"
    the_app.edit_file(target)
    await pilot.pause()
    editor = the_app.query_one("#editor")
    assert the_app.file == target
    assert the_app.saved_text == "print('hi')\n"
    assert editor.text == "print('hi')\n"
    assert editor.language == "python"


async def test_edit_file_opens_plain_file(app, sample_dir):
    the_app, pilot = app
    target = sample_dir / "notes.txt"
    the_app.edit_file(target)
    await pilot.pause()
    editor = the_app.query_one("#editor")
    assert editor.text == "some notes\n"
    assert editor.language != "python"


async def test_edit_file_directory_sets_empty_text(app, sample_dir):
    the_app, pilot = app
    the_app.edit_file(sample_dir)
    await pilot.pause()
    assert the_app.query_one("#editor").text == ""


async def test_edit_file_read_error_shows_dialog(app, monkeypatch, tmp_path):
    target = tmp_path / "locked.py"
    target.write_text("x")
    real_read = Path.read_text

    def boom(self, *args, **kwargs):
        if self == target:
            raise PermissionError("denied")
        return real_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", boom)
    the_app, pilot = app
    the_app.edit_file(target)
    await pilot.pause()
    assert isinstance(the_app.screen, ErrorDialog)


async def test_action_save_file_writes_and_clears_dirty(app, sample_dir):
    the_app, pilot = app
    the_app.edit_file(sample_dir / "hello.py")
    editor = the_app.query_one("#editor")
    editor.text = "print('updated')\n"
    await pilot.pause()
    assert "*" in the_app.query_one(StatusBar).edit_status

    the_app.action_save_file()
    await pilot.pause()
    assert (sample_dir / "hello.py").read_text() == "print('updated')\n"
    assert the_app.saved_text == "print('updated')\n"
    assert "*" not in the_app.query_one(StatusBar).edit_status


async def test_action_save_file_without_file_is_noop(app):
    the_app, _ = app
    the_app.file = None
    the_app.action_save_file()
    assert the_app.saved_text == ""


async def test_update_status_file_selection(app):
    the_app, _ = app
    the_app._update_status("FILE_SELECTION")
    assert the_app.query_one(StatusBar).edit_status == "FILE SELECTION"


async def test_update_status_clean(app, sample_dir):
    the_app, pilot = app
    the_app.edit_file(sample_dir / "hello.py")
    await pilot.pause()
    the_app._update_status("EDIT")
    status = the_app.query_one(StatusBar).edit_status
    assert status.startswith("EDIT")
    assert "hello.py" in status
    assert "*" not in status


async def test_update_status_dirty(app, sample_dir):
    the_app, pilot = app
    the_app.edit_file(sample_dir / "hello.py")
    editor = the_app.query_one("#editor")
    editor.text = "dirty"
    await pilot.pause()
    the_app._update_status("EDIT")
    assert "*" in the_app.query_one(StatusBar).edit_status


async def test_tab_toggles_status(app):
    the_app, pilot = app
    assert the_app.query_one(StatusBar).edit_status == "EDIT"
    await pilot.press("tab")
    assert the_app.query_one(StatusBar).edit_status == "FILE SELECTION"
    await pilot.press("tab")
    assert the_app.query_one(StatusBar).edit_status.startswith("EDIT")


async def test_on_text_area_changed_marks_dirty(app, sample_dir):
    the_app, pilot = app
    the_app.edit_file(sample_dir / "hello.py")
    editor = the_app.query_one("#editor")
    editor.text = "edited"
    await pilot.pause()
    assert "*" in the_app.query_one(StatusBar).edit_status


async def test_action_help(app):
    the_app, pilot = app
    the_app.action_help()
    await pilot.pause()
    assert isinstance(the_app.screen, HelpDialog)


async def test_action_edit_config(app, config_path):
    the_app, pilot = app
    config_path.write_text(json.dumps({"kiss": {"theme": "nord"}}))
    the_app.action_edit_config()
    await pilot.pause()
    assert the_app.file == config_path
    assert the_app.query_one("#editor").text == json.dumps({"kiss": {"theme": "nord"}})


async def test_action_command_palette(app):
    the_app, pilot = app
    the_app.action_command_palette()
    await pilot.pause()
    assert isinstance(the_app.screen, CommandPalette)


async def test_directory_tree_file_selected(app, sample_dir):
    the_app, pilot = app
    target = sample_dir / "hello.py"
    the_app._on_directory_tree_file_selected(SimpleNamespace(path=target))
    await pilot.pause()
    assert the_app.query_one("#editor").text == "print('hi')\n"
    assert the_app.query_one(StatusBar).edit_status.startswith("EDIT")


async def test_on_error_shows_dialog(app):
    the_app, pilot = app
    the_app.on_error(SimpleNamespace(prevent_default=lambda: None))
    await pilot.pause()
    assert isinstance(the_app.screen, ErrorDialog)


async def test_get_system_commands_filtered(app):
    the_app, _ = app
    titles = [cmd.title for cmd in the_app.get_system_commands(the_app.screen)]
    assert titles == ["Theme", "Quit"]


def test_status_bar_watch_swallows_no_matches():
    bar = StatusBar()
    bar.edit_status = "TEST"
    assert bar.edit_status == "TEST"
