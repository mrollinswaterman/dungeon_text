from condition import Condition
from effects import ModifyStat

class Vulnerable(Condition):
    def __init__(self, source):
        super().__init__(source)

        vulnerability = ModifyStat(self.source)
        vulnerability.stat = "damage_taken_multiplier"
        vulnerability.potency = .5
        vulnerability.duration = 3

        self.active_effects = [vulnerability]

    def additional(self) -> None:
        weak = self.get("ModifyStat")
        if weak.duration > 5:
            weak.potency += 1
        else:
            weak.duration += 1

object = Vulnerable
