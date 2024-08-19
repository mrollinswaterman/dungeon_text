import csv
import global_commands

def load_item(type, save_data) -> "Item":

    def load_weapon():
        mold = {}
        mold["damage_dice"] = save_data["damage_dice"]
        mold["crit"] = int(save_data["crit"])
        mold["crit_range"] = save_data["crit_range"]
        mold["weight_class"] = save_data["weight_class"]
        mold["max_dex_bonus"] = int(save_data["max_dex_bonus"])

        obj = Weapon(save_data["id"], save_data["rarity"], mold)
        obj.load(save_data)
        return obj

    def load_armor():
        mold = {}
        mold["weight_class"] = save_data["weight_class"]
        mold["armor"] = int(save_data["armor"])
        mold["max_dex_bonus"] = int(save_data["max_dex_bonus"])

        obj = Armor(save_data["id"], save_data["rarity"], mold)
        obj.load(save_data)
        return obj

    def load_consumable():
        import item_compendium
        id = save_data["id"]
        obj = item_compendium.dict[id](id, save_data["rarity"], save_data["quantity"])
        return obj

    def load_resource():
        return load_consumable()

    match type:
        case "Weapon":
            return load_weapon()
        case "Armor":
            return load_armor()
        case "Consumable":
            return load_consumable()
        case "Resource":
            return load_resource()
        case _:
            raise ValueError(f"Attempted load of unrecognized item type '{type}'.")

def craft_item(type, mold):
    match type:
        case "Weapon":
            return Weapon(mold["id"], mold["rarity"], mold)
        case "Armor":
            return Armor(mold["id"], mold["rarity"], mold)
        case _:
            raise ValueError(f"Attempted to craft item of incorrect type '{type}'.")

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
            raise ValueError("Rarity not found in codex")

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
        """
        Init function for the base Item class
        """
        import player
        self._type = "Item"
        self._id = id
        self._name = id
        #RARITY STUFF
        self._rarity:Rarity = global_commands.generate_item_rarity() if rarity is None else Rarity(rarity)
        self._value = 10 * self._rarity.value
        self._max_durability = 10 * self._rarity.value
        #MISC
        self._durability = self._max_durability
        self._is_consumable = False
        self._weight_class = Weight_Class(None)
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
        return f"{self._rarity.string} {self._name}"
    @property
    def value(self) -> int:
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
    def rarity(self) -> Rarity:
        return self._rarity
    @property
    def is_consumable(self) -> bool:
        return self._is_consumable
    @property
    def weight(self) -> int:
        return self._weight_class.value
    @property
    def weight_class(self) -> Weight_Class:
        return self._weight_class
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
        if global_commands.probability((66 // self._rarity.value)):
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

    def set_pickup_message(self, msg:str) -> None:
        self._pickup_message = msg

    def break_item(self) -> None:
        self._id = "Broken " + self._id
        global_commands.type_text(f"Your {self._id} has broken!")

    def destroy(self) -> None:
        self._id = self._id + " Scrap"
        self._weight_class.value = 1
        self._weight_class.string = "None"
        self._max_durability = 0
    
    def set_description(self, words:str) -> None:
        self._description = words

    def set_owner(self, owner) -> None:
        self._owner = owner

    def save(self) -> None:
        self._tod = {
            "type": self._type,
            "id": self._id,
            "name": self._name,
            "rarity": self._rarity.string,
            "durability": self._durability,
        }
        #eqiupment special stats
        self._tod["mold"] = None
        #consumable special stats
        self._tod["quantity"] = None
        self._tod["unit_weight"] = None
        self._tod["unit_value"] = None

    def load(self, save:dict) -> None:
        self._id = save["id"]
        self._name = save["name"]
        self._type = save["type"]
        self._rarity = Rarity(save["rarity"])
        self._durability = int(save["durability"])
        self._value = 10 * self._rarity.value
        self._max_durability = 10 * self._rarity.value
        return None

    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity.string})",
            f"Value: {self._value}g",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Weight: {self.total_weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self._id}\n Rarity: {self._rarity.string}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n"

