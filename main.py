import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from PIL import Image

import os, json, importlib
# GETTERS AND SETTERS
def getScripts():
    saveData = getSaveData()
    scripts = os.listdir(saveData["scripts_folder"])
    return scripts
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
def setTitleAndNotebookState():
    try:
        if not FILE_IS_SAVED:
            root.title(f"{WINDOW_TITLE} - *{notebook.get()}")
            notebook.configure(state=tk.DISABLED)
        elif FILE_IS_SAVED:
            root.title(f"{WINDOW_TITLE} - {notebook.get()}")
            notebook.configure(state=tk.NORMAL)
        if notebook.get().strip() == "":
            root.title(f"{WINDOW_TITLE}")
    except Exception as e:
        print(f"Set Title and Notebook State: {e}")

def passThroughScript(choseScript: str, content: str):
    saveData = getSaveData()
    convContent = importlib.import_module("scripts."+choseScript+".script").convertGCodes(content, saveData["scripts_folder"]+choseScript)
    return convContent

# BUTTONS - COMMANDS
def saveOrCancel():
    saveOrCancelWin = tk.Toplevel()
    saveOrCancelWin.title("Save before closing?")
    message = "Are you sure you want to close without saving?"
    def _cancel():
        saveOrCancelWin.destroy()
    def _save():
        saveFile()
        removeFileFromNotebook(notebook.get())
        saveOrCancelWin.destroy()
    def _dontSave():
        global FILE_IS_SAVED
        saveOrCancelWin.destroy()
        FILE_IS_SAVED = True
        removeFileFromNotebook(notebook.get())
    tk.Label(saveOrCancelWin, text=message).grid(row=0, column=0, pady=10, padx=10, columnspan=5)
    tk.Button(saveOrCancelWin, text='Save', command=_save, width=8).grid(row=1, column=1, pady=5, sticky="e")
    tk.Button(saveOrCancelWin, text="Don't Save", command=_dontSave, width=8).grid(row=1, column=2, pady=5, sticky="e")
    tk.Button(saveOrCancelWin, text="Cancel", command=_cancel, width=8).grid(row=1, column=3, pady=5, sticky="e")
    saveOrCancelWin.mainloop()

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
    elif content == origContent and not FILE_IS_SAVED:
        FILE_IS_SAVED = True
    setTitleAndNotebookState()

def removeFileFromNotebook(nbFile):
    saveData = getSaveData()
    if not FILE_IS_SAVED:
        saveOrCancel()
        return
    try:
        notebook.delete(nbFile)
        with open(SAVE_FILE, "w") as f:
            saveData["openFiles"].pop(saveData["openFilenames"].index(nbFile))
            saveData["openFilenames"].pop(saveData["openFilenames"].index(nbFile))
            json.dump(saveData, f, indent=1)
        saveData = getSaveData()
    except Exception as e:
        print(f"File Remover Exception: {e}")
        root.title(f"{WINDOW_TITLE}")
        pass
    generateFiles(saveData["openFiles"])

def generateFiles(files):
    global notebook
    for file in files:
        try:
            notebook.add(os.path.basename(file))
            textbox = ctk.CTkTextbox(master=notebook.tab(os.path.basename(file)), font=("Roboto", 20),width=400, corner_radius=1, undo=True)
            textbox.bind("<KeyRelease>", compareFiles)
            textbox.bind("<Tab>", auto_indent)
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
        print(f"Generate Files Exception: {e}")
        root.title(f"{WINDOW_TITLE}")

def addTab(filename):
    saveData = getSaveData()
    with open(SAVE_FILE, "w") as f:
        saveData["openFiles"].append(filename)
        saveData["openFilenames"].append(os.path.basename(filename))
        saveData["defaultOpenDirectory"] = os.path.dirname(filename)
        json.dump(saveData, f, indent=1)
    saveData = getSaveData()
    generateFiles(saveData["openFiles"])

def browseFiles():
    startDir = getStartDir()
    filename = filedialog.askopenfilename(initialdir = startDir,title = "Select a File",
    defaultextension=".txt",filetypes=[("All Files","*.*"),("NC Output File","*.NCF"),("Text Documents","*.txt")])
    saveData = getSaveData()
    if filename in saveData["openFiles"] or filename.strip() == "":
        return
    addTab(filename)

# EVENTS
def auto_indent(event):
    widget = event.widget
    widget.insert("insert", " "*4)
    return "break"

def newFile():
    with open(TEMP_TEXT_FILE, 'w') as f:  
        f.write("")
    addTab(TEMP_TEXT_FILE)

def saveAsFile():
    global FILE_IS_SAVED
    f = asksaveasfile(initialfile = 'Untitled.txt',
    defaultextension=".txt",filetypes=[("All Files","*.*"),("NC Output File","*.NCF"),("Text Documents","*.txt")])
    FILE_IS_SAVED = True
    try:
        content = getCurrTextboxContent()
        with open(f.name, 'w') as f:
            f.write(content)
    except Exception as e:
        print(e)
        pass
    removeFileFromNotebook(notebook.get())
    addTab(f.name)

def saveFile(e=None):
    global FILE_IS_SAVED
    saveData = getSaveData()
    setTitleAndNotebookState()
    fn = saveData["openFilenames"]
    fp = saveData["openFiles"][fn.index(notebook.get())]
    if TEMP_TEXT_FILE in fp:
        saveAsFile()
        return
    if not FILE_IS_SAVED:
        FILE_IS_SAVED=True
        try:
            content = getCurrTextboxContent()
            with open(fp, 'w') as f:
                f.write(content)
        except Exception as e:
            print(e)
            pass

def onTabChange(e = None):
    setTitleAndNotebookState()


WINDOW_TITLE = "NCF Editor"
SAVE_FILE = "data/save.json"
TEMP_TEXT_FILE = "data/tmp/temp.txt"
FILE_IS_SAVED = True
saveData = getSaveData()
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark" if saveData["darkmode"] else "light")
root = ctk.CTk()
root.title("NCF Editor")
root.geometry("1500x800")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
# ---------------------------------------------------------------------
# MENUBAR -------------------------------------------------------------
menubar = tk.Menu(root)
fileMenu = tk.Menu(menubar, tearoff=0)
fileMenu.add_command(label="New", command=newFile)
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
closeImage = ctk.CTkImage(dark_image=Image.open("data/assets/close.png"), size=(12, 12))
xButton = ctk.CTkButton(master=notebook, text="", image=closeImage, width=7, height=7, command= lambda: removeFileFromNotebook(notebook.get()))
xButton.grid(row=0, column=0,sticky="ne")
generateFiles(saveData["openFiles"])
# FILE EDITOR ---------------------------------------------------------
# ---------------------------------------------------------------------


root.mainloop()
