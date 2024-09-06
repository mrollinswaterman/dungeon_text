import global_commands
from condition import Condition
from effects import RampingDamageOverTime

class Poisoned(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__

        poison = RampingDamageOverTime(self.source)
        poison.stacks = 2
        poison.duration = 5
        poison.potency = "1d4"

        self.active_effects = [poison]

    def start(self):
        self.start_message = f"{self.target.action_header} now {self.id}."
        self.end_message = f"{self.target.action_header} no longer {self.id}."
        super().start()

    def additional(self) -> None:
        global_commands.type_text(f"The poison spreads further.")
        poison = self.get("RampingDamageOverTime")
        poison.stacks += 2

    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.default_header} attempting to cleanse the poison...")
        if self.target.roll_a_check("con") >= 15:
            global_commands.type_text("Success! The poison is no longer effective.")
            self.end()
            return True
        else:
            global_commands.type_text(f"{self.target.default_header} failed. {self.target.action_header} still poisoned.")
            return False

object = Poisoned
