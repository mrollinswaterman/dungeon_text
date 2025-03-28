#File for 'stackable' items, anything you can have more than one of

import items
class Stackable(items.Item):

    def __init__(self, anvil:items.Anvil, id:str="stackable"):
        #check for custom rarity, and set it if it's there
        id = anvil.id if id is None else id
        super().__init__(id)

        self.quantity: int = None
        self.unit_weight: int = None
        self.unit_value: int = None

        self.__anvil__ = anvil
        self.smelt()

    #properties
    @property
    def weight(self) -> int:
        return self.quantity * self.unit_weight

    @property
    def value(self) -> int:
        print(self.quantity, self.unit_value)
        return self.quantity * self.unit_value

    @property
    def pickup_message(self) -> str:
        return f"You picked up x{self.quantity} {self.name}." if self.quantity > 1 else f"You picked up a {self.id}."
    
    @property
    def display(self) -> list[str]:
        return [f"{self.name} ({self.rarity.string}): {self.unit_value}g/each, {self.unit_weight} lbs./each",
                f"{' '*5}x{self.quantity} Available"
                ]

    @property
    def format(self) -> list[str]:
        return [
            f"{self.name} ({self.rarity.string})",
            f"{' '*3}Quantity: {self.quantity}",
            f"{' '*3}Cost: {self.unit_value}g/each",
            f"{' '*3}Weight: {self.unit_weight} lbs./each",
            f"{' '*3}Total: {self.value}g, {self.weight} lbs.",
        ]

    #methods
    def smelt(self):
        """Copies an item's anvil stats to it's own class attributes"""
        if self.__anvil__ is None: return None
        for entry in self.__anvil__.__dict__:
            if entry in self.__dict__ and self.__dict__[entry] is None:
                self.__dict__[entry] = self.__anvil__.__dict__[entry]

    def set_quantity(self, amount:int) -> None:
        self.quantity = amount
        self.__anvil__.quantity = amount

    def remove_quantity(self, amount:int=1) -> None:
        if self.quantity >= amount:
            self.set_quantity(self.quantity - amount)
        else: raise ValueError("Can't remove more than the item has.")

    #META functions (ie save/load/format etc)
    def save(self) -> None:
        super().save()
        for entry in self.__anvil__.__dict__:
            if entry in self.__dict__ and entry not in self.saved:
                self.saved[entry] = self.__dict__[entry]
    
class Consumable(Stackable):

    def __init__(self, anvil:items.Anvil, id:str=None):
        super().__init__(anvil, id)

    def use(self) -> bool:
        return self.owner.spend_ap()