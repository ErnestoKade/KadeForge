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

class ExceptionWrapper:
    def __init__(self, root):
        self.root = root
        self.root.title("Exception Wrapper - by ErnestoKade")
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

        # Type
        choice_frame = tk.Frame(left, bg="#1e1e1e")
        choice_frame.pack(pady=5)

        self.type_var = tk.StringVar(value="print")
        tk.Radiobutton(choice_frame, text="Print in console", variable=self.type_var, value="print",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_preview).pack(side="left", padx=8)
        tk.Radiobutton(choice_frame, text="MessageBox (Tkinter)", variable=self.type_var, value="messagebox",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_preview).pack(side="left", padx=8)

        # Function name
        name_frame = tk.Frame(left, bg="#1e1e1e")
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Function name:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10)).pack(side="left")
        self.func_name = tk.StringVar(value="run")
        tk.Entry(name_frame, textvariable=self.func_name, bg="#2d2d2d", fg="white",
                 insertbackground="white", width=20, relief="flat").pack(side="left", padx=8)
        self.func_name.trace_add("write", lambda *args: self.update_preview())

        # Preview
        preview_frame = tk.LabelFrame(left, text="  PREVIEW  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        preview_frame.pack(fill="x", pady=8)

        self.code_preview = tk.Text(preview_frame, height=6, font=("Consolas", 10),
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
        t = self.translations.get(self.current_lang, {}).get("exception_wrapper", {})

        if not t:
            t = {
                "title": "Exception Wrapper",
                "subtitle": "1. Choose type → 2. See preview → 3. Generate",
                "explanation": "This tool wraps a function with try/except to avoid crashes.\n\nTwo versions:\n• Print the error in the console\n• Show a MessageBox (for Tkinter apps)\n\nWhere to insert:\n1. Replace your function call with the wrapped version.\n2. Or wrap the whole function."
            }

        self.title_label.config(text=t.get("title", "Exception Wrapper"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def update_preview(self):
        name = self.func_name.get().strip() or "run"
        if self.type_var.get() == "print":
            code = f'''try:
    {name}()
except Exception as e:
    print(e)'''
        else:
            code = f'''try:
    {name}()
except Exception as e:
    messagebox.showerror("Error", str(e))'''

        self.code_preview.config(state="normal")
        self.code_preview.delete("1.0", tk.END)
        self.code_preview.insert("1.0", code)
        self.code_preview.config(state="disabled")

    def generate_code(self):
        name = self.func_name.get().strip() or "run"
        if self.type_var.get() == "print":
            code = f'''# ===== Exception Wrapper (Console) =====
try:
    {name}()
except Exception as e:
    print(e)
'''
        else:
            code = f'''# ===== Exception Wrapper (MessageBox) =====
from tkinter import messagebox

try:
    {name}()
except Exception as e:
    messagebox.showerror("Error", str(e))
'''

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExceptionWrapper(root)
    root.mainloop()