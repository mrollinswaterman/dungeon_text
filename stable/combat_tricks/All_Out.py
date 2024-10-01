#Power attack combat trick file
from trick import Combat_Trick

class All_Out(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent, parent)
        self.start_message = f"You drop all defensive capabilites to focus on offense."
        self.end_message = f"You return to a balanced fighting stance."

        self.default_roll_to_hit = self.parent.roll_to_hit
        self.default_evasion = self.parent.evasion
        self.replace_effect.target_list = ["roll_to_hit", "evasion"]

    def start(self):
        self.parent.spend_ap()
        super().start()

    def roll_to_hit(self):
        return self.default_roll_to_hit() + max(self.parent.bonus("dex"), self.parent.bonus("str")) // 2
    
    def evasion(self):
        return self.default_evasion() - self.parent.bonus("dex")

    def end(self):
        super().end()

object = All_Out
