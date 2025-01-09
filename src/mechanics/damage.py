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
        self.types:list[str] = []
        for dmg_type in self._source.damage_types:
            self.types.append(dmg_type)

    @property
    def source(self) -> "game_objects.Game_Object":
        base = globals.get_base_type(self._source)
        match base:
            case "Item": return self._source.owner
            case "Game_Object": return self._source