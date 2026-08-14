import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class IconAdder:
    def __init__(self, root):
        self.root = root
        self.root.title("Icon Adder - by ErnestoKade")
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

        # Options
        options_frame = tk.LabelFrame(left, text="  OPTIONS  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        options_frame.pack(fill="x", pady=(0, 8))

        # Icon path
        path_frame = tk.Frame(options_frame, bg="#1e1e1e")
        path_frame.pack(fill="x", padx=10, pady=8)
        tk.Label(path_frame, text="Icon path:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10)).pack(side="left")
        self.icon_path = tk.StringVar(value="assets/icon.ico")
        entry_icon = tk.Entry(path_frame, textvariable=self.icon_path, bg="#2d2d2d", fg="white",
                              insertbackground="white", width=30, relief="flat")
        entry_icon.pack(side="left", padx=8)

        # Type
        type_frame = tk.Frame(options_frame, bg="#1e1e1e")
        type_frame.pack(fill="x", padx=10, pady=4)
        self.type_var = tk.StringVar(value="tk")
        tk.Radiobutton(type_frame, text="Tkinter", variable=self.type_var, value="tk",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_preview).pack(side="left", padx=8)
        tk.Radiobutton(type_frame, text="CustomTkinter", variable=self.type_var, value="ctk",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_preview).pack(side="left", padx=8)

        # Preview
        preview_frame = tk.LabelFrame(left, text="  CODE PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        preview_frame.pack(fill="x", pady=8)

        self.code_preview = tk.Text(preview_frame, height=5, font=("Consolas", 10),
                                    bg="#2d2d2d", fg="#22c55e", relief="flat", wrap="word")
        self.code_preview.pack(fill="x", padx=8, pady=8)
        self.code_preview.config(state="disabled")

        # Button
        self.btn_generate = tk.Button(
            left, text="GENERATE CODE",
            command=self.generate_code,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_generate.pack(pady=6)

        # Final Code
        code_frame = tk.LabelFrame(left, text="  FINAL CODE  ", font=("Segoe UI", 10, "bold"),
                                   bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        code_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            code_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled"
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

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

        self.icon_path.trace_add("write", lambda *args: self.update_preview())
        self.change_language()
        self.update_preview()

    def load_translations(self):
        try:
            current = os.path.abspath(os.path.dirname(__file__))
           
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
        t = self.translations.get(self.current_lang, {}).get("icon_adder", {})

        if not t:
            t = {
                "title": "Icon Adder",
                "subtitle": "1. Choose type → 2. See code → 3. Generate",
                "explanation": "This tool adds an icon to your Tkinter or CustomTkinter window.\n\nWhat it does:\n• Adds the correct iconbitmap line\n• Works for both Tkinter and CustomTkinter\n• Also prepares the PyInstaller --icon argument\n\nWhere to insert:\n\nPut the generated code inside your __init__ method, just after creating the window.\n\nExample:\nself.iconbitmap(\"assets/icon.ico\")"
            }

        self.title_label.config(text=t.get("title", "Icon Adder"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def update_preview(self):
        path = self.icon_path.get().strip() or "assets/icon.ico"
        if self.type_var.get() == "tk":
            code = f'self.iconbitmap("{path}")'
        else:
            code = f'self.iconbitmap("{path}")  # also works with CustomTkinter'

        self.code_preview.config(state="normal")
        self.code_preview.delete("1.0", tk.END)
        self.code_preview.insert("1.0", code)
        self.code_preview.config(state="disabled")

    def generate_code(self):
        path = self.icon_path.get().strip() or "assets/icon.ico"
        
        if self.type_var.get() == "tk":
            code = f'''# ===== Add Icon (Tkinter) =====
# Put this inside your __init__ method

try:
    self.iconbitmap("{path}")
except:
    pass
'''
        else:
            code = f'''# ===== Add Icon (CustomTkinter) =====
# Put this inside your __init__ method

try:
    self.iconbitmap("{path}")
except:
    pass
'''

        # Also add PyInstaller tip
        code += f'''
# For PyInstaller, add this to your command:
# --icon="{path}"
'''

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = IconAdder(root)
    root.mainloop()