import random
import items
import global_commands
from events import Event

BONUS = {
    5: -4,
    6: -3,
    7: -2,
    8: -1, 
    9: -1,
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

TAG_TO_STAT = {
    "str": "Strength",
    "dex": "Dexterity",
    "con": "Constitution",
    "int": "Intelligence",
    "wis": "Wisdom",
    "cha": "Charisma",
    "evasion": "Evasion",
    "damage-taken-multiplier": "Vulnerability"
}

class Status_Effect():

    def __init__(self, id:str, src, stat: str, target, power:int = 0, duration: int = 0):
        #SRC is a player or mob object
        self._id = id
        self._src = src
        self._power = power
        self._duration = duration
        self._stat = stat
        self._target = target
        self._message = ""
        self._change = "increased"
        if self._power < 0:
            self._change = "decreased"
        self._active = True

    #properties
    @property
    def id(self) -> str:
        return f"{self._src.name}'s {self._id}"
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
    def target(self):
        return self._target
    @property
    def message(self):
        return self._message
    @property
    def active(self):
        return self._active
    
    #methods
    def update(self) -> None:
        self._duration -= 1
        if self._duration <= 0:
            self._active = False

    def set_power(self, num:int) -> None:
        self._power = num
        if self._power < 0:
            self._change = "decreased"

    def set_duration(self, num:int) -> None:
        self._duration = num

    def set_message(self, msg:str) -> None:
        self._message = msg


class Player():

    def __init__(self, id: str="Player", name:str = ""):
        self._id = id
        self._name = name

        #statblock
        self._stats = {
            "str": 12,
            "dex": 12,
            "con": 12,
            "int": 12,
            "wis": 12,
            "cha": 12,
            "evasion": 12 + BONUS[12],
            "damage-taken-multiplier": 1
        }

        #calculated stats
        self._max_hp = 8 + BONUS[self._stats["con"]]
        self._hp = self._max_hp

        #xp/gold/items
        self._xp = 0
        self._level = 1
        self._gold = 0
        self._inventory = []
        self._status_effects:list[Status_Effect] = []
        self._level_up_function = None
        
        #static stats
        self._max_ap = 1 + (self._level // 5)
        self._ap = self._max_ap
        self._damage_taken_multiplier = 1

        #equipment
        self._equipped = {
            "Weapon" : None, 
            "Armor": None
        }

    #properties
    @property
    def dead(self) -> bool:
        """
        Checks if the player is dead (ie HP <= 0)
        """
        return self._hp <= 0
    @property
    def level(self) -> int:
        return self._level
    @property
    def str(self) -> int:
        return self._stats["str"]
    @property
    def dex(self) -> int:
        return self._stats["dex"]
    @property
    def con(self) -> int:
        return self._stats["con"]
    @property
    def int(self) -> int:
        return self._stats["int"]
    @property
    def wis(self) -> int:
        return self._stats["wis"]
    @property
    def cha(self) -> int:
        return self._stats["cha"]
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def xp(self):
        return self._xp
    @property
    def armor(self) -> items.Armor:
        """
        Returns player's armor value, proably should be an object too
        """
        return self._equipped["Armor"]
    @property
    def weapon(self) -> items.Weapon:
        """
        Returns player's weapon object
        """
        return self._equipped["Weapon"]
    @property
    def evasion(self):
        return self._stats["evasion"]
    @property
    def carrying_capacity(self) -> int:
        return int(5.5 * self._stats["str"])
    @property
    def current_weight(self) -> int:
        total_weight = 0
        for entry in self._inventory:
            held_item:items.Item = entry
            total_weight += held_item.total_weight
        for item in self._equipped:
            total_weight += self._equipped[item].weight
        return total_weight
    @property
    def gold(self):
        return self._gold
    @property
    def inventory(self) -> dict:
        return self._inventory
    @property
    def inventory_size(self) -> int:
        return len(self._inventory) + 1
    @property
    def id(self):
        return self._id
    @property
    def max_hp(self):
        return self._max_hp
    @property
    def threat(self):
        """
        Returns the player's current threat level which effect mob spawns
        """
        if int(self._level * 1.5) == 1:
            return 2
        return int(self._level * 1.5)
    @property
    def level_up(self):
        """
        Checks if the player has enough XP to level up
        """
        return self.xp > (15 * self._level)
    @property
    def status_effects(self):
        return self._status_effects
    @property
    def max_ap(self) -> None:
        """
        Returns max AP value
        """
        return self._max_ap
    @property
    def ap(self) -> None:
        """
        Returns current Action Point value
        """
        return self._ap
    @property
    def can_act(self) -> bool:
        """
        Checks if the player can act (ie AP > 0)
        """
        return self._ap > 0

    #methods


    #STATUS
    def bonus(self, stat) -> int:
        if isinstance(stat, str):
            return BONUS[self._stats[stat]]
        return BONUS[stat]
    
    def die(self) -> None:
        """
        Kils the player. Lose gold and inventory on death
        """
        self._gold = 0
        self._inventory = []
        #other stuff to be added
    def set_level_up_function(self, func) -> None:
        self._level_up_function = func

    def set_level(self, num:int) -> None:
        self._level = num


    #ROLLS
    def roll_attack(self) -> int:
        """
        Returns an attack roll (d20 + dex bonus)
        """
        roll = random.randrange(1,20)
        if roll == 1:
            return 1
        if roll == 20:
            return 0

        weapon:items.Weapon = self._equipped["Weapon"]
        if weapon.broken is True:
            raise ValueError("Weapon is broken")

        return roll + self.bonus(self.dex)
            
    def roll_damage(self) -> int:
        """
        Returns a damage roll (weapon dice + str bonus)
        """
        weapon:items.Weapon = self._equipped["Weapon"]
        weapon.lose_durability()
        weapon_damage = 0
        for _ in range(weapon.num_damage_dice):
            weapon_damage += random.randrange(1, weapon.damage_dice)
        return weapon_damage + self.bonus(self.str)

    def roll_a_check(self, stat: str) -> int:
        """
        Returns a check with a given stat (d20 + stat bonus)
        """
        return random.randrange(1, 20) + BONUS[self._stats[stat]]
    
    def take_damage(self, damage: int) -> int:
        """
        Reduces the players hp by a damage amount, reduced by armor
        """
        armor:items.Armor = self._equipped["Armor"]
        damage = damage * self._damage_taken_multiplier
        if armor.broken is False:
            armor.lose_durability()
            if damage - self.armor.armor_value < 0:
                return 0 
            else:
                self._hp -= damage - self.armor.armor_value
                return damage - self.armor.armor_value
        self._hp -= damage
        return damage


    #RESOURCES
    def spend_xp(self, stat: str) -> None:
        """
        Levels up a given stat
        """
        self._stats[stat] += 1
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
        if xp <= 0:
            return None
        global_commands.type_text(f" {xp} XP earned.")
        self._xp += xp

        if self.level_up is True:
            self._level_up_function()
    
    def gain_gold(self, gold:int, silently:bool=False) -> None:
        """
        Increases player gold by a given amount
        """
        if gold <= 0:
            return None
        if silently is False:
            global_commands.type_text(f" {gold} Gold gained.\n")
        self._gold += gold

    def spend_gold(self, gold:int) -> bool:
        """
        Reduces player gold by a given amount

        Throws a value error if the player doesnt have enough gold to spend
        """
        if gold > self.gold:   
            return False
        self._gold -= gold
        #print(f" {gold} gold spent. {self._gold} gold remaining.\n")
        return True

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

    def spend_ap(self, num) -> None:
        """
        Spends Action points equal to num
        """
        self._ap -= num

    def reset_ap(self) -> None:
        """
        Resets Action Points to max
        """
        self._ap = self._max_ap

    def change_name(self, name:str) -> None:
        self._name = name

    def heal(self, healing: int) -> None:
        """
        Heals the player for a given amount
        """
        if self._hp <= (self._max_hp - healing):
            self._hp += healing
            global_commands.type_text(f'\n You healed {healing} HP.\n')
            return None
        if self._hp + healing > self._max_hp:
            self._hp = self._max_hp
            global_commands.type_text(f"\n You only healed {self._max_hp - self._hp} HP.\n")
            return None


    #INVENTORY STUFF
    def pick_up(self, item: items.Item | items.Consumable, silently:bool = False) -> bool:
        """
        Picks up an item if the player has inventory space for it
        """
        if item is None:
            return False
        if self.current_weight <= self.carrying_capacity and self.can_carry(item):
            if self.has_item(item) is True and item.is_consumable is True:
                index = self.find_consumable_by_id(item)
                held_item:items.Consumable = self._inventory[index]
                held_item.increase_quantity(item.quantity)
                if silently is False:
                    print(item.pickup_message)
                return True
            self._inventory.append(item)
            if silently is False:
                print(item.pickup_message)
            return True
        else:
            if silently is False:
                global_commands.type_text(" Not enough inventory space\n")
        
    def drop(self, item: items.Item) -> None:
        """
        Drops an item out of the player's inventory
        """
        if item.id in self._inventory:
            self._inventory.remove(item)
        else:
            raise ValueError("Can't drop an item you don't have.\n")

    def equip(self, item: "items.Item", silently=False) -> bool:
        """
        Equips the player with a given weapon
        """
        if item.type in self._equipped:
            if self._equipped[item.type] is not None:
                self._inventory.append(self._equipped[item.type])
            self._equipped[item.type] = item
            if item.type == "Armor":
                self.equip_armor(item)
                return True
            if item in self._inventory:
                self._inventory.remove(item)
            if silently is False:
                print(f" {item.name} equipped.")
            return True
        return False

    def equip_armor(self, armor: "items.Armor") -> None:
        """
        Same as above but for armor
        """
        try:
            self.remove_status_effect(None, "Armor Debuff")
            #self._equipped["Armor"] = armor
            #self._inventory[armor.id] = armor
        except AttributeError:
            pass

        if self.bonus("str") + 1 < armor.numerical_weight_class:
            armor_debuff = Status_Effect("Armor Debuff", armor, "dex", self)
            armor_debuff.set_power(-(armor.numerical_weight_class - 2))
            armor_debuff.set_duration(10000)
            armor_debuff.set_message(f" Your Dexterity is being decreased by 2 by your {armor.id}!\n")
            self.add_status_effect(armor_debuff)
            self._stats["evasion"] = 12 + BONUS[self._stats["dex"]]

        #self._equipped["Armor"] = armor
            
    def can_carry(self, item:items.Item) -> bool:
        return self.current_weight + item.total_weight <= self.carrying_capacity

    def has_item(self, item: items.Item) -> bool:
        """
        Checks if a player has an item in their inventory

        Return the item if its there and False if not
        """
        if item.is_consumable is True:
            for entry in self._inventory:
                held_item:items.Consumable = entry
                if held_item.id == item.id:
                    return True
            return False
        if item in self._inventory:
            return True
        return False
    
    def find_consumable_by_id(self, item: items.Consumable) -> int:
        for entry in self._inventory:
            held_item:items.Consumable = entry
            if held_item.id == item.id:
                return self._inventory.index(held_item)
        return False
    def print_inventory(self) -> None:
        """
        Prints the contents of the player's inventory
        """
        for idx, item in enumerate(self._inventory):
            print(f" {idx+1}. {item}")

        print(f"Carrying Capacity: {self.current_weight}/{self.carrying_capacity}")

    def recieve_reward(self, reward:dict) -> None:
        for entry in reward:
            if entry == "gold":
                self.gain_gold(reward[entry])
            if entry == "xp":
                self.gain_xp(reward[entry])
            if entry == "drop":
                self.pick_up(reward[entry])

    #STATUS EFFECTS / MODIFY STAT FUNCTIONS#
    def add_status_effect(self, effect:Status_Effect) -> None:
        """
        Adds a status effect to the player's status effect list
        and changes the corresponding stat
        """
        #for status in self._status_effects:
            #id, src = status.id, status.src
            #if effect.id == id and effect.src == src: --> All this code makes status effects not stack
                #print(f"The {effect.id} effect hasn't run out yet.")
                #return None
        self._stats[effect.stat] += effect.power
        self._status_effects.append(effect)
        global_commands.type_text(effect.message)

    def remove_status_effect(self, effect:Status_Effect=None, id:str="") -> None:
        if len(id) > 0 and effect is not None:
            for entry in self._status_effects:
                if entry.id == id:
                    self._stats[effect.stat] += -(effect.power)
                    self._status_effects.remove(effect)
                    global_commands.type_with_lines(f" The {effect.id}'s effect has worn off.")
                    return None
        else:
            self._stats[effect.stat] += -(effect.power)
            self._status_effects.remove(effect)
            global_commands.type_with_lines(f" The {effect.id}'s effect has gone away.")
            return None

    def update(self) -> None:
        for effect in self._status_effects:
            effect.update()
            if effect.active is False:
                #removes effect
                self.remove_status_effect(effect)


# arush wrote this while drunk, he won't let me delete it
class bitch(Event):
    def __init__(self, num_bitches: int):
        var: str = "bitch"
        self.bitches = num_bitches
        return f"miles has {self.bitches} {var}s"
