#Weapon+Armor enchantments file

from __future__ import annotations
import csv
from time import sleep
import globals
import mechanics
import effects
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class Enchantment(mechanics.Mechanic):

    def __init__(self, source):
        super().__init__(source)
        self.id = self.__class__.__name__
        self._effects:dict[str, list[tuple[mechanics.Mechanic, float]]] = {
            "on_hit":[],
            "on_attack":[],
            "on_miss":[]
        }

    @property
    def effects(self) -> list[mechanics.Mechanic]:
        return self._effects
    
    @property
    def on_hits(self) -> list[mechanics.Mechanic]:
        ret = []
        for tup in self._effects["on_hit"]:
            ret.append(tup[0])
        return ret
    
    @property
    def on_attacks(self) -> list[mechanics.Mechanic]:
        ret = []
        for tup in self._effects["on_attack"]:
            ret.append(tup[0])

        return ret
    
    @property
    def on_misses(self) -> list[mechanics.Mechanic]:
        ret = []
        for tup in self._effects["on_miss"]:
            ret.append(tup[0])

        return ret

    def apply(self, effect_type:str):
        for entry in self._effects[effect_type]:
            effect:mechanics.Mechanic = entry[0]
            proc_chance = entry[1]
            proc_chance = 1.0 if proc_chance is None else proc_chance
            if globals.probability(proc_chance*100):
                self.target.apply(effect)
            else:
                pass

    def add_effect(self, effect_type:str, obj: mechanics.Mechanic, proc:float=1.0) -> bool:

        eff = (obj, proc)

        self._effects[effect_type].append(eff)
        return True

    def acquire(self, source:dict[str, str] | str) -> bool:
        """
        Acquires the attributes of the specified enchantment and copies them to this instance

        If source is a dictionary, it copies the properties directly

        If source is a str it attempts to retrieve the approrpiate source 
        dictionary from the Enchantments CSV file
        """

        match source:
            case str(): 
                temp = self.load_from_csv(source)
                if temp is None:
                    temp = globals.create_enchantment(source, self.source)
                    if temp is not None:
                        temp = temp.__dict__
                source = temp

        return self.copy_from(source)
    
    def copy_from(self, source:dict[str, str] | None) -> bool:
        """
        Reads a source dictionary and copies the respective attributes to this instance's
        __dict__ property or active, whichever is appropriate
        """
        if source is None: raise ValueError("Unrecoginzed source for enchantment copy!")
        for attr in source:
            if attr in self.__dict__:
                self.__dict__[attr] = source[attr]

            if attr in self._effects and source[attr] != '':
                my_effect = globals.create_status(source[attr], self.source)
                self.add_active(attr, my_effect)

        self.id = self.id
        return True

    def load_from_csv(self, id:str) -> dict[str, str] | None:
        selected:dict[str, str] = None
        with open("enchantments.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] == id:
                    selected = row
                    break
        file.close()

        return selected 

        #add logic to make sure we're enchanting objects with the 
        #correct type (ie no weapon enchantments on armor)
