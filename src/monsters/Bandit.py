#Bandit mob file
import random
import mob

class Bandit(mob.Mob):
    def __init__(self, id="Bandit", level = (1,7)):
        super().__init__(id, level)
        self._stats = {
            "str": 14,
            "dex": 12,
            "con": 12,
            "int": 14,
            "wis": 8,
            "cha": 10,
            "evasion": 9,
            "damage-taken-multiplier": 1
        }
        self._damage = 6
        self._armor = 2
        self._loot = {
            "gold": 15,
            "xp": 8,
            "drops": None
        }

    def special(self) -> bool:
        return False

object = Bandit()
