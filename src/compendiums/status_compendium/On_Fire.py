from tkinter import ON
import globals
import mechanics

class On_Fire(mechanics.Status):

    def __init__(self, source):
        super().__init__(source)
        self.id = "On Fire"
        self.source = "the fire"

        self._effect = mechanics.DamageOverTime(self.source)
        self.effect.duration = 2
        self.effect.potency = "1d6"

    @property
    def refresh_msg(self) -> str:
        self.switch_word = "still"
        return self.base_msg

    def refresh(self):
        self.effect.duration += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to put out {self.source}...")
        if self.target.roll_a_check("dex") >= self.save_target:
            globals.type_text(f"It worked. {self.source} sputters out.")
            self.end()
            return True
        else: 
            globals.type_text(f"No luck. The flames rage on.")
            return False

object = On_Fire
