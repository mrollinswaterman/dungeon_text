#Game Object class
from __future__ import annotations
import enum, random, csv
from typing import Any
import global_commands
import items


class Damage_Type(enum.Enum):
    TRUE = 0
    PHYSICAL = 1
    MAGIC = 2

class Statblock():

    def __init__(self, parent):
        from equipment import Armor

        self.parent:Game_Object = parent
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
        self.armor:Armor | int | None = None
        self.damage: int | str | None = None
        self.dc:int = 0

    def value(self, stat:str) -> int | str:
        return self.__dict__[stat]
    
    def bonus(self, stat:str) -> int:
        return global_commands.bonus(self.__dict__[stat])
    
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


class Status_Effects_Handler():

    from status_effect import Status_Effect
    def __init__(self, parent):
        from status_effect import Status_Effect

        self.parent:Game_Object = parent
        self.dict:dict[str: Status_Effect] = {}
        self.cleanse_pool: set[Status_Effect] = set()

    @property
    def effects(self) -> list[Status_Effect]:
        return list(self.dict.values())

    def get(self, effect:Status_Effect | str | int) -> Status_Effect | None:
        """Returns a status effect from the status effect list's dictionary.
            Can access by str(id) or int(index)"""
        try:
            match effect:
                case str():
                    return self.dict[effect]
                case int():
                    return self.effects[effect]
                case _:
                    return self.dict[effect.id]
        except IndexError | KeyError:
            return None

    def add(self, effect:Status_Effect):
        if effect.id not in self.dict:
            self.dict[effect.id] = effect
        else:
            effect = self.get(effect)
            if effect is not None:
                effect.additional_effect()

    def update(self):
        for effect in self.effects:
            effect.update()
            if effect.active is False:
                self.cleanse_pool.add(effect)

        for effect in self.cleanse_pool:
            self.cleanse(effect)
        self.cleanse_pool = set()
    
    def cleanse(self, effect:Status_Effect | str | int) -> bool:
        effect = self.get(effect)
        if effect is not None:
            effect.cleanse()
            del self.dict[effect.id]
            return True
        else: return False

    def cleanse_all(self):
        for effect in self.effects:
            self.cleanse_pool.add(effect)

        for effect in self.cleanse_pool:
            self.cleanse(effect)
        self.cleanse_pool = set()

