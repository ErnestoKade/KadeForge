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

class UIModernizer:
    def __init__(self, root):
        self.root = root
        self.root.title("UI Modernizer - by ErnestoKade")
        self.root.geometry("1000x740")
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

        # Choices
        choice_frame = tk.Frame(left, bg="#1e1e1e")
        choice_frame.pack(pady=5)

        self.option = tk.StringVar(value="dark_mode")

        options = [
            ("Dark Mode", "dark_mode"),
            ("Modern Buttons", "modern_buttons"),
            ("Color Palette", "color_palette"),
            ("Title + Footer", "title_footer"),
            ("Clean Layout", "clean_layout"),
        ]

        for text, value in options:
            tk.Radiobutton(
                choice_frame, text=text, variable=self.option, value=value,
                bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                activebackground="#1e1e1e", activeforeground="white",
                font=("Segoe UI", 10), command=self.update_preview
            ).pack(side="left", padx=6)

        # Visual Preview
        visual_frame = tk.LabelFrame(left, text="  VISUAL PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        visual_frame.pack(fill="x", pady=8)

        self.preview_container = tk.Frame(visual_frame, bg="#1e1e1e", height=110)
        self.preview_container.pack(fill="x", padx=8, pady=8)
        self.preview_container.pack_propagate(False)

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

        # Code
        code_frame = tk.LabelFrame(left, text="  CODE  ", font=("Segoe UI", 10, "bold"),
                                   bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        code_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            code_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled"
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # RIGHT - Explanation with scroll
        right = tk.LabelFrame(main_container, text="  EXPLANATION  ", font=("Segoe UI", 10, "bold"),
                              bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid", width=260)
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
                                  bg="#1e1e1e", fg="white", justify="left", anchor="nw", wraplength=230)
        self.exp_label.pack(fill="both", expand=True, padx=10, pady=10)

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
        t = self.translations.get(self.current_lang, {}).get("ui_modernizer", {})
        self.title_label.config(text=t.get("title", "UI Modernizer"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def clear_preview(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()

    def update_preview(self):
        self.clear_preview()
        choice = self.option.get()

        if choice == "dark_mode":
            tk.Label(self.preview_container, text="Dark Mode Activated\nDark background + light text",
                     font=("Segoe UI", 12), bg="#1e1e1e", fg="white").pack(expand=True)
        elif choice == "modern_buttons":
            tk.Button(self.preview_container, text="Modern Button", font=("Segoe UI", 11, "bold"),
                      bg="#3b82f6", fg="white", relief="flat", padx=15, pady=6).pack(pady=6)
            tk.Button(self.preview_container, text="Success Button", font=("Segoe UI", 11, "bold"),
                      bg="#22c55e", fg="white", relief="flat", padx=15, pady=6).pack(pady=6)
        elif choice == "color_palette":
            colors = [("#1e1e1e", "bg"), ("#3b82f6", "button"), ("#22c55e", "success"),
                      ("#ef4444", "danger"), ("#f59e0b", "warning")]
            for color, name in colors:
                f = tk.Frame(self.preview_container, bg=color, width=70, height=40)
                f.pack(side="left", padx=5, pady=20)
                f.pack_propagate(False)
                tk.Label(f, text=name, bg=color, fg="white", font=("Segoe UI", 8)).pack(expand=True)
        elif choice == "title_footer":
            tk.Label(self.preview_container, text="App Title", font=("Segoe UI", 16, "bold"),
                     bg="#1e1e1e", fg="white").pack(pady=(10, 2))
            tk.Label(self.preview_container, text="Subtitle here", font=("Segoe UI", 10),
                     bg="#1e1e1e", fg="#aaaaaa").pack()
            tk.Label(self.preview_container, text="Developed by ErnestoKade", font=("Segoe UI", 9),
                     bg="#1e1e1e", fg="#777777").pack(side="bottom", pady=8)
        elif choice == "clean_layout":
            left = tk.Frame(self.preview_container, bg="#2d2d2d", width=140, height=80)
            left.pack(side="left", padx=15, pady=15)
            left.pack_propagate(False)
            tk.Label(left, text="Left\nColumn", bg="#2d2d2d", fg="white").pack(expand=True)
            right = tk.Frame(self.preview_container, bg="#2d2d2d", width=140, height=80)
            right.pack(side="left", padx=15, pady=15)
            right.pack_propagate(False)
            tk.Label(right, text="Right\nColumn", bg="#2d2d2d", fg="white").pack(expand=True)

    def generate_code(self):
        codes = {
            "dark_mode": '''# ===== Dark Mode =====
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
self.configure(fg_color="#1e1e1e")
''',
            "modern_buttons": '''# ===== Modern Buttons =====
btn = ctk.CTkButton(
    self,
    text="My Button",
    width=180,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="#3b82f6",
    hover_color="#2563eb"
)
btn.pack(pady=8)
''',
            "color_palette": '''# ===== Color Palette =====
COLORS = {
    "bg": "#1e1e1e",
    "frame": "#2d2d2d",
    "button": "#3b82f6",
    "button_hover": "#2563eb",
    "text": "#ffffff",
    "text_secondary": "#aaaaaa",
    "success": "#22c55e",
    "danger": "#ef4444",
    "warning": "#f59e0b"
}
''',
            "title_footer": '''# ===== Title + Footer =====
title = ctk.CTkLabel(self, text="App Title", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(self, text="Subtitle here", font=ctk.CTkFont(size=13), text_color="#aaaaaa")
subtitle.pack(pady=(0, 15))

footer = ctk.CTkLabel(self, text="Developed by ErnestoKade", font=ctk.CTkFont(size=11), text_color="#777777")
footer.pack(side="bottom", pady=10)
''',
            "clean_layout": '''# ===== Clean Layout =====
main_frame = ctk.CTkFrame(self, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

left_frame = ctk.CTkFrame(main_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
'''
        }

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", codes[self.option.get()])
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = UIModernizer(root)
    root.mainloop()