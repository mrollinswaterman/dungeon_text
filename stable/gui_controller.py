import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import gui_commands

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

#create start menu
headerFrame = ttk.Frame(root, width=winWidth, height=winHeight, borderwidth=14)
headerFrame.grid(row=0, column=0)
headerText = ttk.Label(headerFrame, text="h", font=headerFont)
headerText.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

#yes button
yesStyle = ttk.Style()
yesStyle.configure("yes.Accent.TButton", font=("Times New Roman", 25))
yesButton =  ttk.Button(headerFrame, 
    text="Yes", 
    style="yes.Accent.TButton", 
    command= lambda: gui_commands.enter_the_dungeon(root))

yesButton.place(relx=.25, rely=.5, anchor=tk.CENTER)

#no button
noStyle = ttk.Style()
noStyle.configure("no.TButton", font=("Times New Roman", 25))
noButton =  ttk.Button(headerFrame, text="No", style="no.TButton")
noButton.place(relx=.75, rely=.5, anchor=tk.CENTER)

root.after(1, gui_commands.type_text, headerText, "testing, testing, 1-2, 1-2")
root.mainloop()
