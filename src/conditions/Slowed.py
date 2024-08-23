#Vulnerable condition
import status_effect 
from src.conditions import Stat_Buff

class Slowed(Stat_Buff.Stat_Buff):
    """
    Slow the target, reducing their max AP for a period of time.
    Often applied from ice attacks
    """
    def __init__(self, src, target=None, id="Slowed"):
        super().__init__(src, target, id)
        import global_variables
        self._target = global_variables.PLAYER if target is None else self._target
        self._target_header = "You are"
        if self._target != global_variables.PLAYER:
            self._target_header = f"The {self._target.id} is "

        self._message = f"{self._target_header} now {self._id}."

        if target == src and self._target != global_variables.PLAYER:
            self._message = f"The {self._target.id} made itself {self._id}"
        elif target == src:
            self._message = f"You made yourself {self._id}"

        self._cleanse_message = f"{self._target_header} no longer {self._id}."
        self._stat = "max_ap"

    def update_message(self):
        pass

    def additional_effect(self, effect: status_effect.Status_Effect):
        self._duration += 1

object = Slowed
