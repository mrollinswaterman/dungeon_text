#Weapon+Armor enchantments file

from __future__ import annotations
import csv
import globals
import mechanics
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import game_objects

class Enchantment(mechanics.Mechanic):

    def __init__(self, source):
        super().__init__(source)
        self.id = "Enchatment"
        self.cost = 1
        self.actives:dict[str, list[tuple[mechanics.Condition | mechanics.Effect, float]]] = {
            "on_hit":[],
            "on_attack":[],
            "on_miss":[]
        }

    @property
    def target(self) -> "game_objects.Game_Object | None":
        base = globals.get_object_type(self.source)
        match base:
            case "game_object": return self.source.target
            case "item": return self.source.owner.target
            case _: raise ValueError("Invalid source for Enchantment class")

    def start(self, effect_type:str):
        for entry in self.actives[effect_type]:
            current = entry[0]
            proc_chance = entry[1]
            proc_chance = 1.0 if proc_chance is None else proc_chance
            if globals.probability(proc_chance*100):
                base = globals.get_object_type(current)
                match base:
                    case "condition": self.target.conditions.add(current)
                    case "effect": current.start()
            else:
                pass

    def add_active(self, active_type:str, obj: mechanics.Condition | mechanics.Effect, proc:float=None) -> bool:

        active = tuple()
        active[0] = obj
        active[1] = proc

        self.actives[active_type].append(active)
        return True

    def acquire(self, source:dict[str, str] | str) -> bool:
        """
        Acquires the attributes of the specified enchantment and copies them to this instance

        If source is a dictionary, it copies the properties directly

        If source is a str it attempts to retrieve the approrpiate source 
        dictionary from the Enchantments CSV file
        """

        match source:
            case str(): source = self.load_from_csv(source)

        return self.copy(source)
    
    def copy(self, source:dict[str, str] | None) -> bool:
        """
        Reads a source dictionary and copies the respective attributes to this instance's
        __dict__ property or active, whichever is appropriate
        """
        if source is None: raise ValueError("Unrecoginzed source for enchantment copy!")
        for attr in source:
            if attr in self.__dict__:
                self.__dict__[attr] = source[attr]

            if attr in self.actives and source[attr] != '':
                self.actives[attr] = globals.create_condition(source[attr])(self.source)

        self.id = self.id + " Enchantment"
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
