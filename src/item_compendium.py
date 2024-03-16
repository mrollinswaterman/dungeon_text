#item compendium
import items
import player
import global_commands

class Health_Potion(items.Consumable):

    def __init__(self, rarity="Common", id="Health Potion", quantity=0):
        super().__init__(id, rarity, quantity)
        self._unit_weight = 0.5

    def use(self, target: player.Player) -> bool:
        """
        Heals the target for a given amount
        """
        if target.hp < target.max_hp:
            self.decrease_quantity(1)
            global_commands.type_with_lines(f"{self.id} used. {self._quantity} remaining.\n")
            target.heal(self._strength)
            self._owner.spend_ap(1)
            return True
        global_commands.type_with_lines(" You are already full HP.")
        return False
    
def generate_hp_potions(rarity="Common", num=1):
    hp = Health_Potion(rarity)
    #the above is just a formula to find numerical rarity from a string
    hp.set_quantity(num)
    return hp

class Repair_Kit(items.Consumable):

    def __init__(self, rarity="Uncommon", id="Repair Kit", quantity=0):
        super().__init__(id, rarity, quantity)
        self._unit_value = 10 * self._numerical_rarity
        self._unit_weight = .5

    def use(self, target: items.Item) -> bool:
        """
        Repairs the item to full durability
        """
        if target.durability[0] < target._durability[1]:#ie item is damaged
            self.decrease_quantity(1)
            global_commands.type_with_lines(f"{self.id} used. {self._quantity} remaining.\n")
            target.repair()
            return True
        return False

def generate_repair_kits(num):
    repair = Repair_Kit()
    repair.set_quantity(num)
    return repair

#tag, id, (num dice, dice type, crit)
WEAPONS_DICTIONARY = [

    (("WP"), "Battleaxe", "1d8,x2"),
    (("WP"), "Light Flail", "1d8,x2"),
    (("WP"), "Scimitar", "1d6,x4"),
    (("WP"), "Trident", "1d10,x2"),
    (("WP"), "Mace", "1d8,x2"),
    (("WP"), "Greatsword", "2d6,x2"),
    (("WP"), "Glaive", "1d10,x3"),
    (("WP"), "Greataxe", "1d12,x3"),
    (("WP"), "Scythe", "2d4,x5"),
    (("WP"), "Halberd", "1d10,x3")
]

ARMOR_DICTIONARY = [
    (("AR"), "Studded Leather", ("Light", None)),
    (("AR"), "Haramaki", ("None", 1)),
    (("AR"), "Chain Shirt", ("Light", None)),
    (("AR"), "Breastplate", ("Medium", None)),
    (("AR"), "Chainmail", ("Medium", 6)),
    (("AR"), "Armored Coat", ("Medium", None)),
    (("AR"), "Scale Mail", ("Medium", None)),
    (("AR"), "Half-plate", ("Heavy", None)),
    (("AR"), "Stoneplate", ("Heavy", 9)),
    (("AR"), "Branded Mail", ("Heavy", None)),
    (("AR"), "Full-plate", ("Heavy", 9)),
]
