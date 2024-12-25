import globals
import mechanics

class On_Fire(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = "On Fire"

        #fire = SingleInstanceDamage(self.source)
        #fire.potency = "1d6"

        self.burning = mechanics.DamageOverTime("the fire")
        self.burning.duration = 3
        self.burning.potency = "1d6"

        self.active_effects = [self.burning]

    def refresh(self) -> None:
        self.burning.duration += 2

    def cleanse_check(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to put out the fire...")
        if self.target.roll_a_check("dex") >= 15:
            globals.type_text("It worked. The fire sputters out.")
            self.end()
            return True
        else: 
            globals.type_text(f"No luck. The flames rage on.")
            return False

object = On_Fire
