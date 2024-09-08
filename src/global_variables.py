#global variables
from player import Player
from shopkeep import Armory, Shopkeep, forge_all_items
from stackable import Stackable
from item_compendium import Health_Potion

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
    "damage_taken_multiplier": "Vulnerability",
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
hp_pots:Stackable = Health_Potion.object(max(1, PLAYER.level // 4))
hp_pots.set_quantity(5)
PLAYER.pick_up(hp_pots, True)
PLAYER.gain_gold(10000)
#PLAYER.pick_up(item_compendium.Firebomb.craft(5), True)

def start():
    import tui
    global START_CMD
    START_CMD = True
    tui.begin()

def stop():
    global START_CMD
    START_CMD = False