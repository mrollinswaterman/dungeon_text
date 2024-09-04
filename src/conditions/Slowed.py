from condition import Condition
from effects import ModifyStat

class Slowed(Condition):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = self.__class__.__name__

        slow = ModifyStat(self.source, self.target)
        slow.stat = "dex"
        slow.potency = -3
        slow.duration = 3

        self.active_effects = [slow]

        self.start_message = f"{self.target.condition_header} now {self.id}."
        self.end_message = f"{self.target.condition_header} no longer {self.id}."

        self.start()

    def additional(self) -> None:
        slow = self.get("ModifyStat")
        if slow.duration > 5:
            slow.potency += 1
        else:
            slow.duration += 1

