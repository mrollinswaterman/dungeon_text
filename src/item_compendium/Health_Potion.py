#HP Pot
import items, global_commands

class Health_Potion(items.Consumable):

    def __init__(self, rarity):
        super().__init__("Health Potion", rarity)
        import global_variables
        self._unit_weight = 0.5
        self._target = global_variables.PLAYER
        self._type = "Health_Potion"

    def use(self, target=None) -> bool:
        """
        Heals the target for a given amount
        Returns True if the target is not already full HP.
        """
        if not self._target.needs_healing:
            global_commands.type_with_lines("You are already full HP.")
            return False
    
        self.decrease_quantity(1)
        global_commands.type_with_lines(f"{self.id} used. {self._quantity} remaining.")
        self._target.heal(self._strength*2)
        return True
    
def craft(rarity, num=1):
    import global_variables
    hp = Health_Potion(rarity)
    hp.set_quantity(num)
    hp.set_target(global_variables.PLAYER)
    return hp