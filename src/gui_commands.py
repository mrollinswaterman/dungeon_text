import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

winWidth = 1475
winHeight = 800
root = tk.Tk()
root.minsize(winWidth, winHeight)

headerFont = Font(
    family="Times New Roman",
    size=42,
    weight="bold",
    slant="italic",
)

root.tk.call('source', 'forest-dark.tcl')
ttk.Style(root).theme_use('forest-dark')

def createStartMenu():
    headerFrame = ttk.Frame(root, width=winWidth, height=winHeight, borderwidth=14)
    headerFrame.grid(row=0, column=0)
    headerText = ttk.Label(headerFrame, text="Would you like to enter the Dungeon?", font=headerFont)
    headerText.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    s = ttk.Style()
    s.configure("start.Accent.TButton", font=("Times New Roman", 20))
    yesButton =  ttk.Button(headerFrame, text="Yes", style="start.Accent.TButton")
    yesButton.place(relx=.25, rely=.5, anchor=tk.CENTER)

    noButton =  ttk.Button(headerFrame, text="No")
    noButton.place(relx=.75, rely=.5, anchor=tk.CENTER)

createStartMenu()
root.mainloop()