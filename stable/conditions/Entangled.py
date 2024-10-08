import global_commands
from condition import Condition
from effects import ModifyStat

class Entangled(Condition):
    def __init__(self, source):
        super().__init__(source)

    def start(self):
        slow = ModifyStat("the entanglement")
        slow.stat = "max_ap"
        slow.potency = -(self.target.stats.max_ap)
        slow.duration = 2

        self.active_effects = [slow]

        super().start()

    def additional(self) -> None:
        slow = self.get("ModifyStat")
        slow.duration += 1

    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.header.action} attempting to break the entanglement...")
        if self.target.roll_a_check("str") >= 15:
            global_commands.type_text(f"It worked. {self.target.header.action} now free.")
            self.end()
            return True
        else: 
            global_commands.type_text(f"{self.target.header.default} failed. {self.target.header.action} not going anywhere.")
            return False

object = Entangled
