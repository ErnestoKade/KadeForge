#  KadeForge

 **Beginner-friendly toolbox for Python / Tkinter / CustomTkinter developers**

Everything is independent • Everything is local • No telemetry • Open source

---

## What is this?

KadeForge is a collection of simple, visual tools that help beginners (and more experienced developers as well) write cleaner and more modern Python GUI applications without needing to search StackOverflow every 5 minutes.

You click a tool → you see a live preview → you get the ready-to-use code with clear explanations of **where** to paste it.

---
## Included Tools

### Main Window 

![Main Window](assets/screenshots/01_prez.png)

### Indent Fixer

![Indent Fixer](assets/screenshots/02_indentfixer.png)

### Tkinter → CustomTkinter

![Tkinter to CustomTkinter](assets/screenshots/15_tk_to_ctk.png)

### Progress Bar Adder

![Progress Bar Adder](assets/screenshots/03_baradder.png)

### UI Modernizer

![UI Modernizer](assets/screenshots/08_uimodern.png)

### Status / Logs Adder

![Status / Logs Adder](assets/screenshots/04_logadder.png)

### Interface Templates

![Interface Templates](assets/screenshots/09_intertemplate.png)

### PyInstaller Builder

![PyInstaller Builder](assets/screenshots/05_installbuilder.png)

### Import Cleaner

![Import Cleaner](assets/screenshots/10_impcleaner.png)

### Icon Adder

![Icon Adder](assets/screenshots/06_iconadder.png)

### Project Doctor

![Project Doctor](assets/screenshots/11_projectdoctor.png)

### Scrollable Frame Adder

![Scrollable Frame Adder](assets/screenshots/16_scrollframadd.png)

### Exception Wrapper

![Exception Wrapper](assets/screenshots/12_wrapper.png)

### Theme Switcher

![Theme Switcher](assets/screenshots/14_themeswitch.png)

### Release Packager

![Release Packager](assets/screenshots/13_releasepack.png)

### Config File Creator

![Config File Creator](assets/screenshots/07_confilecreator.png)

### User Guide

![User Guide](assets/screenshots/17_userguide.png)

## Multilingual User Guide

KadeForge includes a built-in **multilingual help panel** available directly 

inside the application. 

Each tool contains: 
- what the tool is for 
- how to use it 
- the expected result 
- and what to do next 

### Supported languages 

- English 
- Français 
- Español 
- Deutsch 
- Italiano 
- Português 

The language can be changed at any time from the top bar of the User Guide. 

### Code Helpers

- **Indent Fixer** – Fixes broken indentation from copy-paste
- **Import Cleaner** – Removes unused imports + sorts them
- **Pathlib Converter** – Converts classic `os.path` to modern `pathlib`
- **Exception Wrapper** – Wraps functions with try/except safely

### UI Helpers

- **Tkinter → CustomTkinter** – Converts classic Tkinter code to CustomTkinter
- **Progress Bar Adder** – Adds determinate / indeterminate progress bars with %
- **Scrollable Frame Adder** – Creates a fully working scrollable frame (the hardest part for beginners)
- **Theme Switcher** – Adds Dark / Light / System theme support
- **Status / Logs Adder** – Adds a status bar or log panel
- **UI Modernizer** – Modernizes colors, fonts and spacing

### Project Helpers

- **PyInstaller Builder** – Generates the correct one-file / windowed command with icon
- **Icon Adder** – Adds `iconbitmap` + prepares PyInstaller icon command
- **Config File Creator** – Creates `config.json` + load/save functions
- **Project Doctor** – Scans your project for common problems and offers safe fixes

---

## How to use

1. Launch `main.py` (or the compiled `.exe`)
2. Choose a tool
3. Select options → see the live preview
4. Click **Generate Code**
5. Copy the code and paste it where the tool tells you

Every tool has a right panel with clear explanations in multiple languages.

---


## Installation (from source)

bash
git clone https://github.com/YOUR_USERNAME/KadeForge.git
cd KadeForge
pip install -r requirements.txt
python main.py

## Build single .exe

```bash python -m PyInstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --add-data "tools;tools" --add-data "lang;lang" main.py ```

## Requirements 

- Python 3.10+ 
- customtkinter 
- autopep8 (for Indent Fixer)

## Philosophy

No internet required
No telemetry
No complex dependencies
Clear visual feedback for beginners
Code that you can actually understand and modify

## Author

ErnestoKade

## License

KadeForge is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See the [LICENSE](LICENSE) file for full details.


