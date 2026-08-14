import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json
import os
import sys
import shutil
import zipfile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ReleasePackager:
    def __init__(self, root):
        self.root = root
        self.root.title("Release Packager - by ErnestoKade")
        self.root.geometry("1050x760")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_lang = "en"
        self.translations = self.load_translations()
        self.exe_path = None

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

        # Select EXE
        select_frame = tk.Frame(left, bg="#1e1e1e")
        select_frame.pack(fill="x", pady=8)

        self.path_label = tk.Label(select_frame, text="No .exe selected", bg="#1e1e1e", fg="#aaaaaa",
                                   font=("Segoe UI", 10), anchor="w")
        self.path_label.pack(side="left", fill="x", expand=True)

        tk.Button(select_frame, text="Select .exe", command=self.select_exe,
                  bg="#3b82f6", fg="white", relief="flat", font=("Segoe UI", 10),
                  cursor="hand2").pack(side="right")

        # Options
        options_frame = tk.LabelFrame(left, text="  OPTIONS  ", font=("Segoe UI", 10, "bold"),
                                      bg="#1e1e1e", fg="#3b82f6", bd=1, relief="solid")
        options_frame.pack(fill="x", pady=8)

        self.include_readme = tk.BooleanVar(value=True)
        self.include_license = tk.BooleanVar(value=True)

        tk.Checkbutton(options_frame, text="Include README.md", variable=self.include_readme,
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=4)
        tk.Checkbutton(options_frame, text="Include LICENSE", variable=self.include_license,
                       bg="#1e1e1e", fg="white", selectcolor="#2d2d2d", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=4)

        # Button
        self.btn_package = tk.Button(
            left, text="CREATE RELEASE ZIP",
            command=self.create_package,
            font=("Segoe UI", 12, "bold"),
            bg="#22c55e", fg="white",
            activebackground="#16a34a",
            relief="flat", cursor="hand2", height=1
        )
        self.btn_package.pack(pady=10)

        # Log
        log_frame = tk.LabelFrame(left, text="  LOG  ", font=("Segoe UI", 10, "bold"),
                                  bg="#1e1e1e", fg="#22c55e", bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True)

        self.output = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, font=("Consolas", 10),
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
        t = self.translations.get(self.current_lang, {}).get("release_packager", {})

        if not t:
            t = {
                "title": "Release Packager",
                "subtitle": "1. Select .exe → 2. Choose options → 3. Create ZIP",
                "explanation": "This tool creates a clean ZIP ready for GitHub Releases.\n\nIt includes:\n• Your .exe\n• README.md (optional)\n• LICENSE (optional)\n\nThe ZIP is created next to your .exe."
            }

        self.title_label.config(text=t.get("title", "Release Packager"))
        self.subtitle_label.config(text=t.get("subtitle", ""))
        self.exp_label.config(text=t.get("explanation", ""))
        self.root.after(100, lambda: self.exp_canvas.configure(scrollregion=self.exp_canvas.bbox("all")))

    def select_exe(self):
        path = filedialog.askopenfilename(title="Select .exe", filetypes=[("Executable", "*.exe")])
        if path:
            self.exe_path = path
            self.path_label.config(text=path, fg="white")

    def write(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.config(state="disabled")
        self.output.see(tk.END)

    def create_package(self):
        if not self.exe_path:
            messagebox.showwarning("No file", "Please select a .exe first.")
            return

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

        try:
            folder = os.path.dirname(self.exe_path)
            name = os.path.splitext(os.path.basename(self.exe_path))[0]
            zip_path = os.path.join(folder, f"{name}_Release.zip")

            self.write(f"Creating {zip_path}...")

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.exe_path, os.path.basename(self.exe_path))
                self.write(f"✓ Added {os.path.basename(self.exe_path)}")

                if self.include_readme.get():
                    readme = os.path.join(folder, "README.md")
                    if os.path.exists(readme):
                        zipf.write(readme, "README.md")
                        self.write("✓ Added README.md")
                    else:
                        # Create a basic one
                        content = f"# {name}\n\nRelease package."
                        zipf.writestr("README.md", content)
                        self.write("✓ Created basic README.md")

                if self.include_license.get():
                    license_file = os.path.join(folder, "LICENSE")
                    if os.path.exists(license_file):
                        zipf.write(license_file, "LICENSE")
                        self.write("✓ Added LICENSE")
                    else:
                        zipf.writestr("LICENSE", "MIT License\n\nCopyright (c) 2026")
                        self.write("✓ Created basic LICENSE")

            self.write(f"\n✅ Done! ZIP created:\n{zip_path}")
            messagebox.showinfo("Success", f"Release ZIP created:\n{zip_path}")

        except Exception as e:
            self.write(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ReleasePackager(root)
    root.mainloop()