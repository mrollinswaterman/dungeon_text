#Bandit mob file
import game_objects.mob as mob

class Bandit(mob.Mob):
    def __init__(self):
        super().__init__(id="Bandit")
        #base gold & xp
        self.gold += 15
        self.xp += 8

    def special(self) -> bool:
        return False

    def roll_narration(self):
        base = super().roll_narration()        
        me = [
            f"The {self.id} slashes at you with it's sword.",
            f"The {self.id} readies it's blade to strike.",
            f"The {self.id} lashes out wildly.",
        ]
        return base + me

    def hit_narration(self):
        base = super().hit_narration()
        me = [
            f"The {self.id}'s sword cuts through your defense."
        ]
        return base + me

    def miss_narrartion(self):
        base = super().miss_narration()
        me = [
            f"You easily dodge the {self.id}'s wayward strike.",
            f"You duck out of reach of it's sword.",
            f"The {self.id}'s sword whistles past your ear as you sidestep it's swing.",
            f"You manage to deflect the {self.id}'s blade with your own."
        ]
        return base + me

object = Bandit
