from __future__ import annotations
import globals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items

class Mechanic():

    def __init__(self, source:"game_objects.Game_Object | items.Item" | Mechanic):
        self.source = source
        self.id = "Mechanic"

    #properties
    @property
    def target(self) -> "game_objects.Game_Object":
        src_type = globals.get_base_type(self.source)
        match src_type:
            case "Game_Object": return self.source.target
            case "Item": return self.source.owner.target

    @property
    def active(self):
        return True
    
    def update(self):
        return None
    
    def start(self):
        return None
    
    def end(self):
        return None
    
    def __eq__(self, value:Mechanic):
        for entry in self.__dict__:
            if self.__dict__[entry] != value.__dict__[entry]:
                return False
        return True
