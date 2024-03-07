import time

def type_text(text: str, speed: int = .03, delay=True) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    if delay is True:
        time.sleep(.2)
    for char in text:
        time.sleep(speed)
        print(char, end='', flush=True)
    print("")

def type_list(text:str, speed:int = .03, delay= True) -> None:

    text = text.split(' ')
    #print(text)
    if delay is True:
        time.sleep(.2)
    for word in text:
        time.sleep(speed)
        print(word + " ", end="", flush=True)
    print("")