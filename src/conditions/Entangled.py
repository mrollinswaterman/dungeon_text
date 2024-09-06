import global_commands
from condition import Condition
from effects import ModifyStat

class Entangled(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__

    def start(self):
        slow = ModifyStat(self.source)
        slow.stat = "max_ap"
        slow.potency = -(self.target.stats.max_ap)
        slow.duration = 2

        self.active_effects = [slow]

        self.start_message = f"{self.target.action_header} now {self.id}."
        self.end_message = f"{self.target.action_header} no longer {self.id}."
        super().start()

    def additional(self) -> None:
        slow = self.get("ModifyStat")
        slow.duration += 1

    def cleanse_check(self) -> bool:
        global_commands.type_text(f"{self.target.action_header} attempting to break the entanglement...")
        if self.target.roll_a_check("str") >= 15:
            global_commands.type_text(f"It worked. {self.target.action_header} now free.")
            self.end()
            return True
        else: 
            global_commands.type_text(f"{self.target.default_header} failed. {self.target.action_header} not going anywhere.")
            return False

object = Entangled
