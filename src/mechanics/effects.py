##Effects are logical functions that effect gameplay
##For instance, the DamageOverTime effect delas damage to a game_object
##over a set duration

import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items

class Effect(mechanics.Mechanic):

    def __init__(self, source):
        super().__init__(source)
        self.id = f"{self.__class__.__name__} Effect"
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
            raise ValueError(f"Cannot set non-existent value '{attr}'.")

    def update(self) -> None:
        self.duration -= 1
        if not self.active:
            self.end()

    def end(self) -> None:
        self.duration = 0
        return None

class SingleInstanceDamage(Effect):

    def __init__(self, source):
        super().__init__(source)
        self.duration = 1

    def start(self) -> int:
        damage = globals.XdY(self.potency)
        ret = self.target.take_damage(damage, self.source)
        self.end()
        return ret
 
class DamageOverTime(Effect):

    def __init__(self, source):
        super().__init__(source)

    def update(self) -> None:
        super().update()
        damage = globals.XdY(self.potency)
        self.target.take_damage(damage, self.source)

class RampingDoT(Effect):

    def __init__(self, source):
        super().__init__(source)
        self.stacks = 1
        self.max_stacks = 10
    
    def update(self) -> None:
        damage = globals.XdY(self.potency)

        if self.stacks >= self.max_stacks: # at max stacks, deal large amount of damage and cleanse
            self.stacks = self.max_stacks  
            self.target.take_damage((damage * self.stacks) + self.stacks, self.source)
            return self.end()
        else: # damage target, scaling with stacks
            self.target.take_damage(damage * self.stacks, self.source)  
            self.stacks -= 1

        super().update()
    
    def end(self):
        super().end()
        self.stacks = 0

class DecreasingDoT(Effect):

    def __init__(self, source):
        super().__init__(source)
        self.max_potency = self.potency

    def update(self):
        self.potency = self.potency // 2  #halve potency each tick
        self.potency = max(1, self.potency)  #minimum of 1 damage
        self.target.take_damage(self.potency, self.source)  #damage target

class ModifyStat(Effect):

    def __init__(self, source):
        super().__init__(source)
        self.stat:str = ""
        self.duration = 100000

    def start(self) -> None:
        assert self.potency is int()
        try:
            self.target.stats.modify(self.stat, self.potency)
        except KeyError:
            raise ValueError(f"Can't modify non-existent stat '{self.stat}'.")

        polarity = "increased" if self.potency > 0 else "decreased"
        text = f"{self.target.header.ownership} {globals.STATS[self.stat]} {polarity} by {self.potency}."

        globals.type_header(text)

    def end(self) -> None:
        self.target.stats.modify(self.stat, -(self.potency))
        globals.type_header(f"{self.target.header.ownership} {globals.STATS[self.stat]} returned to normal.")

class GainTempHP(Effect):

    def __init__(self, source, target=None):
        super().__init__(source, target)

    def start(self) -> None:
        self.target.gain_temp_hp(self.potency)
        self.end()

class Drain(SingleInstanceDamage):

    def __init__(self, source):
        super().__init__(source)

    def start(self) -> None:
        dmg = super().start()
        healing = dmg * 0.33
        src_type = globals.get_object_type(self.source)
        match src_type:
            case "game_object": self.source.heal(healing)
            case "item": self.source.owner.heal(healing)
            case "enchantment": self.source.source.heal(healing)

        return None

class MethodReplacement(Effect):
    
    def __init__(self, source, target:"game_objects.Game_Object"):
        super().__init__(source)
        self._target = target
        self.duration = 2
        self.target_list = []

    @property
    def target(self):
        return self._target

    def start(self) -> None:
        for entry in self.target_list:
            self.target.__setattr__(entry, self.source.__getattribute__(entry))

    def end(self) -> None:
        super().end()
        for entry in self.target_list:
            self.target.__setattr__(entry, self.source.__getattribute__(f"default_{entry}"))
