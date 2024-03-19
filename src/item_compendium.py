#item compendium
import items
import player
import global_commands
import status_effects
#import mob

PLAYER = None

class Health_Potion(items.Consumable):

    def __init__(self, rarity="Common", id="Health Potion", quantity=0):
        super().__init__(id, rarity, quantity)
        self._unit_weight = 0.5
        self._target:player.Player = PLAYER

    def use(self, target=PLAYER) -> bool:
        """
        Heals the target for a given amount
        """
        if self._target.hp < self._target.max_hp:
            self.decrease_quantity(1)
            global_commands.type_with_lines(f"{self.id} used. {self._quantity} remaining.\n")
            self._target.heal(self._strength)
            self._owner.spend_ap(1)
            return True
        global_commands.type_with_lines(" You are already full HP.")
        return False
    
def generate_hp_potions(rarity="Common", num=1):
    hp = Health_Potion(rarity)
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

class Firebomb(items.Consumable):
    
    def __init__(self, rarity="Uncommon", id="Firebomb", quantity=0):
        super().__init__(id, rarity, quantity)
        self._unit_value = 20 * self._numerical_rarity
        self._unit_weight = 1 
        self._target = None
        self._damage = self._strength

    def use(self, target):
        self._target = target
        throw = self._owner.roll_a_check("dex")
        dodge = target.roll_a_check("dex")

        self._owner.spend_ap()

        global_commands.type_with_lines(f" You throw a {self._id} at the {self._target.id}.\n")

        if dodge >= throw + 10:
            global_commands.type_text(f" The {self._target.id} dodged your {self._id} entirely!")
            return True
        
        if dodge >= throw:
            global_commands.type_text(f" The {self._target.id} partially dodged your {self._id}.\n")
            taken = self._target.take_damage(int(self._damage / 2))
            if global_commands.probability(50 - dodge): #--> this is a formattting thing the message doesn't change 
                global_commands.type_text(f" The {self._id} did {taken} damage to the {self._target.id}.\n")
                self.set_on_fire()
            else:
                global_commands.type_text(f" The {self._id} did {taken} damage to the {self._target.id}.")
            return True
        
        if throw > dodge:
            global_commands.type_text(f" You hit the {self._target.id}.\n")
            taken = self._target.take_damage(int(self._damage))
            if global_commands.probability(50):#--> this is a formattting thing the message doesn't change 
                global_commands.type_text(f" Your {self._id} did {taken} damage to the {self._target.id}.\n")
                self.set_on_fire()
            else:
                global_commands.type_text(f" Your {self._id} did {taken} damage to the {self._target.id}.")
            return True

    def set_on_fire(self) -> None:
        firebomb = status_effects.On_Fire(self._owner, self._target)
        firebomb.set_duration(3)
        firebomb.set_potency(self._numerical_rarity)
        firebomb.set_message(f" The {self._target.id} is now On Fire!")
        self._target.add_status_effect(firebomb)
       
def generate_firebombs(num):
    fb = Firebomb()
    fb.set_quantity(num)
    return fb


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
