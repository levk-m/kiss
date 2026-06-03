from textual.screen import Screen
from textual.widgets import Label
import pyfiglet


class StartScreen(Screen):
    CSS = """
        SplashScreen {
            align: center middle;
            background: $background;
        }
        SplashScreen Label {
            color: $accent;
        }
        """

    def compose(self):
        text = pyfiglet.figlet_format("KISS", font="slant")
        yield Label(text)
