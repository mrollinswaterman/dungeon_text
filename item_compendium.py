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

WEAPONS_DICTIONARY = {
    ("Battleaxe", (1,8), 3),
    ("Light Flail", (1, 8), 2),
    ("Scimitar", (1, 6), 4),
    ("Trident", (1, 10), 2),
    ("Mace", (1, 8), 2),
    ("Greatsword", (2, 6), 2),
    ("Glaive", (1, 10), 3),
    ("Greataxe", (1, 12), 3),
    ("Scythe", (2, 4), 5),
    ("Halberd", (1, 10), 3),
    ("Lance", (1, 8), 2)
}

