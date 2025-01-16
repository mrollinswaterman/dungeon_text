import mechanics

class SingleInstanceDamage(mechanics.Instant):

    def __init__(self, source):
        super().__init__(source)

    def start(self) -> int:
        dmg = self.deal_damage(globals.XdY(self.potency))
        return dmg