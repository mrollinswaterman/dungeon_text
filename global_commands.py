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