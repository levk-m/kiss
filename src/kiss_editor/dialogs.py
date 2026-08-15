import webbrowser

from rich.text import TextType
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Markdown, Static
from textual.widgets._button import ButtonVariant

from kiss_editor.data.help_md import HELP


class TextDialog(ModalScreen[None]):
    DEFAULT_CSS = """
    TextDialog {
        align: center middle;
    }

    TextDialog Center {
        width: 100%;
    }

    TextDialog > Vertical {
        background: $boost;
        min-width: 30%;
        width: auto;
        height: auto;
        border: solid $primary;
    }

    TextDialog Static {
        width: auto;
    }

    TextDialog .spaced {
        padding: 1 4;
    }

    TextDialog #message {
        min-width: 100%;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss(None)", "", show=False),
    ]

    def __init__(self, title: TextType, message: TextType) -> None:
        super().__init__()
        self._title = title
        self._message = message

    @property
    def button_style(self) -> ButtonVariant:
        return "primary"

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Static(self._title, classes="spaced")
            yield Static(self._message, id="message", classes="spaced")
            with Center(classes="spaced"):
                yield Button("OK", variant=self.button_style)

    def on_mount(self) -> None:
        self.query_one(Button).focus()

    def on_button_pressed(self) -> None:
        self.dismiss(None)


class ErrorDialog(TextDialog):
    DEFAULT_CSS = """
        ErrorDialog > Vertical {
            background: $error 15%;
            border: thick $error 50%;
        }

        ErrorDialog #message {
            border-top: solid $panel;
            border-bottom: solid $panel;
        }
        """

    @property
    def button_style(self) -> ButtonVariant:
        return "error"


class HelpDialog(ModalScreen[None]):
    DEFAULT_CSS = """
        HelpDialog {
            align: center middle;
        }

        HelpDialog > Vertical {
            border: thick $primary 50%;
            width: 80%;
            height: 80%;
            background: $boost;
        }

        HelpDialog > Vertical > VerticalScroll {
            height: 1fr;
            margin: 1 2;
        }

        HelpDialog > Vertical > Center {
            padding: 1;
            height: auto;
        }
    """

    BINDINGS = [Binding("escape, ctrl+h", "dismiss(None)", "", show=True)]

    def compose(self) -> ComposeResult:
        with Vertical():
            with VerticalScroll():
                yield Markdown(HELP)
            with Center():
                yield Button("Close", variant="primary")

    def on_mount(self) -> None:
        self.query_one(Markdown).can_focus_children = False
        self.query_one("Vertical > VerticalScroll").focus()

    def on_button_pressed(self) -> None:
        self.dismiss(None)

    def on_markdown_link_clicked(self, event) -> None:
        # just open in browser
        webbrowser.open(event.href)
