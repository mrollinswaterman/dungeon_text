import random
from typing import Union
import global_variables, global_commands
import player
import status_effects

default = {
    "hit_dice": 8,
    "str": 10,
    "dex": 10,
    "con": 10,
    "int": 10,
    "wis": 10,
    "cha": 10,
    "base_evasion": 9,
    "damage_taken_multiplier": 1,
    "damage_multiplier": 1,
    "max_hp": 0,
    "max_ap": 1,
    "armor": 0,
    "damage": 5,
    "dc": 10,
    "loot": {
        "gold": 0,
        "xp": 0,
        "drops": []
    }
}

class Mob():

    def __init__(self, id:str="Anonymous_Mob", level:tuple= (1, 20), statblock=None):
        #identification
        self._id = id
        self._name = self._id
        self._level = random.randrange(min(level), max(level)+1)
        self._range = level

        self._stats = {}

        #if no statblock, use default
        if not statblock:
            print("No statblock given.\n")
            statblock = default

        #copy statblock items to self._stats
        for entry in statblock:
            self._stats[entry] = statblock[entry]

        #copy loot info to self._stats
        self._loot = {}
        for item in self._stats["loot"]:
            self._loot[item] = self._stats["loot"][item]

        #calculate stats
        self.calculate_hp()
        self._stats["max_ap"] = 1 + (self._level // 5)
        self._ap = self.max_ap

        # percent current HP threshold at which the enemy tries to flee (higher==more cowardly)
        self._flee_threshold = 0.2
        self._player:player.Player = global_variables.PLAYER

        self._status_effects: dict[str, status_effects.Status_Effect] = {}
        self._applied_status_effects = set()

        #tracks if the header for the turn has been printed yet
        self._header_printed = False

        self.update()
        self.calculate_loot()

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
        return self._stats["damage"]
    @property
    def evasion(self) -> int:
        return self._stats["base_evasion"] + self.bonus("dex")
    @property
    def armor(self) -> int:
        return self._stats["armor"]
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
    def damage_multiplier(self):
        return self._stats["damage_multiplier"]
    @property
    def damage_taken_multiplier(self):
        return self._stats["damage_taken_multiplier"]
    @property
    def dc(self) -> int:
        return self._stats["dc"]
    @property
    def max_hp(self) -> int:
        return self._stats["max_hp"]
    @property
    def max_ap(self) -> int:
        return self._stats["max_ap"]
    @property
    def ap(self) -> int:
        return self._ap
    @property
    def can_act(self) -> int:
        return self._ap > 0
    @property
    def fleeing(self) -> bool:
        return self._hp <= self.max_hp * self._flee_threshold and self.roll_a_check("cha") > 10
    @property
    def range(self) -> int:
        return self._range
    @property
    def stats(self) -> dict:
        return self._stats
    @property
    def header(self) -> bool:
        return self._header_printed
    
    #methods

    #MISC.
    def bonus(self, stat:str) -> int:
        """
        Returns the numerical bonus of the given stat
        """
        return global_commands.bonus(self._stats[stat])
    
    def calculate_hp(self) -> None:
        """
        Re-calculates mob's HP based on current level,
        then sets stats['hp'] and self._hp variables appropriately
        """
        self._stats["max_hp"] = 0
        temp = self._stats["hit_dice"] + self.bonus("con")
        for _ in range(self._level-1):
            temp += global_commands.d(self._stats["hit_dice"]) + self.bonus("con")

        self._stats["max_hp"] = temp
        self._hp = self.max_hp

    def set_header(self, val:bool) -> None:
        self._header_printed = val

    #ROLLS
    def roll_attack(self) -> int:
        """
        Rolls an attack (d20)
        """
        roll = global_commands.d(20)

        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll + self.bonus("dex") + (self._level // 5)

    def roll_a_check(self, stat:str):
        return global_commands.d(20) + self.bonus(stat)
    
    def roll_damage(self) -> int:
        """
        Rolls damage (damage dice)
        """
        return global_commands.d(self.damage) * self.damage_multiplier + self.bonus("str")
    
    def take_damage(self, damage:int, armor_piercing=False) -> int:
        """
        Takes a given amount of damage, reduced by armor
        """
        damage *= self.damage_taken_multiplier
        if armor_piercing:
            self._hp -= damage
            return damage

        if (damage - self.armor) < 0:
            return 0
        else:
            self._hp -= damage - self.armor
            return damage - self.armor
        
    def fumble_table(self) -> Union[str, bool]:
        """
        Determines if a mob sufferes a negative effect upon rolling a nat 1.
        """
        return global_commands.probability(50)
        
    def attack_of_oppurtunity(self) -> bool:
        """
        Rolls an attack of opportuity against the player
        """
        if self.roll_attack() - 2 >= self._player.evasion:
            return True
        return False
    
    #Resources
    def heal(self, num:int) -> None:
        #heals for the given amount up to max hp value
        self._hp += self._hp + num if (self._hp + num <= self.max_hp) else self.max_hp

    def spend_ap(self, num:int=1) -> None:
        """
        Spend an amount of AP
        """
        if num == 0:#spend_ap(0) indicates a full round action, uses all AP
            self._ap = 0
            return None
        if self.can_act is True:
            self._ap -= 1
        else:
            raise ValueError("No AP to spend")
        
    def reset_ap(self):
        """
        Resets mob's AP to max value
        """
        self._ap = self.max_ap
    
    #STATUS EFFECTS
    def add_status_effect(self, effect:status_effects.Status_Effect) -> None:
        """
        Adds a status effect to the mob
        """
        if effect.id in self._status_effects:
            #if we have the effect already, kick out of the function
            return None
        self._status_effects[effect.id] = effect
        effect.apply()

    def remove_status_effect(self, effect:status_effects.Status_Effect) -> None:
        """
        Removes a status effect from the mob
        """
        del self._status_effects[effect.id]
        effect.cleanse()
        return None

    #Updates
    def calculate_loot(self):
        """
        Adds a random extra amount of XP and Gold per level it is above base
        to the mob's loot pool
        """
        for _ in range(self._range[0], self._level+1):
            x_gold = global_commands.d(6) 
            x_xp = global_commands.d(6)
            self._loot["gold"] += x_gold * self._level // 3
            self._loot["xp"] += x_xp * max(self._level // 5, 1)

    def update(self):
        """
        Updates all relevant stats when a mob's level is changed,
        updates status effects and removes them when their duration
        expires. 
        """
        self.reset_ap()
       
        #update all status effects
        inactive = []
        for entry in self._status_effects:
            effect: status_effects.Status_Effect = self._status_effects[entry]
            effect.update()
            if effect.active is False:
                inactive.append(effect)
        for effect in inactive:
            self.remove_status_effect(effect)
        inactive = []

    def special(self):
        raise NotImplementedError
    
    def trigger(self):
        return False
