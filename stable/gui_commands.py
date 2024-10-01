import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def type_text(widget:tk.Widget, text:str, speed:int=85, charIndex=0):
    char = text[charIndex]
    if charIndex == 0 and char.isalpha(): text = text.capitalize()
    if charIndex < len(text)-1:
        waitTime = speed
        #add waitTime time if char is punctuation
        waitTime += 250 if char in end_line else 0
        #add waitTime if char is a "pause char" ie ",", ":", etc
        waitTime += 150 if char in pause_chars else 0
        #add waitTime time for end of text
        waitTime += 50 if charIndex == len(text) else 0

        widget.after(waitTime, type_text, widget, text, speed, charIndex+1)
    # update the text of the label
    widget['text'] = text[:charIndex+1]

def enter_the_dungeon(main):
    clear(main)

def clear(window:tk.Widget):
    for widget in window.winfo_children():
        widget.destroy()