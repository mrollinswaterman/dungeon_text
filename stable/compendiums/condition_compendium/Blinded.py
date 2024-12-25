import globals
import mechanics

class Blinded(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__
        self.miss_chance = 50

        self.default_attack = self.target.attack

        self.blindness = mechanics.MethodReplacement(self, self.target)
        self.blindness.duration = 10000
        self.blindness.target_list = ["attack"]
        self.active_effects = [self.blindness]

    def start(self):


        super().start()

    def refresh(self) -> None:
        globals.type_text(f"{self.target.header.action} already {self.id}.")
        return None
    
    def attack(self) -> None:
        if not globals.probability(self.miss_chance):
            return self.default_attack()
        else: 
            self.target.spend_ap()
            globals.type_text(f"{self.target.header.ownership} attack missed!")

object = Blinded
