import atomic

class Effect(atomic.Atomic_Effect):

    def __init__(self, target, src):
        super().__init__(target, src)
        self.id = "Flaming"

    def on_hit(self):
        from conditions import On_Fire

        self.deal_damage(2)

        fire = On_Fire.Condition(self.src, self.target)
        fire.set_duration(2)
        fire.set_potency(2)
        self.apply_an_effect(fire)