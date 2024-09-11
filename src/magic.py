import global_commands
import player,mob

class Spell():
    """
    Base spell class. Every spell has a caster and
    and ID. A spell's narration text changes based on if the spell's
    caster is the player or not
    """

    def __init__(self, caster:player.Player | mob.Mob, id:str, code:str):
        import global_variables
        self._id = id
        self._caster = caster
        self.code = code
        self._min_level = 1

        #determines if the caster is the player
        self.player = True if self._caster == global_variables.PLAYER else False

        #stats
        self._mp_cost = 1

    @property
    def caster(self):
        return self._caster
    @property
    def name(self):
        if self.player:
            return f"Your {self._id}"
        return f"{self.caster.id}'s {self._id}"
    @property
    def id(self) -> str:
        return self._id
    @property
    def min_level(self) -> int:
        return self._min_level
    @property
    def mp_cost(self) -> int:
        return self._mp_cost
    @property
    def damage_header(self) -> str:
        return self.name

    def cast(self, target:player.Player | mob.Mob):
        if self.player:
            global_commands.type_text(f"You cast {self.id}.")
        else:
            global_commands.type_text(f"The {self.caster.id} casts {self.id}.")
        self._caster.spend_mp(self._mp_cost)


class Evocation(Spell):
    """
    Evocation spells do damage, and some hit automatically
    """
    def __init__(self, caster:player.Player | mob.Mob, id):
        super().__init__(caster, id)

        self._damage = "1d6"
        self._auto_hit = False

    @property
    def damage(self) -> str | int:
        return self._damage
    @property
    def auto_hit(self) -> bool:
        return self._auto_hit
    
    def roll_damage(self):
        return (global_commands.XdY(self._damage) + self.caster.bonus("int")) * self.caster.damage_multiplier
    
    def cast(self, target:player.Player | mob.Mob):
        super().cast(target)

        if self._auto_hit:
            global_commands.type_text("It hit.")
            taken = target.take_damage((self.roll_damage()), self)
            return None

        roll = self.caster.roll_attack()
        self.caster.stats["damage_multiplier"] += 1 if roll == 0 else 0
        if roll >= target.evasion() - target.bonus("dex") or roll == 0:
            if self.player:
                global_commands.type_text(f"Your spell hit the {target.id}")
            else:
                global_commands.type_text(f"The {self.name} hit you.")
            taken = target.take_damage(self.roll_damage(), self)
            self.caster.stats["damage_multiplier"] -= 1 if roll == 0 else 0
        return None

class Enchantment(Spell):
    """
    Enchantment spells are debuff spells, they reduce enemy stats
    or defenses
    """

class Transmutation(Spell):
    """
    Transmutation spells are self-buff spells, they enchance the caster's stats
    or defenses
    """

class Abjuration(Spell):
    """
    Abjuration is the anti-magic class of spells. They reduce the effectivness of 
    other spells or negate them entirely.
    """