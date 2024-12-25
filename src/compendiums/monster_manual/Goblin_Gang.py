#Goblin Gang mob file
import game_objects.mob as mob

stats = {
    "level": 1,
    "level_range": (2, 6),
    "hit_dice": 8,
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
}

class Goblin_Gang(mob.Mob):
    def __init__(self, id="Goblin Gang", stat_dict=stats):
        super().__init__(id, stat_dict)
        
        #goblin_gang gets x1.5 HP
        self.stats.max_hp *= 1.5
        self.hp = self.stats.max_hp
        
        self.gold += 20
        self.xp += 10

    def special(self) -> bool:
        return False

object = Goblin_Gang