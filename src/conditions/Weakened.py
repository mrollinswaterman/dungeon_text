from condition import Condition
from effects import ModifyStat

class Weakened(Condition):
    def __init__(self, source):
        super().__init__(source)

        weak = ModifyStat(self.source)
        weak.stat = "str"
        weak.potency = -3
        weak.duration = 3

        self.active_effects = [weak]

    def additional(self) -> None:
        weak = self.get("ModifyStat")
        if weak.duration > 5:
            weak.potency += 1
        else:
            weak.duration += 1

object = Weakened
