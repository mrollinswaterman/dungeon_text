import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

winWidth = 1475
winHeight = 800

NARRATION_LABEL = None

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def type_text(widget:tk.Widget, text:str, speed:int=50, charIndex=0):
    char = text[charIndex]
    if charIndex == 0 and char.isalpha(): 
        text = list(text)
        text[0] = text[0].upper()
        text = ''.join(text)
    if charIndex < len(text)-1:
        waitTime = speed
        #add waitTime time if char is punctuation
        waitTime += 250 if char in end_line else 0
        #add waitTime if char is a "pause char" ie ",", ":", etc
        waitTime += 150 if char in pause_chars else 0
        #add waitTime time for end of text
        #waitTime += 50 if charIndex == len(text) else 0

        widget.after(waitTime, type_text, widget, text, speed, charIndex+1)
    # update the text of the label
    widget['text'] = text[:charIndex+1]

def createGameUI(main):
    #import gui_controller
    global NARRATION_LABEL
    sideBarStyle = ttk.Style()
    sideBarStyle.configure("sideBar.TFrame", background="#808080", relief="ridge", borderwidth=15)

    mainScreenStyle = ttk.Style()
    mainScreenStyle.configure("main.TFrame", background="black", relief="ridge", borderwidth=15)

    narratorStyle = ttk.Style()
    narratorStyle.configure("narrator.TFrame", background = "#D3D3D3", relief="ridge", borderwidth=15)

    mainScreenFrame = ttk.Frame(main, width=winWidth * 0.75, height=winHeight * 0.6666, style = "main.TFrame")
    sideBarFrame = ttk.Frame(main, width=winWidth * 0.25, height=winHeight * 0.95, style="sideBar.TFrame")
    narratorFrame = ttk.Frame(main, width=winWidth * 0.75, height=winHeight * 0.28, style="narrator.TFrame")
    
    narrator = ttk.Label(narratorFrame, text="loreum ipsum", font=("Times New Roman", 25))
    NARRATION_LABEL = narrator

    mainScreenFrame.grid(row=0, column=0, columnspan=3, pady=(0, winHeight * 0.258))
    sideBarFrame.grid(row=0, column=4, pady=(winHeight * 0.025, 0))
    narratorFrame.grid(row=0, column=0, sticky="nsew", columnspan=3, pady=(winHeight * 0.695, 0))
    narrator.grid(row=0, column=0, pady=(15,0), padx=(15,0))

    return True


def clear(window:tk.Widget):
    for widget in window.winfo_children():
        widget.destroy()

def quit(main:tk.Widget):
    main.destroy()