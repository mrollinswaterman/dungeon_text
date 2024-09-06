from condition import Condition
from effects import ModifyStat

class Slowed(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__

        slow = ModifyStat(self.source)
        slow.stat = "dex"
        slow.potency = -3
        slow.duration = 3

        self.active_effects = [slow]

    def start(self):
        self.start_message = f"{self.target.action_header} now {self.id}."
        self.end_message = f"{self.target.action_header} no longer {self.id}."
        super().start()

    def additional(self) -> None:
        slow = self.get("ModifyStat")
        if slow.duration > 5:
            slow.potency += 1
        else:
            slow.duration += 1

object = Slowed
