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

class InterfaceTemplates:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Templates - by ErnestoKade")
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

        self.option = tk.StringVar(value="basic")

        options = [
            ("Basic", "basic"),
            ("Two Columns", "two_columns"),
            ("List + Actions", "list_actions"),
            ("Form", "form"),
        ]

        for text, value in options:
            tk.Radiobutton(
                choice_frame, text=text, variable=self.option, value=value,
                bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                activebackground="#1e1e1e", activeforeground="white",
                font=("Segoe UI", 10), command=self.update_preview
            ).pack(side="left", padx=10)

        # Visual Preview
        visual_frame = tk.LabelFrame(left, text="  VISUAL PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        visual_frame.pack(fill="x", pady=8)

        self.preview_container = tk.Frame(visual_frame, bg="#1e1e1e", height=120)
        self.preview_container.pack(fill="x", padx=8, pady=8)
        self.preview_container.pack_propagate(False)

        # Button
        self.btn_generate = tk.Button(
            left, text="GENERATE FULL CODE",
            command=self.generate_code,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_generate.pack(pady=6)

        # Code
        code_frame = tk.LabelFrame(left, text="  FULL CODE  ", font=("Segoe UI", 10, "bold"),
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
        t = self.translations.get(self.current_lang, {}).get("interface_templates", {})
        self.title_label.config(text=t.get("title", "Interface Templates"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def clear_preview(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()

    def update_preview(self):
        self.clear_preview()
        choice = self.option.get()

        if choice == "basic":
            tk.Label(self.preview_container, text="App Title", font=("Segoe UI", 14, "bold"),
                     bg="#1e1e1e", fg="white").pack(pady=(8, 6))
            btn_frame = tk.Frame(self.preview_container, bg="#1e1e1e")
            btn_frame.pack()
            tk.Button(btn_frame, text="Action 1", bg="#3b82f6", fg="white", relief="flat", padx=10).pack(side="left", padx=4)
            tk.Button(btn_frame, text="Action 2", bg="#3b82f6", fg="white", relief="flat", padx=10).pack(side="left", padx=4)
            tk.Label(self.preview_container, text="Ready", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 9)).pack(side="bottom", pady=6)

        elif choice == "two_columns":
            left = tk.Frame(self.preview_container, bg="#2d2d2d", width=130, height=80)
            left.pack(side="left", padx=15, pady=15)
            left.pack_propagate(False)
            tk.Label(left, text="Left\nColumn", bg="#2d2d2d", fg="white").pack(expand=True)

            right = tk.Frame(self.preview_container, bg="#2d2d2d", width=130, height=80)
            right.pack(side="left", padx=15, pady=15)
            right.pack_propagate(False)
            tk.Label(right, text="Right\nColumn", bg="#2d2d2d", fg="white").pack(expand=True)

        elif choice == "list_actions":
            actions = tk.Frame(self.preview_container, bg="#1e1e1e")
            actions.pack(pady=6)
            tk.Button(actions, text="Add", bg="#3b82f6", fg="white", relief="flat", padx=8).pack(side="left", padx=3)
            tk.Button(actions, text="Delete", bg="#ef4444", fg="white", relief="flat", padx=8).pack(side="left", padx=3)
            tk.Button(actions, text="Refresh", bg="#22c55e", fg="white", relief="flat", padx=8).pack(side="left", padx=3)

            list_frame = tk.Frame(self.preview_container, bg="#2d2d2d", height=60)
            list_frame.pack(fill="x", padx=30, pady=4)
            list_frame.pack_propagate(False)
            tk.Label(list_frame, text="• Item 1\n• Item 2\n• Item 3", bg="#2d2d2d", fg="white",
                     font=("Segoe UI", 9), justify="left").pack(pady=5, padx=10, anchor="w")

        elif choice == "form":
            form = tk.Frame(self.preview_container, bg="#1e1e1e")
            form.pack(pady=6)

            tk.Label(form, text="Name:", bg="#1e1e1e", fg="white", font=("Segoe UI", 9)).pack(anchor="w")
            tk.Entry(form, width=25, bg="#2d2d2d", fg="white", relief="flat").pack(pady=(0, 2))

            tk.Label(form, text="Email:", bg="#1e1e1e", fg="white", font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))
            tk.Entry(form, width=25, bg="#2d2d2d", fg="white", relief="flat").pack(pady=(0, 2))

            tk.Button(form, text="Submit", bg="#3b82f6", fg="white", relief="flat", padx=12).pack(pady=6)

    def generate_code(self):
        codes = {
            "basic": '''# ===== Basic Template =====
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")

        title = ctk.CTkLabel(self, text="App Title", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(25, 20))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Action 1", width=160, height=38).pack(pady=6)
        ctk.CTkButton(btn_frame, text="Action 2", width=160, height=38).pack(pady=6)

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w", text_color="#aaaaaa")
        self.status.pack(side="bottom", fill="x", padx=20, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
''',
            "two_columns": '''# ===== Two Columns Template =====
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(left, text="Left Column", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        right = ctk.CTkFrame(main_frame)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Right Column", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

if __name__ == "__main__":
    app = App()
    app.mainloop()
''',
            "list_actions": '''# ===== List + Actions Template =====
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        title = ctk.CTkLabel(self, text="List + Actions", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(pady=20)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(pady=10)

        ctk.CTkButton(actions, text="Add", width=100).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Delete", width=100).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Refresh", width=100).pack(side="left", padx=5)

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="#2d2d2d")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=15)

if __name__ == "__main__":
    app = App()
    app.mainloop()
''',
            "form": '''# ===== Form Template =====
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Form")
        self.geometry("480x420")
        ctk.set_appearance_mode("dark")

        title = ctk.CTkLabel(self, text="Form", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(pady=25)

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        ctk.CTkLabel(form, text="Name:").pack(anchor="w", pady=(8, 0))
        self.entry_name = ctk.CTkEntry(form, width=280, height=34)
        self.entry_name.pack(pady=4)

        ctk.CTkLabel(form, text="Email:").pack(anchor="w", pady=(8, 0))
        self.entry_email = ctk.CTkEntry(form, width=280, height=34)
        self.entry_email.pack(pady=4)

        ctk.CTkButton(form, text="Submit", width=280, height=38).pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
'''
        }

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", codes[self.option.get()])
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceTemplates(root)
    root.mainloop()