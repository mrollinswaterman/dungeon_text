import time

def type_text(text: str, speed: int = .03) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    time.sleep(.2)
    for char in text:
        time.sleep(speed)
        print(char, end='', flush=True)
    print("")