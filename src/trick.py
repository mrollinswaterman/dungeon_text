import global_commands
from game_object import Game_Object

class Combat_Trick():

    def __init__(self, parent:Game_Object):
        self.parent = parent
        self.id:str = self.__class__.__name__
        self.duration = 2#every 2 duration is equivalent to 1 round(1 player turn + 1 mob turn = 2)

        self._target = self.parent
        self.activation_text:str = None
        self.deactivation_text:str = None

        self.targets = []

    @property
    def active(self) -> bool:
        return self.duration > 0
    
    def update(self):
        self.duration -= 1
        if not self.active:
            self.deactivate()

    def activate(self):
        global_commands.type_text(self.activation_text)
        self.run_replacement()

    def run_replacement(self):
        for entry in self.targets:
            self._target.__setattr__(entry, self.__getattribute__(entry))

    def deactivate(self):
        self.duration = 0
        global_commands.type_text(self.deactivation_text)
        for entry in self.targets:
            self._target.__setattr__(entry, self.__getattribute__(f"default_{entry}"))
        self.parent.combat_trick = None
