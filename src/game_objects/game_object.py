#Game Object class

##Required Modules: globals, items
from __future__ import annotations
from multiprocessing import Value
import random, csv

import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import items

class Statblock():

    def __init__(self, parent:Game_Object):

        self.parent = parent
        self.id:str = f"{self.parent.id} Statblock"

        #Core Stats
        self.level:int = self.parent.level
        self.level_range:tuple[int, int] = (1, 20)
        self.hit_dice:int = 8

        #Ability Scores
        self.str:int = 12
        self.dex:int = 12
        self.con:int = 12
        self.int:int = 12
        self.wis:int = 12
        self.cha:int = 12

        #Derived stats
        self.base_evasion:int = 9
        self.damage_taken_multiplier:int = 1
        self.damage_multiplier:int = 1

        #Resources
        self.max_hp:int = 1
        self.max_ap:int = 1
        self.max_mp:int = 0
        self.temp_hp:int = 0
        
        #Combat Stats (mob only)
        self.armor:"items.Armor" | int | None = None
        self.damage: int | str | None = None
        self.dc:int = 0

    def value(self, stat:str) -> int | str:
        return self.__dict__[stat]
    
    def bonus(self, stat:str) -> int:
        return globals.bonus(self.__dict__[stat])
    
    def modify(self, stat:str, num:int):
        self.__dict__[stat] += num

    def load(self, filename:str):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.copy(row)
    
    def copy(self, source:dict):
        for entry in source:
            if entry in self.__dict__:
                match self.__dict__[entry]:
                    case str(): self.__dict__[entry] = source[entry]
                    case int():self.__dict__[entry] = int(source[entry])
                    case _: self.__dict__[entry] = source[entry]

class Condition_Monitor():
    def __init__(self, parent):
        self.parent:Game_Object = parent
        self._effects:dict[str, mechanics.Mechanic] = {}
        self._cleanse_pool:set[mechanics.Mechanic] = set()

    @property
    def active(self) -> list[mechanics.Mechanic]:
        return list(self._effects.values())
    
    @property
    def active_ids(self) -> list[str]:
        return list(self._effects.keys())

    def add(self, effect:mechanics.Mechanic):
        assert effect is mechanics.Mechanic()
        if effect in self.active:
            effect = self._effects[effect.id]
            effect.refresh()
        else:
            self._effects[effect.id] = effect
            effect.start()

    def update(self):
        for element in self.active:
            if element.active:
                element.update()
            if not element.active:
                self._cleanse_pool.add(element)

        self.cleanse()
    
    def cleanse(self):
        """Removes all effects in the cleanse pool from effects list,
            ending them if they are active"""
        for element in self._cleanse_pool:
            if element.active:
                element.end()
            del self._effects[element.id]

        self._cleanse_pool = set()

    def cleanse_all(self):
        """Adds all active effects to the cleanse pool, then cleases"""
        self._cleanse_pool.update(self.active)
        self.cleanse()

class Header():
    """Header class, controls which text is used to describe a GameObject
        3 types: default, action, ownership"""

    parent:Game_Object
    default:str
    action:str
    ownership:str
    damage: str

    def __init__(self, parent:Game_Object):
        self.parent = parent
        self._default = f"The {self.parent.id}"
        self._action = f"The {self.parent.id} is"
        self._ownership = f"The {self.parent.id}'s"
        self.damage = self._default

        self.prev = ""

    @property
    def default(self):
        if self.prev != self._default:
            self.prev = self._default
            return self._default
        else:
            self.prev = "It"
            return self.prev
        
    @property
    def action(self):
        if self.prev != self._action:
            self.prev = self._action
            return self._action
        else:
            self.prev = "It's"
            return self.prev

    @property
    def default(self):
        if self.prev != self._ownership:
            self.prev = self._ownership
            return self._ownership
        else:
            self.prev = "Its"
            return self.prev

