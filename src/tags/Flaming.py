#flaming tag file
import tag
import status_effect
from conditions import On_Fire

class Flaming(tag.Tag):

    def __init__(self, id, src, target):
        super().__init__(id, src, target)
        self._id = "Flaming"

    def apply(self):
        fire:status_effect.Status_Effect = On_Fire(self._src, self._target)
        fire.set_duration(2)
        fire.set_potency(self._rarity.value)
        self._target.add_status_effect(fire)
