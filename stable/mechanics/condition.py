#Condition class file

##Required Module: globals, mechanics
from __future__ import annotations
import globals
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import mechanics
    import game_objects
    import items

class Condition():

    def __init__(self, source:"game_objects.Game_Object | items.Item"):
        self.id = self.__class__.__name__
        self.source:"game_objects.Game_Object | items.Item" = source

        self.active_effects:list["mechanics.Effect"] = []
        self.inactive_effects:list["mechanics.Effect"] = []

        self.start_message:str = ""
        self.refresh_message:str = ""
        self.end_message:str = ""

    #properties
    @property
    def target(self):
        base = globals.get_object_type(self.source)
        match base:
            case "game_object": return self.source.target
            case "item": return self.source.owner.target

    @property
    def active(self) -> bool:
        return len(self.active_effects) > 0
    
    @property
    def duration(self) -> int:
        max_dur = 0
        for effect in self.active_effects:
            if effect.duration > max_dur:
                max_dur = effect.duration
        return max_dur

    #methods
    def get(self, ref:"str | mechanics.Effect") -> "mechanics.Effect | None":
        base = globals.get_object_type(ref)
        match base:
            case "effect":
                ref = ref.__class__.__name__
            case _:
                pass

        for effect in self.active_effects:
            if effect.__class__.__name__ == ref:
                return effect

    def start(self):
        assert self.target is not None
        assert self.source is not None
        self.start_message = f"{self.target.header.action} now {self.id}." if self.start_message == "" else self.start_message
        self.end_message = f"{self.target.header.action} no longer {self.id}." if self.end_message == "" else self.end_message
        globals.type_text(self.start_message)
        for effect in self.active_effects:        
            effect.start()
        for effect in self.active_effects:
            if not effect.active:
                self.active_effects.remove(effect)
                self.inactive_effects.append(effect)

    def update(self):
        for effect in self.active_effects:
            effect.update()
            if not effect.active and effect in self.active_effects:
                effect.end()
                self.active_effects.remove(effect)
                self.inactive_effects.append(effect)
    
    def refresh(self) -> None:
        globals.type_text(self.refresh_message)
        return None
    
    def end(self) -> None:
        globals.type_text(self.end_message)
        for effect in self.active_effects:
            effect.end()
        self.active_effects = []

    def cleanse_check(self) -> bool:
        return False
