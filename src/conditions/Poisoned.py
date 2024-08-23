#Poisoned condition
import status_effect, global_commands

class Condition(status_effect.Status_Effect):
    def __init__(self, src, target=None, id="Poisoned"):
        super().__init__(src, target, id)
        import global_variables
        self._target = global_variables.PLAYER if target is None else self._target
        self._stacks = 0
        self._target_header = "You are"
        if self._target != global_variables.PLAYER:
            self._target_header = f"The {self._target.id} is"

        self._message = f"{self._target_header} now {id}."
        self._cleanse_message = f"{self._target_header} no longer {self._id}."

    @property
    def stacks(self):
        return self._stacks
    @property
    def damage_header(self) -> str:
        return "Poison"
    @property
    def damage_type(self) -> str:
        return "True"

    def set_stacks(self, num:int):
        self._stacks = num
        self._duration = self._stacks
    
    def additional_effect(self, effect):
        self._potency += 1
        global_commands.type_text("The poison's effect becomes more severe...")
        return None

    def update(self):
        if self._active:
            self._duration -= 1
            damage = self._potency * self._stacks
            self._stacks -= 1
            if self._target.roll_a_check("con") >= damage * self._potency:
                damage //= 2
            self._target.take_damage(int(damage), self, True)
            if self._duration <= 0 or self._stacks <= 0:
                self._stacks = 0
                self._duration = 0
                self._active = False
    
    def attempt_cleanse(self, roll: int = 0):
        import global_variables
        if roll >= self._potency * 2 * self._stacks:
            self.cleanse()
        else:
            if self._target != global_variables.PLAYER:
                global_commands.type_text(f"The {self._target.id} failed to cleanse the Poison.")

            else:
                global_commands.type_text(f"You failed to cleanse the Poison.")

    def cleanse(self) -> None:
        self._active = False
        self._duration = 0
        self._stacks = 0
        global_commands.type_text(self._cleanse_message)
        return None
    
    def apply(self) -> None:
        super().apply()
