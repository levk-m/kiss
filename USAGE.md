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
| `Ctrl+G`                   | Go to line        |

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
        "indent-size": 4,
        "auto-close-pairs": true,
        "auto-update-check": true
    }
}
```

| Key                          | Default         | Description                                 |
| ---------------------------- | --------------- | ------------------------------------------- |
| `kiss.theme`                 | `"tokyo-night"` | Application theme                           |
| `kiss.editor-theme`          | `"css"`         | Syntax highlighting colors                  |
| `kiss.show_line_numbers`     | `true`          | Show line numbers                           |
| `kiss.soft_wrap`             | `true`          | Soft-wrap long lines                        |
| `kiss.highlight_cursor_line` | `false`         | Highlight current line                      |
| `kiss.start-screen`          | `false`         | Show splash screen on startup               |
| `kiss.indent-size`           | `4`             | Auto-indent width; `0` disables             |
| `auto-close-pairs`           | `true`          | Auto-close `({[` and `'"`                   |
| `auto-update-check`          | `true`          | Checking for updates after exiting the Kiss |

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
