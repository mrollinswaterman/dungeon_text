#Condition class file
from __future__ import annotations
import global_commands
from effects import Effect

class Condition():

    def __init__(self, source, target):
        from game_object import Game_Object
        from item import Item
        self.id = "Condition"
        self.source:Game_Object | Item = source
        self.target:Game_Object = target

        self.active_effects:list[Effect] = []
        self.inactive_effects:list[Effect] = []

        self.start_message:str = ""
        self.end_message:str = ""

    #properties
    @property
    def active(self) -> bool:
        return len(self.active_effects) > 0 or self.duration == 0
    
    @property
    def duration(self) -> int:
        max_dur = 0
        for effect in self.active_effects:
            if effect.duration > max_dur:
                max_dur = effect.duration
        return max_dur

    #methods
    def get(self, ref:str | Effect) -> Effect:
        match ref:
            case Effect():
                ref = ref.__class__.__name__

        for effect in self.active_effects and self.inactive_effects:
            if effect.__class__.__name__ == ref:
                return effect

    def start(self):
        for effect in self.active_effects:
            effect.target = self.target
            effect.source = self.source           
            effect.start()
        global_commands.type_text(self.start_message)
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
        self.active_effects = []
        self.inactive_effects = []
        global_commands.type_text(self.end_message)
    
    def cleanse_check(self) -> bool:
        return False
    
    def additional(self) -> None:
        return None