class Game_Object():

    def __init__(self, id="Game Object"):
        from items import Item
        from equipment import Weapon, Armor

        #Core properties
        self.id = id
        self.name = self.id
        self.level = 1
        self.stats:Statblock = Statblock(self)

        #Derived stats
        self.stats.max_hp = 10 + self.bonus("con")
        self.hp = self.stats.max_hp
        self.ap = self.stats.max_ap

        #Resources
        self.xp = 0
        self.gold = 0

        #Items / Equipment
        self.inventory:dict[str, Item] = {}
        self.weapon: Weapon | None = None
        self.armor: Armor | int | None = None

        #Combat tools
        self.status_effects:Status_Effects_Handler = Status_Effects_Handler(self)
        self.damage_type:Damage_Type = Damage_Type(1)

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
    def evasion(self) -> int:
        return self.stats.base_evasion + self.bonus("dex")
    
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
        self.status_effects.update() 

    def bonus(self, stat:str) -> int:
        return self.stats.bonus(stat)

    #ROLLS
    def roll_a_check(self, stat:str) -> int:
        """Returns a check with a given stat (d20 + stat bonus)"""
        roll = global_commands.d(20)
        match roll:
            case 1:
                return 1
            case 20:
                return 0
            case _:
                return roll + self.bonus(stat)

    def roll_to_hit(self) -> int:
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
        """Removes HP from the Object, starting with temp HP"""
        num = int(num)
        if self.stats.temp_hp > 0:
            self.stats.temp_hp -= num
            self.stats.temp_hp = 0 if self.stats.temp_hp < 0 else self.stats.temp_hp
        else:
            self.hp -= num

    def gain_temp_hp(self, num:int):
        """Adds temp HP to the Object"""
        self.stats.temp_hp += int(num)

    def heal(self, num:int):
        """Heals the Object for num amount"""
        self.hp += num
        if self.hp > self.stats.max_hp:
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
        self._ap = self.stats.max_ap

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

    def modify(self, stat, num:int):
        self.stats.modify(stat, num)

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
        import player_commands
        roll = self.roll_to_hit() if not player_commands.GOD_MODE else 999
        self.spend_ap()
        self.narrate(self.roll_narration, roll)
        self.apply_on_attacks()

        match roll:
            case 0: return self.critical_hit()

            case 1: return self.critical_fail()

            case _:
                if roll >= self.target.evasion:
                    self.narrate(self.hit_narration)
                    taken = self.roll_damage() if not player_commands.GOD_MODE else 999
                    self.target.take_damage(taken, self)
                    self.apply_on_hits()
                else:
                    self.narrate(self.miss_narration)
        return None

    def take_damage(self, taken:int, source:Game_Object | items.Item | str):
        taken *= self.stats.damage_taken_multiplier
        taken = int(taken)
        if self.armor is None: self.armor = 0
        match source:
            case Game_Object() | items.Item():
                if source.damage_type.name == "PHYSICAL":
                    final = taken
                    #Reduce damage taken by self.armor, adjusted depending on if self.armor is an item object or an int
                    match self.armor:
                        case items.Armor(): final -= self.armor.armor_value
                        case _: final -= self.armor
            case _:
                final = taken

        self.lose_hp(final)
        self.narrate(self.take_damage_narration, (final, source))

    def use(self, item:items.Item):
        raise NotImplementedError

    #ENCHANTMENTS
    def apply_on_attacks(self):
        raise NotImplementedError
    
    def apply_on_hits(self):
        raise NotImplementedError

    #CRITS
    def critical_hit(self):
        global_commands.type_text("A critical hit! Uh oh...")
        self.stats.damage_multiplier = 2
        taken = self.target.take_damage(self.roll_damage(), self)
        self.apply_on_hits()
        self.stats.damage_multiplier = 1
        return None
    
    def critical_fail(self):
        global_commands.type_text("A critical fail!")
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
        global_commands.type_text(final)
        return None

    def roll_narration(self) -> list[str]:
        text = [
            f"The {self.id} moves to attack, ",
            f"The {self.id} lunges at you, ",
            f"The {self.id} prepares to strike... "
        ]
        return text

    def hit_narration(self) -> list[str]:
        text = [
            f"You fail to move before the attack hits you.",
            f"A hit.",
            f"The {self.id} hits you.",
            f"It's attack lands.",
            f"You can't dodge this one.",
            f"You take a hit.",
            f"The {self.id} manages to break your guard."
        ]
        return text
    
    def miss_narration(self) -> list[str]:
        text = [
            f"It's attack goes wide.",
            f"Luck is on your side this time.",
            f"The {self.id} fails.",
            f"You stave off the attack.",
            f"The attack flies right by you.",
            f"You are unscathed.",
            f"The {self.id} doesn't manage to hit you.",
            f"You leap out of harm's way."
        ]
        return text

    def take_damage_narration(self, info:tuple[int, Game_Object | items.Item]) -> list[str]:
        raise NotImplementedError
    
    
    def heal_narration(self, num:int) -> list[str]:
        """Handles specific narration for Object's healing"""
        raise NotImplementedError

    #INVENTORY
    def pick_up(self, item:items.Item, silent=False):
        """Adds an item to the Object's inventory"""
        match item:
            case items.Consumable() | items.Resource():
                #if you have a stack of those items already
                held:items.Consumable | None = self.get_item(item.id)
                if held is not None:
                    held.increase_quantity(item.quantity)
                    item = held
                #if you don't
                else:
                    self.inventory[item.id] = item
            case items.Item():
                self.inventory[item.id] = item
            case _:
                raise ValueError(f"Unrecognized object {item}.")

        item.set_owner(self)
        if not silent: global_commands.type_text(item.pickup_message)
    
    def drop(self, item:items.Item):
        item = self.get_item(item)
        if item is not None:
            del self.inventory[item.id]
            item.set_owner(None)

    def get_item(self, ref: items.Item | str | int | None):
        """
        Checks if the Object has an item in it's inventory. 
        Returns the item if so, else None

        ref: can be str (item id), int (item index), or an instance of the Item class
        """
        match ref:
            case str():
                try: return self.inventory[ref]
                except KeyError: return None

            case int():
                try: return list(self.inventory.values())[ref]
                except IndexError: return None

            case items.Item():
                try: return self.inventory[ref.id]
                except KeyError: return None

            case _: raise ValueError(f"Unrecogized type '{type(ref)}'.")

