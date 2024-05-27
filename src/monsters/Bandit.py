#Bandit mob file
import random
import mob

stats = {
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
    "damage": 6,
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

object = Bandit
