##Required Modules: globals, items

import items, globals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

INFO = items.Anvil()

INFO.anvil_type = "Health_Potion"

INFO.unit_value = 8

INFO.unit_weight = 1

INFO.quantity = 1

class Health_Potion(items.Consumable):

    def __init__(self, rarity:str | items.Rarity | None = None):
        super().__init__(INFO, "Health Potion", rarity)
        self.anvil.rarity = self.rarity
        self.quantity = 1

    def use(self):
        if self.owner.needs_healing:
            self.owner.heal(max(int(self.owner.level * 1.5), self.rarity.value * 2))
            return True
        else:
            globals.type_text("You are already full HP.")
            return False

object = Health_Potion
