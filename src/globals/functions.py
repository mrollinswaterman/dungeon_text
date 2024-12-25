from multiprocessing import Value
import time, sys, csv, random
import game
import globals
import items
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    import game_objects
    import mechanics

end_line = [
    ".", "!", "?"
]

pause_chars = [
    ",", ":", ";", "*"
]

def exit():
    game.RUNNING = False
    save()
    print("")
    sys.exit()

def save():
    import compendiums.item_compendium as item_compendium
    assert game.PLAYER.weapon is not None
    assert game.PLAYER.armor is not None

    player_dict = game.PLAYER.save()
    with open('player.csv', "w", newline='') as file:
        file.truncate(0)
        w = csv.DictWriter(file, player_dict.keys())
        w.writeheader()
        w.writerow(player_dict)
        file.close()

    item_saved_list = []

    #append all inventory item_to_dicts to list
    for entry in game.PLAYER.inventory:
        item:"items.Item" = game.PLAYER.inventory[entry]
        item.save()
        item_saved_list.append(item.saved)

    #append equipped weapon and armor as dicts to the list
    game.PLAYER.weapon.save()
    game.PLAYER.armor.save()
    item_saved_list.append(game.PLAYER.weapon.saved)
    item_saved_list.append(game.PLAYER.armor.saved)

    temp_item:"items.Item" = item_compendium.dict["Health_Potion"]("Common")
    temp_item.save()
    #create fieldnames list from item_to_dict keys
    header1 = list(game.PLAYER.weapon.saved.keys())
    header2 = list(game.PLAYER.armor.saved.keys())
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
    return globals.BONUS[num]

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

def get_object_type(obj:Any) -> str:
    import items
    import game_objects
    import mechanics
    
    parent = obj.__class__.__bases__
    final = None

    while parent != str.__class__.__bases__:
        if parent.__class__.__bases__ == str.__class__.__bases__:
            final = parent
            break

        parent = parent.__class__.__bases__

    #print(parent[0].__name__)
    match obj:
        case str(): return "str"
        case int(): return "int"
        case items.Item(): return "item"
        case game_objects.Game_Object(): return "game_object"
        case mechanics.Combat_Trick(): return "combat_trick"
        case mechanics.Enchantment(): return "enchantment"
        case mechanics.Condition(): return "condition"
        case mechanics.Effect(): return "effect"
        case _: raise ValueError("Unrecognized object")

def get_item_type(item:"items.Item") -> str:
    import items
    match item:
        case items.Stackable(): return "stackable"
        case items.Equipment(): return "equipment"
        case items.Item(): return "item"
        case _: raise ValueError("Not an item")

def get_item_subtype(item:"items.Item") -> str:
    import items
    match item:
        case items.Consumable(): return "consumable"
        case items.Weapon(): return "weapon"
        case items.Armor(): return "armor"
        case items.Item(): return "item"
        case _: raise ValueError("Not an item")

def generate_item_rarity():
    """Generates item rarity based on player level"""
    if probability(5+game.PLAYER.level):
        return items.Rarity("Epic")
    
    if probability(10+game.PLAYER.level * 1.25):
        return items.Rarity("Rare")
    
    if probability(25+game.PLAYER.level // 2):
        return items.Rarity("Uncommon")
    
    return items.Rarity("Common")

def create_condition(id:str) -> "mechanics.Condition":
    import compendiums.condition_compendium as conditions

    if id not in conditions.dict:
        raise ValueError(f"No condition named '{id}' found!")
    
    return conditions.dict[id]

def create_item(source_dict={}):
    import compendiums.item_compendium as item_compendium

    cast = items.Anvil()
    cast.copy(source_dict)
    match cast.anvil_type:
        case "Weapon":
            return items.Weapon(cast)
        case "Armor":
            return items.Armor(cast)
        case _:
            pass

    if cast.anvil_type in item_compendium.dict:
        final:items.Stackable = item_compendium.dict[cast.anvil_type](cast.rarity)
    else: final = items.Stackable(cast)

    final.set_quantity(cast.quantity)
    return final

def spawn_mob(name:str) -> "game_objects.Mob":
    """
    Spawn a specific mob by name
    Returns a Mob Object
    """
    import compendiums.monster_manual as monster_manual
    try:
        return monster_manual.dict[name]()
    except KeyError:
        raise ValueError(f"No mob by id '{name}'.")

def spawn_random_mob() -> "game_objects.Mob":
    """
    Spawns a random mob, appropriate for the player's level
    """
    import compendiums.monster_manual as monster_manual
    if game.PLAYER.level >= globals.LEVELCAP:
        raise ValueError("Player level too high!")

    enemy:"game_objects.Mob" = random.choice(list(monster_manual.dict.values()))()

    lower_bound = max(game.PLAYER.level - 2, 1)
    upper_bound = min(game.PLAYER.level + 5, 20)

    base_level = enemy.stats.level_range[0]
    max_level = enemy.stats.level_range[1]

    if max_level > upper_bound or base_level < lower_bound:
        return spawn_random_mob()
    else: return enemy

def spawn_event(name:str):
    import compendiums.event_compendium as event_compendium
    try:
        return event_compendium.dict[name]()
    except KeyError:
        raise ValueError(f"No event by id '{name}'.")

def spawn_random_event():
    import compendiums.event_compendium as event_compendium
    return random.choice(list(event_compendium.dict.values()))()

def d(num):
    """Rolls a dX where X is some number (ie d6, d20, etc)"""
    return random.randrange(1, num+1)

def XdY(damage:str | list | tuple | int):
    """Rolls X dYs and returns the total (ie 2d4, 3d6, etc)
        If passed a single integer, just returns the integer"""

    final = num = dice = 0

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
