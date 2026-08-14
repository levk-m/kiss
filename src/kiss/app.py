from argparse import ArgumentParser, RawDescriptionHelpFormatter
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
from textual.widgets import DirectoryTree, Footer, Label, TextArea

from kiss.commands import SearchProvider
from kiss.config import CONFIG_PATH, load_config, update_config_theme
from kiss.dialogs import ErrorDialog, HelpDialog
from kiss.screens import StartScreen


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
        self.saved_text = ""

    def compose(self):
        yield StatusBar()
        yield Horizontal(TextArea("", id="editor"), DirectoryTree(self.folder))
        yield Footer()

    def on_mount(self):
        self.theme = self.config_data.get("kiss").get("theme", "tokyo-night")
        self.push_screen(StartScreen())
        self.set_timer(0.5, self.pop_screen)
        if self.file:
            self.edit_file(self.file)

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

    def _update_status(self, mode: str, file: Path | None = None) -> None:
        footer = self.query_one(StatusBar)
        if mode == "FILE_SELECTION":
            footer.edit_status = "FILE SELECTION"
        else:
            editor = self.query_one("#editor")
            dirty = " *" if editor.text != self.saved_text else ""
            name = file or self.file
            footer.edit_status = f"EDIT {name}{dirty}"

    def edit_file(self, path):
        try:
            self.file = path
            config = self.config_data.get("kiss")

            text_editor = self.query_one("#editor")
            text_editor.text = self.file.read_text() if path.is_file() else ""
            self.saved_text = text_editor.text

            language_name = guess_language(text_editor.text, self.file)
            text_editor.language = language_name
            text_editor.theme = config.get("editor-theme", "dracula")

            text_editor.show_line_numbers = config.get("show_line_numbers", True)
            text_editor.wrap_mode = config.get("wrap_mode", "word")

            text_editor.indent_type = "spaces"
            text_editor.indent_width = 4

            text_editor.highlight_cursor_line = config.get(
                "highlight_cursor_line", False
            )

        except Exception as e:
            self.app.push_screen(
                ErrorDialog("Ops!", f"an error occurred, KISS cant open this file: {e}")
            )

    def action_save_file(self):
        if self.file is None:
            return
        editor = self.query_one("#editor")
        self.file.write_text(editor.text)
        self.saved_text = editor.text
        self._update_status("EDIT")

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
                self._update_status("FILE_SELECTION")
            else:
                self._update_status("EDIT")

    def on_text_area_changed(self, event):
        self._update_status("EDIT")


def run():
    parser = ArgumentParser(
        description="KISS - just code it",
        usage="kiss [OPTIONS]",
        epilog="""
To use:
    - kiss {folder} (open this folder)
    - kiss . (open current folder)
    - kiss {some_file} (this file and its parent folder will open)
        """,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("folder", type=Path)
    parser.add_argument("--version", action="version", version="KISS 0.1.0")

    args = parser.parse_args()
    original: Path = args.folder

    if not original.exists():
        raise FileNotFoundError(f"Bad path: {original}")

    folder = original if original.is_dir() else original.parent

    app = Kiss(folder=folder)
    if original.is_file():
        app.file = original

    app.run()
    update_config_theme(app.theme)


if __name__ == "__main__":
    run()
