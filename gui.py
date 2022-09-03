import threading
import constants
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import theme

window = tk.Tk()
window.title(constants.getVersionText())
window.iconphoto(False, tk.PhotoImage(file=os.path.join(constants.app_path, "Assets", "favicon.png")))
theme.use_dark_theme() 

#Important Elements That Require Interactivity
filePathEntry = None
progressBar = None
statusText = None
#Values Are Flipped, 1 is Off, 0 is On
useMeta = tk.IntVar()

def mainloop():
    window.mainloop()

def space(h):
    tk.Label(height=h, text="").pack()


#Callback Functions
def openFilePicker():
    filetypes = (
        ('Unity Package Files', '*.unitypackage'),
        ('All files', '*.*')
    )

    filename = askopenfilename(filetypes=filetypes)
    filePathEntry.delete(0, tk.END)
    filePathEntry.insert(0, filename)

def extract():
    import extract
    #progressBar.start()

    #Start The Extraction On A Seperate Thread
    thread = threading.Thread(target=extract.extract, args=(filePathEntry.get(), (useMeta.get() == 0), progressBar, statusText))
    thread.start()

#Setup UI Elements
def setup():
    space(1)

    #Array of UI Elements
    elements = []

    #Create Elements
    elements.append(ttk.Label(text=constants.getVersionText(), width=70,anchor="center"))
    elements.append(ttk.Button(text="Select UnityPackage", width=35, command=openFilePicker))

    global filePathEntry
    filePathEntry = ttk.Entry(width=35)
    filePathEntry.insert(0, 'UnityPackage Path')
    elements.append(filePathEntry)

    elements.append(ttk.Checkbutton(text='Extract Meta Files', variable=useMeta, onvalue=0, offvalue=1))
    elements.append(ttk.Button(text="Extract", width=35, command=extract))

    global progressBar
    progressBar = ttk.Progressbar(orient='horizontal', mode='determinate', length=280)
    elements.append(progressBar)

    global statusText
    statusText = ttk.Label(text="Not Initialized", width=70,anchor="center")
    elements.append(statusText)

    #Pack Elements
    for element in elements:
        element.pack()

        #Add Some Spacing With Invisible Labels
        space(constants.ui_spacing)




setup()
mainloop()