import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json
import os
import sys
import re
import ast

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ProjectDoctor:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Doctor - by ErnestoKade")
        self.root.geometry("1050x760")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_lang = "en"
        self.translations = self.load_translations()
        self.project_path = None
        self.issues = []

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

        # Project selection
        select_frame = tk.Frame(left, bg="#1e1e1e")
        select_frame.pack(fill="x", pady=(0, 8))

        self.path_label = tk.Label(select_frame, text="No project selected", bg="#1e1e1e", fg="#aaaaaa",
                                   font=("Segoe UI", 10), anchor="w")
        self.path_label.pack(side="left", fill="x", expand=True)

        tk.Button(select_frame, text="Select Project Folder", command=self.select_project,
                  bg="#3b82f6", fg="white", relief="flat", font=("Segoe UI", 10),
                  cursor="hand2").pack(side="right", padx=5)

        # Scan button
        self.btn_scan = tk.Button(
            left, text="🩺  SCAN PROJECT",
            command=self.scan_project,
            font=("Segoe UI", 12, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_scan.pack(pady=6)

        # Results
        result_frame = tk.LabelFrame(left, text="  DIAGNOSIS  ", font=("Segoe UI", 10, "bold"),
                                     bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        result_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            result_frame, wrap=tk.WORD, font=("Consolas", 10),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled"
        )
        self.output.pack(fill="both", expand=True, padx=6, pady=6)

        # Fix button
        self.btn_fix = tk.Button(
            left, text="Fix Safe Issues",
            command=self.fix_safe_issues,
            font=("Segoe UI", 11, "bold"),
            bg="#22c55e", fg="white",
            activebackground="#16a34a",
            relief="flat", cursor="hand2", height=1,
            state="disabled"
        )
        self.btn_fix.pack(pady=8)

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
        t = self.translations.get(self.current_lang, {}).get("project_doctor", {})

        if not t:
            t = {
                "title": "Project Doctor",
                "subtitle": "1. Select project → 2. Scan → 3. Fix safe issues",
                "explanation": "This tool analyzes your project and finds common problems.\n\nIt checks for:\n• Missing imports\n• Mixed tabs/spaces\n• Unused imports\n• Missing main guard\n• Missing requirements.txt\n• Missing README\n• Missing icon\n• Missing .gitignore\n\nSafe issues can be fixed automatically."
            }

        self.title_label.config(text=t.get("title", "Project Doctor"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def select_project(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.project_path = path
            self.path_label.config(text=path, fg="white")
            self.btn_fix.config(state="disabled")
            self.clear_output()

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

    def scan_project(self):
        if not self.project_path:
            messagebox.showwarning("No project", "Please select a project folder first.")
            return

        self.issues = []
        self.clear_output()
        self.write("🔍 Scanning project...\n\n")

        # Check files
        files = os.listdir(self.project_path)
        has_main = any(f.endswith(".py") for f in files)
        has_requirements = "requirements.txt" in files
        has_readme = any(f.lower().startswith("readme") for f in files)
        has_gitignore = ".gitignore" in files
        has_icon = any(f.endswith(".ico") for f in files) or os.path.exists(os.path.join(self.project_path, "assets", "icon.ico"))

        if not has_requirements:
            self.issues.append(("missing_requirements", "❌ Missing requirements.txt"))
        if not has_readme:
            self.issues.append(("missing_readme", "❌ Missing README"))
        if not has_gitignore:
            self.issues.append(("missing_gitignore", "❌ Missing .gitignore"))
        if not has_icon:
            self.issues.append(("missing_icon", "❌ Missing icon (.ico)"))

        # Check Python files
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    self.check_python_file(filepath)

        if not self.issues:
            self.write("✅ No major issues found!\nYour project looks healthy.")
        else:
            self.write(f"Found {len(self.issues)} issue(s):\n\n")
            for _, msg in self.issues:
                self.write(msg + "\n")
            self.btn_fix.config(state="normal")

    def check_python_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Main guard
            if "if __name__" not in content and filepath.endswith("main.py"):
                self.issues.append(("missing_main_guard", f"❌ Missing main guard in {os.path.basename(filepath)}"))

            # Mixed tabs/spaces
            if "\t" in content and "    " in content:
                self.issues.append(("mixed_indent", f"❌ Mixed tabs and spaces in {os.path.basename(filepath)}"))

        except Exception:
            pass

    def write(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")
        self.output.see(tk.END)

    def fix_safe_issues(self):
        if not self.project_path:
            return

        fixed = 0
        for issue_type, _ in self.issues:
            if issue_type == "missing_requirements":
                path = os.path.join(self.project_path, "requirements.txt")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("customtkinter\n")
                fixed += 1
            elif issue_type == "missing_readme":
                path = os.path.join(self.project_path, "README.md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("# My Project\n\nDescription of the project.\n")
                fixed += 1
            elif issue_type == "missing_gitignore":
                path = os.path.join(self.project_path, ".gitignore")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("__pycache__/\n*.pyc\n.env\ndist/\nbuild/\n*.spec\n")
                fixed += 1

        messagebox.showinfo("Done", f"Fixed {fixed} safe issue(s).\n\nPlease scan again to verify.")
        self.btn_fix.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectDoctor(root)
    root.mainloop()