#Stat debuffs
import status_effect

#All the repeated Stat_Buff code here is to save me the trouble of figuring out imports
class Stat_Buff(status_effect.Status_Effect):
    def __init__(self, src, target=None, id="Buff"):
        super().__init__(src, target, id)
        import global_variables
        self._target = global_variables.PLAYER if target is None else self._target
        self._stat = ""
        self._target_header = f"Your"
        if self._target != global_variables.PLAYER:
            self._target_header = f"The {self._target.id}'s"
        self._count = 1

    @property
    def stat(self) -> str:
        return self._stat

    def update_message(self):
        from global_variables import STATS
        self._message = f"{self._target_header} {STATS[self._stat]} increased by {self._potency}."
        if self._cleanse_message == "":
            self._cleanse_message = f"{self._target_header} {STATS[self._stat]} has returned to normal."
        if self._id == "":
            self._id = f"{self._stat} Buff"

    def set_stat(self, stat:str) -> None:
        self._stat = stat
        self.update_message()   

    def apply(self):
        super().apply()
        self._target.stats[self._stat] += self._potency

    def cleanse(self) -> None:
        for _ in range(self._count):
            self._target.stats[self._stat] -= self._potency
        super().cleanse()
    
    def additional_effect(self, effect: status_effect.Status_Effect):
        self.apply()
        self._count += 1
        return None

class Condition(Stat_Buff):
    def __init__(self, src, target=None, id="Debuff"):
        super().__init__(src, target, id)

    def update_message(self):
        from global_variables import STATS
        self._message = f"{self._target_header} {STATS[self._stat]} decreased by {-self._potency}."
        self._cleanse_message = f"{self._target_header} {STATS[self._stat]} has returned to normal."

        if self._id == "":
            self._id = f"{self._id} Debuff"

    def set_potency(self, num: int) -> None:
        super().set_potency(num)
        self._potency = -self._potency
        self.update_message()
