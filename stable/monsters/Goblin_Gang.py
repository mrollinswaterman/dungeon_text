#Goblin Gang mob file
import mob

stats = {
    "base_level": 2,
    "str": 14,
    "dex": 10,
    "con": 14,
    "int": 8,
    "wis": 10,
    "cha": 6,
    "base_evasion": 7,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 0,
    "armor": 0,
    "damage": "3d4",
    "dc": 10,
    "hit_dice": 10,
    "loot": {
        "gold": 20,
        "xp": 10,
        "drops": []
    }
}

class Goblin_Gang(mob.Mob):
    def __init__(self, id="Goblin Gang", level = (2,6), statblock=stats):
        super().__init__(id, level, statblock)
        
        #goblin_gang gets x1.5 HP
        self._stats["max_hp"] *= 1.5
        self._hp = self.max_hp

    def special(self) -> bool:
        return False

object = Goblin_Gang