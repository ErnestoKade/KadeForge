import tkinter as tk
from tkinter import scrolledtext, messagebox
import autopep8
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class IndentFixer:
    def __init__(self, root):
        self.root = root
        self.root.title("Indent Fixer - by ErnestoKade")
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

        # Bad indentation
        bad_frame = tk.LabelFrame(left, text="  BAD INDENTATION  ", font=("Segoe UI", 10, "bold"),
                                  bg="#1e1e1e", fg="#ef4444", bd=1, relief="solid")
        bad_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.input_text = scrolledtext.ScrolledText(
            bad_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white", height=9
        )
        self.input_text.pack(fill="both", expand=True, padx=6, pady=6)

        bad_example = '''def test():
 print("Hello")
  if True:
   print("Broken indentation")
    for i in range(3):
  print(i)
   else:
print("End")'''
        self.input_text.insert("1.0", bad_example)

        # Button
        self.btn_format = tk.Button(
            left, text="FORMAT INDENTATION",
            command=self.format_code,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_format.pack(pady=6)

        # Good indentation
        good_frame = tk.LabelFrame(left, text="  GOOD INDENTATION  ", font=("Segoe UI", 10, "bold"),
                                   bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        good_frame.pack(fill="both", expand=True)

        self.output_text = scrolledtext.ScrolledText(
            good_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white", height=9,
            state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, padx=6, pady=6)

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
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

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
        t = self.translations.get(self.current_lang, {}).get("indent_fixer", {})

        self.title_label.config(text=t.get("title", "Indent Fixer"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))

    def format_code(self):
        code = self.input_text.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Empty", "Please paste some code first!")
            return

        try:
            formatted = autopep8.fix_code(
                code,
                options={'aggressive': 2, 'indent_size': 4, 'max_line_length': 120}
            )
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", formatted)
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Could not format:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IndentFixer(root)
    root.mainloop()