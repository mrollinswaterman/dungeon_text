#Shopkeep class
import random, time, copy, csv
from item import Item
from equipment import Weapon, Armor
from stackable import Stackable
import global_variables, global_commands

def forge_all_items():
    for _ in range(2):
        with open("equipment_stats.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                global_variables.ARMORY.add(global_commands.create_item(row))

class Armory():

    def __init__(self):

        self.weapons:set[Weapon] = set()
        self.armor:set[Armor] = set()

    
    @property
    def master(self) -> set[Armor, Weapon]:
        """Returns a set containing all weapons and armor in the armory"""
        all = self.weapons
        for i in self.armor:
            all.add(i)
        return all

    def get(self, id:str) -> Weapon | Armor:
        """Finds an item in the Armory"""
        for item in self.master:
            if item.id == id:
                return item
        return None
    
    def add(self, item:Item) -> None:
        """Adds an item object to the appropriate set"""
        match item:
            case Weapon():
                self.weapons.add(item)
            case Armor():
                self.armor.add(item)
            case _:
                return False

    def print(self):
        """Prints the Armory's contents"""
        for item in self.master:
            print(item.id)

class Shopkeep():

    def __init__(self):
        self.inventory:list[Item] = []
        self.gold = 100
        self.player = global_variables.PLAYER
        self.max_stock_size = 12

    #properties
    @property
    def stock_size(self) -> int:
        return len(self.inventory)

    #methods
    def get_item(self, ref:str|int) -> Item | Stackable | None:
        match ref:
            case str():
                for item in self.inventory:
                    if item.id == ref:
                        return item
                return None
            case int():
                try:
                    return self.inventory[ref]
                except IndexError:
                    return None

    #BUY/SELL
    def sell(self, item:Item) -> bool:
        """
        Sells an item to a player if the item is in the Shopkeep's inventory and the player has sufficient gold
        Returns True if the sale goes through, False otherwise
        """
        if item is None:
            return False

        match item:
            case Stackable():
                return self.sell_stackable(item)
            case _:
                if item in self.inventory:
                    if self.player.can_carry(item) is True:
                        if self.player.spend_gold(item.value):
                            self.gold += item.value
                            self.inventory.remove(item)
                            item.owner = None
                            global_commands.type_text(self.generate_successful_sale_message(item))
                            self.player.pick_up(item) 
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
        
    def sell_stackable(self, item:Stackable) -> bool:
        import narrator

        num = narrator.ask_quantity()
        held = self.get_item(item)
        selling:Stackable = copy.deepcopy(item)
        if held is not None and held.quantity > 0:
            if num > held.quantity:
                global_commands.type_text(f"The Shopkeep does not have {num} {item.id}s. He'll sell you all that he has.")
                num = held.quantity
            selling.set_quantity(num)
            if self.player.can_carry(selling) is True:
                if self.player.spend_gold(selling.value) is True:
                    self.gold += selling.value
                    held.decrease_quantity(num)
                    if held.quantity <= 0:
                        self.inventory.remove(held)
                        held.owner = None
                    global_commands.type_text(self.generate_successful_sale_message(selling))
                    self.player.pick_up(selling)
                    return True
                else:
                    global_commands.type_text(f"The Shopkeep grunts and gestures to the {item.name}' price. You don't have the coin.")
                    return False
            else:
                global_commands.type_text(f"You can't carry {num} {item.name}.")
                return False
        else:
            global_commands.type_text(f"The Shopkeep doesn't have any {item.name} right now. Come back another time.")
            return False
        
    def buy(self, item:Item, num:int=1) -> bool:
        if item.id in self.player.inventory:
            if self.gold >= item.value:
                self.gold -= item.value
                self.player.gain_gold(item.value)
                self.player.drop(item, num)
                self.stock(item)
                return True
        else:
            global_commands.type_text("The Shopkeep throws you a questioning glance as you try to sell him thin air.")
            return False
        
    #INVENTORY/STOCK
    def stock(self, item: Item) -> bool:
        if self.stock_size < self.max_stock_size:
            self.inventory.append(item)
            item.owner = self
            return True
        return False

    def print_inventory(self):
        if len(self.inventory) == 0:
            print("Shop's empty!")
        global_commands.type_with_lines("For Sale:")
        for i in range(self.stock_size):
            item:Item = self.inventory[i]
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

    def restock(self) -> None:
        #add HP + repair kit stocking here
        from global_variables import ARMORY
        w_count = random.randrange(3, 6)
        a_count = random.randrange(3, 6)

        for _ in range(w_count):
            self.stock(random.choice(list(ARMORY.weapons)))

        for _ in range(a_count):
            self.stock(random.choice(list(ARMORY.armor)))
            
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
