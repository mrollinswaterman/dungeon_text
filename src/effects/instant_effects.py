import effects

class SingleInstanceDamage(effects.Instant_Effect):

    def __init__(self, source):
        super().__init__(source)

    def start(self) -> int:
        dmg = self.deal_damage(globals.XdY(self.potency))
        self.end()
        return dmg

class Drain(SingleInstanceDamage):

    def __init__(self, source):
        super().__init__(source)

    def start(self):
        dmg = super().start()
        healing = dmg * 0.33
        src_type = globals.get_base_type(self.source)
        match src_type:
            case "Game_Object": self.source.heal(healing)
            case "Item": self.source.owner.heal(healing)
            case "Mechanic": self.source.source.heal(healing)

        self.end()
    
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
