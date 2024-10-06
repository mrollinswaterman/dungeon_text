import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import tkinter.scrolledtext as st 

winWidth = 1500
winHeight = 900
bezelWidth = 30

DEFAULT_SPEED = 45

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
    borderWidth:int
    borderType:str

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.frame = None
        self.widgets = {}
        self.borderWidth = 10
        self.borderType = "raised"

class mainWindow(screenObject):
    def __init__(self):
        super().__init__(
            width=int(winWidth * (3/4) - bezelWidth/2), 
            height=int(winHeight * (2/3) - (bezelWidth/2)), 
            color="black"
        )

MAIN = mainWindow()

class sidebar(screenObject):
    def __init__(self):
        super().__init__(
            width=int(winWidth * (1/4) - (bezelWidth/2)), 
            height=int(winHeight - bezelWidth), 
            color="#A8422D"
        )
        self.currentGridPos = (0,0)

    @property
    def nextGridPosition(self) -> tuple[int, int]:
        """Returns the next open spot in the frame's grid. Note that
            calling this property increments the current grid position."""
        nextRow = self.currentGridPos[0] + 1
        nextColumn = self.currentGridPos[1] 
        self.currentGridPos = (nextRow, nextColumn)
        return self.currentGridPos

    def createHeader(self):
        headerFont = Font(
                family="Times New Roman",
                size=30,
                weight="bold"
        )
        header = ttk.Label(
            self.frame, 
            text="Your Actions",
            font=headerFont, 
            background=self.color, 
            foreground="black",
            borderwidth=5,
            padding=5,
            relief="sunken"
        )
        header.grid(row=0, column=0, columnspan=2, padx=int(self.width/4), pady=(self.borderWidth*3, 0))
        self.widgets["header"] = header
        #self.currentGridPos = (0, 1)

    def addButton(self, name:str, cmd) -> None:
        buttonFont = Font(
            family="Times New Roman",
            size="28"
        )
        buttonStyle = ttk.Style()
        buttonStyle.configure("actionButton.TButton", font=buttonFont)
        button = ttk.Button(
            self.frame,
            text=name,
            command=cmd,
            style="actionButton.TButton"
        )
        buttonPos = self.nextGridPosition
        #print(f"Placing button at {buttonPos}\n")
        button.grid(row=buttonPos[0], column=buttonPos[1], columnspan= 2, pady=(35,0))

SIDEBAR = sidebar()

class narrator(screenObject):
    def __init__(self):
        super().__init__(
            width=MAIN.width, 
            height=int(winHeight * (1/3) - (bezelWidth/2)), 
            color="#ffe2a0"
        )
        self.textBox:st.ScrolledText = None
        self.currentText = ""

    def narrate(self, text:str, speed=DEFAULT_SPEED, charIndex=0):
        self.textBox.configure(state="enabled")
        char = text[charIndex]
        if charIndex == 0: 
            text = text + " "
            text = list(text)
            text[0] = text[0].upper()
            text = ''.join(text)
            text = text + "\n\n"
        if charIndex < len(text) - 1:
            waitTime = speed
            #add waitTime time if char is punctuation
            waitTime += 250 if char in end_line else 0
            #add waitTime if char is a "pause char" ie ",", ":", etc
            waitTime += 150 if char in pause_chars else 0
            self.textBox.after(waitTime, self.narrate, self.textBox, text, speed, charIndex+1)
            # update the text of the label
            self.textBox.insert(tk.END, text[charIndex])
            self.textBox.see('end')
        else: self.textBox.configure(state="disabled")

NARRATOR = narrator()

def createGameUI(window:tk.Widget):
    global NARRATOR, SIDEBAR, MAIN

    mainScreenStyle = ttk.Style()
    mainScreenStyle.configure(
        "main.TFrame", 
        background=MAIN.color, 
        relief=MAIN.borderType, 
        borderwidth=MAIN.borderWidth)

    sideBarStyle = ttk.Style()
    sideBarStyle.configure(
        "sideBar.TFrame", 
        background=SIDEBAR.color, 
        relief=SIDEBAR.borderType, 
        borderwidth=SIDEBAR.borderWidth)

    narratorFrameStyle = ttk.Style()
    narratorFrameStyle.configure(
        "narrator.TFrame", 
        background=NARRATOR.color, 
        relief=NARRATOR.borderType, 
        borderwidth=NARRATOR.borderWidth)

    mainScreenFrame = ttk.Frame(window, width=MAIN.width, height=MAIN.height, style="main.TFrame")
    sideBarFrame = ttk.Frame(window, width=SIDEBAR.width, height=SIDEBAR.height, style="sideBar.TFrame")
    narratorFrame = ttk.Frame(window, width=NARRATOR.width, height=NARRATOR.height, style="narrator.TFrame")
    narrator = st.ScrolledText(
        narratorFrame,
        font=("Times New Roman", 25), 
        background=NARRATOR.color, 
        foreground="black",
        padding=5
    )

    MAIN.frame = mainScreenFrame
    SIDEBAR.frame = sideBarFrame
    NARRATOR.frame = narratorFrame
    NARRATOR.textBox = narrator

    mainScreenFrame.grid(row=0, column=0, pady=(bezelWidth/2,0), padx=(bezelWidth/2,0))
    mainScreenFrame.grid_propagate(0)
    narratorFrame.grid(row=1, column=0, padx=(bezelWidth/2,0))
    narratorFrame.grid_propagate(0)
    sideBarFrame.grid(row=0, column=1, rowspan=2, pady=(bezelWidth/2,0))
    sideBarFrame.grid_propagate(0)
    narrator.place(x=15, y=15)

    NARRATOR.widgets["textBox"] = narrator

    return True

def clear(window:tk.Widget):
    for widget in window.winfo_children():
        widget.destroy()

def quit(window:tk.Widget):
    window.destroy()
