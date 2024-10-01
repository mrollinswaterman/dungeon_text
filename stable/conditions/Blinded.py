import global_commands
from condition import Condition
from effects import MethodReplacement

class Blinded(Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__
        self.miss_chance = 50

    def start(self):
        self.default_attack = self.target.attack

        blindness = MethodReplacement(self, self.target)
        blindness.duration = 10000
        blindness.target_list = ["attack"]
        self.active_effects = [blindness]

        super().start()

    def additional(self) -> None:
        global_commands.type_text(f"{self.target.header.action} already {self.id}.")
        return None
    
    def attack(self) -> None:
        if not global_commands.probability(self.miss_chance):
            return self.default_attack()
        else: 
            self.target.spend_ap()
            global_commands.type_text(f"{self.target.header.ownership} attack missed!")

object = Blinded
