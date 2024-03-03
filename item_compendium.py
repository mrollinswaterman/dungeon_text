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

WEAPONS_DICTIONARY = [

    ("Battleaxe", ("W"), (1,8, 3)),
    ("Light Flail", ("W"), (1, 8, 2)),
    ("Scimitar", ("W"), (1, 6, 4)),
    ("Trident", ("W"), (1, 10, 2)),
    ("Mace", ("W"), (1, 8, 2)),
    ("Greatsword", ("W"), (2, 6, 2)),
    ("Glaive", ("W"), (1, 10, 3)),
    ("Greataxe", ("W"), (1, 12, 3)),
    ("Scythe", ("W"), (2, 4, 5)),
    ("Halberd", ("W"), (1, 10, 3)),
    ("Lance", ("W"), (1, 8, 2))
]

