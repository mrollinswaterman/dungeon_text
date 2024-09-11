#status effects file
import global_commands

class Effect():

    def __init__(self, source, target=None):
        from game_object import Game_Object
        from condition import Condition

        self.source:Condition = source
        self.target:Game_Object | None = target
        self.duration:int = 0
        self.potency: int | str = 0
        self.stacks:int = 0
    
    #properties
    @property
    def active(self) -> bool:
        return self.duration > 0
    
    #methods
    def set(self, attr:str, num:int) -> None:
        try:
            self.__setattr__(attr, num)
        except KeyError:
            raise ValueError(f"Cannot set non-existent value '{attr}")

    def start(self) -> None:
        return None

    def update(self) -> None:
        self.duration -= 1
        if not self.active:
            self.end()

    def end(self) -> None:
        self.duration = 0
        return None

class SingleInstanceDamage(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)
        self.duration = 1

    def start(self) -> None:
        match self.potency:
            case str():
                damage = global_commands.XdY(self.potency)
            case _:
                damage = self.potency
        self.target.take_damage(damage, self.source)
        self.end()
 
class DamageOverTime(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)

    def update(self) -> None:
        super().update()
        match self.potency:
            case str():
                damage = global_commands.XdY(self.potency)
            case _:
                damage = self.potency
        self.target.take_damage(damage, self.source)

class RampingDamageOverTime(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)
        self.stacks = 1
        self.max_stacks = 10
    
    def update(self) -> None:
        match self.potency:
            case str():
                damage = global_commands.XdY(self.potency)
            case _:
                damage = self.potency

        if self.stacks >= self.max_stacks:
            self.stacks = self.max_stacks
            self.target.take_damage((damage * self.stacks) + self.stacks, self.source)
        else:
            self.target.take_damage(damage * self.stacks, self.source)
            self.stacks -= 1

        if self.stacks <= 0:
            self.end()

        super().update()
    
    def end(self):
        super().end()
        self.stacks = 0
        self.max_stacks = 0

class ModifyStat(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)
        self.stat:str = ""

    def start(self) -> None:
        import global_variables
        try:
            self.target.stats.modify(self.stat, self.potency)
        except KeyError:
            raise ValueError(f"Can't modify non-existent stat '{self.stat}'.")
        text = f"{self.target.ownership_header} {global_variables.STATS[self.stat]} increased by {self.potency}."
        if self.potency < 0:
            text = f"{self.target.ownership_header} {global_variables.STATS[self.stat]} decreased by {abs(self.potency)}."
        global_commands.type_text(text)

    def end(self) -> None:
        import global_variables
        self.target.stats.modify(self.stat, -(self.potency))
        global_commands.type_text(f"{self.target.ownership_header} {global_variables.STATS[self.stat]} returned to normal.")

class GainTempHP(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)

    def start(self) -> None:
        self.target.gain_temp_hp(self.potency)
        self.end()

class Drain(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)

    def start(self) -> None:
        taken = self.target.take_damage(self.potency, self.source)
        self.source.source.heal(taken * 0.33)
        self.end()
