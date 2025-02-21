import globals
import effects
import game_objects

class Poisoned(effects.Status_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.header._damage = "the poison"
        self._effect = effects.DecreasingDoT(self.source)
        self._effect.duration = 3
        self._effect.potency = "1d4"

        self.save_DC = 10

    @property
    def refresh_msg(self) -> str:
        return f"{self.id} spreads further through {self.target.header.ownership} system..."
    
    def update(self):
        if self.target.roll_a_check("con") >= self.save_DC + self.effect.duration:
            globals.type_text(f"{self.target.header.default} resists the posion, taking no damage.")
            self.effect.duration -= 1
        else:
            super().update()

    def refresh(self):
        super().refresh()
        self.effect.duration += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to cleanse the poison...")
        if self.target.roll_a_check("con") >= self.save_DC:
            globals.type_text(f"Success. The poison is out of {self.target.header.ownership} system.")
            self.end()
            return True
        else: 
            globals.type_text(f"The poison is still active.")
            return False

object = Poisoned
