#Shopkeep class
import random, time, copy, csv
from items import Item, Consumable, Weapon, Armor, craft_item
import global_variables, global_commands

STOCK = {
    "Common": 0,
    "Uncommon": 0,
    "Rare": 0,
    "Epic": 0
}

class Blacksmith():
    """
    A class that take in lists of item data and turns
    them into objects of the correct type
    then stores them in a set for later use
    """

    def __init__(self):
        self._forge_list = []
        self._storehouse = {
            "Weapon": [],
            "Armor": [],
        }

    #properties
    @property
    def forge_list(self):
        return self._forge_list
    @property
    def storehouse(self):
        return self._storehouse

    def items_of_type(self, type=""):
        return self._storehouse[type]
    
    def forge(self, mold:dict):
        """for mold in self._forge_list:
            tag, id, stats = mold
            item:Item = self._tag_map[tag](id)
            item.set_stats(stats)
            STOCK[item.rarity] += 1
            self._storehouse[tag].append(item)"""

        item = craft_item(mold["type"], mold)
        self._storehouse[mold["type"]].append(item)

    def initialize(self):
        self._storehouse = {
            "Weapon": [],
            "Armor": [],
        }
        with open("equipment_stats.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.forge(row)

    def print_storehouse(self):
        for type in self._storehouse:
            for item in self._storehouse[type]:
                print(item)

class Shopkeep():
    """
    A class that stores items for the player to buy
    and that can buy items from the player
    """

    def __init__(self, inventory=[]):
        self._inventory:list[Item] = inventory
        self._stock_size = len(self._inventory)
        self._gold = 100
        self._player = global_variables.PLAYER
        self._max_stock = 10
    #properties
    @property
    def inventory(self):
        return self._inventory
    @property
    def gold(self) -> int:
        return self._gold
    @property
    def stock_size(self) -> int:
        return len(self._inventory)

    #BUY/SELL
    def sell(self, item:Item) -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's 
        inventory and the player has sufficient gold

        Returns True if the sale goes through, False otherwise
        """
        if item is None:
            return False

        import narrator
        if item.is_consumable:
            num = narrator.ask_quantity()
            return self.sell_consumable(item, num)

        if item in self._inventory:
            if self._player.can_carry(item) is True:
                if self._player.spend_gold(item.value) is True:
                    self._gold += item.value
                    self._inventory.remove(item)
                    global_commands.type_text(self.generate_successful_sale_message(item))
                    self._player.pick_up(item) 
                    return True
                else:
                    global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.")
                    return False
            else:
                global_commands.type_text(f"You can't carry the {item.id}.")
                return False
        else:
            global_commands.type_text(f"The Shopkeep doesn't have any {item.id}s right now. Come back another time.")
            return False
        
    def sell_consumable(self, item: Consumable, quantity) -> bool:
        if item is None:
            return False

        if item in self._inventory and item.quantity > 0:
            buyer_version = copy.deepcopy(item)
            my_version:Consumable = self.get_item(item.id)
            if quantity > my_version.quantity:
                global_commands.type_text(f"The Shopkeep does not have {quantity} {item.id}s. He'll sell you all that he has.")
                quantity = my_version.quantity
                
            buyer_version.set_quantity(quantity)
            if self._player.can_carry(buyer_version) is True:
                if self._player.spend_gold(buyer_version.total_value) is True:
                    self._gold += buyer_version.total_value
                    my_version.decrease_quantity(quantity)
                    if my_version.quantity <= 0:
                        self._inventory.remove(my_version)
                    global_commands.type_text(self.generate_successful_sale_message(buyer_version))
                    self._player.pick_up(buyer_version)
                    return True
                else:
                    global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.")
                    return False
            else:
                global_commands.type_text(f"You can't carry {quantity} {item.name}.")
                return False
        else:
            global_commands.type_text(f"The Shopkeep doesn't have any {item.name} right now. Come back another time.")
            return False
        
    def buy(self, item:Item, num:int=1) -> bool:
        if item.id in self._player.inventory:
            if self._gold >= item.value:
                self._gold -= item.value
                self._player.gain_gold(item.value)
                self._player.drop(item, num)
                self.stock(item)
                return True
        else:
            global_commands.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.")
            return False
        
    #INVENTORY/STOCK
    def stock(self, item: Item, num=1) -> None:
        self._inventory.append(item)
        item.set_owner(self)
        self._stock_size = len(self._inventory)

    def print_inventory(self):
        if len(self._inventory) == 0:
            print("Shop's empty!")
        global_commands.type_with_lines("For Sale:")
        for i in range(self.stock_size):
            item:Item = self._inventory[i]
            if i % 2 == 0 and i != 0:
                time.sleep(.05)
                print("\n\n")

            # change rarity.string to some item specific stat block
            string = f" {i+1}. {item.name} ({item.rarity.string}): {item.value}g, {item.weight} lbs"
            string = global_commands.match(string, 55)
            
            print(string + 2*"\t", end='')
            
        print("\n")#double newline after last item
        p = global_variables.PLAYER
        gold = f"Your Gold: {p.gold} \t"
        available = f" Available Capacity: {p.available_carrying_capacity} \t"
        maximum = f" Maximum Capacity {p.carrying}/{p.carrying_capacity}"
        footer = gold + available + maximum
        global_commands.type_with_lines()
        print(footer)
        print("")
        #global_commands.type_text(footer, 0.012)

    def restock(self, warehouse:list, amount:int) -> None:
        ready_to_stock = set()
        for entry in warehouse:
            item:Item = entry

            if item.rarity.string == "Epic":
                if global_commands.probability(5) is True:
                    ready_to_stock.add(item)
            if item.rarity.string == "Rare":
                if global_commands.probability(10) is True:
                    ready_to_stock.add(item)
            if item.rarity.string == "Uncommon":
                if global_commands.probability(33) is True:
                    ready_to_stock.add(item)
            if item.rarity.string == "Common":
                if global_commands.probability(60 - 2*self._player.level) is True:
                    ready_to_stock.add(item)
            
            if len(ready_to_stock) == amount:
                break

        for item in ready_to_stock:
            self.stock(item)

    def get_item(self, ref:str|int) -> Item | None:
        match ref:
            case str():
                for item in self._inventory:
                    if item.id == ref:
                        return item
                return None
            case int():
                try:
                    return self.inventory[ref]
                except IndexError:
                    return None
      
    def empty_inventory(self):
        self._inventory = []
            
    #NARRATION
    def generate_successful_sale_message(self, item:Item) -> str:
        message_list = [
            f"The Shopkeep hands you the {item.name} and happily pockets your gold.",
            f"He takes your coin and slides you the {item.name}.",
            f"Upon seeeing your plump gold pouch, The Shopkeep grunts with approval and gets the {item.name} down for you.",
            f"He nods silently and makes the exchange.",
            f"Gold is gold.",
            f"The Shopkeep grins. You have the coin this time.",
            f"As you take the {item.name}, you wonder if it will be enough to save you..."
        ]

        return random.choice(message_list)
