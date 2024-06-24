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
    ".", "!", ",", "?"
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

def type_with_lines(text:str, num:int=1, speed:float = 0.03, newln=True, delay=True) -> None:
    print("="*110+"\n")
    type_text(text, speed, newln, delay)
    if num > 1:
        print("="*110+"\n")

def error_message(cmd:str="", text:str="") -> None:

    if text == "":
        text = f'Inavlid command "{cmd}". Please try again.'

    lst = text.split(" ")

    for i in lst:
        print(i + " ", end='', flush=True)
        time.sleep(.05)
    
    print("\n")

def type_text(text:str, speed:float=0.03, newln=True, delay=True) -> None:
    """
    Adds "typing" effect to text

    speed: an integer denoting the delay between characters
    """
    if text == "":
        return None

    text = " " + text
    count = 0
    prev = ""

    if delay:
        time.sleep(0.2)

    #if speed is default, adjust it for length, otherwise dont
    match speed: 
        case 0.03:
            if len(text) > 25:
                #print("over 25")
                speed = 0.017
            elif len(text) > 15:
                #print("over 15")
                speed = 0.025
        case _:
            pass



    for idx, char in enumerate(text):
        time.sleep(speed)
        print(char, end='', flush=True)
        count += 1
        if (count >= 120) and char in end_line:
            print("\n")
            count = 0
        
        #wait after punctuation and repeated punctuation (ie "...")
        if char in end_line:
            time.sleep(.1)
            if char == prev:
                time.sleep(.25)

        #wait after end of text
        if idx == len(text):
            time.sleep(0.4)
        
        prev = char

    #newline after typing text
    if newln:
        print("\n")
