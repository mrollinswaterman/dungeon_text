#Typing file

import time

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def error_message(cmd:str="", text:str=None) -> None:
    text = f'Inavlid command "{cmd}". Please try again.' if text is None else text
    type_text(text)

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
    """Adds a typing effect to text"""
    if text is None or text == "":
        return None

    #tracks if the first letter of text has been made uppercase
    first = True
    text = " " + text + " "

    #typing speed, lower = faster
    if speed is None: speed = 3
    for idx, char in enumerate(text):

        if first and char.isalpha():  # if first char is a letter, capitalize it
            char = char.upper()
            first = False

        print(char, end='', flush=True)
        waitTime = speed

        #add waitTime time if char is punctuation
        waitTime += 30 if char in end_line else 0
        #add waitTime if char is a "pause character" ie ",", ":", etc
        waitTime += 20 if char in pause_chars else 0
        #add waitTime time for end of text
        waitTime += 50 if idx == len(text) else 0

        time.sleep(waitTime/100)
        if idx / 120 >= 1.0 and char in end_line:
            print("\n")

    #newline after typing text
    if newln:
        print("\n")