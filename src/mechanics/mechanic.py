from __future__ import annotations
import globals
import game_objects
import items
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import items

class Mechanic():
    """
    desc. needed
    """

    def __init__(self, source):
        self.source:game_objects.Game_Object = source
        self.id = "Mechanic"
        self._target:"game_objects.Game_Object" = None
        self._header = None

    #properties
    @property
    def header(self):
        if not self._header:
            return self.source.header
        else:
            return self._header
    @property
    def target(self) -> game_objects.Game_Object:
        if self._target is not None: return self._target
        src_type = globals.get_base_type(self.source)
        match src_type:
            case "Game_Object": return self.source.target
            case "Item": return self.source.owner.target
    
    def __eq__(self, value:Mechanic):
        for entry in self.__dict__:
            if self.__dict__[entry] != value.__dict__[entry]:
                return False
        return True
