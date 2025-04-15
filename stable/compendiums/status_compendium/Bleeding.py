import globals
import effects

class Bleeding(effects.Status_Effect):
    """
    Deals damage each turn, scaling with how many stacks of bleed the target has. More stacks == more damage

    On refresh, asdd 2 stacks to the target.

    Each turn the target rolls an automatic CON save. On success, the bleed deals no damage this turn
    and it's stacks and duration are reduced. If either hits 0, the status effect is cleansed.

    At max stacks, cleanse all stacks and the target takes massive damage.
    """

    def __init__(self, source):
        super().__init__(source)
        self._header._damage = "the bleeding"

        self._effect = effects.StackingDoT(self)
        self._effect.duration = 4
        self._effect.potency = "1d4"

        self._effects_list = [self._effect]
        self.save_DC = 12

    @property
    def refresh_msg(self) -> str:
        return f"{self.target.header.ownership} bleeding intensifies."
    
    def update(self):
        if self.target.roll_a_check("con") >= self.save_DC + self._effect.stacks:
            globals.type_text(f"{self.target.header.action} able to resist {self._header._damage}, taking no damage.")
            self._effect.duration -= 1
            self._effect.stacks -= 2
            self._effect.check_stacks()
        else:
            super().update()    

    def refresh(self):
        super().refresh()
        self._effect.stacks += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.tries} to stop {self._header._damage}...")
        roll = self.target.roll_a_check("con")
        modifier = max(self.target.bonus("int"), self.target.bonus("wis"))
        if roll + modifier >= self.save_DC:
            globals.type_text(f"Success. {self._header._damage} stops.")
            self.end()
            return True
        else: 
            globals.type_text(f"{self._header._damage} continues.")
            return False

object = Bleeding