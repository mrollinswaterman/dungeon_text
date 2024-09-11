#Power attack combat trick file
import global_commands
from trick import Combat_Trick

class Power_Attack(Combat_Trick):

    def __init__(self, parent):
        super().__init__(parent)
        self.penalty = self.parent.bonus("dex")
        self.activation_text = f"You wind up for a powerful attack..."

        #defaults
        self.default_roll_to_hit = self.parent.roll_to_hit
        self.default_roll_damage = self.parent.roll_damage
        self.default_roll_narration = self.parent.roll_narration

        self.targets = ["roll_to_hit", "roll_damage", "roll_narration"]

    def activate(self):
        super().activate()
        self.parent.attack()

    def roll_to_hit(self):
        return self.default_roll_to_hit() - self.penalty 
    
    def roll_damage(self):
        return self.default_roll_damage() + (((self.parent.weapon.weight_class.value / 2) - 0.5) * self.penalty)
    
    def roll_narration(self, roll):
        text = self.parent.process_roll(roll)
        text = text[len("rolling "):]
        return [f"You rolled {text}"]

object = Power_Attack
