"""Entry point: python -m smartclip"""

from smartclip.app import SmartClipApp
import tkinter as tk


def main():
    root = tk.Tk()
    app = SmartClipApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
