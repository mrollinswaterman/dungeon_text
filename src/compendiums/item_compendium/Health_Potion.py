##Required Modules: globals, items

import items, globals

class Health_Potion(items.Consumable):

    def __init__(self, anvil:items.Anvil=None):
        super().__init__(anvil, "Health_Potion")
        self.quantity = 1

    @property
    def name(self):
        if self.quantity != 1: return "Health Potions"
        return "Health Potion"

    def use(self):
        if not super().use(): return False

        if self.owner.needs_healing:
            self.owner.heal(max(int(self.owner.level * 1.5), self.rarity.value * 3))
            return True
        else:
            globals.type_text("You are already full HP.")
            return False

object = Health_Potion
