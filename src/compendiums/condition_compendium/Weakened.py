import mechanics

class Weakened(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)

        self.weak = mechanics.ModifyStat(self.source)
        self.weak.stat = "str"
        self.weak.potency = -3
        self.weak.duration = 3

        self.active_effects = [self.weak]

    def refresh(self) -> None:
        if self.weak.duration > 5:
            self.weak.potency += 1
        else:
            self.weak.duration += 1

object = Weakened
