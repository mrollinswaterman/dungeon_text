#file for 'stackable' items, anything you can have more than one of
from item import Item, Rarity, Anvil
from equipment import Anvil

class Stackable(Item):

    def __init__(self, anvil:Anvil, id:str, rarity:str | Rarity | None=None):
        #check for custom rarity, and set it if it's there
        id = anvil.id if id is None else id
        rarity = anvil.rarity if rarity is None else rarity
        super().__init__(id, rarity)

        #consumable specific stats
        self.quantity: int = None
        self.unit_weight: int = None
        self.unit_value: int = None

        self.anvil = anvil
        self.craft()

    #properties
    @property
    def weight(self) -> int:
        return self.quantity * self.unit_weight

    @property
    def value(self) -> int:
        return self.quantity * self.unit_value

    @property
    def name(self) -> str:
        return f"{self.id}s" if self.quantity > 1 else self.i

    @property
    def pickup_message(self) -> str:
        return f"You picked up {self.quantity} {self.id}s" if self.quantity > 1 else f"You picked up a {self.id}"
    
    @property
    def format(self) -> str:
        return super().format + [
            f"Quantity: {self.quantity}"
        ]

    #methods
    def craft(self):
        """Copies an item's anvil stats to it's own class attributes"""
        for entry in self.anvil.__dict__:
            if entry in self.__dict__ and self.__dict__[entry] is None:
                self.__dict__[entry] = self.anvil.__dict__[entry]

        #self.quantity = int(self.quantity)
        #self.unit_value = int(self.unit_value)
        #self.unit_weight = int(self.unit_weight)

    #META functions (ie save/load/format etc)
    def save(self) -> None:
        super().save()
        for entry in self.anvil.__dict__:
            if entry in self.__dict__ and entry not in self.saved:
                self.saved[entry] = self.__dict__[entry]

    def format(self) -> list[str]:
        forms = {
            "id": f"{self.name} ({self.rarity.string})",
            "quantity": f"Quantity: {self.quantity}",
            "value": f"Value: {self.unit_value}g/each",
            "unit_weight": f"Unit Weight: {self.unit_weight}/each",
            "weight": f"Total Weight: {self.weight}"
        }
        return forms