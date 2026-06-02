from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable

from textual.app import App, SystemCommand
from textual.containers import Horizontal
from textual.highlight import guess_language
from textual.screen import Screen
from textual.widgets import TextArea, DirectoryTree, Footer, Label

from commands import SearchProvider
from screens import SplashScreen


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
    """

    COMMANDS = App.COMMANDS | {SearchProvider}

    BINDINGS = [
        ("ctrl+s", "save_file"),
        ("ctrl+q", "quit"),
        ("ctrl+p", "command_palette"),
    ]

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.file = None

    def compose(self):
        yield Horizontal(TextArea("", id="editor"), DirectoryTree(self.folder))
        yield Footer()

    def on_mount(self):
        self.theme = "tokyo-night"
        self.push_screen(SplashScreen())
        self.set_timer(0.5, self.pop_screen)

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        for cmd in super().get_system_commands(screen):
            if cmd.title in ["Theme", "Quit"]:
                yield cmd

    def on_error(self, event):
        event.prevent_default()
        self.notify("Ops, error!", severity="error")
        self.exit()

    def _on_directory_tree_file_selected(self, event):
        path: Path = event.path
        self.edit_file(path)

    def edit_file(self, path):
        if not path.is_file():
            return
        self.file = path
        text_editor = self.query_one("#editor")
        text_editor.text = self.file.read_text()

        language_name = guess_language(text_editor.text, self.file)
        text_editor.language = language_name
        text_editor.theme = "dracula"

    def action_save_file(self):
        if self.file is None:
            return
        editor = self.query_one("#editor")
        self.file.write_text(editor.text)


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
