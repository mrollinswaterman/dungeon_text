import random
import os
import csv
import items
import global_commands
from event import Event
import status_effects

HP_POT = None
FIREBOMB = None

ITEM_TYPES = {
    "Weapon": items.Weapon,
    "Armor": items.Armor,
    "Item": items.Item,
    "Consumable": items.Consumable,
    "Health_Potion": items.Health_Potion,
    "Firebomb": items.Firebomb
}

class Player():

    def __init__(self, id: str="Player", name:str = "New Player"):
        self._id = id
        self._name = name
        self._level = 1

        self._stats = {
            "str": 12,
            "dex": 12,
            "con": 12,
            "int": 12,
            "wis": 12,
            "cha": 12,
            "base_evasion": 9,
            "damage_taken_multiplier": 1,
            "damage_multiplier": 1,
            "max_hp": 0,
            "max_ap": 1 + (self._level // 5)
        }

        self._stats["max_hp"] = 10 + self.bonus("con")
        self._hp = self.max_hp
        self._ap = self.max_ap
        
        #xp/gold/items
        self._xp = 0
        self._gold = 0
        self._inventory:dict[str, items.Item] = {}
        self._status_effects:dict[str, status_effects.Status_Effect] = {}
        self._level_up_function = None

        #equipment
        self._equipped = {
            "Weapon": None, 
            "Armor": None
        }

    #properties
    @property
    def dead(self) -> bool:
        return self._hp <= 0
    @property
    def stats(self) -> int:
        return self._stats
    @property
    def level(self) -> int:
        return self._level
    @property
    def hp(self) -> int:
        return self._hp
    @property
    def max_hp(self):
        return self._stats["max_hp"]
    @property
    def max_ap(self):
        return self._stats["max_ap"]
    @property
    def xp(self):
        return self._xp
    @property
    def armor(self) -> items.Armor:
        return self._equipped["Armor"]
    @property
    def weapon(self) -> items.Weapon:
        return self._equipped["Weapon"]
    @property
    def evasion(self):
        return self._stats["base_evasion"] + self.bonus("dex")
    @property
    def carrying_capacity(self) -> int:
        return int(5.5 * self._stats["str"])
    @property
    def needs_healing(self):
        return self._hp < self.max_hp
    @property
    def damage_type(self) -> str:
        return "Physical"
    @property
    def current_weight(self) -> int:
        total_weight = 0
        for entry in self._inventory:
            if self._inventory[entry] is not None:#check to make sure the entry is valid
                held_item:items.Item = self._inventory[entry]
                total_weight += held_item.total_weight
        for item in self._equipped:
            if self._equipped[item] is not None: #check to make sure an item is equipped, add its weight to the total if it is
                total_weight += self._equipped[item].weight
        return total_weight
    @property
    def gold(self):
        return self._gold
    @property
    def inventory(self) -> dict:
        return self._inventory
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def damage_taken_multiplier(self):
        return self._stats["damage_taken_multiplier"]
    @property
    def damage_multiplier(self):
        return self._stats["damage_multiplier"]
    @property
    def max_hp(self):
        return self._stats["max_hp"]
    @property
    def threat(self):
        """
        Returns the player's current threat level which effect mob spawns
        """
        if int(self._level * 1.5) == 1:
            return 2
        return int(self._level * 1.5)
    @property
    def can_level_up(self):
        """
        Checks if the player has enough XP to level up
        """
        return self.xp >= (15 * self._level)
    @property
    def status_effects(self):
        return self._status_effects
    @property
    def equipped(self):
        return self._equipped
    @property
    def ap(self) -> None:
        return self._ap
    @property
    def can_act(self) -> bool:
        """
        Checks if the player can act (ie AP > 0)
        """
        return self._ap > 0 and not self.dead

    #STATUS
    def bonus(self, stat:str) -> int:
        return global_commands.bonus(self._stats[stat])
    
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
        weapon:items.Weapon = self._equipped["Weapon"]
        if weapon.broken is True:
            raise ValueError("Weapon is broken")
        roll = global_commands.d(20)#rolls a d20
        match roll:
            case 1:
                return 1
            case 20:
                return 0
            case _:
                return roll + self.bonus("dex")
            
    def roll_damage(self) -> int:
        """
        Returns a damage roll (weapon dice + str bonus)
        """
        weapon:items.Weapon = self._equipped["Weapon"]
        if weapon.broken:
            global_commands.type_text(f"You can't use a broken {weapon.id}, so your hands will have to do.")
            return (global_commands.d(4) + self.bonus("str")) * self.damage_multiplier
        
        weapon.lose_durability()
        return (weapon.roll_damage() + self.bonus("str")) * self.damage_multiplier

    def roll_a_check(self, stat: str) -> int:
        """
        Returns a check with a given stat (d20 + stat bonus)
        """
        roll = global_commands.d(20)
        match roll:
            case 1:
                return 1
            case 20:
                return 0
            case _:
                return roll + self.bonus(stat)
    
    def take_damage(self, taken: int, src, armor_piercing=False) -> int:
        """
        Reduces the players hp by a damage amount, reduced by armor
        """
        if armor_piercing is True:
            self._hp -= int(taken)
            strings = [
            f"You took {taken} from the {src.damage_header}.",
            f"The {src.damage_header} dealt {taken} damage to you."]
            global_commands.type_text(random.choice(strings))
            return taken

        armor:items.Armor = self._equipped["Armor"]
        taken *= self.damage_taken_multiplier

        if src.damage_type == "Physical" or src.damage_type is None:
            if armor.broken is False:
                armor.lose_durability()
                if (taken - self.armor.armor_value) <= 0:
                    strings = [
                        f"You took no damage from the {src.damage_header}!",
                        f"The {src.damage_header} did no damage to you!"]
                    global_commands.type_text(random.choice(strings))
                    return 0 
                else:
                    self._hp -= (taken - self.armor.armor_value)
                    strings = [
                        f"You took {taken - self.armor.armor_value} damage from the {src.damage_header}.",
                        f"The {src.damage_header} dealt {taken - self.armor.armor_value} to you."]
                    global_commands.type_text(random.choice(strings))
                    return taken - self.armor.armor_value
            else:
                global_commands.type_text(f"Broken {armor.id} does you no good...")

        self._hp -= taken
        strings = [
            f"You took {taken} from the {src.damage_header}.",
            f"The {src.damage_header} dealt {taken} damage to you."]
        global_commands.type_text(random.choice(strings))
        return taken

    def lose_hp(self, num:int) -> None:
        self._hp -= num

    #RESOURCES
    def level_up(self, stat: str) -> None:
        """
        Levels up a given stat
        """
        self._stats[stat] += 1
        self._xp -= 15 * self._level
        self._level += 1
        prev_max = self.max_hp
        self._stats["max_hp"] += (global_commands.d(10) + self.bonus("con"))
        if self._hp == prev_max:# ie, you were full HP before level up
            self._hp = self.max_hp
        if self._hp < (prev_max * .5): #if you were under 1/2 HP, heal to 1/2 HP
            self._hp = (self.max_hp * 0.5)

    def gain_xp(self, xp:int) -> None:
        """
        Increases player XP by a given amount
        """
        if xp <= 0:
            return None
        global_commands.type_text(f"{xp} XP earned.")
        self._xp += xp

        if self.can_level_up is True:
            self._level_up_function()
    
    def gain_gold(self, gold:int, silently:bool=False) -> None:
        """
        Increases player gold by a given amount
        """
        if gold <= 0:
            return None
        if silently is False:
            global_commands.type_text(f"{gold} Gold gained.")
        self._gold += gold

    def spend_gold(self, gold:int) -> bool:
        """
        Reduces player gold by a given amount
        Throws a value error if the player doesnt have enough gold to spend
        """
        if gold > self.gold:   
            return False
        self._gold -= gold
        global_commands.type_text(f" {gold} gold spent. {self._gold} gold remaining.")
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

    def spend_ap(self, num=1) -> None:
        """
        Spends Action points equal to num
        """
        if num == 0:
            self._ap = 0
        elif self.can_act:
            self._ap -= num
        else:
            raise ValueError(f"You don't have {num} AP to spend.")
        return None

    def reset_ap(self) -> None:
        self._ap = self._stats["max_ap"]

    def change_name(self, name:str) -> None:
        self._name = name

    def heal(self, healing: int) -> None:
        """
        Heals the player for a given amount
        """
        if self._hp <= (self.max_hp - healing):
            self._hp += healing
            global_commands.type_text(f"You healed {healing} HP.")
            return None
        if self._hp + healing > self.max_hp:
            self._hp = self.max_hp
            if self.max_hp == self._hp:#if you were already full HP, say nothing
                return None
            global_commands.type_text(f"You only healed {self.max_hp - self._hp} HP.")
            return None

    #INVENTORY STUFF
    def pick_up(self, item: items.Item | items.Consumable, silently:bool = False) -> bool:
        """
        Picks up an item if the player has inventory space for it
        """
        if item is None:
            return False
        if self.can_carry(item):
            if self.has_item(item) is True and item.is_consumable is True:
                held_item:items.Consumable = self._inventory[item.id]
                held_item.increase_quantity(item.quantity)
                if silently is False:
                    print(held_item.pickup_message)
                return True
            self._inventory[item.id] = item
            item.set_owner(self)
            if silently is False:
                print(item.pickup_message)
            return True
        else:
            if silently is False:
                global_commands.type_text("Not enough inventory space\n")
        
    def drop(self, item: items.Item) -> None:
        """
        Drops an item out of the player's inventory
        """
        if item.id in self._inventory:
            del self._inventory[item.id]
            item.set_owner(None)
        else:
            raise ValueError("Can't drop an item you don't have.\n")

    def equip(self, item: "items.Item", silently=False) -> bool:
        """
        Equips the player with a given weapon
        """
        if item.type in self._equipped:
            prev:items.Item = self._equipped[item.type]
            if prev is not None and prev.id != item.id:#if its not none and not the same item, swap it to inventory
                self._inventory[prev.id] = prev
            if item.id in self._inventory and item == self._inventory[item.id]:
                del self._inventory[item.id]
            if silently is False:
                print(f" {item.name} equipped.")
            if item.type == "Armor":
                self.equip_armor(item)
                return True
            self._equipped[item.type] = item
            return True
        return False

    def equip_armor(self, armor: "items.Armor") -> None:
        """
        Same as above but for armor
        """
        self._equipped["Armor"] = armor

        if self.bonus("str") + 1 < armor.numerical_weight_class:
            print("too-heavy")
            armor_debuff = status_effects.Stat_Debuff(armor, self)#armor is src, self is target
            armor_debuff.set_stat("dex")
            armor_debuff.set_id("Maximum Dexterity Bonus")#placeholder id --> just a flag to find and remove it when equipped armor changes
            armor_debuff.set_potency((armor.numerical_weight_class - 2))
            armor_debuff.set_duration(1000000000000)
            self.add_status_effect(armor_debuff, True)

    def can_carry(self, item:items.Item) -> bool:
        """
        Checks if the player can carry item 

        Returns True if they can, False if not
        """
        return self.current_weight + item.total_weight <= self.carrying_capacity

    def has_item(self, item: items.Item) -> bool:
        """
        Checks if a player has an item in their inventory

        Return the item if its there and False if not
        """

        if item is None:
            return False

        if item.id in self._inventory:
            if item.is_consumable:
                return True    
            try:
                return item == self._inventory[item.id]
            except KeyError:
                return False
    
    def find_item_by_name(self, name:str) -> items.Item:
        """
        Finds an item in the player's inventory by it's name

        Returns the item, None if not found
        """
        for entry in self._inventory:
            held_item: items.Item = entry
            if held_item.name == name:
                return entry
            
        return None

    def print_inventory(self) -> None:
        """
        Prints the contents of the player's inventory
        """
        for idx, item in enumerate(self._inventory):
            print(f" {idx+1}. {self._inventory[item]}")

        print(f"Carrying Capacity: {self.current_weight}/{self.carrying_capacity}\n")

    def recieve_reward(self, reward:dict) -> None:
        for entry in reward:
            match entry:
                case "gold":
                    self.gain_gold(reward[entry])
                case "xp":
                    self.gain_xp(reward[entry])
                case "drop":
                    for item in reward[entry]:
                        self.pick_up(item)        
        return None

    #STATUS EFFECTS / MODIFY STAT FUNCTIONS

    def modify_stat(self, stat, num):
        self._stats[stat] += num

    def add_status_effect(self, effect:"status_effects.Status_Effect", silent=False) -> None:
        """
        Adds a status effect to the player's status effect list and applies it
        """
        
        if effect.id in self._status_effects:#if effect already in status_effects
            applied = self._status_effects[effect.id]
            applied.additional_effect(effect)#...apply the effect's additional_effect function
        else:
            self._status_effects[effect.id] = effect
            effect.apply()
        return None

    def remove_status_effect(self, effect:"status_effects.Status_Effect") -> bool:
        if effect.id in self._status_effects:
            del self._status_effects[effect.id]
            effect.cleanse()
            return True
        else:
            return False

    def update(self) -> None:
        removed = []
        self.reset_ap()
        for entry in self._status_effects:
            effect:status_effects.Status_Effect = self._status_effects[entry]
            effect.update()
            if effect.active is False:
                #removes effect
                removed.append(effect)
                #break

        for effect in removed:
            self.remove_status_effect(effect)

    def cleanse_all(self):
        inactive = []
        for entry in self._status_effects:
            inactive.append(self._status_effects[entry])
        
        for effect in inactive:
            self.remove_status_effect(effect)

    def save_to_dict(self) -> dict:
        self.cleanse_all()#for now, cleanse all status effects before saving
        player_tod = {
            "name": self._name,
            "level": self._level
        }
        for stat in self._stats:
            player_tod[stat] = self._stats[stat]
        player_tod["hp"] = self._hp
        player_tod["xp"] = self._xp
        player_tod["gold"] = self._gold 

        return player_tod
    
    def load(self, stats_file, inventory_file) -> None:
        #set values to save file values
        with open(stats_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._name = row["name"]
                self._level = int(row["level"])
                for i in range(2, 13):#magic number, the range of 
                #loaded values that corresponds to the player's stats dictionary
                    key = list(row.keys())[i]
                    self._stats[key] = int(row[key])
                self._hp = int(row["hp"])
                self._xp = int(row["xp"])
                self._gold = int(row["gold"])
                self.reset_ap()
                
        self.load_inventory(inventory_file)
    
    def load_inventory(self, filename) -> None:
        self._inventory = {}
        size = 0
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                size += 1
            file.close()
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                if row["type"] in ITEM_TYPES:
                    item:items.Item = ITEM_TYPES[row["type"]](row["rarity"])
                    item.save()
                    with open("temp.csv", "w", newline='') as temp_file:
                        temp_file.truncate(0)
                        w = csv.DictWriter(temp_file, fieldnames=list(item.tod.keys()))
                        w.writeheader()
                        w.writerow(row)
                        temp_file.close()

                    item.load("temp.csv")
                if idx == size - 2 or idx == size - 1:#if item is equipped weapon or armor
                    self.equip(item, True)
                else:
                    self.pick_up(item, True)
            file.close()

        if os.path.exists("temp.csv"):
            os.remove("temp.csv")
        else:
           pass

# arush wrote this while drunk, he won't let me delete it
class bitch(Event):
    def __init__(self, num_bitches: int):
        var: str = "bitch"
        self.bitches = num_bitches
        return f"miles has {self.bitches} {var}s"
