import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

import importlib

import os, json
global saveData
WINDOW_TITLE = "NCF Editor"
SAVE_FILE = "data/save.json"
SCRIPTS_FOLDER = "scripts/"
FILE_IS_SAVED = True

choseScript = "Fanuc Lathe"

def getScripts():
    scripts = os.listdir(SCRIPTS_FOLDER)
    return scripts

def passThroughScript(choseScript: str, content: str):
    convContent = importlib.import_module("scripts."+choseScript+".script").convertGCodes(content, SCRIPTS_FOLDER+choseScript)
    return convContent
print(passThroughScript(choseScript, content="GZsmthelx0df0\nG32\nG50\nG80\nGZ\nG50"))

def getSaveData():
    with open(SAVE_FILE, 'r') as f:
        saveData = json.load(f)
    return saveData
def getStartDir():
    with open(SAVE_FILE, 'r') as f:
        startDir = json.load(f)["defaultOpenDirectory"]
    return startDir
def getCurrTextboxContent():
    content = notebook.tab(os.path.basename(notebook.get())).children["!ctktextbox"].get(1.0, tk.END).strip()
    return content


def compareFiles(event:tk.Event=None) -> None:
    global FILE_IS_SAVED
    saveData = getSaveData()
    fn = saveData["openFilenames"]
    fp = saveData["openFiles"][fn.index(notebook.get())]
    content = getCurrTextboxContent()
    with open(fp, 'r') as f:
        origContent = f.read().strip()
    if content != origContent and FILE_IS_SAVED:
        FILE_IS_SAVED = False
        root.title(f"{WINDOW_TITLE} - {notebook.get()}*")
        notebook.configure(state=tk.DISABLED)
    elif content == origContent and not FILE_IS_SAVED:
        FILE_IS_SAVED = True
        notebook.configure(state=tk.NORMAL)
        root.title(f"{WINDOW_TITLE} - {notebook.get()}")
        
def removeFileFromNotebook(nbFile):
    try:
        notebook.delete(nbFile)
        saveData = getSaveData()
        with open(SAVE_FILE, "w") as f:
            saveData["openFiles"].pop(saveData["openFilenames"].index(nbFile))
            saveData["openFilenames"].pop(saveData["openFilenames"].index(nbFile))
            json.dump(saveData, f, indent=1)
        saveData = getSaveData()
    except ValueError:
        pass
    generateFiles(saveData["openFiles"])

def generateFiles(files):
    global notebook
    for file in files:
        try:
            notebook.add(os.path.basename(file))
            textbox = ctk.CTkTextbox(master=notebook.tab(os.path.basename(file)), font=("Roboto", 20),width=400, corner_radius=1, undo=True)
            textbox.bind("<KeyRelease>", compareFiles)
            textbox.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
            with open(file, 'r') as f:
                content = f.read()
            textbox.insert(tk.END, text=content)
        except ValueError:
            pass
    notebook.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
    notebook._segmented_button.grid(row=0, column=0, sticky="W")
    try:
        saveData = getSaveData()
        notebook.set(saveData["openFilenames"][-1])
        onTabChange()
        root.bind("<Button-1>", onTabChange)
    except Exception as e:
        print(e)

def browseFiles():
    startDir = getStartDir()
    filename = filedialog.askopenfilename(initialdir = startDir,title = "Select a File",
    defaultextension=".NCF",filetypes=[("All Files","*.*"),("NC Output File","*.NCF"),("Text Documents","*.txt")])
    saveData = getSaveData()
    if filename in saveData["openFiles"] or filename.strip() == "":
        return
    with open(SAVE_FILE, "w") as f:
        saveData["openFiles"].append(filename)
        saveData["openFilenames"].append(os.path.basename(filename))
        saveData["defaultOpenDirectory"] = os.path.dirname(filename)
        json.dump(saveData, f, indent=1)
    saveData = getSaveData()
    generateFiles(saveData["openFiles"])

def saveAsFile():
    f = asksaveasfile(initialfile = 'Untitled.NCF',
    defaultextension=".NCF",filetypes=[("All Files","*.*"),("NC Output File","*.NCF"),("Text Documents","*.txt")])

def saveFile(e=None):
    global FILE_IS_SAVED
    if not FILE_IS_SAVED:
        FILE_IS_SAVED = True
        root.title(f"{WINDOW_TITLE} - {notebook.get()}")
        notebook.configure(state=tk.NORMAL)
    saveData = getSaveData()
    try:
        fn = saveData["openFilenames"]
        fp = saveData["openFiles"][fn.index(notebook.get())]
        content = getCurrTextboxContent()
        with open(fp, 'w') as f:
            f.write(content)
    except:
        pass

def onTabChange(e = None):
    root.title(f"{WINDOW_TITLE} - {notebook.get()}")

ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("NCF Editor")
root.geometry("1500x800")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
# ---------------------------------------------------------------------
# MENUBAR -------------------------------------------------------------
menubar = tk.Menu(root)
fileMenu = tk.Menu(menubar, tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_command(label="Open", command=browseFiles)
fileMenu.add_command(label="Save", command=saveFile)
root.bind('<Control-s>', saveFile)
fileMenu.add_command(label="Save As...", command=saveAsFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
editMenu = tk.Menu(menubar, tearoff=0)
editMenu.add_command(label="Preferences")
transmissionMenu = tk.Menu(menubar, tearoff=0)
transmissionMenu.add_command(label="Send")
helpMenu = tk.Menu(menubar, tearoff=0)
helpMenu.add_command(label="Help Index")
helpMenu.add_command(label="About...")
menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Edit", menu=editMenu)
menubar.add_cascade(label="Transmission", menu=transmissionMenu)
menubar.add_cascade(label="Help", menu=helpMenu)
root.config(menu=menubar)
# MENUBAR -------------------------------------------------------------
# ---------------------------------------------------------------------
# FILE EDITOR ---------------------------------------------------------
root.columnconfigure(0, weight=1)
notebook = ctk.CTkTabview(root)
xButton = ctk.CTkButton(master=notebook, text="X", width=8, height=8, command= lambda: removeFileFromNotebook(notebook.get()))
xButton.grid(row=0, column=0,sticky="ne")
saveData = getSaveData()
generateFiles(saveData["openFiles"])
# FILE EDITOR ---------------------------------------------------------
# ---------------------------------------------------------------------


root.mainloop()
