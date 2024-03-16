import random
from typing import Union
import global_variables, global_commands
import player

class Mob():

    def __init__(self, id:str="Anonymous_Mob", level:tuple= (1, 20)):
        #identification
        self._id = id
        self._name = self._id
        self._level = random.randrange(min(level), max(level))
        self._range = level

        #statblock
        self._stats = {
            "str": 10,
            "dex": 10,
            "con": 10,
            "int": 10,
            "wis": 10,
            "cha": 10,
            "evasion": 9,
            "damage-taken-multiplier": 1
        }
        #calculated stats
        self._max_hp = 8 + self.bonus("con")
        self._hp = self._max_hp

        self._max_ap = 1 + self._level // 5
        self._ap = self._max_ap

        self._damage = 0
        self._evasion = self._stats["evasion"] + self.bonus("dex")
        self._armor= 0

        self._dc = 10

        self._loot = {
            "gold": 0,
            "xp": 0,
            "drops": None
        }

        # %hp threshold at which the enemy flees, higher == more cowardly
        self._flee_threshold = 15 - self.bonus("cha") * 2
        self._player = global_variables.PLAYER

        self._status_effects = set()
        self._applied_status_effects = set()

        self.update()

    #properties
    @property
    def id(self) -> str:
        return self._id
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
    def name(self) -> str:
        return self._name
    @property
    def dc(self) -> int:
        return self._dc
    @property
    def max_ap(self) -> int:
        return self._max_ap
    @property
    def ap(self) -> int:
        return self._ap
    @property
    def can_act(self) -> int:
        return self._ap > 0
    @property
    def fleeing(self) -> bool:
        return self._hp <= self._max_hp * (self._flee_threshold / 100)
    @property
    def range(self) -> int:
        return self._range
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
        
        return roll + self.bonus("dex") + self._level // 5
    
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
        return random.randrange(1, self._damage) + self.bonus("str")
    
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

        return global_commands.probability(50)
        
    def attack_of_oppurtunity(self, target) -> bool:
        
        if self.roll_attack() - 2 >= target.evasion:
            return True
        return False

    def set_level(self, level:int)-> None:
        """
        Sets the mobs levels then calculates HP and loot based on level
        """
        self._level = level
        self.level_up()

    def update(self):
        """
        Updates all relevant stats when a mob's level is changed
        """
        self._loot["gold"] = self._loot["gold"] * max(self._level // 2, 1)
        self._loot["xp"] = self._loot["xp"] * max(self._level // 2, 1)

        self._max_ap = 1 + self._level // 5
        self._ap = self._max_ap

    def level_up(self):
        for _ in range(self._level-1):
            self._max_hp += random.randrange(1, self._max_hp) + round(self._level + 0.1 / 2)
            self._hp = self._max_hp
        self.update()
    
    def bonus(self, stat:str) -> int:
        return player.BONUS[self._stats[stat]]

    def special(self):
        raise NotImplementedError
    
    def trigger(self):
        return False
