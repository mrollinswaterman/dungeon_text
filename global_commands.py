import time

def type_list(text:str, speed:int = .03, delay=False) -> None:

    text = text.split(' ')
    #print(text)
    if delay is True:
        time.sleep(.2)
    for word in text:
        time.sleep(speed)
        print(word + " ", end="", flush=True)
    print("")


def type_text(text: str, speed: int = .03, delay=True) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    if delay is True:
        time.sleep(.2)

    #print(len(text))
    if len(text) > 30:
        speed = 0.01
    elif len(text) > 20:
        speed = 0.02
    else: 
        speed = 0.03
        
    for char in text:
        time.sleep(speed)
        print(char, end='', flush=True)
    print("")
