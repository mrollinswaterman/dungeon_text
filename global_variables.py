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

long_sword = items.Weapon("Long Sword", 1)
long_sword.set_damage_dice((1,8))
long_sword.set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", "Light")
leather_armor.set_armor_value(2)

PLAYER.equip(leather_armor)
PLAYER.equip(long_sword)

PLAYER.gain_gold(300)

SHOPKEEP = shopkeep.Shopkeep()
SHOPKEEP.set_threat(PLAYER.threat)
BLACKSMITH = shopkeep.Blacksmith()

BLACKSMITH.add_to_forge_list(item_compendium.WEAPONS_DICTIONARY)#add weapons to forge list
BLACKSMITH.forge()#randomly generate weapons
SHOPKEEP.restock(BLACKSMITH.items_of_type("WP"), 5)#stock the shop with 5 random weapons from the blacksmith

BLACKSMITH.add_to_forge_list(item_compendium.ARMOR_DICTIONARY)#add armors to forge list
BLACKSMITH.forge()#randomly generate armors
SHOPKEEP.restock(BLACKSMITH.items_of_type("AR"), 3)#stock the shop with 3 random armors from the blacksmith

SHOPKEEP.stock(item_compendium.generate_hp_potions("Common", 5))
SHOPKEEP.stock(item_compendium.generate_repair_kits(5))