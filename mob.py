import random
from typing import Union

class Statblock():

    def __init__(self, id):
        self._id = id
        self._hp = 0
        self._damage = 0
        self._evasion = 0
        self._armor = 0
        self._loot = {
            "gold": 0,
            "xp": 0,
            "drop" : None
        }
        self._dc = 0
        self._special: None | function = None
        self._min_level = 0
        self._max_level = 0

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def damage(self) -> int:
        return self._damage
    @property
    def evasion(self) -> int:
        return self._evasion
    @property
    def armor(self) -> int:
        return self._armor
    @property
    def loot(self):
        return self._loot
    @property
    def dc(self):
        return self._dc
    @property
    def special(self):
        return self._special
    @property
    def level_range(self) -> tuple[int, int]:
        return (self._min_level, self._max_level)
    
    #methods
    def set_hp(self, num:int) -> None:
        self._hp = num
    def set_damage(self, num:int) -> None:
        self._damage = num
    def set_evasion(self, num:int) -> None:
        self._evasion = num
    def set_armor(self, num:int) -> None:
        self._armor = num
    def set_gold(self, num:int) -> None:
        self._loot["gold"] = num
    def set_xp(self, num:int) -> None:
        self._loot["xp"] = num
    def set_drop(self, item) -> None:
        self._loot["drop"] = item
    def set_dc(self, dc: int) -> None:
        self._dc = dc
    def set_special(self, func) -> None:
        self._special = func
    def set_min_max(self, rng:tuple[int,int]) -> None:
        self._min_level = rng[0]
        self._max_level = rng[1]


class Mob():

    def __init__(self, level, statblock: Statblock):
        self._id = statblock.id
        self._name = self._id
        self._level = level
        #base stats
        self._statblock = statblock
        #calculated stats
        self._hp = statblock.hp
        self._damage: int = statblock.damage
        self._evasion: int = statblock.evasion
        self._armor:int = statblock.armor
        self._dc = statblock.dc
        #add loot
        self._loot = statblock.loot
        self._special = statblock.special
        self._min_level = statblock.level_range[0]
        self._max_level = statblock.level_range[1]
        

    #properties
    @property
    def dead(self) -> bool:
        return self.hp <= 0
    @property
    def level(self) -> int:
        return self._level
    @property
    def damage(self) -> int:
        return self._damage
    @property
    def evasion(self) -> int:
        return self._evasion
    @property
    def armor(self) -> int:
        return self._armor
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def loot(self):
        return self._loot
    @property
    def id(self) -> str:
        return self._id
    @property
    def name(self) -> str:
        return self._name
    @property
    def dc(self) -> int:
        return self._dc
    @property
    def statblock(self) -> Statblock:
        return self._statblock
    @property
    def level_range(self) -> tuple[int, int]:
        return (self._min_level, self._max_level)
        
    #methods
    def roll_attack(self) -> int:
        """
        Rolls an attack (d20)
        """
        roll = random.randrange(1,20)

        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll
    
    def roll_damage(self) -> int:
        """
        Rolls damage (damage dice)
        """
        return random.randrange(1, self._damage) + 1
    
    def take_damage(self, damage:int) -> int:
        """
        Takes a given amount of damage, reduced by armor
        """
        if (damage - self._armor) < 0:
            return 0
        else:
            self._hp -= damage - self._armor
            return damage - self._armor
        
    def fumble_table(self) -> Union[str, bool]:
        """
        Determines if a mob sufferes a negative effect upon rolling a nat 1.
        """
        prob = random.randrange(100)

        if prob > 50:
            return False
        
        else: 
            return True
        
    def attack_of_oppurtunity(self, target) -> bool:
        
        if self.roll_attack() - 2 >= target.evasion:
            return True
        return False
        
    def special_move(self, source, target):
        """
        Calls the special move function
        """
        self._special(source, target)

    def add_special_move(self, special) -> None:
        """
        Adds a function to serve as the mob's "special move".
        """
        self._special = special

    def add_gold(self, num:int) -> None:
        """
        Adds an integer value to the mob's gold reward
        """
        self._loot["gold"] += num

    def add_xp(self, num:int) -> None:
        """
        Adds an integer value to the mob's XP reward
        """
        self._loot["xp"] += num

    def set_level(self, level:int)-> None:
        """
        Sets the mobs levels then calculates HP and loot based on level
        """
        self._level = level
        for _ in range(level-1):
            self._hp += random.randrange(1, self._statblock.hp) + round(level + 0.1 / 2)

        self._loot["gold"] = self._loot["gold"] * max(self._level // 2, 1)
        self._loot["xp"] = self._loot["xp"] * max(self._level // 2, 1)
