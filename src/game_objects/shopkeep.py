#Shopkeep class

import random, time, csv
import globals
import game
import items
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import items

def forge_all_items():
    for _ in range(2):
        with open("csv_files/equipment_stats.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                game.ARMORY.add(globals.craft_item(row))

class Armory():

    def __init__(self):

        self.weapons:set["items.Weapon"] = set()
        self.armor:set["items.Armor"] = set()

    @property
    def master(self) -> set["items.Armor", "items.Weapon"]:
        """Returns a set containing all weapons and armor in the armory"""
        all = set()
        for i in self.weapons:
            all.add(i)
        for i in self.armor:
            all.add(i)
        return all 

    def get(self, id:str) -> items.Weapon | items.Armor:
        """Finds an item in the Armory"""
        for item in self.master:
            if item.id == id:
                return item
        return None
    
    def add(self, item:"items.Item") -> None:
        """Adds an item object to the appropriate set"""
        match item:
            case items.Weapon():
                self.weapons.add(item)
            case items.Armor():
                self.armor.add(item)
            case _:
                return False

    def print(self):
        """Prints the Armory's contents"""
        for item in self.master:
            print(item.id)

class Shopkeep():

    def __init__(self):
        self.inventory:list["items.Item"] = []
        self.gold = 100
        self.player = game.PLAYER
        self.max_stock_size = 12

    #properties
    @property
    def stock_size(self) -> int:
        return len(self.inventory)

    #methods
    def get(self, ref:"str | int | items.Item") -> items.Item | items.Stackable | None:
        match ref:
            case str():
                for item in self.inventory:
                    if item.id == ref:
                        return item
            case int():
                try:
                    return self.inventory[ref]
                except IndexError:
                    return None
            case _:
                for item in self.inventory:
                    if item == ref: return item

        globals.type_text(f"The Shopkeep doesn't have any {item.name} right now. Come back later.")
        return None

    #BUY/SELL
    def sell(self, item:"items.Item") -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's inventory and the player has sufficient gold
        Returns True if the sale goes through, False otherwise
        """
        import narrator

        if item is None:
            return False

        item = self.get(item)
        match item:
            case items.Stackable():
                num = narrator.ask_quantity()
                if num > item.quantity:
                    globals.type_text(f"The Shopkeep does not have {num} {item.name}. He'll sell you all that he has.")
                    num = item.quantity
                    self.inventory.remove(item)
                item.remove_quantity(num)
                #at this point, item is re-assigned to a new stackable object instance which is then 
                #added to the shopkeep's inventory to be sold to the player

                #this is done so that the Shopkeep can keep the old instance of the stackable object
                #if the player doesn't buy all available inventory
                item:items.Stackable = globals.craft_item(item.id)
                item.set_quantity(num)
                self.inventory.append(item)
            case _:
                pass

        if self.player.can_carry(item) is True:
            if self.player.spend_gold(item.value):
                self.gold += item.value
                self.inventory.remove(item)
                item.owner = None
                globals.type_text(self.generate_successful_sale_message(item))
                self.player.pick_up(item) 
                return True
            else:
                globals.type_text(f"The Shopkeep grunts and gestures to the {item.id}'s price. You don't have the coin.")
                return False
        else:
            globals.type_text(f"You can't carry the {item.name}.")
            return False
        
    def buy(self, item:"items.Item", num:int=1) -> bool:
        globals.under_construction()
        return None
        if item.id in self.player.inventory:
            if self.gold >= item.value:
                self.gold -= item.value
                self.player.gain_gold(item.value)
                self.player.drop(item, num)
                self.stock(item)
                return True
        else:
            globals.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.")
            return False
        
    #stock
    def stock(self, item: "items.Item") -> bool:
        if self.stock_size < self.max_stock_size:
            self.inventory.append(item)
            item.owner = self
            return True
        return False

    def restock(self) -> None:
        """Restocks the shop, adding default items (hp_pots and repair kits), plus an
            assortment of weapons+armor"""
        w_count = random.randrange(3, 6)
        a_count = random.randrange(3, 6)

        hp_pots:items.Stackable = globals.craft_item("Health_Potion", "Common")
        hp_pots.quantity = 5
        self.stock(hp_pots)

        for _ in range(w_count):
            self.stock(random.choice(list(game.ARMORY.weapons)))

        for _ in range(a_count):
            self.stock(random.choice(list(game.ARMORY.armor)))

    def check_stock(self):
        """Cleans the shopkeeps inventory of any items that should no longer be displayed."""
        for item in self.inventory:
            match item:
                case items.Stackable():
                    if item.quantity <= 0:
                        self.inventory.remove(item)
                case _:
                    pass
    #inventory
    def print_inventory(self):
        if len(self.inventory) == 0:
            print("Shop's empty!")
        globals.type_with_lines("For Sale:")
        print("")
        i = 0
        while (i < self.stock_size-1):
            if i % 2 == 0 and i != 0:
                time.sleep(.05)
                print("\n")
            item_1:list = self.inventory[i].display
            item_2:list = self.inventory[i+1].display

            item_1[0] = f"{i+1}. {item_1[0]}"
            item_2[0] = f"{i+2}. {item_2[0]}"
            globals.print_line_by_line([item_1, item_2], 55)
            i += 2

        print("\n")#double newline after last item
        p = game.PLAYER
        gold = f"Your Gold: {p.gold} \t"
        available = f" Available Capacity: {p.available_carrying_capacity} \t"
        maximum = f" Maximum Capacity {p.carrying}/{p.carrying_capacity}"
        footer = gold + available + maximum
        globals.type_with_lines()
        print(footer)
        print("")
            
    #NARRATION
    def generate_successful_sale_message(self, item:"items.Item") -> str:
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
