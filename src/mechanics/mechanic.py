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
        src_type = globals.get_object_type(self.source)
        match src_type:
            case "game_object": return self.source.target
            case "item": return self.source.owner.target

    @property
    def active(self):
        return True
    
    def update(self):
        return None
    
    def start(self):
        return None
    
    def end(self):
        return None
