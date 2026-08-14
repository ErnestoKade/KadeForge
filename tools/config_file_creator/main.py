import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ConfigFileCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Config File Creator - by ErnestoKade")
        self.root.geometry("1050x760")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_lang = "en"
        self.translations = self.load_translations()

        # Language selector
        lang_frame = tk.Frame(root, bg="#1e1e1e")
        lang_frame.pack(anchor="ne", padx=15, pady=5)

        tk.Label(lang_frame, text="Lang:", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 9)).pack(side="left")

        self.lang_var = tk.StringVar(value="en")
        for code, name in [("en", "EN"), ("fr", "FR"), ("es", "ES"), ("de", "DE"), ("it", "IT"), ("pt", "PT")]:
            tk.Radiobutton(
                lang_frame, text=name, variable=self.lang_var, value=code,
                bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                font=("Segoe UI", 9), command=self.change_language
            ).pack(side="left", padx=2)

        # Title
        self.title_label = tk.Label(root, text="", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="white")
        self.title_label.pack(pady=(5, 2))

        self.subtitle_label = tk.Label(root, text="", font=("Segoe UI", 10), bg="#1e1e1e", fg="#aaaaaa")
        self.subtitle_label.pack(pady=(0, 10))

        # Main container
        main_container = tk.Frame(root, bg="#1e1e1e")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)

        # LEFT
        left = tk.Frame(main_container, bg="#1e1e1e")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Preview
        preview_frame = tk.LabelFrame(left, text="  PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        preview_frame.pack(fill="x", pady=8)

        self.code_preview = tk.Text(preview_frame, height=8, font=("Consolas", 10),
                                    bg="#2d2d2d", fg="#22c55e", relief="flat", wrap="word")
        self.code_preview.pack(fill="x", padx=8, pady=8)
        self.code_preview.config(state="disabled")

        # Generate
        self.btn_generate = tk.Button(
            left, text="GENERATE CODE",
            command=self.generate_code,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_generate.pack(pady=6)

        # Output
        code_frame = tk.LabelFrame(left, text="  FINAL CODE  ", font=("Segoe UI", 10, "bold"),
                                   bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        code_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            code_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled"
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # RIGHT
        right = tk.LabelFrame(main_container, text="  EXPLANATION  ", font=("Segoe UI", 10, "bold"),
                              bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid", width=270)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)

        self.exp_canvas = tk.Canvas(right, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(right, orient="vertical", command=self.exp_canvas.yview)
        self.exp_frame = tk.Frame(self.exp_canvas, bg="#1e1e1e")

        self.exp_frame.bind("<Configure>", lambda e: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))
        self.exp_canvas.create_window((0, 0), window=self.exp_frame, anchor="nw")
        self.exp_canvas.configure(yscrollcommand=scrollbar.set)

        self.exp_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.exp_label = tk.Label(self.exp_frame, text="", font=("Segoe UI", 10),
                                  bg="#1e1e1e", fg="white", justify="left", anchor="nw", wraplength=240)
        self.exp_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.change_language()
        self.update_preview()

    def load_translations(self):
        try:
            tool_dir = os.path.dirname(os.path.abspath(__file__))
            toolbox_dir = os.path.dirname(os.path.dirname(tool_dir))
            path = os.path.join(toolbox_dir, "lang", "translations.json")
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading translations:", e)
            return {"en": {}}

    def change_language(self):
        self.current_lang = self.lang_var.get()
        t = self.translations.get(self.current_lang, {}).get("config_file_creator", {})

        if not t:
            t = {
                "title": "Config File Creator",
                "subtitle": "1. Generate → 2. Copy → 3. Use in your project",
                "explanation": "This tool creates a clean config.json system.\n\nIt generates:\n• config.json example\n• load_config() function\n• save_config() function\n\nWhere to insert:\n1. Create a config.json file in your project.\n2. Put the two functions in your code."
            }

        self.title_label.config(text=t.get("title", "Config File Creator"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def update_preview(self):
        preview = '''{
  "theme": "dark",
  "language": "en",
  "window_size": "800x600"
}'''
        self.code_preview.config(state="normal")
        self.code_preview.delete("1.0", tk.END)
        self.code_preview.insert("1.0", preview)
        self.code_preview.config(state="disabled")

    def generate_code(self):
        code = '''# ===== Config File System =====

import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        # Default config
        default = {
            "theme": "dark",
            "language": "en",
            "window_size": "800x600"
        }
        save_config(default)
        return default
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Example of use:
# config = load_config()
# print(config["theme"])
# config["theme"] = "light"
# save_config(config)
'''

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigFileCreator(root)
    root.mainloop()