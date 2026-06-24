"""SmartClip main application GUI."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import pyperclip

from smartclip.clipboard_monitor import ClipboardMonitor
from smartclip import history
from smartclip import ai_processor

THEME = {
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "accent": "#89b4fa",
    "entry_bg": "#313244",
    "entry_fg": "#cdd6f4",
    "btn_bg": "#45475a",
    "btn_fg": "#cdd6f4",
    "btn_active": "#585b70",
}


class SmartClipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartClip - AI Clipboard Manager")
        self.root.geometry("700x550")
        self.root.configure(bg=THEME["bg"])
        self.root.minsize(500, 400)

        self.monitor = ClipboardMonitor(on_change=self._on_clipboard_change)
        self._build_ui()
        self._refresh_list()
        self.monitor.start()

    def _build_ui(self):
        # Search bar
        search_frame = tk.Frame(self.root, bg=THEME["bg"])
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(
            search_frame, text="Search:", bg=THEME["bg"], fg=THEME["fg"]
        ).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._refresh_list())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["fg"],
            relief=tk.FLAT,
            font=("Segoe UI", 11),
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # History list
        list_frame = tk.Frame(self.root, bg=THEME["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("content", "time")
        self.tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=12
        )
        self.tree.heading("content", text="Content")
        self.tree.heading("time", text="Time")
        self.tree.column("content", width=400, minwidth=200)
        self.tree.column("time", width=150, minwidth=100)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=THEME["entry_bg"],
            foreground=THEME["entry_fg"],
            fieldbackground=THEME["entry_bg"],
            rowheight=26,
        )
        style.configure(
            "Treeview.Heading",
            background=THEME["btn_bg"],
            foreground=THEME["fg"],
        )
        style.map(
            "Treeview",
            background=[("selected", THEME["accent"])],
            foreground=[("selected", THEME["bg"])],
        )

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._on_right_click)

        # Preview
        self.preview = scrolledtext.ScrolledText(
            self.root,
            height=5,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["fg"],
            font=("Consolas", 10),
            relief=tk.FLAT,
            wrap=tk.WORD,
        )
        self.preview.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Buttons
        btn_frame = tk.Frame(self.root, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        buttons = [
            ("Copy", self._copy_selected),
            ("Delete", self._delete_selected),
            ("Pin", self._pin_selected),
            ("Clear All", self._clear_all),
        ]
        for text, cmd in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=THEME["btn_bg"],
                fg=THEME["btn_fg"],
                activebackground=THEME["btn_active"],
                activeforeground=THEME["fg"],
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                padx=12,
            )
            btn.pack(side=tk.LEFT, padx=(0, 5))

        # AI actions
        tk.Label(
            btn_frame,
            text=" |  AI:",
            bg=THEME["bg"],
            fg=THEME["accent"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT, padx=(15, 5))

        ai_buttons = [
            ("Translate", self._ai_translate),
            ("Summarize", self._ai_summarize),
            ("Explain Code", self._ai_explain),
        ]
        for text, cmd in ai_buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg="#2a2a40",
                fg=THEME["accent"],
                activebackground="#3a3a55",
                activeforeground=THEME["accent"],
                relief=tk.FLAT,
                font=("Segoe UI", 10),
                padx=10,
            )
            btn.pack(side=tk.LEFT, padx=(0, 4))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=THEME["bg"],
            fg="#6c7086",
            font=("Segoe UI", 9),
            anchor=tk.W,
        )
        status.pack(fill=tk.X, padx=10, pady=(0, 5))

    # ---------- Callbacks ----------

    def _on_clipboard_change(self, content):
        history.add_entry(content)
        self.root.after(0, self._refresh_list)

    def _refresh_list(self):
        query = self.search_var.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if query:
            rows = history.search_entries(query)
        else:
            rows = history.get_recent()
        import datetime

        for row in rows:
            entry_id, content, _, ts, pinned = row
            text = content[:80].replace("\n", " ")
            if pinned:
                text = "[PIN] " + text
            time_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            self.tree.insert("", tk.END, values=(text, time_str), iid=entry_id)
        count = history.get_count()
        self.status_var.set(f"Total entries: {count}")

    def _get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(sel[0])

    def _get_selected_content(self):
        entry_id = self._get_selected_id()
        if entry_id is None:
            return None
        rows = history.get_recent(999)
        for row in rows:
            if row[0] == entry_id:
                return row[1]
        return None

    def _on_double_click(self, event):
        content = self._get_selected_content()
        if content:
            pyperclip.copy(content)
            self.status_var.set("Copied to clipboard")

    def _on_right_click(self, event):
        content = self._get_selected_content()
        if content:
            self.preview.delete("1.0", tk.END)
            self.preview.insert("1.0", content[:2000])
            self.status_var.set("Preview loaded")

    def _copy_selected(self):
        content = self._get_selected_content()
        if content:
            pyperclip.copy(content)
            self.status_var.set("Copied!")

    def _delete_selected(self):
        entry_id = self._get_selected_id()
        if entry_id:
            history.delete_entry(entry_id)
            self._refresh_list()
            self.status_var.set("Deleted")

    def _pin_selected(self):
        entry_id = self._get_selected_id()
        if entry_id:
            history.pin_entry(entry_id)
            self._refresh_list()
            self.status_var.set("Toggled pin")

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Delete all clipboard history?"):
            history.clear_all()
            self._refresh_list()
            self.status_var.set("All cleared")

    def _run_ai(self, fn, label):
        content = self._get_selected_content()
        if not content:
            self.status_var.set("No entry selected")
            return
        self.status_var.set(f"AI: {label}...")
        threading.Thread(
            target=self._ai_worker, args=(fn, content, label), daemon=True
        ).start()

    def _ai_worker(self, fn, content, label):
        result = fn(content)
        self.root.after(0, lambda: self._show_ai_result(result, label))

    def _show_ai_result(self, result, label):
        if result:
            pyperclip.copy(result)
            self.preview.delete("1.0", tk.END)
            self.preview.insert("1.0", result)
            self.status_var.set(f"{label} done - copied to clipboard")
        else:
            self.status_var.set(
                f"{label} failed - is Ollama running? (ollama serve)"
            )

    def _ai_translate(self):
        self._run_ai(ai_processor.translate_text, "Translate")

    def _ai_summarize(self):
        self._run_ai(ai_processor.summarize_text, "Summarize")

    def _ai_explain(self):
        self._run_ai(ai_processor.explain_code, "Explain")
