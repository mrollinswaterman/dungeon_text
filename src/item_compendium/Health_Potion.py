#HP Pot
import items, global_commands

class Health_Potion(items.Consumable):

    def __init__(self, id="Health_Potion", rarity="Common", quantity=0):
        super().__init__(id, rarity, quantity)
        import global_variables
        self._unit_weight = 0.5
        self._target = global_variables.PLAYER
        self._name = "Health Potion"

    def use(self, target=None) -> bool:
        """
        Heals the target for a given amount
        Returns True if the target is not already full HP.
        """
        #import global_variables
        #self._target = global_variables.PLAYER

        if not self._target.needs_healing:
            global_commands.type_text("You are already full HP.")
            return False
    
        self.decrease_quantity(1)
        global_commands.type_text(f"{self.name} used. {self._quantity} remaining.")
        self._target.heal(self._strength*2)
        return True
    
def craft(rarity, num=1):
    import global_variables
    hp = Health_Potion("Health_Potion", rarity)
    hp.set_quantity(num)
    hp.set_target(global_variables.PLAYER)
    return hp

object = Health_Potion