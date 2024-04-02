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
        }

        self._max_hp = 8 + self.bonus("con")
        self._hp = self._max_hp
        self._max_ap = 1 + (self._level // 5)
        self._ap = self._max_ap
        self._damage_taken_multiplier = 1

        self._stats["evasion"] = 9
        self._stats["damage-taken-multiplier"] = self._damage_taken_multiplier
        self._stats["hp"] = self._hp
        self._stats["ap"] = self._max_ap

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
