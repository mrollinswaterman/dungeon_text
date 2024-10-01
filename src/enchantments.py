#Weapon+Armor enchantments file
import csv, random
import global_commands
from game_object import Game_Object
from equipment import Equipment
from condition import Condition
import conditions

TOME = {}

class Weapon_Enchantment():

    def __init__(self, parent:Game_Object | Equipment=None) -> None:
        self.parent = parent
        self.id = "Weapon Enchatment"
        self.cost = 1
        self.proc_chance:float = 1.0

        self.active_conditions:dict[str, list[Condition]] = {
            "on_hit":[],
            "on_attack":[],
            "on_miss":[]
        }

    @property
    def target(self) -> Game_Object | None:
        match self.parent:
            case Game_Object(): return self.parent.target
            case Equipment(): return self.parent.owner.target

    def initialize(self, object:Game_Object | Equipment):
        self.parent = object
        for typ in self.active_conditions:
            for condition in self.active_conditions[typ]:
                condition.source = self.parent

    def apply(self, effect_type:str):
        for condition in self.active_conditions[effect_type]:
            if global_commands.probability(self.proc_chance*100):
                self.target.conditions.add(condition)

def generate_premades():
    with open("weapon_enchantments.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            current = Weapon_Enchantment()
            current.id = row["enchantment_id"]
            if row["proc_chance"] is not None and row["proc_chance"] != "": current.proc_chance = row["proc_chance"]
            for effect_type in current.active_conditions:
                if row[effect_type] is not None and row[effect_type] != '':
                    new:Condition = conditions.dict[row[effect_type]](current)
                    current.active_conditions[effect_type] = [new]
            TOME[current.id] = current
        file.close()

generate_premades()
    