import mechanics
import globals

class Total_Defense(mechanics.Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent, parent)
        self.start_message = f"You shift your focus to defending yourself."
        self.end_message = f"You are no longer fighting defensively."

        self.default_roll_to_hit = self.parent.roll_to_hit
        self.replace_effect.target_list = ["roll_to_hit"]

    def start(self):
        self.parent.spend_ap(0)#indicates full-round action
        super().start()
        increase_evasion = mechanics.ModifyStat(self)
        increase_evasion.stat = "base_evasion"
        increase_evasion.potency = 5 + (self.parent.level // 5)

        defense = mechanics.Condition(self.parent)
        defense.active_effects = [increase_evasion]
        defense.id = "Total Defense"

        self.parent.conditions.add(defense)

    def roll_to_hit(self):
        return self.default_roll_to_hit() - self.parent.bonus("dex")
    
    def end(self):
        super().end()
        globals.type_text(self.end_message)
        self.parent.conditions.cleanse("Total Defense")

object = Total_Defense
