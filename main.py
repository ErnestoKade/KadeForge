import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Toolbox(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KadeForge - by ErnestoKade")
        self.geometry("720x620")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        try:
            self.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass

        title = ctk.CTkLabel(
            self,
            text="KadeForge",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(15, 2))

        subtitle = ctk.CTkLabel(
            self,
            text="Beginner-friendly tools • Everything is independent",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa"
        )
        subtitle.pack(pady=(0, 12))

        # === 2 COLUMNS ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=5)

        tools = [
            ("Indent Fixer", "indent_fixer"),
            ("Tkinter → CustomTkinter", "tk_to_ctk"),
            ("Progress Bar Adder", "progress_bar_adder"),
            ("UI Modernizer", "ui_modernizer"),
            ("Status / Logs Adder", "status_logger"),
            ("Interface Templates", "interface_templates"),
            ("PyInstaller Builder", "pyinstaller_builder"),
            ("Import Cleaner", "import_cleaner"),
            ("Icon Adder", "icon_adder"),
            ("Project Doctor", "project_doctor"),
            ("Scrollable Frame Adder", "scrollable_frame_adder"),
            ("Exception Wrapper", "exception_wrapper"),
            ("Theme Switcher", "theme_switcher"),
            ("Release Packager", "release_packager"),
            ("Config File Creator", "config_file_creator"),
            ("User Guide", "user_guide"),
        ]

        for i, (text, folder) in enumerate(tools):
            if folder == "user_guide":
                # Button
                btn = ctk.CTkButton(
                    btn_frame,
                    text=text,
                    width=300,
                    height=34,
                    font=ctk.CTkFont(size=13),
                    fg_color="#15803D",          # vert
                    hover_color="#166534",
                    command=lambda f=folder: self.launch_tool(f)
                )
            else:
                btn = ctk.CTkButton(
                    btn_frame,
                    text=text,
                    width=300,
                    height=34,
                    font=ctk.CTkFont(size=13),
                    command=lambda f=folder: self.launch_tool(f)
                )
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=4)
        footer = ctk.CTkLabel(
            self,
            text="Developed by ErnestoKade",
            font=ctk.CTkFont(size=11),
            text_color="#777777"
        )
        footer.pack(side="bottom", pady=10)

    def launch_tool(self, tool_folder):
        tool_path = resource_path(f"tools/{tool_folder}/main.py")

        if not os.path.exists(tool_path):
            messagebox.showinfo(
                "Coming soon",
                f"The tool « {tool_folder} » is not yet implemented."
            )
            return

        try:
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                ["python", tool_path],
                cwd=os.path.dirname(tool_path),
                creationflags=CREATE_NO_WINDOW
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch tool:\n{e}")

if __name__ == "__main__":
    app = Toolbox()
    app.mainloop()