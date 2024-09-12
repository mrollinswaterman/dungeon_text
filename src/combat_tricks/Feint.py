#Feint combat trick file
import global_commands
from trick import Combat_Trick

class Feint(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self._target = self.parent.target
        self.duration = 2

        self.default_evasion = self.parent.target.evasion
        self.activation_text = f"You attempt a feint maneuver."

        self.targets = ["evasion"]

    def activate(self):
        self.parent.spend_ap()
        global_commands.type_text(self.activation_text)
        if self.parent.roll_a_check("cha") >= self.parent.target.roll_a_check("cha"):
            self.run_replacement()
            global_commands.type_text(f"A success. You faked out the {self.parent.target.id}!")
            print(self.parent.target.evasion())
        else:
            global_commands.type_text(f"The {self.parent.target.id} saw through your trick.")
            self.deactivate()
    
    def evasion(self) -> int:
        return self.default_evasion() - self.parent.target.bonus("dex")

object = Feint
