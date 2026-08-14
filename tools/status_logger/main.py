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

class StatusLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Status / Logs Adder - by ErnestoKade")
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

        self.option = tk.StringVar(value="simple_status")

        options = [
            ("Simple Status Bar", "simple_status"),
            ("Live Logs Zone", "live_logs"),
            ("Status + Counter", "status_with_counter"),
        ]

        for text, value in options:
            tk.Radiobutton(
                choice_frame, text=text, variable=self.option, value=value,
                bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                activebackground="#1e1e1e", activeforeground="white",
                font=("Segoe UI", 10), command=self.update_preview
            ).pack(side="left", padx=8)

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
        t = self.translations.get(self.current_lang, {}).get("status_logger", {})
        self.title_label.config(text=t.get("title", "Status / Logs Adder"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def clear_preview(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()

    def update_preview(self):
        self.clear_preview()
        choice = self.option.get()

        if choice == "simple_status":
            fake = tk.Frame(self.preview_container, bg="#2d2d2d", height=90)
            fake.pack(fill="x", padx=30, pady=10)
            fake.pack_propagate(False)
            tk.Label(fake, text="Application content...", bg="#2d2d2d", fg="#aaaaaa", font=("Segoe UI", 10)).pack(expand=True)
            tk.Label(fake, text="Ready", anchor="w", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 10)).pack(side="bottom", fill="x", padx=5, pady=4)

        elif choice == "live_logs":
            log = tk.Text(self.preview_container, height=5, font=("Consolas", 10), bg="#2d2d2d", fg="white", relief="flat")
            log.pack(fill="x", padx=20, pady=10)
            log.insert("end", "Starting analysis...\n")
            log.insert("end", "42 files found\n")
            log.insert("end", "Processing...\n")
            log.insert("end", "Completed successfully ✓\n")
            log.config(state="disabled")

        elif choice == "status_with_counter":
            fake = tk.Frame(self.preview_container, bg="#2d2d2d", height=90)
            fake.pack(fill="x", padx=30, pady=10)
            fake.pack_propagate(False)
            tk.Label(fake, text="Analyzing files...", bg="#2d2d2d", fg="#aaaaaa", font=("Segoe UI", 10)).pack(expand=True)
            tk.Label(fake, text="In progress... | Files: 57", anchor="w", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 10)).pack(side="bottom", fill="x", padx=5, pady=4)

    def generate_code(self):
        codes = {
            "simple_status": '''# ===== Simple Status Bar =====
# Put this inside __init__
self.status = ctk.CTkLabel(
    self,
    text="Ready",
    anchor="w",
    font=ctk.CTkFont(size=13),
    text_color="#aaaaaa"
)
self.status.pack(side="bottom", fill="x", padx=20, pady=8)

# Put this method at the same level as __init__
def update_status(self, text):
    self.status.configure(text=text)
    self.update_idletasks()
''',
            "live_logs": '''# ===== Live Logs Zone =====
# Put this inside __init__
self.log_box = ctk.CTkTextbox(
    self,
    height=150,
    font=ctk.CTkFont(size=13),
    fg_color="#2d2d2d",
    text_color="white"
)
self.log_box.pack(fill="x", padx=20, pady=10)

# Put this method at the same level as __init__
def log(self, message):
    self.log_box.insert("end", message + "\\n")
    self.log_box.see("end")
    self.update_idletasks()
''',
            "status_with_counter": '''# ===== Status + Counter =====
# Put this inside __init__
self.status = ctk.CTkLabel(
    self,
    text="Ready | Files: 0",
    anchor="w",
    font=ctk.CTkFont(size=13),
    text_color="#aaaaaa"
)
self.status.pack(side="bottom", fill="x", padx=20, pady=8)

# Put this method at the same level as __init__
def update_status(self, text, count=None):
    if count is not None:
        self.status.configure(text=f"{text} | Files: {count}")
    else:
        self.status.configure(text=text)
    self.update_idletasks()
'''
        }

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", codes[self.option.get()])
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = StatusLogger(root)
    root.mainloop()