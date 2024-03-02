#globals variable
import player
import items
import item_compendium
import shopkeep

RUNNING = False

PLAYER = player.Player()

iron_sword = items.Weapon("Iron Sword", 1)
iron_sword.set_damage_dice(1,8)
iron_sword.set_crit_multiplier(2)

leather_armor = items.Armor("Leather Armor", 1)
leather_armor.set_armor_value(2)

PLAYER.equip_armor(leather_armor)
PLAYER.equip_weapon(iron_sword)

PLAYER.pick_up(item_compendium.Health_Potion("Health Potion", 1), 5)

SHOPKEEP = shopkeep.Shopkeep()

SHOPKEEP.stock(item_compendium.Health_Potion("Health Potion", 1, 5))
SHOPKEEP.stock(iron_sword)
#rarity 1, quantity 5