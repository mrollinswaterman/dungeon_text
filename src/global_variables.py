#globals variables
from player import Player
from items import Weapon, Armor, numerical_rarity_to_str
from item_compendium import generate_hp_potions, generate_firebombs, generate_repair_kits
from item_compendium import WEAPONS_DICTIONARY, ARMOR_DICTIONARY
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

#create constants
START_CMD = True
RUNNING = False

long_sword = Weapon("Long Sword", "Common")
long_sword.set_damage_dice((1,8))
long_sword.set_crit_multiplier(2)

leather_armor = Armor("Leather Armor", "Light", "Common")
leather_armor.set_armor_value(2)

PLAYER.equip(leather_armor, True)
PLAYER.equip(long_sword, True)

PLAYER.pick_up(generate_hp_potions("Common", 5), True)
PLAYER.pick_up(generate_firebombs(5), True)

SHOPKEEP = Shopkeep()
BLACKSMITH = Blacksmith()

BLACKSMITH.add_to_forge_list(WEAPONS_DICTIONARY)#add weapons to forge list
BLACKSMITH.add_to_forge_list(ARMOR_DICTIONARY)#add armors to forge list

def restock_the_shop():
    """
    Restocks the shop, emptying its inventory before it does so.
    """
    #make sure the shop is up-to-date on player level
    SHOPKEEP.empty_inventory()

    BLACKSMITH.forge()
    for entry in BLACKSMITH.storehouse:
        SHOPKEEP.restock(BLACKSMITH.storehouse[entry], 5)

    threat_str = numerical_rarity_to_str(max(PLAYER.threat // 5, 1))
    pots = generate_hp_potions(threat_str, 5)
    SHOPKEEP.stock(pots)
    #scales HP potions to be higher rarity with player level

    SHOPKEEP.stock(generate_repair_kits(5))

