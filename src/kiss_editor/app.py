import importlib.metadata
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
from textual.widgets import Footer, Label, TextArea
from textual.widgets._text_area import LanguageDoesNotExist
from textual_image.widget import Image as ImageViewer

from kiss_editor.commands import SearchProvider
from kiss_editor.config import CONFIG_PATH, load_config, update_config_theme
from kiss_editor.dialogs import ErrorDialog, HelpDialog
from kiss_editor.screens import KissDirectoryTree, StartScreen

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".jfif",
    ".gif",
    ".bmp",
    ".webp",
    ".ico",
    ".tif",
    ".tiff",
    ".avif",
    ".ppm",
    ".pgm",
    ".pbm",
}


class StatusBar(Horizontal):
    edit_status = reactive("EDIT")

    def compose(self) -> ComposeResult:
        yield Label(self.edit_status, id="status-label")

    def watch_edit_status(self, status: str) -> None:
        try:
            self.query_one(Label).update(status)
        except NoMatches:
            pass


class Kiss(App):
    TITLE = "KISS"

    CSS = """
    KissDirectoryTree {
        dock: left;
        width: 25%;
        border: heavy $panel;
    }
    TextArea {
        dock: right;
        width: 75%;
        border: heavy $panel;
    }
    StatusBar {
        dock: top;
        height: 1;
        background: $surface;
    }
    CommandPalette > Vertical {
        width: 70%;
        max-width: 90;
        min-width: 40;
        border: solid $panel;
    }
    CommandPalette #--input {
        border: none;
        border-bottom: hkey $border;
    }
    CommandPalette > .command-palette--highlight {
        color: $accent;
        text-style: bold;
    }
    #image-viewer {
        dock: right;
        width: 75%;
        height: 100%;
        display: none;
        border: heavy $panel;
        padding: 1 2;
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
        Binding(
            key="ctrl+o", action="edit_config", description="open config", show=False
        ),
    ]

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.file = None
        self.config_data = load_config()
        self.saved_text = ""

    def compose(self):
        yield StatusBar()
        with Horizontal():
            yield TextArea("", id="editor")
            yield ImageViewer(id="image-viewer")
            yield KissDirectoryTree(self.folder)
        yield Footer()

    def on_mount(self):
        conf_data = self.config_data.get("kiss")
        self.theme = conf_data.get("theme", "tokyo-night")
        if conf_data.get("start-screen", False):
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
        self.app.push_screen(ErrorDialog("Error", "Something went wrong."))

    def _on_directory_tree_file_selected(self, event):
        path: Path = event.path
        self.edit_file(path)
        self._update_status()

    def _update_status(self) -> None:
        footer = self.query_one(StatusBar)
        name = self.file

        if name is not None and self._is_img(name):
            footer.edit_status = f"IMAGE {name}"
        elif self.query_one(KissDirectoryTree).has_focus:
            footer.edit_status = "FILE SELECTION"
        elif name is None:
            footer.edit_status = "EDIT"
        else:
            text_area = self.query_one(TextArea)
            row, col = text_area.cursor_location
            dirty = " *" if text_area.text != self.saved_text else ""
            footer.edit_status = f"EDIT {name}{dirty} | row: {row + 1} col: {col + 1}"

    def on_text_area_selection_changed(self, event):
        self._update_status()

    def on_descendant_focus(self, event: events.DescendantFocus) -> None:
        self._update_status()

    def edit_file(self, path):
        if self._is_img(path):
            return self._view_image(path)
        try:
            self.file = path
            config = self.config_data.get("kiss")

            text_editor = self.query_one(TextArea)
            text_editor.display = True
            self.query_one(ImageViewer).display = False
            text_editor.text = self.file.read_text() if path.is_file() else ""
            self.saved_text = text_editor.text
            try:
                language_name = guess_language(text_editor.text, self.file)
                text_editor.language = language_name
            except LanguageDoesNotExist:
                text_editor.language = ""
            text_editor.theme = config.get("editor-theme", "css")

            text_editor.show_line_numbers = config.get("show_line_numbers", True)
            text_editor.soft_wrap = config.get("soft_wrap", True)

            text_editor.indent_type = "spaces"
            text_editor.indent_width = 4

            text_editor.highlight_cursor_line = config.get(
                "highlight_cursor_line", False
            )

        except Exception as e:
            self.app.push_screen(ErrorDialog("Error", f"Couldn't open this file: {e}"))

    def action_save_file(self):
        if self.file is None or self._is_img(self.file):
            return
        editor = self.query_one(TextArea)
        self.file.write_text(editor.text)
        self.saved_text = editor.text
        self._update_status()

    def action_help(self) -> None:
        self.app.push_screen(HelpDialog())

    def action_command_palette(self) -> None:
        # just change placeholder
        self.push_screen(
            CommandPalette(placeholder="Search files or commands… (try 'help')")
        )

    def action_edit_config(self) -> None:
        self.edit_file(Path(CONFIG_PATH))

    def on_text_area_changed(self, event):
        self._update_status()

    @staticmethod
    def _is_img(path: Path) -> bool:
        return (
            path is not None
            and path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        )

    def _view_image(self, path: Path):
        try:
            viewer = self.query_one(ImageViewer)
            viewer.image = path
            self.file = path
            self.saved_text = ""
            self.query_one(TextArea).display = False
            viewer.display = True
            self._update_status()
        except Exception as e:
            self.app.push_screen(ErrorDialog("Error", f"Couldn't open this image: {e}"))


def run():
    parser = ArgumentParser(
        description="KISS - a small terminal editor",
        usage="kiss [OPTIONS]",
        epilog="""
To use:
    - kiss {folder} (open this folder)
    - kiss . (open current folder)
    - kiss {some_file} (this file and its parent folder will open)
        """,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("folder", type=Path, default=".", nargs="?")
    parser.add_argument(
        "--version", action="version", version=importlib.metadata.version("kiss-editor")
    )

    args = parser.parse_args()
    original: Path = args.folder

    if not original.exists():
        parser.error(f"Bad path -> {original}")

    folder = original if original.is_dir() else original.parent

    app = Kiss(folder=folder)
    if original.is_file():
        app.file = original

    app.run()
    update_config_theme(app.theme)


if __name__ == "__main__":
    run()
