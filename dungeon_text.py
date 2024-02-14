from abc import ABC, abstractmethod
import random
from enum import Enum


BONUS = {
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5
}

class Player():

    def __init__(self, name: str):
        self.name = name

        self._xp = 0

        self._stat_map = {
            "str": self._strength,
            "dex": self._dexterity,
            "con": self._constitution,
            "int": self._intelligence,
            "wis": self._wisdom,
            "cha": self._charisma
        }

        #statblock
        self._strength:int = 10
        self._dexterity:int = 10
        self._constitution:int = 10
        self._intelligence:int = 10
        self._wisdom:int = 10
        self._charisma:int = 10

        #calculated stats
        self._max_hp = random.randint(8) + BONUS[self._constitution]
        self._evasion = 10 + BONUS[self._dexterity]

        #equipment
        self._weapon: None = None
        self._armor = None
    
    #properties
    @property
    def str(self) -> int:
        return self._strength
    @property
    def dex(self) -> int:
        return self._dexterity
    @property
    def con(self) -> int:
        return self._constitution
    @property
    def int(self) -> int:
        return self._intelligence
    @property
    def wis(self) -> int:
        return self._wisdom
    @property
    def cha(self) -> int:
        return self._charisma
    @property
    def bonus(self, stat) -> int:
        if type(stat) == str:
            return BONUS[self._stat_map[stat]]
        
        return BONUS[stat]

    #methods
    def roll_attack(self) -> int:
        """
        Returns an attack roll (d20 + dex bonus)
        """
        return random.randint(20) + self.bonus(self.dex)
    
    def roll_damage(self):
        """
        Returns a damage roll (weapon dice + str bonus)
        """
        #should return equipped weapon dmg + str bonus
        raise NotImplementedError

    def roll_a_check(self, stat: str) -> int:
        """
        Returns an check (d20 + stat bonus)
        """
        return random.randint(20) + BONUS[self._stat_map[stat]]
