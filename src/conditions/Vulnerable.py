#Vulnerable condition
import status_effect 
from conditions import Stat_Buff

class Condition(Stat_Buff.Condition):
    """
    Makes the target vulnerable,
    meaning they take x2 damage for the duration
    """
    def __init__(self, src, target=None, id="Vulnerable"):
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
        self._stat = "damage_taken_multiplier"
        self._potency = 1# this is because the apply function adds to the stat,
        #so a potency of 2 would result in a damage-taken of 3, not 2 like we want

    def update_message(self):
        pass

    def additional_effect(self, effect: status_effect.Status_Effect):
        self._potency += 1#might need re-balancing
