"""Clipboard monitor - watches system clipboard for changes."""

import threading
import time
import pyperclip


class ClipboardMonitor:
    """Monitors clipboard content changes in a background thread."""

    def __init__(self, on_change=None, interval=0.5):
        self._interval = interval
        self._running = False
        self._last_content = ""
        self._on_change = on_change
        self._thread = None

    def start(self):
        """Start background monitoring."""
        if self._running:
            return
        self._running = True
        self._last_content = pyperclip.paste() or ""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop monitoring."""
        self._running = False

    def _run(self):
        while self._running:
            try:
                current = pyperclip.paste() or ""
            except Exception:
                current = ""
            if current and current != self._last_content:
                self._last_content = current
                if self._on_change:
                    self._on_change(current)
            time.sleep(self._interval)
