from types import SimpleNamespace

import kiss_editor.dialogs as dialogs
from kiss_editor.data.help_md import HELP
from kiss_editor.dialogs import ErrorDialog, HelpDialog, InputDialog, TextDialog
from textual.widgets import Button, Input, Markdown, Static


def test_text_dialog_attributes():
    dialog = TextDialog("Title", "Message")
    assert dialog._title == "Title"
    assert dialog._message == "Message"
    assert dialog.button_style == "primary"


def test_error_dialog_button_style():
    assert ErrorDialog("E", "M").button_style == "error"


async def test_text_dialog_renders(app):
    the_app, pilot = app
    await the_app.push_screen(TextDialog("Title", "Message"))
    await pilot.pause()
    assert isinstance(the_app.screen, TextDialog)
    dialog = the_app.screen
    messages = [s.content for s in dialog.query(Static)]
    assert "Title" in messages
    assert "Message" in messages
    assert dialog.query_one(Button)


async def test_error_dialog_renders(app):
    the_app, pilot = app
    await the_app.push_screen(ErrorDialog("Error", "Something went wrong."))
    await pilot.pause()
    assert isinstance(the_app.screen, ErrorDialog)
    dialog = the_app.screen
    assert any("Something went wrong." in s.content for s in dialog.query(Static))


async def test_text_dialog_button_dismisses(app):
    the_app, pilot = app
    await the_app.push_screen(TextDialog("Title", "Message"))
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()
    assert not isinstance(the_app.screen, TextDialog)


async def test_help_dialog_renders_help(app):
    the_app, pilot = app
    await the_app.push_screen(HelpDialog())
    await pilot.pause()
    assert isinstance(the_app.screen, HelpDialog)
    dialog = the_app.screen
    markdown = dialog.query_one(Markdown)
    assert markdown.source == HELP
    assert dialog.query_one(Button)


async def test_help_dialog_escape_dismisses(app):
    the_app, pilot = app
    await the_app.push_screen(HelpDialog())
    await pilot.pause()
    await pilot.press("escape")
    await pilot.pause()
    assert not isinstance(the_app.screen, HelpDialog)


async def test_help_dialog_close_button_dismisses(app):
    the_app, pilot = app
    await the_app.push_screen(HelpDialog())
    await pilot.pause()
    dialog = the_app.screen
    dialog.query_one(Button).focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()
    assert not isinstance(the_app.screen, HelpDialog)


def test_help_dialog_link_opens_browser(monkeypatch):
    opened = []
    monkeypatch.setattr(dialogs.webbrowser, "open", lambda href: opened.append(href))
    dialog = HelpDialog()
    dialog.on_markdown_link_clicked(SimpleNamespace(href="https://example.com"))
    assert opened == ["https://example.com"]


async def test_input_dialog_renders_and_focuses_input(app):
    the_app, pilot = app
    await the_app.push_screen(InputDialog("Go to line"))
    await pilot.pause()
    dialog = the_app.screen
    assert isinstance(dialog, InputDialog)
    assert any("Go to line" in s.content for s in dialog.query(Static))
    assert dialog.query_one(Input).has_focus


async def test_input_dialog_enter_dismisses_with_value(app):
    the_app, pilot = app
    results = []
    the_app.push_screen(InputDialog("Go to line"), results.append)
    await pilot.pause()
    the_app.screen.query_one(Input).value = "42"
    await pilot.press("enter")
    await pilot.pause()
    assert results == ["42"]
    assert not isinstance(the_app.screen, InputDialog)


async def test_input_dialog_escape_dismisses_with_none(app):
    the_app, pilot = app
    results = []
    the_app.push_screen(InputDialog("Go to line"), results.append)
    await pilot.pause()
    await pilot.press("escape")
    await pilot.pause()
    assert results == [None]
