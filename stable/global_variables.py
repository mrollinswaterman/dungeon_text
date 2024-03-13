#globals variable
import math
import random
import player
import items
import item_compendium
import shopkeep


START_CMD = True
RUNNING = False

PLAYER = player.Player()

long_sword = items.Weapon("Long Sword", "Common")
long_sword.set_damage_dice((1,8))
long_sword.set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", "Light", "Common")
leather_armor.set_armor_value(2)

print("")#newline for formatting
PLAYER.equip(leather_armor, True)
PLAYER.equip(long_sword, True)

#PLAYER.gain_gold(300, True)
PLAYER.pick_up(item_compendium.generate_hp_potions("Common", 5), True)

SHOPKEEP = shopkeep.Shopkeep()
SHOPKEEP.set_threat(PLAYER.threat)
BLACKSMITH = shopkeep.Blacksmith()

def forge_weapons():
    """
    Adds item compendium weapon list to Blacksmith
    forge list and forges them
    """
    BLACKSMITH.add_to_forge_list(item_compendium.WEAPONS_DICTIONARY)#add weapons to forge list
    BLACKSMITH.forge()#randomly generate weapons

def forge_armors():
    """
    Adds item compendium armor list to Blacksmith
    forge list and forges them
    """
    BLACKSMITH.add_to_forge_list(item_compendium.ARMOR_DICTIONARY)#add armors to forge list
    BLACKSMITH.forge()#randomly generate armors

def restock_the_shop():
    """
    Restocks the shop, emptying its inventory before it does so.
    """
    SHOPKEEP.empty_inventory()

    forge_weapons()
    forge_armors()

    SHOPKEEP.restock(BLACKSMITH.items_of_type("WP"), 5)#stock the shop with 5 random weapons from the blacksmith
    SHOPKEEP.restock(BLACKSMITH.items_of_type("AR"), 3)#stock the shop with 3 random armors from the blacksmith
    SHOPKEEP.stock(item_compendium.generate_hp_potions("Common", 5))
    SHOPKEEP.stock(item_compendium.generate_repair_kits(5))

restock_the_shop()