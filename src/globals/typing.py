#Typing file

import time
from tkinter.tix import TEXT

text_box = ""
typing_speed = 3

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def get_TEXTBOX():
    global text_box
    return text_box

def set_SPEED(num=None):
    global typing_speed
    if num is None: return typing_speed
    typing_speed = num
    return typing_speed

def error_message(cmd:str="", text:str=None) -> None:
    text = f'Inavlid command "{cmd}". Please try again.' if text is None else text
    type_text(text)

def under_construction():
    text = f'That function is currently unavailable!'
    print(text)
    print()

def type_with_lines(text:str=None, num:int=1, speed:float=None, newln=True) -> None:
    print("="*110+"\n")
    type_text(text, speed, newln)
    if num > 1:
        print("="*110+"\n")

def type_header(text:str=None, speed:float=None, newln:bool=True) -> None:
    type_text(text, 1, newln)

def type_header_with_lines(text=None, num=1, speed=None, newln=True) -> None:
    type_with_lines(text, num, 1, newln)

def type_text(text:str=None, speed:float=None, newln=True) -> None:
    import tests
    global text_box
    """Adds a typing effect to text"""
    if text is None or text == "":
        return None
    
    text_box = text

    #tracks if the first letter of text has been made uppercase
    first = True
    text = " " + text + " "

    #typing speed, lower = faster
    if speed is None: speed = set_SPEED()
    for idx, char in enumerate(text):

        if first and char.isalpha():  # if first char is a letter, capitalize it
            char = char.upper()
            first = False

        if text[idx-2] == "." and char.isalpha():
            char = char.upper()

        print(char, end='', flush=True)
        waitTime = speed

        #add waitTime time if char is punctuation
        waitTime += 45 if char in end_line else 0
        #add waitTime if char is a "pause character" ie ",", ":", etc
        waitTime += 35 if char in pause_chars else 0
        #add waitTime time for end of text
        waitTime += 65 if idx == len(text) else 0

        time.sleep(waitTime/100)
        if idx / 120 >= 1.0 and char in end_line:
            print("\n")

    #newline after typing text
    if newln:
        print("\n")