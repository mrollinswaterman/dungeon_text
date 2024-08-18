#globals variables
from player import Player
from items import Rarity
import item_compendium
from shopkeep import Blacksmith, Shopkeep

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
    20: 5
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

RARITY_DICT = {
    "Common": 1,
    "Uncommon": 2,
    "Rare": 3,
    "Epic": 4,
    "Legendary": 5,
    "Unique": 6 
}

WEIGHT_CLASS = {
    "None": 0,
    "Light": 2,
    "Medium": 4,
    "Heavy": 6,
    "Superheavy": 8
}

#create constants
START_CMD = True
RUNNING = False

SHOPKEEP = Shopkeep()
BLACKSMITH = Blacksmith()
BLACKSMITH.initialize()

starter_weapon = BLACKSMITH.storehouse["Weapon"][0]
starter_armor = BLACKSMITH.storehouse["Armor"][0]

PLAYER.equip(starter_weapon, True)
PLAYER.equip(starter_armor, True)
PLAYER.pick_up(item_compendium.Health_Potion.craft("Common", 5), True)
#PLAYER.pick_up(item_compendium.Firebomb.craft(5), True)

def restock_the_shop():
    """
    Restocks the shop, emptying its inventory before it does so.
    """
    #make sure the shop is up-to-date on player level
    SHOPKEEP.empty_inventory()

    BLACKSMITH.initialize()
    for entry in BLACKSMITH.storehouse:
        SHOPKEEP.restock(BLACKSMITH.storehouse[entry], 5)

    pots = item_compendium.Health_Potion.craft(max(PLAYER.threat // 5, 1), 5)
    SHOPKEEP.stock(pots)
    #scales HP potions to be higher rarity with player level

    #SHOPKEEP.stock(item_compendium.Repair_Kit.craft(5))

def start():
    import tui
    global START_CMD
    START_CMD = True
    tui.begin()

def stop():
    global START_CMD
    START_CMD = False