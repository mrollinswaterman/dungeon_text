#Power attack combat trick file
from trick import Combat_Trick
from effects import ModifyStat
from condition import Condition

class Total_Defense(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self.activation_text = f"You shift your focus to defending yourself."

        self._target = self.parent
        self.default_roll_to_hit = self.parent.roll_to_hit
        self.targets = ["roll_to_hit"]

    def activate(self):
        self.parent.spend_ap(0)#indicates full-round action
        super().activate()
        increase_evasion = ModifyStat(self)
        increase_evasion.stat = "base_evasion"
        increase_evasion.potency = 5 + (self.parent.level // 5)

        defense = Condition(self.parent)
        defense.active_effects = [increase_evasion]
        defense.id = "Total Defense"

        self.parent.conditions.add(defense)

    def roll_to_hit(self):
        return self.default_roll_to_hit() - self.parent.bonus("dex")
    
    def deactivate(self):
        super().deactivate()
        self.parent.conditions.cleanse("Total Defense")

object = Total_Defense
