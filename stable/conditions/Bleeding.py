import global_commands
from condition import Condition
from effects import RampingDamageOverTime

class Bleeding(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.max_dice_damage = 6

        bleed = RampingDamageOverTime("the bleeding")
        bleed.max_stacks = 6
        bleed.duration = 3
        bleed.potency = "1d6"

        self.active_effects = [bleed]

    def start(self):
        super().start()

    def update(self):
        bleed = self.get("RampingDamageOverTime")
        if self.target.roll_a_check("con") >= self.max_dice_damage * bleed.stacks:
            global_commands.type_text(f"{self.target.header.default} resists the bleeding, taking no damage.")
            bleed.duration -= 1
        else:
            super().update()

    def additional(self) -> None:
        bleed = self.get("RampingDamageOverTime")
        bleed.duration += 2
    
    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.header.action} attempting to stop the bleeding...")
        if self.target.roll_a_check("con") >= 15:
            global_commands.type_text("Success! The bleeding trickles to nothing.")
            self.end()
            return True
        else: 
            global_commands.type_text(f"{self.target.header.action} failed. The bleed continues.")
            return False

object = Bleeding
