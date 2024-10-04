import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

winWidth = 1475
winHeight = 900

DEFAULT_SPEED = 50

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

class screenObject():
    width:int
    height:int
    color:str
    frame:tk.Widget
    widgets:dict[str, tk.Widget]
    borderwidth:int

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.frame = None
        self.widgets = {}
        self.borderwidth = 15

class mainWindow(screenObject):
    def __init__(self):
        super().__init__(width=1125, height=600, color="black")

MAIN = mainWindow()

class sidebar(screenObject):
    def __init__(self):
        super().__init__(width=350, height=500, color="#A8422D")

    def createHeader(self):
        headerFont = Font(
                family="Times New Roman",
                size=25,
                underline=True
        )
        header = ttk.Label(
            self.frame, 
            text="Your Actions",
            font=headerFont, 
            background=self.color, 
            foreground="black",
            padding=5
        )
        #header.place(relx=0.5, rely=(20/self.height), anchor=tk.CENTER)
        header.grid(row=0, column=0, columnspan=2)
        self.widgets["Header"] = header

SIDEBAR = sidebar()

class narrator(screenObject):
    def __init__(self):
        super().__init__(width=MAIN.width, height=300, color="#ffe2a0")
        self.textBox = None

NARRATOR = narrator()

def type_text(widget:tk.Widget=None, text:str="",speed:int=DEFAULT_SPEED, charIndex=0, clear:bool=False):
    if widget is None: widget = NARRATOR.textBox
    print(widget)
    char = text[charIndex]
    if charIndex == 0: 
        text = text + " "
        text = list(text)
        text[0] = text[0].upper()
        text = ''.join(text)
    if charIndex < len(text) - 1:
        waitTime = speed
        #add waitTime time if char is punctuation
        waitTime += 250 if char in end_line else 0
        #add waitTime if char is a "pause char" ie ",", ":", etc
        waitTime += 150 if char in pause_chars else 0
        widget.after(waitTime, type_text, widget, text, speed, charIndex+1, clear)
        # update the text of the label
        widget['text'] = text[:charIndex+1]

    if charIndex == len(text) - 1 and clear:
        clear_text(widget, text, int(speed/4))

def clear_text(widget:tk.Label=None, text:str="", speed:int=50):
    if widget is None: widget = NARRATOR.textBox
    if len(text) > 0:
        text = text[:-1]
        widget["text"] = text
        widget.after(speed, clear_text, widget, text, speed)

def createGameUI(window:tk.Widget):
    global NARRATOR, SIDEBAR, MAIN

    mainScreenStyle = ttk.Style()
    mainScreenStyle.configure("main.TFrame", background=MAIN.color, relief="groove", borderwidth=MAIN.borderwidth)

    sideBarStyle = ttk.Style()
    sideBarStyle.configure("sideBar.TFrame", background=SIDEBAR.color, relief="groove", borderwidth=SIDEBAR.borderwidth)

    narratorFrameStyle = ttk.Style()
    narratorFrameStyle.configure("narrator.TFrame", background=NARRATOR.color, relief="groove", borderwidth=NARRATOR.borderwidth)

    mainScreenFrame = ttk.Frame(window, width=MAIN.width, height=MAIN.height, style="main.TFrame")
    sideBarFrame = ttk.Frame(window, width=SIDEBAR.width, height=SIDEBAR.height, style="sideBar.TFrame")
    narratorFrame = ttk.Frame(window, width=NARRATOR.width, height=NARRATOR.height, style="narrator.TFrame")
    narrator = ttk.Label(
        narratorFrame,
        text="textBox", 
        font=("Times New Roman", 25), 
        background=NARRATOR.color, 
        foreground="black",
        padding=5
    )

    MAIN.frame = mainScreenFrame
    SIDEBAR.frame = sideBarFrame
    NARRATOR.frame = narratorFrame
    NARRATOR.textBox = narrator

    mainScreenFrame.grid(row=0, column=0, sticky="nsew")
    narratorFrame.grid(row=1, column=0, sticky="nsew")
    sideBarFrame.grid(row=0, column=1, rowspan=2, sticky="nsew")
    narrator.place(x=15, y=15)

    NARRATOR.widgets["textBox"] = narrator

def clear(window:tk.Widget):
    for widget in window.winfo_children():
        widget.destroy()

def quit(window:tk.Widget):
    window.destroy()
