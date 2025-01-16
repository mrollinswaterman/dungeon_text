import globals
import mechanics

class Bleeding(mechanics.Status):

    def __init__(self, source):
        super().__init__(source)
        self.source = "the bleeding"

        self._effect = mechanics.StackingDoT(self.source)
        self.effect.duration = 4
        self.effect.potency = "1d4"

        self.save_DC = 10

    @property
    def refresh_msg(self) -> str:
        return f"{self.target.header.ownership} bleeding intensifies."
    
    def update(self):
        if self.target.roll_a_check("con") >= self.save_DC + self.effect.stacks:
            globals.type_text(f"{self.target.header.default} resists {self.source}, taking no damage.")
            self.effect.duration -= 1
            self.effect.stacks -= 2
        else:
            super().update()    

    def refresh(self):
        super().refresh()
        self.effect.stacks += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to stop {self.source}...")
        roll = self.target.roll_a_check("con")
        modifier = max(self.target.bonus("int"), self.target.bonus("wis"))
        if roll + modifier >= self.save_DC:
            globals.type_text(f"Success. {self.source} stops.")
            self.end()
            return True
        else: 
            globals.type_text(f"{self.source} continues.")
            return False

object = Bleeding