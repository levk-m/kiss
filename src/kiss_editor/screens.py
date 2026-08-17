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
    def render_label(self, node: TreeNode[DirEntry], base_style: bool, style: bool):
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
            ".kt": "🎯",
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
            # and imgs
            ".png": "🖼️",
            ".jpeg": "🖼️",
            ".jpg": "🖼️",
        }

        text = super().render_label(node, base_style, style)

        if not node.data:
            return text

        path = node.data.path

        if not path.is_dir():
            icon = ICON_MAP.get(path.suffix, "📄")
            text = Text(icon, style=text.style) + text[1:]

        return text
