import webbrowser

from rich.text import TextType
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Markdown, OptionList, Static
from textual.widgets._button import ButtonVariant
from textual.widgets.option_list import Option

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


class InputDialog(ModalScreen[str | None]):
    DEFAULT_CSS = """
    InputDialog {
        align: center middle;
    }

    InputDialog > Vertical {
        background: $boost;
        min-width: 30%;
        width: auto;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }
    """

    BINDINGS = [Binding("escape", "dismiss(None)", "", show=False)]

    def __init__(self, title: str) -> None:
        super().__init__()
        self._title = title

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self._title)
            yield Input()

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class TemplateDialog(ModalScreen[str | None]):
    """List of templates; dismisses with the selected template code or None."""

    DEFAULT_CSS = """
    TemplateDialog {
        align: center middle;
    }

    TemplateDialog > Vertical {
        background: $boost;
        width: 50%;
        height: 60%;
        border: solid $primary;
        padding: 1 2;
    }

    TemplateDialog Input {
        margin-bottom: 1;
    }

    TemplateDialog OptionList {
        border: solid $panel;
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss(None)", "", show=False),
        Binding("up", "list_up", "", show=False),
        Binding("down", "list_down", "", show=False),
    ]

    def __init__(
        self, templates: dict[str, str], title: str = "Insert template"
    ) -> None:
        super().__init__()
        self._templates = templates
        self._title = title

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self._title)
            yield Input(placeholder="Filter by name…", id="filter")
            yield OptionList(*(Option(name, id=name) for name in self._templates))

    def on_mount(self) -> None:
        self.query_one(OptionList).highlighted = 0
        self.query_one("#filter").focus()

    def _set_options(self, query: str) -> None:
        option_list = self.query_one(OptionList)
        option_list.clear_options()
        option_list.add_options(
            Option(name, id=name)
            for name in self._templates
            if query.lower() in name.lower()
        )
        option_list.highlighted = 0 if option_list.option_count else None

    def on_input_changed(self, event: Input.Changed) -> None:
        self._set_options(event.value.strip())

    def _selected_code(self) -> str | None:
        option_list = self.query_one(OptionList)
        index = option_list.highlighted
        if index is None:
            return None
        option = option_list.options[index]
        return self._templates.get(option.id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        code = self._selected_code()
        if code is not None:
            self.dismiss(code)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(self._templates[event.option.id])

    def action_list_up(self) -> None:
        self.query_one(OptionList).action_cursor_up()

    def action_list_down(self) -> None:
        self.query_one(OptionList).action_cursor_down()
