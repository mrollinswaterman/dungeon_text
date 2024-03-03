#globals variable
import math
import random
import player
import items
import item_compendium
import shopkeep

RUNNING = False

PLAYER = player.Player()

long_sword = items.Weapon("Long Sword", 1)
long_sword.set_damage_dice((1,8))
long_sword.set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", 1)
leather_armor.set_armor_value(2)

PLAYER.equip_armor(leather_armor)
PLAYER.equip_weapon(long_sword)

#PLAYER.pick_up(item_compendium.Health_Potion("Health Potion", 1), 5)

SHOPKEEP = shopkeep.Shopkeep()
SHOPKEEP.set_threat(PLAYER.threat)

SHOPKEEP.restock(item_compendium.WEAPONS_DICTIONARY, 5)