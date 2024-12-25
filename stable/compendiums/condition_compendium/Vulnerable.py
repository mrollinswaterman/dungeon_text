import mechanics

class Vulnerable(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)

        self.vulnerability = mechanics.ModifyStat(self.source)
        self.vulnerability.stat = "damage_taken_multiplier"
        self.vulnerability.potency = .5
        self.vulnerability.duration = 3

        self.active_effects = [self.vulnerability]

    def refresh(self) -> None:
        if self.vulnerability.duration > 5:
            self.vulnerability.potency += 1
        else:
            self.vulnerability.duration += 1

object = Vulnerable
