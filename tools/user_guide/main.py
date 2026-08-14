import tkinter as tk
from tkinter import scrolledtext
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class UserGuide:
    def __init__(self, root):
        self.root = root
        self.root.title("User Guide - KadeForge")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_lang = "en"
        self.current_tool = "progress_bar"
        self.translations = self.load_translations()

        # === TOP BAR (Language) ===
        top_frame = tk.Frame(root, bg="#1e1e1e")
        top_frame.pack(fill="x", padx=15, pady=8)

        tk.Label(top_frame, text="Language:", bg="#1e1e1e", fg="#aaaaaa", font=("Segoe UI", 11)).pack(side="left")

        self.lang_var = tk.StringVar(value="en")
        for code, name in [("en", "EN"), ("fr", "FR"), ("es", "ES"), ("de", "DE"), ("it", "IT"), ("pt", "PT")]:
            tk.Radiobutton(
                top_frame, text=name, variable=self.lang_var, value=code,
                bg="#1e1e1e", fg="white", selectcolor="#2d2d2d",
                font=("Segoe UI", 10), command=self.change_language
            ).pack(side="left", padx=3)

        # === MAIN CONTAINER ===
        main = tk.Frame(root, bg="#1e1e1e")
        main.pack(fill="both", expand=True, padx=15, pady=5)

        # LEFT - List of tools
        left = tk.Frame(main, bg="#1e1e1e", width=270)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text="TOOLS", font=("Segoe UI", 13, "bold"), bg="#1e1e1e", fg="#3b82f6").pack(pady=(5, 10))

        self.tools_list = [
            ("Progress Bar Adder", "progress_bar"),
            ("Indent Fixer", "indent_fixer"),
            ("Tkinter → CustomTkinter", "tk_to_ctk"),
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
        ]

        self.tool_buttons = {}
        for text, key in self.tools_list:
            btn = tk.Button(
                left, text=text, anchor="w",
                bg="#2d2d2d", fg="white", relief="flat",
                font=("Segoe UI", 11),
                cursor="hand2", 
                command=lambda k=key: self.select_tool(k)
            )
            btn.pack(fill="x", pady=2, padx=5)
            self.tool_buttons[key] = btn

        # RIGHT - Content
        right = tk.Frame(main, bg="#1e1e1e")
        right.pack(side="left", fill="both", expand=True)

        self.content = scrolledtext.ScrolledText(
            right, wrap=tk.WORD, font=("Segoe UI", 12),
            bg="#2d2d2d", fg="white", insertbackground="white",
            state="disabled", padx=15, pady=15
        )
        self.content.pack(fill="both", expand=True)

        self.select_tool("progress_bar")
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
        self.show_content()

    def select_tool(self, tool_key):
        self.current_tool = tool_key

        for key, btn in self.tool_buttons.items():
            if key == tool_key:
                btn.config(bg="#3b82f6")
            else:
                btn.config(bg="#2d2d2d")

        self.show_content()

    def show_content(self):
        sections = {
            "en": {"what": "1. WHAT IS IT FOR?", "how": "2. HOW TO USE IT?", "result": "3. EXPECTED RESULT", "next": "4. WHAT TO DO NEXT?"},
            "fr": {"what": "1. À QUOI ÇA SERT ?", "how": "2. COMMENT L'UTILISER ?", "result": "3. RÉSULTAT ATTENDU", "next": "4. QUE FAIRE ENSUITE ?"},
            "es": {"what": "1. ¿PARA QUÉ SIRVE?", "how": "2. ¿CÓMO USARLO?", "result": "3. RESULTADO ESPERADO", "next": "4. ¿QUÉ HACER DESPUÉS?"},
            "de": {"what": "1. WOFÜR IST ES GUT?", "how": "2. WIE BENUTZT MAN ES?", "result": "3. ERWARTETES ERGEBNIS", "next": "4. WAS DANACH TUN?"},
            "it": {"what": "1. A COSA SERVE?", "how": "2. COME USARLO?", "result": "3. RISULTATO ATTESO", "next": "4. COSA FARE DOPO?"},
            "pt": {"what": "1. PARA QUE SERVE?", "how": "2. COMO USAR?", "result": "3. RESULTADO ESPERADO", "next": "4. O QUE FAZER A SEGUIR?"}
        }
        sec = sections.get(self.current_lang, sections["en"])

        guides = {
        "en": {
            "progress_bar": {"title": "Progress Bar Adder", "what": "This tool helps you add a progress bar so the user can see that your program is working.", "how": "• Choose the type (with % or moving bar)\n• Look at the preview\n• Click GENERATE CODE\n• Copy the code", "result": "You get ready-to-use code for a progress bar.", "next": "Paste the code inside your __init__ method and call the update functions when needed."},
            "indent_fixer": {"title": "Indent Fixer", "what": "This tool fixes bad indentation in your Python code.", "how": "• Paste your code on the left\n• Click the button\n• Copy the fixed code on the right", "result": "Clean and correctly indented code.", "next": "Replace your old code with the new fixed version."},
            "tk_to_ctk": {"title": "Tkinter → CustomTkinter", "what": "This tool converts classic Tkinter code into modern CustomTkinter code.", "how": "• Paste your Tkinter code\n• Click CONVERT\n• Copy the new code", "result": "Code ready for CustomTkinter.", "next": "Replace your old file or copy the widgets into your project. Don't forget: pip install customtkinter"},
            "ui_modernizer": {"title": "UI Modernizer", "what": "This tool gives you modern ready-to-use pieces of interface (buttons, colors, dark mode...).", "how": "• Choose an option\n• Look at the preview\n• Click GENERATE CODE", "result": "Modern code snippets.", "next": "Copy the parts you like and paste them into your __init__ method."},
            "status_logger": {"title": "Status / Logs Adder", "what": "This tool adds a status bar or a live log zone at the bottom of your window.", "how": "• Choose the type\n• Look at the preview\n• Click GENERATE CODE", "result": "Code for status bar or logs.", "next": "Paste the widget in __init__ and the functions at the same level as __init__."},
            "interface_templates": {"title": "Interface Templates", "what": "This tool gives you complete ready-to-use window templates.", "how": "• Choose a template\n• Look at the preview\n• Click GENERATE FULL CODE", "result": "A full working window code.", "next": "Create a new file, paste the code and run it. Then modify it as you want."},
            "pyinstaller_builder": {"title": "PyInstaller Builder", "what": "This tool creates the correct command to turn your Python program into a .exe file.", "how": "• Choose your options (onefile, icon, etc.)\n• Look at the live command\n• Click GENERATE COMMAND", "result": "A ready-to-copy PyInstaller command.", "next": "Open PowerShell in your project folder, paste the command and press Enter."},
            "import_cleaner": {"title": "Import Cleaner", "what": "This tool removes unused imports and sorts them cleanly.", "how": "• Paste your code\n• Click CLEAN & SORT IMPORTS\n• Copy the cleaned version", "result": "Clean and sorted imports.", "next": "Replace the import section at the top of your file with the new version."},
            "icon_adder": {"title": "Icon Adder", "what": "This tool adds an icon to your Tkinter or CustomTkinter window.", "how": "• Choose Tkinter or CustomTkinter\n• Enter the icon path\n• Click GENERATE CODE", "result": "The correct iconbitmap line.", "next": "Paste the code inside your __init__ method, just after creating the window."},
            "project_doctor": {"title": "Project Doctor", "what": "This tool checks your project for common problems (missing files, bad indentation, etc.).", "how": "• Select your project folder\n• Click SCAN PROJECT\n• Optionally click Fix Safe Issues", "result": "A list of problems found in your project.", "next": "Fix the issues manually or use the automatic fix for safe ones."},
            "scrollable_frame_adder": {"title": "Scrollable Frame Adder", "what": "This tool creates a scrollable area (very useful when you have a lot of widgets).", "how": "• Choose Tkinter or CustomTkinter\n• Look at the preview\n• Click GENERATE CODE", "result": "Complete code for a scrollable frame.", "next": "Paste the code in your __init__ and put your widgets inside the scrollable frame."},
            "exception_wrapper": {"title": "Exception Wrapper", "what": "This tool protects your functions so the program does not crash when an error happens.", "how": "• Choose the type (console or messagebox)\n• Enter the function name\n• Click GENERATE CODE", "result": "A try/except block ready to use.", "next": "Replace your function call with the protected version."},
            "theme_switcher": {"title": "Theme Switcher", "what": "This tool adds a Dark / Light / System theme selector to your CustomTkinter app.", "how": "• Click GENERATE CODE\n• Copy the code", "result": "Code for a theme switcher menu.", "next": "Paste the menu in __init__ and the function at the same level as __init__."},
            "release_packager": {"title": "Release Packager", "what": "This tool creates a clean ZIP file ready to upload on GitHub Releases.", "how": "• Select your .exe file\n• Choose if you want README and LICENSE\n• Click CREATE RELEASE ZIP", "result": "A ZIP file next to your .exe.", "next": "Upload the ZIP to the Releases section of your GitHub repository."},
            "config_file_creator": {"title": "Config File Creator", "what": "This tool creates a simple system to save and load settings (config.json).", "how": "• Click GENERATE CODE\n• Copy the code", "result": "Functions load_config() and save_config() + example.", "next": "Create a config.json file and put the two functions in your project."}
        },
        "fr": {
            "progress_bar": {"title": "Ajouteur de Barre de Progression", "what": "Cet outil t'aide à ajouter une barre de progression pour que l'utilisateur voie que ton programme travaille.", "how": "• Choisis le type (avec % ou barre qui bouge)\n• Regarde l'aperçu\n• Clique sur GENERATE CODE\n• Copie le code", "result": "Tu obtiens un code prêt à l'emploi pour une barre de progression.", "next": "Colle le code dans ta méthode __init__ et appelle les fonctions de mise à jour quand tu en as besoin."},
            "indent_fixer": {"title": "Correcteur d'Indentation", "what": "Cet outil corrige la mauvaise indentation de ton code Python.", "how": "• Colle ton code à gauche\n• Clique sur le bouton\n• Copie le code corrigé à droite", "result": "Code propre et correctement indenté.", "next": "Remplace ton ancien code par la nouvelle version corrigée."},
            "tk_to_ctk": {"title": "Convertisseur Tkinter → CustomTkinter", "what": "Cet outil convertit du code Tkinter classique en code CustomTkinter moderne.", "how": "• Colle ton code Tkinter\n• Clique sur CONVERT\n• Copie le nouveau code", "result": "Code prêt pour CustomTkinter.", "next": "Remplace ton ancien fichier ou copie les widgets dans ton projet. N'oublie pas : pip install customtkinter"},
            "ui_modernizer": {"title": "Moderniseur d'Interface", "what": "Cet outil te donne des morceaux d'interface modernes prêts à l'emploi (boutons, couleurs, dark mode...).", "how": "• Choisis une option\n• Regarde l'aperçu\n• Clique sur GENERATE CODE", "result": "Extraits de code modernes.", "next": "Copie les parties qui te plaisent et colle-les dans ta méthode __init__."},
            "status_logger": {"title": "Ajouteur de Status / Logs", "what": "Cet outil ajoute une barre de status ou une zone de logs en bas de ta fenêtre.", "how": "• Choisis le type\n• Regarde l'aperçu\n• Clique sur GENERATE CODE", "result": "Code pour barre de status ou logs.", "next": "Colle le widget dans __init__ et les fonctions au même niveau que __init__."},
            "interface_templates": {"title": "Modèles d'Interfaces", "what": "Cet outil te donne des modèles de fenêtres complets et prêts à l'emploi.", "how": "• Choisis un modèle\n• Regarde l'aperçu\n• Clique sur GENERATE FULL CODE", "result": "Un code de fenêtre complet et fonctionnel.", "next": "Crée un nouveau fichier, colle le code et lance-le. Ensuite modifie-le comme tu veux."},
            "pyinstaller_builder": {"title": "Constructeur PyInstaller", "what": "Cet outil crée la bonne commande pour transformer ton programme Python en fichier .exe.", "how": "• Choisis tes options (onefile, icône, etc.)\n• Regarde la commande en direct\n• Clique sur GENERATE COMMAND", "result": "Une commande PyInstaller prête à copier.", "next": "Ouvre PowerShell dans le dossier de ton projet, colle la commande et appuie sur Entrée."},
            "import_cleaner": {"title": "Nettoyeur d'Imports", "what": "Cet outil supprime les imports inutilisés et les trie proprement.", "how": "• Colle ton code\n• Clique sur CLEAN & SORT IMPORTS\n• Copie la version nettoyée", "result": "Imports propres et triés.", "next": "Remplace la section des imports en haut de ton fichier par la nouvelle version."},
            "icon_adder": {"title": "Ajouteur d'Icône", "what": "Cet outil ajoute une icône à ta fenêtre Tkinter ou CustomTkinter.", "how": "• Choisis Tkinter ou CustomTkinter\n• Entre le chemin de l'icône\n• Clique sur GENERATE CODE", "result": "La bonne ligne iconbitmap.", "next": "Colle le code dans ta méthode __init__, juste après la création de la fenêtre."},
            "project_doctor": {"title": "Project Doctor", "what": "Cet outil vérifie ton projet pour trouver les problèmes courants (fichiers manquants, mauvaise indentation, etc.).", "how": "• Sélectionne le dossier de ton projet\n• Clique sur SCAN PROJECT\n• Tu peux aussi cliquer sur Fix Safe Issues", "result": "Une liste des problèmes trouvés dans ton projet.", "next": "Corrige les problèmes à la main ou utilise la correction automatique pour les problèmes sûrs."},
            "scrollable_frame_adder": {"title": "Ajouteur de Frame Scrollable", "what": "Cet outil crée une zone qui défile (très utile quand tu as beaucoup de widgets).", "how": "• Choisis Tkinter ou CustomTkinter\n• Regarde l'aperçu\n• Clique sur GENERATE CODE", "result": "Code complet pour une frame scrollable.", "next": "Colle le code dans ton __init__ et mets tes widgets à l'intérieur de la frame scrollable."},
            "exception_wrapper": {"title": "Wrapper d'Exception", "what": "Cet outil protège tes fonctions pour que le programme ne plante pas quand une erreur arrive.", "how": "• Choisis le type (console ou messagebox)\n• Entre le nom de la fonction\n• Clique sur GENERATE CODE", "result": "Un bloc try/except prêt à l'emploi.", "next": "Remplace ton appel de fonction par la version protégée."},
            "theme_switcher": {"title": "Changeur de Thème", "what": "Cet outil ajoute un sélecteur de thème (Dark / Light / System) à ton application CustomTkinter.", "how": "• Clique sur GENERATE CODE\n• Copie le code", "result": "Code pour un menu de changement de thème.", "next": "Colle le menu dans __init__ et la fonction au même niveau que __init__."},
            "release_packager": {"title": "Packager de Release", "what": "Cet outil crée un fichier ZIP propre prêt à être mis sur GitHub Releases.", "how": "• Sélectionne ton fichier .exe\n• Choisis si tu veux README et LICENSE\n• Clique sur CREATE RELEASE ZIP", "result": "Un fichier ZIP à côté de ton .exe.", "next": "Envoie le ZIP dans la section Releases de ton dépôt GitHub."},
            "config_file_creator": {"title": "Créateur de Fichier Config", "what": "Cet outil crée un système simple pour sauvegarder et charger des réglages (config.json).", "how": "• Clique sur GENERATE CODE\n• Copie le code", "result": "Les fonctions load_config() et save_config() + un exemple.", "next": "Crée un fichier config.json et mets les deux fonctions dans ton projet."}
        },
        "es": {
            "progress_bar": {"title": "Añadir Barra de Progreso", "what": "Esta herramienta te ayuda a añadir una barra de progreso para que el usuario vea que tu programa está trabajando.", "how": "• Elige el tipo (con % o barra que se mueve)\n• Mira la vista previa\n• Haz clic en GENERATE CODE\n• Copia el código", "result": "Obtienes código listo para usar de una barra de progreso.", "next": "Pega el código dentro de tu método __init__ y llama a las funciones de actualización cuando las necesites."},
            "indent_fixer": {"title": "Corrector de Indentación", "what": "Esta herramienta corrige la mala indentación de tu código Python.", "how": "• Pega tu código a la izquierda\n• Haz clic en el botón\n• Copia el código corregido a la derecha", "result": "Código limpio y correctamente indentado.", "next": "Reemplaza tu código antiguo con la nueva versión corregida."},
            "tk_to_ctk": {"title": "Convertidor Tkinter → CustomTkinter", "what": "Esta herramienta convierte código Tkinter clásico en código CustomTkinter moderno.", "how": "• Pega tu código Tkinter\n• Haz clic en CONVERT\n• Copia el nuevo código", "result": "Código listo para CustomTkinter.", "next": "Reemplaza tu archivo antiguo o copia los widgets en tu proyecto. No olvides: pip install customtkinter"},
            "ui_modernizer": {"title": "Modernizador de UI", "what": "Esta herramienta te da piezas modernas de interfaz listas para usar (botones, colores, modo oscuro...).", "how": "• Elige una opción\n• Mira la vista previa\n• Haz clic en GENERATE CODE", "result": "Fragmentos de código modernos.", "next": "Copia las partes que te gusten y pégalas en tu método __init__."},
            "status_logger": {"title": "Añadir Status / Logs", "what": "Esta herramienta añade una barra de estado o una zona de logs en la parte inferior de tu ventana.", "how": "• Elige el tipo\n• Mira la vista previa\n• Haz clic en GENERATE CODE", "result": "Código para barra de estado o logs.", "next": "Pega el widget en __init__ y las funciones al mismo nivel que __init__."},
            "interface_templates": {"title": "Plantillas de Interfaz", "what": "Esta herramienta te da plantillas de ventanas completas y listas para usar.", "how": "• Elige una plantilla\n• Mira la vista previa\n• Haz clic en GENERATE FULL CODE", "result": "Un código de ventana completo y funcional.", "next": "Crea un nuevo archivo, pega el código y ejecútalo. Luego modifícalo como quieras."},
            "pyinstaller_builder": {"title": "Constructor de PyInstaller", "what": "Esta herramienta crea el comando correcto para convertir tu programa Python en un archivo .exe.", "how": "• Elige tus opciones (onefile, icono, etc.)\n• Mira el comando en vivo\n• Haz clic en GENERATE COMMAND", "result": "Un comando de PyInstaller listo para copiar.", "next": "Abre PowerShell en la carpeta de tu proyecto, pega el comando y pulsa Enter."},
            "import_cleaner": {"title": "Limpiador de Imports", "what": "Esta herramienta elimina los imports no utilizados y los ordena limpiamente.", "how": "• Pega tu código\n• Haz clic en CLEAN & SORT IMPORTS\n• Copia la versión limpia", "result": "Imports limpios y ordenados.", "next": "Reemplaza la sección de imports al principio de tu archivo con la nueva versión."},
            "icon_adder": {"title": "Añadir Icono", "what": "Esta herramienta añade un icono a tu ventana Tkinter o CustomTkinter.", "how": "• Elige Tkinter o CustomTkinter\n• Introduce la ruta del icono\n• Haz clic en GENERATE CODE", "result": "La línea correcta de iconbitmap.", "next": "Pega el código dentro de tu método __init__, justo después de crear la ventana."},
            "project_doctor": {"title": "Project Doctor", "what": "Esta herramienta revisa tu proyecto en busca de problemas comunes (archivos faltantes, mala indentación, etc.).", "how": "• Selecciona la carpeta de tu proyecto\n• Haz clic en SCAN PROJECT\n• Opcionalmente haz clic en Fix Safe Issues", "result": "Una lista de problemas encontrados en tu proyecto.", "next": "Corrige los problemas manualmente o usa la corrección automática para los seguros."},
            "scrollable_frame_adder": {"title": "Añadir Frame Scrollable", "what": "Esta herramienta crea una zona con scroll (muy útil cuando tienes muchos widgets).", "how": "• Elige Tkinter o CustomTkinter\n• Mira la vista previa\n• Haz clic en GENERATE CODE", "result": "Código completo para un frame scrollable.", "next": "Pega el código en tu __init__ y pon tus widgets dentro del frame scrollable."},
            "exception_wrapper": {"title": "Wrapper de Excepción", "what": "Esta herramienta protege tus funciones para que el programa no se cierre cuando ocurre un error.", "how": "• Elige el tipo (consola o messagebox)\n• Introduce el nombre de la función\n• Haz clic en GENERATE CODE", "result": "Un bloque try/except listo para usar.", "next": "Reemplaza la llamada a tu función con la versión protegida."},
            "theme_switcher": {"title": "Cambiador de Tema", "what": "Esta herramienta añade un selector de tema (Dark / Light / System) a tu aplicación CustomTkinter.", "how": "• Haz clic en GENERATE CODE\n• Copia el código", "result": "Código para un menú de cambio de tema.", "next": "Pega el menú en __init__ y la función al mismo nivel que __init__."},
            "release_packager": {"title": "Empaquetador de Release", "what": "Esta herramienta crea un archivo ZIP limpio listo para subir a GitHub Releases.", "how": "• Selecciona tu archivo .exe\n• Elige si quieres README y LICENSE\n• Haz clic en CREATE RELEASE ZIP", "result": "Un archivo ZIP junto a tu .exe.", "next": "Sube el ZIP a la sección Releases de tu repositorio de GitHub."},
            "config_file_creator": {"title": "Creador de Archivo Config", "what": "Esta herramienta crea un sistema simple para guardar y cargar ajustes (config.json).", "how": "• Haz clic en GENERATE CODE\n• Copia el código", "result": "Las funciones load_config() y save_config() + ejemplo.", "next": "Crea un archivo config.json y pon las dos funciones en tu proyecto."}
        },
        "de": {
            "progress_bar": {"title": "Fortschrittsbalken Hinzufügen", "what": "Dieses Tool hilft dir, einen Fortschrittsbalken hinzuzufügen, damit der Benutzer sieht, dass dein Programm arbeitet.", "how": "• Wähle den Typ (mit % oder beweglicher Balken)\n• Schau dir die Vorschau an\n• Klicke auf GENERATE CODE\n• Kopiere den Code", "result": "Du bekommst fertigen Code für einen Fortschrittsbalken.", "next": "Füge den Code in deine __init__-Methode ein und rufe die Update-Funktionen bei Bedarf auf."},
            "indent_fixer": {"title": "Einrückungs-Korrektor", "what": "Dieses Tool korrigiert schlechte Einrückung in deinem Python-Code.", "how": "• Füge deinen Code links ein\n• Klicke auf den Button\n• Kopiere den korrigierten Code rechts", "result": "Sauberer und korrekt eingerückter Code.", "next": "Ersetze deinen alten Code durch die neue korrigierte Version."},
            "tk_to_ctk": {"title": "Tkinter → CustomTkinter Konverter", "what": "Dieses Tool konvertiert klassischen Tkinter-Code in modernen CustomTkinter-Code.", "how": "• Füge deinen Tkinter-Code ein\n• Klicke auf CONVERT\n• Kopiere den neuen Code", "result": "Code bereit für CustomTkinter.", "next": "Ersetze deine alte Datei oder kopiere die Widgets in dein Projekt. Nicht vergessen: pip install customtkinter"},
            "ui_modernizer": {"title": "UI Modernisierer", "what": "Dieses Tool gibt dir moderne, fertige Interface-Teile (Buttons, Farben, Dark Mode...).", "how": "• Wähle eine Option\n• Schau dir die Vorschau an\n• Klicke auf GENERATE CODE", "result": "Moderne Code-Snippets.", "next": "Kopiere die Teile, die dir gefallen, und füge sie in deine __init__-Methode ein."},
            "status_logger": {"title": "Status / Logs Hinzufügen", "what": "Dieses Tool fügt eine Statusleiste oder eine Live-Log-Zone am unteren Rand deines Fensters hinzu.", "how": "• Wähle den Typ\n• Schau dir die Vorschau an\n• Klicke auf GENERATE CODE", "result": "Code für Statusleiste oder Logs.", "next": "Füge das Widget in __init__ und die Funktionen auf derselben Ebene wie __init__ ein."},
            "interface_templates": {"title": "Interface Vorlagen", "what": "Dieses Tool gibt dir komplette, fertige Fenstervorlagen.", "how": "• Wähle eine Vorlage\n• Schau dir die Vorschau an\n• Klicke auf GENERATE FULL CODE", "result": "Ein vollständiger, funktionierender Fenstercode.", "next": "Erstelle eine neue Datei, füge den Code ein und führe ihn aus. Ändere ihn danach nach Wunsch."},
            "pyinstaller_builder": {"title": "PyInstaller Builder", "what": "Dieses Tool erstellt den richtigen Befehl, um dein Python-Programm in eine .exe-Datei umzuwandeln.", "how": "• Wähle deine Optionen (onefile, Icon usw.)\n• Schau dir den Live-Befehl an\n• Klicke auf GENERATE COMMAND", "result": "Ein fertiger PyInstaller-Befehl zum Kopieren.", "next": "Öffne PowerShell in deinem Projektordner, füge den Befehl ein und drücke Enter."},
            "import_cleaner": {"title": "Import Cleaner", "what": "Dieses Tool entfernt ungenutzte Imports und sortiert sie sauber.", "how": "• Füge deinen Code ein\n• Klicke auf CLEAN & SORT IMPORTS\n• Kopiere die bereinigte Version", "result": "Saubere und sortierte Imports.", "next": "Ersetze den Import-Bereich am Anfang deiner Datei durch die neue Version."},
            "icon_adder": {"title": "Icon Adder", "what": "Dieses Tool fügt ein Icon zu deinem Tkinter- oder CustomTkinter-Fenster hinzu.", "how": "• Wähle Tkinter oder CustomTkinter\n• Gib den Icon-Pfad ein\n• Klicke auf GENERATE CODE", "result": "Die richtige iconbitmap-Zeile.", "next": "Füge den Code in deine __init__-Methode ein, direkt nach dem Erstellen des Fensters."},
            "project_doctor": {"title": "Project Doctor", "what": "Dieses Tool prüft dein Projekt auf häufige Probleme (fehlende Dateien, schlechte Einrückung usw.).", "how": "• Wähle deinen Projektordner\n• Klicke auf SCAN PROJECT\n• Optional klicke auf Fix Safe Issues", "result": "Eine Liste der gefundenen Probleme in deinem Projekt.", "next": "Behebe die Probleme manuell oder nutze die automatische Korrektur für sichere Probleme."},
            "scrollable_frame_adder": {"title": "Scrollable Frame Hinzufügen", "what": "Dieses Tool erstellt einen scrollbaren Bereich (sehr nützlich, wenn du viele Widgets hast).", "how": "• Wähle Tkinter oder CustomTkinter\n• Schau dir die Vorschau an\n• Klicke auf GENERATE CODE", "result": "Vollständiger Code für einen scrollbaren Frame.", "next": "Füge den Code in deine __init__ ein und setze deine Widgets in den scrollbaren Frame."},
            "exception_wrapper": {"title": "Exception Wrapper", "what": "Dieses Tool schützt deine Funktionen, damit das Programm nicht abstürzt, wenn ein Fehler auftritt.", "how": "• Wähle den Typ (Konsole oder MessageBox)\n• Gib den Funktionsnamen ein\n• Klicke auf GENERATE CODE", "result": "Ein fertiger try/except-Block.", "next": "Ersetze deinen Funktionsaufruf durch die geschützte Version."},
            "theme_switcher": {"title": "Theme Switcher", "what": "Dieses Tool fügt einen Theme-Umschalter (Dark / Light / System) zu deiner CustomTkinter-App hinzu.", "how": "• Klicke auf GENERATE CODE\n• Kopiere den Code", "result": "Code für ein Theme-Umschaltmenü.", "next": "Füge das Menü in __init__ und die Funktion auf derselben Ebene wie __init__ ein."},
            "release_packager": {"title": "Release Packager", "what": "Dieses Tool erstellt eine saubere ZIP-Datei, die bereit für GitHub Releases ist.", "how": "• Wähle deine .exe-Datei\n• Wähle, ob du README und LICENSE möchtest\n• Klicke auf CREATE RELEASE ZIP", "result": "Eine ZIP-Datei neben deiner .exe.", "next": "Lade die ZIP in den Releases-Bereich deines GitHub-Repositories hoch."},
            "config_file_creator": {"title": "Config-Datei Ersteller", "what": "Dieses Tool erstellt ein einfaches System zum Speichern und Laden von Einstellungen (config.json).", "how": "• Klicke auf GENERATE CODE\n• Kopiere den Code", "result": "Die Funktionen load_config() und save_config() + Beispiel.", "next": "Erstelle eine config.json-Datei und füge die beiden Funktionen in dein Projekt ein."}
        },
        "it": {
            "progress_bar": {"title": "Aggiungi Barra di Progresso", "what": "Questo strumento ti aiuta ad aggiungere una barra di progresso in modo che l'utente veda che il tuo programma sta lavorando.", "how": "• Scegli il tipo (con % o barra che si muove)\n• Guarda l'anteprima\n• Clicca su GENERATE CODE\n• Copia il codice", "result": "Ottieni codice pronto all'uso per una barra di progresso.", "next": "Incolla il codice dentro il metodo __init__ e chiama le funzioni di aggiornamento quando necessario."},
            "indent_fixer": {"title": "Correttore di Indentazione", "what": "Questo strumento corregge la cattiva indentazione del tuo codice Python.", "how": "• Incolla il tuo codice a sinistra\n• Clicca sul pulsante\n• Copia il codice corretto a destra", "result": "Codice pulito e correttamente indentato.", "next": "Sostituisci il tuo vecchio codice con la nuova versione corretta."},
            "tk_to_ctk": {"title": "Convertitore Tkinter → CustomTkinter", "what": "Questo strumento converte codice Tkinter classico in codice CustomTkinter moderno.", "how": "• Incolla il tuo codice Tkinter\n• Clicca su CONVERT\n• Copia il nuovo codice", "result": "Codice pronto per CustomTkinter.", "next": "Sostituisci il tuo vecchio file o copia i widget nel tuo progetto. Non dimenticare: pip install customtkinter"},
            "ui_modernizer": {"title": "Modernizzatore UI", "what": "Questo strumento ti dà pezzi di interfaccia moderni pronti all'uso (pulsanti, colori, dark mode...).", "how": "• Scegli un'opzione\n• Guarda l'anteprima\n• Clicca su GENERATE CODE", "result": "Snippet di codice moderni.", "next": "Copia le parti che ti piacciono e incollale nel metodo __init__."},
            "status_logger": {"title": "Aggiungi Status / Logs", "what": "Questo strumento aggiunge una barra di stato o una zona di log in fondo alla tua finestra.", "how": "• Scegli il tipo\n• Guarda l'anteprima\n• Clicca su GENERATE CODE", "result": "Codice per barra di stato o log.", "next": "Incolla il widget in __init__ e le funzioni allo stesso livello di __init__."},
            "interface_templates": {"title": "Modelli di Interfaccia", "what": "Questo strumento ti dà modelli di finestre completi e pronti all'uso.", "how": "• Scegli un modello\n• Guarda l'anteprima\n• Clicca su GENERATE FULL CODE", "result": "Un codice di finestra completo e funzionante.", "next": "Crea un nuovo file, incolla il codice ed eseguilo. Poi modificalo come vuoi."},
            "pyinstaller_builder": {"title": "Costruttore PyInstaller", "what": "Questo strumento crea il comando corretto per trasformare il tuo programma Python in un file .exe.", "how": "• Scegli le tue opzioni (onefile, icona, ecc.)\n• Guarda il comando in tempo reale\n• Clicca su GENERATE COMMAND", "result": "Un comando PyInstaller pronto da copiare.", "next": "Apri PowerShell nella cartella del progetto, incolla il comando e premi Invio."},
            "import_cleaner": {"title": "Pulitore di Import", "what": "Questo strumento rimuove gli import non utilizzati e li ordina in modo pulito.", "how": "• Incolla il tuo codice\n• Clicca su CLEAN & SORT IMPORTS\n• Copia la versione pulita", "result": "Import puliti e ordinati.", "next": "Sostituisci la sezione degli import all'inizio del file con la nuova versione."},
            "icon_adder": {"title": "Aggiungi Icona", "what": "Questo strumento aggiunge un'icona alla tua finestra Tkinter o CustomTkinter.", "how": "• Scegli Tkinter o CustomTkinter\n• Inserisci il percorso dell'icona\n• Clicca su GENERATE CODE", "result": "La riga corretta di iconbitmap.", "next": "Incolla il codice dentro il metodo __init__, subito dopo la creazione della finestra."},
            "project_doctor": {"title": "Project Doctor", "what": "Questo strumento controlla il tuo progetto alla ricerca di problemi comuni (file mancanti, cattiva indentazione, ecc.).", "how": "• Seleziona la cartella del progetto\n• Clicca su SCAN PROJECT\n• Opzionalmente clicca su Fix Safe Issues", "result": "Una lista dei problemi trovati nel tuo progetto.", "next": "Correggi i problemi manualmente o usa la correzione automatica per quelli sicuri."},
            "scrollable_frame_adder": {"title": "Aggiungi Frame Scrollabile", "what": "Questo strumento crea un'area con scorrimento (molto utile quando hai tanti widget).", "how": "• Scegli Tkinter o CustomTkinter\n• Guarda l'anteprima\n• Clicca su GENERATE CODE", "result": "Codice completo per un frame scrollabile.", "next": "Incolla il codice nel tuo __init__ e metti i tuoi widget dentro il frame scrollabile."},
            "exception_wrapper": {"title": "Wrapper di Eccezione", "what": "Questo strumento protegge le tue funzioni in modo che il programma non vada in crash quando si verifica un errore.", "how": "• Scegli il tipo (console o messagebox)\n• Inserisci il nome della funzione\n• Clicca su GENERATE CODE", "result": "Un blocco try/except pronto all'uso.", "next": "Sostituisci la chiamata alla funzione con la versione protetta."},
            "theme_switcher": {"title": "Cambia Tema", "what": "Questo strumento aggiunge un selettore di tema (Dark / Light / System) alla tua app CustomTkinter.", "how": "• Clicca su GENERATE CODE\n• Copia il codice", "result": "Codice per un menu di cambio tema.", "next": "Incolla il menu in __init__ e la funzione allo stesso livello di __init__."},
            "release_packager": {"title": "Packager di Release", "what": "Questo strumento crea un file ZIP pulito pronto per essere caricato su GitHub Releases.", "how": "• Seleziona il tuo file .exe\n• Scegli se vuoi README e LICENSE\n• Clicca su CREATE RELEASE ZIP", "result": "Un file ZIP accanto al tuo .exe.", "next": "Carica lo ZIP nella sezione Releases del tuo repository GitHub."},
            "config_file_creator": {"title": "Creatore File Config", "what": "Questo strumento crea un sistema semplice per salvare e caricare impostazioni (config.json).", "how": "• Clicca su GENERATE CODE\n• Copia il codice", "result": "Le funzioni load_config() e save_config() + esempio.", "next": "Crea un file config.json e metti le due funzioni nel tuo progetto."}
        },
        "pt": {
            "progress_bar": {"title": "Adicionar Barra de Progresso", "what": "Esta ferramenta ajuda-te a adicionar uma barra de progresso para que o utilizador veja que o teu programa está a trabalhar.", "how": "• Escolhe o tipo (com % ou barra que se move)\n• Olha para a pré-visualização\n• Clica em GENERATE CODE\n• Copia o código", "result": "Obténs código pronto a usar para uma barra de progresso.", "next": "Cola o código dentro do teu método __init__ e chama as funções de atualização quando precisares."},
            "indent_fixer": {"title": "Corretor de Indentação", "what": "Esta ferramenta corrige a má indentação do teu código Python.", "how": "• Cola o teu código à esquerda\n• Clica no botão\n• Copia o código corrigido à direita", "result": "Código limpo e corretamente indentado.", "next": "Substitui o teu código antigo pela nova versão corrigida."},
            "tk_to_ctk": {"title": "Conversor Tkinter → CustomTkinter", "what": "Esta ferramenta converte código Tkinter clássico em código CustomTkinter moderno.", "how": "• Cola o teu código Tkinter\n• Clica em CONVERT\n• Copia o novo código", "result": "Código pronto para CustomTkinter.", "next": "Substitui o teu ficheiro antigo ou copia os widgets para o teu projeto. Não te esqueças: pip install customtkinter"},
            "ui_modernizer": {"title": "Modernizador de UI", "what": "Esta ferramenta dá-te peças modernas de interface prontas a usar (botões, cores, modo escuro...).", "how": "• Escolhe uma opção\n• Olha para a pré-visualização\n• Clica em GENERATE CODE", "result": "Trechos de código modernos.", "next": "Copia as partes de que gostas e cola-as no teu método __init__."},
            "status_logger": {"title": "Adicionar Status / Logs", "what": "Esta ferramenta adiciona uma barra de status ou uma zona de logs na parte inferior da tua janela.", "how": "• Escolhe o tipo\n• Olha para a pré-visualização\n• Clica em GENERATE CODE", "result": "Código para barra de status ou logs.", "next": "Cola o widget em __init__ e as funções no mesmo nível que __init__."},
            "interface_templates": {"title": "Modelos de Interface", "what": "Esta ferramenta dá-te modelos de janelas completos e prontos a usar.", "how": "• Escolhe um modelo\n• Olha para a pré-visualização\n• Clica em GENERATE FULL CODE", "result": "Um código de janela completo e funcional.", "next": "Cria um novo ficheiro, cola o código e executa-o. Depois modifica-o como quiseres."},
            "pyinstaller_builder": {"title": "Construtor PyInstaller", "what": "Esta ferramenta cria o comando correto para transformar o teu programa Python num ficheiro .exe.", "how": "• Escolhe as tuas opções (onefile, ícone, etc.)\n• Olha para o comando em direto\n• Clica em GENERATE COMMAND", "result": "Um comando PyInstaller pronto a copiar.", "next": "Abre o PowerShell na pasta do teu projeto, cola o comando e carrega no Enter."},
            "import_cleaner": {"title": "Limpador de Imports", "what": "Esta ferramenta remove imports não utilizados e ordena-os de forma limpa.", "how": "• Cola o teu código\n• Clica em CLEAN & SORT IMPORTS\n• Copia a versão limpa", "result": "Imports limpos e ordenados.", "next": "Substitui a secção de imports no início do teu ficheiro pela nova versão."},
            "icon_adder": {"title": "Adicionar Ícone", "what": "Esta ferramenta adiciona um ícone à tua janela Tkinter ou CustomTkinter.", "how": "• Escolhe Tkinter ou CustomTkinter\n• Introduz o caminho do ícone\n• Clica em GENERATE CODE", "result": "A linha correta de iconbitmap.", "next": "Cola o código dentro do teu método __init__, logo após criar a janela."},
            "project_doctor": {"title": "Project Doctor", "what": "Esta ferramenta verifica o teu projeto à procura de problemas comuns (ficheiros em falta, má indentação, etc.).", "how": "• Seleciona a pasta do teu projeto\n• Clica em SCAN PROJECT\n• Opcionalmente clica em Fix Safe Issues", "result": "Uma lista de problemas encontrados no teu projeto.", "next": "Corrige os problemas manualmente ou usa a correção automática para os seguros."},
            "scrollable_frame_adder": {"title": "Adicionar Frame Scrollable", "what": "Esta ferramenta cria uma zona com scroll (muito útil quando tens muitos widgets).", "how": "• Escolhe Tkinter ou CustomTkinter\n• Olha para a pré-visualização\n• Clica em GENERATE CODE", "result": "Código completo para um frame scrollable.", "next": "Cola o código no teu __init__ e põe os teus widgets dentro do frame scrollable."},
            "exception_wrapper": {"title": "Wrapper de Exceção", "what": "Esta ferramenta protege as tuas funções para que o programa não falhe quando ocorre um erro.", "how": "• Escolhe o tipo (consola ou messagebox)\n• Introduz o nome da função\n• Clica em GENERATE CODE", "result": "Um bloco try/except pronto a usar.", "next": "Substitui a chamada da tua função pela versão protegida."},
            "theme_switcher": {"title": "Seletor de Tema", "what": "Esta ferramenta adiciona um seletor de tema (Dark / Light / System) à tua aplicação CustomTkinter.", "how": "• Clica em GENERATE CODE\n• Copia o código", "result": "Código para um menu de mudança de tema.", "next": "Cola o menu em __init__ e a função no mesmo nível que __init__."},
            "release_packager": {"title": "Empacotador de Release", "what": "Esta ferramenta cria um ficheiro ZIP limpo pronto para carregar no GitHub Releases.", "how": "• Seleciona o teu ficheiro .exe\n• Escolhe se queres README e LICENSE\n• Clica em CREATE RELEASE ZIP", "result": "Um ficheiro ZIP ao lado do teu .exe.", "next": "Carrega o ZIP na secção Releases do teu repositório GitHub."},
            "config_file_creator": {"title": "Criador de Arquivo Config", "what": "Esta ferramenta cria um sistema simples para guardar e carregar definições (config.json).", "how": "• Clica em GENERATE CODE\n• Copia o código", "result": "As funções load_config() e save_config() + exemplo.", "next": "Cria um ficheiro config.json e põe as duas funções no teu projeto."}
        }
    }

        lang_guides = guides.get(self.current_lang, guides["en"])
        content = lang_guides.get(self.current_tool, {
            "title": self.current_tool.replace("_", " ").title(),
            "what": "Guide not yet available for this tool in this language.",
            "how": "Coming soon.",
            "result": "Coming soon.",
            "next": "Coming soon."
        })

        text = f"""══════════════════════════════════════
{content['title']}
══════════════════════════════════════

{sec['what']}
{content['what']}

{sec['how']}
{content['how']}

{sec['result']}
{content['result']}

{sec['next']}
{content['next']}
        """

        self.content.config(state="normal")
        self.content.delete("1.0", tk.END)
        self.content.insert("1.0", text)
        self.content.config(state="disabled")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = UserGuide(root)
    root.mainloop()