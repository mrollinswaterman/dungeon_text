#Shopkeep class
import math, random
from copy import deepcopy
import items
import item_compendium
import player
import global_commands

class Blacksmith():
    """
    A class that take in lists of item data and turns
    them into objects of the correct type
    then stores them in a set for later use
    """

    def __init__(self, forge_list:list=[]):
        self._forge_list = forge_list
        self._storehouse = {
            "WP": set(),
            "AR": set(),
        }
        self._tag_map = {
            "WP": items.Weapon,
            "AR": items.Armor
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
    
    def forge(self):
        for mold in self._forge_list:
            tag, id, stats = mold
            item:items.Item = self._tag_map[tag](id)
            item.set_stats(stats)
            self._storehouse[tag].add(item)
        self._forge_list = []

    def add_to_forge_list(self, items):
        if type(items) == list:
            self._forge_list = self._forge_list + items
        else:
            self._forge_list.append(items) 

class Shopkeep():
    """
    A class that stores items for the player to buy
    and that can buy items from the player
    """

    def __init__(self, inventory=[]):
        self._inventory:list[items.Item] = inventory
        self._stock_size = len(self._inventory)
        self._gold = 100
        self._threat = 0
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
    #methods

    def stock(self, item: items.Item, num=1) -> None:
        self._inventory.append(item)
        self._stock_size = len(self._inventory)
        
    def set_threat(self, num:int) -> None:
        self._threat = num

    def sell(self, item:items.Item, buyer:player.Player, num:int=1) -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's 
        inventory and the player has sufficient gold

        Returns True if the sale goes through, False otherwise
        """
        if item.is_consumable:
            self.sell_consumable(item, buyer, num)
        else:
            if item in self._inventory:
                if buyer.can_carry(item) is True:
                    if buyer.spend_gold(item.value) is True:
                        self._gold += item.value
                        self._inventory.remove(item)
                        buyer.pick_up(item, 1) 
                        global_commands.type_text(f" The Shopkeep hands you the {item.name}, and happily pockets your gold.\n")
                        return True
                    else:
                        global_commands.type_text(f" The Shopkeep grunts and gestures to the {item.name}'s price. You don't have the coin.\n")
                        return False
                else:
                    global_commands.type_text(f" You can't carry the {item.name}.\n")
                    return False
            else:
                global_commands.type_text(f" The Shopkeep doesn't have any {item.name}s right now. Come back another time.\n")
                return True
        
    def sell_consumable(self, item: items.Consumable, buyer: player.Player, quantity) -> bool:
        if item in self._inventory and item.quantity > 0:
            buyer_version = deepcopy(item)
            buyer_version.set_quantity(1)
            my_version:items.Consumable = self.find_item(item.id)
            if quantity <= my_version.quantity:
               pass
            else:
                global_commands.type_text(f"The Shopkeep does not have {quantity} {item.name}s. He'll sell you all that he has.\n")
                quantity = my_version.quantity
            buyer_version.set_quantity(quantity)
            if buyer.can_carry(buyer_version) is True:
                if buyer.spend_gold(buyer_version.total_value) is True:
                    self._gold += buyer_version.total_value
                    my_version.decrease_quantity(quantity)
                    buyer_version.set_quantity(1)
                    global_commands.type_text(f" The Shopkeep hands you the {item.name}s and happily pockets your gold.\n")
                    buyer.pick_up(buyer_version, quantity)
                    return True
                else:
                    global_commands.type_text(f" The Shopkeep grunts and gestures to the {item.name}'s price. You don't have the coin.\n")
                    return False
            else:
                global_commands.type_text(f" You can't carry {quantity} {item.name}s.\n")
                return False
        else:
            global_commands.type_text(f" The Shopkeep doesn't have any {item.name}s right now. Come back another time.\n")
            return True

        
    def buy(self, item:items.Item, seller:player.Player, num:int=1) -> bool:
        if item.id in seller.inventory:
            if self._gold >= item.value:
                self._gold -= item.value
                seller.gain_gold(item.value)
                seller.drop(item, num)
                self.stock(item)
                return True
        else:
            global_commands.type_text(" The Shopkeep throws you a questioning glance as you try to sell him thin air.\n")
            return False
        
    def print_invevtory(self) -> None:
        if len(self._inventory) == 0:
            print("Shop's empty!")

        print("-"*110 + '\n')
        for num in range(self.stock_size+1):
            if num % 2 == 0:
                try:
                    item1:items.Item = self._inventory[num]
                    item2:items.Item = self._inventory[num+1]
                    string = (f"{num+1}. {item1.id} ({item1.stats}): {item1.value}g, {item1.weight} lbs"+'\t'*3+
                    f"{num+2}. {item2.id} ({item2.stats}): {item2.value}g, {item2.weight} lbs\n")
                    global_commands.type_list(string)
                    #print("")
                except IndexError:
                    try:
                        item1:items.Item = self._inventory[num]
                        string = f"{num+1}. {item1.id} ({item1.stats}): {item1.value}g, {item1.weight} lbs\n"
                        global_commands.type_list(string)
                        #print("")
                    except IndexError:
                        pass
            else:
                pass

        print("-"*110 + '\n')

    def restock(self, warehouse, amount) -> None:
        for item in warehouse:
            stock_chance = random.randrange(0, 100)
            stock_chance += self._threat
            if item not in self._inventory:
                if stock_chance > 90:
                    self.stock(item)
                elif stock_chance > 75 and item.numerical_rarity <= 3:
                    self.stock(item)
                elif stock_chance > 50 and item.numerical_rarity <= 2:
                    self.stock(item)
                elif stock_chance > 10 and item.numerical_rarity == 1:
                    self.stock(item)

            if len(self._inventory)  == self._max_stock - amount:
                break

        if len(self._inventory) < self._max_stock - amount:
            self.restock(warehouse, amount)

    def find_item(self, id:str) -> items.Item:
        for item in self._inventory:
            if item.id == id:
                return item
