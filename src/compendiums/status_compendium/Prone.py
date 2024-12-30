import globals
import mechanics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game_objects

class Prone(mechanics.Status):

    def __init__(self, source):
        super().__init__(source)

        self._effect:mechanics.Effect = mechanics.ModifyStat(self.source)
        self.effect.stat = "dex"
        self.effect.potency = int(-self.target.stats[self.stat] // 2)

    def save_attempt(self):
        self.end()

object = Prone


