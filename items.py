import random

class Item():

    def __init__(self, id, rarity):

        self._id = id
        self._rarity = rarity
        self._value = 5 * rarity
        self._max_durability = 10 * self._rarity
        self._durability = self._max_durability

    #properties
    @property
    def id(self) -> str:
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
    def rarity(self) -> int:
        return self._rarity
    
    #methods
    def lose_durability(self) -> None:
        prob = random.randrange(100)
        #weapon only loses durability occasionally, probability decreases with rarity
        if prob < (60 // self.rarity):
            self._durability -= 1

    def repair(self) -> None:
        """
        Repairs weapon, returning its current durability to max value
        """
        self._durability = self._max_durability

    def __str__(self) -> str:
        return f'Item: {self._id}\n Rarity: {self._rarity}\n Value: {self._value}\n Durability: {self._durability}/{self._max_durability}\n'

class Weapon(Item):

    def __init__(self, id, rarity):
        super().__init__(id, rarity)
        self._damage_dice = 0
        self._num_damage_dice = 0
        self._crit = 0

    #properties
    @property
    def damage_dice(self) -> int:
        """
        Returns damage dice
        """
        return self._damage_dice
    
    def set_damage_dice(self, num, dice) -> None:
        self._damage_dice = dice
        self._num_damage_dice = num

    def Set_crit_multiplier(self, crit)->None:
        self._crit = crit
    
    def __str__(self) -> str:
        return f'Item: {self._id}\n Rarity: {self._rarity}\n Value: {self._value}\n Durability: {self._durability}/{self._max_durability}\n Damage Dice: {self._num_damage_dice}d{self._damage_dice}\n'

class Armor(Item):

    def __init__(self, id, rarity):
        super().__init__(id, rarity)
        self._armor_value = 2*self._rarity

    #properties
    @property
    def armor_value(self) -> int:
        """
        Return the value of the armor
        """
        return self._armor_value
    
    def set_armor_value(self, armor) -> None:
        self._armor_value = armor
    
    def __str__(self) -> str:
        return f'Item: {self._id}\n Rarity: {self._rarity}\n Value: {self._value}\n Durability: {self._durability}/{self._max_durability}\n Armor Value: {self._armor_value}\n'