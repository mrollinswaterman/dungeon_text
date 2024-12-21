import time, sys, csv, random
import global_variables

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
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7
}

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def exit():
    global_variables.RUNNING = False
    save()
    print("")
    sys.exit()

def save():
    from item import Item
    from item_compendium import Health_Potion

    assert global_variables.PLAYER.weapon is not None
    assert global_variables.PLAYER.armor is not None

    player_dict = global_variables.PLAYER.save()
    with open('player.csv', "w", newline='') as file:
        file.truncate(0)
        w = csv.DictWriter(file, player_dict.keys())
        w.writeheader()
        w.writerow(player_dict)
        file.close()

    item_saved_list = []

    #append all inventory item_to_dicts to list
    for entry in global_variables.PLAYER.inventory:
        item:Item = global_variables.PLAYER.inventory[entry]
        item.save()
        item_saved_list.append(item.saved)

    #append equipped weapon and armor as dicts to the list
    global_variables.PLAYER.weapon.save()
    global_variables.PLAYER.armor.save()
    item_saved_list.append(global_variables.PLAYER.weapon.saved)
    item_saved_list.append(global_variables.PLAYER.armor.saved)

    temp_item = Health_Potion.object("Common")
    temp_item.save()
    #create fieldnames list from item_to_dict keys
    header1 = list(global_variables.PLAYER.weapon.saved.keys())
    header2 = list(global_variables.PLAYER.armor.saved.keys())
    header3 = list(temp_item.saved.keys())

    fields = []
    for i in header1: 
        if i not in fields: fields.append(i)
    for i in header2: 
        if i not in fields: fields.append(i)
    for i in header3: 
        if i not in fields: fields.append(i)

    with open("inventory.csv", "w", newline='') as file:
            file.truncate(0)
            w = csv.DictWriter(file, fieldnames=list(fields))
            w.writeheader()
            w.writerows(item_saved_list)
            file.close()

def bonus(num:int) -> int:
    return BONUS[num]

def get_cmd() -> str:
    cmd = input(">> ").lower()
    print("")
    return cmd

def find_max_depth(master:list[list[str]]) -> int:
    mx = len(master[0])
    for i in master:
        if len(i) > mx:
            mx = len(i)
    return mx

def print_line_by_line(master:list[list[str]], max_width:int=35) -> None:
    max_depth = find_max_depth(master)
    i = 0
    #fill all empty list spaces with " " strings
    for lst in master: 
        for x in range(max_depth):
            try:
                error = lst[x]
            except IndexError:
                lst.append(" ")
    while (i < max_depth):
        current = ""
        pieces = []
        for lst in master:
            pieces.append(lst[i])
        for j, string in enumerate(pieces):
            while(len(string) < max_width):
                string = string + " "
            #Adds a tab between each item, except the first
            current = f"{current} {string}" if j == 0 else f"{current}{" " * 5}{string}"
        time.sleep(.01)
        i += 1
        print(current)

def generate_item_rarity():
    """Generates item rarity based on player level"""
    from item import Rarity

    if probability(5+global_variables.PLAYER.level):
        return Rarity("Epic")
    
    if probability(10+global_variables.PLAYER.level * 1.25):
        return Rarity("Rare")
    
    if probability(25+global_variables.PLAYER.level // 2):
        return Rarity("Uncommon")
    
    return Rarity("Common")

def create_item(source_dict={}):
    from item import Anvil
    from equipment import Weapon, Armor
    from stackable import Stackable
    import item_compendium
    cast = Anvil()
    cast.copy(source_dict)
    match cast.anvil_type:
        case "Weapon":
            return Weapon(cast)
        case "Armor":
            return Armor(cast)
        case _:
            pass

    if cast.anvil_type in item_compendium.dict:
        final:Stackable = item_compendium.dict[cast.anvil_type](cast.rarity)
    else: final = Stackable(cast)

    final.set_quantity(cast.quantity)
    return final

def d(num):
    """Rolls a dX where X is some number (ie d6, d20, etc)"""
    return random.randrange(1, num+1)

def XdY(damage:str | list | tuple | int):
    """Rolls X dYs and returns the total (ie 2d4, 3d6, etc)
        If passed a single integer, just returns the integer"""
    final = 0
    num = None
    dice = None

    match damage:
        case str():
            num = int(damage.split("d")[0])
            dice = int(damage.split("d")[1])
        case list() | tuple():
            num, dice = damage
        case int(): return damage
        case _:
            raise ValueError(f"Invalid type '{type(damage)}' for XdY.")

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
        if first and char.isalpha():
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
