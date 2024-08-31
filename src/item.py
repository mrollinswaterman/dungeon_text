from __future__ import annotations
from typing import get_type_hints
from typing import Any
import global_commands

class Rarity():

    def __init__(self, rarity):
        
        codex = {
            "Common": 1,
            "Uncommon": 2,
            "Rare": 3,
            "Epic": 4,
            "Legendary": 5,
            "Unique": 6 
        }

        if rarity in list(codex.keys()):
            self.value = codex[rarity]
            self.string = rarity
        elif rarity in list(codex.values()):
            self.value = rarity
            self.string = list(codex.keys())[self.value-1]
        else:
            raise ValueError(f"Rarity '{rarity}' not found in codex.")

class Weight_Class():

    def __init__(self, class_ref):
        codex = {
            None: 2,
            "None": 2,
            "Light": 4,
            "Medium": 6,
            "Heavy": 8,
            "Superheavy": 10
        }

        if class_ref in list(codex.keys()):
            self.value = codex[class_ref]
            self.string = class_ref
        elif class_ref in list(codex.values()):
            self.value = class_ref
            self.string = codex.keys(self.value-1)
        else:
            raise ValueError("Weight class not found in codex.")

class Anvil():
    id:str
    anvil_type:str

    #EQUIPMENT attributes
    weight_class:Weight_Class
    rarity:Rarity
    max_dex_bonus:int
    durability:int

    #Weapon attributes
    damage:str
    crit:int
    crit_range:int

    #Armor attributes
    armor_value:int
    

    def __init__(self):
        self.id = None
        self.anvil_type = None

        #EQUIPMENT attributes
        self.weight_class:Weight_Class = None
        self.rarity:Rarity = None
        self.max_dex_bonus:int = 6
        self.durability:int = None

        #Weapon attributes
        self.damage:str = None
        self.crit:int = None
        self.crit_range:int = None

        #Armor attributes
        self.armor_value:int = None

    def copy(self, source:dict):
        """
        Copies a given source dictionary onto the anvil's own attributes,
        adjusting for typed values (ie an attribute that is typed as an 'int' should be copied as an int
        even if the source value is a string)
        """
        for entry in source:
            if entry in self.__dict__:
                if source[entry] is not None and source[entry] != "":
                    entry_type = get_type_hints(Anvil)[entry]
                    self.__dict__[entry] = entry_type(source[entry])
                else: self.__dict__[entry] = source[entry]

        self.anvil_type = source["type"] 

class Item():

    def __init__(self, id:str, rarity=None):
        from game_object import Game_Object
        self.id = id
        self._name = ""
        self.rarity:Rarity = None
        match rarity:
            case str() | int(): self.rarity = Rarity(rarity)
            case Rarity(): self.rarity = rarity
            case _: self.rarity = global_commands.generate_item_rarity()
        self.description = ""
        self.owner:Game_Object = None
        self.saved:dict[str, Any] = {}

    #properties
    @property
    def level(self) -> int:
        return self.owner.level

    @property
    def weight(self) -> float:
        return 5

    @property
    def value(self) -> int:
        return 10 * self.rarity.value

    @property
    def pickup_message(self) -> str:
        return f"You picked up a {self.id}."

    @property
    def name(self) -> str:
        return self._name

    #methods
    def initialize(self) -> None:
        return None

    #META functions (save/load/format, etc)
    def save(self) -> None:
        self.saved = {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "rarity": self.rarity.string
        }

    def load(self, save_file:dict) -> None:
        for entry in save_file:
            if entry in self.__dict__:
                self.__dict__[entry] = save_file[entry]
        
        self.rarity = Rarity(self.rarity)

    def format(self) -> list[str]:
        forms = {
            "id": f"{self.id} ({self.rarity.string})",
            "value": f"Value: {self.value}g",
            "weight": f"Weight: {self.weight} lbs"
        }
        return forms

    def __str__(self) -> str:
        me = ""
        forms = self.format()
        for entry in forms:
            me = me + forms[entry] +"\n"
        return me
