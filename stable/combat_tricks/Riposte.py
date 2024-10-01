#Feint combat trick file
import global_commands
from trick import Combat_Trick
from effects import ModifyStat
from condition import Condition

class Riposte(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self._target = self.parent.target

        self.activation_text = f""

    def activate(self):
        increase_base_evasion = ModifyStat(self)
        increase_base_evasion.stat = "base_evasion"
        increase_base_evasion.potency = 3

        riposte = Condition(self)
        riposte.active_effects = [increase_base_evasion]
        self.parent.conditions.add(riposte)
    
    def deactivate(self):
        raise NotImplementedError
    
    def on_miss(self):
        roll = self.parent.roll_to_hit()
        if roll > self.parent.target.evasion():
            taken = self._target.take_damage((self._target.roll_damage() // 2), "Your riposte")

object = Riposte
