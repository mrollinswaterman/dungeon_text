#Shopkeep class
import items
import player
import global_commands

class Shopkeep():

    def __init__(self, inventory=set()):
        self._inventory:set[items.Item] = inventory
        self._gold = 100
    #properties
    @property
    def inventory(self):
        return self._inventory
    @property
    def gold(self) -> int:
        return self._gold
    
    #methods

    def stock(self, item: items.Item) -> None:
        self._inventory.add(item)

    def sell(self, item:items.Item, buyer:player.Player, num:int=1) -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's 
        inventory and the player has sufficient gold

        Returns True if the sale goes through, False otherwise
        """
        if item in self._inventory:
            if buyer.gold >= item.value:
                buyer.lose_gold(item.value)
                self._gold += item.value
                if isinstance(item, items.Consumable) and item.quantity >= num:
                    item.quantity -= num
                    if item.quantity == 0:
                        self._inventory.remove(item)
                self._inventory.remove(item)
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
                self._inventory.add(item)
                return True
        else:
            global_commands.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.\n")
            return False
        
    def print_invevtory(self) -> None:
        for i, item in enumerate(self._inventory):
            print(f"")
            