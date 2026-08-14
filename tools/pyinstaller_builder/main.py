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

class PyInstallerBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("PyInstaller Builder - by ErnestoKade")
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

        # === OPTIONS ===
        options_frame = tk.LabelFrame(left, text="  OPTIONS  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        options_frame.pack(fill="x", pady=(0, 8))

        # Script name
        script_frame = tk.Frame(options_frame, bg="#1e1e1e")
        script_frame.pack(fill="x", padx=10, pady=6)
        tk.Label(script_frame, text="Script name:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10)).pack(side="left")
        self.script_var = tk.StringVar(value="main.py")
        entry_script = tk.Entry(script_frame, textvariable=self.script_var, bg="#2d2d2d", fg="white",
                                insertbackground="white", width=16, relief="flat")
        entry_script.pack(side="left", padx=8)

        # Mode
        mode_frame = tk.Frame(options_frame, bg="#1e1e1e")
        mode_frame.pack(fill="x", padx=10, pady=4)
        self.mode_var = tk.StringVar(value="onefile")
        tk.Radiobutton(mode_frame, text="--onefile (single .exe)", variable=self.mode_var, value="onefile",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)
        tk.Radiobutton(mode_frame, text="--onedir (folder)", variable=self.mode_var, value="onedir",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)

        # Console
        console_frame = tk.Frame(options_frame, bg="#1e1e1e")
        console_frame.pack(fill="x", padx=10, pady=4)
        self.console_var = tk.StringVar(value="windowed")
        tk.Radiobutton(console_frame, text="--windowed (no console)", variable=self.console_var, value="windowed",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)
        tk.Radiobutton(console_frame, text="--console (show console)", variable=self.console_var, value="console",
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)

        # Icon
        icon_frame = tk.Frame(options_frame, bg="#1e1e1e")
        icon_frame.pack(fill="x", padx=10, pady=4)
        self.icon_var = tk.BooleanVar(value=True)
        tk.Checkbutton(icon_frame, text="Include icon", variable=self.icon_var,
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left")
        self.icon_path = tk.StringVar(value="assets/icon.ico")
        entry_icon = tk.Entry(icon_frame, textvariable=self.icon_path, bg="#2d2d2d", fg="white",
                              insertbackground="white", width=20, relief="flat")
        entry_icon.pack(side="left", padx=8)

        # Add data
        data_frame = tk.Frame(options_frame, bg="#1e1e1e")
        data_frame.pack(fill="x", padx=10, pady=4)
        self.assets_var = tk.BooleanVar(value=True)
        self.tools_var = tk.BooleanVar(value=True)
        tk.Checkbutton(data_frame, text="--add-data assets", variable=self.assets_var,
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)
        tk.Checkbutton(data_frame, text="--add-data tools", variable=self.tools_var,
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10),
                       command=self.update_command).pack(side="left", padx=5)

        # === LIVE COMMAND PREVIEW ===
        preview_frame = tk.LabelFrame(left, text="  LIVE COMMAND  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        preview_frame.pack(fill="x", pady=8)

        self.command_preview = tk.Text(preview_frame, height=3, font=("Consolas", 10),
                                       bg="#2d2d2d", fg="#22c55e", relief="flat", wrap="word")
        self.command_preview.pack(fill="x", padx=8, pady=8)
        self.command_preview.config(state="disabled")

        # Generate button
        self.btn_generate = tk.Button(
            left, text="GENERATE COMMAND",
            command=self.generate_code,
            font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white",
            activebackground="#2563eb",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_generate.pack(pady=6)

        # Final Code
        code_frame = tk.LabelFrame(left, text="  FINAL COMMAND  ", font=("Segoe UI", 10, "bold"),
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

        # Traces
        self.script_var.trace_add("write", lambda *args: self.update_command())
        self.icon_path.trace_add("write", lambda *args: self.update_command())

        self.change_language()
        self.update_command()

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
        t = self.translations.get(self.current_lang, {}).get("pyinstaller_builder", {})

        if not t:
            t = {
                "title": "PyInstaller Builder",
                "subtitle": "1. Choose options → 2. See live command → 3. Generate",
                "explanation": "This tool builds the perfect PyInstaller command for your project.\n\nOptions:\n• --onefile or --onedir\n• --windowed or --console\n• Icon support\n• Add data folders (assets / tools)\n\nWhere to use:\n\n1. Open PowerShell in your project folder\n2. Paste the generated command\n3. Press Enter\n\nThe .exe will be created in the 'dist' folder.\n\nTip: Always test with --onedir first if you have problems."
            }

        self.title_label.config(text=t.get("title", "PyInstaller Builder"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def update_command(self):
        cmd = ["python -m PyInstaller"]

        if self.mode_var.get() == "onefile":
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")

        if self.console_var.get() == "windowed":
            cmd.append("--windowed")
        else:
            cmd.append("--console")

        if self.icon_var.get() and self.icon_path.get().strip():
            cmd.append(f'--icon="{self.icon_path.get().strip()}"')

        if self.assets_var.get():
            cmd.append('--add-data "assets;assets"')
        if self.tools_var.get():
            cmd.append('--add-data "tools;tools"')

        script = self.script_var.get().strip() or "main.py"
        cmd.append(script)

        full_cmd = " ".join(cmd)

        self.command_preview.config(state="normal")
        self.command_preview.delete("1.0", tk.END)
        self.command_preview.insert("1.0", full_cmd)
        self.command_preview.config(state="disabled")

        self.current_command = full_cmd

    def generate_code(self):
        self.update_command()
        final = f"""# ===== PyInstaller Command =====
# Copy and paste this into PowerShell (in your project folder)

{self.current_command}

# After running:
# → The executable will be in the "dist" folder
"""
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", final)
        self.output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyInstallerBuilder(root)
    root.mainloop()