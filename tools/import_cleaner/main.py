import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import sys
import re

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ImportCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Import Cleaner - by ErnestoKade")
        self.root.geometry("1050x760")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_lang = "en"
        self.translations = self.load_translations()

        # === Language selector ===
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

        # === MAIN CONTAINER ===
        main_container = tk.Frame(root, bg="#1e1e1e")
        main_container.pack(fill="both", expand=True, padx=15, pady=5)

        # LEFT SIDE
        left = tk.Frame(main_container, bg="#1e1e1e")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Original code
        original_frame = tk.LabelFrame(left, text="  ORIGINAL CODE  ", font=("Segoe UI", 10, "bold"),
                                       bg="#1e1e1e", fg="#ef4444", bd=1, relief="solid")
        original_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.input_text = scrolledtext.ScrolledText(
            original_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white", height=12
        )
        self.input_text.pack(fill="both", expand=True, padx=6, pady=6)

        example = '''import os
import sys
import json
import tkinter as tk
from tkinter import messagebox
import unused_module
from pathlib import Path
import re

def hello():
    print("Hello")
    path = Path("test")
'''
        self.input_text.insert("1.0", example)

        # Button
        self.btn_clean = tk.Button(
            left, text="CLEAN & SORT IMPORTS",
            command=self.clean_imports,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_clean.pack(pady=6)

        # Cleaned code
        cleaned_frame = tk.LabelFrame(left, text="  CLEANED CODE  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        cleaned_frame.pack(fill="both", expand=True)

        self.output_text = scrolledtext.ScrolledText(
            cleaned_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, padx=6, pady=6)

        # RIGHT SIDE - Explanation
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

    def load_translations(self):
        try:
            current = os.path.abspath(os.path.dirname(__file__))
            # Remonte jusqu'à trouver le dossier "lang"
            for _ in range(6):
                candidate = os.path.join(current, "lang", "translations.json")
                if os.path.exists(candidate):
                    with open(candidate, "r", encoding="utf-8") as f:
                        return json.load(f)
                current = os.path.dirname(current)
            raise FileNotFoundError("translations.json not found")
        except Exception as e:
            print("Error loading translations:", e)
            return {"en": {}}

    def change_language(self):
        self.current_lang = self.lang_var.get()
        t = self.translations.get(self.current_lang, {}).get("import_cleaner", {})

        if not t:
            t = {
                "title": "Import Cleaner",
                "subtitle": "1. Paste code → 2. Clean → 3. Get sorted imports",
                "explanation": "This tool removes unused imports and sorts them cleanly.\n\nWhat it does:\n• Removes imports that are not used in the code\n• Sorts imports alphabetically\n• Keeps only what is necessary\n\nWhere to insert:\n\nSimply replace the import section at the top of your file with the cleaned version.\n\nTip: Always check the result, some dynamic imports may be removed."
            }

        self.title_label.config(text=t.get("title", "Import Cleaner"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def clean_imports(self):
        code = self.input_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Empty", "Please paste some code first!")
            return

        try:
            lines = code.splitlines()
            import_lines = []
            other_lines = []
            in_imports = True

            for line in lines:
                stripped = line.strip()
                if in_imports and (stripped.startswith("import ") or stripped.startswith("from ")):
                    import_lines.append(line)
                else:
                    if stripped and not stripped.startswith("#"):
                        in_imports = False
                    other_lines.append(line)

            used_names = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', "\n".join(other_lines)))

            cleaned_imports = []
            for line in import_lines:
                names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', line)
                if any(name in used_names for name in names if name not in ("import", "from", "as")):
                    cleaned_imports.append(line)

            cleaned_imports = sorted(set(cleaned_imports), key=lambda x: x.strip())

            result = "\n".join(cleaned_imports) + "\n\n" + "\n".join(other_lines)

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result.strip())
            self.output_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Could not clean imports:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImportCleaner(root)
    root.mainloop()