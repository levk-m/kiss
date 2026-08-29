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
- **Go to line** (`Ctrl+G`) — enter a number, jump straight there
- **Command palette** (`Ctrl+P`) — fuzzy-find files, switch themes
- **Image viewer** — open images directly in the terminal (requires Kitty, Sixel or iTerm support)
- **Config** — `~/.kiss_conf.json`, open with `Ctrl+O`
- **Help dialog** — `Ctrl+H`
- **Splash screen** — ASCII logo on startup
- **Update check** — notifies when a newer version is available on exit
- **Enter handling** — auto-indent to match the current line on newline

---

### For keybindings and commands, see **[USAGE.md](USAGE.md)**.
