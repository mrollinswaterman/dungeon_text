#Feint combat trick file
import stable.globals.functions as functions
from mechanics.trick import Combat_Trick
from game_objects.game_object import Game_Object

class Feint(Combat_Trick):

    def __init__(self, parent:Game_Object):
        super().__init__(parent, parent.target)

        self.default_evasion = self.parent.target.evasion
        self.start_message = f"You attempt a feint maneuver."

        self.replace_effect.target_list = ["evasion"]

    def start(self):
        self.parent.spend_ap()
        functions.type_text(self.start_message)
        if self.parent.roll_a_check("cha") >= self.parent.target.roll_a_check("cha"):
            self.replace_effect.start()
            functions.type_text(f"A success. You faked out the {self.parent.target.id}!")
        else:
            functions.type_text(f"The {self.parent.target.id} saw through your trick.")
            self.end()
    
    def evasion(self) -> int:
        return self.default_evasion() - self.parent.target.bonus("dex")

object = Feint
