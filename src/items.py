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

    try:
        return item_compendium.dict[id](id, rarity)
    except KeyError:
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
        #eqiupment special stats
        self._tod["mold"] = None
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

    def __init__(self, id, rarity=None, mold:dict=None):
        super().__init__(id, rarity)
        self._mold = mold
        #durability
        self._max_durability = 10 * self._numerical_rarity
        self._durability = self._max_durability
        #value
        self._value = 15 * self._numerical_rarity

        self._type = "Weapon"

        self.smelt()

    #properties
    @property
    def mold(self) -> dict:
        return self._mold
    @property
    def damage_dice(self) -> int:
        return int(str(self._mold["damage_dice"]).split("d")[1])
    @property
    def num_damage_dice(self) -> int:
        return int(str(self._mold["damage_dice"]).split("d")[0])
    @property
    def stats(self) -> int:
        return f"{self.num_damage_dice}d{self.damage_dice}, x{self.crit}"
    @property
    def crit(self) -> int:
        return self._mold["crit"]
    @property
    def crit_range(self) -> int:
        return self._mold["crit_range"]
    @property
    def max_dex_bonus(self) -> int:
        return self._mold["max_dex_bonus"]
    @property
    def type(self) -> str:
        return "Weapon"
    @property
    def attack_bonus(self) -> int:
        return self._numerical_rarity
    @property
    def weight(self) -> int:
        heft = WEIGHT_CLASS[self._mold["weight_class"]]
        return int(2.5 * heft + (self.damage_dice * self.num_damage_dice)) 
   
    def smelt(self, new_mold) -> None:
        self._mold = new_mold

    def roll_damage(self) -> int:
        return global_commands.XdY([self.num_damage_dice, self.damage_dice])

    def save(self) -> dict:
        super().save()
        self._tod["mold"] = self._mold

    def load(self, stats_file, ) -> None:
        super().load(stats_file, )
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                raise Exception
                self._damage_dice = int(row["damage_dice"])
                self._num_damage_dice = int(row["num_damage_dice"])
                self._crit = int(row["crit"])
            file.close()
        self.update()
    
    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity})",
            f"Damage: {self.num_damage_dice}d{self.damage_dice}, x{self.crit}",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Value: {self._value}g",
            f"Weight: {self.weight} lbs",
        ]
        return forms
    
    def __str__(self) -> str:
        return (f"{self.id}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n Damage Dice: {self.num_damage_dice}d{self.damage_dice}\n Weight: {self.weight} lbs\n")

class Armor(Item):

    def __init__(self, id:str, rarity=None, mold:dict=None):
        super().__init__(id, rarity)
        self._mold = mold
        self._type = "Armor"
        self._value = (25 * self.numerical_rarity) + (10 * self.numerical_weight_class)
        self._max_durability = 15 * self._numerical_rarity
        self._durability = self._max_durability

    #properties
    @property
    def mold(self) -> dict:
        return self._mold
    @property
    def armor_value(self) -> int:
        return self._mold["armor"]
    @property
    def stats(self) -> str:
        return f"{self.weight_class}, {self.armor_value}P"
    @property
    def weight_class(self) -> str:
        return self._mold["weight_class"]
    @property
    def numerical_weight_class(self) -> int:
        return WEIGHT_CLASS[self.weight_class]
    @property
    def max_dex_bonus(self) -> int:
        return self._mold["max_dex_bonus"]
    @property
    def weight(self) -> int:
        return self.numerical_weight_class * 5 + 2*self.armor_value

    #methods
    def smelt(self, new_mold:dict) -> None:
        self._mold = new_mold
        return None

    def save(self) -> dict:
        super().save()
        self._tod["mold"] = self._mold
        return self._tod

    def load(self, stats_file) -> None:
        super().load(stats_file)
        with open(stats_file, encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                raise Exception
            file.close()
        self.update()

    def format(self):
        forms = [
            f"{self.id} ({self._rarity})",
            f"Class: {self.weight_class}",
            f"Armor: {self.armor_value}P",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Value: {self._value}g",
            f"Weight: {self._weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self.id}\n Class: {self.weight_class}\n Armor Value: {self.armor_value}\n Rarity: {self._rarity}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n"

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

    def set_weight(self, num: int) -> None:
        super().set_weight(num)
        self._unit_weight = num

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

    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity})",
            f"Quantity: {self._quantity}",
            f"Value: {self._value}g",
            f"Weight: {self.total_weight} lbs"
        ]
        return forms

TYPES = {
    "Item": Item,
    "Weapon": Weapon,
    "Armor": Armor,
    "Consumable": Consumable,
    "Resource": Resource
}