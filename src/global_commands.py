import time, sys, csv, random
import global_variables

TAG_TO_STAT = {
    "str": "Strength",
    "dex": "Dexterity",
    "con": "Constitution",
    "int": "Intelligence",
    "wis": "Wisdom",
    "cha": "Charisma",
    "base_evasion": "Evasion",
    "damage_take_multiplier": "Vulnerability",
    "damage_multiplier": "Damage",
    "armor": "Armor",
    "max_hp": "Maximum Health"
}

BONUS = {
    5: -4,
    6: -3,
    7: -2,
    8: -1, 
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5
}

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";"
]

def exit():
    global_variables.RUNNING = False
    save()
    print("")
    sys.exit()

def save():
    import items
    player_dict = global_variables.PLAYER.save_to_dict()
    with open('player.csv', "w", newline='') as file:
        file.truncate(0)
        w = csv.DictWriter(file, player_dict.keys())
        w.writeheader()
        w.writerow(player_dict)
        file.close()

    item_dict_list = []

    #append all inventory item_to_dicts to list
    for entry in global_variables.PLAYER.inventory:
        item:items.Item = global_variables.PLAYER.inventory[entry]
        item.save()
        item_dict_list.append(item.tod)

    #append equipped weapon and armor as dicts to the list
    global_variables.PLAYER.weapon.save()
    global_variables.PLAYER.armor.save()
    item_dict_list.append(global_variables.PLAYER.weapon.tod)
    item_dict_list.append(global_variables.PLAYER.armor.tod)

    #create fieldnames list from item_to_dict keys
    fields = list(global_variables.PLAYER.weapon.tod.keys())
    with open("inventory.csv", "w", newline='') as file:
            file.truncate(0)
            w = csv.DictWriter(file, fieldnames=fields)
            w.writeheader()
            w.writerows(item_dict_list)
            file.close()

def bonus(num:int) -> int:
    return BONUS[num]

def get_cmd():
    cmd = input(">> ").lower()
    print("")
    return cmd

def match(text:str | list | tuple, size:int) -> str | tuple:
    """
    Adds " " to the end of a given string until it is
    the desired length.
    Used for formatting mostly
    """
    if type(text) == str:
        while(len(text) < size):
            text = text + " "
        return text
    else:
        final = []
        for item in text:
            final.append(match(item, size))
        
        return tuple(final)

def generate_item_rarity() -> str:
    """
    Generates item rarity based on player level
    """
    if probability(10+global_variables.PLAYER.level):
        return "Epic"
    
    if probability(15+global_variables.PLAYER.level * 1.25):
        return "Rare"
    
    if probability(33+global_variables.PLAYER.level // 2):
        return "Uncommon"
    
    return "Common"

def d(num):
    """
    Rolls a dX where X is some number (ie d6, d20, etc)
    """
    return random.randrange(1, num+1)

def XdY(damage:str | list | int):
    """
    Rolls X dYs and returns the total (ie 2d4, 3d6, etc)
    """
    ty:str | list | int = type(damage)
    final = 0
    num = None
    dice = None

    if ty == str:
        num = int(damage.split("d")[0])
        dice = int(damage.split("d")[1])

    elif ty == list or ty == tuple:
        num = damage[0]
        dice = damage[1]
    
    elif ty == int:
        num = 1
        dice = damage
    
    else:
        raise ValueError(f"Invalid type '{ty}' for XdY.")

    for _ in range(num):
            final += d(dice)
    return final
    

def probability(chance):
    return random.random() < (chance / 100)

def type_with_lines(text:str=None, num:int=1, speed:float=None, newln=True) -> None:
    print("="*110+"\n")
    type_text(text, speed, newln)
    if num > 1:
        print("="*110+"\n")

def error_message(cmd:str="", text:str=None) -> None:

    text = f'Inavlid command "{cmd}". Please try again.' if text is None else text
    type_text(text)

def type_text(text:str=None, speed:float=None, newln=True) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    if text is None:
        return None

    text = " " + text
    prev = ""

    #typing speed, lower = faster
    speed = 2

    for idx, char in enumerate(text):
        print(char, end='', flush=True)
        waitTime = speed/100

        #add waitTime time if char is punctuation
        waitTime += 0.3 if char in end_line else 0

        #add waitTime if char is a "pause character" ie ",", ":", etc
        waitTime += 0.15 if char in pause_chars else 0

        #add waitTime time for ellipses (...)
        try:
            next = text[idx+1]
        except IndexError:
            next = None
        waitTime += 0.2 if (next == char or char == prev) and char in end_line else 0

        #add waitTime time for end of text
        waitTime += 0.4 if idx == len(text) else 0

        time.sleep(waitTime)

        if idx / 120 >= 1.0 and char in end_line:
            print("\n")
        prev = char

    #newline after typing text
    if newln:
        print("\n")
