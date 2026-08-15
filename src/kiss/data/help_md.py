HELP = """
# KISS — Help

A small terminal editor built on [Textual](https://github.com/Textualize/textual).
Report issues and star the repo at [github.com/levk-m/kiss](https://github.com/levk-m/kiss).

---

## Command Palette

Open with `Ctrl+P`.

- **Search** — fuzzy-match files and commands as you type.
- **Theme** — switch the application theme on the fly.
- **Help** — show this page.
- **Edit config** — open `~/.kiss_conf.json`.

---

## Configuration

KISS reads settings from `~/.kiss_conf.json` (JSON).

Open the config with `Ctrl+O` or from the command palette (`Edit config`).
Changes take effect after restarting KISS.

```json
{
    "kiss": {
        "theme": "tokyo-night",
        "editor-theme": "dracula",
        "show_line_numbers": true,
        "soft_wrap": true,
        "highlight_cursor_line": false,
        "start-screen": false
    }
}
```

| Option | Default | Description |
| -- | -- | -- |
| `theme` | `tokyo-night` | Application theme (see list below) |
| `editor-theme` | `dracula` | Syntax highlighting theme (see list below) |
| `show_line_numbers` | `true` | Show line numbers in the gutter |
| `soft_wrap` | `true` | Soft-wrap long lines |
| `highlight_cursor_line` | `false` | Highlight the line under the cursor |
| `start-screen` | `false` | Show the splash screen on startup |

### Available application themes

`textual-dark`, `textual-light`, `nord`, `gruvbox`, `catppuccin-mocha`,
`catppuccin-latte`, `catppuccin-frappe`, `catppuccin-macchiato`, `dracula`,
`tokyo-night`, `monokai`, `flexoki`, `solarized-light`, `solarized-dark`,
`rose-pine`, `rose-pine-moon`, `rose-pine-dawn`, `atom-one-dark`,
`atom-one-light`, `ansi-dark`, `ansi-light`

### Available editor themes

`css`, `monokai`, `dracula`, `vscode_dark`, `github_light`

`css` is the default editor theme. It has no fixed background — it adapts to
the current application theme's palette, so the editor blends with the app UI.

---

## Keybindings

### Navigation

| Key | Action |
| -- | -- |
| Cursor up / down / left / right | Move cursor |
| Home / Ctrl+A | Move to line start |
| End / Ctrl+E | Move to line end |
| PgUp / Ctrl+PgUp | Page up |
| PgDn / Ctrl+PgDn | Page down |
| Ctrl+Left / Ctrl+Right | Move by word |
| Alt+Left / Alt+Right | Move to word start / end |

### Selection

| Key | Action |
| -- | -- |
| Shift+Arrows | Select character / line |
| Shift+Home / Shift+End | Select to line start / end |
| Shift+PgUp / Shift+PgDn | Select page up / down |
| F6 | Select current line |
| F7 | Select all |

### Editing

| Key | Action |
| -- | -- |
| Backspace / Ctrl+Backspace | Delete character before cursor |
| Delete / Ctrl+D | Delete character under cursor |
| Alt+Del | Delete to start of word |
| Ctrl+Left / Ctrl+Right | Decrease / increase indent |
| Ctrl+U | Delete to line start |
| Ctrl+K | Delete to line end |
| Ctrl+X / Super+X | Cut |
| Ctrl+C / Super+C | Copy |
| Ctrl+V | Paste |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

### Interface

| Key | Action |
| -- | -- |
| Tab / Shift+Tab | Focus next / previous element |
| Ctrl+S | Save |
| Ctrl+P | Command palette |
| Ctrl+O | Open config |
| Ctrl+H | Help |
| Ctrl+Q | Quit |
"""
