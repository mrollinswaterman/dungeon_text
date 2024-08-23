import atomic

class Effect(atomic.Atomic_Effect):

    def __init__(self, target, src):
        super().__init__(target, src)


    def on_hit(self):
        from conditions import On_Fire
        self.methods["deal_damage"](2)

        effect = On_Fire.On_Fire(self.src, self.target)
        effect.set_duration(2)
        effect.set_potency(2)

        self.methods["apply_an_effect"](effect)