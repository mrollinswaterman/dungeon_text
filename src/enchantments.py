#Weapon+Armor enchantments file
import csv
from game_object import Game_Object
from equipment import Equipment
from condition import Condition
import conditions

TOME = {}

class Weapon_Enchantment():

    def __init__(self, parent:Game_Object | Equipment=None) -> None:
        self.parent = parent
        self.id = "Weapon Enchatment"
        self.target:Game_Object = None
        self.cost = 1

        self.active_effects:dict[str:list[Condition]] = {
            "on_hit":[],
            "on_attack":[],
            "on_miss":[]
        }

    def initialize(self, object:Game_Object | Equipment):
        self.parent = object
        match self.parent:
            case Game_Object(): self.target = self.parent.target
            case Equipment(): self.target = self.parent.owner.target
        for typ in self.active_effects:
            for effect in self.active_effects[typ]:
                effect.source = self.parent

    def apply(self, effect_type:str):
        print(f"Applying {effect_type}s\n")
        for condition in self.active_effects[effect_type]:
            self.target.conditions.add(condition)

def generate_premades():
    with open("weapon_enchantments.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            current = Weapon_Enchantment()
            current.id = row["enchantment_id"]
            for effect_type in current.active_effects:
                if row[effect_type] is not None and row[effect_type] != '':
                    new:Condition = conditions.dict[row[effect_type]](current)
                    current.active_effects[effect_type] = [new]
            TOME[current.id] = current
        file.close()

generate_premades()

#print(TOME)
    