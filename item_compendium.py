#item compendium
import items
import player

class Health_Potion(items.Consumable):

    def __init__(self, id, rarity):
        super().__init__(id, rarity)

    def use(self, target: player.Player) -> None:
        """
        Heals the target for a given amount
        """
        if target.hp < target.max_hp:
            self._quantity -= 1
            target.heal(self._strength)
            return True
        
        return False