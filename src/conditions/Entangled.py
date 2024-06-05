#Entangled condition
import status_effect, global_commands

class Entangled(status_effect.Status_Effect):

    def __init__(self, src, target=None, id="Entangled"):
        """
        Init function for Entangled status effect

        target_header and cleanse_header change based on the target of the effect,
        either the global_variables.PLAYER or a mob, and head the self._message and cleanse function text ouput.
        """
        super().__init__(src, target, id)
        import global_variables
        self._target = global_variables.PLAYER if target is None else self._target
        self._stat = "ap"
        self._target_header = "You are"
        self._cleanse_header = "You try"
        if self._target != global_variables.PLAYER:
            self._target_header = f"The {self._target.id} is"
            self._cleanse_header = f"The {self._target.id} tries"

        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} no longer {id}."
        self._cleanse_stat = "str"

    def update(self) -> None:
        super().update()
        if self._active:
            self.attempt_cleanse()

    def apply(self):
        super().apply()
        self._target.stats[self._stat] -= self._potency

    def cleanse(self):
        self._target.stats[self._stat] += self._potency
        super().cleanse()

    def attempt_cleanse(self, roll: int = 0) -> bool:
        global_commands.type_text(f"{self._cleanse_header} to break free of the entanglement...")
        if roll >= self._src.dc - 2:
            global_commands.type_text("Success!")
            return self._target.remove_status_effect(self)
        global_commands.type_text("No luck.")
        return False
    
    def additional_effect(self, effect: status_effect.Status_Effect):
        global_commands.type_text("The entanglment's duration grows...")
        self._duration += 1
        return None