class Weapon(Item):

    def __init__(self, id, rarity=None, mold:dict=None):
        super().__init__(id, rarity)
        self._mold = mold
        self._weight_class = Weight_Class(mold["weight_class"])
        #durability
        self._max_durability = 10 * self._rarity.value
        self._durability = self._max_durability
        #value
        self._value = 15 * self._rarity.value

        self._type = "Weapon"

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
        return int(self._mold["crit"])
    @property
    def crit_range(self) -> int:
        if self._mold["crit_range"] == '' or self._mold["crit_range"] is None:
            return 20
        else: return int(self._mold["crit_range"])
    @property
    def max_dex_bonus(self) -> int:
        return int(self._mold["max_dex_bonus"])
    @property
    def type(self) -> str:
        return "Weapon"
    @property
    def attack_bonus(self) -> int:
        return self._rarity.value
    @property
    def weight(self) -> int:
        return int(self._weight_class.value + (self.damage_dice - 6) + (self.num_damage_dice - 1)) 
   
    def smelt(self, new_mold) -> None:
        self._mold = new_mold

    def roll_damage(self) -> int:
        return global_commands.XdY([self.num_damage_dice, self.damage_dice])

    def save(self) -> None:
        super().save()
        self._tod["mold"] = True
        for entry in self._mold:
            self._tod[entry] = self._mold[entry]

    def load(self, stats_file) -> None:
        super().load(stats_file)
        self.update_values()

    def update_values(self) -> None:
        self._value = 15 * self._rarity.value
        self._max_durability = 10 * self._rarity.value
    
    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity.string})",
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
        self._weight_class = Weight_Class(mold["weight_class"])
        self._type = "Armor"
        self._value = (20 * self._rarity.value) + (8 * self._weight_class.value)
        self._max_durability = 15 * self._rarity.value
        self._durability = self._max_durability

    #properties
    @property
    def mold(self) -> dict:
        return self._mold
    @property
    def armor_value(self) -> int:
        return int(self._mold["armor"])
    @property
    def stats(self) -> str:
        return f"{self.weight_class.string}, {self.armor_value}P"
    @property
    def weight_class(self) -> Weight_Class:
        return self._weight_class
    @property
    def max_dex_bonus(self) -> int:
        return int(self._mold["max_dex_bonus"])
    @property
    def weight(self) -> int:
        return int(self._weight_class.value * 5 + 2 * self.armor_value)

    #methods
    def smelt(self, new_mold:dict) -> None:
        self._mold = new_mold
        return None

    def save(self) -> None:
        super().save()
        self._tod["mold"] = True
        for entry in self._mold:
            self._tod[entry] = self._mold[entry]

    def load(self, stats_file) -> None:
        super().load(stats_file)
        self.update_values()
        return None
    
    def update_values(self) -> None:
        self._value = 10 * self._rarity.value
        self._max_durability = 10 * self._rarity.value

    def format(self):
        forms = [
            f"{self.id} ({self._rarity.string})",
            f"Class: {self.weight_class.string}",
            f"Armor: {self.armor_value}P",
            f"Durability: {self._durability}/{self._max_durability}",
            f"Value: {self._value}g",
            f"Weight: {self.weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self.id}\n Class: {self.weight_class.string}\n Armor Value: {self.armor_value}\n Rarity: {self._rarity.string}\n Value: {self._value}g\n Durability: {self._durability}/{self._max_durability}\n"

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
        forms = [
            f"{self.name} ({self._rarity.string})",
            f"Quantity: {self._quantity}",
            f"Value: {self.unit_value}g/each",
            f"Total Weight: {self.weight} lbs"
        ]
        return forms

    def __str__(self) -> str:
        return f"{self.id}\n Quantity: {self._quantity}\n Rarity: {self._rarity.string}\n Value: {self.value}g/each\n"


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

    def format(self) -> list[str]:
        forms = [
            f"{self.id} ({self._rarity.string})",
            f"Quantity: {self._quantity}",
            f"Value: {self.value}g",
            f"Weight: {self.weight} lbs"
        ]
        return forms
