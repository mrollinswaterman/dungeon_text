import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

winWidth = 1475
winHeight = 800

mainFrameW = int(winWidth / 2)
mainFrameH = int(winHeight / 4)

sidebarW = winWidth * 0.25
sidebarH = winHeight * 0.95
sidebarColor = "#A8422D"

narratorFrameW = mainFrameW
narratorFrameH = int(winHeight / 4)
narratorFrameColor = "#ffe2a0"

MAINFRAME = None
NARRATOR = None
SIDEBAR = None

DEFAULT_SPEED = 50

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def type_text(widget:tk.Widget=NARRATOR, text:str="",speed:int=DEFAULT_SPEED, charIndex=0, clear:bool=False):
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
        #widget.after(int(speed * 2), clear_text, widget, text, int(speed/4))

def clear_text(widget:tk.Label, text:str, speed:int=50):
    if len(text) > 0:
        text = text[:-1]
        widget["text"] = text
        widget.after(speed, clear_text, widget, text, speed)

def createGameUI(window:tk.Widget):
    global NARRATOR, SIDEBAR, MAINFRAME

    mainScreenStyle = ttk.Style()
    mainScreenStyle.configure("main.TFrame", background="black", relief="groove", borderwidth=15)

    sideBarStyle = ttk.Style()
    sideBarStyle.configure("sideBar.TFrame", background=sidebarColor, relief="groove", borderwidth=15)

    narratorFrameStyle = ttk.Style()
    narratorFrameStyle.configure("narrator.TFrame", background=narratorFrameColor, relief="groove", borderwidth=15)

    mainScreenFrame = ttk.Frame(window, width=mainFrameW, height=mainFrameH, style="main.TFrame")
    sideBarFrame = ttk.Frame(window, width=sidebarW, height=sidebarH, style="sideBar.TFrame")
    narratorFrame = ttk.Frame(window, width=narratorFrameW, height=narratorFrameH, style="narrator.TFrame")
    narrator = ttk.Label(
        narratorFrame, 
        text="loreum ipsum", 
        font=("Times New Roman", 25), 
        background=narratorFrameColor, 
        foreground="black",
        padding=5
    )

    MAINFRAME = mainScreenFrame
    SIDEBAR = sideBarFrame
    NARRATOR = narrator

    mainScreenFrame.grid(row=0, column=0, columnspan=3, rowspan=1, sticky="nsew")#, pady=(0, winHeight * 0.258)
    sideBarFrame.grid(row=0, column=4, rowspan=1, columnspan= 1, sticky="nsew")#, pady=(winHeight * 0.025, 0)
    narratorFrame.grid(row=1, column=0,columnspan=3, rowspan=1, sticky="nsew")#, pady=(winHeight * 0.695, 0)
    #narrator.grid(row=0, column=0, pady=(15,0), padx=(15,0))

    return True

def createPlayerTurnOptions():
    header = ttk.Label(
        SIDEBAR, 
        text="Your Actions",
        font=("Times New Roman", 25), 
        background=sidebarColor, 
        foreground="black",
        padding=5
    )
    header.grid(row=0, column=0, pady=(15,0), padx=(15,0))


def clear(window:tk.Widget):
    for widget in window.winfo_children():
        widget.destroy()

def quit(window:tk.Widget):
    window.destroy()