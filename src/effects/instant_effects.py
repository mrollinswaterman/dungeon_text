import effects

class SingleInstanceDamage(effects.Instant_Effect):

    def __init__(self, source):
        super().__init__(source)

    def start(self) -> int:
        dmg = self.deal_damage(globals.XdY(self.potency))
        self.end()
        return dmg
    
class Heal(effects.Instant_Effect):
    def __init__(self, source, target=None):
        super().__init__(source, target)

    def start(self):
        self.target.heal(self.potency)
        self.end()
    
class GainTempHP(effects.Instant_Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)

    def start(self):
        self.target.gain_temp_hp(self.potency)
        self.end()
