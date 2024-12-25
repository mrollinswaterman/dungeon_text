#equipment file, ie items you can equip

##Required Modules: globals, items, mechanics, game_objects
from __future__ import annotations
import random
import items
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import globals
    import items
    import mechanics
    import game_objects

class Equipment(items.Item):

    def __init__(self, anvil:"items.Anvil", id:str=None, rarity: "items.Rarity" | str | int=None):
        import game_objects
        #check for custom rarity, and set it if it's there
        id = anvil.id if id is None else id
        rarity = anvil.rarity if rarity is None else rarity
        super().__init__(id, rarity)
        self.weight_class:"items.Weight_Class" | str | int = None
        self.max_dex_bonus:int = None
        self.damage_type:"game_objects.Damage_Type" = game_objects.Damage_Type(1)
        self.durability:int = None

        self.enchantments:dict[str, "mechanics.Weapon_Enchantment"] = {}

        self.anvil = anvil
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
    def enchantment_space_remaining(self) -> int:
        total = 0
        for entry in self.enchantments:
            obj:"mechanics.Weapon_Enchantment" = self.enchantments[entry]
            total += obj.cost
        return self.rarity.value - total

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
        """Copies an item's anvil stats to it's own class attributes"""
        for entry in self.anvil.__dict__:
            if entry in self.__dict__ and self.__dict__[entry] is None:
                self.__dict__[entry] = self.anvil.__dict__[entry]

        if self.durability is None:
            self.durability = self.max_durability

        #set enchants to empty dictionary to avoid any confusion
        self.enchantments = {}

        #if my anvil has enchantments, procces the enchantments and proc chances strings
        if self.anvil.enchanted:
            process_enchants:str = self.anvil.__dict__["enchantments"]
            process_procs:str = self.anvil.__dict__["proc_chances"]
            process_enchants = process_enchants.split("/")
            process_procs = process_procs.split("/")
            #enchant self with every enchantment from saved enchantments, then set that enchantment's proc chance
            #to the corresponding value
            for idx, entry in enumerate(process_enchants):
                self.enchant(entry, True)
                obj = self.get_enchantment(entry)
                obj.proc_chance = float(process_procs[idx])

    def apply(self, effect_type:str):
        for entry in self.enchantments:
            self.enchantments[entry].apply(effect_type)

    def get_enchantment(self, ref) -> "mechanics.Enchantment":
        match ref:
            case str(): return self.enchantments[ref]
            case mechanics.Enchantment(): return self.enchantments[ref.id]
            case int(): return list(self.enchantments.values())[ref]
            case _: raise ValueError(f"This item is does not have and enchantment matching '{ref}'")

    def enchant(self, enchantment, silent=False) -> bool:
        match enchantment:
            case mechanics.Enchantment():
                enchantment:"mechanics.Enchantment" = enchantment
            case _:
                enchantment = mechanics.TOME[enchantment]

        if enchantment.cost <= self.enchantment_space_remaining and enchantment.id not in self.enchantments:
            self.enchantments[enchantment.id] = enchantment
            if enchantment.proc_chance == 1.0: 
                enchantment.proc_chance = (random.randrange(25, 75) / 100) + (self.rarity.value/15)
            enchantment.initialize(self)
            if not silent: print(f"{self.id} is now enchanted with {enchantment.id}\n")
            self.id = f"{enchantment.id} {self.id}"

        else: print(f"This item has no room for a {enchantment.id} enchantment.\n")
    
    def disenchant(self, enchantment) -> bool:
        enchantment:"mechanics.Weapon_Enchantment" = self.get_enchantment(enchantment)
        del self.enchantments[enchantment.id]
        self.id = self.anvil.id
        for entry in self.enchantments:
            self.id = f"{self.enchantments[entry].id} {self.id}"

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
            #(resultwords)
            self.id = ''.join(resultwords)

    def destroy(self) -> None:
        """Destroys the item irrepairably"""
        #in the future might have this just clreate a Resource object called Scrap and set self equal to it
        for entry in self.__dict__:
            self.__dict__[entry] = None
        self.id = "Scrap"

    #META functions (save/load/format, etc)
    def save(self):
        #reset ID before saving it
        self.id = self.anvil.id
        super().save()
        for entry in self.anvil.__dict__:
            if entry in self.__dict__ and entry not in self.saved:
                self.saved[entry] = self.__dict__[entry]
        self.saved["durability"] = self.durability if self.durability is not None else self.max_durability
        self.saved["weight_class"] = self.weight_class.string

        #save enchantments and their respective proc chances into a string seperated by "/"s
        #i.e "Flaming/Serrated"
        saved_enchantments = ""
        saved_proc_chances = ""
        for entry in self.enchantments:
            saved_enchantments = f"{saved_enchantments}/{entry}"
            saved_proc_chances = f"{saved_proc_chances}/{self.enchantments[entry].proc_chance}"

        #cut the first char of the strings to eliminate the leading "\"
        self.saved["enchantments"] = saved_enchantments[1:len(saved_enchantments)]
        self.saved["proc_chances"] = saved_proc_chances[1:len(saved_proc_chances)]

class Weapon(Equipment):

    def __init__(self, anvil:"items.Anvil", id=None, rarity=None):
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
        return super().display + [f"{' '*5}Damage: {self.anvil.damage}, {self.crit_range}–20/x{self.crit}, Dex Cap: +{self.max_dex_bonus}"]

    @property
    def format(self) -> list[str]:
        return super().format + [
            f"{' '*3}Damage: {self.anvil.damage}{' '*3}Crit: {self.crit_range}–20/x{self.crit}",
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

    #weapon methods
    def roll_damage(self) -> int:
        return globals.XdY([self.num_damage_dice, self.damage_die])

    #META functions (save/load/format, etc)
    def save(self) -> None:
        super().save()

    def load(self, stats_file) -> None:
        super().load(stats_file)

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
        #return f"({super().display}, {self.armor_value}/{list(self.damage_type.name)[0]}): {self.value}g, {self.weight} lbs."
        #return super().display + [f"Armor: {self.armor_value}/{self.damage_type.name}"]
        return super().display + [f"{' '*5}Armor: {self.armor_value} {list(self.damage_type.name)[0]}, Dex Cap: +{self.max_dex_bonus}"]
    @property
    def format(self) -> list[str]:
        return super().format + [
            f"{' '*3}Armor: {self.armor_value}/{self.damage_type.name}",
            f"{' '*3}Durability: {self.durability}/{self.max_durability}",
        ]

    #methods
