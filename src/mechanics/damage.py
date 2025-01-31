#file for damage class instances and damage types
import game
import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items

class DamageInstance(mechanics.Mechanic):

    def __init__(self, source, amount:int):

        self.source:items.Item | game_objects.Game_Object | mechanics.Mechanic = source
        self.amount = amount
        self.type:DamageType = self.source.damage_type

    @property
    def source_id(self) -> "game_objects.Game_Object":
        base = globals.get_base_type(self.source)
        match base:
            case "Item": return self.source.owner.header.damage
            case "Game_Object": return self.source.header.damage
            case "Mechanic": return self.source.source.header.damage


class DamageType(mechanics.Mechanic):

    def __init__(self):

        self._physical:list[str | bool] = ["Physical"]
        self._magic:list[str | bool] = []

    @property
    def is_physical(self) -> bool:
        return len(self._physical) > 0
    
    @property
    def physical(self) -> list:
        return self._physical

    @property
    def is_magic(self) -> bool:
        return len(self._magic) > 0
    
    @property
    def magic(self) -> list:
        return self._magic
    
    def __str__(self):
        ret = ""
        if self.is_physical:
            ret = "Physical:"
            for entry in self.physical:
                ret = f" {ret} {entry}"
        if self.is_magic:
            ret = ret + '\n' + "Magic:"
            for entry in self.magic:
                ret = f" {ret} {entry}"

        if len(ret) <= 0:
            ret = "None"
        return ret
    
    def __eq__(self, value):
        for entry in self.__dict__:
            if entry not in value.__dict__:
                return False
            if self.__dict__[entry] != value.__dict__[entry]:
                return False
        return True