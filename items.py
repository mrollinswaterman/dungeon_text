import random

RARITY = {
    1: "Common",
    2: "Uncommon",
    3: "Rare",
    4: "Epic",
    5: "Legendary",
    6: "Unique"
}

WEIGHT_CLASS = {
    "None": 0,
    "Light": 2,
    "Medium": 4,
    "Heavy": 6,
    "Superheavy": 8
}

class Item():

    def __init__(self, id, rarity):

        self._id = id
        self._rarity = rarity
        self._value = 5 * rarity
        self._max_durability = 10 * self._rarity
        self._durability = self._max_durability
        self._is_consumable = False
        self._weight = 0
        self._pickup_message = ""
        self._description = ""
        self._broken = False
        self._type = "Item"

    #properties
    @property
    def id(self) -> str:
        return f"{RARITY[self._rarity]} {self._id}"
    @property
    def name(self) -> str:
        return self._id
    @property
    def value(self) -> int:
        return self._value
    @property
    def broken(self) -> bool:
        return self._durability <= 0
    @property
    def durability(self) -> tuple[int, int]:
        return (self._durability, self._max_durability)
    @property
    def rarity(self) -> str:
        return RARITY[self._rarity]
    @property
    def numerical_rarity(self) -> int:
        return self._rarity
    @property
    def stats(self):
        raise NotImplementedError
    @property
    def is_consumable(self) -> bool:
        return self._is_consumable
    @property
    def weight(self) -> int:
        return self._weight
    @property
    def pickup_message(self) -> str:
        return self._pickup_message
    @property
    def description(self) -> str:
        return self._description
    @property
    def broken(self) -> bool:
       return self._durability <= 0
    @property
    def type(self) -> str:
        return self._type
    #methods
    def lose_durability(self) -> None:
        prob = random.randrange(100)
        #weapon only loses durability occasionally, probability decreases with rarity
        if prob < (60 // self._rarity):
            self._durability -= 1
            if self.broken is True:
                self.item_has_broken()

    def remove_durability(self, num:int) -> None:
        self._durability -= num
        if self.broken is True:
            self._durability = 0
            self.item_has_broken()

    def repair(self) -> None:
        """
        Repairs weapon, returning its current durability to max value
        """
        self._durability = self._max_durability

    def set_weight(self, num:int) -> None:
        self._weight = num

    def set_stats(self, stats: tuple[int, int, int]):
        raise NotImplementedError

    def set_pickup_message(self, msg:str) -> None:
        self._pickup_message = msg

    def item_has_broken(self) -> None:
        print(f"Your {self._id} has broken!")
    
    def set_description(self, words:str) -> None:
        self._description = words


    def __str__(self) -> str:
        return f'{self.id}\n Rarity: {RARITY[self._rarity]}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n'

class Weapon(Item):

    def __init__(self, id, rarity=0):
        super().__init__(id, rarity)
        if self._rarity == 0:
            self._rarity = random.randrange(1, 4)
        self._value = 15 * self._rarity
        self._max_durability = 10 * self._rarity
        self._durability = self._max_durability
        self._damage_dice = 0
        self._num_damage_dice = 0
        self._crit = 0
        self._type = "Weapon"

    #properties
    @property
    def damage_dice(self) -> int:
        """
        Returns damage dice
        """
        return self._damage_dice
    @property
    def num_damage_dice(self) -> int:
        return self._num_damage_dice
    @property
    def stats(self) -> int:
        return f"{self._num_damage_dice}d{self._damage_dice}, x{self._crit}"
    @property
    def crit(self) -> int:
        return self._crit
    @property
    def type(self) -> str:
        return self._type
    
    def set_stats(self, statblock: str):
        """
        Sets a weapons stats based on a tuplized statblock

        Returns nothing
        """
        #finds the index of each piece of info
        num_idx = statblock.index('d')
        num = eval(statblock[0:num_idx])
        dice_idx = statblock.index(",")
        dice = eval(statblock[num_idx+1: dice_idx])
        crit = eval(statblock[dice_idx+2: len(statblock)])

        #sets the appropriate stats
        self.set_damage_dice((num, dice))
        self.set_crit_multiplier(crit)
        self._weight = int(2.5 * self._num_damage_dice + (self._damage_dice // 2))

    def set_damage_dice(self, dice:tuple[int,int]) -> None:
        num, type = dice
        self._damage_dice = type
        self._num_damage_dice = num

    def set_crit_multiplier(self, crit)->None:
        self._crit = crit
    
    def __str__(self) -> str:
        return (f"""{self.id}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n Damage Dice: {self._num_damage_dice}d{self._damage_dice}\n Weight: {self.weight} lbs\n""")

class Armor(Item):

    def __init__(self, id, weight_class:int="Light", rarity=0):
        super().__init__(id, rarity)
        if self._rarity == 0:
            self._rarity = random.randrange(1, 4)
        self._weight_class = weight_class
        self._numerical_weight_class = WEIGHT_CLASS[self._weight_class]
        self._armor_value = int(self._numerical_weight_class + self._rarity - (self._numerical_weight_class / 2))
        self._value = (25 * rarity) + (10 * self.numerical_weight_class)
        self._broken = False
        self._type = "Armor"

    #properties
    @property
    def armor_value(self) -> int:
        """
        Return the value of the armor
        """
        return self._armor_value
    @property
    def stats(self) -> str:
        return f"{self.weight_class}, {self.armor_value}P"
    @property
    def weight_class(self) -> str:
        return self._weight_class
    @property
    def numerical_weight_class(self) -> int:
        return self._numerical_weight_class

    #methods
    def set_armor_value(self, armor) -> None:
        self._armor_value = armor

    def set_stats(self, stats) -> None:
        """
        Sets armor weight class and armor value (if given),
        then re-calculates value and armor value as necessary
        """
        if stats is None or len(stats) == 0:
            return None

        weight, armor = stats
        self._weight_class = weight
        self._numerical_weight_class = WEIGHT_CLASS[self._weight_class]
        if armor is not None:
            self.set_armor_value(armor)
        else:
            self.set_armor_value(int(self._numerical_weight_class + self._rarity - (self._numerical_weight_class / 2)))
        self._value = (25 * self._rarity) + (10 * self.numerical_weight_class)
        self._weight = (10 * self._numerical_weight_class) + self._armor_value
    
    def __str__(self) -> str:
        return f'{self.id}\n Weight: {self.weight_class}\n Rarity: {self._rarity}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n Armor Value: {self._armor_value}\n'
    
class Consumable(Item):

    def __init__(self, id:str, rarity:int,quantity:int=0):
        super().__init__(id, rarity)
        self._quantity = quantity
        self._strength = rarity * 2
        self._is_consumable = True
        self._type = "Consumable"
        self._unit_weight = 1

    #properties
    @property
    def quantity(self) -> int:
        return self._quantity
    @property
    def stats(self) -> str:
        return self._quantity

    #methods
    def use(self, target):
        raise ValueError("Unimplemented")

    def increase_quantity(self, num:int) -> None:
        self._quantity += num
        self._weight = self._unit_weight * self._quantity

    def decrease_quantity(self, num:int) -> None:
        self._quantity -= num
        self._weight = self._unit_weight * self._quantity

    def set_pickup_message(self, msg: str="") -> None:
        if self._quantity > 1:
            self._pickup_message = f"You picked up {self._quantity} {self.id}s\n"
        else:
            self._pickup_message = f"You picked up a {self._id}\n"

    def __str__(self) -> str:
        return f'{self.id}\n Rarity: {self._rarity}\n Value: {self._value}g\n Quantity: {self._quantity}'
    


