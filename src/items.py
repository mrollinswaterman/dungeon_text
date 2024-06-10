import csv
import global_commands

RARITY = {
    "Common": 1,
    "Uncommon": 2,
    "Rare": 3,
    "Epic": 4,
    "Legendary": 5,
    "Unique": 6 
}

WEIGHT_CLASS = {
    "None": 0,
    "Light": 2,
    "Medium": 4,
    "Heavy": 6,
    "Superheavy": 8
}

def numerical_rarity_to_str(rare:int):
    return list(RARITY.keys())[rare-1]

def generate_item(id, rarity, type):
    import item_compendium

    print(item_compendium.master)

    if id in item_compendium.master:
        return item_compendium.master[id](id, rarity)

    return TYPES[type](id, rarity)

class Item():

    def __init__(self, id:str, rarity=None):
        """
        Init function for the base Item class
        """
        import player
        self._type = "Item"
        self._id = id
        self._name = id
        #RARITY STUFF
        self._rarity = global_commands.generate_item_rarity() if rarity is None else rarity
        self._numerical_rarity = RARITY[self._rarity]
        self._value = 10 * self._numerical_rarity
        self._max_durability = 10 * self._numerical_rarity
        #MISC
        self._durability = self._max_durability
        self._is_consumable = False
        self._weight = 0
        self._pickup_message = f"You picked up a {self._id}."
        self._description = ""
        self._broken = False

        self._owner:"player.Player" = None

        self._tod = {}

    #properties
    @property
    def id(self) -> str:
        return self._id
    @property
    def name(self) -> str:
        """
        Returns the item's full indentifiction, including rarity
        """
        return f"{self._rarity} {self._name}"
    @property
    def value(self) -> int:
        return self._value
    @property
    def total_value(self) -> int:
        return self._value
    @property
    def owner(self) -> int:
        return self._owner
    @property
    def broken(self) -> bool:
        return self._durability <= 0 and not self.destroyed
    @property
    def destroyed(self) -> bool:
        return self._durability <= -(self._max_durability // 2)
    @property
    def durability(self) -> tuple[int, int]:
        return (self._durability, self._max_durability)
    @property
    def rarity(self) -> str:
        return self._rarity
    @property
    def numerical_rarity(self) -> int:
        return self._numerical_rarity
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
    def total_weight(self) -> int:
        return self._weight
    @property
    def pickup_message(self) -> str:
        return self._pickup_message
    @property
    def description(self) -> str:
        return self._description
    @property
    def type(self) -> str:
        return self._type
    @property
    def tod(self) -> dict:
        return self._tod
    #methods
    def lose_durability(self) -> None:
        """
        Checks to see if the item loses durability on this use
        """
        if global_commands.probability((66 // self._numerical_rarity)):
            self._durability -= 1
            if self.broken is True:
                self.break_item()

    def remove_durability(self, num:int) -> None:
        """
        Removes (num) durability from the item
        """
        self._durability -= num
        if self.broken is True:
            self._durability = 0
            self.break_item()

    def repair(self) -> None:
        """
        Repairs weapon, returning its current durability to max value
        """
        if not self.destroyed:
            self._durability = self._max_durability
            stopword = "Broken"
            query = self._id.split()

            resultwords = [word for word in query if word != stopword]
            print(resultwords)
            self._id = ''.join(resultwords)

    def set_weight(self, num:int) -> None:
        self._weight = num

    def set_stats(self, stats: tuple[int, int, int]):
        raise NotImplementedError

    def set_pickup_message(self, msg:str) -> None:
        self._pickup_message = msg

    def break_item(self) -> None:
        self._id = "Broken " + self._id
        global_commands.type_text(f"Your {self._id} has broken!")

    def destroy(self) -> None:
        self._id = self._id + " Scrap"
        self._weight = 1
        self._max_durability = 0
    
    def set_description(self, words:str) -> None:
        self._description = words

    def set_owner(self, owner) -> None:
        self._owner = owner

    def update(self) -> None:
        """
        Recalculates numerical rarity, value and max durability
        Only intended to be used after loading an item from
        a save file
        """
        self._numerical_rarity = RARITY[self._rarity]
        self._value = 10 * self._numerical_rarity
        self._max_durability = 10 * self._numerical_rarity

    def save(self) -> None:
        self._tod = {
            "type": self._type,
            "id": self._id,
            "name": self._name,
            "rarity": self._rarity,
            "durability": self._durability,
        }
        #weapons special stats
        self._tod["damage_dice"] = None
        self._tod["num_damage_dice"] = None
        self._tod["crit"] = None
        #armor special stats
        self._tod["weight_class"] = None
        #consumable special stats
        self._tod["quantity"] = None
        self._tod["unit_weight"] = None
        self._tod["unit_value"] = None

    def load(self, stats_file) -> None:
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._id = row["id"]
                self._name = row["name"]
                self._type = row["type"]
                self._rarity = row["rarity"]
                self._durability = int(row["durability"])
            file.close()
        self.update()

    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity})",
            f"Value: {self._value}g",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Weight: {self.total_weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self._id}\n Rarity: {self._rarity}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n"

class Weapon(Item):

    def __init__(self, id, rarity=None):
        super().__init__(id, rarity)
        self._value = 15 * self._numerical_rarity
        self._max_durability = 10 * self._numerical_rarity
        self._durability = self._max_durability
        self._damage_dice = 0
        self._num_damage_dice = 0
        self._crit = 0
        self._type = "Weapon"

    #properties
    @property
    def damage_dice(self) -> int:
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
        return "Weapon"
    @property
    def attack_bonus(self) -> int:
        return self._numerical_rarity
    
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

    def set_crit_multiplier(self, num:int)->None:
        self._crit = num

    def roll_damage(self) -> int:
        return global_commands.XdY([self._num_damage_dice, self._damage_dice])

    def update(self) -> None:
        self._value = 15 * self._numerical_rarity
        self._max_durability = 10 * self._numerical_rarity
        self._weight = int(2.5 * self._num_damage_dice + (self._damage_dice // 2))

    def save(self) -> dict:
        super().save()
        self._tod["damage_dice"] = self._damage_dice
        self._tod["num_damage_dice"] = self._num_damage_dice
        self._tod["crit"] = self._crit

    def load(self, stats_file, ) -> None:
        super().load(stats_file, )
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._damage_dice = int(row["damage_dice"])
                self._num_damage_dice = int(row["num_damage_dice"])

                self._crit = int(row["crit"])
            file.close()
        self.update()
    
    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity})",
            f"Damage: {self._num_damage_dice}d{self._damage_dice}, x{self._crit}",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Value: {self._value}g",
            f"Weight: {self.weight} lbs",
        ]
        return forms
    
    def __str__(self) -> str:
        return (f"{self.id}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n Damage Dice: {self._num_damage_dice}d{self._damage_dice}\n Weight: {self.weight} lbs\n")

