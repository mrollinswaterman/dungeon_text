import csv, random, enum
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

    def __init__(self, w_class):
        codex = {
            None: 2,
            "None": 2,
            "Light": 4,
            "Medium": 6,
            "Heavy": 8,
            "Superheavy": 10
        }

        if w_class in list(codex.keys()):
            self.value = codex[w_class]
            self.string = w_class
        elif w_class in list(codex.values()):
            self.value = w_class
            self.string = codex.keys(self.value-1)
        else:
            raise ValueError("Weight class not found in codex.")

class Item():

    def __init__(self, id:str, rarity=None):
        from game_object import Game_Object
        self.id = id
        self.name = ""
        self.rarity:Rarity = global_commands.generate_item_rarity() if rarity is None else Rarity(rarity)
        self.description = ""
        self.owner:Game_Object = None
        self.saved:dict[str, Any] = {}

    #properties
    #@property
    #def name(self) -> str:
        #return f"{self.rarity.string} {self.id}"
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

class Consumable(Item):

    def __init__(self, id:str, rarity="Common", quantity=1):
        super().__init__(id, rarity)
        self._quantity = int(quantity)
        self._plural = True if self._quantity > 1 else False
        self._strength = self._rarity.value * 2
        self._is_consumable = True
        self._type = "Consumable"
        self._target = None
        self._unit_weight = 1
        self._unit_value = 8 * self._rarity.value
    #properties
    @property
    def name(self) -> str:
        return f"{self._id}s" if self._plural else self._id
    @property
    def pickup_message(self) -> None:
        if self._plural:
            return f"You picked up {self._quantity} {self._id}s"
        return f"You picked up a {self._id}"
    @property
    def quantity(self) -> int:
        return self._quantity
    @property
    def stats(self) -> str:
        return self._quantity
    @property
    def weight(self) -> int:
        return self._unit_weight * self._quantity
    @property 
    def unit_weight(self) -> float:
        return self._unit_weight
    @property
    def value(self) -> int:
        return self._unit_value * self._quantity
    @property
    def unit_value(self) -> int:
        return self._unit_value
    @property
    def target(self):
        return self._target

    #methods
    def use(self, target):
        raise ValueError("Unimplemented")

    def increase_quantity(self, num:int) -> None:
        self._quantity += num
        self.update()

    def decrease_quantity(self, num:int) -> None:
        self._quantity -= num
        self.update()
    
    def set_quantity(self, num:int) -> None:
        self._quantity = num
        self.update()
    
    def set_target(self, tar) -> None:
        self._target = tar

    def enchant(self, effect) -> None:
        raise ValueError("Consumable items cannot be enchanted.")

    def update(self) -> None:
        self._plural = True if self._quantity > 1 else False
        self._value = self._unit_value * self._quantity
        self._weight = self._unit_weight * self._quantity

    def save(self) -> None:
        super().save()
        self._tod["quantity"] = self._quantity
        self._tod["unit_weight"] = self._unit_weight
        self._tod["unit_value"] = self._unit_value

    def load(self, save) -> None:
        super().load(save)
        self._quantity = int(save["quantity"])
        self._unit_weight = float(save["unit_weight"])
        self._unit_value = float(save["unit_value"])
        self.update()
        return None
    
    def format(self) -> list[str]:
        forms = {
            "id": f"{self.name} ({self._rarity.string})",
            "quantity": f"Quantity: {self._quantity}",
            "value": f"Value: {self.unit_value}g/each",
            "unit_weight": f"Unit Weight: {self.unit_weight}/each",
            "weight": f"Total Weight: {self.weight}"
        }
        return forms

class Resource(Consumable):

    def __init__(self, id, rarity="Common", quantity=1):
        super().__init__(id, rarity, quantity)
        self._pickup_message = f"You picked up x{self._quantity} {self.id}."
        self._durability = 1
        self._max_durability = 1
        self._type = "Resource"
        self._plural = False

    @property
    def pickup_message(self):
        return f"You picked up x{self._quantity} {self.id}."
    
    def set_weight(self, num:int) -> None:
        self._weight_class.value = num

