import global_commands
from condition import Condition
from effects import RampingDamageOverTime

class Bleeding(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__

        bleed = RampingDamageOverTime(self.source)
        bleed.stacks = 3
        bleed.duration = 2
        bleed.potency = "1d6"

        self.active_effects = [bleed]

    def start(self):
        self.start_message = f"{self.target.action_header} now {self.id}."
        self.end_message = f"{self.target.action_header} no longer {self.id}."
        super().start()

    def additional(self) -> None:
        bleed = self.get("RampingDamageOverTime")
        bleed.stacks += 2
    
    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.default_header} attempting to stop the bleeding...")
        if self.target.roll_a_check("con") >= 15:
            global_commands.type_text("Success! The bleeding trickles to nothing.")
            self.end()
            return True
        else: 
            global_commands.type_text(f"{self.target.default_header} failed. The bleed continues.")
            return False

object = Bleeding
