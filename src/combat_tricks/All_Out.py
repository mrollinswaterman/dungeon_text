#Power attack combat trick file
from trick import Combat_Trick

class All_Out(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self.activation_text = f"You drop all defensive capabilites to focus on offense."

        self._target = self.parent
        self.default_roll_to_hit = self.parent.roll_to_hit
        self.default_evasion = self.parent.evasion
        self.targets = ["roll_to_hit", "evasion"]

    def activate(self):
        self.parent.spend_ap()
        super().activate()

    def roll_to_hit(self):
        print("all_out roll 2 hit\n")
        return self.default_roll_to_hit() + max(self.parent.bonus("dex"), self.parent.bonus("str")) // 2
    
    def evasion(self):
        print("all_out evas\n")
        return self.default_evasion() - self.parent.bonus("dex")

    def deactivate(self):
        super().deactivate()

object = All_Out
