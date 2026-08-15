from textual.screen import Screen
from textual.widgets import Label


class StartScreen(Screen):
    CSS = """
        StartScreen {
            align: center middle;
            background: $background;
        }
        StartScreen Label {
            color: $accent;
        }
        """

    def compose(self):
        text = r"""
        __ __ ______________
       / //_//  _/ ___/ ___/
      / ,<   / / \__ \\__ \
     / /| |_/ / ___/ /__/ /
    /_/ |_/___//____/____/

        """
        yield Label(text)
