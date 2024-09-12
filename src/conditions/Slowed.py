from condition import Condition
from effects import ModifyStat

class Slowed(Condition):
    def __init__(self, source):
        super().__init__(source)

        slow = ModifyStat(self.source)
        slow.stat = "dex"
        slow.potency = -3
        slow.duration = 3

        self.active_effects = [slow]

    def additional(self) -> None:
        slow = self.get("ModifyStat")
        if slow.duration > 5:
            slow.potency += 1
        else:
            slow.duration += 1

object = Slowed
