#Feint combat trick file
import mechanics

class Riposte(mechanics.Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self._target = self.parent.target

        self.activation_text = f""

    def activate(self):
        increase_base_evasion = mechanics.ModifyStat(self)
        increase_base_evasion.stat = "base_evasion"
        increase_base_evasion.potency = 3

        riposte = mechanics.Condition(self)
        riposte.active_effects = [increase_base_evasion]
        self.parent.conditions.add(riposte)
    
    def deactivate(self):
        raise NotImplementedError
    
    def on_miss(self):
        roll = self.parent.roll_to_hit()
        if roll > self.parent.target.evasion():
            taken = self._target.take_damage((self._target.roll_damage() // 2), "Your riposte")

object = Riposte
