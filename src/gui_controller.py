import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import gui_commands
import scene_controller

root = tk.Tk()
root.minsize(gui_commands.winWidth, gui_commands.winHeight)
root.maxsize(gui_commands.winWidth, gui_commands.winHeight)

root.tk.call('source', 'forest-dark.tcl')
ttk.Style(root).theme_use('forest-dark')

headerFont = Font(
    family="Times New Roman",
    size=42,
    weight="bold",
    slant="italic"
)

narrationFont = Font(
    family="Times New Roman",
    size=20,
)

def enter_the_dungeon():
    gui_commands.clear(root)
    if gui_commands.createGameUI(root) is True:
        scene_controller.SCENE.begin_encounter()
        #gui_commands.SIDEBAR.createHeader()

#create start menu
headerFrame = ttk.Frame(root, width=gui_commands.winWidth-5, height=gui_commands.winHeight-5, relief="raised")
headerFrame.place(relx=.5, rely=.5, anchor=tk.CENTER)

headerText = ttk.Label(headerFrame, text="lorem ipsum", font=headerFont)
headerText.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

#yes button
yesStyle = ttk.Style()
yesStyle.configure("yes.Accent.TButton", font=("Times New Roman", 25))
yesButton =  ttk.Button(
    headerFrame, 
    text="Yes", 
    style="yes.Accent.TButton", 
    command= lambda: enter_the_dungeon()
)
yesButton.place(relx=.25, rely=.5, anchor=tk.CENTER)

#no button
noStyle = ttk.Style()
noStyle.configure("no.TButton", font=("Times New Roman", 25))
noButton =  ttk.Button(
    headerFrame, 
    text="No", 
    style="no.TButton", 
    command=lambda: gui_commands.quit(root)
)
noButton.place(relx=.75, rely=.5, anchor=tk.CENTER)

root.after(1, gui_commands.type_text, headerText, "Would you like to enter the Dungeon?")
root.mainloop()
