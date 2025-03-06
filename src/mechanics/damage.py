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
        super().__init__(source)
        self.source:items.Item | game_objects.Game_Object | mechanics.Mechanic = source
        self._header = self.source.header
        self.amount = amount
        self.id = f"{self.source.id} Damage Instance"
        self.type:DamageType = self.source.damage_type

    @property
    def source_id(self) -> "game_objects.Game_Object":
        base = globals.get_base_type(self.source)
        match base:
            case "Item": return self.source.owner.header.damage
            case "Game_Object": return self.source.header.damage
            case "Mechanic": return self.source.header.damage


class DamageType(mechanics.Mechanic):
    """
    Each Game Object has a Damage Type object associated with it that describes the 
    types of damage it can deal

    The resistances and immunities of each Game Object are also represented by Damage Type objects

    Each Damage Instance object inherits the Damage Type of it's source
    """

    physical = False
    magic = False
    slashing = False
    piercing = False
    bludgeoning = False

    def __init__(self):
        pass

    def set(self, types:list[str]) -> None:
        """
        Sets the damage types of a damage type object

        Takes a list of stirng literals and for each them, if the string is present in the
        object's dictionary, it sets 
        """
        for item in types:
            if item.lower() in self.__dict__:
                self.__dict__[item.lower()] = True

    def unset(self, types:list[str]) -> None:
        """
        Inverse function to self.set, turns all given types to False
        """
        for item in types:
            if item.lower() in self.__dict__:
                self.__dict__[item.lower()] = False

    def __str__(self):
        ret = ""
        return ret
    
    def __eq__(self, value):
        for entry in self.__dict__:
            if self.__dict__[entry] != value.__dict__[entry]:
                return False
        return True