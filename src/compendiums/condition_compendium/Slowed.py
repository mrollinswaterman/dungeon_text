import mechanics

class Slowed(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)

        slow = mechanics.ModifyStat(self.source)
        slow.stat = "dex"
        slow.potency = -3
        slow.duration = 3

        self.active_effects = [slow]

    def refresh(self) -> None:
        slow = self.get("ModifyStat")
        if slow.duration > 5:
            slow.potency += 1
        else:
            slow.duration += 1

object = Slowed