class Game_Object():

    def __init__(self, id="Game Object"):

        #Core properties
        self.id = id
        self.name = self.id
        self.level = 1
        self.stats:Statblock = Statblock(self)
        self.header:Header = Header(self)

        #Derived stats
        self.stats.max_hp = 10 + self.bonus("con")
        self.hp = self.stats.max_hp
        self.ap = self.stats.max_ap

        #Resources
        self.xp = 0
        self.gold = 0

        #Items / Equipment
        self.inventory:dict[str, "items.Item"] = {}
        self.weapon: "items.Weapon" | None = None
        self.armor: "items.Armor" | int | None = None

        #Combat tools
        self.condition_monitor:Condition_Monitor = Condition_Monitor(self)
        self.damage_types:list[str] = ["Physical", "Slashing"]
        self.immunities:list[str] = [None]
        self.resistances: list[str] = [None]

        #Player Exclusive
        self.combat_trick = None
        self._bonus_crit_range = None

        #Misc.
        self.prev_narration = ""

    #PROPERTIES
    @property
    def dead(self) -> bool:
        """Checks if the Object is alive or not"""
        return self.hp <= 0
    
    @property
    def caster_level(self) -> int:
        return 1 + (self.level // 5)

    @property
    def base_attack_bonus(self) -> int:
        return max(1, self.level // 5)

    @property
    def needs_healing(self) -> bool:
        return self.hp < self.stats.max_hp
    
    @property
    def can_act(self) -> bool:
        """Checks if the Object can act (ie AP > 0)"""
        return self.ap > 0 and not self.dead
    
    @property
    def target(self) -> Game_Object:
        """Returns the Object's target"""
        raise NotImplementedError

    #METHODS
    def update(self):
        self.reset_ap()
        self.condition_monitor.update() 
        self.clean_inventory()

    def apply(self, effect:mechanics.Mechanic):
        self.condition_monitor.add(effect)

    def bonus(self, stat:str) -> int:
        return self.stats.bonus(stat)
    
    def evasion(self) -> int:
        return self.stats.base_evasion + self.bonus("dex")

    #ROLLS
    def roll_a_check(self, stat:str) -> int:
        """Returns a check with a given stat (d20 + stat bonus)"""
        roll = globals.d(20)
        match roll:
            case 1:
                return 1
            case 20:
                return 0
            case _:
                return roll + self.bonus(stat)

    def roll_to_hit(self) -> int:
        roll = globals.d(20)
        if roll == 1:
            return 1
        if roll == 20:
            return 0
        return roll + self.bonus("dex") + (self.level // 5)
    
    def roll_damage(self) -> "mechanics.DamageInstance":
        raise NotImplementedError

    #MODIFY RESOURCES
    def lose_hp(self, num:int):
        """Removes HP from the Object, starting with temp HP"""
        num = int(num)
        if self.stats.temp_hp > 0:
            self.stats.temp_hp -= num
            self.stats.temp_hp = 0 if self.stats.temp_hp < 0 else self.stats.temp_hp
        else:
            self.hp -= num

    def gain_temp_hp(self, num:int):
        """Adds temp HP to the Object. Object only gets the highest temp_hp value.
            i.e, newly added temp_hp replaces old temp_hp if it's value is higher, else it is ignored."""
        if self.stats.temp_hp > int(num):
            return None 
        else:
            self.stats.temp_hp = int(num)

    def heal(self, num:int):
        """Heals the Object for num amount"""
        self.hp += num
        if self.hp > self.stats.max_hp:
            num = num - (self.hp - self.stats.max_hp)
            self.hp = self.stats.max_hp
        self.heal_narration(num)

    def spend_ap(self, num:int=1) -> bool:
        """Spends Action points equal to num, 0 spends max AP points"""
        if num == 0 and self.ap == self.stats.max_ap:
            self.ap = 0
        elif num == 0:
            return False
        elif self.can_act:
            self.ap -= num
        else:
            raise ValueError(f"Not enough AP. {num} required, and only {self.ap} available!")
        return True

    def reset_ap(self) -> None:
        self.ap = self.stats.max_ap

    def spend_mp(self, num:int=1) -> bool:
        if num == 0:
            self.mp = 0
            return False
        if self.mp >= num:
            self.mp -= num
            return True
        return False
    
    def regain_mp(self, num:int | None=None):
        if num is None:
            self.mp = self.stats.max_mp
            return True
        self.mp += num
        return True

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

    #COMBAT
    def attack(self):
        self.spend_ap()
        roll = self.roll_to_hit()
        #probably a prettier way to do this
        if self.id == "Player":
            self.narrate(self.roll_narration, roll)
        else: self.narrate(self.roll_narration)
        self.apply_on_attacks()

        match roll:
            case 0: return self.critical_hit()

            case 1: return self.critical_fail()

            case _:
                if roll >= self.target.evasion():
                    self.narrate(self.hit_narration)
                    dealt = self.roll_damage()
                    print(f"DEALT: {dealt}")
                    self.target.take_damage(dealt)
                    self.apply_on_hits()
                else:
                    self.narrate(self.miss_narration)
                    self.apply_on_misses()
        return None
    
    def check_immunities(self, damage:"mechanics.DamageInstance") -> "mechanics.DamageInstance":
        for immunity in self.immunities:
            if immunity in damage.types:
                damage.amount = 0
                return damage
            
    def check_resistances(self, damage:"mechanics.DamageInstance") -> "mechanics.DamageInstance":
        for resist in self.resistances:
            if resist in damage.types:
                damage.amount //= 2
                return damage

    def take_damage(self, damage:"mechanics.DamageInstance") -> int:
        damage = self.check_immunities(damage)
        damage = self.check_resistances(damage)

        my_armor = 0
        match self.armor:
            case items.Armor(): my_armor = self.armor.value
            case int(): my_armor = self.armor
            case _: raise ValueError(f"unrecogized armor type '{self.armor}'\n")

        taken = int(damage.amount * self.stats.damage_taken_multiplier)

        taken -= my_armor

        if taken < 0: taken = 0

        damage.amount = taken

        self.lose_hp(taken)
        self.narrate(self.take_damage_narration, damage)

        return damage.amount

    def modify(self, stat:str, amount:int, source) -> None:
        try:
            self.stats.modify(stat, amount)
        except KeyError:
            raise ValueError(f"Can't modify non-existent stat '{stat}'.")

        text = f"{self.header.ownership} {globals.STATS[stat]} increased by {amount}."
        if amount < 0:
            text = f"{self.header.ownership} {globals.STATS[stat]} decreased by {abs(amount)}."

        globals.type_text(text)

    def use(self, item:"items.Item"):
        base = globals.get_type(item)
        match base:
            case "Consumable":
                item.use()
                return True
            case _: 
                return False

    #ENCHANTMENTS
    def apply_on_attacks(self):
        raise NotImplementedError
    
    def apply_on_hits(self):
        raise NotImplementedError
    
    def apply_on_misses(self):
        raise NotImplementedError

    #CRITS
    def critical_hit(self):
        globals.type_text("A critical hit! Uh oh...")
        self.stats.damage_multiplier = 2
        taken = self.target.take_damage(self.roll_damage())
        self.apply_on_hits()
        self.stats.damage_multiplier = 1
        return None
    
    def critical_fail(self):
        globals.type_text("A critical fail!")
        self.fumble_table()

    def fumble_table(self):
        raise NotImplementedError

    #NARRATION
    def narrate(self, func, param=None) -> None:
        text:list[str] = func() if param is None else func(param)
        if self.prev_narration in text:
            text.remove(self.prev_narration)
        final = random.choice(text)
        self.prev_narration = final
        globals.type_text(final)
        return None

    def roll_narration(self) -> list[str]:
        text = [
            f"{self.header.default} moves to attack, ",
            f"{self.header.default} lunges at you, ",
            f"{self.header.default} prepares to strike... "
        ]
        return text

    def hit_narration(self) -> list[str]:
        text = [
            f"You fail to move before the attack hits you.",
            f"A hit.",
            f"{self.header.default} hits you.",
            f"It's attack lands.",
            f"You can't dodge this one.",
            f"You take a hit.",
            f"{self.header.default} manages to break your guard."
        ]
        return text
    
    def miss_narration(self) -> list[str]:
        text = [
            f"It's attack goes wide.",
            f"Luck is on your side this time.",
            f"{self.header.default} fails.",
            f"You stave off the attack.",
            f"The attack flies right by you.",
            f"You are unscathed.",
            f"{self.header.default} doesn't manage to hit you.",
            f"You leap out of harm's way."
        ]
        return text

    def take_damage_narration(self, damage:"mechanics.DamageInstance") -> list[str]:
        raise NotImplementedError

    def heal_narration(self, num:int) -> list[str]:
        """Handles specific narration for Object's healing"""
        raise NotImplementedError

    #INVENTORY
    def pick_up(self, item:"items.Item", silent=False):
        """Adds an item to the Object's inventory"""
        base = globals.get_subtype(item)
        match base:
            case "Stackable":
                #if you have a stack of those items already, just add to it
                held:"items.Stackable" | None = self.get_item(item.id)
                if held is not None:
                    held.set_quantity(held.quantity + item.quantity)
                    #item = held
                #if you don't, add the object to your inventory
                else:
                    self.inventory[item.id] = item
            case "Item" | "Equipment":
                self.inventory[item.id] = item
            case _:
                raise ValueError(f"Unrecognized object {item}.")

        item.owner = self
        if not silent: globals.type_text(item.pickup_message)
    
    def drop(self, item:"items.Item"):
        item = self.get_item(item)
        if item is not None:
            del self.inventory[item.id]
            item.owner = None

    def clean_inventory(self):
        """Check all stackable items and make sure anything with quantity 0 is removed"""
        for entry in self.inventory:
            item:"items.Item | items.Stackable" = self.inventory[entry]
            base = globals.get_subtype(item)
            match base:
                case "Stackable": 
                    if item.quantity <= 0:
                        del self.inventory[entry]
                        item.owner = None

    def get_item(self, ref: "items.Item" | str | int | None) -> "items.Item | None":
        """
        Checks if the Object has an item in it's inventory. 
        Returns the item if so, else None

        ref: can be str (item id), int (item index), or an instance of the Item class
        """
        base = globals.get_base_type(ref)
        match base:
            case "str":
                try: return self.inventory[ref]
                except KeyError: return None

            case "int":
                try: return list(self.inventory.values())[ref]
                except IndexError: return None

            case "Item":
                try: return self.inventory[ref.id]
                except KeyError: return None

            case _: raise ValueError(f"Unrecogized type '{type(ref)}'.")
