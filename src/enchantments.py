#Weapon+Armor enchantments file
"""from game_object import Game_Object
from item import Item
from effects import Effect
from condition import Condition

class Weapon_Enchantment():

    def __init__(self, parent:Game_Object | Item) -> None:
        self.parent = parent
        self.id = "Enchantment"
        self.target = None
        self.cost = 1

        match parent:
            case Game_Object(): self.target = self.parent.target
            case Item(): self.target = self.parent.owner.target

        self.active_effects:dict[str:list[Condition]] = {
            "on_hit":[],
            "on_attack":[],
            "on_miss":[]
        }

    def apply(self, effect_type:str):
        for condition in self.active_effects[effect_type]:
            self.target.conditions.add(condition)"""


    