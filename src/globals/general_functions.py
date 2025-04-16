from multiprocessing import Value
import time, sys, csv, random
import game
import globals
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import game_objects
    import mechanics

def exit():
    game.RUNNING = False
    save()
    print("")
    sys.exit()

def save():
    globals.type_text("Saving...")
    import items
    import compendiums.item_compendium as item_compendium
    assert game.PLAYER.weapon is not None
    assert game.PLAYER.armor is not None

    player_dict = game.PLAYER.save()
    with open(globals.PLAYER_FILEPATH, "w", newline='') as file:
        file.truncate(0)
        w = csv.DictWriter(file, player_dict.keys())
        w.writeheader()
        w.writerow(player_dict)
        file.close()

    item_saved_list = []

    #append all inventory item_to_dicts to list
    for entry in game.PLAYER.inventory:
        item:items.Item = game.PLAYER.inventory[entry]
        item.save()
        item_saved_list.append(item.saved)

    #append equipped weapon and armor as dicts to the list
    game.PLAYER.weapon.save()
    game.PLAYER.armor.save()
    item_saved_list.append(game.PLAYER.weapon.saved)
    item_saved_list.append(game.PLAYER.armor.saved)

    temp_item:items.Item = globals.craft_item("Health_Potion")
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

    with open(globals.INVENTORY_FILEPATH, "w", newline='') as file:
            file.truncate(0)
            w = csv.DictWriter(file, fieldnames=list(fields))
            w.writeheader()
            w.writerows(item_saved_list)
            file.close()

    print(" Saved!")

def bonus(num:int) -> int:
    return globals.BONUS[num]

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
            current = f"{current} {string}" if j == 0 else f"{current}{' ' * 5}{string}"
        time.sleep(.01)
        i += 1
        print(current)

def d(num):
    """Rolls a dX where X is some number (ie d6, d20, etc)"""
    return random.randrange(1, num+1)

def XdY(damage:str | list | tuple | int, max=False) -> int:
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
    
    if not max: return final
    else:
        return num*dice

def probability(chance):
    return random.random() < (chance / 100)

