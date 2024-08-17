#Bandit mob file
import random
import global_commands, mob

stats = {
    "base_level": 2,
    "str": 14,
    "dex": 12,
    "con": 12,
    "int": 14,
    "wis": 8,
    "cha": 10,
    "base_evasion": 9,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 1,
    "damage": "2d4",
    "dc": 10,
    "hit_dice": 10,
    "loot": {
        "gold": 15,
        "xp": 8,
        "drops": []
    }
}

class Bandit(mob.Mob):
    def __init__(self, id="Bandit", level = (2,7), statblock=stats):
        super().__init__(id, level, statblock)

    def special(self) -> bool:
        return False

    def roll_text(self):
        base = super().roll_text()        
        me = [
            f"The {self.id} slashes at you with it's sword.",
            f"The {self.id} readies it's blade to strike.",
            f"The {self.id} lashes out wildly.",
        ]
        return base + me

    def hit_text(self):
        base = super().hit_text()
        me = [
            f"The {self.id}'s sword cuts through your defense."
        ]
        return base + me

    def miss_text(self):
        base = super().miss_text()
        me = [
            f"You easily dodge the {self.id}'s wayward strike.",
            f"You duck out of reach of it's sword.",
            f"The {self.id}'s sword whistles past your ear as you sidestep it's swing.",
            f"You manage to deflect the {self.id}'s blade with your own."
        ]
        return base + me

object = Bandit
