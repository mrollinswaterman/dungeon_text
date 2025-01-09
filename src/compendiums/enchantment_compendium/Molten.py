import mechanics

class Molten(mechanics.Enchantment):

    def __init__(self, source):
        super().__init__(source)

        heat = mechanics.SingleInstanceDamage(self.source)
        heat.potency = "1d6"

        self.add_active("on_attack", heat)

object = Molten

