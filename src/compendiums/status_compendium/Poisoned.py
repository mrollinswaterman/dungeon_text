import globals
import mechanics

class Poisoned(mechanics.Status):

    def __init__(self, source):
        super().__init__(source)
        self.source = "the poison"

        self._effect = mechanics.DecreasingDoT(self.source)
        self.effect.duration = 3
        self.effect.potency = "1d4"

        self.save_target = 10

    @property
    def refresh_msg(self) -> str:
        return f"{self.id} spreads further through {self.target.header.ownership} system..."
    
    def update(self):
        if self.target.roll_a_check("con") >= self.save_target + self.effect.duration:
            globals.type_text(f"{self.target.header.default} resists the posion, taking no damage.")
            self.effect.duration -= 1
        else:
            super().update()

    def refresh(self):
        super().refresh()
        self.effect.duration += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to cleanse the poison...")
        if self.target.roll_a_check("con") >= self.save_target:
            globals.type_text(f"Success. The poison is out of {self.target.header.ownership} system.")
            self.end()
            return True
        else: 
            globals.type_text(f"The poison is still active.")
            return False

object = Poisoned
