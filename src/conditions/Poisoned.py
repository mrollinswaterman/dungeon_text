import global_commands
from condition import Condition
from effects import RampingDamageOverTime

class Poisoned(Condition):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = self.__class__.__name__

        poison = RampingDamageOverTime(self.source, self.target)
        poison.stacks = 2
        poison.duration = 5
        poison.potency = "1d4"

        self.active_effects = [poison]

        self.start_message = f"{self.target.condition_header} now {self.id}."
        self.end_message = f"{self.target.condition_header} no longer {self.id}."

        self.start()

    def additional(self) -> None:
        poison = self.get("RampingDamageOverTime")
        poison.stacks += 2

    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.default_header} attempting to cleanse the poison...")
        if self.target.roll_a_check("con") >= 15:
            global_commands.type_text("Success! The poison is no longer effective.")
            self.end()
            return True
        else:
            global_commands.type_text(f"{self.target.default_header} failed. {self.target.condition_header} still poisoned.")
            return False
