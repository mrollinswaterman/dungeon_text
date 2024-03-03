#Shopkeep class
import math, random
import items
import item_compendium
import player
import global_commands

class Shopkeep():

    def __init__(self, inventory={}):
        self._inventory:dict[int, items.Item] = inventory
        self._stock_size = len(list(self._inventory.keys()))
        self._gold = 100
        self._threat = 0
    #properties
    @property
    def inventory(self):
        return self._inventory
    @property
    def gold(self) -> int:
        return self._gold
    @property
    def stock_size(self) -> int:
        return len(list(self._inventory.keys()))
    #methods

    def stock(self, item: items.Item, num=1) -> None:
        self._inventory[self.stock_size + 1] = item
        
    def set_threat(self, num:int) -> None:
        self._threat = num

    def sell(self, item:items.Item, buyer:player.Player, num:int=1) -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's 
        inventory and the player has sufficient gold

        Returns True if the sale goes through, False otherwise
        """
        id_num = 0

        if item in list(self._inventory.values()):
            for i in self._inventory:
                if self._inventory[i] == item:
                    id_num = i
                    break
            if buyer.gold >= item.value:
                buyer.lose_gold(item.value)
                self._gold += item.value
                if isinstance(item, items.Consumable) and item.quantity >= num:
                    item.quantity -= num
                    if item.quantity == 0:
                        del self._inventory[id_num]
                del self._inventory[id_num]
                buyer.pick_up(item, num) 
                global_commands.type_text(f"The Shopkeep hands you the {item.id}, and happily pockets your gold coins.\n")
                return True
            else:
                global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.\n")
                return False
        else:
            global_commands.type_text(f"The Shopkeep doesn't have any {item.id}s right now. Come back another time.\n")
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
            global_commands.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.\n")
            return False
        
    def print_invevtory(self) -> None:
        if len(self.inventory) == 0:
            print("Shop's empty!")
        print("")
        for num in self._inventory:
            item:items.Item = self._inventory[num]
            global_commands.type_text(f"{num}. {item.id} ({item.stats}): {item.value}g", 0.01, False)
            print(""*110)

    def restock(self, warehouse: dict[tuple[str, tuple[int,int], int]], amount) -> None:
        for entry in warehouse:
            id, stats = entry



            stock_chance = random.randrange(0, 100)
            stock_chance += self._threat
            if item not in list(self._inventory.keys()):
                if stock_chance > 90:
                    self.stock(item)
                elif stock_chance > 75 and item.numerical_rarity <= 3:
                    self.stock(item)
                elif stock_chance > 50 and item.numerical_rarity <= 2:
                    self.stock(item)
                elif stock_chance > 10 and item.numerical_rarity == 1:
                    self.stock(item)

            if len(self._inventory) == amount:
                break

        if len(self._inventory) < amount:
            self.stock(warehouse, amount)