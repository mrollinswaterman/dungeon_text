#Inventory class file
import globals
import os
import csv
import time
import game_objects
import items

class Inventory():
    def __init__(self, owner:game_objects.Game_Object):
        self.owner = owner
        self.contents:dict[str, items.Item | items.Stackable] = {}

    @property
    def total_weight(self):
        ret = 0.0
        for item in self.contents:
            ret += self.contents[item].weight
        return int(ret)

    def pick_up(self, item: items.Item | items.Stackable, silent:bool=False) -> bool:
        """Adds an item to the Object's inventory"""
        if not self.owner.can_carry(item):
            return False
        base = globals.get_subtype(item)
        match base:
            case "Stackable":
                #if you have a stack of those items already, just add to it
                held:"items.Stackable" | None = self.get_item(item.id)
                if held is not None:
                    held.set_quantity(held.quantity + item.quantity)
                #if you don't, add the object to your inventory
                else:
                    self.contents[item.id] = item
            case "Item" | "Equipment":
                self.contents[item.id] = item
            case _:
                raise ValueError(f"Unrecognized object {item}.")

        item.owner = self.owner
        return True
    
    def drop(self, item:items.Item, silent=False):
        item = self.get_item(item)
        if item is not None:
            if not silent:
                globals.type_text(f"{self.owner.header.default} dropped {item.name}!")
            del self.contents[item.id]
            item.owner = None

    def clear(self):
        for item in self.contents:
            item.owner = None

        self.contents = {}

    def get_item(self, ref:items.Item | str | int | None) -> "items.Item | None":
        """
        Checks if the Object has an item in it's inventory. 
        Returns the item if so, else None

        ref: can be str (item id), int (item index), or an instance of the Item class
        """
        base = globals.get_base_type(ref)
        match base:
            case "str":
                try: return self.contents[ref]
                except KeyError: return None

            case "int":
                try: return list(self.contents.values())[ref]
                except IndexError: return None

            case "Item":
                try: return self.contents[ref.id]
                except KeyError: return None

            case _: raise ValueError(f"Unrecogized type '{type(ref)}'.")

    def print_item(self, start:int, equipment:"items.Item"):
        """
        Processes an item's format property and feeds it to globals.print_line_by_line
        to be printed
        """
        index = start
        item_1 = [""]
        item_2 = [""]
        equip_format = [""]
        if self.get_item(index + 1) is not None:
            item_1 = self.get_item(index).format
            item_1[0] = f"{index+1}. {item_1[0]}"

            item_2 = self.get_item(index + 1).format
            item_2[0] = f"{index+2}. {item_2[0]}"
        elif self.get_item(index) is not None:
            item_1 = self.get_item(index).format
            item_1[0] = f"{index+1}. {item_1[0]}"

        if equipment is not None:
            equip_format = equipment.format
            equipment_index = 1 if index == 0 else index
            equip_format[0] = f"{equipment_index}. {equip_format[0]}"

        globals.print_line_by_line([item_1, item_2, equip_format])
    
    def display(self):
        """Formats and prints the players inventory, line-by-line"""
        item_index = 0

        while(item_index < len(self.contents) + 4):
            equipment = None
            if item_index == 0:
                equipment = self.owner.weapon
            elif item_index == 2:
                equipment = self.owner.armor
            self.print_item(item_index, equipment)
            item_index += 2
            print("\n")

    def print_contents(self):
        line_len = 30
        globals.type_with_lines()
        print(f'{line_len * " "}Inventory:{line_len * " "}\t\t\tEquipped:\n')
        self.display()
        print(f"Gold: {self.owner.gold}g", end='')
        time.sleep(0.05)
        print(f"\t Carrying Capacity: {self.owner.carrying}/{self.owner.carrying_capacity}\n")
        globals.type_with_lines()
        return None
    
    def load(self, filename:str) -> None:
        #check if inventory file is emtpty
        empty_check = True if os.stat(filename).st_size == 0 else False
        if empty_check: return None
        size = 0
        for item in list(self.contents.keys()):
            del self.contents[item]
        self.contents = {}
        self.owner.weapon = None
        self.owner.armor = None
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                size += 1
            file.close()
        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader):
                id = row["id"]
                item = globals.craft_item(id)
                item.load(row)
                if idx >= size - 2:
                    self.owner.equip(item, True)
                else:
                    self.pick_up(item, True)
            file.close()