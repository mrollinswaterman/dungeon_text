#equipment file, ie items you can equip

##Required Modules: globals, items, mechanics, game_objects
from __future__ import annotations
import random
import items
import globals
import mechanics

class Equipment(items.Item):

    def __init__(self, anvil:"items.Anvil", id:str=None, rarity: items.Rarity | str | int=None):
        id = anvil.id if id is None else id
        #check for custom rarity, and set it if it's there
        rarity = anvil.rarity if rarity is None else rarity
        super().__init__(id, rarity)
        self.weight_class:items.Weight_Class = items.Weight_Class()
        self.damage_type:mechanics.DamageType = mechanics.DamageType()
        self.max_dex_bonus:int = None
        self.durability:int = None

        self.__anvil__ = anvil
        self.smelt()
    
    #properties
    @property
    def weight(self) -> int:
        return self.weight_class.value

    @property
    def value(self) -> float:
        return 15 * self.rarity.value

    @property
    def max_durability(self) -> int:
        return 10 * self.rarity.value

    @property
    def broken(self) -> bool:
        return self.durability < 0 and self.durability > -(self.max_durability // 2)

    @property
    def destroyed(self) -> bool:
        return self.durability < -(self.max_durability // 2)

    @property
    def display(self) -> str:
        return [f"{self.id}, {self.weight_class.string} ({self.rarity.string}): {self.value}g, {self.weight} lbs.",]
    
    @property
    def format(self) -> list[str]:
        return super().format + [f"{' '*3}Class: {self.weight_class.string}, Dex Cap: +{self.max_dex_bonus}"]

    #methods
    def smelt(self):
        """
        Copies an item's anvil stats to its own internal __dict__
        """
        super().smelt()
        if self.durability is None:
            self.durability = self.max_durability
        self.damage_type = globals.build_damage_type(self.__anvil__.__dict__["damage_type"])
        self.weight_class = items.Weight_Class(self.__anvil__.__dict__["weight_class"])

    def apply(self, effect_type:str):
        """Applies an effect type"""
        for entry in self.enchantments:
            entry.apply(effect_type)

    #durability
    def lose_durability(self) -> None:
        """Checks to see if the item loses durability on this use"""
        if globals.probability((66 // self.rarity.value)):
            self.durability -= 1
            if self.broken is True:
                self.destroy()

    def remove_durability(self, num:int) -> None:
        """Removes a specified about of durability from the item"""
        self.durability -= num
        if self.broken is True:
            self.durability = 0
            self.destroy()

    def repair(self) -> None:
        """Repairs the item, returning its current durability to max value"""
        if not self.destroyed:
            self.durability = self.max_durability
            stopword = "Broken"
            query = self.id.split()
            resultwords = [word for word in query if word != stopword]
            self.id = ''.join(resultwords)

    def destroy(self) -> None:
        """Destroys the item irrepairably"""
        #in the future might have this just create a Resource object called Scrap and set self equal to it
        for entry in self.__dict__:
            self.__dict__[entry] = None
        self.id = "Scrap"

    #META functions (save/load/format, etc)
    def save(self):
        #reset ID before saving it
        self.id = self.__anvil__.id
        super().save()
        self.saved["durability"] = self.durability if self.durability is not None else self.max_durability
    
    def load(self, source:dict[str, str]) -> None:
        if "durability" in source:
            self.durability = int(source["durability"])

        if "rarity" in source:
                self.rarity = items.Rarity(source["rarity"])
        return None

class Weapon(Equipment):

    def __init__(self, anvil:items.Anvil, id=None, rarity=None):
        #set Weapon specific attributes to null before smelt
        self.damage:str | None = None
        self.crit:int | None = None
        self.crit_range:int | None = None

        #placeholder values for integer damage dice
        self.damage_die:int = None
        self.num_damage_dice:int = None

        super().__init__(anvil, id, rarity)

    #properties
    @property
    def weight(self) -> int:
        return int(self.weight_class.value + (self.damage_die - 6) + (self.num_damage_dice - 1)) 

    @property
    def attack_bonus(self) -> int:
        return self.rarity.value

    @property
    def display(self) -> list[str]:
        #return f"({super().display}, {self.damage}, {self.crit_range}–20/x{self.crit}): {self.value}g, {self.weight} lbs."
        return super().display + [f"{' '*5}Damage: {self.__anvil__.damage} {self.damage_type}, {self.crit_range}–20/x{self.crit}, Dex Cap: +{self.max_dex_bonus}"]

    @property
    def format(self) -> list[str]:
        return super().format + [
            f"{' '*3}Damage: {self.__anvil__.damage}{' '*3}Crit: {self.crit_range}–20/x{self.crit}",
            f"{' '*3}Durability: {self.durability}/{self.max_durability}",
        ]
    #methods
    def smelt(self) -> None:
        super().smelt()
        #Process self.damage to split it into num_dice and die (ie 1d8 -> 1 , 8)
        dmg = self.damage.split("d")
        self.damage_die = int(dmg[1])
        self.num_damage_dice = int(dmg[0])

        #set crit range to 20 if it's null
        self.crit_range = 20 if self.crit_range is None or self.crit_range == "" else self.crit_range

        #set damage type
        self.damage_type = globals.build_damage_type(self.__anvil__.__dict__["damage_type"])

    #weapon methods
    def roll_damage(self) -> int:
        return globals.XdY([self.num_damage_dice, self.damage_die])

    #META functions (save/load/format, etc)
    def save(self) -> None:
        super().save()

class Armor(Equipment):

    def __init__(self, anvil:"items.Anvil", id=None, rarity=None):
        self.armor_value: int = None
        super().__init__(anvil, id, rarity)

    #properties
    @property
    def weight(self) -> int:
        return int(self.weight_class.value * 4 + 2 * self.armor_value)

    @property
    def value(self) -> dict:
        return 15 * (self.rarity.value + self.weight_class.value) + random.randrange(self.armor_value, 5*self.armor_value)

    @property
    def max_durability(self) -> int:
        return 15 * self.rarity.value
    
    @property
    def display(self) -> list[str]:
        return super().display + [f"{' '*5}Armor: {self.armor_value}, Dex Cap: +{self.max_dex_bonus}"]

    @property
    def format(self) -> list[str]:
        return super().format + [
            f"{' '*3}Armor: {self.armor_value}",
            f"{' '*3}Durability: {self.durability}/{self.max_durability}",
        ]

    #methods
