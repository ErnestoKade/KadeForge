import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ProgressBarAdder:
    def __init__(self, root):
        self.root = root
        self.root.title("Progress Bar Adder - by ErnestoKade")
        self.root.geometry("1000x740")
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

        # Choice
        choice_frame = tk.Frame(left, bg="#1e1e1e")
        choice_frame.pack(pady=5)

        self.bar_type = tk.StringVar(value="determinate")

        tk.Radiobutton(choice_frame, text="With percentage (%)", variable=self.bar_type,
                       value="determinate", bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                       font=("Segoe UI", 11), command=self.update_visual).pack(side="left", padx=12)

        tk.Radiobutton(choice_frame, text="Indeterminate (left ↔ right)", variable=self.bar_type,
                       value="indeterminate", bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                       font=("Segoe UI", 11), command=self.update_visual).pack(side="left", padx=12)

        # Visual
        visual_frame = tk.LabelFrame(left, text="  VISUAL PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        visual_frame.pack(fill="x", pady=8)

        self.preview_frame = tk.Frame(visual_frame, bg="#1e1e1e", height=90)
        self.preview_frame.pack(fill="x", padx=10, pady=10)
        self.preview_frame.pack_propagate(False)

        # Generate button
        self.btn_generate = tk.Button(left, text="GENERATE CODE", command=self.generate_code,
                                      font=("Segoe UI", 11, "bold"), bg="#3b82f6", fg="white",
                                      activebackground="#2563eb", relief="flat", cursor="hand2", height=1)
        self.btn_generate.pack(pady=6)

        # Code
        code_frame = tk.LabelFrame(left, text="  CODE  ", font=("Segoe UI", 10, "bold"),
                                   bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        code_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(code_frame, wrap=tk.NONE, font=("Consolas", 10),
                                                bg="#2d2d2d", fg="white", insertbackground="white",
                                                state="disabled")
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # RIGHT SIDE - Explanation with scroll
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
                                  bg="#1e1e1e", fg="white", justify="left", anchor="nw", wraplength=220)
        self.exp_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.change_language()
        self.update_visual()

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
        t = self.translations.get(self.current_lang, {}).get("progress_bar", {})

        self.title_label.config(text=t.get("title", "Progress Bar Adder"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))

    def update_visual(self):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        try:
            self.progress.stop()
        except:
            pass

        if self.bar_type.get() == "determinate":
            self.progress = ttk.Progressbar(self.preview_frame, orient="horizontal", length=400, mode="determinate")
            self.progress.pack(pady=5)
            self.percent_label = tk.Label(self.preview_frame, text="0%", bg="#1e1e1e", fg="white", font=("Segoe UI", 11))
            self.percent_label.pack()
            self.animate_determinate()
        else:
            self.progress = ttk.Progressbar(self.preview_frame, orient="horizontal", length=400, mode="indeterminate")
            self.progress.pack(pady=8)
            tk.Label(self.preview_frame, text="Loading...", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 11)).pack()
            self.progress.start(12)

    def animate_determinate(self):
        def run(i=0):
            if i > 100:
                return
            self.progress["value"] = i
            self.percent_label.config(text=f"{i}%")
            self.root.after(30, lambda: run(i + 2))
        run()

    def generate_code(self):
        if self.bar_type.get() == "determinate":
            code = '''# ===== Progress Bar with percentage =====
from tkinter import ttk

# Put this inside __init__
self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
self.progress.pack(pady=10)

self.percent_label = tk.Label(self, text="0%", bg="#1e1e1e", fg="white", font=("Segoe UI", 12))
self.percent_label.pack()

# Put this method at the same level as __init__
def update_progress(self, current, total):
    percent = int((current / total) * 100)
    self.progress["value"] = percent
    self.percent_label.config(text=f"{percent}%  ({current}/{total})")
    self.update_idletasks()
'''
        else:
            code = '''# ===== Indeterminate Progress Bar =====
from tkinter import ttk

# Put this inside __init__
self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="indeterminate")
self.progress.pack(pady=10)

# Put these methods at the same level as __init__
def start_loading(self):
    self.progress.start(10)

def stop_loading(self):
    self.progress.stop()
'''

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressBarAdder(root)
    root.mainloop()