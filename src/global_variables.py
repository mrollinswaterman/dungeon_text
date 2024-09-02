#globals variables
from player import Player
#import item_compendium
from shopkeep import Armory, Shopkeep, forge_all_items

PLAYER:Player = Player()

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
}

CORE_STATS = {
    "str": "Strength",
    "dex": "Dexterity",
    "con": "Constitution",
    "int": "Intelligence",
    "wis": "Wisdom",
    "cha": "Charisma",
}

STATS = {
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

#create constants
START_CMD = True
RUNNING = False

SHOPKEEP = Shopkeep()
ARMORY = Armory()

forge_all_items()

PLAYER.equip(ARMORY.get("Longsword"), True)
PLAYER.equip(ARMORY.get("Padded Leather"), True)
PLAYER.pick_up(ARMORY.get("Greataxe"), True)
#PLAYER.pick_up(item_compendium.Health_Potion.craft("Common", 5), True)
PLAYER.gain_gold(10000)
#PLAYER.pick_up(item_compendium.Firebomb.craft(5), True)
PLAYER.print_inventory()

def start():
    import tui
    global START_CMD
    START_CMD = True
    tui.begin()

def stop():
    global START_CMD
    START_CMD = False