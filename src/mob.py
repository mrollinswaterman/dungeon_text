import random
from typing import Union
import global_variables

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
        self._special: Special_Move = None
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
    def min_level(self) -> int:
        return self._min_level
    @property
    def max_level(self) -> int:
        return self._max_level
    
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
    def set_special(self, move) -> None:
        if isinstance(move, Special_Move):
            print("Already spec")
            self._special = move
        else:
            print("Converting func to special move..")
            move = Special_Move(self, move)
            self._special = move
    def set_min_max(self, rang:tuple[int,int]) -> None:
        self._min_level = rang[0]
        self._max_level = rang[1]

class Mob():

    def __init__(self,statblock: Statblock, level:int = 0):
        #identification
        self._id = statblock.id
        self._name = self._id
        #base stats
        self._statblock = statblock
        #calculated stats
        self._hp = statblock.hp
        self._damage: int = statblock.damage
        self._evasion: int = statblock.evasion
        self._armor:int = statblock.armor
        self._dc = statblock.dc
        self._loot = statblock.loot
        self._special = statblock.special
        self._special.set_src(self)
        #level stuff
        self._min_level = statblock.min_level
        self._max_level = statblock.max_level
        if level == 0:
            self._level = random.randrange(statblock.min_level, global_variables.PLAYER.threat+1)
        else:
            self._level = level
        self.update()
        self._max_ap = 1 + self._level // 5
        self._ap = self._max_ap

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
    @property
    def max_ap(self) -> int:
        return self._max_ap
    @property
    def ap(self) -> int:
        return self._ap
    @property
    def special(self) -> "Special_Move":
        return self._special
    @property
    def can_act(self) -> int:
        return self._ap > 0
        
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
        
        return roll + self._level // 5
    
    def spend_ap(self, num:int) -> None:
        if self.can_act:
            self._ap -= 1
        else:
            raise ValueError("No AP to spend")
        
    def reset_ap(self):
        self._ap = self._max_ap
    
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

    def update(self):
        """
        Updates all relevant stats when a mob's level is changed
        """
        for _ in range(self._level-1):
            self._hp += random.randrange(1, self._statblock.hp) + round(self._level + 0.1 / 2)

        self._loot["gold"] = self._loot["gold"] * max(self._level // 2, 1)
        self._loot["xp"] = self._loot["xp"] * max(self._level // 2, 1)

class Special_Move():

    def __init__(self, src: Mob, func=None, target=None):
        self._src = src
        self._target = target
        self._action = func
        self._ap_cost = 1
        self._conditions = None
        self._conditions_target = None

    #properties
    @property
    def src(self) -> Mob:
        return self._src
    @property
    def target(self):
        return self._target
    @property
    def action(self):
        return self._action
    @property
    def ap_cost(self) -> int:
        return self._ap_cost
    @property
    def conditions(self):
        if self._conditions_target is True:
            return self._conditions(self._target)
        elif self._conditions_target is False:
            return self._conditions(self._src)
        return self._conditions_target
    
    #SETTERS
    def set_src(self, src:Mob):
        self._src = src
    def set_action(self, func):
        self._action = func
    def set_ap_cost(self, num:int) -> None:
        self._ap_cost = num
    def set_conditions(self, func, target=None) -> None:
        if self._conditions is None:
            self._conditions = func
            self._conditions_target = target
    def set_target(self, tar) -> None:
        if self._target is None:
            self._target = tar

    #RUN
    def run(self):
        if self._target is None:
            raise ValueError("No target.")
            return False
        
        if self._ap_cost > self._src.ap:
            return False
        if self.conditions is True:
            self._action(self._src, self._target)
            self._src.spend_ap(self._ap_cost)
            return True
        return False