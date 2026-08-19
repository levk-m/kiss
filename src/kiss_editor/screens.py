from rich.style import Style
from rich.text import Text
from textual.screen import Screen
from textual.widgets import DirectoryTree, Label, TextArea
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode


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


class KissDirectoryTree(DirectoryTree):
    ICON_MAP = {
        ".py": "🐍",
        ".js": "🟨",  # maybe "💩" is better ? for ts too
        ".ts": "🟦",
        ".rb": "💎",
        ".php": "🐘",
        ".pl": "🐫",
        ".go": "🐹",
        ".rs": "🦀",
        ".java": "☕",
        ".kt": "🪁",
        ".swift": "🐦",
        ".cs": "🔮",
        ".c": "🦾",
        ".cpp": "➕",
        ".dart": "🎯",
        ".html": "🌐",
        ".css": "🎨",
        ".sql": "🗄️",
        ".json": "📜",
        ".yaml": "⚙️",
        ".toml": "🔧",
        ".xml": "🧩",
        ".sh": "🐚",
        ".bat": "🦇",
        ".ps1": "🟦",
        ".dockerfile": "🐳",
        ".md": "📝",
        ".lua": "🌙",
        ".r": "📊",
        ".vue": "🟢",
        ".jsx": "⚛️",
        ".tsx": "⚛️",
        ".scala": "🌀",
        ".ex": "💧",
        ".exs": "💧",
        ".hs": "λ",
        ".clj": "🦚",
        ".fs": "📐",
        ".erl": "🧪",
        ".groovy": "🥛",
        ".tf": "🧱",
        ".env": "🔑",
        ".lock": "🔒",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".jfif": "🖼️",
        ".gif": "🎞️",
        ".bmp": "🎨",
        ".webp": "🖼️",
        ".ico": "🎯",
        ".tif": "🗂️",
        ".tiff": "🗂️",
        ".avif": "📸",
        ".ppm": "📊",
        ".pgm": "🏁",
        ".pbm": "🔳",
        ".mp3": "🎵",
        ".wav": "📻",
        ".flac": "🎧",
        ".ogg": "🔊",
        ".m4a": "📱",
        ".mp4": "🎥",
        ".mkv": "🎬",
        ".avi": "🎞️",
        ".mov": "📹",
        ".webm": "🎬",
        ".zip": "📦",
        ".rar": "📚",
        ".7z": "🗜️",
        ".tar": "🧱",
        ".gz": "💨",
    }

    def render_label(
        self, node: TreeNode[DirEntry], base_style: Style, style: Style
    ) -> Text:

        text = super().render_label(node, base_style, style)

        if not node.data:
            return text

        path = node.data.path

        if not path.is_dir():
            icon = self.ICON_MAP.get(path.suffix, "📄")
            text = Text(icon, style=text.style) + text[1:]

        return text


class KissArea(TextArea):
    CSS = """
    TextArea {
        dock: right;
        width: 75%;
        border: heavy $panel;
    }
    """

    async def _on_key(self, event):
        if event.key == "enter":
            event.stop()
            event.prevent_default()

            row, col = self.cursor_location
            lines = self.text.split("\n")

            curr_line = lines[row] if row < len(lines) else ""

            indent = 0
            for ch in curr_line:
                if ch == " ":
                    indent += 1
                elif ch == "\t":  # tab
                    indent += 4
                else:
                    break

            text_before = curr_line[:col].rstrip()
            if text_before and text_before[-1] in [":", "(", "{", "["]:
                indent += 4

            start, end = self.selection
            self._replace_via_keyboard("\n" + " " * indent, start, end)
            return
        await super()._on_key(event)
