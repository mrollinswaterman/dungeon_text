import mechanics

class Molten(mechanics.Enchantment):

    def __init__(self, parent):
        super().__init__(parent)

        self.molten:mechanics.Effect = mechanics.SingleInstanceDamage(self)
        self.molten.potency = 4

        self.heat:mechanics.Effect = mechanics.DamageOverTime(self)
        self.heat