# SmartClip - AI-Powered Clipboard Manager

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

A lightweight, local-first clipboard manager with AI superpowers. SmartClip monitors your clipboard, stores history, and lets you process copied text with a local LLM — all on your own machine.

## Features

- **Clipboard Monitoring** — Automatically captures everything you copy (Ctrl+C)
- **Searchable History** — Full-text search across all past clipboard entries
- **Pin Important Items** — Keep frequently used snippets pinned at the top
- **Dark Theme GUI** — Clean, modern interface built with tkinter
- **AI Processing** (via Ollama):
  - Translate text to any language
  - Summarize long passages
  - Explain code snippets in plain English
  - Format/beautify code
- **Local & Private** — All data stays on your machine. No cloud, no tracking.

## Quick Start

### Prerequisites

- Python 3.9 or higher
- (Optional) [Ollama](https://ollama.com) for AI features

### Installation

```bash
git clone https://github.com/ZJJ50777-UI/SmartClip.git
cd SmartClip
pip install -r requirements.txt
```

### Run

```bash
python -m smartclip
```

### Enable AI Features (Optional)

If you have a powerful GPU (like RTX 4080), install Ollama and pull a model:

```bash
# Install Ollama from https://ollama.com
ollama pull qwen2.5:3b
```

Then SmartClip's AI buttons (Translate, Summarize, Explain Code) will work using your local GPU.

## Usage

| Action | How |
|--------|-----|
| Capture | Just copy anything (Ctrl+C) — SmartClip records it |
| Search | Type in the search bar to filter history |
| Preview | Right-click any entry |
| Copy back | Double-click or select + click "Copy" |
| Pin | Select + "Pin" to keep at top |
| AI Translate | Select entry → "Translate" (needs Ollama) |
| AI Summarize | Select entry → "Summarize" (needs Ollama) |
| Delete | Select + "Delete" |

## Tech Stack

- **GUI**: tkinter (built-in, zero extra dependencies for UI)
- **Clipboard**: pyperclip
- **Storage**: SQLite
- **AI Backend**: Ollama (local LLM, optional)

## Project Structure

```
SmartClip/
├── smartclip/
│   ├── __init__.py          # Package metadata
│   ├── __main__.py          # Entry point
│   ├── app.py               # Main GUI application
│   ├── clipboard_monitor.py # Background clipboard watcher
│   ├── history.py           # SQLite storage layer
│   └── ai_processor.py      # Ollama integration
├── requirements.txt
├── setup.py
└── README.md
```

## Why SmartClip?

- **Local-first**: No data leaves your computer
- **GPU-accelerated AI**: Leverages your RTX 4080 for instant AI processing
- **Simple & fast**: Minimal dependencies, starts instantly
- **Open source**: MIT licensed, do whatever you want

## Roadmap

- [ ] System tray integration
- [ ] Image clipboard support
- [ ] Global hotkeys (Ctrl+Shift+V)
- [ ] Export/import history
- [ ] Plugin system for custom AI actions

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Made with ❤️ by [ZJJ50777](https://github.com/ZJJ50777-UI)**
