<p align="center">
  <img src="examples/kiss-prev.png" alt="KISS editor preview" width="900">
</p>

<p align="center">
  <strong>KISS</strong> — <em>keep it simple, stupid.</em>
</p>

A small terminal editor built with [Textual](https://github.com/Textualize/textual).
It opens files and folders, with syntax highlighting, a file tree and undo/redo.
Just an editor — no LSP, no plugins, no ambitions to become an IDE.

---

## About & status

KISS is early-stage software. It's not a replacement for nano or vim — just a
small editor that tries to stay simple and useful. It's for learning, and for the moments where a tiny no-nonsense
editor is enough. Some things are still
missing (see [TODO](#todo)).

[![codecov](https://codecov.io/gh/levk-m/kiss/graph/badge.svg?token=01WH0NHU9Q)](https://codecov.io/gh/levk-m/kiss)
[![Tests](https://img.shields.io/github/actions/workflow/status/levk-m/kiss/test.yml?branch=main&label=tests)](https://github.com/levk-m/kiss/actions)

---

## Install

for unix systems:

```bash
curl -fsSL https://raw.githubusercontent.com/levk-m/kiss/main/install.sh | bash
```

via package managers:

```bash
[uv tool / pipx] install kiss-editor
```

or from source (requires Python 3.12+ and [uv](https://docs.astral.sh/uv/)):

```bash
git clone https://github.com/levk-m/kiss.git
cd kiss
uv sync
uv run kiss
```

Or run directly without cloning:

```bash
uvx kiss-editor
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

The usual editor essentials are here — undo/redo, clipboard, line numbers,
word wrap, cursor line highlight. On top of that KISS adds:

- **File tree** — browse and open files with custom icons per file type
- **Syntax highlighting** — auto-detected from the file
- **Command palette** (`Ctrl+P`) — fuzzy-find files, switch themes
- **Image viewer** — open images directly in the terminal (requires Kitty, Sixel or iTerm support)
- **Config** — `~/.kiss_conf.json`, open with `Ctrl+O`
- **Help dialog** — `Ctrl+H`
- **Splash screen** — ASCII logo on startup
- **Update check** — notifies when a newer version is available on exit
- **Enter handling** — auto-indent to match the current line on newline

---

## Keybindings

### Navigation

| Key                        | Action            |
| -------------------------- | ----------------- |
| Arrows                     | Move cursor       |
| `Home` / `Ctrl+A`          | Go to line start  |
| `End` / `Ctrl+E`           | Go to line end    |
| `PgUp` / `Ctrl+PgUp`       | Page up           |
| `PgDn` / `Ctrl+PgDn`       | Page down         |
| `Ctrl+Left` / `Ctrl+Right` | Page left / right |
| `Alt+Left`                 | Word start        |
| `Alt+Right`                | Word end          |

### Selection

| Key                         | Action                  |
| --------------------------- | ----------------------- |
| `Shift`+Arrows              | Select character / line |
| `Shift+Home`                | Select to line start    |
| `Shift+End`                 | Select to line end      |
| `Shift+PgUp` / `Shift+PgDn` | Select page up / down   |
| `F6`                        | Select current line     |
| `F7`                        | Select all              |

### Editing

| Key                            | Action                     |
| ------------------------------ | -------------------------- |
| `Backspace` / `Ctrl+Backspace` | Delete char before cursor  |
| `Delete` / `Ctrl+D`            | Delete char under cursor   |
| `Alt+Del`                      | Delete to start of word    |
| `Ctrl+U`                       | Delete to line start       |
| `Ctrl+K`                       | Delete to line end         |
| `Ctrl+Left` / `Ctrl+Right`     | Decrease / increase indent |
| `Ctrl+X` / `Super+X`           | Cut                        |
| `Ctrl+C` / `Super+C`           | Copy                       |
| `Ctrl+V`                       | Paste                      |
| `Ctrl+Z`                       | Undo                       |
| `Ctrl+Y`                       | Redo                       |

### Interface

| Key                 | Action                            |
| ------------------- | --------------------------------- |
| `Tab` / `Shift+Tab` | Focus next / previous element     |
| `Ctrl+S`            | Save                              |
| `Ctrl+P`            | Command palette (files, themes)   |
| `Ctrl+H`            | Help dialog                       |
| `Ctrl+O`            | Open config (`~/.kiss_conf.json`) |
| `Ctrl+Q`            | Quit                              |

---

## Configuration

JSON config file at `~/.kiss_conf.json`. Open it with `Ctrl+O` — changes take effect after restart.
A copyable example lives at `examples/kiss_conf.json`.

```json
{
    "kiss": {
        "theme": "tokyo-night",
        "editor-theme": "dracula",
        "show_line_numbers": true,
        "soft_wrap": true,
        "highlight_cursor_line": false,
        "start-screen": false,
        "indent-size": 4
    }
}
```

| Key                          | Default         | Description                   |
| ---------------------------- | --------------- | ----------------------------- |
| `kiss.theme`                 | `"tokyo-night"` | Application theme             |
| `kiss.editor-theme`          | `"css"`         | Syntax highlighting colors    |
| `kiss.show_line_numbers`     | `true`          | Show line numbers             |
| `kiss.soft_wrap`             | `true`          | Soft-wrap long lines          |
| `kiss.highlight_cursor_line` | `false`         | Highlight current line        |
| `kiss.start-screen`          | `false`         | Show splash screen on startup |
| `kiss.indent-size`           | `4`             | Auto-indent width; `0` disables |

### Application themes

`textual-dark`, `textual-light`, `nord`, `gruvbox`, `catppuccin-mocha`,
`catppuccin-latte`, `catppuccin-frappe`, `catppuccin-macchiato`, `dracula`,
`tokyo-night`, `monokai`, `flexoki`, `solarized-light`, `solarized-dark`,
`rose-pine`, `rose-pine-moon`, `rose-pine-dawn`, `atom-one-dark`,
`atom-one-light`, `ansi-dark`, `ansi-light`

### Editor themes

`css`, `monokai`, `dracula`, `vscode_dark`, `github_light`

`css` is the default editor theme. It has no fixed background — it adapts to
the current application theme's palette, so the editor blends with the app UI.

---

## TODO

- **Custom command palette** — replace the default Textual palette with a bespoke one
- **Search within file** — `Ctrl+F` (maybe)
- **Markdown viewer** — two modes: render and edit

---

## License

MIT License.

**Repo:** [github.com/levk-m/kiss](https://github.com/levk-m/kiss)
