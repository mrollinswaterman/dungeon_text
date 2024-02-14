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
        self._hp = self._max_hp
        self._evasion = 10 + BONUS[self._dexterity]
        self._xp = 0
        self._level = 1
        self._gold = 0
        self._inventory = []

        #equipment
        self._weapon: None = None
        self._armor = None
    
    #properties
    @property
    def dead(self):
        return self._hp <= 0
    @property
    def level(self):
        return self.level
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
    @property
    def hp(self):
        return self._hp
    @property
    def armor(self):
        #should return armor value of equipped armor
        return 3
    @property
    def carrying_capacity(self) -> int:
        return 10 + self.bonus(self.str) + self.bonus(self.con)

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
        Returns a check with a given stat (d20 + stat bonus)
        """
        return random.randint(20) + BONUS[self._stat_map[stat]]
    
    def take_damage(self, damage: int) -> None:
        """
        Reduces the players hp by a damage amount, reduced by armor
        """
        if damage - self.armor < 0:
            pass
        else:
            self._hp -= damage - self.armor

    def pick_up(self, item) -> None:
        """
        Picks up an item if the player has inventory space for it
        """
        if len(self._inventory) < self.carrying_capacity:
            self._inventory.append(item)

        else:
            raise ValueError("Not enough inventory space")
        
    def drop(self, item) -> None:
        """
        Drops an item out of the player's inventory
        """
        if item in self._inventory:
            self._inventory.remove(item)

        else:
            raise ValueError("Can't drop an item you don't have")

class Item():

    def __init__(self, id, rarity):

        #rarity map
        self._id = id
        self._rarity = rarity
        self._value = 5 * rarity

    #properties
    @property
    def id(self):
        return self._id
    @property
    def value(self):
        return self._value
    

class Weapon(Item):

    def __init__(self, id, rarity, damage_dice: int):
        super().__init__(id, rarity)
        self._damage_dice = damage_dice

        self._max_durability = 10 * self._rarity
        self._durability = self._max_durability

    #properties
    @property
    def broken(self):
        return self._durability <= 0
    @property
    def durability(self):
        return self._durability
    
    def lose_durability(self) -> None:
        self._durability -= 1 


sword = Weapon("weapon", 1, 8)

print(sword.value)

