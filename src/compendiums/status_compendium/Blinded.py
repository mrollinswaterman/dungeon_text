import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class Blinded(mechanics.Status):

    def __init__(self, source, target:"game_objects.Game_Object"=None):
        super().__init__(source)
        self.miss_chance = 50
        self._target = target

        self.default = self.target.attack

        self._effect:mechanics.MethodReplacement = mechanics.MethodReplacement(self, self.target)
        self.effect.replacement_target = "attack"

    @property
    def target(self):
        return self._target if self._target is None else super().target

    def replacement_method(self):
        if globals.probability(self.miss_chance):
            return self.default()
        else:
            self.target.spend_ap()
            globals.type_text(f"{self.target.header.default} missed due to Blindness!")

object = Blinded