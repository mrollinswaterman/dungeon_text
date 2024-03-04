#item compendium
import items
import player

class Health_Potion(items.Consumable):

    def __init__(self, id, rarity, quantity=0):
        super().__init__(id, rarity, quantity=0)

    def use(self, target: player.Player) -> None:
        """
        Heals the target for a given amount
        """
        if target.hp < target.max_hp:
            self._quantity -= 1
            target.heal(self._strength)
            return True
        return False

#tag, id, (num dice, dice type, crit)
WEAPONS_DICTIONARY = [

    (("WP"), "Battleaxe", "1d8,x2"),
    (("WP"), "Light Flail", "1d8,x2"),
    (("WP"), "Scimitar", "1d6,x4"),
    (("WP"), "Trident", "1d10,x2"),
    (("WP"), "Mace", "1d8,x2"),
    (("WP"), "Greatsword", "2d6,x2"),
    (("WP"), "Glaive", "1d10,x3"),
    (("WP"), "Greataxe", "1d12,x3"),
    (("WP"), "Scythe", "2d4,x5"),
    (("WP"), "Halberd", "1d10,x3"),
    (("WP"), "Lance", "1d8,x2")
]

ARMOR_DICTIONARY = [
    (("AR"), "Studded Leather", ("Light")),
    (("AR"), "Haramaki", ("Light")),
    (("AR"), "Chain Shirt", ("Light")),
    (("AR"), "Breastplate", ("Medium")),
    (("AR"), "Chainmail", ("Medium")),
    (("AR"), "Armored Coat", ("Medium")),
    (("AR"), "Scale Mail", ("Medium")),
    (("AR"), "Half-plate", ("Heavy")),
    (("AR"), "Stoneplate", ("Heavy")),
    (("AR"), "Branded Mail", ("Heavy")),
    (("AR"), "Full-plate", ("Heavy")),
]
