import random
import items
import global_commands
from events import Event

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

    def __init__(self, name: str=""):
        self._name = name

        #statblock
        self._strength:int = 12
        self._dexterity:int = 12
        self._constitution:int = 12
        self._intelligence:int = 12
        self._wisdom:int = 12
        self._charisma:int = 12

        #calculated stats
        self._max_hp = 8 + BONUS[self._constitution]
        self._hp = self._max_hp
        self._evasion = 12 + BONUS[self._dexterity]
        self._xp = 0
        self._level = 1
        self._gold = 0
        self._inventory = {}
        self._status_effects = []
        
        #equipment
        self._weapon: items.Weapon = None
        self._armor: items.Armor = None

        #stat-map
        self._stat_map = {
            "str": self._strength,
            "dex": self._dexterity,
            "con": self._constitution,
            "int": self._intelligence,
            "wis": self._wisdom,
            "cha": self._charisma,
            "evasion": self._evasion,
        }

    #properties
    @property
    def dead(self) -> bool:
        return self._hp <= 0
    @property
    def level(self) -> int:
        return self._level
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
    def hp(self) -> int:
        return self._hp
    @property
    def xp(self):
        return self._xp
    @property
    def armor(self) -> int:
        if self._armor.broken is True:
            return 0
        return self._armor.armor_value
    @property
    def weapon(self) -> items.Weapon:
        return self._weapon
    @property
    def evasion(self):
        return self._evasion
    @property
    def carrying_capacity(self) -> int:
        return 10 + self.bonus(self.str) + self.bonus(self.con)
    @property
    def gold(self):
        return self._gold
    @property
    def name(self):
        return self._name
    @property
    def max_hp(self):
        return self._max_hp
    @property
    def threat(self):
        """
        Returns the player's current threat level which effect mob spawns
        """
        return(self._level, self._level * 2 + 1)
    @property
    def level_up(self):
        return self.xp > (15 * self._level)
    @property
    def status_effects(self):
        return self._status_effects

    #methods
    def bonus(self, stat):
        if type(stat) == str:
            return BONUS[self._stat_map[stat]]
        
        return BONUS[stat]
    
    def roll_attack(self) -> int:
        """
        Returns an attack roll (d20 + dex bonus)
        """
        if self._weapon.broken is True:
            raise ValueError("Weapon is broken")
        
        roll = random.randrange(1,20)
        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll + self.bonus(self.dex)
            
    def roll_damage(self) -> int:
        """
        Returns a damage roll (weapon dice + str bonus)
        """
        self._weapon.lose_durability()
        return random.randrange(1, self._weapon.damage_dice) + self.bonus(self.str)

    def roll_a_check(self, stat: str) -> int:
        """
        Returns a check with a given stat (d20 + stat bonus)
        """
        return random.randrange(1, 20) + BONUS[self._stat_map[stat]]
    
    def take_damage(self, damage: int) -> int:
        """
        Reduces the players hp by a damage amount, reduced by armor
        """
        if self._armor.broken is False:
            self._armor.lose_durability()
        if damage - self.armor < 0:
            return 0 
        else:
            self._hp -= damage - self.armor
            return damage - self.armor

    def pick_up(self, item: items.Item | items.Consumable, num: int) -> None:
        """
        Picks up an item if the player has inventory space for it
        """
        if len(self._inventory) < self.carrying_capacity:
            if item.id in self._inventory:
                self._inventory[item.id].increase_quantity(num)
            else:
                self._inventory[item.id] = item
                if isinstance(item, items.Consumable):
                    self._inventory[item.id].increase_quantity(num)

        else:
            raise ValueError("Not enough inventory space")
        
    def drop(self, item: items.Item) -> None:
        """
        Drops an item out of the player's inventory
        """
        if item.id in self._inventory:
            del self._inventory[item.id]

        else:
            raise ValueError("Can't drop an item you don't have")
        
    def spend_xp(self, stat: str) -> None:
        """
        Levels up a given stat
        """
        self._stat_map[stat] += 2
        self._xp -= 15 * self._level
        self._level += 1
        prev_max = self._max_hp
        self._max_hp += random.randrange(1, 8) + BONUS[self.con]
        if self._hp == prev_max:
            self._hp = self._max_hp

        if self._hp < (prev_max // 2):
            self._hp = self._max_hp // 2
        

    def gain_xp(self, xp: int) -> None:
        """
        Increases player XP by a given amount
        """
        self._xp += xp
    
    def gain_gold(self, gold:int) -> None:
        """
        Increases player gold by a given amount
        """
        self._gold += gold

    def spend_gold(self, gold:int) -> None:
        """
        Reduces player gold by a given amount

        Throws a value error if the player doesnt have enough gold to spend
        """
        if gold > self.gold:   
            raise ValueError("Not enough gold")

        self._gold -= gold

    def lose_gold(self, amount:int) -> None:
        """
        Takes a certain amount of gold from the player, if the player doesnt
        have sufficient gold, sets gold to 0
        """
        
        if self._gold - amount >= 0:
            self._gold -= amount
            return amount

        else:
            all_i_have = self._gold
            self._gold = 0
            return all_i_have

    def die(self) -> None:
        """
        Kils the player. Lose gold and inventory on death
        """
        self._gold = 0
        self._inventory = []
        #other stuff to be added

    def change_name(self, name:str) -> None:
        self._name = name

    def equip_weapon(self, weapon: "items.Weapon") ->  None:
        """
        Equips the player with a given weapon
        """
        self._weapon = weapon
        self._inventory[weapon.id] = weapon

    def equip_armor(self, armor: "items.Armor") -> None:
        """
        Same as above but for armor
        """
        self._armor = armor
        self._inventory[armor.id] = armor

    def heal(self, healing: int) -> None:
        """
        Heals the player for a given amount
        """
        if self._hp <= (self._max_hp - healing):
            self._hp += healing
            global_commands.type_text(f'\nYou healed {healing} HP.\n')
            return None
        if self._hp + healing > self._max_hp:
            self._hp = self._max_hp
            global_commands.type_text(f"\nYou only healed {self._max_hp - self._hp} HP.\n")
            return None

    def has_item(self, item: str) -> items.Consumable | bool | items.Item:
        """
        Checks if a player has an item in their inventory

        Return the item if its there and False if not
        """
        if item in self._inventory:
            if self._inventory[item].quantity > 0:
                return self._inventory[item]
        
        return False

    def print_inventory(self) -> None:
        """
        Prints the contents of the player's inventory
        """
        for item in self._inventory:
            print(self._inventory[item])

    def add_status_effect(self, effect) -> None:
        self._stat_map[effect.stat] += effect.power
        self._status_effects.append(effect)

    def update(self) -> None:
        for effect in self._status_effects:
            effect.update()
            if effect.duration < 0:
                #removes effect
                self._stat_map[effect.stat] += -(effect.power)
                self._status_effects.remove(effect)


# arush wrote this while drunk, he won't let me delete it
class bitch(Event):
    def __init__(self, num_bitches: int):
        var: str = "bitch"
        self.bitches = num_bitches
        return f"miles has {self.bitches} {var}s"


class Status_Effect():

    def __init__(self, id:str, src, stat: str, target: Player, power:int = 0, duration: int = 0):
        #SRC is a player or mob object
        self._id = id
        self._src = src
        self._power = power
        self._duration = duration
        self._stat = stat
        self._target = target

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def src(self):
        return self._src
    @property
    def power(self) -> int:
        return self._power
    @property
    def duration(self) -> int:
        return self._duration
    @property
    def stat(self) -> str:
        return self._stat
    @property
    def target(self) -> Player:
        return self._target
    
    #methods
    def update(self) -> None:
        self._duration -= 1
    def set_power(self, num:int) -> None:
        self._power = num
    def set_duration(self, num:int) -> None:
        self._duration = num