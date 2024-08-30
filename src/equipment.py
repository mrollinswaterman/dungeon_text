#equipment file, ie items you can equip
from __future__ import annotations
import random
import global_commands
from items import Item, Weight_Class, Rarity
from game_object import Damage_Type

class Anvil():

    def __init__(self):
        self.id = "None"
        self.anvil_type = "Anvil"

        #Universal attributes
        self.weight_class:Weight_Class = Weight_Class(None)
        self.rarity:Rarity = Rarity(1)
        self.max_dex_bonus:int = 6
        #self.damage_type:Damage_Type = Damage_Type(1)

        #Weapon attributes
        self.damage:str | None = None
        self.crit:int | None = None
        self.crit_range:int | None = None

        #Armor attributes
        self.armor_value:int | None = None

    def copy(self, source:dict):
        for entry in source:
            if entry in self.__dict__:
                self.__dict__[entry] = source[entry]
        
        self.anvil_type = f"{source['type']} Anvil"
        self.weight_class = Weight_Class(self.weight_class)
        self.rarity = Rarity(self.rarity)

class Equipment(Item):

    def __init__(self, id, rarity, anvil:Anvil):
        super().__init__(id, rarity)
        self.weight_class:Weight_Class = None
        #self.rarity:Rarity = None
        self.max_dex_bonus:int = 0
        self.damage_type:Damage_Type = Damage_Type(1)

        self.anvil = anvil
        self.smelt()
    
    #properties
    @property
    def value(self) -> float:
        return 15 * self.rarity.value

    @property
    def weight(self) -> int:
        return self.weight_class.value

    @property
    def max_durability(self) -> int:
        return 10 * self.rarity.value

    @property
    def broken(self) -> bool:
        return self.durability < 0 and self.durability > -(self.max_durability // 2)

    @property
    def destroyed(self) -> bool:
        return self.durability < -(self.max_durability // 2)

    #methods
    def smelt(self):
        """Copies an item's anvil stats to it's own class attributes"""
        self.anvil.parent = self
        for entry in self.anvil.__dict__:
            if entry in self.__dict__:
                self.__dict__[entry] = self.anvil.__dict__[entry]

        #reset durability after anvil adjustments
        self.durability = self.max_durability

    #durability
    def lose_durability(self) -> None:
        """Checks to see if the item loses durability on this use"""
        if global_commands.probability((66 // self.rarity.value)):
            self._durability -= 1
            if self.broken is True:
                self.destroy()

    def remove_durability(self, num:int) -> None:
        """Removes a specified about of durability from the item"""
        self._durability -= num
        if self.broken is True:
            self._durability = 0
            self.destroy()

    def repair(self) -> None:
        """Repairs the item, returning its current durability to max value"""
        if not self.destroyed:
            self.durability = self.max_durability
            stopword = "Broken"
            query = self.id.split()
            resultwords = [word for word in query if word != stopword]
            print(resultwords)
            self.id = ''.join(resultwords)

    def destroy(self) -> None:
        """Destroys the item irrepairably"""
        #in the future might have this just clreate a Resource object called Scrap and set self equal to it
        for entry in self.__dict__:
            self.__dict__[entry] = None
        self.id = "Scrap"

    #META functions (save/load/format, etc)
    def save(self):
        super().save()
        for entry in self.anvil.__dict__:
            if entry in self.__dict__:
                self.saved[entry] = self.__dict__[entry]
        self.saved["durability"] = self.durability
        self.saved["weight_class"] = self.weight_class.string

    def load(self, save_file):
        super().load(save_file)
        self.weight_class = Weight_Class(self.weight_class)

class Weapon(Equipment):

    def __init__(self, id, rarity, anvil):
        #set Weapon specific attributes to null before smelt
        self.damage:str | None = None
        self.crit:int | None = None
        self.crit_range:int | None = None

        #placeholder values for integer damage dice
        self.damage_die:int = 0
        self.num_damage_dice:int = 0
        super().__init__(id, rarity, anvil)

    #properties
    @property
    def stats(self) -> str:
        return f"{self.num_damage_dice}d{self.damage_die}, x{self.crit}"
    @property
    def attack_bonus(self) -> int:
        return self.rarity.value
    @property
    def weight(self) -> int:
        return int(self.weight_class.value + (self.damage_die - 6) + (self.num_damage_dice - 1)) 

    #methods
    def smelt(self) -> None:
        super().smelt
        #Process self.damage to split it into num_dice and die (ie 1d8 -> 1 , 8)
        dmg = self.damage.split("d")
        self.damage_die = int(dmg[1])
        self.num_damage_dice = int(dmg[0])

        #set crit range to 20 if it's null
        self.crit_range = 20 if self.crit_range == None or self.crit_range == "" else self.crit_range

    #weapon methods
    def roll_damage(self) -> int:
        return global_commands.XdY([self.num_damage_dice, self.damage_die])

    #META functions (save/load/format, etc)
    def save(self) -> None:
        super().save()

    def load(self, stats_file) -> None:
        super().load(stats_file)
    
    def format(self) -> dict[str, str]:
        forms = {
            "id": f"{self.id} ({self.rarity.string})",
            "damage":f"Damage: {self.num_damage_dice}d{self.damage_die}",
            "crit": f"Critical: {self.crit_range}–20/x{self.crit}", 
            "max_dex_bonus": f"Max Dex Bonus: +{self.max_dex_bonus}",
            "durability": f"Durability: {self._durability}/{self.max_durability}",
            "value": f"Value: {self.value}g",
            "weight": f"Weight: {self.weight}",
        }
        return forms

class Armor(Equipment):

    def __init__(self, id:str, rarity, anvil):
        self.armor_value: int = 0
        super().__init__(id, rarity, anvil)
        self.durability = self.max_durability

    #properties
    @property
    def max_durability(self) -> int:
        return 15 * self.rarity.value
    @property
    def value(self) -> dict:
        return (15 * self.rarity.value) + (15 * self.weight_class.value) + random.randrange(self.armor_value, 5*self.armor_value)
    @property
    def stats(self) -> str:
        return f"{self.weight_class.string}, {self.armor_value}P"
    @property
    def weight(self) -> int:
        return int(self.weight_class.value * 4 + 2 * self.armor_value)

    #methods
    #META functions (save/load/format, etc)
    def format(self):
        forms = {
            "id": f"{self.id} ({self.rarity.string})",
            "weight_class": f"Class: {self.weight_class.string}",
            "armor": f"Armor: {self.armor_value}P",
            "max_dex_bonus": f"Max Dex Bonus: +{self.max_dex_bonus}",
            "durability": f"Durability: {self._durability}/{self.max_durability}",
            "value": f"Value: {self.value}g",
            "weight": f"Weight: {self.weight}"
        }
        return forms