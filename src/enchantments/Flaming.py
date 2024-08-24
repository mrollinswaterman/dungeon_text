import atomic

class Effect(atomic.Atomic_Effect):

    def __init__(self, target, src):
        super().__init__(target, src)
        self.id = "Flaming"

    def on_hit(self):
        from conditions import On_Fire
        fire = On_Fire.Condition(self.src, self.target)
        fire.set_duration(2)
        fire.set_potency(2)
        fire.set_message(f"Your {self.src.id} set the {self.target.id} on fire.")
        self.apply_an_effect(fire)