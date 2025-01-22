#file for damage class instances and damage types
import globals
from typing import TYPE_CHECKING
from mechanics.mechanic import Mechanic
if TYPE_CHECKING:
    import game_objects
    import items

class DamageInstance(Mechanic):

    def __init__(self, source:"game_objects.Game_Object | items.Item", amount:int):

        self._source = source
        self.amount = amount
        self.type:DamageType = self.source.damage_type

    @property
    def source(self) -> "game_objects.Game_Object":
        base = globals.get_base_type(self._source)
        match base:
            case "Item": return self._source.owner
            case "Game_Object": return self._source

class DamageType(Mechanic):

    def __init__(self):

        self._physical:list[str | bool] = []
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