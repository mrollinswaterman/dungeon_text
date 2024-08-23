#On Fire condition
import status_effect, global_commands

class Condition(status_effect.Status_Effect): 
    def __init__(self, src, target=None, id="On Fire"):
        super().__init__(src, target, id)
        import global_variables
        self._target = global_variables.PLAYER if target is None else self._target
        self._target_header = "You are"
        if self._target != global_variables.PLAYER:
            self._target_header = f"The {self._target.id} is"
        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} not longer {id}."

    @property
    def damage_header(self) -> str:
        return "Fire"
    @property
    def damage_type(self) -> str:
        return "True"

    def update(self):
        if self._active:
            self._duration -= 1
            taken = self._target.take_damage(self._potency, self, True)

            if self._duration <= 0:
                self._active = False
    
    def additional_effect(self, effect: status_effect.Status_Effect):
        global_commands.type_text("More fire has no effect.")
