import globals
import effects

class Poisoned(effects.Status_Effect):
    """
    Poisons the target, dealing damage every turn. 
    
    Each time damage is dealt, the target makes an automatic 
    constitution check. If they succeed the check, the poison's 
    potency is permanently reduced.

    Example: 1d4 --> 1d3 --> 1d2 --> 1
    """

    def __init__(self, source):
        super().__init__(source)
        self._header._damage = "the poison"
        self._effect = effects.DamageOverTime(self)
        self._effect.duration = 3
        self._effect.potency = "1d4"

        self._effects_list.append(self._effect)
        self.save_DC = 10

    @property
    def refresh_msg(self) -> str:
        return f"{self.id} spreads further through {self.target.header.ownership} system..."
    
    def update(self):
        super().update()
        if self.target.roll_a_check("con") >= self.save_DC + self._effect.max_potency:
            globals.type_text(f"{self.target.header.action} able to resist the posion, reducing it's potency.")
            self._effect.decrease_potency()

    def refresh(self):
        super().refresh()
        self._effect.duration += 2
        if self.target.roll_a_check("con") < self.save_DC + self._effect.max_potency:
            globals.type_text(f"The poison's effect grows more potent...")
            self._effect.increase_potency

    
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
