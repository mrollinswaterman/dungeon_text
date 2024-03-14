import time
import random

def probability(chance):
    return random.random() < (chance / 100)


def type_with_lines(text:str, num:int=1, speed:int = 0.03, delay=True) -> None:
    print("_"*110+"\n")
    type_text(text, speed, delay)
    if num > 1:
        print("_"*110+"\n")

def print_with_lines(text:str, num:int=1) -> None:
    print("_"*110+"\n")
    print(text)
    if num > 1:
        print("_"*110+"\n")

def type_list(text:str, speed:int = .03, delay=False) -> None:

    text = text.split(' ')
    #print(text)
    if delay is True:
        time.sleep(.2)
    for word in text:
        if word != "" and word != " ":
            time.sleep(speed)
        print(word + " ", end="", flush=True)

def type_text(text: str, speed: int = .03, delay=True) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    if delay is True:
        time.sleep(.2)

    if len(text) > 30:
        speed = 0.01
    elif len(text) > 20:
        speed = 0.02
    else: 
        speed = 0.03
        
    for idx, char in enumerate(text):
        time.sleep(speed)
        print(char, end='', flush=True)
    print("")#newline after typing text
