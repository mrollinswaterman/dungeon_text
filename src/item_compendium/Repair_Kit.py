#Repair Kit
import items, global_commands

class Repair_Kit(items.Consumable):

    def __init__(self, id="Repair Kit", rarity="Uncommon", quantity=0):
        super().__init__(id, rarity, quantity)
        self._unit_value = 10 * self._rarity.value
        self._unit_weight = 5
        self._name = "Repair Kit"

    def use(self, target:items.Item) -> bool:
        """
        Repairs the item to full durability,
        Returns True if the item is not already full durability
        """
        if target.durability[0] < target._durability[1]:#ie item is damaged
            self.decrease_quantity(1)
            global_commands.type_text(f"{self._id} used. {self._quantity} remaining.")
            target.repair()
            return True
        return False
    
def craft(num=1):
    repair = Repair_Kit()
    repair.set_quantity(num)
    return repair

object = Repair_Kit