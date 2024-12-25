##Required Modules: mechanics, globals
import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects
    import mechanics

class Combat_Trick(mechanics.Mechanic):

    def __init__(self, source, target:"game_objects.Game_Object"):
        super().__init__(source)
        self.id = self.__class__.__name__
        self._target = target

        self.start_message:str = ""
        self.end_message:str = ""

        self.replace_effect = mechanics.MethodReplacement(self, self.target)
    
    @property
    def target(self):
        return self._target

    def update(self) -> None:
        self.replace_effect.update()
        if not self.replace_effect.active:
            self.end()

    def start(self) -> None:
        globals.type_text(self.start_message)
        self.replace_effect.start()

    def end(self) -> None:
        globals.type_text(self.end_message)
        self.replace_effect.end()
        self.source.combat_trick = None
