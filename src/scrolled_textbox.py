#Scrolled textbox widget custom class file taken from https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/
  
import tkinter as tk 
import tkinter.scrolledtext as st 
  
# Creating tkinter window 
win = tk.Tk() 
win.title("ScrolledText Widget") 
  
# Title Label 
tk.Label(win,  
         text = "ScrolledText Widget Example",  
         font = ("Times New Roman", 15),  
         background = 'green',  
         foreground = "white").grid(column = 0, 
                                    row = 0) 
  
# Creating scrolled text area 
# widget with Read only by 
# disabling the state 
text_area = st.ScrolledText(win, 
                            width = 30,  
                            height = 8,  
                            font = ("Times New Roman", 
                                    15)) 
  
text_area.grid(column = 0, pady = 10, padx = 10) 
  
# Inserting Text which is read only 
def narrate(widget:st.ScrolledText, text, speed=45, charIndex=0):
    if charIndex < len(text):
        widget.after(speed, narrate, widget, text, speed, charIndex+1)
        # update the text of the label
        widget.insert(tk.END, text[charIndex])
        widget.see("end")
    else: 
        widget.configure(state="disabled")

win.after(100, narrate, text_area, f"{"Hello World\nGoodbye World\n"*25}")
win.mainloop()



