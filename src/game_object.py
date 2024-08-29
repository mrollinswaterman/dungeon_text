#Game Object class
import enum
from typing import Any
import global_commands

class Damage_Type(enum.Enum):
    TRUE = 0
    PHYSICAL = 1
    MAGIC = 2

class Game_Object():

    def __init__(self, id="Game Object"):
        from items import Item, Weapon, Armor
        from status_effect import Status_Effect
        self.id = id
        self.name = self.id

        self.level = 1

        self.stats:dict[str: Any] = {
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
            "max_ap": 1,
            "max_mp": 0,
            "temp_hp": None,
        }

        self.stats["max_hp"] = 10 + self.bonus("con")
        self.hp = self.max_hp
        self.ap = self.max_ap

        self.xp = 0
        self.gold = 0

        self.inventory:dict[str, Item] = {}
        self.weapon: Weapon | None = None
        self.armor: Armor | int | None = None

        self.status_effects:dict[str: Status_Effect] = {}

        self.damage_type:Damage_Type = Damage_Type(1)

    #PROPERTIES
    @property
    def dead(self) -> bool:
        """Checks if the Object is alive or not"""
        return self.hp <= 0
    
    @property
    def max_hp(self) -> int:
        """Returns the Object's max hp value from it's statblock"""
        return self.stats["max_hp"]
    
    @property
    def max_ap(self) -> int:
        """Returns the Object's max action point value from it's statblock"""
        return self.stats["max_ap"]
    
    @property
    def max_mp(self) -> int:
        """Returns the Object's max magic point value from it's statblock"""
        return self.stats["max_mp"]
    
    @property
    def damage_taken_multiplier(self):
        return self.stats["damage_taken_multiplier"]

    @property
    def damage_multiplier(self):
        return self.stats["damage_multiplier"]
    
    @property
    def caster_level(self) -> int:
        return 1 + (self.level // 5)

    @property
    def evasion(self) -> int:
        return self.stats["base_evasion"] + self.bonus("dex")
    
    @property
    def needs_healing(self):
        return self.hp < self.max_hp
    
    @property
    def can_act(self) -> bool:
        """Checks if the Object can act (ie AP > 0)"""
        return self.ap > 0 and not self.dead
    
    @property
    def target(self):
        """Returns the Object's target"""
        raise NotImplementedError

    #METHODS
    def bonus(self, stat:str) -> int:
        return global_commands.bonus(self.stats[stat])

    #ROLLS
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

    def roll_to_hit(self):
        roll = global_commands.d(20)

        if roll == 1:
            return 1
        if roll == 20:
            return 0
        
        return roll + self.bonus("dex") + (self.level // 5)
    
    def roll_damage(self):
        raise NotImplementedError

    #MODIFY RESOURCES
    def lose_hp(self, num:int):

        num = int(num)
        self.hp -= num

    def heal(self, num:int):
        """Heals the Object for num amount"""
        self.hp += num

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        self.heal_narration(num)

    def heal_narration(self, num:int):
        """Handles specific narration for Object's healing"""
        raise NotImplementedError

    def spend_ap(self, num=1) -> bool:
        """
        Spends Action points equal to num, 0 spends max AP points
        """
        if num == 0 and self.ap == self.max_ap:
            self.ap = 0
        elif num == 0:
            return False
        elif self.can_act:
            self.ap -= num
        else:
            raise ValueError(f"Not enough AP. {num} required, and only {self.ap} available!")

        return True

    def reset_ap(self) -> None:
        self._ap = self.stats["max_ap"]

    def modify_stat(self, stat, num):
        self.stats[stat] += num

    def gain_gold(self, num:int) -> int:
        self.gold += num
        return self.gold

    def lose_gold(self, num:int) -> int:
        """Takes an amount of gold from the Object, up to their total gold. Returns the amount of gold lost"""

        if (self.gold - num) >= 0:
            self.gold -= num
            return num
        else:
            g = self._gold
            self._gold = 0
            return g

    def set_level(self, num:int) -> None:
        self.level = num

    def take_damage(self, taken:int, src):
        from items import Item, Armor
        src: Item | Game_Object | str = src

        taken *= self.stats["damage_taken_multiplier"]
        taken = int(taken)

        match src:
            case Game_Object() | Item():
                if src.damage_type.name == "PHYSICAL":
                    final = 0
                    match self.armor:
                        case Armor(): final -= self.armor.armor_value
                        case _: final -= self.armor
            case _:
                final = taken

        self.lose_hp(final)
        self.take_damage_narration(final, src)

    #INVENTORY
    def pick_up(self, item, silent=False):
        """Adds an item to the Object's inventory"""

        from items import Item, Consumable, Resource
        item:Item = item

        match item:
            case Consumable() | Resource():
                #if you have a stack of those items already
                held:Consumable | None = self.get_item(item.id)
                if held is not None:
                    held.increase_quantity(item.quantity)
                    item = held
                #if you don't
                else:
                    self.inventory[item.id] = item
            case Item():
                self.inventory[item.id] = item
            case _:
                raise ValueError(f"Unrecognized object {item}.")

        item.set_owner(self)
        if not silent: global_commands.type_text(item.pickup_message)
    
    def drop(self, item):
        from items import Item
        item:Item = self.get_item(item)
        
        if item is not None:
            del self.inventory[item.id]
            item.set_owner(None)

    def get_item(self, ref):
        """
        Checks if the Object has an item in it's inventory. 
        Returns the item if so, else None

        ref: can be str (item id), int (item index), or an instance of the Item class
        """

        from items import Item
        ref:Item | str | int | None = ref

        match ref:
            case str():
                try: return self.inventory[ref]
                except KeyError: return None

            case int():
                try: return list(self.inventory.values())[ref]
                except IndexError: return None

            case Item():
                try: return self.inventory[ref.id]
                except KeyError: return None

            case _: raise ValueError(f"Unrecogized type '{type(ref)}'.")