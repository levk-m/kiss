from rich.style import Style
from rich.text import Text
from textual.screen import Screen
from textual.widgets import DirectoryTree, Label
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
