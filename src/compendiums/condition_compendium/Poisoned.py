import globals
import mechanics

class Poisoned(mechanics.Condition):
    def __init__(self, source):
        super().__init__(source)

        self.poison = mechanics.DecreasingDoT("the poison")
        self.poison.duration = 3
        self.poison.potency = "1d4"

        self.active_effects = [self.poison]

    def update(self):
        if self.target.roll_a_check("con") >= 10 + self.poison.duration:
            globals.type_text(f"{self.target.header.default} resists the poison, taking no damage.")
            self.poison.duration -= 1
        else:
            super().update()

    def refresh(self) -> None:
        globals.type_text(f"The poison spreads further.")
        self.poison.duration += 2

    def cleanse_check(self) -> bool:
        globals.type_text(f"{self.target.header.action} attempting to cleanse the poison...")
        if self.target.roll_a_check("con") >= 15:
            globals.type_text("Success! The poison is no longer effective.")
            self.end()
            return True
        else:
            globals.type_text(f"{self.target.header.default} failed. {self.target.header.action} still poisoned.")
            return False

object = Poisoned
