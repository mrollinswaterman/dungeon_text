from condition import Condition
from effects import ModifyStat

class Vulnerable(Condition):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = self.__class__.__name__

        vulnerability = ModifyStat(self.source, self.target)
        vulnerability.stat = "damage_taken_multiplier"
        vulnerability.potency = .5
        vulnerability.duration = 3

        self.active_effects = [vulnerability]

        self.start_message = f"{self.target.condition_header} now {self.id}."
        self.end_message = f"{self.target.condition_header} no longer {self.id}."

        self.start()

    def additional(self) -> None:
        weak = self.get("ModifyStat")
        if weak.duration > 5:
            weak.potency += 1
        else:
            weak.duration += 1

