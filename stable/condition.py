#Condition class file
from __future__ import annotations
import global_commands
from effects import Effect

class Condition():

    def __init__(self, source):
        from game_object import Game_Object
        from item import Item
        self.id = self.__class__.__name__
        self.source:Game_Object | Item = source
        self._target:Game_Object | None = None

        self.active_effects:list[Effect] = []
        self.inactive_effects:list[Effect] = []

        self.start_message:str = ""
        self.continue_message:str = ""
        self.end_message:str = ""

    #properties
    @property
    def target(self):
        return self._target

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
    def get(self, ref:str | Effect) -> Effect | None:
        match ref:
            case Effect():
                ref = ref.__class__.__name__
            case _:
                pass

        for effect in self.active_effects:
            if effect.__class__.__name__ == ref:
                return effect

    def start(self):
        assert self._target is not None
        self.start_message = f"{self._target.header.action} now {self.id}." if self.start_message == "" else self.start_message
        self.end_message = f"{self._target.header.action} no longer {self.id}." if self.end_message == "" else self.end_message
        global_commands.type_text(self.start_message)
        for effect in self.active_effects:        
            effect.start()
        for effect in self.active_effects:
            if not effect.active:
                self.active_effects.remove(effect)
                self.inactive_effects.append(effect)

    def update(self):
        for effect in self.active_effects:
            effect.update()
            if not effect.active:
                effect.end()
                self.active_effects.remove(effect)
                self.inactive_effects.append(effect)
    
    def end(self) -> None:
        global_commands.type_text(self.end_message)
        for effect in self.active_effects:
            effect.end()
        self.active_effects = []
        self.inactive_effects = []

    
    def cleanse_check(self) -> bool:
        return False
    
    def additional(self) -> None:
        global_commands.type_text(self.continue_message)
        return None
