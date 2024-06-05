#Repair Kit
import items, global_commands

class Repair_Kit(items.Consumable):

    def __init__(self):
        super().__init__("Repair Kit", "Uncommon", 0)
        self._unit_value = 10 * self._numerical_rarity
        self._unit_weight = .5
        self._type = "Repair_Kit"

    def use(self, target:items.Item) -> bool:
        """
        Repairs the item to full durability,
        Returns True if the item is not already full durability
        """
        if target.durability[0] < target._durability[1]:#ie item is damaged
            self.decrease_quantity(1)
            global_commands.type_text(f"{self.id} used. {self._quantity} remaining.")
            target.repair()
            return True
        return False
    
def craft(num):
    repair = Repair_Kit()
    repair.set_quantity(num)
    return repair