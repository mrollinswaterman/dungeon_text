#item compendium
import items
import player

class Health_Potion(items.Consumable):

    def __init__(self, rarity=1, id="Health Potion", quantity=0):
        super().__init__(id, rarity, quantity)
        self._value = 10 * rarity
    
    def use(self, target: player.Player) -> None:
        """
        Heals the target for a given amount
        """
        if target.hp < target.max_hp:
            self._quantity -= 1
            target.heal(self._strength)
            return True
        return False
    
def generate_hp_potions(rarity, num):
    hp = Health_Potion(list(items.RARITY.values()).index(rarity) +1)
    #the above is just a formula to find numerical rarity from a string
    hp.increase_quantity(num)
    return hp


    
class Repair_Kit(items.Consumable):

    def __init__(self, rarity=2, id="Repair Kit", quantity=0):
        super().__init__(id, rarity, quantity)

        self._value = 10 * rarity

    def use(self, target: items.Item) -> None:
        """
        Repairs the item to full durability
        """
        if target.durability[0] < target._durability[1]:#ie item is damaged
            target.repair()
            return True
        return False

def generate_repair_kits(num):

    repair = Repair_Kit()
    repair.increase_quantity(num)
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
    (("WP"), "Halberd", "1d10,x3"),
    (("WP"), "Lance", "1d8,x2")
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
