import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

import os, json

openedFiles = []
openedFilenames = []
SAVE_FILE = "data/save.json"

def removeFileFromNotebook(nbFile):
    global openedFiles
    notebook.delete(nbFile)
    openedFiles.pop(openedFilenames.index(nbFile))
    openedFilenames.pop(openedFilenames.index(nbFile))
    with open(SAVE_FILE, 'r') as f:
        openedFilesJson = json.load(f)
    with open(SAVE_FILE, "w") as f:
        openedFilesJson["openedFiles"] = openedFiles
        json.dump(openedFilesJson, f, indent=1)
    with open(SAVE_FILE, 'r') as f:
        openedFiles = json.load(f)["openedFiles"]
    generateFiles(openedFiles)

def generateFiles(files):
    for file in files:
        try:
            notebook.add(os.path.basename(file))
            textbox = ctk.CTkTextbox(master=notebook.tab(os.path.basename(file)), font=("Roboto", 20),width=400, corner_radius=0)
            openedFilenames.append(os.path.basename(file))
            textbox.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
            with open(file, 'r') as f:
                content = f.read()
            textbox.insert(0.0, text=content)
        except ValueError:
            pass

    notebook.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
    notebook._segmented_button.grid(row=0, column=0, sticky="W")
    xButton = ctk.CTkButton(master=notebook, text="X", width=8, height=8, command= lambda: removeFileFromNotebook(notebook.get()))
    xButton.grid(row=0, column=0,sticky="ne")
    try:
        notebook.set(openedFilenames[-1])
    except:
        pass

def browseFiles():
    global openedFiles
    with open(SAVE_FILE, 'r') as f:
        startingDir = json.load(f)
    filename = filedialog.askopenfilename(initialdir = startingDir["defaultOpenDirectory"],title = "Select a File",filetypes = (("NCF Files","*.NCF*"),("All Files","*.*"))) 
    # Change label contents
    with open(SAVE_FILE, 'r') as f:
        openedFilesJson = json.load(f)
    if filename in openedFilesJson["openedFiles"] or filename.strip() == "":
        return
    with open(SAVE_FILE, "w") as f:
        openedFilesJson["openedFiles"].append(filename)
        openedFilesJson["defaultOpenDirectory"] = os.path.dirname(filename)
        openedFiles = openedFilesJson
        json.dump(openedFilesJson, f, indent=1)
    with open(SAVE_FILE, 'r') as f:
        openedFiles = json.load(f)["openedFiles"]
    generateFiles(openedFiles)
    

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("NCF Editor")
root.geometry("1920x1080")
root.grid_rowconfigure(0, weight=1)  # configure grid system
root.grid_columnconfigure(0, weight=1)

# MENUBAR -------------------------------------------------------------
menubar = tk.Menu(root)
fileMenu = tk.Menu(menubar, tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_command(label="Open", command=browseFiles)
fileMenu.add_command(label="Save")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
transmissionMenu = tk.Menu(menubar, tearoff=0)
transmissionMenu.add_command(label="Send")
helpMenu = tk.Menu(menubar, tearoff=0)
helpMenu.add_command(label="Help Index")
helpMenu.add_command(label="About...")
menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Transmission", menu=transmissionMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
root.config(menu=menubar)
# MENUBAR -------------------------------------------------------------
# ---------------------------------------------------------------------
# FILE EDITOR ---------------------------------------------------------
root.columnconfigure(0, weight=1)
notebook = ctk.CTkTabview(root)
with open(SAVE_FILE, 'r') as f:
    openedFiles = json.load(f)["openedFiles"]
generateFiles(openedFiles)
# FILE EDITOR ---------------------------------------------------------
# ---------------------------------------------------------------------


root.mainloop()
