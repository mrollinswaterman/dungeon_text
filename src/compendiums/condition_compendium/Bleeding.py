import globals
import mechanics

class Bleeding(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)
        self.max_dice_damage = 6

        self.bleed = mechanics.RampingDoT("the bleeding")
        #bleed.max_stacks = 6
        self.bleed.duration = 4
        self.bleed.potency = "1d4"

        self.active_effects = [self.bleed]

    def start(self):
        super().start()

    def update(self):
        if self.target.roll_a_check("con") >= self.max_dice_damage * self.bleed.stacks:
            globals.type_text(f"{self.target.header.default} resists the bleeding, taking no damage.")
            self.bleed.duration -= 1
        else:
            super().update()

    def refresh(self) -> None:
        self.bleed.stacks += 2
    
    def cleanse_check(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to stop the bleeding...")
        if self.target.roll_a_check("con") >= 15:
            globals.type_text("Success! The bleeding trickles to nothing.")
            self.end()
            return True
        else: 
            globals.type_text(f"{self.target.header.action} failed. The bleed continues.")
            return False

object = Bleeding
