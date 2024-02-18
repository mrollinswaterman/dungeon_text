import random
from typing import Optional, Union

class Statblock():

    def __init__(self, id):
        self._id = id
        self._hp = 0
        self._damage = 0
        self._evasion = 0
        self._armor = 0
        self._loot = (0, 0)

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
    
    #methods
    def set_hp(self, num:int) -> None:
        self._hp = num
    def set_damage(self, num:int) -> None:
        self._damage = num
    def set_evasion(self, num:int) -> None:
        self._evasion = num
    def set_armor(self, num:int) -> None:
        self._armor = num
    def set_loot(self, loot:tuple[int, int]) -> None:
        self._loot = loot


class Mob():

    def __init__(self, level, statblock: Statblock):
        self._id = statblock.id
        self._level = level

        #base stats
        self._stat_block = statblock

        #calculated stats
        self._hp = statblock.hp
        for _ in range(level-1):
            self._hp += random.randrange(1, statblock.hp) + round(level + 0.1 / 2)
        self._damage: int = statblock.damage
        self._evasion: int = statblock.evasion
        self._armor:int = statblock.armor
        
        #add loot
        self._loot = []
        for item in statblock.loot:
            self._loot.append(item*level // 2)

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
        prob = random.randrange(100)

        if prob > 50:
            return False
        
        else: 
            return True