import csv
import globals
from ast import literal_eval as make_tuple
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import items
    import game_objects

class Statblock():

    def __init__(self, parent:"game_objects.Game_Object"):

        self.parent = parent
        self.id:str = f"{self.parent.id} Statblock"

        #Core Stats
        self.level:int = self.parent.level
        self.level_range:tuple[int, int] = (1, 20)
        self.hit_die:int = 8

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
        self.armor:"items.Armor" | int | None = 0
        self.damage: int | str | None = None
        self.base_save_dc:int = 0

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
            if source[entry] is None or source[entry] == '': continue
            if entry in self.__dict__ and entry != "id":
                match self.__dict__[entry]:
                    case str(): self.__dict__[entry] = source[entry]
                    case int(): self.__dict__[entry] = int(source[entry])
                    case tuple(): self.__dict__[entry] = make_tuple(source[entry])
                    case _: self.__dict__[entry] = source[entry]

        #print(self.__dict__)

    def __str__(self):
        ret = ""
        for entry in self.__dict__:
            ret = ret + f"{entry}: {self.__dict__[entry]}\n"
        return ret