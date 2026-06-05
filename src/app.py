import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable

from textual import events
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.command import CommandPalette
from textual.containers import Horizontal
from textual.css.query import NoMatches
from textual.highlight import guess_language
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DirectoryTree, Footer, Input, Label, Markdown, TextArea

from src.commands import SearchProvider
from src.dialogs import ErrorDialog, HelpDialog
from src.screens import StartScreen
from src.config import CONFIG_PATH, load_config, update_config_theme


class StatusBar(Horizontal):
    edit_status = reactive("EDIT")

    def compose(self) -> ComposeResult:
        yield Label(self.edit_status, id="status-label")

    def watch_edit_status(self, status: str) -> None:
        try:
            self.query_one("#status-label").update(status)
        except NoMatches:
            pass


class Kiss(App):
    TITLE = "KISS"

    CSS = """
    DirectoryTree {
        dock: left;
        width: 25%;
        border: round black;
    }
    TextArea {
        dock: right;
        width: 75%;
        border: round black;
    }
    StatusBar {
        dock: top;
        height: 1;
        background: $surface;
    }
    """

    COMMANDS = App.COMMANDS | {SearchProvider}

    BINDINGS = [
        Binding(
            key="ctrl+s", action="save_file", description="Save new changes", show=False
        ),
        Binding(key="ctrl+q", action="quit", description="quit"),
        Binding(
            key="ctrl+p", action="command_palette", description="commands", show=False
        ),
        Binding(key="ctrl+h", action="help", description="help"),
        Binding(key="ctrl+shift+c", action="edit_config", description="open config"),
    ]

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.file = None
        self.config_data = load_config()

    def compose(self):
        yield StatusBar()
        yield Horizontal(TextArea("", id="editor"), DirectoryTree(self.folder))
        yield Footer()

    def on_mount(self):
        self.theme = self.config_data.get("kiss").get("theme", "tokyo-night")
        self.push_screen(StartScreen())
        self.set_timer(0.5, self.pop_screen)

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        for cmd in super().get_system_commands(screen):
            if cmd.title in ["Theme", "Quit"]:
                yield cmd

    def on_error(self, event):
        event.prevent_default()
        self.app.push_screen(ErrorDialog("Ops", "an error occurred"))

    def _on_directory_tree_file_selected(self, event):
        footer = self.query_one(StatusBar)
        footer.edit_status = "FILE SELECTION"

        path: Path = event.path
        self.edit_file(path)

    def edit_file(self, path):
        try:
            self.file = path
            config = self.config_data.get("kiss")

            text_editor = self.query_one("#editor")
            text_editor.text = self.file.read_text() if path.is_file() else ""

            language_name = guess_language(text_editor.text, self.file)
            text_editor.language = language_name
            text_editor.theme = config.get("editor-theme", "dracula")

            text_editor.show_line_numbers = config.get("show_line_numbers", True)
            text_editor.wrap_mode = config.get("wrap_mode", "word")

            text_editor.indent_type = "spaces"
            text_editor.indent_width = 4

        except Exception as e:
            self.app.push_screen(
                ErrorDialog("Ops!", f"an error occurred, KISS cant open this file: {e}")
            )

    def action_save_file(self):
        if self.file is None:
            return
        editor = self.query_one("#editor")
        self.file.write_text(editor.text)

    def action_help(self) -> None:
        self.app.push_screen(HelpDialog())

    def action_command_palette(self) -> None:
        # just change placeholder
        self.push_screen(CommandPalette(placeholder="Search files and commands..."))

    def action_edit_config(self) -> None:
        self.edit_file(Path(CONFIG_PATH))

    def on_key(self, event: events.Key) -> None:
        if event.key in ["tab", "shift+tab"]:
            footer = self.query_one(StatusBar)
            if footer.edit_status != "FILE SELECTION":
                footer.edit_status = "FILE SELECTION"
            else:
                footer.edit_status = f"EDIT {self.file if self.file else ''}"


if __name__ == "__main__":
    parser = ArgumentParser("KISS")
    parser.add_argument("folder", type=Path)

    args = parser.parse_args()
    folder: Path = args.folder

    if not folder.exists():
        raise FileNotFoundError(f"Bad path: {folder}")

    if not folder.is_dir():
        folder = folder.parent

    app = Kiss(folder=folder)
    app.run()
    update_config_theme(app.theme)
