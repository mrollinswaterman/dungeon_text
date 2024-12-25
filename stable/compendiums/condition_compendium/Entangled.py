import globals
import mechanics

class Entangled(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)

        self.slow = mechanics.ModifyStat("the entanglement")

        self.slow.stat = "max_ap"

        self.slow.potency = -(self.target.stats.max_ap)

        self.slow.duration = 2

        self.active_effects = [self.slow]

    def refresh(self) -> None:
        self.slow.duration += 1

    def cleanse_check(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to break the entanglement...")
        if self.target.roll_a_check("str") >= 15:
            globals.type_text(f"It worked. {self.target.header.action} now free.")
            self.end()
            return True
        else: 
            globals.type_text(f"{self.target.header.default} failed. {self.target.header.action} not going anywhere.")
            return False

object = Entangled
