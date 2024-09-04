import global_commands
from condition import Condition
from effects import DamageOverTime, SingleInstanceDamage

class On_Fire(Condition):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = self.__class__.__name__

        fire = SingleInstanceDamage(self.source, self.target)
        fire.potency = "1d6"

        burning = DamageOverTime(self.source, self.target)
        burning.duration = 3
        burning.potency = "1d6"

        self.active_effects = [fire, burning]

        self.start_message = f"{self.target.condition_header} now {self.id}."
        self.end_message = f"{self.target.condition_header} no longer {self.id}."

        self.start()

    def additional(self) -> None:
        burning = self.get("DamageOverTime")
        burning.duration += 2

    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.default_header} attempting to put out the fire...")
        if self.target.roll_a_check("dex") >= 15:
            global_commands.type_text("It worked. The fire sputters out.")
            self.end()
            return True
        else: 
            global_commands.type_text(f"No luck. The flames rage on.")
            return False