class Armor(Item):

    def __init__(self, id:str, rarity=None, weight_class:int="Light"):
        super().__init__(id, rarity)
        self._weight_class = weight_class
        self._numerical_weight_class = WEIGHT_CLASS[self._weight_class]
        self._armor_value = int(self._numerical_weight_class + self._numerical_rarity - (self._numerical_weight_class / 2))
        self._value = (25 * self._numerical_rarity) + (10 * self.numerical_weight_class)
        self._broken = False
        self._weight = (self._numerical_weight_class * 5) + self._armor_value
        self._type = "Armor"

    #properties
    @property
    def armor_value(self) -> int:
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
            self.set_armor_value(int(self._numerical_weight_class + self._numerical_rarity - (self._numerical_weight_class / 2)))
        self._value = (25 * self._numerical_rarity) + (10 * self.numerical_weight_class)
        self._weight = (10 * self._numerical_weight_class) + self._armor_value

    def update(self) -> None:
        super().update()
        self._numerical_weight_class = WEIGHT_CLASS[self._weight_class]
        self._armor_value = int(self._numerical_weight_class + self._numerical_rarity - (self._numerical_weight_class / 2))
        self._value = (25 * self._numerical_rarity) + (10 * self.numerical_weight_class)

    def save(self) -> dict:
        super().save()
        self._tod["weight_class"] = self._weight_class

    def load(self, stats_file) -> None:
        super().load(stats_file)
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._weight_class = row["weight_class"]
            file.close()
        self.update()

    def format(self):
        forms = [
            f"{self.id} ({self._rarity})",
            f"Class: {self.weight_class}",
            f"Armor: {self._armor_value}P",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Value: {self._value}g",
            f"Weight: {self._weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self.id}\n Class: {self.weight_class}\n Armor Value: {self._armor_value}\n Rarity: {self._rarity}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n"

class Consumable(Item):

    def __init__(self, id:str, rarity="Common", quantity=1):
        super().__init__(id, rarity)
        self._quantity = quantity
        self._plural = True if self._quantity > 1 else False
        self._strength = self._numerical_rarity * 2
        self._is_consumable = True
        self._type = "Consumable"
        self._target = None
        self._unit_weight = 1
        self._unit_value = 8 * self._numerical_rarity
        self._value = self._unit_value * self._quantity

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
        return self._unit_weight
    @property
    def value(self) -> int:
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

    def update(self) -> None:
        self._plural = True if self._quantity > 1 else False
        self._value = self._unit_value * self._quantity
        self._weight = self._unit_weight * self._quantity

    def save(self) -> None:
        super().save()
        self._tod["quantity"] = self._quantity
        self._tod["unit_weight"] = self._unit_weight
        self._tod["unit_value"] = self._unit_value

    def load(self, stats_file) -> None:
        super().load(stats_file)
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self._quantity = int(row["quantity"])
                self._unit_weight = float(row["unit_weight"])
                self._unit_value = float(row["unit_value"])
            file.close()
        self.update()
    
    def format(self) -> list[str]:
        forms = [
            f"{self.name} ({self._rarity})",
            f"Quantity: {self._quantity}",
            f"Value: {self._unit_value}g/each",
            f"Total Weight: {self.total_weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self.id}\n Quantity: {self._quantity}\n Rarity: {self._rarity}\n Value: {self._unit_value}g/each\n"

TYPES = {
    "Item": Item,
    "Weapon": Weapon,
    "Armor": Armor,
    "Consumable": Consumable
}