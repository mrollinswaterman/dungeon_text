import types
import global_commands
from game_object import Game_Object

class Combat_Trick():

    def __init__(self, parent:Game_Object):
        self.parent = parent
        self.id:str = self.__class__.__name__

        self._target = self.parent
        self.activation_text:str = None
        self.deactivation_text:str = None

        self.targets = []

    def activate(self):
        global_commands.type_text(self.activation_text)
        self.run_replacement()

    def run_replacement(self):
        for entry in self.targets:
            self._target.__setattr__(entry, self.__getattribute__(entry))

    def deactivate(self):
        global_commands.type_text(self.deactivation_text)
        for entry in self.targets:
            self._target.__setattr__(entry, self.__getattribute__(f"default_{entry}"))
        self.parent.combat_trick = None
