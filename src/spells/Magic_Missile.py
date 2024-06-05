import global_commands, magic

class Magic_Missile(magic.Evocation):

    def __init__(self, caster, id="Magic Missile"):
        super().__init__(caster, id)
        self._damage = "1d4"
        self._auto_hit = True

    @property
    def name(self) -> str:
        import global_variables
        if self.caster == global_variables.PLAYER:
            return f"Your {self._id}s"
        return f"{self.caster.id}'s {self._id}s"
    
    def roll_damage(self):
        dmg = 0
        for _ in range(self.caster.caster_level):
            dmg += (global_commands.XdY(self.damage) + 1)

        return dmg * self.caster.damage_multiplier

