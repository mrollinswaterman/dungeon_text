#Shopkeep class
import math, random, time
from copy import deepcopy
import items
import item_compendium
import global_commands
import global_variables

STATS = {
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

    def __init__(self, forge_list:list=[]):
        self._forge_list = forge_list
        self._storehouse = {
            "WP": [],
            "AR": [],
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
            STATS[item.rarity] += 1
            self._storehouse[tag].append(item)

    def add_to_forge_list(self, items):
        if type(items) == list:
            self._forge_list = self._forge_list + items
        else:
            self._forge_list.append(items)
    
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
        self._inventory:list[items.Item] = inventory
        self._stock_size = len(self._inventory)
        self._gold = 100
        self._player_level = 0
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
    def set_player_level(self, num:int) -> None:
        self._player_level = num

    #BUY/SELL
    def sell(self, item:items.Item, buyer, num:int=1) -> bool:
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
                        global_commands.type_text(self.generate_successful_sale_message(item))
                        buyer.pick_up(item) 
                        return True
                    else:
                        global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.")
                        return False
                else:
                    global_commands.type_text(f"You can't carry the {item.id}.")
                    return False
            else:
                global_commands.type_text(f"The Shopkeep doesn't have any {item.id}s right now. Come back another time.")
                return True
        
    def sell_consumable(self, item: items.Consumable, buyer, quantity) -> bool:
        if item in self._inventory and item.quantity > 0:
            buyer_version = deepcopy(item)
            my_version:items.Consumable = self.find_item(item.id)
            if quantity <= my_version.quantity:
               pass
            else:
                global_commands.type_text(f"The Shopkeep does not have {quantity} {item.id}s. He'll sell you all that he has.\n")
                quantity = my_version.quantity
            if buyer.can_carry(buyer_version) is True:
                if buyer.spend_gold(buyer_version.total_value) is True:
                    self._gold += buyer_version.total_value
                    my_version.decrease_quantity(quantity)
                    global_commands.type_text(self.generate_successful_sale_message(buyer_version))
                    buyer.pick_up(buyer_version)
                    return True
                else:
                    global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.")
                    return False
            else:
                global_commands.type_text(f"You can't carry {quantity} {item.id}s.")
                return False
        else:
            global_commands.type_text(f"The Shopkeep doesn't have any {item.id}s right now. Come back another time.")
            return False
        
    def buy(self, item:items.Item, seller, num:int=1) -> bool:
        if item.id in seller.inventory:
            if self._gold >= item.value:
                self._gold -= item.value
                seller.gain_gold(item.value)
                seller.drop(item, num)
                self.stock(item)
                return True
        else:
            global_commands.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.\n")
            return False
        
    #INVENTORY/STOCK
    def stock(self, item: items.Item, num=1) -> None:
        self._inventory.append(item)
        item.set_owner(self)
        self._stock_size = len(self._inventory)

    def print_inventory(self):
        if len(self._inventory) == 0:
            print("Shop's empty!")
        global_commands.type_with_lines("For Sale:\n")
        for i in range(self.stock_size):
            item:items.Item = self._inventory[i]
            if i % 2 == 0 and i != 0:
                time.sleep(.05)
                print("\n\n")

            string = f"{i+1}. {item.name} ({item.stats}): {item.value}g, {item.weight} lbs"
            while (len(string) < 55):
                string = string + " "
            
            print(string + 2*"\t", end='')
            
        print("\n")#newline after last

        global_commands.print_with_lines(f"Your Gold: {global_variables.PLAYER.gold} \tCarrying Capacity: {global_variables.PLAYER.current_weight}/{global_variables.PLAYER.carrying_capacity}")

    def restock(self, warehouse:list, amount:int) -> None:
        ready_to_stock = set()
        for entry in warehouse:
            item:items.Item = entry

            if item.rarity == "Epic":
                if global_commands.probability(5) is True:
                    ready_to_stock.add(item)
            if item.rarity == "Rare":
                if global_commands.probability(10) is True:
                    ready_to_stock.add(item)
            if item.rarity == "Uncommon":
                if global_commands.probability(33) is True:
                    ready_to_stock.add(item)
            if item.rarity == "Common":
                if global_commands.probability(60 - 2*self._player_level) is True:
                    ready_to_stock.add(item)
            
            if len(ready_to_stock) == amount:
                break

        for item in ready_to_stock:
            self.stock(item)

    def find_item(self, id:str) -> items.Item:
        for item in self._inventory:
            if item.id == id:
                return item
            
    def empty_inventory(self):
        self._inventory = []
            
    #NARRATION
    def generate_successful_sale_message(self, item:items.Item) -> str:
        message_list = [
            f"The Shopkeep hands you the {item.name} and happily pockets your gold.",
            f"He takes your coin and slides you the {item.name}.",
            f"Upon seeeing your plump gold pouch, The Shopkeep grunts with approval and gets the {item.name} down for you.",
            f"He nods silently and makes the exchange.",
            f"Gold is gold.",
            f"The Shopkeep grins. You have the coin this time.",
            f"As you take the {item.name}, you wonder if it will be enough."
        ]

        return random.choice(message_list) + "\n"
