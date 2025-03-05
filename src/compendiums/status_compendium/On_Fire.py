import random
import effects
import globals

class On_Fire(effects.Status_Effect):

    def __init__(self, source):
        super().__init__(source)
        self.id = "On Fire"
        self._header._damage = "the fire"

        self._effect = effects.DamageOverTime(self)
        self._effect.duration = 2
        self._effect.potency = "1d6"

        self._effects_list.append(self._effect)
        self.save_DC = 10

        self.save_messages = [
            f"Success. The flames die down.",
            f"It worked. {self._header.damage} sputters out."
        ]

    @property
    def refresh_msg(self) -> str:
        self.switch_word = "still"
        return self.base_msg

    def refresh(self):
        self._effect.duration += 2
    
    def save_attempt(self) -> bool:
        globals.type_text(f"{self.target.header.tries} to put out {self._header.damage}...")
        if self.target.roll_a_check("dex") >= self.save_DC:
            globals.type_text(random.choice(self.save_messages))
            self.end()
            return True
        else: 
            globals.type_text(f"No luck. The flames rage on.")
            return False

object = On_Fire
