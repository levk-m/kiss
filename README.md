                _  _____ ________
               | |/ /| |/ __|/ __|
               | ' <\| |\__ \ (__
               |_|\_\|_|___/\___|

                      KISS
            keep it simple, stupid.

A terminal text editor. Not an IDE, not Emacs, not Vim.
Just an editor. Syntax highlighting, file tree, undo/redo.
The middle ground between nano and vim — usable by default.

---

## Why KISS?

| What | Why |
|------|-----|
| [Textual](https://github.com/Textualize/textual) framework | Modern TUI, no curses hell |
| No LSP, no plugins, no bloat | It edits files. That's it. |
| Opens in <100ms | Fast enough to be your `$EDITOR` |

---

## Install

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/MarkLevkovich/keepiss.git
cd keepiss
uv sync
uv run kiss
```

Or run directly without cloning:

```bash
uvx kiss
```

---

## Usage

```
kiss <file>         Edit a file
kiss <dir>          Browse a directory
kiss .              Open current directory
```

---

## Features

- **File tree** — browse and open files from the sidebar
- **Syntax highlighting** — auto-detected, Dracula by default
- **Command palette** (`Ctrl+P`) — fuzzy-find files, switch themes
- **Undo / Redo** — `Ctrl+Z` / `Ctrl+Y`
- **Clipboard** — cut, copy, paste (`Ctrl+X/C/V`)
- **Line numbers**, word wrap, cursor line highlight
- **Config** — `~/.kiss_conf.json`, open with `Ctrl+Shift+C`
- **Help dialog** — `Ctrl+H`
- **Splash screen** — pyfiglet logo on startup
- **Status bar** — shows filename, unsaved changes (`*`), focus mode

---

## Keybindings

### Navigation

| Key | Action |
|-----|--------|
| Arrows | Move cursor |
| `Home` / `Ctrl+A` | Go to line start |
| `End` / `Ctrl+E` | Go to line end |
| `PgUp` / `Ctrl+PgUp` | Page up |
| `PgDn` / `Ctrl+PgDn` | Page down |
| `Ctrl+Left` / `Ctrl+Right` | Page left / right |
| `Alt+Left` | Word start |
| `Alt+Right` | Word end |

### Selection

| Key | Action |
|-----|--------|
| `Shift`+Arrows | Select character / line |
| `Shift+Home` | Select to line start |
| `Shift+End` | Select to line end |
| `Shift+PgUp` / `Shift+PgDn` | Select page up / down |
| `F6` | Select current line |
| `F7` | Select all |

### Editing

| Key | Action |
|-----|--------|
| `Backspace` / `Ctrl+Backspace` | Delete char before cursor |
| `Delete` / `Ctrl+D` | Delete char under cursor |
| `Alt+Del` | Delete to start of word |
| `Ctrl+U` | Delete to line start |
| `Ctrl+K` | Delete to line end |
| `Ctrl+Left` / `Ctrl+Right` | Decrease / increase indent |
| `Ctrl+X` / `Super+X` | Cut |
| `Ctrl+C` / `Super+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

### Interface

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Focus next / previous element |
| `Ctrl+S` | Save |
| `Ctrl+P` | Command palette (files, themes) |
| `Ctrl+H` | Help dialog |
| `Ctrl+Shift+C` | Open config (`~/.kiss_conf.json`) |
| `Ctrl+Q` | Quit |

---

## Configuration

JSON config file at `~/.kiss_conf.json`. Open it with `Ctrl+Shift+C` — changes take effect after restart.

```json
{
  "kiss": {
    "theme": "tokyo-night",
    "editor-theme": "dracula",
    "show_line_numbers": true,
    "wrap_mode": "word",
    "highlight_cursor_line": false
  }
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `kiss.theme` | `"tokyo-night"` | Application theme |
| `kiss.editor-theme` | `"dracula"` | Syntax highlighting colors |
| `kiss.show_line_numbers` | `true` | Show line numbers |
| `kiss.wrap_mode` | `"word"` | Text wrapping mode |
| `kiss.highlight_cursor_line` | `false` | Highlight current line |

---

## TODO

- **Enter handling** — auto-indent to match the current line on newline
- **Packages** — `.deb`, `.rpm`, AUR (`PKGBUILD`)

---

## License

MIT — do whatever you want.

**Repo:** [github.com/MarkLevkovich/keepiss](https://github.com/MarkLevkovich/keepiss)
