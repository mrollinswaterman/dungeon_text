from condition import Condition
from effects import ModifyStat

class Weakened(Condition):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = self.__class__.__name__

        weak = ModifyStat(self.source, self.target)
        weak.stat = "str"
        weak.potency = -3
        weak.duration = 3

        self.active_effects = [weak]

        self.start_message = f"{self.target.condition_header} now {self.id}."
        self.end_message = f"{self.target.condition_header} no longer {self.id}."

        self.start()

    def additional(self) -> None:
        weak = self.get("ModifyStat")
        if weak.duration > 5:
            weak.potency += 1
        else:
            weak.duration += 1

