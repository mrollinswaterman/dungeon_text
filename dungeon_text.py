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
    def str_bonus(self) -> int:
        return BONUS[self._strength]
    @property
    def dex(self) -> int:
        return self._dexterity
    @property
    def dex_bonus(self) -> int:
        return BONUS[self._dexterity]
    @property
    def con(self) -> int:
        return self._constitution
    @property
    def con_bonus(self) -> int:
        return BONUS[self._constitution]
    @property
    def int(self) -> int:
        return self._intelligence
    @property
    def int_bonus(self) -> int:
        return BONUS[self._intelligence]
    @property
    def wis(self) -> int:
        return self._wisdom
    @property
    def wis_bonus(self) -> int:
        return BONUS[self._wisdom]
    @property
    def cha(self) -> int:
        return self._charisma
    @property
    def cha_bonus(self) -> int:
        return BONUS[self._charisma]
    
    #